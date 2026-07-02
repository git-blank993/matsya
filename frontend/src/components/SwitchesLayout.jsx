import React from 'react';
import { MetalSwitch } from './Controls';

// Subcomponents for P3/S3 Power Status
function InsulationDisplay({ label, value, unit, idKey = null }) {
  return (
    <div id={idKey} className="insulation-wrapper">
      <div className="iso-yellow-box">
        <div className="iso-led-row">
          <div className="iso-led"></div>
          <div className="iso-led"></div>
          <div className="iso-led"></div>
        </div>
        <div className="iso-lcd">{value}</div>
        <div className="iso-btn-row">
          <div className="iso-btn"></div>
          <div className="iso-btn"></div>
          <div className="iso-btn"></div>
        </div>
      </div>
      <div className="tape-label bottom-label">{label}</div>
    </div>
  );
}

function BattManDisplay({ label, value, unit, idKey = null }) {
  return (
    <div id={idKey} className="battman-wrapper">
      <div className="battman-gauge">
        <div className="battman-brand">MASTERVOLT</div>
        <div className="battman-lcd">{value}</div>
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

function RedVoltageDisplay({ label, value, unit, idKey = null }) {
  return (
    <div id={idKey} className="red-led-wrapper">
      <div className="red-led-lcd">{value}</div>
      <div className="tape-label bottom-label">{label}</div>
      <span className="tape-label side-label">{unit}</span>
    </div>
  );
}

function RotarySwitch({ label, levels, selectedLevel, idKey = null, onToggle }) {
  const idx = levels.indexOf(selectedLevel) >= 0 ? levels.indexOf(selectedLevel) : 0;
  
  let angle = 0;
  if (levels.length > 1) {
    const span = levels.length === 2 ? 60 : 90;
    const step = span / (levels.length - 1);
    angle = -(span / 2) + (idx * step);
  }

  return (
    <div id={idKey} className="rotary-switch-container" onClick={onToggle}>
      <span className="rotary-switch-title">{label}</span>
      <div className="rotary-switch-body">
        <div className="rotary-labels-row">
          {levels.map((lvl, i) => (
            <span key={i} className={`rotary-label ${i === idx ? 'rotary-lbl-sel' : ''}`}>
              {lvl}
            </span>
          ))}
        </div>
        <div className="rotary-knob" style={{ transform: `rotate(${angle}deg)` }}>
          <div className="rotary-knob-indicator"></div>
        </div>
      </div>
    </div>
  );
}

// Wrapper to standardise toggle usage
function ToggleBlock({ label, isOn, stateKey, prefix, apiCall }) {
  return (
    <div style={{ padding: '2px 0' }}>
      <MetalSwitch
        label={label}
        isOn={isOn}
        onToggle={() => apiCall(`/api/toggle/switches.${prefix}.${stateKey}`)}
        idKey={`tog-sw-${prefix}-${stateKey.replace(/_/g, '-')}`}
      />
    </div>
  );
}

export function SwitchesPLayout({ appState, apiCall }) {
  const sw = appState.switches?.p || {};
  const t = (label, isOn, stateKey) => <ToggleBlock label={label} isOn={isOn} stateKey={stateKey} prefix="p" apiCall={apiCall} />;

  return (
    <div className="main-content-wrapper" style={{ padding: '8px', overflowY: 'auto', background: 'var(--color-bg)' }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '8px' }}>
        
        {/* Power Status Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '4px', alignItems: 'center' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black', width: '100%' }}>Power Status</div>
          <InsulationDisplay label="EB_P INSULATION" value={sw.ib_insulation} unit="k ohm" />
          <BattManDisplay label="EB_P STATUS" value={sw.eb_b_status} unit="V" />
          <RedVoltageDisplay label="UB_P VOLTAGE" value={sw.ub_voltage} unit="V" />
          <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', marginTop: '10px' }}>
            <RotarySwitch label="Power EB_" levels={["UB_", "E_Batts"]} selectedLevel={sw.power_selection_eb} onToggle={() => apiCall('/api/toggle/switches.p.power_selection_eb')} />
            <RotarySwitch label="Power UB" levels={["AB", "MB"]} selectedLevel={sw.power_selection_ub} onToggle={() => apiCall('/api/toggle/switches.p.power_selection_ub')} />
          </div>
          {t("UB MCB", sw.ub_mcb, "ub_mcb")}
        </div>

        {/* Thruster Controls Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>Thruster Controls</div>
          {t("Speed Control", sw.speed_control, "speed_control")}
          {t("Heading trim", sw.heading_trim, "heading_trim")}
          {t("Depth trim", sw.depth_trim, "depth_trim")}
          {t("lateral trim", sw.lateral_trim, "lateral_trim")}
        </div>

        {/* BATS Control Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>BATS Control</div>
          {t("HP_AP_ON/OFF", sw.hp_ap_on_off, "hp_ap_on_off")}
          {t("HP_BP_ON/OFF", sw.hp_bp_on_off, "hp_bp_on_off")}
          {t("HP_Reg_set", sw.hp_reg_set, "hp_reg_set")}
          {t("Pitch ON/OFF", sw.pitch_on_off, "pitch_on_off")}
          {t("VBT_Set value", sw.vbt_set_value, "vbt_set_value")}
          {t("Pitch up & Down _Analog", sw.pitch_up_down_analog, "pitch_up_down_analog")}
          {t("FreeBoard_P", sw.freeboard_p, "freeboard_p")}
          {t("Dive in", sw.dive_in, "dive_in")}
          {t("Water OUT_ON/OFF", sw.water_out_on_off, "water_out_on_off")}
        </div>

        {/* General Control Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>General control Switches</div>
          {t("Co2 scrubber_P", sw.co2_scrubber_p, "co2_scrubber_p")}
          {t("Joystick Enable", sw.joystick_enable, "joystick_enable")}
          {t("Pilot selection", sw.pilot_selection, "pilot_selection")}
          {t("Copilot selection", sw.copilot_selection, "copilot_selection")}
          {t("VHS_Power_P", sw.vhs_power_p, "vhs_power_p")}
          {t("LED_Emegency_Port", sw.led_emergency_port, "led_emergency_port")}
          {t("UW Camera _P", sw.uw_camera_p, "uw_camera_p")}
          {t("SONAR", sw.sonar, "sonar")}
          {t("Surface_INS", sw.surface_ins, "surface_ins")}
        </div>

        {/* Power Direct Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>POWER DIRECT CONTROL_PORT</div>
          {t("MB_P_1*", sw.mb_p_1, "mb_p_1")}
          {t("MB_P_2*", sw.mb_p_2, "mb_p_2")}
          {t("MB_P_3*", sw.mb_p_3, "mb_p_3")}
          {t("MB_P_4*", sw.mb_p_4, "mb_p_4")}
          {t("MB_P_5*", sw.mb_p_5, "mb_p_5")}
          {t("AB_P_BMS*", sw.ab_p_bms, "ab_p_bms")}
          {t("MB_P_BMS*", sw.mb_p_bms, "mb_p_bms")}
          {t("AB_P Power selection*", sw.ab_p_power_selection, "ab_p_power_selection")}
          {t("MB_P-PDE_P*", sw.mb_p_pde_p, "mb_p_pde_p")}
        </div>

        {/* SDW Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>Service Drop Weight Switches</div>
          {t("Port side SDW 1", sw.port_side_sdw_1, "port_side_sdw_1")}
          {t("Port side SDW 2", sw.port_side_sdw_2, "port_side_sdw_2")}
          {t("Port side SDW 3", sw.port_side_sdw_3, "port_side_sdw_3")}
          {t("Port side SDW 4", sw.port_side_sdw_4, "port_side_sdw_4")}
          {t("Port side SDW 5", sw.port_side_sdw_5, "port_side_sdw_5")}
          {t("Starboard side SDW 1", sw.starboard_side_sdw_1, "starboard_side_sdw_1")}
          {t("Starboard side SDW 2", sw.starboard_side_sdw_2, "starboard_side_sdw_2")}
          {t("Starboard side SDW 3", sw.starboard_side_sdw_3, "starboard_side_sdw_3")}
          {t("Starboard side SDW 4", sw.starboard_side_sdw_4, "starboard_side_sdw_4")}
          {t("Starboard side SDW 5", sw.starboard_side_sdw_5, "starboard_side_sdw_5")}
        </div>

        {/* Emergency Jettisoning Column (Split internally) */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px', gridColumn: 'span 2' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>Emergency Jettisoning_P</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
              {t("EJ Manipulator_1", sw.ej_manipulator_1, "ej_manipulator_1")}
              {t("EJ Manipulator_2", sw.ej_manipulator_2, "ej_manipulator_2")}
              {t("EJ Manipulator_3", sw.ej_manipulator_3, "ej_manipulator_3")}
              {t("EJ Manipulator_4", sw.ej_manipulator_4, "ej_manipulator_4")}
              {t("EJ Trim System_1", sw.ej_trim_system_1, "ej_trim_system_1")}
              {t("EJ Trim System_2", sw.ej_trim_system_2, "ej_trim_system_2")}
              {t("EJ Trim System_3", sw.ej_trim_system_3, "ej_trim_system_3")}
              {t("EJ Trim System_4", sw.ej_trim_system_4, "ej_trim_system_4")}
              {t("EJ Sampling Basket_1", sw.ej_sampling_basket_1, "ej_sampling_basket_1")}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
              {t("EJ Sampling Basket_2", sw.ej_sampling_basket_2, "ej_sampling_basket_2")}
              {t("EJ Sampling Basket_3", sw.ej_sampling_basket_3, "ej_sampling_basket_3")}
              {t("EJ Sampling Basket_4", sw.ej_sampling_basket_4, "ej_sampling_basket_4")}
              {t("EM Buoy Release_1", sw.em_buoy_release_1, "em_buoy_release_1")}
              {t("EM Buoy Release_2", sw.em_buoy_release_2, "em_buoy_release_2")}
              {t("EM Buoy Release_3", sw.em_buoy_release_3, "em_buoy_release_3")}
              {t("EM Buoy Release_4", sw.em_buoy_release_4, "em_buoy_release_4")}
              {t("Emergency Drop Weight_P1(SC)", sw.em_drop_weight_p1_sc, "em_drop_weight_p1_sc")}
              {t("Emergency Drop Weight_P2(PC)", sw.em_drop_weight_p2_pc, "em_drop_weight_p2_pc")}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function SwitchesSLayout({ appState, apiCall }) {
  const sw = appState.switches?.s || {};
  const t = (label, isOn, stateKey) => <ToggleBlock label={label} isOn={isOn} stateKey={stateKey} prefix="s" apiCall={apiCall} />;

  return (
    <div className="main-content-wrapper" style={{ padding: '8px', overflowY: 'auto', background: 'var(--color-bg)' }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '8px' }}>
        
        {/* Power Status Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '4px', alignItems: 'center' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black', width: '100%' }}>Power Status</div>
          <InsulationDisplay label="EB_S INSULATION" value={sw.ib_insulation} unit="k ohm" />
          <BattManDisplay label="EB_S STATUS" value={sw.eb_b_status} unit="V" />
          <RedVoltageDisplay label="UB_S VOLTAGE" value={sw.ub_voltage} unit="V" />
          <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', marginTop: '10px' }}>
            <RotarySwitch label="Power EB_" levels={["UB_", "E_Batts"]} selectedLevel={sw.power_selection_eb} onToggle={() => apiCall('/api/toggle/switches.s.power_selection_eb')} />
            <RotarySwitch label="Power UB" levels={["AB", "MB"]} selectedLevel={sw.power_selection_ub} onToggle={() => apiCall('/api/toggle/switches.s.power_selection_ub')} />
          </div>
          {t("UB MCB", sw.ub_mcb, "ub_mcb")}
        </div>

        {/* Thruster Controls Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>Thruster Controls</div>
          {t("Speed Control", sw.speed_control, "speed_control")}
          {t("Heading trim", sw.heading_trim, "heading_trim")}
          {t("Depth trim", sw.depth_trim, "depth_trim")}
          {t("lateral trim", sw.lateral_trim, "lateral_trim")}
        </div>

        {/* BATS Control Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>BATS Control</div>
          {t("HP_AS_ON/OFF", sw.hp_as_on_off, "hp_as_on_off")}
          {t("HP_BS_ON/OFF", sw.hp_bs_on_off, "hp_bs_on_off")}
          {t("HP_Reg_set", sw.hp_reg_set, "hp_reg_set")}
          {t("Pitch ON/OFF", sw.pitch_on_off, "pitch_on_off")}
          {t("VBT_Set value", sw.vbt_set_value, "vbt_set_value")}
          {t("Pitch up & Down _Analog", sw.pitch_up_down_analog, "pitch_up_down_analog")}
          {t("FreeBoard_S", sw.freeboard_s, "freeboard_s")}
          {t("Dive in", sw.dive_in, "dive_in")}
          {t("Water OUT_ON/OFF", sw.water_out_on_off, "water_out_on_off")}
        </div>

        {/* General Control Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>General control Switches</div>
          {t("Co2 scrubber_S", sw.co2_scrubber_s, "co2_scrubber_s")}
          {t("Joystick Enable", sw.joystick_enable, "joystick_enable")}
          {t("Pilot selection", sw.pilot_selection, "pilot_selection")}
          {t("Copilot selection", sw.copilot_selection, "copilot_selection")}
          {t("VHS_Power_S", sw.vhs_power_s, "vhs_power_s")}
          {t("LED_Emegency_Port", sw.led_emergency_port, "led_emergency_port")}
          {t("UW Camera _S", sw.uw_camera_s, "uw_camera_s")}
          {t("SONAR", sw.sonar, "sonar")}
          {t("Surface_INS", sw.surface_ins, "surface_ins")}
        </div>

        {/* Power Direct Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>POWER DIRECT CONTROL_STARBOARD</div>
          {t("MB_S_1*", sw.mb_s_1, "mb_s_1")}
          {t("MB_S_2*", sw.mb_s_2, "mb_s_2")}
          {t("MB_S_3*", sw.mb_s_3, "mb_s_3")}
          {t("MB_S_4*", sw.mb_s_4, "mb_s_4")}
          {t("MB_S_5*", sw.mb_s_5, "mb_s_5")}
          {t("AB_S_BMS*", sw.ab_s_bms, "ab_s_bms")}
          {t("MB_S_BMS*", sw.mb_s_bms, "mb_s_bms")}
          {t("AB_S Power selection*", sw.ab_s_power_selection, "ab_s_power_selection")}
          {t("MB_S-PDE_S*", sw.mb_s_pde_s, "mb_s_pde_s")}
        </div>

        {/* SDW Column */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>Service Drop Weight Switches</div>
          {t("Port side SDW 1", sw.port_side_sdw_1, "port_side_sdw_1")}
          {t("Port side SDW 2", sw.port_side_sdw_2, "port_side_sdw_2")}
          {t("Port side SDW 3", sw.port_side_sdw_3, "port_side_sdw_3")}
          {t("Port side SDW 4", sw.port_side_sdw_4, "port_side_sdw_4")}
          {t("Port side SDW 5", sw.port_side_sdw_5, "port_side_sdw_5")}
          {t("Starboard side SDW 1", sw.starboard_side_sdw_1, "starboard_side_sdw_1")}
          {t("Starboard side SDW 2", sw.starboard_side_sdw_2, "starboard_side_sdw_2")}
          {t("Starboard side SDW 3", sw.starboard_side_sdw_3, "starboard_side_sdw_3")}
          {t("Starboard side SDW 4", sw.starboard_side_sdw_4, "starboard_side_sdw_4")}
          {t("Starboard side SDW 5", sw.starboard_side_sdw_5, "starboard_side_sdw_5")}
        </div>

        {/* Emergency Jettisoning Column (Split internally) */}
        <div className="mcc-col" style={{ display: 'flex', flexDirection: 'column', gap: '0px', gridColumn: 'span 2' }}>
          <div className="mcc-panel-title" style={{ background: '#ffea00', color: 'black' }}>Emergency Jettisoning_S</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
              {t("EJ Manipulator_1", sw.ej_manipulator_1, "ej_manipulator_1")}
              {t("EJ Manipulator_2", sw.ej_manipulator_2, "ej_manipulator_2")}
              {t("EJ Manipulator_3", sw.ej_manipulator_3, "ej_manipulator_3")}
              {t("EJ Manipulator_4", sw.ej_manipulator_4, "ej_manipulator_4")}
              {t("EJ Trim System_1", sw.ej_trim_system_1, "ej_trim_system_1")}
              {t("EJ Trim System_2", sw.ej_trim_system_2, "ej_trim_system_2")}
              {t("EJ Trim System_3", sw.ej_trim_system_3, "ej_trim_system_3")}
              {t("EJ Trim System_4", sw.ej_trim_system_4, "ej_trim_system_4")}
              {t("EJ Sampling Basket_1", sw.ej_sampling_basket_1, "ej_sampling_basket_1")}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
              {t("EJ Sampling Basket_2", sw.ej_sampling_basket_2, "ej_sampling_basket_2")}
              {t("EJ Sampling Basket_3", sw.ej_sampling_basket_3, "ej_sampling_basket_3")}
              {t("EJ Sampling Basket_4", sw.ej_sampling_basket_4, "ej_sampling_basket_4")}
              {t("EM Buoy Release_1", sw.em_buoy_release_1, "em_buoy_release_1")}
              {t("EM Buoy Release_2", sw.em_buoy_release_2, "em_buoy_release_2")}
              {t("EM Buoy Release_3", sw.em_buoy_release_3, "em_buoy_release_3")}
              {t("EM Buoy Release_4", sw.em_buoy_release_4, "em_buoy_release_4")}
              {t("Emergency Drop Weight_S1(SC)", sw.em_drop_weight_s1_sc, "em_drop_weight_s1_sc")}
              {t("Emergency Drop Weight_S2(PC)", sw.em_drop_weight_s2_pc, "em_drop_weight_s2_pc")}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
