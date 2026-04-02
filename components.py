from fasthtml.common import Div, Span, NotStr, H3, A
import math


# ----------------- ICONS (SVG Placeholders via NotStr) -----------------
def IconSettings():
    return NotStr(
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>'
    )


def IconPower():
    return NotStr(
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path><line x1="12" y1="2" x2="12" y2="12"></line></svg>'
    )


# ----------------- WIDGETS -----------------


def TopbarInlineMetric(label, value, unit="", id_key=None):
    """Header strip inline key-value pairs"""
    return Div(
        Span(label, cls="topbar-metric-label"),
        Div(
            Span(str(value), cls="topbar-metric-value"),
            Span(unit, cls="topbar-metric-unit") if unit else None,
            cls="topbar-metric-box",
        ),
        cls="topbar-metric",
        id=id_key,
        hx_swap_oob="true" if id_key else None,
    )


def VerticalGauge(
    label, value, max_val, unit="", low_is_good=False, scale_labels=None, id_key=None
):
    """Tall vertical tracking bar representing Depth or Altitude"""
    percent = min(100, max(0, (value / max_val) * 100))
    fill_cls = (
        "gauge-fill-green"
        if not low_is_good
        else ("gauge-fill-red" if percent > 80 else "gauge-fill-green")
    )

    # Scale labels next to gauge
    labels_children = []
    if scale_labels:
        for lbl in scale_labels:
            labels_children.append(Span(str(lbl), cls="gauge-scale-label"))
    y_axis = Div(*labels_children, cls="gauge-scale")

    return Div(
        Div(
            y_axis,
            Div(
                Div(cls=f"gauge-fill {fill_cls}", style=f"height: {percent}%;"),
                cls="gauge-track",
            ),
            cls="gauge-body",
        ),
        H3(label, cls="gauge-title"),
        Div(
            Span(f"{value:.1f}", cls="gauge-value"),
            Span(unit, cls="gauge-unit"),
            cls="gauge-readout",
        ),
        cls="gauge-container",
        id=id_key,
        hx_swap_oob="true" if id_key else None,
    )


def SimpleRpmBox(label, value, id_key=None):
    """Specific T1-T8 RPM boxes"""
    return Div(
        Span(label, cls="rpm-label"),
        Div(str(value), cls="rpm-value"),
        cls="rpm-box",
        id=id_key,
        hx_swap_oob="true" if id_key else None,
    )


def SimpleMetricBox(label, value, unit="", id_key=None):
    """Tiny input-like read-only boxes (used for Roll/Pitch and footers)"""
    return Div(
        Span(label, cls="metric-label"),
        Div(Span(str(value), cls="metric-value"), cls="metric-input"),
        Span(unit, cls="metric-unit") if unit else None,
        cls="metric-box",
        id=id_key,
        hx_swap_oob="true" if id_key else None,
    )


def CompassBox():
    """The central map box with N, E, S, W indicators"""
    return Div(
        Span("N", cls="compass-label compass-n"),
        Span("S", cls="compass-label compass-s"),
        Span("W", cls="compass-label compass-w"),
        Span("E", cls="compass-label compass-e"),
        Div(cls="compass-inner"),
        cls="compass-box",
    )


def SidebarMetric(label, value, unit="", id_key=None):
    """Right sidebar environmental metrics"""
    return Div(
        Span(label, cls="sidebar-metric-label"),
        Div(
            Span(str(value), cls="sidebar-metric-value"),
            Span(unit, cls="sidebar-metric-unit"),
            cls="sidebar-metric-readout",
        ),
        cls="sidebar-metric",
        id=id_key,
        hx_swap_oob="true" if id_key else None,
    )


def StatusPill(label, is_ok, ok_text="OK", err_text="ERR", id_key=None):
    """Right sidebar status flags"""
    status_cls = "status-pill-ok" if is_ok else "status-pill-err"
    text = ok_text if is_ok else err_text
    return Div(
        f"{label} {text}",
        cls=f"status-pill {status_cls}",
        id=id_key,
        hx_swap_oob="true" if id_key else None,
    )


def ToggleSwitch(label, is_on, id_key=None):
    """Vercel styled pill toggle for right sidebar"""
    toggle_cls = "toggle-on" if is_on else "toggle-off"
    dot_cls = "toggle-dot-on" if is_on else "toggle-dot-off"
    return Div(
        Span(label, cls="toggle-label"),
        Div(
            Span("ON" if is_on else "OFF", cls="toggle-state-text"),
            Div(Div(cls=f"toggle-dot {dot_cls}"), cls=f"toggle-track {toggle_cls}"),
            cls="toggle-controls",
        ),
        cls="toggle-switch",
        id=id_key,
        hx_swap_oob="true" if id_key else None,
    )


def BottomTabsNav(tabs, active_tab="Main"):
    """Bottom footer with segmented navigation"""
    nav_links = []
    for t in tabs:
        active_cls = "tab-active" if t == active_tab else "tab-inactive"
        url = "/" if t == "Main" else ("/hsss" if t == "HSSS" else ("/ballast" if t == "Ballast" else ("/propulsion" if t == "Propulsion" else "#")))
        nav_links.append(
            A(
                t,
                href=url,
                cls=f"tab-link {active_cls}",
            )
        )
    return Div(*nav_links, cls="bottom-tabs")


def BigNumber(label, value, unit=""):
    """Big prominent readout for the key telemetry values"""
    return Div(
        Span(label, cls="big-number-label"),
        Div(
            Span(str(value), cls="big-number-value"),
            Span(unit, cls="big-number-unit"),
            cls="big-number-readout",
        ),
        cls="big-number",
    )


def LedPanel(leds, id_key=None):
    """Two rows of 3 LED indicators: PSS/PDS/IDS and PSP/PDP/IDP"""

    def led(label, is_on):
        cls = "led-dot led-on" if is_on else "led-dot led-off"
        return Div(Div(cls=cls), Span(label, cls="led-label"), cls="led-item")

    return Div(
        Div(
            led("PSS", leds.pss),
            led("PDS", leds.pds),
            led("IDS", leds.ids),
            cls="led-row",
        ),
        Div(
            led("PSP", leds.psp),
            led("PDP", leds.pdp),
            led("IDP", leds.idp),
            cls="led-row",
        ),
        cls="led-panel",
        id=id_key,
        hx_swap_oob="true" if id_key else None,
    )


# ----------------- HSSS SPECIFIC WIDGETS -----------------


def SemiCircleGauge(
    label,
    value,
    min_val,
    max_val,
    unit,
    label_sub="",
    scale_labels=None,
    is_oxygen=False,
):
    """A semi-circle CSS gauge for CO2 and Oxygen"""
    percent = (value - min_val) / (max_val - min_val) * 100
    percent = max(0, min(100, percent))
    rotation = (percent / 100) * 180

    # Optional scale labels positions calculated along arc
    labels_divs = []
    if scale_labels:
        n = len(scale_labels)
        for i, sl in enumerate(scale_labels):
            f = i / (n - 1) if n > 1 else 0.5
            angle = math.pi * (1 - f)
            
            r = 120
            cx = 130
            cy = 120
            
            x = cx + r * math.cos(angle)
            y = cy - r * math.sin(angle)
            
            style = f"left: {x}px; top: {y}px; transform: translate(-50%, -50%);"
            labels_divs.append(Span(str(sl), cls="sc-label", style=style))

    gauge_type = "sc-gauge-oxygen" if is_oxygen else "sc-gauge-co2"

    return Div(
        Div(*labels_divs, cls="sc-labels-container"),
        Div(
            Div(
                cls=f"sc-fill {gauge_type}", style=f"transform: rotate({rotation}deg);"
            ),
            Div(cls="sc-cover"),
            cls="sc-track",
        ),
        Div(
            Span(f"{value:.0f}" if not is_oxygen else f"{value:.1f}", cls="sc-value"),
            Span(label, cls="sc-title"),
            Span(f"({unit})", cls="sc-unit"),
            cls="sc-readout",
        ),
        cls="semi-circle-gauge",
    )


def HorizontalProgressBar(label, value, min_val, max_val, unit, scale_labels=None):
    """Horizontal progress bar for Pressure, Temp, Humidity"""
    percent = (value - min_val) / (max_val - min_val) * 100
    percent = max(0, min(100, percent))

    labels_row = None
    if scale_labels:
        labels_children = [Span(str(sl), cls="hp-scale-label") for sl in scale_labels]
        labels_row = Div(*labels_children, cls="hp-scale-row")

    return Div(
        Div(
            Span(label, cls="hp-title"),
            Div(str(value), cls="hp-value-box"),
            cls="hp-header",
        ),
        Div(Div(cls="hp-fill", style=f"width: {percent}%;"), cls="hp-track"),
        labels_row,
        cls="horizontal-progress-bar",
    )


def SensorStatusPill(label, status_text, is_ok):
    """Rectangular block used for indicating Smoke, Flame, and Heat sensor statuses"""
    bg_cls = "sensor-ok" if is_ok else "sensor-err"
    return Div(
        Span(label, cls="sensor-label"),
        Div(status_text, cls=f"sensor-status {bg_cls}"),
        cls="sensor-pill-container",
    )


def HSSSLabelInput(label, value, unit):
    """White box model input display for Hydrogen, LP_L Pressure, etc"""
    return Div(
        Span(label, cls="hsss-input-label"),
        Div(
            Div(str(value), cls="hsss-input-value"),
            Span(unit, cls="hsss-input-unit"),
            cls="hsss-input-row",
        ),
        cls="hsss-input-container",
    )


# ----------------- BALLAST SPECIFIC WIDGETS -----------------


def BallastActionButton(label):
    """Gray action button for ballast commands (Ready to Dive, Dive open, etc.)"""
    return Div(label, cls="ballast-btn")


def BallastPressureRead(label, value, is_enabled):
    """Pressure read row: label + value box + mini toggle switch"""
    toggle_cls = "toggle-on" if is_enabled else "toggle-off"
    dot_cls = "toggle-dot-on" if is_enabled else "toggle-dot-off"
    return Div(
        Span(label, cls="ballast-pressure-label"),
        Div(
            Div(str(value), cls="ballast-pressure-value"),
            Div(
                Span("ON" if is_enabled else "OFF", cls="toggle-state-text"),
                Div(
                    Div(cls=f"toggle-dot {dot_cls}"),
                    cls=f"toggle-track {toggle_cls}",
                ),
                cls="toggle-controls",
            ),
            cls="ballast-pressure-right",
        ),
        cls="ballast-pressure-read",
    )


def BallastActSlider(label, value, min_val=-150, max_val=150):
    """ACT position read-only slider: Open <----[thumb]----> Closed with scale"""
    percent = (value - min_val) / (max_val - min_val) * 100
    percent = max(0, min(100, percent))
    scale_labels = ["-150", "-100", "-50", "0", "50", "100", "150"]
    scale_items = [Span(sl, cls="act-scale-label") for sl in scale_labels]
    return Div(
        Span(label, cls="act-slider-title"),
        Div(
            Span("Open", cls="act-slider-side"),
            Div(
                Div(
                    Div(cls="act-thumb", style=f"left: {percent}%;"),
                    cls="act-track",
                ),
                Div(*scale_items, cls="act-scale-row"),
                cls="act-track-wrap",
            ),
            Span("Closed", cls="act-slider-side"),
            cls="act-slider-row",
        ),
        cls="act-slider-container",
    )


def VBSTankGauge(level, max_val=300):
    """Vertical tank gauge for the Variable Ballast System"""
    percent = min(100, max(0, (level / max_val) * 100))
    scale_labels = ["300", "250", "200", "150", "100", "50", "0"]
    labels_children = [Span(str(lbl), cls="vbs-tank-scale-label") for lbl in scale_labels]
    y_axis = Div(*labels_children, cls="vbs-tank-scale")
    return Div(
        Div("VBS Tank", cls="vbs-tank-title"),
        Div(
            y_axis,
            Div(
                Div(cls="vbs-tank-fill", style=f"height: {percent}%;"),
                cls="vbs-tank-track",
            ),
            cls="vbs-tank-body",
        ),
        Div(
            Span(f"{level:.0f}", cls="vbs-tank-value"),
            Span("L", cls="vbs-tank-unit"),
            cls="vbs-tank-readout",
        ),
        cls="vbs-tank-gauge",
    )


def VBSMetricRow(label, value, unit):
    """Label + value display box + unit for VBS HPU metrics"""
    return Div(
        Span(label, cls="vbs-metric-label"),
        Div(
            Div(str(value), cls="vbs-metric-value"),
            Span(unit, cls="vbs-metric-unit") if unit else None,
            cls="vbs-metric-right",
        ),
        cls="vbs-metric-row",
    )


def VBSWaterButton(label):
    """Water IN / Water OUT action button"""
    return Div(label, cls="vbs-water-btn")


def VBSSetControl(value):
    """VBS SET control with up/down arrows and current value display"""
    return Div(
        Span("VBS SET", cls="vbs-set-label"),
        Div(
            Div("▲", cls="vbs-set-arrow"),
            Div(str(int(value)), cls="vbs-set-value"),
            Div("▼", cls="vbs-set-arrow"),
            cls="vbs-set-spinbox",
        ),
        cls="vbs-set-container",
    )


def TrimPositionBar(value, max_val=4500):
    """Horizontal position bar for TRIM showing 0–4500 mm"""
    percent = min(100, max(0, (value / max_val) * 100))
    scale_labels = ["0", "500", "1000", "1500", "2000", "2500", "3000", "3500", "4000", "4500"]
    scale_items = [Span(sl, cls="trim-scale-label") for sl in scale_labels]
    return Div(
        Div(
            Div(
                Div(cls="trim-thumb", style=f"left: {percent}%;"),
                cls="trim-track",
            ),
        ),
        Div(*scale_items, cls="trim-scale-row"),
        cls="trim-position-bar",
    )


def SpeedControlSlider(value, min_val=1, max_val=7):
    """Speed control display slider from 1 to 7"""
    percent = min(100, max(0, ((value - min_val) / (max_val - min_val)) * 100))
    scale_labels = ["1", "2", "3", "4", "5", "6", "7"]
    scale_items = [Span(sl, cls="speed-scale-label") for sl in scale_labels]
    return Div(
        Span("Speed Control", cls="speed-ctrl-label"),
        Div(
            Div(
                Div(cls="speed-thumb", style=f"left: {percent}%;"),
                cls="speed-track",
            ),
            Div(*scale_items, cls="speed-scale-row"),
            cls="speed-track-wrap",
        ),
        cls="speed-control-slider",
    )


def OIMToggleRow(label, is_on):
    """Horizontal OIM reset row: label ........ toggle"""
    toggle_cls = "toggle-on" if is_on else "toggle-off"
    dot_cls = "toggle-dot-on" if is_on else "toggle-dot-off"
    return Div(
        Span(label, cls="oim-toggle-label"),
        Div(
            Span("ON" if is_on else "OFF", cls="toggle-state-text"),
            Div(
                Div(cls=f"toggle-dot {dot_cls}"),
                cls=f"toggle-track {toggle_cls}",
            ),
            cls="toggle-controls",
        ),
        cls="oim-toggle-row",
    )


# ----------------- PROPULSION SCREEN SPECIFIC WIDGETS -----------------


def ThrusterRPMGauge(label, rpm, max_rpm=1600):
    """Semi-circle RPM gauge for Propulsion screen, styled like original dashboard"""
    percent = min(100, max(0, (rpm / max_rpm) * 100))
    rotation = (percent / 100) * 180  # 0 → 180 deg

    # Arc needle: dark fill rotating from left
    # Scale labels along the arc
    scale_values = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600]
    labels_divs = []
    n = len(scale_values)
    r = 62
    cx = 70
    cy = 65
    for i, sv in enumerate(scale_values):
        f = i / (n - 1)
        angle = math.pi * (1 - f)
        x = cx + r * math.cos(angle)
        y = cy - r * math.sin(angle)
        style = f"left:{x:.0f}px;top:{y:.0f}px;transform:translate(-50%,-50%);"
        labels_divs.append(Span(str(sv), cls="tg-scale-label", style=style))

    return Div(
        # Labels container
        Div(*labels_divs, cls="tg-labels-container"),
        # Semi-circle track + fill + cover
        Div(
            Div(cls="tg-fill", style=f"transform:rotate({rotation}deg);"),
            Div(cls="tg-cover"),
            cls="tg-track",
        ),
        # Readout below
        Div(
            Span(f"{rpm:.0f}", cls="tg-rpm-value"),
            cls="tg-readout",
        ),
        Span(label, cls="tg-label"),
        Span("RPM", cls="tg-rpm-unit"),
        cls="thruster-gauge",
    )


def ThrusterPowerEnableToggles(thruster_id, power, enable):
    """Compact vertical pair of Power/Enable toggles for Propulsion center column"""
    def mini_toggle(label, is_on):
        t_cls = "toggle-on" if is_on else "toggle-off"
        d_cls = "toggle-dot-on" if is_on else "toggle-dot-off"
        return Div(
            Span(label, cls="prop-toggle-label"),
            Div(
                Div(
                    Div(cls=f"toggle-dot {d_cls}"),
                    cls=f"toggle-track {t_cls}",
                ),
                Span("ON" if is_on else "OFF", cls="prop-toggle-state"),
                cls="prop-toggle-controls",
            ),
            cls="prop-toggle-row",
        )

    return Div(
        mini_toggle(f"T{thruster_id}_Power", power),
        mini_toggle(f"T{thruster_id}_Enable", enable),
        cls="prop-toggle-pair",
    )


def ThrusterPanel(thruster_id, t):
    """Full thruster card: gauge + voltage/current/temp + ctrl + power/enable"""
    return Div(
        Div(f"T{thruster_id}", cls="thruster-panel-id"),
        ThrusterRPMGauge(f"T{thruster_id} Speed", t.rpm),
        Div(
            Div(
                Span("Voltage", cls="tp-metric-label"),
                Div(str(t.voltage), cls="tp-metric-value"),
                Span("V", cls="tp-metric-unit"),
                cls="tp-metric-row",
            ),
            Div(
                Span("Current", cls="tp-metric-label"),
                Div(str(t.current), cls="tp-metric-value"),
                Span("A", cls="tp-metric-unit"),
                cls="tp-metric-row",
            ),
            Div(
                Span("Temp", cls="tp-metric-label"),
                Div(str(t.temp), cls="tp-metric-value"),
                Span("°C", cls="tp-metric-unit"),
                cls="tp-metric-row",
            ),
            cls="tp-metrics",
        ),
        Div(
            Span(f"T{thruster_id} ctrl", cls="tp-ctrl-label"),
            Div(str(int(t.ctrl)), cls="tp-ctrl-value"),
            cls="tp-ctrl-row",
        ),
        cls="thruster-panel",
    )


def PropCenterToggleBlock(thruster_id, power, enable):
    """Power + Enable toggle pair with label for the center column"""
    def tiny_tog(label, is_on):
        t_cls = "toggle-on" if is_on else "toggle-off"
        d_cls = "toggle-dot-on" if is_on else "toggle-dot-off"
        return Div(
            Span(label, cls="prop-center-tog-label"),
            Div(
                Div(
                    Div(cls=f"toggle-dot {d_cls}"),
                    cls=f"toggle-track {t_cls}",
                ),
                Span("ON" if is_on else "OFF", cls="prop-center-tog-state"),
                cls="prop-center-tog-controls",
            ),
            cls="prop-center-tog-row",
        )

    return Div(
        tiny_tog(f"T{thruster_id}_Power", power),
        tiny_tog(f"T{thruster_id}_Enable", enable),
        cls="prop-center-block",
    )


def PropAxisControl(label, value):
    """Bottom axis control box: Heading ctrl, Fwd ctrl, etc."""
    return Div(
        Span(label, cls="prop-axis-label"),
        Div(str(int(value)), cls="prop-axis-value"),
        cls="prop-axis-ctrl",
    )
