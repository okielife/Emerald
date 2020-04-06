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

    def to_idf(self) -> str:
        out_string = ''
        out_string += '  Zone,\n'
        out_string += '    ' + self.name + ',\n'
        out_string += '    0, ! Relative north\n'
        out_string += '    0, 0, 0,  ! Origin Point\n'
        out_string += '    1,  ! Type?\n'
        out_string += '    1,  ! Multiplier\n'
        out_string += '    autocalculate,  ! Multiplier\n'
        out_string += '    autocalculate;  ! Volume\n'
        out_string += '\n'
        return out_string


@dataclass()
class Material:
    name: str
    thickness: float  # meters
    thermal_conductivity: float  # W/mK
    density: float  # kg/m3
    specific_heat: float  # J/kgK
    source_description: str

    def to_idf(self) -> str:
        out_string = ''
        out_string += '  Material,\n'
        out_string += '    ' + self.name + ',\n'
        out_string += '    MediumRough,\n'
        out_string += '    ' + str(self.thickness) + ',\n'
        out_string += '    ' + str(self.thermal_conductivity) + ',\n'
        out_string += '    ' + str(self.density) + ',\n'
        out_string += '    ' + str(self.specific_heat) + ',\n'
        out_string += '    0.9, 0.6, 0.6;\n'
        out_string += '\n'
        return out_string


@dataclass()
class Construction:
    name: str
    layers: List[Material]

    def to_idf(self) -> str:
        out_string = ''
        out_string += '  Construction,\n'
        out_string += '    ' + self.name + ',\n'
        layers_string = ''
        for i, l in enumerate(self.layers):
            layers_string += '    ' + l.name
            if i < len(self.layers) - 1:
                layers_string += ',\n'
            else:
                layers_string += ';\n'
        out_string += layers_string
        out_string += '\n'
        return out_string


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

    def to_idf(self) -> str:
        bc_instance_name = ''
        if self.outdoor_bc_instance:
            bc_instance_name = self.outdoor_bc_instance.name
        sun_exposed_string = 'NoSun'
        if self.sun_exposed:
            sun_exposed_string = 'SunExposed'
        wind_exposed_string = 'NoWind'
        if self.wind_exposed:
            wind_exposed_string = 'WindExposed'
        vertex_string = ''
        for i, v in enumerate(self.vertices):
            vertex_string += '    ' + str(v.part_2d.x) + ', ' + str(v.part_2d.y) + ', ' + str(v.height)
            if i < len(self.vertices) - 1:
                vertex_string += ',\n'
            else:
                vertex_string += ';\n'
        out_string = ''
        out_string += '  BuildingSurface:Detailed,\n'
        out_string += '    ' + self.name + ',\n'
        out_string += '    ' + SurfaceType.to_building_surface_key_choice(self.surface_type) + ',\n'
        out_string += '    ' + self.construction.name + ',\n'
        out_string += '    ' + self.zone.name + ',\n'
        out_string += '    ' + BoundaryConditionType.to_building_surface_key_choice(self.outdoor_bc_type) + ',\n'
        out_string += '    ' + bc_instance_name + ',\n'
        out_string += '    ' + sun_exposed_string + ',\n'
        out_string += '    ' + wind_exposed_string + ',\n'
        out_string += '    ' + str(self.view_factor_to_ground) + ',\n'
        out_string += '    ' + str(len(self.vertices)) + ',\n'
        out_string += vertex_string
        out_string += '\n'
        return out_string
