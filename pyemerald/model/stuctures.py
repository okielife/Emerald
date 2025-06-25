from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union


class SurfaceType(Enum):
    WALL = 1
    FLOOR = 2
    CEILING = 3
    ROOF = 4

    @staticmethod
    def to_building_surface_key_choice(this_type: 'SurfaceType') -> str:
        if this_type == SurfaceType.WALL:
            return "Wall"
        elif this_type == SurfaceType.FLOOR:
            return "Floor"
        elif this_type == SurfaceType.CEILING:
            return "Ceiling"
        elif this_type == SurfaceType.ROOF:
            return "Roof"


class BoundaryConditionType(Enum):
    OUTDOORS = 1
    GROUND = 2
    OTHER_ZONE = 3

    @staticmethod
    def to_building_surface_key_choice(this_type: 'BoundaryConditionType') -> str:
        if this_type == BoundaryConditionType.OUTDOORS:
            return "Outdoors"
        elif this_type == BoundaryConditionType.GROUND:
            return "Ground"
        elif this_type == BoundaryConditionType.OTHER_ZONE:
            return "Zone"


@dataclass()
class ScheduleTypeLimit:
    name: str
    min: float = -1
    max: float = -1
    discrete_or_continuous: str = 'Continuous'


@dataclass()
class ScheduleConstant:
    name: str
    type_limits: ScheduleTypeLimit
    value: float


@dataclass()
class ScheduleCompact:
    name: str
    type_limits: ScheduleTypeLimit
    fields: List[Union[str, float]]


@dataclass()
class Zone:
    name: str


@dataclass()
class Material:
    name: str
    thickness: float  # meters
    thermal_conductivity: float  # W/mK
    density: float  # kg/m3
    specific_heat: float  # J/kgK
    source_description: str


@dataclass()
class MaterialWindowGlazing:
    name: str
    thickness: float


@dataclass()
class MaterialWindowGas:
    name: str
    gas_type: str
    thickness: float


@dataclass()
class Construction:
    name: str
    layers: List[Union[Material, MaterialWindowGlazing, MaterialWindowGas]]


@dataclass()
class Vertex2D:
    label: str
    x: float
    y: float


class Vertex3D:
    part_2d: Vertex2D
    height: float

    @staticmethod
    def from_vertex_and_height(_part_2d: Vertex2D, _height: float) -> 'Vertex3D':
        v = Vertex3D()
        v.part_2d = _part_2d
        v.height = _height
        return v

    @staticmethod
    def from_x_y_z(_x: float, _y: float, _height: float) -> 'Vertex3D':
        v = Vertex3D()
        v.part_2d = Vertex2D('no_label', _x, _y)
        v.height = _height
        return v


@dataclass()
class Surface:
    name: str
    zone: Zone
    surface_type: SurfaceType
    construction: Construction
    outdoor_bc_type: BoundaryConditionType
    outdoor_bc_instance: Union[Zone, None]
    view_factor_to_ground: float
    wind_exposed: bool
    sun_exposed: bool
    vertices: List[Vertex3D]


@dataclass()
class Window:
    name: str
    construction: Construction
    base_surface: Surface
    vertices: List[Vertex3D]
    blind_control: bool


@dataclass()
class WindowShadingBlind:
    name: str
    slat_orientation: str = 'Horizontal'
    slat_width: float = 0.03  # meters
    slat_separation: float = 0.03  # meters
    slat_thickness: float = 0.00025
    slat_angle_when_control_is_idle: float = 45
    slat_conductivity: float = 0.048  # estimated as insulating fiber board from engineersedge.com
    slat_beam_solar_transmittance: float = 0.1  # it blocks most of it
    slat_front_side_solar_reflectance: float = 0.7
    slat_back_side_solar_reflectance: float = 0.7
    slat_diffuse_solar_transmittance: float = 0.1
    slat_front_side_diffuse_solar_reflectance: float = 0.7
    slat_back_side_diffuse_solar_reflectance: float = 0.7
    slat_beam_visible_transmittance: float = 0.1
    front_side_beam_visible_reflectance: float = 0.5
    back_side_beam_visible_reflectance: float = 0.5
    diffuse_visible_transmittance: float = 0.1
    front_side_diffuse_visible_reflectance: float = 0.5
    back_side_diffuse_visible_reflectance: float = 0.5


@dataclass()
class WindowShadingControl:
    name: str
    zone: Zone
    control_sequence: int
    shading_type: str
    # construction_with_blind: Construction
    control_type: str = 'OnIfHighSolarOnWindow'
    # schedule name: blank
    set_point: float = 10
    # is scheduled: blank
    # glare control: blank
    shading_device: WindowShadingBlind = None
    slat_control_type: str = 'BlockBeamSolar'
    # slat angle schedule: blank
    # setpoint 2: blank
    # daylighting control object: blank
    # multiple surface control type: blank
    windows: List[Window] = field(default_factory=list)


@dataclass()
class Door:
    name: str
    construction: Construction
    base_surface: Surface
    vertices: List[Vertex3D]


@dataclass()
class OutputVariable:
    variable_name: str
    instance_key: str


@dataclass()
class OutputMeter:
    meter_name: str


@dataclass()
class Infiltration:
    name: str
    zone: Zone
    schedule: Union[ScheduleCompact, ScheduleConstant]
    design_volume_flow_rate: float


@dataclass()
class Person:
    name: str
    zone: Zone
    in_zone_schedule: Union[ScheduleCompact, ScheduleConstant]
    activity_schedule: Union[ScheduleCompact, ScheduleConstant]


@dataclass()
class Lights:
    name: str
    zone: Zone
    schedule: Union[ScheduleCompact, ScheduleConstant]
    design_level: float  # electrical input to the light
    fraction_radiant: float = 0.59  # long-wave fraction
    fraction_visible: float = 0.2  # short-wave fraction
    # note that heat gain fraction is 1.0 minus frac radiant minus frac visible


@dataclass()
class Equipment:
    name: str
    zone: Zone
    schedule: Union[ScheduleCompact, ScheduleConstant]
    design_level: float
    fraction_radiant: float = 0.3
    fraction_latent: float = 0.0


@dataclass()
class ExteriorEquipment:
    name: str
    fuel: str = 'Electricity'
    schedule: Union[ScheduleCompact, ScheduleConstant] = ''
    design_level: float = 0.0


@dataclass()
class WaterHeaterMixed:
    name: str
    tank_volume: float  # m3
    setpoint_temp_schedule: Union[ScheduleCompact, ScheduleConstant]
    dead_band_temperature_difference: float  # Delta-Celsius
    max_temperature_limit: float  # Celsius
    # control_type: str   # "Cycle" or "Modulate"
    max_capacity: float
    # min_capacity: float = 0.0
    # ignition_minimum_flow_rate: float = 0.0
    # ignition_delay: float = 0.0
    # fuel_type: str = "Electricity"
    thermal_efficiency: float
    # plf_curve: str = ""
    off_cycle_parasitic_fuel_rate: float
    # off_cycle_parasitic_fuel_type: str = "Electricity"
    # off_cycle_parasitic_fuel_heat_fraction_to_tank: float = 0.0
    on_cycle_parasitic_fuel_rate: float
    # on_cycle_parasitic_fuel_type: str = "Electricity"
    # on_cycle_parasitic_fuel_heat_fraction_to_tank: float = 0.0
    # ambient_temperature_indicator: str = "Zone"
    # ambient_temp_schedule: str = ""
    ambient_temp_zone: Zone
    # ambient_temp_oa_node: str = ""
    off_cycle_loss_coefficient_to_ambient: float
    # off_cycle_loss_fraction_to_zone: float = 1.0
    on_cycle_loss_coefficient_to_ambient: float
    # on_cycle_loss_fraction_to_zone: float = 1.0
    peak_use_flow_rate: float
    use_flow_rate_fraction_schedule: Union[ScheduleCompact, ScheduleConstant]
    # use_side_inlet_node: str
    # use_side_outlet_node: str  # once we connect the water use with the water heater, add these in
    # use_side_effectiveness: float

    def to_idf_object(self) -> List[str]:
        return [
            self.name, self.tank_volume, self.setpoint_temp_schedule.name,
            self.dead_band_temperature_difference,
            self.max_temperature_limit,
            "Cycle",
            self.max_capacity, "", "", "",
            "Electricity",
            self.thermal_efficiency,
            "",
            self.off_cycle_parasitic_fuel_rate, "Electricity", 0.0,
            self.on_cycle_parasitic_fuel_rate, "Electricity", 0.0,
            "Zone", "", self.ambient_temp_zone.name, "",
            self.off_cycle_loss_coefficient_to_ambient, 1.0,
            self.on_cycle_loss_coefficient_to_ambient, 1.0,
            self.peak_use_flow_rate, self.use_flow_rate_fraction_schedule.name,
            # self.use_side_inlet_node, self.use_side_outlet_node,
            # self.use_side_effectiveness
        ]
