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
            ToggleSwitch("Joystick", s.sidebar.joystick),
            ToggleSwitch("Thrusters Enable", s.sidebar.thrusters_enable),
            ToggleSwitch("High Speed", s.sidebar.high_speed),
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
                    BallastPressureRead("Read Pressure_S", b.main_ballast.read_pressure_s, b.main_ballast.pressure_s_enable),
                    BallastPressureRead("Read Pressure_P", b.main_ballast.read_pressure_p, b.main_ballast.pressure_p_enable),
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
                    ToggleSwitch("power", b.trim.power),
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
                    ToggleSwitch("CW/CCW", b.trim.cw_ccw),
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
                OIMToggleRow("OIM_S1_Ext_Reset", b.oim.s1_ext_reset),
                OIMToggleRow("OIM_S2_Int_Reset", b.oim.s2_int_reset),
                OIMToggleRow("OIM_P1_Ext_Reset", b.oim.p1_ext_reset),
                OIMToggleRow("OIM_P2_Int_Reset", b.oim.p2_int_reset),
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
            PropCenterToggleBlock(2, pd.t2.power, pd.t2.enable),
            PropCenterToggleBlock(6, pd.t6.power, pd.t6.enable),
            PropCenterToggleBlock(5, pd.t5.power, pd.t5.enable),
            PropCenterToggleBlock(1, pd.t1.power, pd.t1.enable),
            PropCenterToggleBlock(4, pd.t4.power, pd.t4.enable),
            PropCenterToggleBlock(8, pd.t8.power, pd.t8.enable),
            PropCenterToggleBlock(7, pd.t7.power, pd.t7.enable),
            PropCenterToggleBlock(3, pd.t3.power, pd.t3.enable),
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

        # Sidebar (less frequent toggle)
        if random.random() < 0.05:
            s.sidebar.joystick = not s.sidebar.joystick
        if random.random() < 0.05:
            s.sidebar.thrusters_enable = not s.sidebar.thrusters_enable
        if random.random() < 0.05:
            s.sidebar.high_speed = not s.sidebar.high_speed

        # Leds (less frequent toggle)
        for attr in ["pss", "pds", "ids", "psp", "pdp", "idp"]:
            if random.random() < 0.05:
                setattr(s.leds, attr, not getattr(s.leds, attr))

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
            if random.random() < 0.02:
                t.power = not t.power
            if random.random() < 0.02:
                t.enable = not t.enable
        pd.heading_ctrl = round(max(-180, min(180, pd.heading_ctrl + random.uniform(-0.5, 0.5))), 1)
        pd.fwd_ctrl = round(max(-100, min(100, pd.fwd_ctrl + random.uniform(-0.5, 0.5))), 1)
        pd.lat_ctrl = round(max(-100, min(100, pd.lat_ctrl + random.uniform(-0.5, 0.5))), 1)
        pd.vertical_ctrl = round(max(-100, min(100, pd.vertical_ctrl + random.uniform(-0.5, 0.5))), 1)

        # Broadcast rebuilt layouts to support clients on all routes
        await broadcast(AppLayout(active_tab="Main"))
        await broadcast(AppLayout(active_tab="HSSS"))
        await broadcast(AppLayout(active_tab="Ballast"))
        await broadcast(AppLayout(active_tab="Propulsion"))

        # 1 Hz refresh rate
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
