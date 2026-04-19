"use client";
import { useEffect, useRef } from 'react';
import gsap from 'gsap';

const MetricItem = ({ label, value, color, percent }) => {
  const barRef = useRef(null);

  useEffect(() => {
    if (barRef.current) {
      gsap.to(barRef.current, {
        width: `${percent || 0}%`,
        duration: 1,
        ease: "power2.out"
      });
    }
  }, [percent]);

  return (
    <div className="metric-item">
      <div className="metric-header">
        <span>{label}</span>
        <span>{value}</span>
      </div>
      <div className="progress-bar">
        <div 
          ref={barRef}
          className="progress-fill" 
          style={{ width: `0%`, backgroundColor: color }}
        ></div>
      </div>
    </div>
  );
};

const MetricBar = ({ stats = {} }) => {
  return (
    <div className="metric-container">
      <MetricItem 
        label="Success Rate" 
        value={`${stats.success || 100}%`} 
        color="#22c55e" 
        percent={stats.success || 100}
      />
      <MetricItem 
        label="Throughput (RPM)" 
        value={`${stats.rpm || 0}`} 
        color="var(--accent-blue)" 
        percent={stats.rpm_pct || 0}
      />
      <MetricItem 
        label="Proxy Health" 
        value="98.2%" 
        color="var(--accent-purple)" 
        percent={98}
      />
    </div>
  );
};

export default MetricBar;
