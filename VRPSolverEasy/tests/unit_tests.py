import random
import unittest
import os
from VRPSolverEasy.src import solver, constants
from VRPSolverEasy.demos import CVRPTW,CVRP,HFVRP,MDVRP

class TestAllVariants(unittest.TestCase):

    def test_cvrp(self):
        """test model in there is only resource of capacity
        with optimal solution"""
        dist = 5
        cost_per_distance = 10
        nb_links = 5
        model = solver.Model()
        model.add_vehicle_type(
            1,
            0,
            0,
            "VEH1",
            capacity=100,
            max_number=3,
            var_cost_dist=cost_per_distance)
        model.add_depot(id=0, name="D1")
        for i in range(1, 5):
            model.add_customer(id=i, name="C" + str(i), demand=20)
        model.add_link(name="arc1", start_point_id=0, end_point_id=1, distance=dist)
        model.add_link(name="arc2", start_point_id=1, end_point_id=2, distance=dist)
        model.add_link(name="arc3", start_point_id=2, end_point_id=3, distance=dist)
        model.add_link(name="arc4", start_point_id=3, end_point_id=4, distance=dist)
        model.add_link(name="arc5", start_point_id=4, end_point_id=0, distance=dist)

        # model.export("cvrp",true) DEBUG MODE

        model.solve()
        cost = dist * cost_per_distance * nb_links
        self.assertEqual(constants.OPTIMAL_SOL_FOUND, model.status)
        self.assertAlmostEqual(
            cost, model.solution.value, places=5)

    def test_cvrp_no_feasible(self):
        """test model in there is only resource of capacity
        with no feasible solution"""
        model = solver.Model()
        model.add_vehicle_type(
            1,
            0,
            0,
            "VEH1",
            capacity=50,
            max_number=3,
            var_cost_dist=10)
        model.add_depot(id=0, name="D1")
        for i in range(1, 5):
            model.add_customer(id=i, name="C" + str(i), demand=20)
        model.add_link(name="arc1", start_point_id=0, end_point_id=1, distance=5)
        model.add_link(name="arc2", start_point_id=1, end_point_id=2, distance=6)
        model.add_link(name="arc3", start_point_id=2, end_point_id=3, distance=4)
        model.add_link(name="arc4", start_point_id=3, end_point_id=4, distance=4)
        model.add_link(name="arc5", start_point_id=4, end_point_id=0, distance=4)
        model.solve()

        # model.export("cvrp_noFeasible",true) DEBUG MODE

        self.assertEqual(
            constants.BETTER_SOL_DOES_NOT_EXISTS,
            model.status)

    def test_cvrptw(self):
        """test model in there is two resources time and capacity"""
        cost_per_time = 10
        cost_per_distance = 10
        dist = 5
        nb_links = 5
        model = solver.Model()
        model.add_vehicle_type(
            1,
            0,
            0,
            "VEH1",
            capacity=200,
            max_number=3,
            var_cost_dist=cost_per_distance,
            var_cost_time=cost_per_time,
            tw_end=200)
        model.add_depot(id=0, name="D1", tw_begin=0, tw_end=200)
        time_between_points = 4
        begin_time = 0
        for i in range(1, 5):
            model.add_customer(
                id=i,
                name="C" + str(i),
                demand=20,
                tw_begin=begin_time,
                tw_end=begin_time + 5)
            begin_time += 5
        model.add_link(
            name="arc1",
            start_point_id=0,
            end_point_id=1,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc2",
            start_point_id=1,
            end_point_id=2,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc3",
            start_point_id=2,
            end_point_id=3,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc4",
            start_point_id=3,
            end_point_id=4,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc5",
            start_point_id=4,
            end_point_id=0,
            distance=dist,
            time=time_between_points)
        model.solve()       
        model.export("cvrptw")
        cost = ((dist * cost_per_distance) +
                (time_between_points * cost_per_time)) * nb_links
        self.assertEqual(constants.OPTIMAL_SOL_FOUND, model.status)
        self.assertAlmostEqual(
            cost, model.solution.value, places=5)
        print(model.solution)

    def test_cvrptw_with_parallel_arcs(self):
        """test model in there is two resources time and capacity 
        and parallel arcs"""
        cost_per_time = 10
        cost_per_distance = 10
        dist = 5
        nb_links = 5
        model = solver.Model()
        model.add_vehicle_type(
            1,
            0,
            0,
            "VEH1",
            capacity=200,
            max_number=3,
            var_cost_dist=cost_per_distance,
            var_cost_time=cost_per_time,
            tw_end=200)
        model.add_depot(id=0, name="D1", tw_begin=0, tw_end=200)
        time_between_points = 4
        begin_time = 0
        for i in range(1, 5):
            model.add_customer(
                id=i,
                name="C" + str(i),
                demand=20,
                tw_begin=begin_time,
                tw_end=begin_time + 5)
            begin_time += 5
        model.add_link(
            name="arc1",
            start_point_id=0,
            end_point_id=1,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc2",
            start_point_id=1,
            end_point_id=2,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc3",
            start_point_id=2,
            end_point_id=3,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc4",
            start_point_id=3,
            end_point_id=4,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc5",
            start_point_id=4,
            end_point_id=0,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc6",
            start_point_id=4,
            end_point_id=0,
            distance=dist,
            time=1,
            fixed_cost=5)
        model.solve()       
        self.assertEqual(constants.OPTIMAL_SOL_FOUND, model.status)
        self.assertAlmostEqual(
            425, model.solution.value, places=5)
        print(model.solution)

    def test_cvrptw_nofeasible_on_time(self):
        """test model it's infeasible on time"""
        model = solver.Model()
        model.add_vehicle_type(
            1,
            0,
            0,
            "VEH1",
            capacity=200,
            max_number=3,
            var_cost_dist=10,
            var_cost_time=10)
        model.add_depot(id=0, name="D1", tw_begin=0, tw_end=10)
        time_between_points = 3
        begin_time = 0
        for i in range(1, 5):
            model.add_customer(
                id=i,
                name="C" + str(i),
                demand=20,
                tw_begin=begin_time,
                tw_end=begin_time + 5)
            begin_time += 5
        model.add_link(
            name="arc1",
            start_point_id=0,
            end_point_id=1,
            distance=5,
            time=time_between_points)
        model.add_link(
            name="arc2",
            start_point_id=1,
            end_point_id=2,
            distance=6,
            time=time_between_points)
        model.add_link(
            name="arc3",
            start_point_id=2,
            end_point_id=3,
            distance=4,
            time=time_between_points)
        model.add_link(
            name="arc4",
            start_point_id=3,
            end_point_id=4,
            distance=4,
            time=time_between_points)
        model.add_link(
            name="arc5",
            start_point_id=4,
            end_point_id=0,
            distance=4,
            time=time_between_points)
        model.solve()
        
        print(model.solution)
        print(model.message)
        self.assertEqual(
            constants.VEHICLES_ERROR,
            model.status)

    def test_ovrptw(self):
        """test variant open vehicle routing problem with time windows"""
        cost_per_time = 10
        cost_per_distance = 10
        dist = 5
        nb_links = 5
        model = solver.Model()
        model.add_vehicle_type(
            1,
            0,
            -1,
            "VEH1",
            capacity=200,
            max_number=3,
            var_cost_dist=cost_per_distance,
            var_cost_time=cost_per_time,
            tw_end=200)
        model.add_depot(id=0, name="D1", tw_begin=0, tw_end=200)
        time_between_points = 4
        begin_time = 0
        for i in range(1, 5):
            model.add_customer(
                id=i,
                name="C" + str(i),
                demand=20,
                tw_begin=begin_time,
                tw_end=begin_time + 5)
            begin_time += 5
        model.add_link(
            name="arc1",
            start_point_id=0,
            end_point_id=1,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc2",
            start_point_id=1,
            end_point_id=2,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc3",
            start_point_id=2,
            end_point_id=3,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc4",
            start_point_id=3,
            end_point_id=4,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc5",
            start_point_id=4,
            end_point_id=0,
            distance=dist,
            time=time_between_points)
        model.solve()       
        self.assertEqual(constants.OPTIMAL_SOL_FOUND, model.status)
        print(model.solution)
        print(model.message)
        self.assertAlmostEqual(
            360, model.solution.value, places=5)
        print(model.solution)

    def test_solve_without_all(self):
        """raise an error if we have any components in the model"""
        model = solver.Model()
        with self.assertRaises(Exception):
            model.solve()

    def test_solve_without_points_links(self):
        """raise an error if we have only vehicle types in the model"""
        model = solver.Model()
        with self.assertRaises(Exception):
            model.add_vehicle_type(
                1,
                0,
                0,
                "VEH1",
                capacity=200,
                max_number=3,
                var_cost_dist=10,
                var_cost_time=10)
            model.solve()

    def test_solve_without_links(self):
        """raise an error if we have any links"""
        model = solver.Model()
        with self.assertRaises(Exception):
            model.add_vehicle_type(
                1,
                0,
                0,
                "VEH1",
                capacity=200,
                max_number=3,
                var_cost_dist=10,
                var_cost_time=10)
            model.add_depot(id=0, name="D1", tw_begin=0, tw_end=10)
            model.solve()

    def test_solve_without_points(self):
        """raise an error if we have any links"""
        model = solver.Model()
        with self.assertRaises(Exception):
            model.add_vehicle_type(
                1,
                0,
                0,
                "VEH1",
                capacity=200,
                max_number=3,
                var_cost_dist=10,
                var_cost_time=10)
            model.add_link(
                name="arc1",
                start_point_id=0,
                end_point_id=1,
                distance=5,
                time=5)
            model.solve()
        print(model.solution)

    def test_solve_without_customers(self):
        """raise an error if we have a unknown points in links"""
        model = solver.Model()
        model.add_vehicle_type(
            1,
            0,
            0,
            "VEH1",
            capacity=200,
            max_number=3,
            var_cost_dist=10,
            var_cost_time=10)
        model.add_link(
            name="arc1",
            start_point_id=0,
            end_point_id=1,
            distance=5,
            time=5)
        model.add_depot(id=0, name="D1", tw_begin=0, tw_end=10)
        model.solve()
        print(model.solution)
        self.assertEqual(constants.LINKS_ERROR, model.status)


class TestAllClass(unittest.TestCase):

    def test_vehicle_type_with_wrong_properties(self):
        """raise an error the properties of vehicle types are not respected"""
        model = solver.Model()
        # check three non-optional parameters

        # check id vehicle >1
        with self.assertRaises(solver.PropertyError):
            model.add_vehicle_type(0, 2, 6)

        # check start point >-1
        with self.assertRaises(solver.PropertyError):
            model.add_vehicle_type(3, -2, 6)

        # check end point >-1
        with self.assertRaises(solver.PropertyError):
            model.add_vehicle_type(4, 2, -6)

        # check type name
        with self.assertRaises(solver.PropertyError):
            model.add_vehicle_type(4, 2, 3, 5)

        # check max_number>0
        with self.assertRaises(solver.PropertyError):
            model.add_vehicle_type(
                4, 2, 6, "veh1", -5, fixed_cost=5, max_number=-8)

    def test_add_in_dict_vehicle_types(self):
        """ we must have a new vehicle type in dict vehicle_types after add"""
        model = solver.Model()
        model.add_vehicle_type(id=5, start_point_id=3, end_point_id=2)
        self.assertIn(5, model.vehicle_types)

    def test_delete_in_dict_vehicle_types(self):
        """ the old vehicle type must be removed from dict after delete"""
        model = solver.Model()
        model.add_vehicle_type(id=5, start_point_id=3, end_point_id=2)
        model.delete_vehicle_type(5)
        self.assertNotIn(5, model.vehicle_types)

    def test_add_vehicle_types_without_function(self):
        """ we can set vehicle types by using directly the dictionary """
        model = solver.Model()
        model.vehicle_types[1] = solver.VehicleType(1, 2, 3)
        self.assertIn(1, model.vehicle_types)

    def test_add_bad_vehicle_types(self):
        """ raise an error if the setting of vehicle_type is not correct"""
        model = solver.Model()
        with self.assertRaises(solver.PropertyError):
            model.vehicle_types[1] = 5

    def test_point_with_wrong_properties(self):
        """raise an error the properties of point are not respected"""
        model = solver.Model()

        # check id non optional parameter
        with self.assertRaises(Exception):
            model.add_point()

        # check type name
        with self.assertRaises(solver.PropertyError):
            model.add_point(1, name=5)

        # check id_customer >0
        with self.assertRaises(solver.PropertyError):
            model.add_point(5, id_customer=-5)

        # check id_customer <1022
        with self.assertRaises(solver.PropertyError):
            model.add_point(5, id_customer=1054)

        # check demand is integer
        with self.assertRaises(solver.PropertyError):
            model.add_point(5, demand=3.5)

        # check demand>0
        with self.assertRaises(solver.PropertyError):
            model.add_point(5, demand=-20)

    def test_add_in_dict_point(self):
        """ we must have a new point in dict points after add"""
        model = solver.Model()
        model.add_point(id=5)
        self.assertIn(5, model.points)

    def test_dict_points_for_delete(self):
        """ the old point must be removed from dict after delete"""
        model = solver.Model()
        model.add_vehicle_type(id=5, start_point_id=3, end_point_id=2)
        model.delete_vehicle_type(5)
        self.assertNotIn(5, model.vehicle_types)

    def test_add_points_without_function(self):
        """ we can set point by using directly the dictionary """
        model = solver.Model()
        model.points[1] = solver.Point(1)
        self.assertIn(1, model.points)

    def test_add_bad_point(self):
        """ raise an error if the setting of point is not correct"""
        model = solver.Model()
        with self.assertRaises(solver.PropertyError):
            model.vehicle_types[1] = {1: 5}

    def test_link_with_wrong_properties(self):
        """ raise error if the user gives bad type of variables """
        model = solver.Model()

        # check is_directed
        with self.assertRaises(Exception):
            model.add_link(is_directed=9)

        # check type startpoint
        with self.assertRaises(solver.PropertyError):
            model.add_link(start_point_id="C1")

        # check type startpoint
        with self.assertRaises(solver.PropertyError):
            model.add_link(end_point_id="C2")

        # check distance must be >= 0
        with self.assertRaises(solver.PropertyError):
            model.add_link(distance=-51)

        # check time must be >= 0
        with self.assertRaises(solver.PropertyError):
            model.add_link(time=-52)

        # check fixed cost must be a number
        with self.assertRaises(solver.PropertyError):
            model.add_link(fixed_cost=[1, 2])

    def test_add_customer(self):
        """ dict of points must be contain new customer """
        model = solver.Model()
        model.add_customer(5, "C1")
        self.assertIn(5, model.points)

    def test_id_customer(self):
        """ if any id_customer is given, id_customer mus be equal to id """
        model = solver.Model()
        model.add_customer(5, "C1")
        self.assertEqual(5, model.points[5].id_customer)

    def test_id_customer_with_id_too_bigger(self):
        """ raise an error if id_customer is not given by user and id >1022 """
        model = solver.Model()
        with self.assertRaises(solver.PropertyError):
            model.add_customer(1025, "C1")

    def test_id_customer_with_id_different(self):
        """ assert id_customer is different of id if it's
            given by the user """
        model = solver.Model()
        model.add_customer(1025, "C1", id_customer=5)
        self.assertEqual(model.points[1025].id_customer, 5)

    def test_add_depot(self):
        """The id_customer of depot must be equal to 0. """
        model = solver.Model()
        model.add_depot(5, "C1")
        model.add_depot(9999, "C1")
        self.assertEqual(0, model.points[5].id_customer)
        self.assertEqual(0, model.points[9999].id_customer)

    def test_solution(self):
        """ test class solution after resolving a cvrptw problem """
        dist_max = 15
        time_max = 15
        cost_per_distance = 10
        cost_per_time = 10
        model = solver.Model()
        model.add_vehicle_type(
            1,
            0,
            0,
            "VEH1",
            capacity=100,
            max_number=3,
            var_cost_dist=cost_per_distance,
            var_cost_time=cost_per_time,
            tw_begin=0,
            tw_end=200)
        model.add_depot(id=0, name="D1", tw_end=200)

        for i in range(1, 5):
            model.add_customer(id=i, name="C" + str(i), demand=20, tw_end=200)

        # Here the arcs of solutions
        model.add_link(
            name="arc1",
            start_point_id=0,
            end_point_id=1,
            distance=1,
            time=1)
        model.add_link(
            name="arc2",
            start_point_id=1,
            end_point_id=2,
            distance=2,
            time=2)
        model.add_link(
            name="arc3",
            start_point_id=2,
            end_point_id=3,
            distance=3,
            time=3)
        model.add_link(
            name="arc4",
            start_point_id=3,
            end_point_id=4,
            distance=4,
            time=4)
        model.add_link(
            name="arc5",
            start_point_id=4,
            end_point_id=0,
            distance=5,
            time=5)

        # Here the available arcs but more expensive
        for i in range(25):
            model.add_link(name="arc_forbidden" + str(i),
                       start_point_id=random.randint(0, 4),
                       end_point_id=random.randint(0, 4),
                       distance=dist_max, time=time_max)

        # solve model
        model.solve()
        cost = sum(i * cost_per_distance for i in range(1, 6)) * 2

        # test defined solution
        self.assertEqual(model.solution.is_defined(), True)

        # test status
        self.assertEqual(constants.OPTIMAL_SOL_FOUND, model.status)

        # test solution value
        self.assertAlmostEqual(
            cost, model.solution.value, places=5)

        # test ids
        self.assertIn(model.solution.routes[0].point_ids, [[0, 1, 2, 3, 4, 0],
                                                       [0, 4, 3, 2, 1, 0]])

        # test arcs names
        self.assertIn(model.solution.routes[0].incoming_arc_names,
                      [["", "arc1", "arc2", "arc3", "arc4", "arc5"],
                       ["", "arc5", "arc4", "arc3", "arc2", "arc1"]])

        # test arcs names
        self.assertEqual(model.solution.routes[0].cap_consumption,
                         [0,
                          20,
                          40,
                          60,
                          80,
                          80])

        # test vehicle type id
        self.assertEqual(model.solution.routes[0].vehicle_type_id, 1)

        # test time consumption
        self.assertIn(model.solution.routes[0].time_consumption,
                      [[0, 5, 9, 12, 14, 15],
                      [0, 1, 3, 6, 10, 15]])

    def test_enumerate(self):
        """ test enumeration of all feasibles solutions """
        cost_per_time = 10
        cost_per_distance = 10
        dist = 5
        model = solver.Model()
        model.add_vehicle_type(
            1,
            0,
            0,
            "VEH1",
            capacity=200,
            max_number=3,
            var_cost_dist=cost_per_distance,
            var_cost_time=cost_per_time,
            tw_end=200)
        model.add_depot(id=0, name="D1", tw_begin=0, tw_end=200)
        time_between_points = 4
        begin_time = 0
        for i in range(1, 5):
            model.add_customer(
                id=i,
                name="C" + str(i),
                demand=20,
                tw_begin=begin_time,
                tw_end=begin_time + 5)
            begin_time += 5
        model.add_link(
            name="arc1",
            start_point_id=0,
            end_point_id=1,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc2",
            start_point_id=1,
            end_point_id=2,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc3",
            start_point_id=2,
            end_point_id=3,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc4",
            start_point_id=3,
            end_point_id=4,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc5",
            start_point_id=4,
            end_point_id=0,
            distance=dist,
            time=time_between_points)
        model.set_parameters(action="enumAllFeasibleRoutes")
        model.solve()
        print(model.solution)
        model.export("enumerate-cvrptw")

    def test_config_file(self):
        """ test configuration file for advanced parametrisation """
        cost_per_time = 10
        cost_per_distance = 10
        dist = 5
        model = solver.Model()
        model.add_vehicle_type(
            1,
            0,
            0,
            "VEH1",
            capacity=200,
            max_number=3,
            var_cost_dist=cost_per_distance,
            var_cost_time=cost_per_time,
            tw_end=200)
        model.add_depot(id=0, name="D1", tw_begin=0, tw_end=200)
        time_between_points = 4
        begin_time = 0
        for i in range(1, 5):
            model.add_customer(
                id=i,
                name="C" + str(i),
                demand=20,
                tw_begin=begin_time,
                tw_end=begin_time + 5)
            begin_time += 5
        model.add_link(
            name="arc1",
            start_point_id=0,
            end_point_id=1,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc2",
            start_point_id=1,
            end_point_id=2,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc3",
            start_point_id=2,
            end_point_id=3,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc4",
            start_point_id=3,
            end_point_id=4,
            distance=dist,
            time=time_between_points)
        model.add_link(
            name="arc5",
            start_point_id=4,
            end_point_id=0,
            distance=dist,
            time=time_between_points)
        path_project = os.path.join(os.path.dirname
                                            (os.path.realpath(__file__)))
        model.set_parameters(config_file=path_project +
                             os.path.normpath(
                                "/config/bc.cfg" ))
        print(path_project)
        model.solve()
        print(model.solution)

class TestAllDemos(unittest.TestCase):
    def test_cvrp_demos_an32k5(self):
        """test demo A-n32-k5 in augerat format"""
        path_project = os.path.join(os.path.dirname
                                            (os.path.realpath(__file__ + "/../")))
        path_demo = path_project + os.path.normpath(
                                "/demos/data/CVRP/A-n32-k5.vrp")
        objective_value = CVRP.solve_demo(path_demo)
        self.assertAlmostEqual(
            784, objective_value, places=0)
        return None

    def test_cvrp_demos_bn31k5(self):
        """test demo B-n31-k5 in augerat format"""
        path_project = os.path.join(os.path.dirname
                                            (os.path.realpath(__file__ + "/../")))
        path_demo = path_project + os.path.normpath(
                                "/demos/data/CVRP/B-n31-k5.vrp")
        objective_value = CVRP.solve_demo(path_demo)
        self.assertAlmostEqual(
            672, objective_value, places=1)
        return None

    def test_cvrptw_demos_c101(self):
        """test demo C101 in solomon format"""
        path_project = os.path.join(os.path.dirname
                                            (os.path.realpath(__file__ + "/../")))
        path_demo = path_project + os.path.normpath(
                                "/demos/data/CVRPTW/C101.txt")
        objective_value = CVRPTW.solve_demo(path_demo)
        self.assertAlmostEqual(
            828.95, objective_value, places=1)
        return None

    def test_cvrptw_demos_r101(self):
        """test demo R101 in solomon format"""
        path_project = os.path.join(os.path.dirname
                                            (os.path.realpath(__file__ + "/../")))
        path_demo = path_project + os.path.normpath(
                                "/demos/data/CVRPTW/R101.txt")
        objective_value = CVRPTW.solve_demo(path_demo)
        self.assertAlmostEqual(
            1642.875, objective_value, places=1)
        return None

    def test_hfvrp_c50_13fsmd(self):
        """test demo c50_13fsmd in queiroga format"""
        path_project = os.path.join(os.path.dirname
                                            (os.path.realpath(__file__ + "/../")))
        path_demo = path_project + os.path.normpath(
                                "/demos/data/HFVRP/c50_13fsmd.txt")
        objective_value = HFVRP.solve_demo(path_demo)
        self.assertAlmostEqual(
           1491.85, objective_value, places=1)
        return None

    def test_hfvrp_c50_16fsmd(self):
        """test demo c50_16fsmd in queiroga format"""
        path_project = os.path.join(os.path.dirname
                                            (os.path.realpath(__file__ + "/../")))
        path_demo = path_project + os.path.normpath(
                                "/demos/data/HFVRP/c50_16fsmd.txt")
        objective_value = HFVRP.solve_demo(path_demo)
        self.assertAlmostEqual(
            1131, objective_value, places=1)
        return None

    def test_mdvrp_p01(self):
        """test demo p01 in Cordeau format"""
        path_project = os.path.join(os.path.dirname
                                            (os.path.realpath(__file__ + "/../")))
        path_demo = path_project + os.path.normpath(
                                "/demos/data/MDVRP/p01")

        objective_value = MDVRP.solve_demo(path_demo)
        self.assertAlmostEqual(
           576.86, objective_value, places=1)
        return None



def VRPSolverEasyTestAll():
    suite_all = unittest.TestSuite()
    suite_all.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestAllVariants))
    suite_all.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestAllClass))
    suite_all.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestAllDemos))
    result_test = unittest.TextTestRunner().run(suite_all)
    if not result_test.wasSuccessful():
        raise Exception("Tests failed")


if __name__ == '__main__':
    VRPSolverEasyTestAll()
