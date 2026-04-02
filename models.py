from pydantic import BaseModel


# ----------------- ATOMIC TYPES -----------------
class NumericTelemetry(BaseModel):
    value: float = 0.0
    unit: str = ""


# ----------------- STATE SECTIONS -----------------
class HeaderTelemetry(BaseModel):
    dive_num: int = 0
    mission_time: str = "00:00:00"
    present_time: str = "00:00:00"
    heading: NumericTelemetry = NumericTelemetry(value=0.0, unit="deg")
    depth: NumericTelemetry = NumericTelemetry(value=0.0, unit="m")
    altitude: NumericTelemetry = NumericTelemetry(value=0.0, unit="m")
    mb_p_soc: NumericTelemetry = NumericTelemetry(value=0.0, unit="%")
    mb_s_soc: NumericTelemetry = NumericTelemetry(value=0.0, unit="%")


class IMUTelemetry(BaseModel):
    roll: NumericTelemetry = NumericTelemetry(value=0.0, unit="")
    pitch: NumericTelemetry = NumericTelemetry(value=0.0, unit="")
    heading_p: NumericTelemetry = NumericTelemetry(value=0.0, unit="deg")


class BottomStrip(BaseModel):
    east_speed: NumericTelemetry = NumericTelemetry(value=0.0, unit="m/s")
    vert_speed: NumericTelemetry = NumericTelemetry(value=0.0, unit="m/s")
    north_speed: NumericTelemetry = NumericTelemetry(value=0.0, unit="m/s")
    ship_heading: NumericTelemetry = NumericTelemetry(value=0.0, unit="deg")


class PropulsionTelemetry(BaseModel):
    t1_rpm: float = 0
    t2_rpm: float = 0
    t3_rpm: float = 0
    t4_rpm: float = 0
    t5_rpm: float = 0
    t6_rpm: float = 0
    t7_rpm: float = 0
    t8_rpm: float = 0
    latitude: NumericTelemetry = NumericTelemetry(value=0.0, unit="deg")
    longitude: NumericTelemetry = NumericTelemetry(value=0.0, unit="deg")


class ThrusterTelemetry(BaseModel):
    """Per-thruster detailed telemetry shown in the Propulsion screen"""
    rpm: float = 0.0           # 0-1600
    voltage: float = 0.0       # V
    current: float = 0.0       # A
    temp: float = 0.0          # deg C
    ctrl: float = 0.0          # control setpoint
    power: bool = False         # power toggle
    enable: bool = False        # enable toggle


class PropulsionDetailState(BaseModel):
    """Full detail state for the Propulsion dedicated screen"""
    t1: ThrusterTelemetry = ThrusterTelemetry()
    t2: ThrusterTelemetry = ThrusterTelemetry()
    t3: ThrusterTelemetry = ThrusterTelemetry()
    t4: ThrusterTelemetry = ThrusterTelemetry()
    t5: ThrusterTelemetry = ThrusterTelemetry()
    t6: ThrusterTelemetry = ThrusterTelemetry()
    t7: ThrusterTelemetry = ThrusterTelemetry()
    t8: ThrusterTelemetry = ThrusterTelemetry()
    heading_ctrl: float = 0.0
    fwd_ctrl: float = 0.0
    lat_ctrl: float = 0.0
    vertical_ctrl: float = 0.0
    speed_factor: int = 4


class EnvironmentTelemetry(BaseModel):
    o2: NumericTelemetry = NumericTelemetry(value=0.0, unit="%")
    co2: NumericTelemetry = NumericTelemetry(value=0.0, unit="ppm")
    temp: NumericTelemetry = NumericTelemetry(value=0.0, unit="deg C")
    pressure: NumericTelemetry = NumericTelemetry(value=0.0, unit="mbar")


class SidebarControls(BaseModel):
    joystick: bool = False
    thrusters_enable: bool = False
    high_speed: bool = False
    ir_ok: bool = True
    water_ingress: bool = False
    comm_status: bool = False


class LedIndicators(BaseModel):
    pss: bool = False
    pds: bool = False
    ids: bool = False
    psp: bool = False
    pdp: bool = False
    idp: bool = False


class HSSSSideTelemetry(BaseModel):
    co2: NumericTelemetry = NumericTelemetry(value=0.0, unit="ppm")
    oxygen: NumericTelemetry = NumericTelemetry(value=21.0, unit="% v/v")
    pressure: NumericTelemetry = NumericTelemetry(value=0.0, unit="")
    temp: NumericTelemetry = NumericTelemetry(value=0.0, unit="")
    humidity: NumericTelemetry = NumericTelemetry(value=0.0, unit="")
    smoke_sensor: str = "NO SMOKE"
    flame_sensor: str = "NO FLAME"
    heat_sensor: str = "Normal"
    hydrogen: NumericTelemetry = NumericTelemetry(value=0.0, unit="%")
    lp_l_pressure: NumericTelemetry = NumericTelemetry(value=0.0, unit="bar")
    hp_b1_pressure: NumericTelemetry = NumericTelemetry(value=0.0, unit="bar")
    hp_b2_pressure: NumericTelemetry = NumericTelemetry(value=0.0, unit="bar")
    hp_b3_pressure: NumericTelemetry = NumericTelemetry(value=0.0, unit="bar")


class HSSSTelemetry(BaseModel):
    p: HSSSSideTelemetry = HSSSSideTelemetry()
    s: HSSSSideTelemetry = HSSSSideTelemetry()


# ----------------- BALLAST STATE SECTIONS -----------------
class MainBallastState(BaseModel):
    act3_pos: float = 0.0        # -150 to 150
    act3_pos2: float = 0.0
    act3_pos3: float = 0.0
    read_pressure_s: float = 0.0
    read_pressure_p: float = 0.0
    pressure_s_enable: bool = False
    pressure_p_enable: bool = False


class VBSTelemetry(BaseModel):
    hpu_enable: bool = False
    hpu_pressure: NumericTelemetry = NumericTelemetry(value=0.0, unit="bar")
    hpu_temp: NumericTelemetry = NumericTelemetry(value=0.0, unit="deg C")
    tank_level: float = 1.0      # 0-300 L
    vbs_set: float = 0.0


class TrimTelemetry(BaseModel):
    position_mm: float = 0.0    # 0-4500
    power: bool = False
    cw_ccw: bool = False
    voltage: NumericTelemetry = NumericTelemetry(value=0.0, unit="V")
    current: NumericTelemetry = NumericTelemetry(value=0.0, unit="A")
    temp: NumericTelemetry = NumericTelemetry(value=0.0, unit="deg C")
    speed: NumericTelemetry = NumericTelemetry(value=0.0, unit="mm/min")
    speed_control: float = 1.0  # 1-7


class OIMControls(BaseModel):
    s1_ext_reset: bool = False
    s2_int_reset: bool = False
    p1_ext_reset: bool = False
    p2_int_reset: bool = False


class BallastTelemetry(BaseModel):
    main_ballast: MainBallastState = MainBallastState()
    vbs: VBSTelemetry = VBSTelemetry()
    trim: TrimTelemetry = TrimTelemetry()
    oim: OIMControls = OIMControls()


# ----------------- ROOT STATE -----------------
class MatsyaUIState(BaseModel):
    is_powered_on: bool = False
    active_tab: str = "Main"

    header: HeaderTelemetry = HeaderTelemetry()
    imu: IMUTelemetry = IMUTelemetry()
    bottom: BottomStrip = BottomStrip()
    propulsion: PropulsionTelemetry = PropulsionTelemetry()
    propulsion_detail: PropulsionDetailState = PropulsionDetailState()
    environment: EnvironmentTelemetry = EnvironmentTelemetry()
    sidebar: SidebarControls = SidebarControls()
    leds: LedIndicators = LedIndicators()
    hsss: HSSSTelemetry = HSSSTelemetry()
    ballast: BallastTelemetry = BallastTelemetry()
