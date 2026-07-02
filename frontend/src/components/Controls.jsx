import React from 'react';

export function ToggleSwitch({ label, isOn, onToggle, idKey = null }) {
  const toggleCls = isOn ? "toggle-on" : "toggle-off";
  const dotCls = isOn ? "toggle-dot-on" : "toggle-dot-off";

  return (
    <div className="toggle-switch" id={idKey} onClick={onToggle}>
      <span className="toggle-label">{label}</span>
      <div className="toggle-controls">
        <span className="toggle-state-text">{isOn ? "ON" : "OFF"}</span>
        <div className={`toggle-track ${toggleCls}`}>
          <div className={`toggle-dot ${dotCls}`}></div>
        </div>
      </div>
    </div>
  );
}

export function MetalSwitch({ label, isOn, onToggle, idKey = null }) {
  const toggleCls = isOn ? "metal-switch-on" : "metal-switch-off";

  return (
    <div className="metal-switch-container" id={idKey} onClick={onToggle}>
      <div className="metal-switch-body">
        <div className="metal-switch-base">
          <div className="metal-switch-neck">
            <div className={`metal-switch-lever ${toggleCls}`}></div>
          </div>
        </div>
      </div>
      <span className="metal-switch-label">{label}</span>
    </div>
  );
}

export function CompactToggle({ label, isOn, onToggle, idKey = null }) {
  const bg = isOn ? "#4caf50" : "#f44336";
  const align = isOn ? "flex-end" : "flex-start";
  return (
    <div 
      id={idKey} 
      onClick={onToggle}
      style={{
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        background: '#222', 
        padding: '4px 8px', 
        borderRadius: '4px',
        border: '1px solid #444',
        cursor: 'pointer',
        fontSize: '11px',
        width: '100%',
        boxSizing: 'border-box'
      }}
    >
      <span style={{ color: '#ddd', flex: 1, textAlign: 'left', paddingRight: '10px' }}>{label}</span>
      <div style={{
        width: '32px', height: '16px', borderRadius: '8px', background: '#111', 
        display: 'flex', alignItems: 'center', padding: '2px', boxSizing: 'border-box',
        justifyContent: align
      }}>
        <div style={{
          width: '12px', height: '12px', borderRadius: '50%', background: bg,
          boxShadow: '0 0 4px rgba(0,0,0,0.5)'
        }}></div>
      </div>
    </div>
  );
}

