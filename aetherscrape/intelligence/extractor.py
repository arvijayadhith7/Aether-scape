import os
import json
from typing import Type, TypeVar, Optional, List, Any, Protocol
from pydantic import BaseModel, Field
import google.generativeai as genai
from openai import OpenAI
from bs4 import BeautifulSoup
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

T = TypeVar("T", bound=BaseModel)

class LLMProvider(Protocol):
    async def generate_json(self, prompt: str, schema: Type[T]) -> dict:
        ...
    async def generate_text(self, prompt: str) -> str:
        ...

class GeminiProvider:
    def __init__(self, api_key: str, model_name: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    async def generate_json(self, prompt: str, schema: Type[T]) -> dict:
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            ),
        )
        return json.loads(response.text)

    async def generate_text(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

class NVIDIAProvider:
    def __init__(self, api_key: str, model_name: str):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        self.model_name = model_name

    async def generate_json(self, prompt: str, schema: Type[T]) -> dict:
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        return json.loads(completion.choices[0].message.content)

    async def generate_text(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return completion.choices[0].message.content

class SemanticExtractor:
    """Uses LLMs to intelligently extract structured data from raw HTML/Markdown."""
    
    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None, model_name: Optional[str] = None):
        self.provider_type = provider or os.getenv("LLM_PROVIDER", "gemini")
        self.api_key = api_key
        self.overridden_model = model_name

    def _get_model(self, tier: str = "quality") -> str:
        """Determines the model to use based on performance tier."""
        if self.overridden_model:
            return self.overridden_model
            
        if self.provider_type == "nvidia":
            # Quality: 405B, Fast: 8B
            if tier == "fast":
                return os.getenv("NVIDIA_FAST_MODEL", "meta/llama-3.1-8b-instruct")
            return os.getenv("NVIDIA_QUALITY_MODEL", "meta/llama-3.1-405b-instruct")
        else:
            # Gemini tiers
            if tier == "fast":
                return "gemini-1.5-flash-8b"
            return "gemini-1.5-flash"

    def _get_provider(self, tier: str = "quality") -> LLMProvider:
        model = self._get_model(tier)
        if self.provider_type == "nvidia":
            key = self.api_key or os.getenv("NVIDIA_API_KEY")
            return NVIDIAProvider(key, model)
        else:
            key = self.api_key or os.getenv("GOOGLE_API_KEY")
            return GeminiProvider(key, model)

    def _clean_html(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)

    async def extract(self, html: str, schema: Type[T], description: str = "", tier: str = "quality") -> T:
        """Extracts data with optional performance tier (fast/quality)."""
        clean_text = self._clean_html(html)
        context_text = clean_text[:100000]

        prompt = f"""
        Extract valid JSON matching this schema: {schema.model_json_schema()}
        Goal: {description}
        Content:
        ---
        {context_text}
        ---
        """
        
        provider = self._get_provider(tier)
        try:
            data = await provider.generate_json(prompt, schema)
            return schema.model_validate(data)
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            raise

    async def summarize(self, data: Any, tier: str = "fast") -> str:
        """Generates a brief summary of the extracted data."""
        prompt = f"Summarize this extracted data in 2-3 concise, professional sentences for a dashboard highlight. Data: {json.dumps(data)}"
        provider = self._get_provider(tier)
        try:
            return await provider.generate_text(prompt)
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return "Summary unavailable."
