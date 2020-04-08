from typing import List

from pyemerald.model.stuctures import (
    BoundaryConditionType,
    Construction,
    Material,
    OutputMeter,
    OutputVariable,
    Surface,
    SurfaceType,
    Vertex2D,
    Vertex3D,
    Zone,
)


class Model:

    def __init__(self):
        self.idf_string = ''
        # order does matter here, materials need to be declared before constructions, etc.
        self._setup_settings()
        self._setup_location()
        self._setup_schedules()
        self._setup_internal_gains()
        self._setup_zones()
        self._setup_materials()
        self._setup_constructions()
        self._setup_floor_vertices()
        self._setup_surfaces()
        self._water_use()
        self._setup_hvac()
        self._setup_outputs()

    @staticmethod
    def _build_wall_vertices(vertex_a: Vertex2D, vertex_b: Vertex2D, ceiling_height: float) -> List[Vertex3D]:
        """The vertices should be given in clockwise order as you walk around the exterior of the space"""
        return [
            Vertex3D(vertex_a, 0),
            Vertex3D(vertex_a, ceiling_height),
            Vertex3D(vertex_b, ceiling_height),
            Vertex3D(vertex_b, 0)
        ]

    @staticmethod
    def _add_height_to_vertices(height: float, vertices: List[Vertex2D]) -> List[Vertex3D]:
        return_vertices = list()
        for vertex in vertices:
            return_vertices.append(Vertex3D(vertex, height))
        return return_vertices

    def _add_idf_object(self, object_name: str, *object_data):
        if len(object_data) == 0:
            self.idf_string += '  ' + object_name + ';\n'
        else:
            self.idf_string += '  ' + object_name + ',\n'
            for i, f in enumerate(object_data):
                if i+1 == len(object_data):
                    self.idf_string += '    ' + str(f) + ';\n'
                else:
                    self.idf_string += '    ' + str(f) + ',\n'
        self.idf_string += '\n'

    def _setup_settings(self):
        self._add_idf_object('Version', 9.3)
        self._add_idf_object('TimeStep', 4)
        self._add_idf_object('Building', 'EmeraldWay', 0, 'Country', 0.5, 0.05, 'MinimalShadowing', 6, 2)
        self._add_idf_object('SimulationControl', 'No', 'No', 'No', 'Yes', 'Yes')
        self._add_idf_object('GlobalGeometryRules', 'UpperLeftCorner', 'CounterClockwise', 'World')
        self._add_idf_object('RunPeriod', 'Year 2020', 1, 1, 2020, 12, 31, 2020, '', 'Yes', 'Yes', 'No', 'Yes', 'Yes')
        self._add_idf_object('RunPeriodControl:DaylightSavingTime', '2nd Sunday in March', '2nd Sunday in November')

    def _setup_location(self):
        self._add_idf_object('Site:Location', 'Cashion', 35.798, -97.679, -6, 396)
        self._add_idf_object(
            'Site:GroundTemperature:BuildingSurface',
            19.53, 19.50, 19.54, 19.60, 20.00, 21.64, 22.23, 22.38, 21.45, 20.12, 19.80, 19.63
        )
        self._add_idf_object(
            'SizingPeriod:DesignDay',
            'Winter Sizing Period', 1, 21, 'WinterDesignDay', -11.4, 0.0, 'DefaultMultipliers', '', 'WetBulb', -11.4,
            '', '', '', '', 96634, 6.1, 0, 'No', 'No', 'No', 'ASHRAEClearSky', '', '', '', '', 0.0
        )
        self._add_idf_object(
            'SizingPeriod:DesignDay',
            'Summer Sizing Period', 7, 21, 'SummerDesignDay', 37.5, 11.7, 'DefaultMultipliers', '', 'WetBulb', 23.4,
            '', '', '', '', 96634, 5.5, 170, 'No', 'No', 'No', 'ASHRAETau', '', '', 0.426, 2.214
        )

    def _setup_zones(self):
        # set up zones
        self.zone_indoor = Zone("Indoor")
        self.zone_garage = Zone("Garage")
        # write IDF
        self._add_idf_object('Zone', self.zone_indoor.name, 0, 0, 0, 0, 1, 1, 'AutoCalculate', 'AutoCalculate')
        self._add_idf_object('Zone', self.zone_garage.name, 0, 0, 0, 0, 1, 1, 'AutoCalculate', 'AutoCalculate')

    def _setup_materials(self):
        # setup materials
        self.material_brick = Material('Brick', 0.11, 0.7, 1970, 800, 'Handbook 2017 - Brick, Building')
        self.material_sheathing = Material('Sheathing', 0.02, 0.09, 288, 1300, 'https://researchgate.net')
        self.material_wall_insulation = Material('R13Insulation', 0.09, 0.04, 45, 2020, 'https://www.greenspec.co.uk')
        self.material_gypsum = Material('Gypsum', 0.013, 0.16, 800, 837, 'https://researchgate.net')
        self.material_shingles = Material('Shingles', 0.01, 0.74, 2110, 920, 'Handbook 2017 - Asphalt')
        self.material_roof_insulation = Material('R31Insulation', 0.21, 0.04, 45, 2020, 'https://www.greenspec.co.uk')
        self.material_concrete = Material('6InchConcrete', 0.15, 1.73, 2242, 837, 'In IDF data-sets')
        self.material_wood_floor = Material('WoodFlooring', 0.15, 0.17, 750, 2390, 'Handbook 2017 - Assuming Oak')
        # write IDF
        all_materials = [
            self.material_brick, self.material_sheathing, self.material_wall_insulation, self.material_gypsum,
            self.material_shingles, self.material_roof_insulation, self.material_concrete, self.material_wood_floor
        ]
        for m in all_materials:
            self._add_idf_object(
                'Material',
                m.name, 'MediumRough', m.thickness, m.thermal_conductivity, m.density, m.specific_heat, 0.9, 0.6, 0.6
            )

    def _setup_constructions(self):
        # set up constructions
        self.construction_exterior_wall = Construction('BrickWallConstruction', [
            self.material_brick, self.material_sheathing, self.material_wall_insulation, self.material_gypsum
        ])
        self.construction_insulated_partition_wall = Construction('InsulatedPartitionWall', [
            self.material_gypsum, self.material_wall_insulation, self.material_gypsum
        ])
        self.construction_roof = Construction('RoofConstruction', [
            self.material_shingles, self.material_sheathing, self.material_roof_insulation
        ])
        self.construction_floor = Construction('FloorConstruction', [
            self.material_concrete, self.material_wood_floor
        ])
        self.construction_garage_floor = Construction('GarageFloorConstruction', [self.material_concrete])
        # write IDF
        all_constructions = [
            self.construction_exterior_wall,
            self.construction_insulated_partition_wall,
            self.construction_roof,
            self.construction_floor,
            self.construction_garage_floor
        ]
        for c in all_constructions:
            self._add_idf_object('Construction', c.name, *[layer.name for layer in c.layers])

    def _setup_floor_vertices(self):
        # set up vertices
        self.v_1 = Vertex2D('1', 28.3211, 43.5974)
        self.v_2 = Vertex2D('2', 29.631, 45.624)
        self.v_3 = Vertex2D('3', 27.1138, 47.2509)
        self.v_4 = Vertex2D('4', 29.2371, 50.5361)
        self.v_5 = Vertex2D('5', 32.1169, 48.6747)
        self.v_6 = Vertex2D('6', 33.1648, 50.296)
        self.v_7 = Vertex2D('7', 32.1409, 50.9578)
        self.v_8 = Vertex2D('8', 34.3194, 54.3282)
        self.v_9 = Vertex2D('9', 34.8313, 53.9973)
        self.v_10 = Vertex2D('10', 36.6513, 56.8132)
        self.v_11 = Vertex2D('11', 35.798, 57.3647)
        self.v_12 = Vertex2D('12', 36.7908, 58.9006)
        self.v_13 = Vertex2D('13', 36.4068, 59.1488)
        self.v_14 = Vertex2D('14', 38.1992, 61.9219)
        self.v_15 = Vertex2D('15', 38.5832, 61.6737)
        self.v_16 = Vertex2D('16', 39.5759, 63.2097)
        self.v_17 = Vertex2D('17', 43.4583, 60.7003)
        self.v_18 = Vertex2D('18', 45.6644, 64.1134)
        self.v_19 = Vertex2D('19', 51.232, 60.5148)
        self.v_20 = Vertex2D('20', 43.5247, 48.5902)
        self.v_21 = Vertex2D('21', 44.058, 48.2455)
        self.v_22 = Vertex2D('22', 41.7002, 44.5977)
        self.v_23 = Vertex2D('23', 41.1669, 44.9424)
        self.v_24 = Vertex2D('24', 40.5878, 44.0464)
        self.v_25 = Vertex2D('25', 41.1211, 43.7017)
        self.v_26 = Vertex2D('26', 40.1698, 42.2298)
        self.v_27 = Vertex2D('27', 39.6365, 42.5745)
        self.v_28 = Vertex2D('28', 36.7686, 38.1375)
        self.v_29 = Vertex2D('29', 33.4408, 40.2884)
        self.v_30 = Vertex2D('30', 33.0548, 39.6911)
        self.v_31 = Vertex2D('31', 30.7082, 41.2077)
        self.v_32 = Vertex2D('32', 31.0943, 41.805)
        self.v_34 = Vertex2D('34', 39.4716, 55.1688)
        self.v_35 = Vertex2D('35', 41.5036, 58.1914)
        self.v_36 = Vertex2D('36', 47.1678, 54.5592)

    def _setup_surfaces(self):
        # set up surfaces
        ceiling_height = 3  # eventually we need to fine tune this
        self.surface_main_bath_exterior_wall_west = Surface(
            'Main Bath Exterior Wall West',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_1, self.v_2, ceiling_height))
        self.surface_dax_exterior_wall_south = Surface(
            'Dax Exterior Wall South',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_2, self.v_3, ceiling_height))
        self.surface_dax_exterior_wall_west = Surface(
            'Dax Exterior Wall West',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_3, self.v_4, ceiling_height))
        self.surface_dax_exterior_wall_north = Surface(
            'Dax Exterior Wall North',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_4, self.v_5, ceiling_height))
        self.surface_entry_exterior_wall = Surface(
            'Entry Exterior Wall',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_5, self.v_6, ceiling_height))
        self.surface_office_exterior_wall_south = Surface(
            'Office Exterior Wall South',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_6, self.v_7, ceiling_height))
        self.surface_office_exterior_wall_west = Surface(
            'Office Exterior Wall West',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_7, self.v_8, ceiling_height))
        self.surface_office_exterior_wall_north = Surface(
            'Office Exterior Wall North',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_8, self.v_9, ceiling_height))
        self.surface_utility_exterior_wall_west = Surface(
            'Utility Exterior Wall West',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_9, self.v_10, ceiling_height))
        # conditioned-to-garage interface walls
        self.inter_zone_surface_small_garage = Surface(
            'Inter-zone Surface Small Garage Side',
            self.zone_indoor, SurfaceType.WALL, self.construction_insulated_partition_wall,
            BoundaryConditionType.OTHER_ZONE, self.zone_garage, 0.0, False, False,
            self._build_wall_vertices(self.v_10, self.v_34, ceiling_height))
        self.inter_zone_surface_intermediate = Surface(
            'Inter-zone Surface Intermediate Wall',
            self.zone_indoor, SurfaceType.WALL, self.construction_insulated_partition_wall,
            BoundaryConditionType.OTHER_ZONE, self.zone_garage, 0.0, False, False,
            self._build_wall_vertices(self.v_34, self.v_35, ceiling_height))
        self.inter_zone_surface_large_garage = Surface(
            'Inter-zone Surface Large Garage Side',
            self.zone_indoor, SurfaceType.WALL, self.construction_insulated_partition_wall,
            BoundaryConditionType.OTHER_ZONE, self.zone_garage, 0.0, False, False,
            self._build_wall_vertices(self.v_35, self.v_36, ceiling_height))
        # now do the garage exterior walls
        self.surface_garage_exterior_wall_south_a = Surface(
            'Garage Exterior Wall South A',
            self.zone_garage, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_10, self.v_11, ceiling_height))
        self.surface_garage_exterior_wall_west_a = Surface(
            'Garage Exterior Wall West A',
            self.zone_garage, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_11, self.v_12, ceiling_height))
        self.surface_garage_exterior_wall_south_b = Surface(
            'Garage Exterior Wall South B',
            self.zone_garage, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_12, self.v_13, ceiling_height))
        self.surface_garage_exterior_wall_west_b_with_window = Surface(
            'Garage Exterior Wall West B With Window',
            self.zone_garage, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_13, self.v_14, ceiling_height))
        self.surface_garage_exterior_wall_north_a = Surface(
            'Garage Exterior Wall North A',
            self.zone_garage, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_14, self.v_15, ceiling_height))
        self.surface_garage_exterior_wall_west_c = Surface(
            'Garage Exterior Wall West C',
            self.zone_garage, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_15, self.v_16, ceiling_height))
        self.surface_garage_exterior_wall_north_b_with_small_garage_and_man_door = Surface(
            'Garage Exterior Wall North B With Small Garage Door And Man Door',
            self.zone_garage, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_16, self.v_17, ceiling_height))
        self.surface_garage_exterior_wall_west_d = Surface(
            'Garage Exterior Wall West D',
            self.zone_garage, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_17, self.v_18, ceiling_height))
        self.surface_garage_exterior_wall_north_c_with_large_garage_door = Surface(
            'Garage Exterior Wall North C With Large Garage Door',
            self.zone_garage, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_18, self.v_19, ceiling_height))
        self.surface_garage_exterior_wall_east = Surface(
            'Garage Exterior Wall East',
            self.zone_garage, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_19, self.v_36, ceiling_height))
        # back to the remaining conditioned space exterior surfaces
        self.surface_master_exterior_wall_east = Surface(
            'Master Exterior Wall East',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_36, self.v_20, ceiling_height))
        self.surface_dining_exterior_wall_north = Surface(
            'Dining Exterior Wall North',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_20, self.v_21, ceiling_height))
        self.surface_dining_exterior_wall_east = Surface(
            'Dining Exterior Wall East',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_21, self.v_22, ceiling_height))
        self.surface_dining_exterior_wall_south = Surface(
            'Dining Exterior Wall South',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_22, self.v_23, ceiling_height))
        self.surface_living_exterior_wall_east_with_northern_window = Surface(
            'Living Room Exterior Wall East With Northern Window',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_23, self.v_24, ceiling_height))
        self.surface_living_exterior_wall_north = Surface(
            'Living Room Exterior Wall North',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_24, self.v_25, ceiling_height))
        self.surface_living_exterior_wall_east_behind_chimney = Surface(
            'Living Room Exterior Wall East Behind Chimney',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_25, self.v_26, ceiling_height))
        self.surface_living_exterior_wall_south = Surface(
            'Living Room Exterior Wall South',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_26, self.v_27, ceiling_height))
        self.surface_living_and_gibson_exterior_wall_east = Surface(
            'Living And Gibs Exterior Wall East',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_27, self.v_28, ceiling_height))
        self.surface_gibson_exterior_wall_south = Surface(
            'Gibs Exterior Wall South',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_28, self.v_29, ceiling_height))
        self.surface_study_exterior_wall_east = Surface(
            'Study Exterior Wall East',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_29, self.v_30, ceiling_height))
        self.surface_study_exterior_wall_south = Surface(
            'Study Exterior Wall South With Window',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_30, self.v_31, ceiling_height))
        self.surface_study_exterior_wall_west = Surface(
            'Study Exterior Wall West',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_31, self.v_32, ceiling_height))
        self.surface_main_bath_exterior_wall_south = Surface(
            'Main Bath Exterior Wall South',
            self.zone_indoor, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_32, self.v_1, ceiling_height))
        # now the ceilings/roofs - need to fix this up later
        ceiling_vertex_list_ccw_from_above = [
            self.v_32,
            self.v_31,
            self.v_30,
            self.v_29,
            self.v_28,
            self.v_27,
            self.v_26,
            self.v_25,
            self.v_24,
            self.v_23,
            self.v_22,
            self.v_21,
            self.v_20,
            self.v_36,
            self.v_35,
            self.v_34,
            self.v_10,
            self.v_9,
            self.v_8,
            self.v_7,
            self.v_6,
            self.v_5,
            self.v_4,
            self.v_3,
            self.v_2,
            self.v_1
        ]
        ceiling_vertex_list_clockwise_from_above = ceiling_vertex_list_ccw_from_above[::-1]
        self.surface_ceiling_conditioned_space = Surface(
            'Conditioned Space Ceiling',
            self.zone_indoor, SurfaceType.ROOF, self.construction_roof,
            BoundaryConditionType.OUTDOORS, None, 0.0, True, True,
            self._add_height_to_vertices(ceiling_height, ceiling_vertex_list_ccw_from_above)
        )
        self.surface_ceiling_garage_space = Surface(
            'Garage Ceiling',
            self.zone_garage, SurfaceType.ROOF, self.construction_roof,
            BoundaryConditionType.OUTDOORS, None, 0.0, True, True,
            self._add_height_to_vertices(ceiling_height, [
                self.v_10,
                self.v_34,
                self.v_35,
                self.v_36,
                self.v_19,
                self.v_18,
                self.v_17,
                self.v_16,
                self.v_15,
                self.v_14,
                self.v_13,
                self.v_12,
                self.v_11
            ])
        )
        self.surface_floor_conditioned_space = Surface(
            'Conditioned Space Floor',
            self.zone_indoor, SurfaceType.FLOOR, self.construction_floor,
            BoundaryConditionType.GROUND, None, 1.0, False, False,
            self._add_height_to_vertices(0.0, ceiling_vertex_list_clockwise_from_above)
        )
        self.surface_floor_garage_space = Surface(
            'Garage Floor',
            self.zone_garage, SurfaceType.FLOOR, self.construction_garage_floor,
            BoundaryConditionType.GROUND, None, 1.0, False, False,
            self._add_height_to_vertices(0, [
                self.v_11,
                self.v_12,
                self.v_13,
                self.v_14,
                self.v_15,
                self.v_16,
                self.v_17,
                self.v_18,
                self.v_19,
                self.v_36,
                self.v_35,
                self.v_34,
                self.v_10
            ])
        )
        all_surfaces = [
            self.surface_main_bath_exterior_wall_west,
            self.surface_dax_exterior_wall_south,
            self.surface_dax_exterior_wall_west,
            self.surface_dax_exterior_wall_north,
            self.surface_entry_exterior_wall,
            self.surface_office_exterior_wall_south,
            self.surface_office_exterior_wall_west,
            self.surface_office_exterior_wall_north,
            self.surface_utility_exterior_wall_west,
            self.inter_zone_surface_small_garage,
            self.inter_zone_surface_intermediate,
            self.inter_zone_surface_large_garage,
            self.surface_garage_exterior_wall_south_a,
            self.surface_garage_exterior_wall_west_a,
            self.surface_garage_exterior_wall_south_b,
            self.surface_garage_exterior_wall_west_b_with_window,
            self.surface_garage_exterior_wall_north_a,
            self.surface_garage_exterior_wall_west_c,
            self.surface_garage_exterior_wall_north_b_with_small_garage_and_man_door,
            self.surface_garage_exterior_wall_west_d,
            self.surface_garage_exterior_wall_north_c_with_large_garage_door,
            self.surface_garage_exterior_wall_east,
            self.surface_master_exterior_wall_east,
            self.surface_dining_exterior_wall_north,
            self.surface_dining_exterior_wall_east,
            self.surface_dining_exterior_wall_south,
            self.surface_living_exterior_wall_east_with_northern_window,
            self.surface_living_exterior_wall_north,
            self.surface_living_exterior_wall_east_behind_chimney,
            self.surface_living_exterior_wall_south,
            self.surface_living_and_gibson_exterior_wall_east,
            self.surface_gibson_exterior_wall_south,
            self.surface_study_exterior_wall_east,
            self.surface_study_exterior_wall_south,
            self.surface_study_exterior_wall_west,
            self.surface_main_bath_exterior_wall_south,
            self.surface_ceiling_conditioned_space,
            self.surface_ceiling_garage_space,
            self.surface_floor_conditioned_space,
            self.surface_floor_garage_space
        ]
        for s in all_surfaces:
            bc_instance_name = ''
            if s.outdoor_bc_instance:
                bc_instance_name = s.outdoor_bc_instance.name
            sun_exposed_string = 'NoSun'
            if s.sun_exposed:
                sun_exposed_string = 'SunExposed'
            wind_exposed_string = 'NoWind'
            if s.wind_exposed:
                wind_exposed_string = 'WindExposed'
            vertex_list = []
            for i, v in enumerate(s.vertices):
                vertex_list.extend([v.part_2d.x, v.part_2d.y, v.height])
            self._add_idf_object(
                'BuildingSurface:Detailed',
                s.name,
                SurfaceType.to_building_surface_key_choice(s.surface_type),
                s.construction.name, s.zone.name,
                BoundaryConditionType.to_building_surface_key_choice(s.outdoor_bc_type), bc_instance_name,
                sun_exposed_string, wind_exposed_string, s.view_factor_to_ground, len(s.vertices), *vertex_list
            )

    def _setup_outputs(self):
        # setup outputs
        self.output_variables = [
            OutputVariable('Site Outdoor Air DryBulb Temperature', '*'),
            OutputVariable('Site Wind Speed', '*'),
            OutputVariable('Site Horizontal Infrared Radiation Rate per Area', '*'),
            OutputVariable('Site Precipitation Depth', '*'),
            # OutputVariable('Site Daylight Saving Time Status', '*'),
            # OutputVariable('Site Day Type Index', '*'),
            OutputVariable('Zone Mean Air Temperature', '*'),
            OutputVariable('Zone Mean Radiant Temperature', '*'),
            OutputVariable('Zone Predicted Sensible Load to Setpoint Heat Transfer Rate', '*'),
            OutputVariable('Zone Predicted Sensible Load to Heating Setpoint Heat Transfer Rate', '*'),
            OutputVariable('Zone Predicted Sensible Load to Cooling Setpoint Heat Transfer Rate', '*'),
            # OutputVariable('Surface Inside Face Temperature', '*'),
            # OutputVariable('Surface Outside Face Temperature', '*'),
            # OutputVariable('Surface Outside Face Sunlit Fraction', '*'),
            OutputVariable('Zone Thermostat Heating Setpoint Temperature', '*'),
            OutputVariable('Zone Thermostat Cooling Setpoint Temperature', '*'),
            OutputVariable('Zone Air Terminal Sensible Heating Energy', '*'),
            OutputVariable('Zone Air Terminal Sensible Cooling Energy', '*'),
            OutputVariable('Fan Air Mass Flow Rate', '*'),
            OutputVariable('Cooling Coil Total Cooling Rate', '*'),
            OutputVariable('Cooling Coil Sensible Cooling Rate', '*'),
            OutputVariable('Cooling Coil Electric Power', '*'),
            OutputVariable('Heating Coil Heating Rate', '*'),
            OutputVariable('Heating Coil Electric Power', '*'),
            OutputVariable('Schedule Value', '*'),
        ]
        self.output_meters = [
            OutputMeter('EnergyTransfer:Facility',),
            OutputMeter('Electricity:Facility'),
        ]
        # write IDF
        for ov in self.output_variables:
            self._add_idf_object('Output:Variable', ov.instance_key, ov.variable_name, 'hourly')
        for om in self.output_meters:
            self._add_idf_object('Output:Meter:MeterFileOnly', om.meter_name, 'monthly')
        self._add_idf_object('Output:VariableDictionary', 'IDF')
        self._add_idf_object('Output:Surfaces:Drawing', 'DXF:WireFrame')
        self._add_idf_object('Output:Constructions', 'Constructions')
        self._add_idf_object('OutputControl:Table:Style', 'All')
        self._add_idf_object('Output:Table:SummaryReports', 'AllSummary')
        self._add_idf_object('Output:SQLite', 'SimpleAndTabular')
        self._add_idf_object('Output:Diagnostics', 'DisplayExtraWarnings', 'DisplayUnusedSchedules')

    def _setup_schedules(self):
        self._add_idf_object('ScheduleTypeLimits', 'AnyNumber')
        self._add_idf_object('Schedule:Constant', 'HeatingSetpoint', 'AnyNumber', 21.1)
        self._add_idf_object('Schedule:Constant', 'CoolingSetpoint', 'AnyNumber', 23.9)
        self._add_idf_object('Schedule:Constant', 'ScheduleDualSetPoint', 'AnyNumber', 4)

    def _setup_internal_gains(self):
        pass

    def _water_use(self):
        # water heater, water usage, etc
        pass

    def _setup_hvac(self):
        # hvac unit is:
        # Carrier Sentry - 4 Ton 14 SEER Residential Heat Pump Condensing Unit
        # https://www.carrierenterprise.com/carrier-4-ton-14-seer-single-stage-heat-pump-condenser-with-puron-refrigerant-ch14nb04800g  # noqa: E501

        # Outdoor Unit:
        #   Model: CH14NB04800GAAAA
        #   Serial: 4616X84977
        #   Condenser Motor HP: 1/4 HP
        #   Condenser Motor RPM: 1110
        #   Condenser Motor Type: Permanent Split Compressor
        #   Cooling Capacity: 46000
        #   Cooling Capacity Range: 44500
        #   Cooling Rated Capacity Btu/h: 48000
        #   COP: 3.64-3.94
        #   EER: 11.5-12.5
        #   Full Load Amps: 1.45
        #   Heating Capacity: 43500
        #   HSPF: 8.2-9
        #   Metering Device: TXV
        #   Motor Type: Direct Drive
        #   Phase: Single
        #   Rated Load Amps: 19
        #   Refrigerant: R-410a
        #   Rows: 2
        #   SEER: 14
        #   Sound Level (dBA): 79
        #   Stage: Single
        #   Tonnage: 4
        #   Voltage: 208-230 VAC
        #
        # Indoor Unit:
        #   Heat Package In This Unit: KFCEH3101C15A
        #   Model: FB4CNF048
        #   Serial: 1516A83297
        #   Motor HP: 0.75
        #   Motor Full Load Amps: 6
        #   Static Pressure: 0.2 inH2O
        #
        # AHRI: https://www.ahridirectory.org/Search/SearchHome
        #   AHRI Certified Reference Number: 7835942
        #   Manufacturer Type: Systems
        #   AHRI Type: HRCU-A-CB
        #   Outdoor Unit Model Number: CARRIER  CH14NB048****A
        #   Brand Name: CARRIER
        #   Indoor Unit Model Number: FB4CNF048L+TXV
        #   Cooling Capacity (A2) - Single or High Stage (95F),btuh: 45500
        #   SEER: 14.00
        #   EER (A2) (95F): 11.70
        #   Heating Capacity (H12) - (47F),btuh: 44500
        #   HSPF (Region IV): 8.20
        #   Heating Capacity (H32) - (17F),btuh: 27800
        #   Indoor Full-Load Air Volume Rate (A2 SCFM): 1400

        # set up some system properties
        system_air_volume_flow_rate_cfm = 1400  # CFM
        rated_cooling_capacity_btu_h = 45500
        rated_heating_capacity_btu_h = 44500
        rated_heating_capacity_watts = rated_heating_capacity_btu_h * 0.29
        rated_cooling_capacity_watts = rated_cooling_capacity_btu_h * 0.29
        indoor_unit_static_pressure_inches = 0.2
        static_pressure_pascals = indoor_unit_static_pressure_inches * 249
        sys_vol_flow = system_air_volume_flow_rate_cfm * 0.00047194745
        max_supply_temp_for_supplemental_heater = 40
        seer_cooling_btu_per_watt = 14
        cop_cooling = seer_cooling_btu_per_watt / 3.412
        hspf_heating_btu_per_watt = 8.2
        cop_heating = hspf_heating_btu_per_watt / 3.412
        min_outdoor_temp_for_compressor = -8
        rated_shr = 0.7  # assumed
        supplemental_heater_capacity_watts = 10000  # assumed
        defrost_time_period = 0.06
        self._add_idf_object(
            'ThermostatSetpoint:DualSetpoint',
            'ThermostatControl', 'HeatingSetpoint', 'CoolingSetpoint'
        )
        self._add_idf_object(
            'ZoneControl:Thermostat',
            'Thermostat', 'Indoor', 'ScheduleDualSetPoint', 'ThermostatSetpoint:DualSetpoint', 'ThermostatControl'
        )
        self._add_idf_object(
            'ZoneHVAC:EquipmentConnections',
            'Indoor', 'HVACEquipment', 'ZoneSupplyAirNode', '', 'ZoneAirNode', 'ZoneReturnAirNode'
        )
        self._add_idf_object(
            'ZoneHVAC:EquipmentList',
            'HVACEquipment', 'SequentialLoad', 'ZoneHVAC:AirDistributionUnit', 'ADU', 1, 1
        )
        self._add_idf_object(
            'ZoneHVAC:AirDistributionUnit',
            'ADU', 'ZoneSupplyAirNode', 'AirTerminal:SingleDuct:ConstantVolume:NoReheat', 'AirTerminal'
        )
        self._add_idf_object(
            'AirTerminal:SingleDuct:ConstantVolume:NoReheat',
            'AirTerminal', '', 'ZoneEquipmentInlet', 'ZoneSupplyAirNode', sys_vol_flow
        )
        self._add_idf_object(
            'AirLoopHVAC',
            'HeatPump', '', '', sys_vol_flow, 'Branches', '', 'AirLoopSupplyInlet', 'AirLoopDemandOutlet',
            'AirLoopDemandInlet', 'AirLoopSupplyOutlet'
        )
        self._add_idf_object(
            'BranchList',
            'Branches', 'Branch'
        )
        self._add_idf_object(
            'Branch',
            'Branch', '', 'AirLoopHVAC:UnitaryHeatPump:AirToAir', 'HeatPump',
            'AirLoopSupplyInlet', 'AirLoopSupplyOutlet'
        )
        self._add_idf_object(
            'AirLoopHVAC:SupplyPath',
            'HPSupplyPath', 'AirLoopDemandInlet', 'AirLoopHVAC:ZoneSplitter', 'ZoneSplitter'
        )
        self._add_idf_object(
            'AirLoopHVAC:ZoneSplitter',
            'ZoneSplitter', 'AirLoopDemandInlet', 'ZoneEquipmentInlet'
        )
        self._add_idf_object(
            'AirLoopHVAC:ReturnPath',
            'HPReturnPath', 'AirLoopDemandOutlet', 'AirLoopHVAC:ZoneMixer', 'ZoneMixer'
        )
        self._add_idf_object(
            'AirLoopHVAC:ZoneMixer',
            'ZoneMixer', 'AirLoopDemandOutlet', 'ZoneReturnAirNode'
        )
        self._add_idf_object(
            'AirLoopHVAC:UnitaryHeatPump:AirToAir',
            'HeatPump', '', 'AirLoopSupplyInlet', 'AirLoopSupplyOutlet', sys_vol_flow, sys_vol_flow, sys_vol_flow,
            'Indoor',
            'Fan:OnOff', 'Fan',
            'Coil:Heating:DX:SingleSpeed', 'HeatingCoil',
            'Coil:Cooling:DX:SingleSpeed', 'CoolingCoil',
            'Coil:Heating:Electric', 'SupplementalCoil',
            max_supply_temp_for_supplemental_heater,
        )
        self._add_idf_object(
            'Coil:Heating:DX:SingleSpeed',
            'HeatingCoil', '', rated_heating_capacity_watts, cop_heating, sys_vol_flow, '',
            'CoolingCoilOutlet', 'HeatingCoilOutlet',
            'HtgCapFT', 'HtgCapFF', 'HtgEirFT', 'HtgEirFF', 'HtgPLF', 'HtgDefrostEirFT',
            min_outdoor_temp_for_compressor, '', '', '', '', '', '', defrost_time_period
        )
        self._add_idf_object(
            'Curve:Cubic',
            'HtgCapFT', 0.758746, 0.027626, 0.000148716, 0.0000034992, -20, 20
        )
        self._add_idf_object(
            'Curve:Cubic',
            'HtgCapFF', 0.84, 0.16, 0.0, 0.0, 0.5, 1.5
        )
        self._add_idf_object(
            'Curve:Cubic',
            'HtgEirFT', 1.19248, -0.0300438, 0.00103745, -0.000023328, -20, 20
        )
        self._add_idf_object(
            'Curve:Quadratic',
            'HtgEirFF', 1.3824, -0.4336, 0.0512, 0.0, 1.0
        )
        self._add_idf_object(
            'Curve:Quadratic',
            'HtgPLF', 0.75, 0.25, 0.0, 0.0, 1.0
        )
        self._add_idf_object(
            'Curve:Biquadratic',
            'HtgDefrostEirFT', 1, 0, 0, 0, 0, 0, 0, 50, 0, 50
        )
        self._add_idf_object(
            'Coil:Heating:Electric',
            'SupplementalCoil', '', 1, supplemental_heater_capacity_watts, 'HeatingCoilOutlet', 'AirLoopSupplyOutlet'
        )
        self._add_idf_object(
            'Coil:Cooling:DX:SingleSpeed',
            'CoolingCoil', '', rated_cooling_capacity_watts, rated_shr, cop_cooling, sys_vol_flow, '',
            'FanOutlet', 'CoolingCoilOutlet', 'ClgCapFT', 'ClgCapFF', 'ClgEirFT', 'ClgEirFF', 'ClgPLF', '',
            '', '', '', '', 'CoilCondInlet'
        )
        self._add_idf_object(
            'Curve:Biquadratic',
            'ClgCapFT', 0.94258779, 0.00954335, 0.0006838, -0.01104267, 0.00000525, -0.0000097, 12.77, 23.88, 18.0, 46.1
        )
        self._add_idf_object(
            'Curve:Quadratic',
            'ClgCapFF', 0.8, 0.2, 0.0, 0.5, 1.5
        )
        self._add_idf_object(
            'Curve:Biquadratic',
            'ClgEirFT', 0.34241441, 0.03488501, -0.000624, 0.00497722, 0.00043795, -0.00072803, 12.77, 23.88, 18.0, 46.1
        )
        self._add_idf_object(
            'Curve:Quadratic',
            'ClgEirFF', 1.1552, -0.1808, 0.0256, 0.5, 1.5
        )
        self._add_idf_object(
            'Curve:Quadratic',
            'ClgPLF', 0.85, 0.15, 0.0, 0.0, 1.0
        )
        self._add_idf_object(
            'OutdoorAir:Node',
            'CoilCondInlet', -1
        )
        self._add_idf_object(
            'Fan:OnOff',
            'Fan', '', '', static_pressure_pascals, sys_vol_flow, '', '', 'AirLoopSupplyInlet', 'FanOutlet'
        )
