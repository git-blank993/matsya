from fasthtml.common import Div, Span, Link, H1, to_xml, FastHTML, H2, H3, Title, serve
from starlette.staticfiles import StaticFiles
from models import MatsyaUIState
from components import (
    TopbarInlineMetric,
    VerticalGauge,
    SimpleRpmBox,
    SimpleMetricBox,
    CompassBox,
    SidebarMetric,
    StatusPill,
    ToggleSwitch,
    BottomTabsNav,
    BigNumber,
    LedPanel,
    SemiCircleGauge,
    HorizontalProgressBar,
    SensorStatusPill,
    HSSSLabelInput,
    BallastActionButton,
    BallastPressureRead,
    BallastActSlider,
    VBSTankGauge,
    VBSMetricRow,
    VBSWaterButton,
    VBSSetControl,
    TrimPositionBar,
    SpeedControlSlider,
    OIMToggleRow,
    ThrusterPanel,
    PropCenterToggleBlock,
    PropAxisControl,
    BatteryPanel,
    PDEPanel,
    IDEPanel,
    UmbilicalPanel,
    ImagingToggle,
    LedDimmerSlider,
    CameraActionGrid,
    PanTiltBar,
    PanTiltPad,
    SensorToggleBlock,
    SensorLedStatus,
    AlarmLedStatus,
    ScientificSensorRowItem,
    SensorBoxMetric,
    BuzzerPanel,
    LogTable,
    HorizontalToggle,
    RedSignalIndicator,
    StatusChartRowComponent,
    KwhDataGrid,
    KwhVerticalGauge,
    MccIndicator,
    MccStatusBox,
    MccMessageInput,
    MccShipData,
    MccRadioGroup,
    MccCrewStatus,
    MccPowerDropdown,
)

import asyncio
import random
from datetime import datetime


# Favicon + Inter Font + Custom Stylesheet
inter_font = Link(
    href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap",
    rel="stylesheet",
)
custom_css = Link(href="/static/styles.css", rel="stylesheet")

app = FastHTML(exts="ws", hdrs=(inter_font, custom_css))
app.mount("/static", StaticFiles(directory="static"), name="static")
rt = app.route

# ----------------- STATE -----------------
app_state = MatsyaUIState()
connected_clients = set()


# ----------------- WEBSOCKETS -----------------
async def on_conn(ws, send):
    connected_clients.add(send)


async def on_disconn(ws, send):
    connected_clients.discard(send)


@app.ws("/ws", conn=on_conn, disconn=on_disconn)
async def ws_handler(msg: str, send):
    pass


async def broadcast(html_component):
    xml_str = to_xml(html_component)
    for client_send in list(connected_clients):
        try:
            await client_send(xml_str)
        except Exception:
            connected_clients.discard(client_send)


# ----------------- UI VIEWS -----------------
def HeaderArea():
    s = app_state.header
    return Div(
        # Top strip: Dive info + Title + Present Time
        Div(
            Div(
                Div(
                    Span("DIVE #", cls="header-label"),
                    Span(s.dive_num, cls="header-value-box"),
                    cls="header-metric",
                ),
                Div(
                    Span("Mission Run Time", cls="header-label"),
                    Span(s.mission_time, cls="header-value-box mono"),
                    cls="header-metric",
                ),
                cls="header-left",
            ),
            H1("Manned Submersible — MATSYA 6000", cls="header-title"),
            Div(
                Span("Present Time", cls="header-label"),
                Span(s.present_time, cls="header-value-box mono"),
                cls="header-metric",
            ),
            cls="header-top",
        ),
        # Bottom metric strip
        Div(
            TopbarInlineMetric("Heading", s.heading.value, s.heading.unit),
            TopbarInlineMetric("Depth", s.depth.value, s.depth.unit),
            TopbarInlineMetric("Altitude", s.altitude.value, s.altitude.unit),
            TopbarInlineMetric("MB_P SOC", s.mb_p_soc.value, s.mb_p_soc.unit),
            TopbarInlineMetric("MB_S SOC", s.mb_s_soc.value, s.mb_s_soc.unit),
            cls="header-metrics-strip",
        ),
        cls="header-area",
    )


def AppLayout(active_tab="Main"):
    s = app_state

    # ---- RIGHT SIDEBAR (Shared across tabs) ----
    sidebar_col = Div(
        # Environment section
        Div(
            SidebarMetric("O₂", s.environment.o2.value, s.environment.o2.unit),
            SidebarMetric("CO₂", s.environment.co2.value, s.environment.co2.unit),
            SidebarMetric("Temp", s.environment.temp.value, s.environment.temp.unit),
            SidebarMetric(
                "Pressure", s.environment.pressure.value, s.environment.pressure.unit
            ),
            cls="sidebar-section",
        ),
        Div(cls="sidebar-divider"),
        # Controls section
        Div(
            ToggleSwitch("Joystick", s.sidebar.joystick, id_key="toggle-joystick", toggle_url="/api/toggle_joystick"),
            ToggleSwitch("Thrusters Enable", s.sidebar.thrusters_enable, id_key="toggle-thrusters", toggle_url="/api/toggle_thrusters_enable"),
            ToggleSwitch("High Speed", s.sidebar.high_speed, id_key="toggle-high-speed", toggle_url="/api/toggle_high_speed"),
            cls="sidebar-section",
        ),
        Div(cls="sidebar-divider"),
        # Status section
        Div(
            StatusPill("IR", s.sidebar.ir_ok),
            StatusPill(
                "Water Ingress",
                is_ok=not s.sidebar.water_ingress,
                ok_text="CLEAR",
                err_text="ALERT",
            ),
            StatusPill(
                "Comm", s.sidebar.comm_status, ok_text="Status OK", err_text="Status"
            ),
            cls="sidebar-section",
        ),
        Div(cls="sidebar-divider"),
        # LED indicators panel
        LedPanel(s.leds),
        # ON button at bottom
        Div(
            Div(
                "OFF" if s.is_powered_on else "ON",
                cls="on-button" + (" power-on" if s.is_powered_on else ""),
                hx_post="/api/toggle_power",
                hx_swap="none",
            ),
            cls="sidebar-footer",
        ),
        cls="col-sidebar",
    )

    if active_tab == "Main":
        # ---- LEFT COLUMN: Altitude Gauge ----
        alt_col = Div(
            VerticalGauge(
                "Altitude",
                s.header.altitude.value,
                max_val=10,
                unit="m",
                low_is_good=False,
                scale_labels=list(range(10, -1, -1)),
            ),
            cls="col-altitude",
        )

        # ---- CENTER COLUMN: Roll/Pitch + Compass + Big Numbers ----
        center_col = Div(
            Div(
                SimpleMetricBox("Roll", s.imu.roll.value),
                SimpleMetricBox("Pitch", s.imu.pitch.value),
                cls="roll-pitch-row",
            ),
            Div(CompassBox(), cls="compass-area"),
            Div(
                BigNumber("Altitude", s.header.altitude.value, "m"),
                BigNumber("Heading_P", s.imu.heading_p.value, "deg"),
                BigNumber("Depth", s.header.depth.value, "m"),
                cls="big-numbers-row",
            ),
            cls="col-center",
        )

        # ---- DEPTH + PROPULSION COLUMN ----
        depth_prop_col = Div(
            Div(
                VerticalGauge(
                    "Depth",
                    s.header.depth.value,
                    max_val=12,
                    unit="m",
                    low_is_good=True,
                    scale_labels=list(range(-2, 13)),
                ),
                cls="depth-gauge-wrap",
            ),
            Div(
                H3("Propulsion", cls="section-title"),
                Div(
                    SimpleRpmBox("T2 RPM", s.propulsion.t2_rpm),
                    SimpleRpmBox("T1 RPM", s.propulsion.t1_rpm),
                    cls="rpm-row",
                ),
                Div(SimpleRpmBox("T3 RPM", s.propulsion.t3_rpm), cls="rpm-row-center"),
                Div(SimpleRpmBox("T4 RPM", s.propulsion.t4_rpm), cls="rpm-row-center"),
                Div(SimpleRpmBox("T5 RPM", s.propulsion.t5_rpm), cls="rpm-row-center"),
                Div(
                    SimpleRpmBox("T8 RPM", s.propulsion.t8_rpm),
                    SimpleRpmBox("T6 RPM", s.propulsion.t6_rpm),
                    cls="rpm-row",
                ),
                Div(SimpleRpmBox("T7 RPM", s.propulsion.t7_rpm), cls="rpm-row-center"),
                Div(cls="prop-separator"),
                Div(
                    SimpleMetricBox("Latitude", s.propulsion.latitude.value, "deg"),
                    SimpleMetricBox("Longitude", s.propulsion.longitude.value, "deg"),
                    cls="latlon-stack",
                ),
                cls="propulsion-panel",
            ),
            cls="col-depth-prop",
        )

        main_content_area = Div(
            Div(alt_col, center_col, depth_prop_col, sidebar_col, cls="main-content"),
            Div(
                SimpleMetricBox("East_speed", s.bottom.east_speed.value, "m/s"),
                SimpleMetricBox("Vert_speed", s.bottom.vert_speed.value, "m/s"),
                SimpleMetricBox("North_Speed", s.bottom.north_speed.value, "m/s"),
                SimpleMetricBox("Ship Heading", s.bottom.ship_heading.value, "deg"),
                cls="bottom-speed-strip",
            ),
            cls="main-content-wrapper",
        )

    elif active_tab == "HSSS":

        def render_hsss_panel(title, side_data, sf_suffix):
            return Div(
                Div(title, cls="hsss-panel-title"),
                Div(
                    SemiCircleGauge(
                        f"CO2{sf_suffix}",
                        side_data.co2.value,
                        0,
                        5000,
                        "ppm",
                        scale_labels=["0", "1000", "2000", "3000", "4000", "5000"],
                    ),
                    SemiCircleGauge(
                        f"Oxygen{sf_suffix}",
                        side_data.oxygen.value,
                        19,
                        25,
                        "% v/v",
                        scale_labels=["19", "20", "21", "22", "23", "24", "25"],
                        is_oxygen=True,
                    ),
                    cls="hsss-gauges-row",
                ),
                Div(
                    Div(
                        HorizontalProgressBar(
                            f"Pressure in mbar{sf_suffix}",
                            side_data.pressure.value,
                            800,
                            1200,
                            "",
                            scale_labels=[
                                "800",
                                "850",
                                "900",
                                "950",
                                "1000",
                                "1050",
                                "1100",
                                "1150",
                                "1200",
                            ],
                        ),
                        HorizontalProgressBar(
                            f"Temp in Deg C{sf_suffix}",
                            side_data.temp.value,
                            0,
                            100,
                            "",
                            scale_labels=[
                                "0",
                                "10",
                                "20",
                                "30",
                                "40",
                                "50",
                                "60",
                                "70",
                                "80",
                                "90",
                                "100",
                            ],
                        ),
                        HorizontalProgressBar(
                            f"Humidity{sf_suffix} in %",
                            side_data.humidity.value,
                            0,
                            100,
                            "",
                            scale_labels=[
                                "0",
                                "10",
                                "20",
                                "30",
                                "40",
                                "50",
                                "60",
                                "70",
                                "80",
                                "90",
                                "100",
                            ],
                        ),
                        cls="hsss-col-left",
                    ),
                    Div(
                        SensorStatusPill(
                            f"Smoke Sensor{sf_suffix.lower()}",
                            side_data.smoke_sensor,
                            is_ok=(side_data.smoke_sensor == "NO SMOKE"),
                        ),
                        SensorStatusPill(
                            f"Flame Sensor{sf_suffix.lower()}",
                            side_data.flame_sensor,
                            is_ok=(side_data.flame_sensor == "NO FLAME"),
                        ),
                        SensorStatusPill(
                            f"Heat Sensor{sf_suffix.lower()}",
                            side_data.heat_sensor,
                            is_ok=(side_data.heat_sensor == "Normal"),
                        ),
                        HSSSLabelInput(
                            f"Hydrogen{sf_suffix}", side_data.hydrogen.value, "%"
                        ),
                        HSSSLabelInput(
                            f"LP_L Pressure{sf_suffix}",
                            side_data.lp_l_pressure.value,
                            "bar",
                        ),
                        cls="hsss-col-right",
                    ),
                    cls="hsss-two-col",
                ),
                Div(
                    HSSSLabelInput(
                        f"HP_B1 Pressure{sf_suffix}",
                        side_data.hp_b1_pressure.value,
                        "bar",
                    ),
                    HSSSLabelInput(
                        f"HP_B2 Pressure{sf_suffix}",
                        side_data.hp_b2_pressure.value,
                        "bar",
                    ),
                    HSSSLabelInput(
                        f"HP_B3 Pressure{sf_suffix}",
                        side_data.hp_b3_pressure.value,
                        "bar",
                    ),
                    cls="hsss-bottom-row",
                ),
                cls="hsss-panel",
            )

        main_content_area = Div(
            Div(
                Div(
                    render_hsss_panel("HSSS_P", s.hsss.p, "_P"),
                    render_hsss_panel("HSSS_S", s.hsss.s, "_S"),
                    cls="hsss-content-row",
                ),
                sidebar_col,
                cls="main-content",
            ),
            cls="main-content-wrapper",
        )
    elif active_tab == "Ballast":
        b = s.ballast

        # ---- MAIN BALLAST SYSTEM PANEL ----
        main_ballast_panel = Div(
            Div(
                BallastActionButton("Ready to Dive open"),
                BallastActionButton("Ready to Dive Close"),
                BallastActionButton("Dive open"),
                BallastActionButton("Dive Close"),
                BallastActionButton("Surface open"),
                BallastActionButton("Surface Close"),
                cls="ballast-btn-grid",
            ),
            Div(
                Div(
                    BallastPressureRead("Read Pressure_S", b.main_ballast.read_pressure_s, b.main_ballast.pressure_s_enable, id_key="tog-bpr-s", toggle_url="/api/toggle/ballast.main_ballast.pressure_s_enable"),
                    BallastPressureRead("Read Pressure_P", b.main_ballast.read_pressure_p, b.main_ballast.pressure_p_enable, id_key="tog-bpr-p", toggle_url="/api/toggle/ballast.main_ballast.pressure_p_enable"),
                    cls="ballast-pressure-col",
                ),
                Div("Main\nBallast\nSystem", cls="ballast-main-label"),
                cls="ballast-mid-row",
            ),
            BallastActSlider("ACT 3 pos",  b.main_ballast.act3_pos),
            BallastActSlider("ACT 3 pos 2", b.main_ballast.act3_pos2),
            BallastActSlider("ACT 3 pos 3", b.main_ballast.act3_pos3),
            cls="ballast-main-panel",
        )

        # ---- VBS PANEL ----
        vbs_panel = Div(
            Div("VBS", cls="vbs-panel-title"),
            Div(
                Div(
                    Div(
                        Div("VBS_HPU_Enable", cls="vbs-hpu-label"),
                        Div(
                            "HPU ON" if b.vbs.hpu_enable else "HPU OFF",
                            cls="vbs-hpu-btn" + (" vbs-hpu-on" if b.vbs.hpu_enable else ""),
                        ),
                        cls="vbs-hpu-row",
                    ),
                    VBSMetricRow("HPU Pressure", b.vbs.hpu_pressure.value, "bar"),
                    VBSMetricRow("HPU temp", b.vbs.hpu_temp.value, "deg C"),
                    VBSWaterButton("Water IN"),
                    VBSWaterButton("Water OUT"),
                    VBSSetControl(b.vbs.vbs_set),
                    cls="vbs-left-col",
                ),
                VBSTankGauge(b.vbs.tank_level),
                cls="vbs-content-row",
            ),
            cls="ballast-vbs-panel",
        )

        # ---- TRIM PANEL ----
        trim_panel = Div(
            Div(
                Div("Trim Position (mm)", cls="trim-position-label"),
                Div("TRIM", cls="trim-title"),
                cls="trim-header",
            ),
            TrimPositionBar(b.trim.position_mm),
            Div(
                Div(
                    ToggleSwitch("power", b.trim.power, id_key="tog-trim-pwr", toggle_url="/api/toggle/ballast.trim.power"),
                    cls="trim-toggle-col",
                ),
                Div(
                    SimpleMetricBox("Voltage", b.trim.voltage.value, "V"),
                    SimpleMetricBox("Current", b.trim.current.value, "A"),
                    cls="trim-metrics-left",
                ),
                Div(
                    SimpleMetricBox("Temp", b.trim.temp.value, "deg C"),
                    SimpleMetricBox("speed", b.trim.speed.value, "mm/min"),
                    cls="trim-metrics-right",
                ),
                Div(
                    ToggleSwitch("CW/CCW", b.trim.cw_ccw, id_key="tog-trim-cw", toggle_url="/api/toggle/ballast.trim.cw_ccw"),
                    cls="trim-toggle-col",
                ),
                cls="trim-metrics-row",
            ),
            cls="ballast-trim-panel",
        )

        # ---- OIM / SPEED CONTROL PANEL ----
        oim_panel = Div(
            SpeedControlSlider(b.trim.speed_control),
            Div(
                OIMToggleRow("OIM_S1_Ext_Reset", b.oim.s1_ext_reset, id_key="tog-oim-s1e", toggle_url="/api/toggle/ballast.oim.s1_ext_reset"),
                OIMToggleRow("OIM_S2_Int_Reset", b.oim.s2_int_reset, id_key="tog-oim-s2i", toggle_url="/api/toggle/ballast.oim.s2_int_reset"),
                OIMToggleRow("OIM_P1_Ext_Reset", b.oim.p1_ext_reset, id_key="tog-oim-p1e", toggle_url="/api/toggle/ballast.oim.p1_ext_reset"),
                OIMToggleRow("OIM_P2_Int_Reset", b.oim.p2_int_reset, id_key="tog-oim-p2i", toggle_url="/api/toggle/ballast.oim.p2_int_reset"),
                cls="oim-toggles-col",
            ),
            cls="ballast-oim-panel",
        )

        main_content_area = Div(
            Div(
                Div(
                    Div(main_ballast_panel, vbs_panel, cls="ballast-top-row"),
                    Div(trim_panel, oim_panel, cls="ballast-bottom-row"),
                    cls="ballast-content-col",
                ),
                sidebar_col,
                cls="main-content",
            ),
            cls="main-content-wrapper",
        )

    elif active_tab == "Propulsion":
        pd = s.propulsion_detail

        # Left half: T2, T4 (port side thrusters)
        left_col = Div(
            ThrusterPanel(2, pd.t2),
            ThrusterPanel(4, pd.t4),
            cls="prop-thruster-col",
        )

        # Second left: T6, T8 (port aft)
        mid_left_col = Div(
            ThrusterPanel(6, pd.t6),
            ThrusterPanel(8, pd.t8),
            cls="prop-thruster-col",
        )

        # Center column: Power/Enable toggles for all 8 thrusters
        center_col = Div(
            Div("POWER / ENABLE", cls="prop-center-header"),
            PropCenterToggleBlock(2, pd.t2.power, pd.t2.enable, toggle_url_p="/api/toggle/propulsion_detail.t2.power", toggle_url_e="/api/toggle/propulsion_detail.t2.enable"),
            PropCenterToggleBlock(6, pd.t6.power, pd.t6.enable, toggle_url_p="/api/toggle/propulsion_detail.t6.power", toggle_url_e="/api/toggle/propulsion_detail.t6.enable"),
            PropCenterToggleBlock(5, pd.t5.power, pd.t5.enable, toggle_url_p="/api/toggle/propulsion_detail.t5.power", toggle_url_e="/api/toggle/propulsion_detail.t5.enable"),
            PropCenterToggleBlock(1, pd.t1.power, pd.t1.enable, toggle_url_p="/api/toggle/propulsion_detail.t1.power", toggle_url_e="/api/toggle/propulsion_detail.t1.enable"),
            PropCenterToggleBlock(4, pd.t4.power, pd.t4.enable, toggle_url_p="/api/toggle/propulsion_detail.t4.power", toggle_url_e="/api/toggle/propulsion_detail.t4.enable"),
            PropCenterToggleBlock(8, pd.t8.power, pd.t8.enable, toggle_url_p="/api/toggle/propulsion_detail.t8.power", toggle_url_e="/api/toggle/propulsion_detail.t8.enable"),
            PropCenterToggleBlock(7, pd.t7.power, pd.t7.enable, toggle_url_p="/api/toggle/propulsion_detail.t7.power", toggle_url_e="/api/toggle/propulsion_detail.t7.enable"),
            PropCenterToggleBlock(3, pd.t3.power, pd.t3.enable, toggle_url_p="/api/toggle/propulsion_detail.t3.power", toggle_url_e="/api/toggle/propulsion_detail.t3.enable"),
            cls="prop-center-col",
        )

        # Mid right: T5, T7
        mid_right_col = Div(
            ThrusterPanel(5, pd.t5),
            ThrusterPanel(7, pd.t7),
            cls="prop-thruster-col",
        )

        # Right col: T1, T3
        right_col = Div(
            ThrusterPanel(1, pd.t1),
            ThrusterPanel(3, pd.t3),
            cls="prop-thruster-col",
        )

        main_content_area = Div(
            Div(
                Div(
                    left_col,
                    mid_left_col,
                    center_col,
                    mid_right_col,
                    right_col,
                    sidebar_col,
                    cls="main-content",
                ),
                # Bottom axis control strip
                Div(
                    PropAxisControl("Heading ctrl", pd.heading_ctrl),
                    PropAxisControl("Fwd ctrl", pd.fwd_ctrl),
                    PropAxisControl("Lat ctrl", pd.lat_ctrl),
                    PropAxisControl("Vertical ctrl", pd.vertical_ctrl),
                    Div(
                        Span("🐢", cls="prop-speed-icon"),
                        Span(str(pd.speed_factor), cls="prop-speed-value"),
                        Span("speed factor", cls="prop-speed-label"),
                        cls="prop-speed-factor",
                    ),
                    cls="prop-bottom-strip",
                ),
                cls="prop-content-wrapper",
            ),
            cls="main-content-wrapper",
        )

    elif active_tab == "POWER":
        p = s.power
        
        row1 = Div(
            BatteryPanel("MB_P", "MB_P", p.mb_p, ["100", "120", "140", "160", "180"], 100, 180),
            BatteryPanel("AUX_P", "AUX_P", p.aux_p, ["0", "10", "20", "30", "40"], 0, 40),
            BatteryPanel("MB_S", "MB_S", p.mb_s, ["100", "120", "140", "160", "180"], 100, 180),
            BatteryPanel("AUX_S", "AUX_S", p.aux_s, ["0", "10", "20", "30", "40"], 0, 40),
            cls="power-row"
        )
        
        row2 = Div(
            PDEPanel("PDE_P", "PDE_P", p.pde_p),
            IDEPanel("IDE_P", "IDE_P", p.ide_p),
            PDEPanel("PDE_S", "PDE_S", p.pde_s),
            IDEPanel("IDE_S", "IDE_S", p.ide_s),
            cls="power-row"
        )
        
        row3 = Div(
            UmbilicalPanel("UB_Port", "PSP", p.ub_port),
            UmbilicalPanel("UB_Stbd", "PSS", p.ub_stbd),
            cls="power-row power-row-bottom"
        )

        main_content_area = Div(
            Div(
                Div(row1, row2, row3, cls="power-grid-container"),
                sidebar_col,
                cls="main-content",
            ),
            cls="main-content-wrapper",
        )

    elif active_tab == "Imaging":
        img = s.imaging
        
        # Left Part (LEDs + Cameras)
        led_p_col = Div(
            Div(
                ImagingToggle("LED P1", img.led_p1.power, id_key="tog-led-p1", toggle_url="/api/toggle/imaging.led_p1.power"),
                ImagingToggle("LED P2", img.led_p2.power, id_key="tog-led-p2", toggle_url="/api/toggle/imaging.led_p2.power"),
                ImagingToggle("LED P3", img.led_p3.power, id_key="tog-led-p3", toggle_url="/api/toggle/imaging.led_p3.power"),
                cls="img-toggle-block"
            ),
            Div(
                LedDimmerSlider("led 3 Dim%(10x)", img.led_p1.dim),
                LedDimmerSlider("led 5 Dim%(10x)", img.led_p2.dim),
                LedDimmerSlider("led 7 Dim%(10x)", img.led_p3.dim),
                cls="img-toggle-block"
            ),
            cls="img-led-row"
        )
        
        led_s_col = Div(
            Div(
                ImagingToggle("LED S1", img.led_s1.power, id_key="tog-led-s1", toggle_url="/api/toggle/imaging.led_s1.power"),
                ImagingToggle("LED S2", img.led_s2.power, id_key="tog-led-s2", toggle_url="/api/toggle/imaging.led_s2.power"),
                ImagingToggle("LED S3", img.led_s3.power, id_key="tog-led-s3", toggle_url="/api/toggle/imaging.led_s3.power"),
                cls="img-toggle-block"
            ),
            Div(
                LedDimmerSlider("led 4 Dim%(10x)", img.led_s1.dim),
                LedDimmerSlider("led 6 Dim%(10x)", img.led_s2.dim),
                LedDimmerSlider("led 8 Dim%(10x)", img.led_s3.dim),
                cls="img-toggle-block" 
            ),
            cls="img-led-row"
        )
        
        led_section = Div(
            Div("LED Controls", cls="img-panel-title"),
            Div(
                Div(Div("Underwater LED_P", style="font-size:12px; font-weight:700; color:var(--color-text); text-align:center;"), led_p_col, cls="img-col-main"),
                Div(Div("Underwater LED_S", style="font-size:12px; font-weight:700; color:var(--color-text); text-align:center;"), led_s_col, cls="img-col-main"),
                cls="img-top-row"
            ),
            cls="img-panel"
        )
        
        # Camera Panel
        cam_section = Div(
            Div("Camera Controls", cls="img-panel-title"),
            Div(
                # Camera P col
                Div(
                    ImagingToggle("HD camera P", img.hd_camera_p, inline=True, id_key="tog-hd-cam-p", toggle_url="/api/toggle/imaging.hd_camera_p"),
                    Div(
                        Div(
                            ImagingToggle("HD SDI_P1", img.hd_sdi_p1, id_key="tog-hd-sdi-p1", toggle_url="/api/toggle/imaging.hd_sdi_p1"),
                            ImagingToggle("HD SDI_P2", img.hd_sdi_p2, id_key="tog-hd-sdi-p2", toggle_url="/api/toggle/imaging.hd_sdi_p2"),
                            cls="sdi-col"
                        ),
                        Div(
                            ImagingToggle("HD SDI_P3", img.hd_sdi_p3, id_key="tog-hd-sdi-p3", toggle_url="/api/toggle/imaging.hd_sdi_p3"),
                            ImagingToggle("HD SDI_P4", img.hd_sdi_p4, id_key="tog-hd-sdi-p4", toggle_url="/api/toggle/imaging.hd_sdi_p4"),
                            cls="sdi-col"
                        ),
                        cls="sdi-grid"
                    ),
                    Div("HD Camera_P", style="font-size:14px; font-weight:800; color:var(--color-text); text-align:center; margin-bottom:8px;"),
                    CameraActionGrid(),
                    cls="img-cam-col"
                ),
                # Camera S col
                Div(
                    ImagingToggle("HD camera S", img.hd_camera_s, inline=True, id_key="tog-hd-cam-s", toggle_url="/api/toggle/imaging.hd_camera_s"),
                    Div(
                        Div(
                            ImagingToggle("HD Camera S2", img.hd_camera_s2, inline=True, id_key="tog-hd-cam-s2", toggle_url="/api/toggle/imaging.hd_camera_s2"),
                            ImagingToggle("HD SDI_S1", img.hd_sdi_s1, inline=True, id_key="tog-hd-sdi-s1", toggle_url="/api/toggle/imaging.hd_sdi_s1"),
                            cls="sdi-col"
                        ),
                        Div(
                            ImagingToggle("HD SDI_S2", img.hd_sdi_s2, inline=True, id_key="tog-hd-sdi-s2", toggle_url="/api/toggle/imaging.hd_sdi_s2"),
                            ImagingToggle("HD SDI_S3", img.hd_sdi_s3, inline=True, id_key="tog-hd-sdi-s3", toggle_url="/api/toggle/imaging.hd_sdi_s3"),
                            cls="sdi-col"
                        ),
                        cls="sdi-grid"
                    ),
                    Div("HD Camera _S", style="font-size:14px; font-weight:800; color:var(--color-text); text-align:center; margin-bottom:8px;"),
                    CameraActionGrid(),
                    cls="img-cam-col"
                ),
                cls="img-cam-grid"
            ),
            cls="img-panel"
        )
        
        left_col = Div(led_section, cam_section, cls="img-col-main")
        
        # Right Part (Pan/Tilt)
        pt = img.pt_p1
        right_col = Div(
            Div(
                PanTiltBar("PAN", pt.pan, -170, 170, ["-170", "-100", "0", "100", "170"]),
                PanTiltBar("TILT", pt.tilt, -50, 110, ["-50", "0", "50", "110"]),
                cls="img-panel img-pt-panel"
            ),
            Div(
                Div(
                    Div("Pan&Tilt P1", cls="pt-tab active"),
                    Div("Pan &Tilt S1", cls="pt-tab"),
                    Div("Pan& Tilt S2", cls="pt-tab"),
                    cls="pt-tabs-row"
                ),
                Div("PnT CTRL P1", style="font-size:14px; font-weight:800; color:var(--color-text); padding:10px 0 0 0; text-align:center;"),
                PanTiltPad(pt.pan, pt.tilt),
                cls="img-panel", style="margin-top:0;"
            ),
            cls="img-col-right"
        )
        
        main_content_area = Div(
            Div(
                Div(left_col, right_col, cls="img-layout-row"),
                sidebar_col,
                cls="main-content"
            ),
            cls="main-content-wrapper"
        )

    elif active_tab == "Sensors":
        sens = s.sensors
        
        port_toggles = Div(
            Div("Port side", cls="sens-panel-title"),
            SensorToggleBlock("Depth Sensor Pri", sens.toggles.depth_sensor_pri, id_key="tog-sens-ds-pri", toggle_url="/api/toggle/sensors.toggles.depth_sensor_pri"),
            SensorToggleBlock("INS", sens.toggles.ins, id_key="tog-sens-ins", toggle_url="/api/toggle/sensors.toggles.ins"),
            SensorToggleBlock("CTDO", sens.toggles.ctdo, id_key="tog-sens-ctdo", toggle_url="/api/toggle/sensors.toggles.ctdo"),
            SensorToggleBlock("DVL", sens.toggles.dvl, id_key="tog-sens-dvl", toggle_url="/api/toggle/sensors.toggles.dvl"),
            SensorToggleBlock("Multibeam Sonar", sens.toggles.multibeam_sonar, id_key="tog-sens-mbs1", toggle_url="/api/toggle/sensors.toggles.multibeam_sonar"),
            cls="sens-panel"
        )
        stbd_toggles = Div(
            Div("Starboard", cls="sens-panel-title"),
            SensorToggleBlock("Altimeter", sens.toggles.altimeter, id_key="tog-sens-alt", toggle_url="/api/toggle/sensors.toggles.altimeter"),
            SensorToggleBlock("Dissolved O2", sens.toggles.dissolved_o2, id_key="tog-sens-do2", toggle_url="/api/toggle/sensors.toggles.dissolved_o2"),
            SensorToggleBlock("CTDO_S", sens.toggles.ctdo_s, id_key="tog-sens-ctdo-s", toggle_url="/api/toggle/sensors.toggles.ctdo_s"),
            SensorToggleBlock("MBS", sens.toggles.mbs, id_key="tog-sens-mbs2", toggle_url="/api/toggle/sensors.toggles.mbs"),
            SensorToggleBlock("IMG SONAR", sens.toggles.img_sonar, id_key="tog-sens-img-sonar", toggle_url="/api/toggle/sensors.toggles.img_sonar"),
            cls="sens-panel"
        )
        
        wi_p = Div(
            Div("Water Ingress_p", cls="sens-panel-title"),
            SensorLedStatus("WI PS_P", sens.indicators.wi_ps_p),
            SensorLedStatus("WI IDE_P", sens.indicators.wi_ide_p),
            SensorLedStatus("WI PDE_P", sens.indicators.wi_pde_p),
            cls="sens-panel sens-panel-clear"
        )
        
        ins_p = Div(
            Div("Insulation_P", cls="sens-panel-title"),
            SensorLedStatus("IR UB_P", sens.indicators.ir_ub_p),
            SensorLedStatus("IR IDE_P", sens.indicators.ir_ide_p),
            SensorLedStatus("IR PDE_P INT", sens.indicators.ir_pde_p_int),
            SensorLedStatus("IR PDE_P EXT", sens.indicators.ir_pde_p_ext),
            SensorLedStatus("IR PDE 148_P", sens.indicators.ir_pde_148_p),
            cls="sens-panel sens-panel-clear"
        )

        sensor_alarm_p = Div(
            Div("Sensor Alarm", cls="sens-panel-title"),
            AlarmLedStatus("O2 alarm", sens.indicators.o2_alarm),
            AlarmLedStatus("Co2 alarm", sens.indicators.co2_alarm),
            AlarmLedStatus("Pressure 2", sens.indicators.pressure_2),
            AlarmLedStatus("Altitude_P", sens.indicators.altitude_p),
            AlarmLedStatus("Depth alarm", sens.indicators.depth_alarm),
            cls="sens-panel sens-panel-clear"
        )
        
        warning_panel = Div(
            Div("Warning and Alarm Panel", cls="warning-panel-title"),
            Div(
                BuzzerPanel(sens.buzzer_active),
                Div(
                    SensorToggleBlock("Laser Light 2", sens.toggles.laser_light_2, id_key="tog-sens-ll2", toggle_url="/api/toggle/sensors.toggles.laser_light_2"),
                    SensorToggleBlock("Pan and Tilt P1", sens.toggles.pan_and_tilt_p1, id_key="tog-sens-pt-p1", toggle_url="/api/toggle/sensors.toggles.pan_and_tilt_p1"),
                    SensorToggleBlock("Pan and Tilt S1", sens.toggles.pan_and_tilt_s1, id_key="tog-sens-pt-s1", toggle_url="/api/toggle/sensors.toggles.pan_and_tilt_s1"),
                    SensorToggleBlock("Pan and Tilt S2", sens.toggles.pan_and_tilt_s2, id_key="tog-sens-pt-s2", toggle_url="/api/toggle/sensors.toggles.pan_and_tilt_s2"),
                    cls="warning-toggles"
                ),
                cls="warning-panel-content"
            ),
            cls="warning-panel-section"
        )
        
        ins_s = Div(
            Div("Insulation_S", cls="sens-panel-title"),
            SensorLedStatus("IR UB_S", sens.indicators.ir_ub_s),
            SensorLedStatus("IR IDE_S", sens.indicators.ir_ide_s),
            SensorLedStatus("IR PDE_S INT", sens.indicators.ir_pde_s_int),
            SensorLedStatus("IR PDE_S EXT", sens.indicators.ir_pde_s_ext),
            SensorLedStatus("IR PDE 148_S", sens.indicators.ir_pde_148_s),
            cls="sens-panel sens-panel-clear"
        )
        wi_s = Div(
            Div("Water Ingress_S", cls="sens-panel-title"),
            SensorLedStatus("WI PS_S", sens.indicators.wi_ps_s),
            SensorLedStatus("WI IDE_S", sens.indicators.wi_ide_s),
            SensorLedStatus("WI PDE_S", sens.indicators.wi_pde_s),
            cls="sens-panel sens-panel-clear"
        )
        
        sci = sens.scientific
        sci_table = Div(
            Div(
                Span("CTDO Sensor", cls="sci-sens-header-sub"),
                Span("Scientific Sensors", cls="sci-sens-main-title"),
                cls="sci-sens-top"
            ),
            Div(
                Span("", cls="sci-sens-th"),
                Span("Port", cls="sci-sens-th text-center"),
                Span("Stbd", cls="sci-sens-th text-center"),
                Span("", cls="sci-sens-th"),
                cls="sci-sens-table-header"
            ),
            ScientificSensorRowItem("Conductivity", sci.conductivity.port, sci.conductivity.stbd, "S/m"),
            ScientificSensorRowItem("Salinity", sci.salinity.port, sci.salinity.stbd, "PSU"),
            ScientificSensorRowItem("Water denisty", sci.water_density.port, sci.water_density.stbd, "kg/m3"),
            ScientificSensorRowItem("Turbidity", sci.turbidity.port, sci.turbidity.stbd, "NTU"),
            ScientificSensorRowItem("pH", sci.ph.port, sci.ph.stbd, ""),
            ScientificSensorRowItem("CTD Temp", sci.ctd_temp.port, sci.ctd_temp.stbd, "DegC"),
            ScientificSensorRowItem("Pressure", sci.pressure.port, sci.pressure.stbd, ""),
            ScientificSensorRowItem("Dissolved Oxygen", sci.dissolved_oxygen.port, sci.dissolved_oxygen.stbd, "uM"),
            ScientificSensorRowItem("ORP", sci.orp.port, sci.orp.stbd, ""),
            cls="sci-sens-table"
        )
        
        surf = sens.surface_ins
        surf_ins_panel = Div(
            Div("Surface INS", cls="sens-right-title"),
            SensorBoxMetric("S_Roll", surf.s_roll, "deg"),
            SensorBoxMetric("S_Pitch", surf.s_pitch, "deg"),
            SensorBoxMetric("S_Heading", surf.s_heading, "deg"),
            SensorBoxMetric("S_Speed1", surf.s_speed1, "m/s"),
            SensorBoxMetric("S_Speed2", surf.s_speed2, "m/s"),
            SensorBoxMetric("S_Speed3", surf.s_speed3, "m/s"),
            SensorBoxMetric("S_Latitude", surf.s_latitude, ""),
            SensorBoxMetric("S_Longitude", surf.s_longitude, ""),
            cls="sens-right-panel"
        )
        
        ssg = sens.subsea_gps
        subsea_panel = Div(
            Div("SubSea GPS", cls="sens-right-title"),
            SensorBoxMetric("GPS Latitude", ssg.gps_latitude, ""),
            SensorBoxMetric("GPS Longitude", ssg.gps_longitude, ""),
            cls="sens-right-panel sens-subsea"
        )
        
        redt = sens.redt_depth
        redt_panel = Div(
            Div("Redt Depth Sensor", cls="sens-right-title"),
            SensorBoxMetric("S_Depth", redt.s_depth, "m"),
            cls="sens-right-panel sens-redt"
        )

        top_row = Div(
            Div(port_toggles, stbd_toggles, cls="sens-toggles-pair"),
            sci_table,
            Div(surf_ins_panel, subsea_panel, redt_panel, cls="sens-right-stack"),
            cls="sens-top-area"
        )
        
        bottom_row = Div(
            wi_p, ins_p, sensor_alarm_p, warning_panel, ins_s, wi_s,
            cls="sens-bottom-area"
        )
        
        main_content_area = Div(
            Div(
                Div(top_row, bottom_row, cls="sens-dashboard"),
                sidebar_col,
                cls="main-content"
            ),
            cls="main-content-wrapper"
        )

    elif active_tab == "Logging":
        log_state = s.logging
        t = log_state.toggles

        # ---- TOP: Events and Errors Tables ----
        tables_row = Div(
            LogTable("Event Logging", True, log_state.events),
            LogTable("Error Logging", False, log_state.errors),
            cls="logging-tables-row"
        )
        
        # ---- BOTTOM: Toggles and LEDs Panel ----
        toggles_left = Div(
            Div(
                HorizontalToggle("148 V LED S1", t.led_s1_148v, id_key="tog-log-led-s1", toggle_url="/api/toggle/logging.toggles.led_s1_148v"),
                HorizontalToggle("148 V LED S2", t.led_s2_148v, id_key="tog-log-led-s2", toggle_url="/api/toggle/logging.toggles.led_s2_148v"),
                cls="log-tog-col"
            ),
            Div(
                HorizontalToggle("148 V LED S3", t.led_s3_148v, id_key="tog-log-led-s3", toggle_url="/api/toggle/logging.toggles.led_s3_148v"),
                HorizontalToggle("148 V LED S4", t.led_s4_148v, id_key="tog-log-led-s4", toggle_url="/api/toggle/logging.toggles.led_s4_148v"),
                cls="log-tog-col"
            ),
            Div(
                HorizontalToggle("148 V LED P1", t.led_p1_148v, id_key="tog-log-led-p1", toggle_url="/api/toggle/logging.toggles.led_p1_148v"),
                HorizontalToggle("148 V LED P2", t.led_p2_148v, id_key="tog-log-led-p2", toggle_url="/api/toggle/logging.toggles.led_p2_148v"),
                cls="log-tog-col"
            ),
            Div(
                HorizontalToggle("148 V LED P3", t.led_p3_148v, id_key="tog-log-led-p3", toggle_url="/api/toggle/logging.toggles.led_p3_148v"),
                HorizontalToggle("148 V LED P4", t.led_p4_148v, id_key="tog-log-led-p4", toggle_url="/api/toggle/logging.toggles.led_p4_148v"),
                cls="log-tog-col"
            ),
            cls="log-toggles-left"
        )
        
        toggles_right = Div(
            Div(
                HorizontalToggle("Trim_S", t.trim_s, id_key="tog-log-trim-s", toggle_url="/api/toggle/logging.toggles.trim_s"),
                RedSignalIndicator("Trim_S signal", t.trim_s_signal),
                cls="log-tog-group"
            ),
            Div(
                HorizontalToggle("PDE_P 1", t.pde_p_1, id_key="tog-log-pde-1", toggle_url="/api/toggle/logging.toggles.pde_p_1"),
                RedSignalIndicator("PDE_P signal", t.pde_p_signal),
                HorizontalToggle("PDE_P 2", t.pde_p_2, id_key="tog-log-pde-2", toggle_url="/api/toggle/logging.toggles.pde_p_2"),
                cls="log-tog-group-center"
            ),
            Div(
                HorizontalToggle("Trim_P", t.trim_p, id_key="tog-log-trim-p", toggle_url="/api/toggle/logging.toggles.trim_p"),
                RedSignalIndicator("Trim_P signal", t.trim_p_signal),
                cls="log-tog-group"
            ),
            cls="log-toggles-right"
        )
        
        toggles_panel = Div(
            toggles_left,
            toggles_right,
            cls="log-toggles-panel"
        )

        main_content_area = Div(
            Div(
                Div(tables_row, toggles_panel, cls="logging-dashboard"),
                sidebar_col,
                cls="main-content"
            ),
            cls="main-content-wrapper"
        )

    elif active_tab == "Status":
        status_state = s.status
        
        row1 = StatusChartRowComponent(
            status_state.chart1_selection,
            [-45, -20, 0, 20, 45],
            [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 57]
        )
        
        row2 = StatusChartRowComponent(
            status_state.chart2_selection,
            [-15, -10, 0, 10, 15],
            [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 57]
        )
        
        main_content_area = Div(
            Div(
                Div(row1, row2, cls="status-dashboard"),
                sidebar_col,
                cls="main-content"
            ),
            cls="main-content-wrapper"
        )

    elif active_tab == "50 Kwh":
        kwh = s.kwh
        
        # Extracted lists of batteries
        port_bats = [kwh.port.bat1, kwh.port.bat2, kwh.port.bat3, kwh.port.bat4, kwh.port.bat5]
        stbd_bats = [kwh.stbd.bat6, kwh.stbd.bat7, kwh.stbd.bat8, kwh.stbd.bat9, kwh.stbd.bat10]
        
        port_grid = KwhDataGrid("port side", ["BAT 1", "BAT 2", "BAT 3", "BAT 4", "BAT 5"], port_bats)
        stbd_grid = KwhDataGrid("starboard side", ["BAT 6", "BAT 7", "BAT 8", "BAT 9", "BAT 10"], stbd_bats)
        
        # Center section between grids
        center_toggles = Div(
            RedSignalIndicator("VBS_Enable_sig", kwh.vbs_enable_sig),
            RedSignalIndicator("Trim_Enable_sig", kwh.trim_enable_sig),
            HorizontalToggle("Trim_Enable", kwh.trim_enable),
            cls="kwh-center-toggles" # We'll need to style this to have labels left of the dots
        )
        # Actually in the picture, Trim_Enable is just a normal switch with label above
        
        center_toggles = Div(
            Div(
                Div("VBS_Enable_sig", cls="kwh-sig-label"),
                Div(cls=f"kwh-sig-dot {'signal-dot-on' if kwh.vbs_enable_sig else 'signal-dot-off'}"),
                cls="kwh-sig-row"
            ),
            Div(
                Div("Trim_Enable_sig", cls="kwh-sig-label"),
                Div(cls=f"kwh-sig-dot {'signal-dot-on' if kwh.trim_enable_sig else 'signal-dot-off'}"),
                cls="kwh-sig-row"
            ),
            ToggleSwitch("Trim_Enable", kwh.trim_enable, id_key="tog-kwh-trim", toggle_url="/api/toggle/kwh.trim_enable"),
            cls="kwh-center-toggles"
        )

        top_section = Div(
            port_grid,
            center_toggles,
            stbd_grid,
            cls="kwh-top-section"
        )
        
        # Bottom section: gauges
        pg = kwh.port_gauges
        sg = kwh.stbd_gauges
        
        port_gauges_row = Div(
            KwhVerticalGauge("BAT VOL", pg.vol, 100, 170, [100, 120, 140, 160, 170]),
            KwhVerticalGauge("BAT TEMP", pg.temp, 0, 50, [0, 25, 50]),
            KwhVerticalGauge("BAT SOC", pg.soc, 0, 200, [0, 50, 100, 150, 200]),
            KwhVerticalGauge("BAT CUR", pg.cur, 0, 100, [0, 25, 50, 75, 100]),
            cls="kwh-gauges-row"
        )
        
        stbd_gauges_row = Div(
            KwhVerticalGauge("BAT VOL 2", sg.vol, 100, 170, [100, 120, 140, 160, 170]),
            KwhVerticalGauge("BAT TEMP 2", sg.temp, 0, 50, [0, 25, 50]),
            KwhVerticalGauge("BAT SOC 2", sg.soc, 0, 200, [0, 50, 100, 150, 200]),
            KwhVerticalGauge("BAT CUR 2", sg.cur, 0, 100, [0, 25, 50, 75, 100]),
            cls="kwh-gauges-row"
        )

        bottom_section = Div(
            port_gauges_row,
            Div(ToggleSwitch("VBS_Enable", kwh.vbs_enable, id_key="tog-kwh-vbs", toggle_url="/api/toggle/kwh.vbs_enable"), cls="kwh-bottom-center"),
            stbd_gauges_row,
            cls="kwh-bottom-section"
        )
        
        main_content_area = Div(
            Div(
                Div(
                    Div("BATTERY 50 kWh STATUS", cls="kwh-main-title"),
                    top_section, 
                    bottom_section, 
                    cls="kwh-dashboard"
                ),
                sidebar_col,
                cls="main-content"
            ),
            cls="main-content-wrapper"
        )

    elif active_tab == "MCC":
        mcc = s.mcc
        ind = mcc.indicators
        st = mcc.status
        
        col1 = Div(
            MccIndicator("CO2 Sensor-D", ind.co2_sensor_d),
            MccIndicator("Trim System-D", ind.trim_system_d),
            MccIndicator("Magnetometer-D", ind.magnetometer_d),
            MccIndicator("Conduct & Temp-D", ind.conduct_temp_d),
            MccIndicator("Thruster_T1-D", ind.thruster_t1_d),
            MccIndicator("Thruster_T2-D", ind.thruster_t2_d),
            MccIndicator("Thruster_En_P-D", ind.thruster_en_p_d),
            MccIndicator("Thruster_En_S-D", ind.thruster_en_s_d),
            MccIndicator("4K camera P-D", ind.camera_4k_p_d),
            MccIndicator("HD Camera P3-D", ind.hd_camera_p3_d),
            MccIndicator("SD_Camera_P4-D", ind.sd_camera_p4_d),
            MccIndicator("CTDO-D", ind.ctdo_d),
            cls="mcc-col"
        )
        
        col2 = Div(
            MccIndicator("Forwd_Low-D", ind.forwd_low_d),
            MccIndicator("Forwd_Medi-D", ind.forwd_medi_d),
            MccIndicator("Lateral_Low-D", ind.lateral_low_d),
            MccIndicator("Lateral_Medi-D", ind.lateral_medi_d),
            MccIndicator("Verti_Low-D", ind.verti_low_d),
            MccIndicator("Verti_Medi-D", ind.verti_medi_d),
            MccIndicator("Heading_Low-D", ind.heading_low_d),
            MccIndicator("Heading_Medi-D", ind.heading_medi_d),
            MccIndicator("4K camera S-D", ind.camera_4k_s_d),
            MccIndicator("HD Camera S1-D", ind.hd_camera_s1_d),
            MccIndicator("SD Camera S4-D", ind.sd_camera_s4_d),
            MccIndicator("Dissolved O2-D", ind.dissolved_o2_d),
            Div(
                Div("Data Receiving Mode", cls="mcc-disabled-label"),
                Div(st.data_receiving_mode, cls="mcc-disabled-box"),
                cls="mcc-disabled-wrap"
            ),
            cls="mcc-col"
        )

        col3 = Div(
            MccIndicator("LED Light S2-D", ind.led_light_s2_d),
            MccIndicator("LED Light S3-D", ind.led_light_s3_d),
            MccIndicator("LED Light S4-D", ind.led_light_s4_d),
            MccIndicator("INS-D", ind.ins_d),
            MccIndicator("DVL-D", ind.dvl_d),
            MccIndicator("Depth Sensor Pri-D", ind.depth_sensor_pri_d),
            MccIndicator("Altimeter-D", ind.altimeter_d),
            MccIndicator("LED Light P2-D", ind.led_light_p2_d),
            MccIndicator("LED Light P3-D", ind.led_light_p3_d),
            MccIndicator("LED Light P4-D", ind.led_light_p4_d),
            cls="mcc-col"
        )
        
        col4_center = Div(
            Div(
                MccStatusBox("Modem Ready Status", st.modem_ready_status, "mcc-bg-green"),
                MccStatusBox("Read/ Write", st.read_write, "mcc-bg-gray"),
                MccStatusBox("Data Sending Mode", st.data_sending_mode, "mcc-bg-gray"),
                cls="mcc-center-top"
            ),
            Div(
                ToggleSwitch("Acoustic comm Auto", st.acoustic_comm_auto),
                cls="mcc-center-toggle"
            ),
            Div(
                Div("MCC message", cls="mcc-msg-title"),
                Div(st.mcc_message, cls="mcc-msg-box"),
                Div("Pilot message", cls="mcc-msg-title"),
                Div(st.pilot_message, cls="mcc-msg-box"),
                cls="mcc-center-msg"
            ),
            Div(
                MccShipData("Ship Latitude", st.ship_latitude),
                MccShipData("Ship Longitude", st.ship_longitude),
                MccShipData("Ship Heading", st.ship_heading),
                MccShipData("Ship Time", st.ship_time),
                cls="mcc-center-ship"
            ),
            cls="mcc-col mcc-col-center"
        )
        
        col5_right = Div(
            MccRadioGroup(st.power_status),
            Div(
                MccCrewStatus("PILOT", st.pilot_ok),
                MccCrewStatus("CO-PILOT", st.copilot_ok),
                MccCrewStatus("OBSERVER", st.observer_ok),
                cls="mcc-crew-group"
            ),
            MccPowerDropdown(st.power_dropdown),
            Div(
                ToggleSwitch("data mode", st.data_mode),
                cls="mcc-right-toggle"
            ),
            cls="mcc-col mcc-col-right"
        )

        mcc_panel = Div(
            Div("Data from MCC", cls="mcc-panel-title"),
            Div(col1, col2, col3, col4_center, col5_right, cls="mcc-grid"),
            cls="mcc-panel"
        )

        main_content_area = Div(
            Div(
                mcc_panel,
                sidebar_col,
                cls="main-content"
            ),
            cls="main-content-wrapper"
        )

    else:
        main_content_area = Div(
            Div(
                H2(f"{active_tab} Tab Content", style="margin:auto;"),
                sidebar_col,
                cls="main-content",
            ),
            cls="main-content-wrapper",
        )

    # Combine everything
    return Div(
        HeaderArea(),
        main_content_area,
        BottomTabsNav(
            [
                "Main",
                "HSSS",
                "Ballast",
                "Propulsion",
                "POWER",
                "Imaging",
                "Sensors",
                "Logging",
                "Status",
                "50 Kwh",
                "MCC",
            ],
            active_tab=active_tab,
        ),
        id=f"dashboard-content-{active_tab.lower()}",
        cls="dashboard-root",
        hx_swap_oob="true",
    )


@rt("/")
def get():
    return Title("MATSYA 6000 View"), Div(
        AppLayout(active_tab="Main"), id="ws-container", hx_ext="ws", ws_connect="/ws"
    )


@rt("/hsss")
def get_hsss():
    return Title("MATSYA 6000 View - HSSS"), Div(
        AppLayout(active_tab="HSSS"), id="ws-container", hx_ext="ws", ws_connect="/ws"
    )


@rt("/ballast")
def get_ballast():
    return Title("MATSYA 6000 View - Ballast"), Div(
        AppLayout(active_tab="Ballast"), id="ws-container", hx_ext="ws", ws_connect="/ws"
    )


@rt("/propulsion")
def get_propulsion():
    return Title("MATSYA 6000 View - Propulsion"), Div(
        AppLayout(active_tab="Propulsion"), id="ws-container", hx_ext="ws", ws_connect="/ws"
    )


@rt("/power")
def get_power():
    return Title("MATSYA 6000 View - POWER"), Div(
        AppLayout(active_tab="POWER"), id="ws-container", hx_ext="ws", ws_connect="/ws"
    )


@rt("/imaging")
def get_imaging():
    return Title("MATSYA 6000 View - Imaging"), Div(
        AppLayout(active_tab="Imaging"), id="ws-container", hx_ext="ws", ws_connect="/ws"
    )


@rt("/sensors")
def get_sensors():
    return Title("MATSYA 6000 View - Sensors"), Div(
        AppLayout(active_tab="Sensors"), id="ws-container", hx_ext="ws", ws_connect="/ws"
    )

@rt("/logging")
def get_logging():
    return Title("MATSYA 6000 View - Logging"), Div(
        AppLayout(active_tab="Logging"), id="ws-container", hx_ext="ws", ws_connect="/ws"
    )

@rt("/status")
def get_status():
    return Title("MATSYA 6000 View - Status"), Div(
        AppLayout(active_tab="Status"), id="ws-container", hx_ext="ws", ws_connect="/ws"
    )

@rt("/50-kwh")
def get_50kwh():
    return Title("MATSYA 6000 View - 50 Kwh"), Div(
        AppLayout(active_tab="50 Kwh"), id="ws-container", hx_ext="ws", ws_connect="/ws"
    )

@rt("/mcc")
def get_mcc():
    return Title("MATSYA 6000 View - MCC"), Div(
        AppLayout(active_tab="MCC"), id="ws-container", hx_ext="ws", ws_connect="/ws"
    )


# ----------------- APIs -----------------

simulator_task = None


async def simulate_data():
    s = app_state
    while True:
        # Header
        s.header.mission_time = datetime.now().strftime("%H:%M:%S")
        s.header.present_time = datetime.now().strftime("%H:%M:%S")
        s.header.heading.value = round(
            (s.header.heading.value + random.uniform(-1, 1)) % 360, 1
        )
        s.header.depth.value = round(
            max(0, s.header.depth.value + random.uniform(-0.5, 0.5)), 1
        )
        s.header.altitude.value = round(
            max(0, s.header.altitude.value + random.uniform(-0.2, 0.2)), 1
        )
        s.header.mb_p_soc.value = round(
            max(0, min(100, s.header.mb_p_soc.value + random.uniform(-0.1, 0.1))), 1
        )
        s.header.mb_s_soc.value = round(
            max(0, min(100, s.header.mb_s_soc.value + random.uniform(-0.1, 0.1))), 1
        )

        # IMU
        s.imu.roll.value = round(s.imu.roll.value + random.uniform(-1, 1), 1)
        s.imu.pitch.value = round(s.imu.pitch.value + random.uniform(-1, 1), 1)
        s.imu.heading_p.value = s.header.heading.value

        # Bottom Strip
        s.bottom.east_speed.value = round(
            s.bottom.east_speed.value + random.uniform(-0.1, 0.1), 2
        )
        s.bottom.vert_speed.value = round(
            s.bottom.vert_speed.value + random.uniform(-0.1, 0.1), 2
        )
        s.bottom.north_speed.value = round(
            s.bottom.north_speed.value + random.uniform(-0.1, 0.1), 2
        )
        s.bottom.ship_heading.value = round(
            (s.bottom.ship_heading.value + random.uniform(-1, 1)) % 360, 1
        )

        # Propulsion
        for i in range(1, 9):
            current = getattr(s.propulsion, f"t{i}_rpm")
            setattr(
                s.propulsion,
                f"t{i}_rpm",
                round(max(0, current + random.uniform(-20, 20)), 0),
            )
        s.propulsion.latitude.value = round(
            s.propulsion.latitude.value + random.uniform(-0.0001, 0.0001), 4
        )
        s.propulsion.longitude.value = round(
            s.propulsion.longitude.value + random.uniform(-0.0001, 0.0001), 4
        )

        # Environment
        s.environment.o2.value = round(
            max(0, s.environment.o2.value + random.uniform(-0.01, 0.01)), 2
        )
        s.environment.co2.value = round(
            max(0, s.environment.co2.value + random.uniform(-0.5, 0.5)), 1
        )
        s.environment.temp.value = round(
            s.environment.temp.value + random.uniform(-0.1, 0.1), 1
        )
        s.environment.pressure.value = round(
            s.environment.pressure.value + random.uniform(-1, 1), 1
        )

        # Sidebar (less frequent toggle) (Removed for interactivity)
        # Leds (less frequent toggle) (Removed for interactivity)
        # Logging (Removed for interactivity)
        
        # 50 KWH
        kwh = s.kwh
        for k in ["bat1", "bat2", "bat3", "bat4", "bat5"]:
            b = getattr(kwh.port, k)
            b.cur = max(0, b.cur + random.uniform(-1, 1))
            b.vot = max(0, b.vot + random.uniform(-1, 1))
            b.temp = max(0, b.temp + random.uniform(-0.5, 0.5))
            b.soc = min(100, max(0, b.soc + random.uniform(-0.1, 0.1)))
        
        for k in ["bat6", "bat7", "bat8", "bat9", "bat10"]:
            b = getattr(kwh.stbd, k)
            b.cur = max(0, b.cur + random.uniform(-1, 1))
            b.vot = max(0, b.vot + random.uniform(-1, 1))
            b.temp = max(0, b.temp + random.uniform(-0.5, 0.5))
            b.soc = min(100, max(0, b.soc + random.uniform(-0.1, 0.1)))
            
        # (KWH toggles removed for interactivity)
        kwh.port_gauges.vol = min(170, max(100, kwh.port_gauges.vol + random.uniform(-2, 2)))
        kwh.port_gauges.temp = min(50, max(0, kwh.port_gauges.temp + random.uniform(-1, 1)))
        kwh.port_gauges.soc = min(200, max(0, kwh.port_gauges.soc + random.uniform(-2, 2)))
        kwh.port_gauges.cur = min(100, max(0, kwh.port_gauges.cur + random.uniform(-1, 1)))

        kwh.stbd_gauges.vol = min(170, max(100, kwh.stbd_gauges.vol + random.uniform(-2, 2)))
        kwh.stbd_gauges.temp = min(50, max(0, kwh.stbd_gauges.temp + random.uniform(-1, 1)))
        kwh.stbd_gauges.soc = min(200, max(0, kwh.stbd_gauges.soc + random.uniform(-2, 2)))
        kwh.stbd_gauges.cur = min(100, max(0, kwh.stbd_gauges.cur + random.uniform(-1, 1)))

        # HSSS Panel Simulation
        for side in [s.hsss.p, s.hsss.s]:
            side.co2.value = round(max(0, side.co2.value + random.uniform(-10, 10)), 1)
            side.oxygen.value = round(
                max(19, min(25, side.oxygen.value + random.uniform(-0.05, 0.05))), 1
            )
            side.pressure.value = round(
                max(0, side.pressure.value + random.uniform(-1, 1)), 1
            )
            side.temp.value = round(
                max(0, side.temp.value + random.uniform(-0.2, 0.2)), 1
            )
            side.humidity.value = round(
                max(0, min(100, side.humidity.value + random.uniform(-0.5, 0.5))), 1
            )
            side.hydrogen.value = round(
                max(0, side.hydrogen.value + random.uniform(-0.1, 0.1)), 1
            )
            side.lp_l_pressure.value = round(
                max(0, side.lp_l_pressure.value + random.uniform(-0.1, 0.1)), 1
            )
            side.hp_b1_pressure.value = round(
                max(0, side.hp_b1_pressure.value + random.uniform(-0.1, 0.1)), 1
            )
            side.hp_b2_pressure.value = round(
                max(0, side.hp_b2_pressure.value + random.uniform(-0.1, 0.1)), 1
            )
            side.hp_b3_pressure.value = round(
                max(0, side.hp_b3_pressure.value + random.uniform(-0.1, 0.1)), 1
            )

        # Ballast Simulation
        b = s.ballast
        for attr in ["act3_pos", "act3_pos2", "act3_pos3"]:
            current = getattr(b.main_ballast, attr)
            setattr(b.main_ballast, attr, round(max(-150, min(150, current + random.uniform(-2, 2))), 1))
        b.main_ballast.read_pressure_s = round(max(0, b.main_ballast.read_pressure_s + random.uniform(-0.5, 0.5)), 1)
        b.main_ballast.read_pressure_p = round(max(0, b.main_ballast.read_pressure_p + random.uniform(-0.5, 0.5)), 1)
        b.vbs.hpu_pressure.value = round(max(0, b.vbs.hpu_pressure.value + random.uniform(-1, 1)), 1)
        b.vbs.hpu_temp.value = round(max(0, b.vbs.hpu_temp.value + random.uniform(-0.2, 0.2)), 1)
        b.vbs.tank_level = round(max(0, min(300, b.vbs.tank_level + random.uniform(-1, 1))), 1)
        b.trim.position_mm = round(max(0, min(4500, b.trim.position_mm + random.uniform(-10, 10))), 1)
        b.trim.voltage.value = round(max(0, b.trim.voltage.value + random.uniform(-0.1, 0.1)), 1)
        b.trim.current.value = round(max(0, b.trim.current.value + random.uniform(-0.05, 0.05)), 2)
        b.trim.temp.value = round(max(0, b.trim.temp.value + random.uniform(-0.1, 0.1)), 1)
        b.trim.speed.value = round(max(0, b.trim.speed.value + random.uniform(-1, 1)), 1)

        # Propulsion detail simulation
        pd = s.propulsion_detail
        for tid in ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"]:
            t = getattr(pd, tid)
            t.rpm = round(max(0, min(1600, t.rpm + random.uniform(-30, 30))), 0)
            t.voltage = round(max(0, min(50, t.voltage + random.uniform(-0.1, 0.1))), 1)
            t.current = round(max(0, min(30, t.current + random.uniform(-0.05, 0.05))), 2)
            t.temp = round(max(0, min(120, t.temp + random.uniform(-0.2, 0.2))), 1)
            t.ctrl = round(max(-100, min(100, t.ctrl + random.uniform(-1, 1))), 1)
            # (power/enable toggles removed for interactivity)
        pd.heading_ctrl = round(max(-180, min(180, pd.heading_ctrl + random.uniform(-0.5, 0.5))), 1)
        pd.fwd_ctrl = round(max(-100, min(100, pd.fwd_ctrl + random.uniform(-0.5, 0.5))), 1)
        pd.lat_ctrl = round(max(-100, min(100, pd.lat_ctrl + random.uniform(-0.5, 0.5))), 1)
        pd.vertical_ctrl = round(max(-100, min(100, pd.vertical_ctrl + random.uniform(-0.5, 0.5))), 1)
        
        # Power Simulation
        p = s.power
        for bat in [p.mb_p, p.mb_s]:
            bat.voltage.value = round(max(100, min(180, bat.voltage.value + random.uniform(-1, 1))), 1)
            bat.current.value = round(max(0, bat.current.value + random.uniform(-0.5, 0.5)), 1)
            bat.power.value = round(max(0, bat.power.value + random.uniform(-0.1, 0.1)), 2)
            bat.soc.value = round(max(0, min(100, bat.soc.value + random.uniform(-0.1, 0.1))), 2)
            bat.temp.value = round(max(0, bat.temp.value + random.uniform(-0.2, 0.2)), 2)
            
        for bat in [p.aux_p, p.aux_s]:
            bat.voltage.value = round(max(0, min(40, bat.voltage.value + random.uniform(-0.5, 0.5))), 1)
            bat.current.value = round(max(0, bat.current.value + random.uniform(-0.5, 0.5)), 1)
            bat.power.value = round(max(0, bat.power.value + random.uniform(-0.1, 0.1)), 2)
            bat.soc.value = round(max(0, min(100, bat.soc.value + random.uniform(-0.1, 0.1))), 2)
            bat.temp.value = round(max(0, bat.temp.value + random.uniform(-0.2, 0.2)), 2)

        for enc in [p.pde_p, p.pde_s]:
            enc.voltage.value = round(max(0, enc.voltage.value + random.uniform(-0.5, 0.5)), 1)
            enc.current.value = round(max(0, enc.current.value + random.uniform(-0.5, 0.5)), 1)
            enc.temp.value = round(max(0, enc.temp.value + random.uniform(-0.2, 0.2)), 2)
            enc.ir_24.value = round(max(0, enc.ir_24.value + random.uniform(-0.1, 0.1)), 2)
            enc.ir_ext.value = round(max(0, enc.ir_ext.value + random.uniform(-0.1, 0.1)), 2)
            enc.ir_148.value = round(max(0, enc.ir_148.value + random.uniform(-0.1, 0.1)), 2)

        for enc in [p.ide_p, p.ide_s]:
            enc.voltage.value = round(max(0, enc.voltage.value + random.uniform(-0.5, 0.5)), 2)
            enc.current.value = round(max(0, enc.current.value + random.uniform(-0.5, 0.5)), 1)
            enc.temp.value = round(max(0, enc.temp.value + random.uniform(-0.2, 0.2)), 2)
            enc.ir.value = round(max(0, enc.ir.value + random.uniform(-0.1, 0.1)), 2)

        for ub in [p.ub_port, p.ub_stbd]:
            ub.voltage.value = round(max(0, ub.voltage.value + random.uniform(-0.5, 0.5)), 1)
            ub.current.value = round(max(0, ub.current.value + random.uniform(-0.5, 0.5)), 2)
            ub.temp.value = round(max(0, ub.temp.value + random.uniform(-0.2, 0.2)), 2)
            ub.ir.value = round(max(0, ub.ir.value + random.uniform(-0.1, 0.1)), 2)

        # Imaging Simulation
        img = s.imaging
        for l in [img.led_p1, img.led_p2, img.led_p3, img.led_s1, img.led_s2, img.led_s3]:
            # (power toggles removed for interactivity)
            l.dim = round(max(0, min(10, l.dim + random.uniform(-0.5, 0.5))), 1)

        # (Camera toggles removed for interactivity)

        for pt in [img.pt_p1, img.pt_s1, img.pt_s2]:
            pt.pan = round(max(-170, min(170, pt.pan + random.uniform(-5, 5))), 1)
            pt.tilt = round(max(-50, min(110, pt.tilt + random.uniform(-5, 5))), 1)

        # Sensors Simulation
        sens = s.sensors
        sci = sens.scientific
        for sensor in [sci.conductivity, sci.salinity, sci.water_density, sci.turbidity, sci.ph, sci.ctd_temp, sci.pressure, sci.dissolved_oxygen, sci.orp]:
            sensor.port = round(max(0, sensor.port + random.uniform(-0.1, 0.1)), 2)
            sensor.stbd = round(max(0, sensor.stbd + random.uniform(-0.1, 0.1)), 2)
            
        surf = sens.surface_ins
        surf.s_roll = round(surf.s_roll + random.uniform(-0.5, 0.5), 1)
        surf.s_pitch = round(surf.s_pitch + random.uniform(-0.5, 0.5), 1)
        surf.s_heading = round((surf.s_heading + random.uniform(-1, 1)) % 360, 1)
        
        ssg = sens.subsea_gps
        ssg.gps_latitude = round(ssg.gps_latitude + random.uniform(-0.0001, 0.0001), 4)
        ssg.gps_longitude = round(ssg.gps_longitude + random.uniform(-0.0001, 0.0001), 4)

        sens.redt_depth.s_depth = round(max(0, sens.redt_depth.s_depth + random.uniform(-0.1, 0.1)), 1)

        # Broadcast rebuilt layouts to support clients on all routes
        await broadcast(AppLayout(active_tab="Main"))
        await broadcast(AppLayout(active_tab="HSSS"))
        await broadcast(AppLayout(active_tab="Ballast"))
        await broadcast(AppLayout(active_tab="Propulsion"))
        await broadcast(AppLayout(active_tab="POWER"))
        await broadcast(AppLayout(active_tab="Imaging"))
        await broadcast(AppLayout(active_tab="Sensors"))
        await broadcast(AppLayout(active_tab="Logging"))
        await broadcast(AppLayout(active_tab="Status"))
        await broadcast(AppLayout(active_tab="50 Kwh"))
        await broadcast(AppLayout(active_tab="MCC"))
        await asyncio.sleep(1)


@rt("/api/toggle_power", methods=["POST"])
async def toggle_power():
    """Toggles the power state and controls the simulator."""
    global simulator_task
    app_state.is_powered_on = not app_state.is_powered_on
    if app_state.is_powered_on:
        if simulator_task is None or simulator_task.done():
            simulator_task = asyncio.create_task(simulate_data())
    else:
        if simulator_task and not simulator_task.done():
            simulator_task.cancel()
            simulator_task = None

    # Broadcast layouts to all clients
    await broadcast(AppLayout(active_tab="Main"))
    await broadcast(AppLayout(active_tab="HSSS"))
    await broadcast(AppLayout(active_tab="Ballast"))
    await broadcast(AppLayout(active_tab="Propulsion"))
    await broadcast(AppLayout(active_tab="POWER"))
    await broadcast(AppLayout(active_tab="Imaging"))
    await broadcast(AppLayout(active_tab="Sensors"))
    await broadcast(AppLayout(active_tab="Logging"))
    await broadcast(AppLayout(active_tab="Status"))
    await broadcast(AppLayout(active_tab="50 Kwh"))
    await broadcast(AppLayout(active_tab="MCC"))
    return ""


@rt("/api/toggle_joystick", methods=["POST"])
async def toggle_joystick():
    s = app_state.sidebar
    s.joystick = not s.joystick
    comp = ToggleSwitch("Joystick", s.joystick, id_key="toggle-joystick", toggle_url="/api/toggle_joystick")
    await broadcast(comp)
    return ""


@rt("/api/toggle_thrusters_enable", methods=["POST"])
async def toggle_thrusters_enable():
    s = app_state.sidebar
    s.thrusters_enable = not s.thrusters_enable
    comp = ToggleSwitch("Thrusters Enable", s.thrusters_enable, id_key="toggle-thrusters", toggle_url="/api/toggle_thrusters_enable")
    await broadcast(comp)
    return ""


@rt("/api/toggle_high_speed", methods=["POST"])
async def toggle_high_speed():
    s = app_state.sidebar
    s.high_speed = not s.high_speed
    comp = ToggleSwitch("High Speed", s.high_speed, id_key="toggle-high-speed", toggle_url="/api/toggle_high_speed")
    await broadcast(comp)
    return ""


@rt("/api/toggle/{state_path:path}", methods=["POST"])
async def generic_toggle(state_path: str):
    """Generic endpoint to toggle booleans anywhere in app_state by dot-separated path."""
    parts = state_path.split(".")
    obj = app_state
    for p in parts[:-1]:
        obj = getattr(obj, p)
    
    val = getattr(obj, parts[-1])
    setattr(obj, parts[-1], not val)

    # Broadcast updated layouts
    await broadcast(AppLayout(active_tab="Main"))
    await broadcast(AppLayout(active_tab="HSSS"))
    await broadcast(AppLayout(active_tab="Ballast"))
    await broadcast(AppLayout(active_tab="Propulsion"))
    await broadcast(AppLayout(active_tab="POWER"))
    await broadcast(AppLayout(active_tab="Imaging"))
    await broadcast(AppLayout(active_tab="Sensors"))
    await broadcast(AppLayout(active_tab="Logging"))
    await broadcast(AppLayout(active_tab="Status"))
    await broadcast(AppLayout(active_tab="50 Kwh"))
    await broadcast(AppLayout(active_tab="MCC"))
    return ""



@rt("/api/start_sim", methods=["GET", "POST"])
async def start_sim():
    """Starts the background task to mutate data."""
    global simulator_task
    if simulator_task is None or simulator_task.done():
        simulator_task = asyncio.create_task(simulate_data())
        return {"status": "Simulation started"}
    return {"status": "Simulation already running"}


@rt("/api/stop_sim", methods=["GET", "POST"])
async def stop_sim():
    """Stops the background task."""
    global simulator_task
    if simulator_task and not simulator_task.done():
        simulator_task.cancel()
        simulator_task = None
        return {"status": "Simulation stopped"}
    return {"status": "Simulation not running"}


@rt("/api/test", methods=["POST", "GET"])
async def test_update():
    """Simple testing route to randomly mutate state and broadcast change once"""
    # Trigger one step of simulation by running it inline
    s = app_state
    s.header.mission_time = datetime.now().strftime("%H:%M:%S")
    s.header.depth.value = round(
        max(0, s.header.depth.value + random.uniform(-0.5, 0.5)), 1
    )
    # Broadcast rebuilt layouts
    await broadcast(AppLayout(active_tab="Main"))
    await broadcast(AppLayout(active_tab="HSSS"))
    return {"status": "Updated"}


if __name__ == "__main__":
    serve()
