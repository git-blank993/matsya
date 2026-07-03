import React from 'react';
import { fmtVal } from '../utils';

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

export function Toggle3Pos({ labelTop, labelBottom, value, onToggle, idKey = null }) {
  // value: -1 (down), 0 (center), 1 (up)
  let posClass = "pos-center";
  if (value === 1) posClass = "pos-up";
  if (value === -1) posClass = "pos-down";

  return (
    <div className="toggle-3pos-container" id={idKey}>
      <div className="toggle-3pos-label">{labelTop}</div>
      <div className="toggle-3pos-body" onClick={onToggle}>
        <div className="metal-switch-base">
          <div className="metal-switch-neck">
            <div className={`metal-switch-lever ${posClass}`}></div>
          </div>
        </div>
      </div>
      <div className="toggle-3pos-label">{labelBottom}</div>
    </div>
  );
}

export function AlarmIndicator({ label, isOn, idKey = null }) {
  return (
    <div className={`alarm-indicator ${isOn ? 'on' : 'off'}`} id={idKey}>
      <div className="alarm-indicator-text">{label}</div>
    </div>
  );
}

export function Buzzer({ label, isOn, idKey = null }) {
  return (
    <div className={`buzzer-container ${isOn ? 'ringing' : ''}`} id={idKey}>
      <div className="buzzer-label">{label}</div>
      <div className="buzzer-speaker">
        <div className="buzzer-grill"></div>
        <div className="buzzer-grill"></div>
        <div className="buzzer-grill"></div>
      </div>
    </div>
  );
}

// Custom Hardware Components for New Layouts

export function RotarySwitch({ label, value, options, onChange, idKey = null }) {
  // Simple representation of a rotary switch
  return (
    <div className="rotary-switch-container" id={idKey} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '8px' }}>
      <div style={{ fontSize: '10px', color: '#000', marginBottom: '4px', fontWeight: 'bold' }}>{label}</div>
      <div style={{ width: '40px', height: '40px', background: '#ccc', borderRadius: '4px', border: '2px solid #888', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }} onClick={onChange}>
        <div style={{ width: '30px', height: '30px', borderRadius: '50%', background: '#333', position: 'relative', transform: `rotate(${value === 1 ? -45 : 45}deg)`, transition: 'transform 0.2s' }}>
          <div style={{ width: '4px', height: '15px', background: '#fff', position: 'absolute', top: '2px', left: '13px', borderRadius: '2px' }}></div>
        </div>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', width: '40px', marginTop: '4px', fontSize: '10px', color: '#000' }}>
        <span>1</span><span>2</span>
      </div>
    </div>
  );
}

export function CircuitBreaker({ labelTop, labelBottom, isOn, onToggle, idKey = null }) {
  return (
    <div className="circuit-breaker" id={idKey} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '4px' }}>
      {labelTop && <div style={{ fontSize: '10px', color: '#000', marginBottom: '4px', fontWeight: 'bold', whiteSpace: 'pre-wrap', textAlign: 'center' }}>{labelTop}</div>}
      <div style={{ width: '30px', height: '40px', background: '#ddd', border: '1px solid #999', borderRadius: '2px', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', boxShadow: 'inset 0 0 4px #aaa' }} onClick={onToggle}>
        <div style={{ width: '20px', height: '16px', background: isOn ? '#444' : '#222', border: '1px solid #111', borderRadius: '2px', transform: isOn ? 'translateY(-6px)' : 'translateY(6px)', transition: 'all 0.1s' }}></div>
      </div>
      {labelBottom && <div style={{ fontSize: '10px', color: '#000', marginTop: '4px', fontWeight: 'bold', whiteSpace: 'pre-wrap', textAlign: 'center' }}>{labelBottom}</div>}
    </div>
  );
}

export function LcdScreen({ idKey = null }) {
  return (
    <div id={idKey} style={{ width: '180px', height: '180px', background: '#aaa', border: '2px solid #888', borderRadius: '8px', padding: '10px', display: 'flex', flexDirection: 'column', boxShadow: '0 4px 8px rgba(0,0,0,0.2)' }}>
      <div style={{ flex: 1, background: '#111', borderRadius: '4px', border: '2px solid #333' }}></div>
      <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '8px' }}>
        <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#666' }}></div>
        <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#666' }}></div>
        <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#666' }}></div>
        <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#666' }}></div>
      </div>
    </div>
  );
}

export function BlackPushButton({ labelTop, labelBottom, onClick, idKey = null }) {
  return (
    <div id={idKey} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '4px' }}>
      {labelTop && <div style={{ fontSize: '9px', color: '#000', marginBottom: '2px', fontWeight: 'bold' }}>{labelTop}</div>}
      <div style={{ width: '24px', height: '16px', background: '#222', border: '2px solid #000', borderRadius: '2px', cursor: 'pointer', boxShadow: '0 2px 2px rgba(0,0,0,0.3)' }} onClick={onClick}></div>
      {labelBottom && <div style={{ fontSize: '9px', color: '#000', marginTop: '2px', fontWeight: 'bold' }}>{labelBottom}</div>}
    </div>
  );
}

export function RoundPushButton({ labelTop, labelBottom, onClick, idKey = null }) {
  return (
    <div id={idKey} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '4px' }}>
      {labelTop && <div style={{ fontSize: '9px', color: '#000', marginBottom: '4px', fontWeight: 'bold', textAlign: 'center', whiteSpace: 'pre-wrap' }}>{labelTop}</div>}
      <div style={{ width: '24px', height: '24px', borderRadius: '50%', background: '#111', border: '3px solid #888', cursor: 'pointer', boxShadow: '0 2px 4px rgba(0,0,0,0.3)' }} onClick={onClick}></div>
      {labelBottom && <div style={{ fontSize: '9px', color: '#000', marginTop: '4px', fontWeight: 'bold', textAlign: 'center', whiteSpace: 'pre-wrap' }}>{labelBottom}</div>}
    </div>
  );
}

export function MastervoltDisplay({ label, value, idKey = null }) {
  return (
    <div className="battman-wrapper" id={idKey}>
      <div className="battman-gauge">
        <div className="battman-brand">MASTERVOLT</div>
        <div className="battman-lcd">{fmtVal(value)}</div>
        <div className="battman-btn-row">
          <div className="battman-btn battman-arrow">◀</div>
          <div className="battman-btn battman-menu">MENU</div>
          <div className="battman-btn battman-arrow">▶</div>
        </div>
        <div className="battman-model">BattMan Pro</div>
      </div>
      <div className="tape-label bottom-label">{label}</div>
    </div>
  );
}

export function YellowLedDisplay({ label, value, unit="k ohm", idKey = null }) {
  return (
    <div className="insulation-wrapper" id={idKey}>
      <div className="iso-yellow-box">
        <div className="iso-led-row">
          <div className="iso-led"></div>
          <div className="iso-led"></div>
          <div className="iso-led"></div>
        </div>
        <div className="iso-lcd">{fmtVal(value)}</div>
        <div className="iso-btn-row">
          <div className="iso-btn"></div>
          <div className="iso-btn"></div>
          <div className="iso-btn"></div>
        </div>
      </div>
      <div className="tape-label bottom-label">{label}</div>
      <span className="tape-label side-label">{unit}</span>
    </div>
  );
}

export function DigitalVoltageDisplay({ label, value, unit="V", idKey = null }) {
  return (
    <div className="red-led-wrapper" id={idKey}>
      <div className="red-led-lcd">{fmtVal(value)}</div>
      <div className="tape-label bottom-label">{label}</div>
      <span className="tape-label side-label">{unit}</span>
    </div>
  );
}
