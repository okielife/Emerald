from house.stuctures import *


class DataManager:

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

    def __init__(self):
        # set up zones
        self.zone_conditioned = Zone("ConditionedSpace")
        self.zone_garage = Zone("Garage")
        # set up materials
        self.material_brick = Material('Brick', 0.11, 0.7, 1970, 800, 'Handbook 2017 - Brick, Building')
        self.material_sheathing = Material('Sheathing', 0.02, 0.09, 288, 1300, 'https://researchgate.net')
        self.material_wall_insulation = Material('R13Insulation', 0.09, 0.04, 45, 2020, 'https://www.greenspec.co.uk')
        self.material_gypsum = Material('Gypsum', 0.013, 0.16, 800, 837, 'https://researchgate.net')
        self.material_shingles = Material('Shingles', 0.01, 0.74, 2110, 920, 'Handbook 2017 - Asphalt')
        self.material_roof_insulation = Material('R31Insulation', 0.21, 0.04, 45, 2020, 'https://www.greenspec.co.uk')
        self.material_concrete = Material('6InchConcrete', 0.15, 1.73, 2242, 837, 'In IDF data-sets')
        self.material_wood_floor = Material('WoodFlooring', 0.15, 0.17, 750, 2390, 'Handbook 2017 - Assuming Oak')
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
        # set up surfaces
        ceiling_height = 3  # eventually we need to fine tune this
        self.surface_main_bath_exterior_wall_west = Surface(
            'Main Bath Exterior Wall West',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_1, self.v_2, ceiling_height))
        self.surface_dax_exterior_wall_south = Surface(
            'Dax Exterior Wall South',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_2, self.v_3, ceiling_height))
        self.surface_dax_exterior_wall_west = Surface(
            'Dax Exterior Wall West',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_3, self.v_4, ceiling_height))
        self.surface_dax_exterior_wall_north = Surface(
            'Dax Exterior Wall North',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_4, self.v_5, ceiling_height))
        self.surface_entry_exterior_wall = Surface(
            'Entry Exterior Wall',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_5, self.v_6, ceiling_height))
        self.surface_office_exterior_wall_south = Surface(
            'Office Exterior Wall South',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_6, self.v_7, ceiling_height))
        self.surface_office_exterior_wall_west = Surface(
            'Office Exterior Wall West',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_7, self.v_8, ceiling_height))
        self.surface_office_exterior_wall_north = Surface(
            'Office Exterior Wall North',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_8, self.v_9, ceiling_height))
        self.surface_utility_exterior_wall_west = Surface(
            'Utility Exterior Wall West',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_9, self.v_10, ceiling_height))
        # conditioned-to-garage interface walls
        self.inter_zone_surface_small_garage = Surface(
            'Inter-zone Surface Small Garage Side',
            self.zone_conditioned, SurfaceType.WALL, self.construction_insulated_partition_wall,
            BoundaryConditionType.OTHER_ZONE, self.zone_garage, 0.0, False, False,
            self._build_wall_vertices(self.v_10, self.v_34, ceiling_height))
        self.inter_zone_surface_intermediate = Surface(
            'Inter-zone Surface Intermediate Wall',
            self.zone_conditioned, SurfaceType.WALL, self.construction_insulated_partition_wall,
            BoundaryConditionType.OTHER_ZONE, self.zone_garage, 0.0, False, False,
            self._build_wall_vertices(self.v_34, self.v_35, ceiling_height))
        self.inter_zone_surface_large_garage = Surface(
            'Inter-zone Surface Large Garage Side',
            self.zone_conditioned, SurfaceType.WALL, self.construction_insulated_partition_wall,
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
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_36, self.v_20, ceiling_height))
        self.surface_dining_exterior_wall_north = Surface(
            'Dining Exterior Wall North',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_20, self.v_21, ceiling_height))
        self.surface_dining_exterior_wall_east = Surface(
            'Dining Exterior Wall East',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_21, self.v_22, ceiling_height))
        self.surface_dining_exterior_wall_south = Surface(
            'Dining Exterior Wall South',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_22, self.v_23, ceiling_height))
        self.surface_living_exterior_wall_east_with_northern_window = Surface(
            'Living Room Exterior Wall East With Northern Window',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_23, self.v_24, ceiling_height))
        self.surface_living_exterior_wall_north = Surface(
            'Living Room Exterior Wall North',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_24, self.v_25, ceiling_height))
        self.surface_living_exterior_wall_east_behind_chimney = Surface(
            'Living Room Exterior Wall East Behind Chimney',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_25, self.v_26, ceiling_height))
        self.surface_living_exterior_wall_south = Surface(
            'Living Room Exterior Wall South',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_26, self.v_27, ceiling_height))
        self.surface_living_and_gibson_exterior_wall_east = Surface(
            'Living And Gibs Exterior Wall East',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_27, self.v_28, ceiling_height))
        self.surface_gibson_exterior_wall_south = Surface(
            'Gibs Exterior Wall South',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_28, self.v_29, ceiling_height))
        self.surface_study_exterior_wall_east = Surface(
            'Study Exterior Wall East',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_29, self.v_30, ceiling_height))
        self.surface_study_exterior_wall_south = Surface(
            'Study Exterior Wall South With Window',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_30, self.v_31, ceiling_height))
        self.surface_study_exterior_wall_west = Surface(
            'Study Exterior Wall West',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_31, self.v_32, ceiling_height))
        self.surface_main_bath_exterior_wall_south = Surface(
            'Main Bath Exterior Wall South',
            self.zone_conditioned, SurfaceType.WALL, self.construction_exterior_wall,
            BoundaryConditionType.OUTDOORS, None, 0.5, True, True,
            self._build_wall_vertices(self.v_32, self.v_1, ceiling_height))
        # now the ceilings/roofs - need to fix this up later
        self.surface_ceiling_conditioned_space = Surface(
            'Conditioned Space Ceiling',
            self.zone_conditioned, SurfaceType.ROOF, self.construction_roof,
            BoundaryConditionType.OUTDOORS, None, 0.0, True, True,
            self._add_height_to_vertices(ceiling_height, [
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
            ])
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
            self.zone_conditioned, SurfaceType.FLOOR, self.construction_floor,
            BoundaryConditionType.GROUND, None, 1.0, False, False,
            self._add_height_to_vertices(0.0, [
                self.v_1,
                self.v_2,
                self.v_3,
                self.v_4,
                self.v_5,
                self.v_6,
                self.v_7,
                self.v_8,
                self.v_9,
                self.v_10,
                self.v_34,
                self.v_35,
                self.v_36,
                self.v_20,
                self.v_21,
                self.v_22,
                self.v_23,
                self.v_24,
                self.v_25,
                self.v_26,
                self.v_27,
                self.v_28,
                self.v_29,
                self.v_30,
                self.v_31,
                self.v_32
            ])
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

    def surface_string(self) -> str:
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
        surface_string = ''
        for s in all_surfaces:
            surface_string += s.to_idf()
        return surface_string

    def zone_data_string(self) -> str:
        zone_string = ''
        zone_string += self.zone_conditioned.to_idf()
        zone_string += self.zone_garage.to_idf()
        return zone_string

    def material_data_string(self) -> str:
        material_string = ''
        material_string += self.material_brick.to_idf()
        material_string += self.material_sheathing.to_idf()
        material_string += self.material_wall_insulation.to_idf()
        material_string += self.material_gypsum.to_idf()
        material_string += self.material_shingles.to_idf()
        material_string += self.material_roof_insulation.to_idf()
        material_string += self.material_concrete.to_idf()
        material_string += self.material_wood_floor.to_idf()
        return material_string

    def construction_data_string(self) -> str:
        construction_string = ''
        construction_string += self.construction_exterior_wall.to_idf()
        construction_string += self.construction_insulated_partition_wall.to_idf()
        construction_string += self.construction_floor.to_idf()
        construction_string += self.construction_roof.to_idf()
        construction_string += self.construction_garage_floor.to_idf()
        return construction_string

    @staticmethod
    def header_data_string() -> str:
        return """
  Version, 9.3;

  Timestep, 4;

  Building,
    25095 Emerald Way,       !- Name
    0,                       !- North Axis {deg}
    Suburbs,                 !- Terrain
    0.5,                     !- Loads Convergence Tolerance Value {W}
    0.05,                    !- Temperature Convergence Tolerance Value {deltaC}
    MinimalShadowing,        !- Solar Distribution
    25,                      !- Maximum Number of Warmup Days
    3;                       !- Minimum Number of Warmup Days

  HeatBalanceAlgorithm, ConductionTransferFunction;

  SurfaceConvectionAlgorithm:Inside, TARP;

  SurfaceConvectionAlgorithm:Outside, DOE-2;

  SimulationControl,
    No,                      !- Do Zone Sizing Calculation
    No,                      !- Do System Sizing Calculation
    No,                      !- Do Plant Sizing Calculation
    No,                      !- Run Simulation for Sizing Periods
    Yes;                     !- Run Simulation for Weather File Run Periods

  RunPeriod,
    Run Period 1,            !- Name
    1,                       !- Begin Month
    1,                       !- Begin Day of Month
    2020,                    !- Begin Year
    12,                      !- End Month
    31,                      !- End Day of Month
    2020,                    !- End Year
    ,                        !- Day of Week for Start Day
    Yes,                     !- Use Weather File Holidays and Special Days
    Yes,                     !- Use Weather File Daylight Saving Period
    No,                      !- Apply Weekend Holiday Rule
    Yes,                     !- Use Weather File Rain Indicators
    Yes;                     !- Use Weather File Snow Indicators

 Site:Location,
    Cashion OK 73016,        !- Location Name
    35.798,                  !- Latitude {N+ S-}
    -97.679,                 !- Longitude {W- E+}
    -6.00,                   !- Time Zone Relative to GMT {GMT+/-}
    396.00;                  !- Elevation {m}

  Site:GroundTemperature:BuildingSurface,
    19.527, 19.502, 19.536, 19.598, 20.002, 21.640, 22.225, 22.375, 21.449, 20.121, 19.802, 19.633;

  GlobalGeometryRules,
    UpperLeftCorner,         !- Starting Vertex Position
    CounterClockWise,        !- Vertex Entry Direction
    World;                   !- Coordinate System
        \n"""

    @staticmethod
    def footer_data_string() -> str:
        return """
  Output:Variable,*,Site Outdoor Air Drybulb Temperature,hourly;

  Output:Variable,*,Site Daylight Saving Time Status,hourly;

  Output:Variable,*,Site Day Type Index,hourly;

  Output:Variable,*,Zone Mean Air Temperature,hourly;

  Output:Variable,*,Zone Mean Radiant Temperature,hourly;

  Output:Variable,*,Surface Inside Face Temperature,hourly;

  Output:Variable,*,Surface Outside Face Temperature,hourly;

  Output:Variable,*,Surface Outside Face Sunlit Fraction,hourly;

  Output:VariableDictionary,IDF;

  Output:Surfaces:Drawing,dxf:wireframe;

  Output:Constructions,Constructions;

  Output:Meter:MeterFileOnly,EnergyTransfer:Building,monthly;

  Output:Meter:MeterFileOnly,EnergyTransfer:Facility,monthly;

  Output:Meter:MeterFileOnly,Electricity:Facility,monthly;
  
  OutputControl:Table:Style,
    ALL;                     !- Column Separator

  Output:Table:SummaryReports,
    AllSummary;              !- Report 1 Name

  Output:Diagnostics,DisplayExtrawarnings;

        """

    @staticmethod
    def hvac_data_string() -> str:
        return """

  ScheduleTypeLimits,
    Discrete,
    0,
    1,
    Discrete;

  ScheduleTypeLimits,
    AnyNumber;

  Schedule:Constant,
    AlwaysOn,
    Discrete,
    1;

  Schedule:Constant,
    HeatingSetpoint,
    AnyNumber,
    21.1;

  Schedule:Constant,
    CoolingSetpoint,
    AnyNumber,
    23.9;
    
ThermostatSetpoint:DualSetpoint,
  Thermostat Dual SP Control,                              !- Name
  HeatingSetpoint,                                         !- Heating Setpoint Temperature Schedule Name
  CoolingSetpoint;                                         !- Cooling Setpoint Temperature Schedule Name

Schedule:Compact,
  HVACTemplate-Always 4,                                   !- Name
  AnyNumber,                                 !- Schedule Type Limits Name
  Through: 12/31,                                          !- Field 1
  For: AllDays,                                            !- Field 2
  Until: 24:00,                                            !- Field 3
  4;                                                       !- Field 4

ZoneControl:Thermostat,
  ConditionedSpace Thermostat,                             !- Name
  ConditionedSpace,                                        !- Zone or ZoneList Name
  HVACTemplate-Always 4,                                   !- Control Type Schedule Name
  ThermostatSetpoint:DualSetpoint,                         !- Control Object Type
  Thermostat Dual SP Control;                              !- Control Name

ZoneHVAC:EquipmentConnections,
  ConditionedSpace,                                        !- Zone Name
  ConditionedSpace Equipment,                              !- Zone Conditioning Equipment List Name
  ConditionedSpace Supply Inlet,                           !- Zone Air Inlet Node or NodeList Name
  ,                                                        !- Zone Air Exhaust Node or NodeList Name
  ConditionedSpace Zone Air Node,                          !- Zone Air Node Name
  ConditionedSpace Return Outlet;                          !- Zone Return Air Node Name

ZoneHVAC:EquipmentList,
  ConditionedSpace Equipment,                              !- Name
  SequentialLoad,                                          !- Load Distribution Scheme
  ZoneHVAC:AirDistributionUnit,                            !- Zone Equipment Object Type
  ConditionedSpace ATU,                                    !- Zone Equipment Name
  1,                                                       !- Zone Equipment Cooling Sequence
  1,                                                       !- Zone Equipment Heating or No-Load Sequence
  ,                                                        !- Zone Equipment Sequential Cooling Fraction Schedule Name
  ;                                                        !- Zone Equipment Sequential Heating Fraction Schedule Name

ZoneHVAC:AirDistributionUnit,
  ConditionedSpace ATU,                                    !- Name
  ConditionedSpace Supply Inlet,                           !- Air Distribution Unit Outlet Node Name
  AirTerminal:SingleDuct:ConstantVolume:NoReheat,          !- Air Terminal Object Type
  ConditionedSpace CV;                                     !- Air Terminal Name

AirTerminal:SingleDuct:ConstantVolume:NoReheat,
  ConditionedSpace CV,                                     !- Name
  ,                                                        !- Availability Schedule Name
  ConditionedSpace Zone Equip Inlet,                       !- Air Inlet Node Name
  ConditionedSpace Supply Inlet,                           !- Air Outlet Node Name
  0.755,                                                !- Maximum air flow rate {m3/s}
  ,                                                        !- Design Specification Outdoor Air Object Name
  ;                                                        !- Per Person Ventilation Rate Mode

AirLoopHVAC,
  HeatPump,                                                !- Name
  ,                                                        !- Controller List Name
  ,                          !- Availability Manager List Name
  0.755,                                                !- Design Supply Air Flow Rate {m3/s}
  HeatPump Branches,                                       !- Branch List Name
  ,                                                        !- Connector List Name
  HeatPump Air Loop Inlet,                                 !- Supply Side Inlet Node Name
  HeatPump Return Air Outlet,                              !- Demand Side Outlet Node Name
  HeatPump Supply Path Inlet,                              !- Demand Side Inlet Node Names
  HeatPump Air Loop Outlet;                                !- Supply Side Outlet Node Names

BranchList,
  HeatPump Branches,                                       !- Name
  HeatPump Main Branch;                                    !- Branch Name

Branch,
  HeatPump Main Branch,                                    !- Name
  ,                                                        !- Pressure Drop Curve Name
  AirLoopHVAC:UnitaryHeatPump:AirToAir,                    !- Component Object Type
  HeatPump Heat Pump,                                      !- Component Name
  HeatPump Air Loop Inlet,                               !- Component Inlet Node Name
  HeatPump Air Loop Outlet;                                !- Component Outlet Node Name

AirLoopHVAC:SupplyPath,
  HeatPump Supply Path,                                    !- Name
  HeatPump Supply Path Inlet,                              !- Supply Air Path Inlet Node Name
  AirLoopHVAC:ZoneSplitter,                                !- Component Object Type
  HeatPump Zone Splitter;                                  !- Component Name

AirLoopHVAC:ZoneSplitter,
  HeatPump Zone Splitter,                                  !- Name
  HeatPump Supply Path Inlet,                              !- Inlet Node Name
  ConditionedSpace Zone Equip Inlet;                       !- Outlet Node Name

AirLoopHVAC:ReturnPath,
  HeatPump Return Path,                                    !- Name
  HeatPump Return Air Outlet,                              !- Return Air Path Outlet Node Name
  AirLoopHVAC:ZoneMixer,                                   !- Component Object Type
  HeatPump Zone Mixer;                                     !- Component Name

AirLoopHVAC:ZoneMixer,
  HeatPump Zone Mixer,                                     !- Name
  HeatPump Return Air Outlet,                              !- Outlet Node Name
  ConditionedSpace Return Outlet;                          !- Inlet Node Name

AirLoopHVAC:UnitaryHeatPump:AirToAir,
  HeatPump Heat Pump,                                      !- Name
  ,                                                        !- Availability Schedule Name
  HeatPump Air Loop Inlet,                               !- Air Inlet Node Name
  HeatPump Air Loop Outlet,                                !- Air Outlet Node Name
  0.755,                                                   !- Cooling Supply Air Flow Rate
  0.755,                                                   !- Heating Supply Air Flow Rate
  0.755,                                                   !- No Load Supply Air Flow Rate
  ConditionedSpace,                                        !- Controlling Zone or Thermostat Location
  Fan:OnOff,                                               !- Supply Air Fan Object Type
  HeatPump Supply Fan,                                     !- Supply Air Fan Name
  Coil:Heating:DX:SingleSpeed,                             !- Heating Coil Object Type
  HeatPump HP Heating Coil,                                !- Heating Coil Name
  Coil:Cooling:DX:SingleSpeed,                             !- Cooling Coil Object Type
  HeatPump Cooling Coil,                                   !- Cooling Coil Name
  Coil:Heating:Electric,                                   !- Supplemental Heating Coil Object Type
  HeatPump Sup Heat Coil,                                  !- Supplemental Heating Coil Name
  40,                                                !- Maximum Supply Air Temperature from Supplemental Heater
  21,                                                      !- Maximum Outdoor Dry-Bulb Temperature for Supplemental Heater Operation
  BlowThrough,                                             !- Fan Placement
  HVACTemplate-Always 0;                                   !- Supply Air Fan Operating Mode Schedule Name

Schedule:Compact,
  HVACTemplate-Always 0,                                   !- Name
  AnyNumber,                                 !- Schedule Type Limits Name
  Through: 12/31,                                          !- Field 1
  For: AllDays,                                            !- Field 2
  Until: 24:00,                                            !- Field 3
  0;                                                       !- Field 4

Coil:Heating:DX:SingleSpeed,
  HeatPump HP Heating Coil,                                !- Name
  ,                                                        !- Availability Schedule Name
  14067,                                                   !- Rated Total Heating Capacity {W}
  2.75,                                                    !- Rated COP
  0.755,                                                   !- Rated Air Flow Rate {m3/s}
  ,                                                        !- Rated Evaporator Fan Power Per Volume Flow Rate
  HeatPump Cooling Coil Outlet,                            !- Air Inlet Node Name
  HeatPump Heating Coil Outlet,                            !- Air Outlet Node Name
  HeatPump HP Heating Coil Cap-FT,                         !- Total Heating Capacity Function of Temperature Curve Name
  HeatPump HP Heating Coil Cap-FF,                         !- Total Heating Capacity Function of Flow Fraction Curve Name
  HeatPump HP Heating Coil EIR-FT,                         !- Energy Input Ratio Function of Temperature Curve Name
  HeatPump HP Heating Coil EIR-FF,                         !- Energy Input Ratio Function of Flow Fraction Curve Name
  HeatPump HP Heating Coil PLF,                            !- Part Load Fraction Correlation Curve Name
  HeatPump HP Heating Coil DefrEIR-FT,                     !- Defrost Energy Input Ratio Function of Temperature Curve Name
  -8,                                                      !- Minimum Outdoor Dry-Bulb Temperature for Compressor Operation {C}
  ,                                                        !- Outdoor Dry-Bulb Temperature to Turn On Compressor
  5,                                                       !- Maximum Outdoor Dry-Bulb Temperature for Defrost Operation {C}
  0,                                                       !- Crankcase Heater Capacity {W}
  0,                                                       !- Maximum Outdoor Dry-Bulb Temperature for Crankcase Heater Operation {C}
  ReverseCycle,                                            !- Defrost Strategy
  Timed,                                                   !- Defrost Control
  0.058333,                                                !- Defrost Time Period Fraction
  1000;                                                !- Resistive Defrost Heater Capacity {W}

Curve:Cubic,
  HeatPump HP Heating Coil Cap-FT,                         !- Name
  0.758746,                                                !- Coefficient1 Constant
  0.027626,                                                !- Coefficient2 x
  0.000148716,                                             !- Coefficient3 x**2
  0.0000034992,                                            !- Coefficient4 x**3
  -20.0,                                                   !- Minimum Value of x
  20.0;                                                    !- Maximum Value of x

Curve:Cubic,
  HeatPump HP Heating Coil Cap-FF,                         !- Name
  0.84,                                                    !- Coefficient1 Constant
  0.16,                                                    !- Coefficient2 x
  0.0,                                                     !- Coefficient3 x**2
  0.0,                                                     !- Coefficient4 x**3
  0.5,                                                     !- Minimum Value of x
  1.5;                                                     !- Maximum Value of x

Curve:Cubic,
  HeatPump HP Heating Coil EIR-FT,                         !- Name
  1.19248,                                                 !- Coefficient1 Constant
  -0.0300438,                                              !- Coefficient2 x
  0.00103745,                                              !- Coefficient3 x**2
  -0.000023328,                                            !- Coefficient4 x**3
  -20.0,                                                   !- Minimum Value of x
  20.0;                                                    !- Maximum Value of x

Curve:Quadratic,
  HeatPump HP Heating Coil EIR-FF,                         !- Name
  1.3824,                                                  !- Coefficient1 Constant
  -0.4336,                                                 !- Coefficient2 x
  0.0512,                                                  !- Coefficient3 x**2
  0.0,                                                     !- Minimum Value of x
  1.0;                                                     !- Maximum Value of x

Curve:Quadratic,
  HeatPump HP Heating Coil PLF,                            !- Name
  0.75,                                                    !- Coefficient1 Constant
  0.25,                                                    !- Coefficient2 x
  0.0,                                                     !- Coefficient3 x**2
  0.0,                                                     !- Minimum Value of x
  1.0;                                                     !- Maximum Value of x

Curve:Biquadratic,
  HeatPump HP Heating Coil DefrEIR-FT,                     !- Name
  1,                                                       !- Coefficient1 Constant
  0,                                                       !- Coefficient2 x
  0,                                                       !- Coefficient3 x**2
  0,                                                       !- Coefficient4 y
  0,                                                       !- Coefficient5 y**2
  0,                                                       !- Coefficient6 x*y
  0,                                                       !- Minimum Value of x
  50,                                                      !- Maximum Value of x
  0,                                                       !- Minimum Value of y
  50;                                                      !- Maximum Value of y

Coil:Heating:Electric,
  HeatPump Sup Heat Coil,                                  !- Name
  ,                                                        !- Availability Schedule Name
  1,                                                       !- Efficiency
  10000,                                                   !- Nominal Capacity of the Coil {W}
  HeatPump Heating Coil Outlet,                            !- Air Inlet Node Name
  HeatPump Air Loop Outlet,                                !- Air Outlet Node Name
  ;                                                        !- Coil Temp Setpoint Node

Coil:Cooling:DX:SingleSpeed,
  HeatPump Cooling Coil,                                   !- Name
  ,                                                        !- Availability Schedule Name
  14067,                                                   !- Gross Rated Total Cooling Capacity {W}
  0.7,                                                     !- Gross Rated Sensible Heat Ratio
  3,                                                       !- Rated COP
  0.755,                                                   !- Rated Air Flow Rate {m3/s}
  ,                                                        !- Rated Evaporator Fan Power per Volume Flow Rate {W/(m3/s)}
  HeatPump Supply Fan Outlet,                              !- Air Inlet Node Name
  HeatPump Cooling Coil Outlet,                            !- Air Outlet Node Name
  HeatPump Cool Coil Cap-FT,                               !- Total Cooling Capacity Function of Temperature Curve Name
  HeatPump Cool Coil Cap-FF,                               !- Total Cooling Capacity Function of Flow Fraction Curve Name
  HeatPump Cool Coil EIR-FT,                               !- Energy Input Ratio Function of Temperature Curve Name
  HeatPump Cool Coil EIR-FF,                               !- Energy Input Ratio Function of Flow Fraction Curve Name
  HeatPump Cool Coil PLF,                                  !- Part Load Fraction Correlation Curve Name
  ,                                                        !- Minimum Outdoor Dry-Bulb Temperature for Compressor Operation {C}
  0,                                                       !- Nominal Time for Condensate Removal to Begin
  0,                                                       !- Ratio of Initial Moisture Evaporation Rate and Steady State Latent Capacity
  0,                                                       !- Maximum Cycling Rate
  0,                                                       !- Latent Capacity Time Constant
  HeatPump Cooling Coil Condenser Inlet,                   !- Condenser Air Inlet Node Name
  AirCooled,                                               !- Condenser Type
  0,                                                       !- Evaporative Condenser Effectiveness
  ,                                                        !- Evaporative Condenser Air Flow Rate
  0,                                                       !- Evaporative Condenser Pump Rated Power Consumption
  0,                                                       !- Crankcase Heater Capacity
  10;                                                      !- Maximum Outdoor Dry-Bulb Temperature for Crankcase Heater Operation

Curve:Biquadratic,
! DOE-2.1E, COOL-CAP-FT for PTAC w/ SI temps
  HeatPump Cool Coil Cap-FT,                               !- Name
  0.942587793,                                             !- Coefficient1 Constant
  0.009543347,                                             !- Coefficient2 x
  0.00068377,                                              !- Coefficient3 x**2
  -0.011042676,                                            !- Coefficient4 y
  0.000005249,                                             !- Coefficient5 y**2
  -0.00000972,                                             !- Coefficient6 x*y
  12.77778,                                                !- Minimum Value of x
  23.88889,                                                !- Maximum Value of x
  18.0,                                                    !- Minimum Value of y
  46.11111;                                                !- Maximum Value of y

Curve:Quadratic,
! DOE-2.1E, RATED-CCAP-FFLOW for PTAC
  HeatPump Cool Coil Cap-FF,                               !- Name
  0.8,                                                     !- Coefficient1 Constant
  0.2,                                                     !- Coefficient2 x
  0,                                                       !- Coefficient3 x**2
  0.5,                                                     !- Minimum Value of x
  1.5;                                                     !- Maximum Value of x

Curve:Biquadratic,
! DOE-2.1E, COOL-EIR-FT for PTAC w/ SI temps
  HeatPump Cool Coil EIR-FT,                               !- Name
  0.342414409,                                             !- Coefficient1 Constant
  0.034885008,                                             !- Coefficient2 x
  -0.0006237,                                              !- Coefficient3 x**2
  0.004977216,                                             !- Coefficient4 y
  0.000437951,                                             !- Coefficient5 y**2
  -0.000728028,                                            !- Coefficient6 x*y
  12.77778,                                                !- Minimum Value of x
  23.88889,                                                !- Maximum Value of x
  18.0,                                                    !- Minimum Value of y
  46.11111;                                                !- Maximum Value of y

Curve:Quadratic,
! DOE-2.1E, RATED-CEIR-FFLOW for PTAC
  HeatPump Cool Coil EIR-FF,                               !- Name
  1.1552,                                                  !- Coefficient1 Constant
  -0.1808,                                                 !- Coefficient2 x
  0.0256,                                                  !- Coefficient3 x**2
  0.5,                                                     !- Minimum Value of x
  1.5;                                                     !- Maximum Value of x

Curve:Quadratic,
! PLF = l.- Cd(1.-PLR) where Cd = 0.15
  HeatPump Cool Coil PLF,                                  !- Name
  0.85,                                                    !- Coefficient1 Constant
  0.15,                                                    !- Coefficient2 x
  0,                                                       !- Coefficient3 x**2
  0,                                                       !- Minimum Value of x
  1;                                                       !- Maximum Value of x

OutdoorAir:Node,
  HeatPump Cooling Coil Condenser Inlet,                   !- Name
  -1;                                                      !- Height Above Ground

Fan:OnOff,
  HeatPump Supply Fan,                                     !- Name
  AlwaysOn,                                                !- Availability Schedule Name
  0.7,                                                     !- Fan Efficiency
  600,                                                     !- Pressure Rise {Pa}
  0.755,                                                !- Maximum Flow Rate {m3/s}
  0.9,                                                     !- Motor Efficiency
  1,                                                       !- Motor in Airstream Fraction
  HeatPump Air Loop Inlet,                               !- Air Inlet Node Name
  HeatPump Supply Fan Outlet;                              !- Air Outlet Node Name

SetpointManager:SingleZone:Cooling,
  HeatPump Economizer Supply Air Temp Manager,             !- Name
  Temperature,                                             !- Control Variable
  13,                                                      !- minimum supply air temperature {C}
  45,                                                      !- maximum supply air temperature {C}
  ConditionedSpace,                                        !- Control Zone Name
  ConditionedSpace Zone Air Node,                          !- Zone Node Name
  ConditionedSpace Supply Inlet,                           !- Zone Inlet Node Name
  HeatPump Air Loop Outlet;                                !- Setpoint Node or NodeList Name

        \n"""