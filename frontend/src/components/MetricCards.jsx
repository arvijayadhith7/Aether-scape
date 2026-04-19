"use client";

const StatCard = ({ label, value, bg, color }) => (
  <div className="stat-card" style={{ backgroundColor: bg, color: color }}>
    <div style={{ fontSize: '0.9rem', fontWeight: 900, textTransform: 'uppercase', opacity: 0.8 }}>{label}</div>
    <div className="stat-val">{value}</div>
  </div>
);

const MetricCards = ({ results = {} }) => {
  return (
    <div className="stats-row">
      <StatCard 
        label="Records Pulled" 
        value={results.pulled || "0"} 
        bg="#8b5cf6" 
        color="white" 
      />
      <StatCard 
        label="Bandwidth Savvy" 
        value={results.saved || "0 KB"} 
        bg="#dbeafe" 
        color="#1d4ed8" 
      />
      <StatCard 
        label="Extraction Errors" 
        value={results.errors || "0"} 
        bg="#ffe4e6" 
        color="#be123c" 
      />
    </div>
  );
};

export default MetricCards;
