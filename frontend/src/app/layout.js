import "./globals.css";

export const metadata = {
  title: "AetherScape | Intelligent Web Research",
  description: "Bypass layout changes and anti-bot systems with AI-powered scraping.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&family=Fira+Code&display=swap" rel="stylesheet" />
      </head>
      <body>{children}</body>
    </html>
  );
}
