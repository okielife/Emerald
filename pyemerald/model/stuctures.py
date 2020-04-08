from dataclasses import dataclass
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
class Construction:
    name: str
    layers: List[Material]


@dataclass()
class Vertex2D:
    label: str
    x: float
    y: float


@dataclass()
class Vertex3D:
    part_2d: Vertex2D
    height: float


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
    # sub_surfaces: List[SubSurface]


@dataclass()
class OutputVariable:
    variable_name: str
    instance_key: str


@dataclass()
class OutputMeter:
    meter_name: str
