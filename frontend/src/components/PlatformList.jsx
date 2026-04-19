"use client";

const PlatformItem = ({ name, records, rate, logoColor }) => (
  <div className="platform-item">
    <div style={{ width: 32, height: 32, backgroundColor: logoColor, borderRadius: 8 }}></div>
    <div className="platform-info">
      <div style={{ fontWeight: 700, fontSize: '0.85rem' }}>{name}</div>
      <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>{records}</div>
    </div>
    <div style={{ fontWeight: 700, fontSize: '0.85rem' }}>{rate}</div>
  </div>
);

const PlatformList = () => {
  return (
    <div className="platform-sidebar">
      <div style={{ fontWeight: 700, fontSize: '0.9rem' }}>Other platforms</div>
      <input 
        className="field-input" 
        style={{ marginTop: '1rem', padding: '0.5rem' }} 
        placeholder="Search..." 
      />
      <div className="platform-list">
        <PlatformItem name="Foursquare" records="11k" rate="3k/h" logoColor="#4ade80" />
        <PlatformItem name="Yelp" records="2.5k" rate="500/h" logoColor="#f87171" />
        <PlatformItem name="Open Table" records="32k" rate="500/h" logoColor="#fb923c" />
        <PlatformItem name="Tripadvisor" records="10k" rate="1.5k/h" logoColor="#60a5fa" />
        <PlatformItem name="Zomato" records="11k" rate="1.3k/h" logoColor="#f43f5e" />
      </div>
    </div>
  );
};

export default PlatformList;
