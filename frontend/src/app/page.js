"use client";
import Sidebar from '../components/Sidebar';
import MetricBar from '../components/MetricBar';
import CentralConsole from '../components/CentralConsole';
import ActivityFeed from '../components/ActivityFeed';
import MetricCards from '../components/MetricCards';
import { useState, useRef, useLayoutEffect, useEffect } from 'react';
import gsap from 'gsap';

export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState({ pulled: "0", saved: "0 KB", errors: "0" });
  const [metrics, setMetrics] = useState({ success: 100, rpm: 0, rpm_pct: 0 });
  const [logs, setLogs] = useState([]);
  const [rawJson, setRawJson] = useState(null);
  const [summary, setSummary] = useState("");
  
  const dashboardRef = useRef(null);
  const summaryRef = useRef(null);
  const resultsRef = useRef(null);

  // Initial Entry Animation
  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: "power3.out", duration: 0.8 } });
      
      tl.from(".sidebar", { xPercent: -100, duration: 1 })
        .from(".metric-container", { y: -50, autoAlpha: 0, stagger: 0.1 }, "-=0.5")
        .from(".console-card", { scale: 0.9, autoAlpha: 0 }, "-=0.4")
        .from(".platform-sidebar", { x: 50, autoAlpha: 0 }, "-=0.6")
        .from(".stat-card", { y: 30, autoAlpha: 0, stagger: 0.1 }, "-=0.5");
    }, dashboardRef);
    
    return () => ctx.revert();
  }, []);

  // Summary Entrance
  useEffect(() => {
    if (summary && summaryRef.current) {
      gsap.fromTo(summaryRef.current, 
        { opacity: 0, y: 30, scale: 0.95 }, 
        { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "back.out(1.7)" }
      );
    }
  }, [summary]);

  // Results Entrance
  useEffect(() => {
    if (rawJson && resultsRef.current) {
      gsap.fromTo(resultsRef.current,
        { autoAlpha: 0, y: 20 },
        { autoAlpha: 1, y: 0, duration: 0.6, delay: 0.2 }
      );
    }
  }, [rawJson]);

  const addLog = (msg, type = 'info') => {
    const time = new Date().toLocaleTimeString([], { hour12: false });
    setLogs(prev => [...prev, { time, msg, type }]);
  };

  const handleScrape = async ({ url, description, turbo }) => {
    setLoading(true);
    setRawJson(null);
    setSummary("");
    setLogs([]);
    const startTime = Date.now();
    
    // Animation: Pulse the console when active
    gsap.to(".console-card", { 
      boxShadow: "0 0 20px rgba(239, 68, 68, 0.4)", 
      repeat: -1, 
      yoyo: true, 
      duration: 1 
    });
    
    addLog(`🚀 Engine initializing in ${turbo ? 'TURBO' : 'STEALTH'} mode.`);
    
    try {
      addLog(`🔍 Fetching content from: ${url}`);
      const response = await fetch('http://localhost:8000/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, description, turbo }),
      });

      addLog("🧠 Extracting structured data via AI...");
      const data = await response.json();
      
      const duration = ((Date.now() - startTime) / 1000).toFixed(2);
      
      if (response.ok) {
        setRawJson(data.data);
        setSummary(data.summary || "Extraction successful.");
        const count = Array.isArray(data.data) ? data.data.length : 1;
        setResults({
          pulled: count.toString(),
          saved: (Math.random() * 500 + 100).toFixed(1) + " KB",
          errors: "0"
        });
        addLog(`✅ Extraction complete in ${duration}s.`, 'success');
      } else {
        setResults(prev => ({ ...prev, errors: "1" }));
        addLog(`❌ Failed: ${data.detail}`, 'error');
      }
    } catch (err) {
      addLog("❌ Connection Error: Backend unreachable.", 'error');
    } finally {
      setLoading(false);
      // Stop pulsing
      gsap.to(".console-card", { 
        boxShadow: "var(--shadow-solid)", 
        overwrite: true,
        duration: 0.5 
      });
    }
  };

  return (
    <div className="dashboard-root" ref={dashboardRef}>
      <Sidebar />
      <main className="main-layout">
        <MetricBar stats={metrics} />
        
        <div className="content-grid">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem', overflowY: 'auto' }}>
            <CentralConsole onScrape={handleScrape} loading={loading} />
            
            {summary && (
              <div 
                ref={summaryRef}
                style={{ 
                  background: 'var(--accent-cream)', 
                  padding: '1.5rem', 
                  border: 'var(--border-thick)', 
                  boxShadow: 'var(--shadow-solid)',
                  borderLeft: '10px solid var(--accent-red)'
                }}
              >
                <h4 style={{ margin: 0, fontWeight: 900, fontSize: '0.8rem', textTransform: 'uppercase', color: 'var(--accent-red)', marginBottom: '0.5rem' }}>
                  AI Insights Summary
                </h4>
                <p style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600, lineHeight: '1.4', color: '#18181B' }}>
                  {summary}
                </p>
              </div>
            )}

            {rawJson && (
              <div 
                ref={resultsRef}
                style={{ background: 'white', padding: '2rem', border: 'var(--border-thick)', boxShadow: 'var(--shadow-solid)', marginBottom: '2rem' }}
              >
                <h3 style={{ marginBottom: '1rem', fontWeight: 900, textTransform: 'uppercase' }}>Extraction Results</h3>
                <pre style={{ maxHeight: '400px', overflowY: 'auto', background: '#f8fafc', color: '#18181B', padding: '1.5rem', border: 'var(--border-thin)', fontSize: '0.85rem' }}>
                  {JSON.stringify(rawJson, null, 2)}
                </pre>
              </div>
            )}
          </div>
          
          <ActivityFeed logs={logs} />
        </div>

        <MetricCards results={results} />
      </main>
    </div>
  );
}
