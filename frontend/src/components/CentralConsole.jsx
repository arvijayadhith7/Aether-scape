"use client";
import { useState, useRef } from 'react';
import gsap from 'gsap';

const CentralConsole = ({ onScrape, loading }) => {
  const [url, setUrl] = useState('');
  const [description, setDescription] = useState('');
  const [turbo, setTurbo] = useState(true);
  
  const btnRef = useRef(null);
  const cardRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Bounce effect on submit
    gsap.to(cardRef.current, { scale: 0.98, duration: 0.1, yoyo: true, repeat: 1 });
    onScrape({ url, description, turbo });
  };

  const onBtnEnter = () => {
    gsap.to(btnRef.current, { scale: 1.05, duration: 0.3, ease: "power2.out" });
  };

  const onBtnLeave = () => {
    gsap.to(btnRef.current, { scale: 1, duration: 0.3, ease: "power2.out" });
  };

  return (
    <div className="console-card" ref={cardRef}>
      <div className="platform-logo">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#18181B', fontWeight: '900', fontSize: '2.5rem' }}>
          AETHERSCAPE
        </div>
      </div>
      
      <form onSubmit={handleSubmit} style={{ width: '100%' }}>
        <div className="input-grid" style={{ gridTemplateColumns: '1fr' }}>
          <div className="field-group">
            <label>Target Website URL</label>
            <input 
              className="field-input" 
              placeholder="https://example.com/data" 
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
          </div>
          <div className="field-group">
            <label>Extraction Prompt / Description</label>
            <input 
              className="field-input" 
              placeholder="e.g. Find all course names and prices..." 
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>
        </div>

        <div style={{ marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', fontWeight: 900, fontSize: '0.8rem' }}>
            <input 
              type="checkbox" 
              checked={turbo} 
              onChange={(e) => setTurbo(e.target.checked)}
              style={{ width: '20px', height: '20px', accentColor: 'var(--accent-red)', border: 'var(--border-thick)' }}
            />
            TURBO PERFORMANCE MODE (FAST EXTRACTION)
          </label>
        </div>

        <div className="action-buttons">
          <button 
            ref={btnRef}
            onMouseEnter={onBtnEnter}
            onMouseLeave={onBtnLeave}
            type="submit" 
            className="btn-primary" 
            disabled={loading}
          >
            {loading ? 'SCRAPING...' : 'EXECUTE SMART SCRAPE'}
          </button>
          <button type="button" className="btn-outline">DOWNLOAD JSON</button>
        </div>
      </form>
    </div>
  );
};

export default CentralConsole;
