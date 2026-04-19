"use client";
import { useEffect, useRef } from 'react';
import gsap from 'gsap';

const ActivityFeed = ({ logs = [] }) => {
  const scrollRef = useRef(null);
  const logsRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
    
    // Animate the last log entry appearing
    const lastLog = logsRef.current?.lastElementChild;
    if (lastLog) {
      gsap.fromTo(lastLog, 
        { autoAlpha: 0, x: 20 }, 
        { autoAlpha: 1, x: 0, duration: 0.4, ease: "power2.out" }
      );
    }
  }, [logs]);

  return (
    <div className="platform-sidebar" style={{ display: 'flex', flexDirection: 'column' }}>
      <div style={{ fontWeight: 900, fontSize: '1rem', textTransform: 'uppercase', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span style={{ color: 'var(--accent-red)' }}>●</span> LIVE ACTIVITY LOG
      </div>
      
      <div 
        ref={scrollRef}
        className="log-container" 
        style={{ 
          flex: 1, 
          background: 'white', 
          border: 'var(--border-thin)', 
          padding: '1rem', 
          fontSize: '0.8rem', 
          fontFamily: "'Fira Code', monospace",
          overflowY: 'auto',
          maxHeight: '400px'
        }}
      >
        <div ref={logsRef}>
          {logs.length === 0 ? (
            <div style={{ color: 'var(--text-muted)' }}>Waiting for engine initialization...</div>
          ) : (
            logs.map((log, i) => (
              <div key={i} style={{ marginBottom: '0.5rem', display: 'flex', gap: '8px' }}>
                <span style={{ color: '#888' }}>[{log.time}]</span>
                <span style={{ color: log.type === 'error' ? 'var(--accent-red)' : 'var(--text-main)' }}>
                  {log.msg}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
      
      <div style={{ marginTop: '1rem', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)' }}>
        ENGINE STATUS: {logs.length > 0 ? 'ACTIVE' : 'IDLE'}
      </div>
    </div>
  );
};

export default ActivityFeed;
