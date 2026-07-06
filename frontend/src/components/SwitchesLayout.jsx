import React from 'react';
import { 
  MetalSwitch, 
  RotarySwitch, 
  KnobSwitch,
  CircuitBreaker, 
  LcdScreen, 
  BlackPushButton, 
  RoundPushButton, 
  MastervoltDisplay, 
  YellowLedDisplay, 
  DigitalVoltageDisplay,
  Buzzer
} from './Controls';

// Port Side Layout
export function SwitchesPLayout({ appState, apiCall }) {
  const sw = appState.switches?.p || {};
  const sw_s = appState.switches?.s || {}; // For STBD SDW
  
  const tc = (labelTop, labelBottom, isOn, stateKey, customPath = null) => (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '4px' }}>
      {labelTop && <div style={{ fontSize: '12px', color: '#000', fontWeight: 'bold', marginBottom: '4px', whiteSpace: 'pre-wrap', textAlign: 'center' }}>{labelTop}</div>}
      <MetalSwitch 
        isOn={isOn} 
        onToggle={() => apiCall(customPath || `/api/toggle/switches.p.${stateKey}`)} 
        idKey={`tog-p-${stateKey}`} 
        label="" 
      />
      {labelBottom && <div style={{ fontSize: '12px', color: '#000', fontWeight: 'bold', marginTop: '4px', whiteSpace: 'pre-wrap', textAlign: 'center' }}>{labelBottom}</div>}
    </div>
  );

  return (
    <div className="main-content-wrapper" style={{ padding: '8px', overflowY: 'auto', background: 'var(--color-bg)' }}>
      <div style={{ width: '100%', boxSizing: 'border-box' }}>
        
        <div style={{ width: '100%', background: '#ccc', border: '1px solid #aaa', padding: '20px', borderRadius: '4px', position: 'relative', marginBottom: '20px', boxSizing: 'border-box' }}>
          
          {/* Top rotary switches — centered */}
          <div style={{ display: 'flex', justifyContent: 'center', gap: '60px' }}>
            <RotarySwitch label="AB P" value={sw.ab_p ? 2 : 1} onChange={() => apiCall('/api/toggle/switches.p.ab_p')} />
            <RotarySwitch label="E_BATT_P" value={sw.e_batts ? 2 : 1} onChange={() => apiCall('/api/toggle/switches.p.e_batts')} />
          </div>

          {/* MCB + displays row — centered */}
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-start', gap: '30px', marginTop: '10px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <div style={{ display: 'flex', gap: '5px' }}>
                <CircuitBreaker isOn={sw.ub_p_mcb} onToggle={() => apiCall('/api/toggle/switches.p.ub_p_mcb')} />
                <CircuitBreaker isOn={sw.ub_p_mcb2} onToggle={() => apiCall('/api/toggle/switches.p.ub_p_mcb2')} />
              </div>
              <div style={{ fontSize: '10px', color: '#000', fontWeight: 'bold', background: '#ccc', border: '1px solid #aaa', padding: '1px 4px', marginTop: '4px' }}>UB_P MCB</div>
            </div>
            <DigitalVoltageDisplay label="UB P VOLTAGE" value={sw.ub_voltage} />
            <MastervoltDisplay label="EB P STATUS" value={sw.eb_b_status} />
            <YellowLedDisplay label="EB P INSULATION" value={sw.ib_insulation} />
          </div>

          {/* LCD + switch columns — centered */}
          <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px', gap: '30px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', paddingTop: '10px' }}>
              <div style={{ display: 'flex', gap: '20px' }}>
                <BlackPushButton labelTop="NC" labelBottom="PDE_P_CLR_RST" onClick={() => {}} />
                <BlackPushButton labelTop="NO" labelBottom="DIM_P_RESET" onClick={() => {}} />
              </div>
              <div style={{ display: 'flex', gap: '15px' }}>
                {tc("AB_P_BMS", "", sw.ab_p_bms, "ab_p_bms")}
                {tc("AB_P", "", sw.ab_p_power, "ab_p_power")}
                {tc("PDE_P_DIM", "", sw.pde_p_dim, "pde_p_dim")}
              </div>
              <div style={{ display: 'flex', gap: '15px' }}>
                {tc("IDE1_P", "", sw.ide_p_1, "ide_p_1")}
                {tc("IDE2", "", sw.ide_2, "ide_2")}
                {tc("SPARE 2", "Keep in\n'ON'", sw.spare_2, "spare_2")}
              </div>
              <div style={{ display: 'flex', gap: '15px' }}>
                {tc("", "", sw.p_x1, "p_x1")}
                {tc("", "", sw.p_x2, "p_x2")}
                {tc("", "", sw.p_x3, "p_x3")}
              </div>
            </div>
            <LcdScreen />
          </div>

          {/* Bottom switch row — centered */}
          <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '10px', marginTop: '10px' }}>
            {tc("PDE-P\n24V CONTROL", "SECONDARY\nPRIMARY", sw.pde_p_24v, "pde_p_24v")}
            {tc("MB_P_BMS", "ON", sw.mb_p_bms, "mb_p_bms")}
            {tc("MB_P_1", "ON", sw.mb_1, "mb_1")}
            {tc("MB_P_2", "ON", sw.mb_2, "mb_2")}
            {tc("MB_P_3", "ON", sw.mb_3, "mb_3")}
            {tc("MB_P_4", "ON", sw.mb_4, "mb_4")}
            {tc("MB_P_5", "ON", sw.mb_5, "mb_5")}
            {tc("PDE-P-OLR", "STATUS", sw.pde_p_olr, "pde_p_olr")}
            {tc("PDE_P_148", "IN STATUS", sw.pde_p_148, "pde_p_148")}
          </div>

          <div style={{ marginTop: '30px', background: '#ddd', border: '1px solid #aaa', padding: '15px', borderRadius: '4px' }}>
            <div style={{ fontSize: '14px', fontWeight: 'bold', color: '#000', marginBottom: '15px', textAlign: 'center' }}>SERVICE DROP WEIGHT SWITCHES</div>
            <div style={{ display: 'flex', gap: '50px', justifyContent: 'center' }}>
              <div>
                <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#000', marginBottom: '10px' }}>PORT SIDE-SDW</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                  {[1,2,3,4,5].map(i => tc(`SDWP_${i}\nON`, "OFF", sw[`port_side_sdw_${i}`], `port_side_sdw_${i}`))}
                </div>
              </div>
              <div>
                <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#000', marginBottom: '10px' }}>STBD_SIDE-SDW</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                  {[1,2,3,4,5].map(i => tc(`SDWS_${i}\nON`, "OFF", sw_s[`starboard_side_sdw_${i}`], `starboard_side_sdw_${i}`, `/api/toggle/switches.s.starboard_side_sdw_${i}`))}
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

// Starboard Side Layout
export function SwitchesSLayout({ appState, apiCall }) {
  const sw = appState.switches?.s || {};
  
  const tc = (labelTop, labelBottom, isOn, stateKey) => (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '4px' }}>
      {labelTop && <div style={{ fontSize: '12px', color: '#000', fontWeight: 'bold', marginBottom: '4px', whiteSpace: 'pre-wrap', textAlign: 'center' }}>{labelTop}</div>}
      <MetalSwitch 
        isOn={isOn} 
        onToggle={() => apiCall(`/api/toggle/switches.s.${stateKey}`)} 
        idKey={`tog-s-${stateKey}`} 
        label="" 
      />
      {labelBottom && <div style={{ fontSize: '12px', color: '#000', fontWeight: 'bold', marginTop: '4px', whiteSpace: 'pre-wrap', textAlign: 'center' }}>{labelBottom}</div>}
    </div>
  );

  return (
    <div className="main-content-wrapper" style={{ padding: '8px', overflowY: 'auto', background: 'var(--color-bg)' }}>
      <div style={{ width: '100%', boxSizing: 'border-box' }}>
        
        <div style={{ width: '100%', background: '#ccc', border: '1px solid #aaa', padding: '20px', borderRadius: '4px', position: 'relative', marginBottom: '20px', boxSizing: 'border-box' }}>
          
          {/* Top rotary switches — centered */}
          <div style={{ display: 'flex', justifyContent: 'center', gap: '60px' }}>
            <RotarySwitch label="AB S" value={sw.ab_s ? 2 : 1} onChange={() => apiCall('/api/toggle/switches.s.ab_s')} />
            <RotarySwitch label="E_BATT_S" value={sw.e_batts ? 2 : 1} onChange={() => apiCall('/api/toggle/switches.s.e_batts')} />
          </div>

          {/* MCB + displays row — centered */}
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-start', gap: '30px', marginTop: '10px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <div style={{ display: 'flex', gap: '5px' }}>
                <CircuitBreaker isOn={sw.ub_s_mcb} onToggle={() => apiCall('/api/toggle/switches.s.ub_s_mcb')} />
                <CircuitBreaker isOn={sw.ub_s_mcb2} onToggle={() => apiCall('/api/toggle/switches.s.ub_s_mcb2')} />
              </div>
              <div style={{ fontSize: '10px', color: '#000', fontWeight: 'bold', background: '#ccc', border: '1px solid #aaa', padding: '1px 4px', marginTop: '4px' }}>UB_S MCB</div>
            </div>
            <DigitalVoltageDisplay label="UB S VOLTAGE" value={sw.ub_voltage} />
            <MastervoltDisplay label="EB S STATUS" value={sw.eb_b_status} />
            <YellowLedDisplay label="EB S INSULATION" value={sw.ib_insulation} />
          </div>
          {/* LCD + switch columns — centered */}
          <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px', gap: '40px' }}>
            <LcdScreen />
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div style={{ display: 'flex', gap: '15px' }}>
                {tc("DIM", "OFF", sw.dim, "dim")}
              </div>
              <div style={{ display: 'flex', gap: '15px' }}>
                {tc("OFF", "", sw.s_off1, "s_off1")}
                {tc("OFF", "", sw.s_off2, "s_off2")}
                {tc("OFF", "", sw.s_off3, "s_off3")}
              </div>
              <div style={{ display: 'flex', gap: '15px' }}>
                {tc("SPARE2", "Keep in\n'24'", sw.spare_2, "spare_2")}
                {tc("IDE2", "", sw.ide_2, "ide_2")}
                {tc("IDE1_S", "", sw.ide_1_s, "ide_1_s")}
              </div>
              <div style={{ display: 'flex', gap: '15px' }}>
                {tc("", "", sw.s_x1, "s_x1")}
                {tc("", "", sw.s_x2, "s_x2")}
                {tc("", "", sw.s_x3, "s_x3")}
              </div>
            </div>
          </div>

          {/* Bottom switch row — centered */}
          <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '10px', marginTop: '10px' }}>
            {tc("SECONDARY", "PRIMARY\n24V CONTROL", sw.pde_s_24v, "pde_s_24v")}
            {tc("ON", "MB_S_BMS", sw.mb_s_bms, "mb_s_bms")}
            {tc("ON", "MB_S_1", sw.mb_1_s, "mb_1_s")}
            {tc("ON", "MB_S_2", sw.mb_2_s, "mb_2_s")}
            {tc("ON", "MB_S_3", sw.mb_3_s, "mb_3_s")}
            {tc("ON", "MB_S_4", sw.mb_4_s, "mb_4_s")}
            {tc("ON", "MB_S_5", sw.mb_5_s, "mb_5_s")}
            {tc("ON", "PDE-S-OLR\nSTATUS", sw.pde_s_olr, "pde_s_olr")}
            {tc("MB_S-PDE_S", "PDE-S-148\nIN STAT", sw.mbs_pde, "mbs_pde")}
          </div>

          <div style={{ marginTop: '40px', background: '#ddd', border: '1px solid #aaa', padding: '15px', borderRadius: '4px' }}>
            <div style={{ fontSize: '14px', fontWeight: 'bold', color: '#000', marginBottom: '15px', textAlign: 'center' }}>GENERAL CONTROL SWITCHES</div>
            <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginTop: '10px' }}>
              {tc("CO2_SCRUB_P", "PORT_PWR", sw.co2_p, "co2_p")}
              {tc("CO2_SCRUB_S", "STBD_PWR", sw.co2_s, "co2_s")}
              {tc("EMG_LED_S", "ON", sw.emg_led, "emg_led")}
              {tc("SURFACE INS", "ON", sw.sur_ins, "sur_ins")}
              {tc("SONAR", "ON", sw.sonar, "sonar")}
              {tc("UW_LED_P", "ON", sw.uw_led_p, "uw_led_p")}
              {tc("UW_LED_S", "ON", sw.uw_led_s, "uw_led_s")}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

// SW-3 Emergency Layout
export function Switches3Layout({ appState, apiCall }) {
  const sw3 = appState.switches?.sw3 || {};
  
  const tc = (labelTop, labelBottom, isOn, stateKey) => (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '2px' }}>
      {labelTop && <div style={{ fontSize: '11px', color: '#000', fontWeight: 'bold', marginBottom: '2px', whiteSpace: 'pre-wrap', textAlign: 'center' }}>{labelTop}</div>}
      <MetalSwitch 
        isOn={isOn} 
        onToggle={() => apiCall(`/api/toggle/switches.sw3.${stateKey}`)} 
        idKey={`tog-sw3-${stateKey}`} 
        label="" 
      />
      {labelBottom && <div style={{ fontSize: '11px', color: '#000', fontWeight: 'bold', marginTop: '2px', whiteSpace: 'pre-wrap', textAlign: 'center' }}>{labelBottom}</div>}
    </div>
  );

  // Switch row for water leak / insulation panels
  const swRow = (label, isOn, stateKey) => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', margin: '2px 0' }}>
      <MetalSwitch
        isOn={isOn}
        onToggle={() => apiCall(`/api/toggle/switches.sw3.${stateKey}`)}
        idKey={`tog-sw3-${stateKey}`}
        label=""
      />
      {label && <div style={{ fontSize: '11px', fontWeight: 'bold', color: '#000', whiteSpace: 'nowrap' }}>{label}</div>}
    </div>
  );

  return (
    <div className="main-content-wrapper" style={{ padding: '8px', overflowY: 'auto', background: 'var(--color-bg)' }}>
      <div style={{ width: '100%', boxSizing: 'border-box' }}>
        
        <div style={{ width: '100%', background: '#ccc', border: '1px solid #aaa', padding: '20px', borderRadius: '4px', position: 'relative', marginBottom: '20px', boxSizing: 'border-box' }}>
          
          <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#000', textAlign: 'center', marginBottom: '20px' }}>EMERGENCY JETTISONING SWITCHES</div>

          {/* Top Section */}
          <div style={{ display: 'flex', justifyContent: 'center', gap: '60px' }}>
            <div>
              <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#000', marginBottom: '10px', borderBottom: '1px solid #999', paddingBottom: '4px' }}>TRIM-EMG JET-STBD</div>
              <div style={{ display: 'flex', gap: '15px' }}>
                {tc("T-EJ-P1", "T-EJ-S1", sw3.trim_p1, "trim_p1")}
                {tc("T-EJ-P2", "T-EJ-S2", sw3.trim_p2, "trim_p2")}
                {tc("T-EJ-P3", "T-EJ-S3", sw3.trim_p3, "trim_p3")}
                {tc("T-EJ-P4", "T-EJ-S4", sw3.trim_p4, "trim_p4")}
              </div>
            </div>
            
            <div>
              <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#000', marginBottom: '10px', borderBottom: '1px solid #999', paddingBottom: '4px' }}>MARKER BUOY</div>
              <div style={{ display: 'flex', gap: '15px' }}>
                {tc("MB-EJ-P1", "MB-EJ-S1", sw3.mb_p1, "mb_p1")}
                {tc("MB-EJ-P2", "MB-EJ-S2", sw3.mb_p2, "mb_p2")}
                {tc("MB-EJ-P3", "MB-EJ-S3", sw3.mb_p3, "mb_p3")}
                {tc("MB-EJ-P4", "MB-EJ-S4", sw3.mb_p4, "mb_p4")}
              </div>
            </div>
          </div>

          {/* Middle Section */}
          <div style={{ display: 'flex', marginTop: '20px', alignItems: 'center', justifyContent: 'center', gap: '40px' }}>
            
            <div>
              <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#000', marginBottom: '10px' }}>MANIPULATOR</div>
              <div style={{ display: 'flex', gap: '10px' }}>
                {tc("EJM-P1", "EJM-S1", sw3.mani_p1, "mani_p1")}
                {tc("EJM-P2", "EJM-S2", sw3.mani_p2, "mani_p2")}
                {tc("EJM-P3", "EJM-S3", sw3.mani_p3, "mani_p3")}
                {tc("EJM-P4", "EJM-S4", sw3.mani_p4, "mani_p4")}
              </div>
              <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
                {tc("EDW_P1", "EDW_S1", sw3.edw_p1, "edw_p1")}
                {tc("EDW_P2", "EDW_S2", sw3.edw_p2, "edw_p2")}
              </div>
            </div>

            <div style={{ width: '120px', height: '180px', background: '#ddd', borderRadius: '8px', border: '2px solid #fff', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '10px', boxShadow: '0 4px 8px rgba(0,0,0,0.2)' }}>
              <div style={{ width: '60px', height: '60px', borderRadius: '50%', background: '#111', border: '4px solid #333', marginBottom: '20px' }}></div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                {[...Array(6)].map((_, i) => <div key={i} style={{ width: '40px', height: '2px', background: '#999' }}></div>)}
              </div>
              <div style={{ fontSize: '8px', color: '#555', marginTop: 'auto', fontWeight: 'bold' }}>AXIS</div>
            </div>

            <div style={{ paddingLeft: '0' }}>
              <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#000', marginBottom: '10px' }}>SAMPLE BASKET</div>
              <div style={{ display: 'flex', gap: '10px' }}>
                {tc("EJS-P1", "EJS-S1", sw3.samp_p1, "samp_p1")}
                {tc("EJS-P2", "EJS-S2", sw3.samp_p2, "samp_p2")}
                {tc("EJX-P1", "EJX-S1", sw3.ejx_p1, "ejx_p1")}
                {tc("EJX-P2", "EJX-S2", sw3.ejx_p2, "ejx_p2")}
              </div>
              <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
                {tc("EDW_P3", "EDW_S3", sw3.edw_p3, "edw_p3")}
                {tc("EDW_P4", "EDW_S4", sw3.edw_p4, "edw_p4")}
              </div>
            </div>
          </div>

          {/* Bottom Indicator/Switch Panels — centered */}
          <div style={{ display: 'flex', marginTop: '30px', gap: '30px', justifyContent: 'center', alignItems: 'flex-start' }}>
            
            {/* WATER LEAK PORT STBD */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#000', marginBottom: '10px', textAlign: 'center' }}>WATER LEAK<br/>PORT STBD</div>
              <div style={{ display: 'flex', gap: '4px', background: '#bbb', border: '1px solid #999', padding: '8px', borderRadius: '4px' }}>
                {/* Port column */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
                  {swRow('PS',  sw3.wl_ps_p,  'wl_ps_p')}
                  {swRow('IDE', sw3.wl_ide_p, 'wl_ide_p')}
                  {swRow('PDE', sw3.wl_pde_p, 'wl_pde_p')}
                  {swRow('PJB', sw3.wl_pjb_p, 'wl_pjb_p')}
                  {swRow('TJB', sw3.wl_tjb_p, 'wl_tjb_p')}
                  {swRow('BAT', sw3.wl_bat_p, 'wl_bat_p')}
                </div>
                {/* Stbd column */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2px', marginLeft: '4px' }}>
                  {swRow('', sw3.wl_ps_s,  'wl_ps_s')}
                  {swRow('', sw3.wl_ide_s, 'wl_ide_s')}
                  {swRow('', sw3.wl_pde_s, 'wl_pde_s')}
                  {swRow('', sw3.wl_pjb_s, 'wl_pjb_s')}
                  {swRow('', sw3.wl_tjb_s, 'wl_tjb_s')}
                  {swRow('', sw3.wl_bat_s, 'wl_bat_s')}
                </div>
              </div>
            </div>

            {/* ALARM PANEL */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#000', marginBottom: '10px' }}>ALARM PANEL</div>
              <div style={{ display: 'flex', gap: '30px', background: '#ddd', padding: '10px 16px', borderRadius: '4px', border: '1px solid #aaa', alignItems: 'center' }}>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <div style={{ fontSize: '8px', fontWeight: 'bold' }}>BUZZER_1</div>
                  <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: '#222', border: '2px solid #111', marginTop: '4px' }}></div>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
                    {[0,1,2,3].map(i => <div key={i} style={{ width: '16px', height: '16px', background: '#111', border: '2px solid #000', borderRadius: '2px' }}></div>)}
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
                    {[0,1,2,3].map(i => <div key={i} style={{ width: '16px', height: '16px', background: '#111', border: '2px solid #000', borderRadius: '2px' }}></div>)}
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
                    {[0,1,2,3].map(i => <div key={i} style={{ width: '16px', height: '16px', background: '#111', border: '2px solid #000', borderRadius: '2px' }}></div>)}
                  </div>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <div style={{ fontSize: '8px', fontWeight: 'bold' }}>BUZZER_2</div>
                  <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: '#222', border: '2px solid #111', marginTop: '4px' }}></div>
                </div>
              </div>
            </div>

            {/* INSULATION PORT STBD */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#000', marginBottom: '10px', textAlign: 'center' }}>INSULATION<br/>PORT STBD</div>
              <div style={{ display: 'flex', gap: '4px', background: '#bbb', border: '1px solid #999', padding: '8px', borderRadius: '4px' }}>
                {/* Port column */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
                  {swRow('',     sw3.ins_ps_p,   'ins_ps_p')}
                  {swRow('',     sw3.ins_ide_p,  'ins_ide_p')}
                  {swRow('',     sw3.ins_pde_p,  'ins_pde_p')}
                  {swRow('',     sw3.ins_148_p,  'ins_148_p')}
                  {swRow('',     sw3.ins_pseb_p, 'ins_pseb_p')}
                  {swRow('',     sw3.ins_sp1_p,  'ins_sp1_p')}
                </div>
                {/* Stbd column with labels */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2px', marginLeft: '4px' }}>
                  {swRow('PS UB',  sw3.ins_ps_s,   'ins_ps_s')}
                  {swRow('IDE',    sw3.ins_ide_s,  'ins_ide_s')}
                  {swRow('PDE',    sw3.ins_pde_s,  'ins_pde_s')}
                  {swRow('148V',   sw3.ins_148_s,  'ins_148_s')}
                  {swRow('PS EB',  sw3.ins_pseb_s, 'ins_pseb_s')}
                  {swRow('SPARE 1',sw3.ins_sp1_s,  'ins_sp1_s')}
                </div>
              </div>
            </div>

          </div>

          {/* Bottom Section Controls */}
          <div style={{ marginTop: '30px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'center', gap: '12px' }}>
              <BlackPushButton labelBottom="SUBMERSIBLE CTRL" onClick={() => {}} />
              <BlackPushButton labelBottom="WATER OUT" onClick={() => {}} />
              <BlackPushButton labelBottom="TRIM" onClick={() => {}} />
              {tc("FREEBOARD_P", "FREEBOARD_S", sw3.fb_p, "fb_p")}
              {tc("DIVE-IN-ON", "DIVE-IN-OFF", sw3.dive_in, "dive_in")}
              {tc("HP-AP-ON", "HP-AP-OFF", sw3.hp_ap, "hp_ap")}
              {tc("HP-BP-ON", "HP-BP-OFF", sw3.hp_bp, "hp_bp")}
            </div>

            <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', flexWrap: 'wrap', paddingBottom: '10px' }}>
              <KnobSwitch label="FWD CTRL" value={1} onChange={() => {}} />
              <KnobSwitch label="HEAD TRIM" value={1} onChange={() => {}} />
              <KnobSwitch label="DEP TRIM" value={1} onChange={() => {}} />
              <KnobSwitch label="LAT TRIM" value={1} onChange={() => {}} />
              <KnobSwitch label="HP REG" value={1} onChange={() => {}} />
              <KnobSwitch label="VBT CTRL" value={1} onChange={() => {}} />
              <KnobSwitch label="PITCH CTRL" value={1} onChange={() => {}} />
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
