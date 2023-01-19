from VRPSolverEasy.src import solver, constants
import random
import unittest


class test_all_variants(unittest.TestCase):

    def test_CVRP(self):
        """test model in there is only resource of capacity
        with optimal solution"""
        dist = 5
        cost_per_distance = 10
        nb_links = 5
        m = solver.create_model()
        m.add_VehicleType(
            1,
            0,
            0,
            "VEH1",
            capacity=100,
            maxNumber=3,
            varCostDist=cost_per_distance)
        m.add_Depot(id=0, name="D1")
        for i in range(1, 5):
            m.add_Customer(id=i, name="C" + str(i), demand=20)
        m.add_Link("arc1", startPointId=0, endPointId=1, distance=dist)
        m.add_Link("arc2", startPointId=1, endPointId=2, distance=dist)
        m.add_Link("arc3", startPointId=2, endPointId=3, distance=dist)
        m.add_Link("arc4", startPointId=3, endPointId=4, distance=dist)
        m.add_Link("arc5", startPointId=4, endPointId=0, distance=dist)

        # m.export("CVRP",true) DEBUG MODE

        m.solve()
        cost = dist * cost_per_distance * nb_links
        self.assertEqual(constants.OPTIMAL_SOL_FOUND, m.solution.status)
        self.assertAlmostEqual(
            cost, m.solution.statistics.solutionValue, places=5)

    def test_CVRP_noFeasible(self):
        """test model in there is only resource of capacity
        with no feasible solution"""
        m = solver.create_model()
        m.add_VehicleType(
            1,
            0,
            0,
            "VEH1",
            capacity=50,
            maxNumber=3,
            varCostDist=10)
        m.add_Depot(id=0, name="D1")
        for i in range(1, 5):
            m.add_Customer(id=i, name="C" + str(i), demand=20)
        m.add_Link("arc1", startPointId=0, endPointId=1, distance=5)
        m.add_Link("arc2", startPointId=1, endPointId=2, distance=6)
        m.add_Link("arc3", startPointId=2, endPointId=3, distance=4)
        m.add_Link("arc4", startPointId=3, endPointId=4, distance=4)
        m.add_Link("arc5", startPointId=4, endPointId=0, distance=4)
        m.solve()

        # m.export("CVRP_noFeasible",true) DEBUG MODE

        self.assertEqual(
            constants.BETTER_SOL_DOES_NOT_EXISTS,
            m.solution.status)

    def test_CVRPTW(self):
        """test model in there is two resources time and capacity"""
        cost_per_time = 10
        cost_per_distance = 10
        dist = 5
        nb_links = 5
        m = solver.create_model()
        m.add_VehicleType(
            1,
            0,
            0,
            "VEH1",
            capacity=200,
            maxNumber=3,
            varCostDist=cost_per_distance,
            varCostTime=cost_per_time,
            twEnd=200)
        m.add_Depot(id=0, name="D1", twBegin=0, twEnd=200)
        time_between_points = 4
        begin_time = 0
        for i in range(1, 5):
            m.add_Customer(
                id=i,
                name="C" + str(i),
                demand=20,
                twBegin=begin_time,
                twEnd=begin_time + 5)
            begin_time += 5
        m.add_Link(
            "arc1",
            startPointId=0,
            endPointId=1,
            distance=dist,
            time=time_between_points)
        m.add_Link(
            "arc2",
            startPointId=1,
            endPointId=2,
            distance=dist,
            time=time_between_points)
        m.add_Link(
            "arc3",
            startPointId=2,
            endPointId=3,
            distance=dist,
            time=time_between_points)
        m.add_Link(
            "arc4",
            startPointId=3,
            endPointId=4,
            distance=dist,
            time=time_between_points)
        m.add_Link(
            "arc5",
            startPointId=4,
            endPointId=0,
            distance=dist,
            time=time_between_points)
        m.solve()
        m.export("CVRPTW")
        cost = ((dist * cost_per_distance) +
                (time_between_points * cost_per_time)) * nb_links
        self.assertEqual(constants.OPTIMAL_SOL_FOUND, m.solution.status)
        self.assertAlmostEqual(
            cost, m.solution.statistics.solutionValue, places=5)
        print(m.solution)

    def test_CVRPTW_nofeasible_on_time(self):
        """test model it's infeasible on time"""
        m = solver.create_model()
        m.add_VehicleType(
            1,
            0,
            0,
            "VEH1",
            capacity=200,
            maxNumber=3,
            varCostDist=10,
            varCostTime=10)
        m.add_Depot(id=0, name="D1", twBegin=0, twEnd=10)
        time_between_points = 3
        begin_time = 0
        for i in range(1, 5):
            m.add_Customer(
                id=i,
                name="C" + str(i),
                demand=20,
                twBegin=begin_time,
                twEnd=begin_time + 5)
            begin_time += 5
        m.add_Link(
            "arc1",
            startPointId=0,
            endPointId=1,
            distance=5,
            time=time_between_points)
        m.add_Link(
            "arc2",
            startPointId=1,
            endPointId=2,
            distance=6,
            time=time_between_points)
        m.add_Link(
            "arc3",
            startPointId=2,
            endPointId=3,
            distance=4,
            time=time_between_points)
        m.add_Link(
            "arc4",
            startPointId=3,
            endPointId=4,
            distance=4,
            time=time_between_points)
        m.add_Link(
            "arc5",
            startPointId=4,
            endPointId=0,
            distance=4,
            time=time_between_points)
        m.solve()
        m.export("CVRPTW_noFeasible_on_time")
        print(m.solution)
        self.assertEqual(
            constants.BETTER_SOL_DOES_NOT_EXISTS,
            m.solution.status)

    def test_solve_without_all(self):
        """raise an error if we have any components in the model"""
        m = solver.create_model()
        with self.assertRaises(Exception):
            m.solve()

    def test_solve_without_points_links(self):
        """raise an error if we have only vehicle types in the model"""
        m = solver.create_model()
        with self.assertRaises(Exception):
            m.add_VehicleType(
                1,
                0,
                0,
                "VEH1",
                capacity=200,
                maxNumber=3,
                varCostDist=10,
                varCostTime=10)
            m.solve()

    def test_solve_without_links(self):
        """raise an error if we have any links"""
        m = solver.create_model()
        with self.assertRaises(Exception):
            m.add_VehicleType(
                1,
                0,
                0,
                "VEH1",
                capacity=200,
                maxNumber=3,
                varCostDist=10,
                varCostTime=10)
            m.add_Depot(id=0, name="D1", twBegin=0, twEnd=10)
            m.solve()

    def test_solve_without_points(self):
        """raise an error if we have any links"""
        m = solver.create_model()
        with self.assertRaises(Exception):
            m.add_VehicleType(
                1,
                0,
                0,
                "VEH1",
                capacity=200,
                maxNumber=3,
                varCostDist=10,
                varCostTime=10)
            m.add_Link(
                "arc1",
                startPointId=0,
                endPointId=1,
                distance=5,
                time=5)
            m.solve()
        print(m.solution)

    def test_solve_without_customers(self):
        """raise an error if we have a unknown points in links"""
        m = solver.create_model()
        m.add_VehicleType(
            1,
            0,
            0,
            "VEH1",
            capacity=200,
            maxNumber=3,
            varCostDist=10,
            varCostTime=10)
        m.add_Link("arc1", startPointId=0, endPointId=1, distance=5, time=5)
        m.add_Depot(id=0, name="D1", twBegin=0, twEnd=10)
        m.solve()
        print(m.solution)
        self.assertEqual(constants.LINKS_ERROR, m.solution.status)


class test_all_class(unittest.TestCase):

    def test_VehicleType_with_wrong_properties(self):
        """raise an error the properties of vehicle types are not respected"""
        m = solver.create_model()
        # check three non-optional parameters
        with self.assertRaises(Exception):
            m.add_VehicleType(1, 2)

        # check id point >1
        with self.assertRaises(solver.PropertyError):
            m.add_VehicleType(0, 2, 6)

        # check start point >0
        with self.assertRaises(solver.PropertyError):
            m.add_VehicleType(3, -2, 6)

        # check end point >0
        with self.assertRaises(solver.PropertyError):
            m.add_VehicleType(4, 2, -6)

        # check type name
        with self.assertRaises(solver.PropertyError):
            m.add_VehicleType(4, 2, 3, 5)

        # check maxNumber>0
        with self.assertRaises(solver.PropertyError):
            m.add_VehicleType(4, 2, 6, "veh1", -5, fixedCost=5, maxNumber=-8)

    def test_add_in_dict_Vehicletypes(self):
        """ we must have a new vehicle type in dict vehicleTypes after add"""
        m = solver.create_model()
        m.add_VehicleType(id=5, startPointId=3, endPointId=2)
        self.assertIn(5, m.vehicleTypes)

    def test_delete_in_dict_VehicleTypes(self):
        """ the old vehicle type must be removed from dict after delete"""
        m = solver.create_model()
        m.add_VehicleType(id=5, startPointId=3, endPointId=2)
        m.delete_VehicleType(5)
        self.assertNotIn(5, m.vehicleTypes)

    def test_add_VehicleTypes_without_function(self):
        """ we can set vehicle types by using directly the dictionary """
        m = solver.create_model()
        m.vehicleTypes[1] = solver.VehicleType(1, 2, 3)
        self.assertIn(1, m.vehicleTypes)

    def test_add_bad_VehicleTypes(self):
        """ raise an error if the setting of vehicleType is not correct"""
        m = solver.create_model()
        with self.assertRaises(solver.PropertyError):
            m.vehicleTypes[1] = 5

    def test_Point_with_wrong_properties(self):
        """raise an error the properties of point are not respected"""
        m = solver.create_model()

        # check id non optional parameter
        with self.assertRaises(Exception):
            m.add_Point()

        # check type name
        with self.assertRaises(solver.PropertyError):
            m.add_Point(1, name=5)

        # check idCustomer >0
        with self.assertRaises(solver.PropertyError):
            m.add_Point(5, idCustomer=-5)

        # check idCustomer <1022
        with self.assertRaises(solver.PropertyError):
            m.add_Point(5, idCustomer=1054)

        # check demandOrCapacity is integer
        with self.assertRaises(solver.PropertyError):
            m.add_Point(5, demandOrCapacity=3.5)

        # check demandOrCapacity>0
        with self.assertRaises(solver.PropertyError):
            m.add_Point(5, demandOrCapacity=-20)

    def test_add_in_dict_Point(self):
        """ we must have a new point in dict Points after add"""
        m = solver.create_model()
        m.add_Point(id=5)
        self.assertIn(5, m.points)

    def test_dict_Points_for_delete(self):
        """ the old point must be removed from dict after delete"""
        m = solver.create_model()
        m.add_VehicleType(id=5, startPointId=3, endPointId=2)
        m.delete_VehicleType(5)
        self.assertNotIn(5, m.vehicleTypes)

    def test_add_Points_without_function(self):
        """ we can set point by using directly the dictionary """
        m = solver.create_model()
        m.points[1] = solver.Point(1)
        self.assertIn(1, m.points)

    def test_add_bad_Point(self):
        """ raise an error if the setting of point is not correct"""
        m = solver.create_model()
        with self.assertRaises(solver.PropertyError):
            m.vehicleTypes[1] = {1: 5}

    def test_Link_with_wrong_properties(self):
        """ raise error if the user gives bad type of variables """
        m = solver.create_model()

        # check isDirected
        with self.assertRaises(Exception):
            m.add_Link(isDirected=9)

        # check type startPoint
        with self.assertRaises(solver.PropertyError):
            m.add_Link(startPointId="C1")

        # check type startPoint
        with self.assertRaises(solver.PropertyError):
            m.add_Link(endPointId="C2")

        # check distance must be >= 0
        with self.assertRaises(solver.PropertyError):
            m.add_Link(distance=-51)

        # check time must be >= 0
        with self.assertRaises(solver.PropertyError):
            m.add_Link(time=-52)

        # check fixed cost must be a number
        with self.assertRaises(solver.PropertyError):
            m.add_Link(fixedCost=[1, 2])

    def test_add_Customer(self):
        """ dict of points must be contain new customer """
        m = solver.create_model()
        m.add_Customer(5, "C1")
        self.assertIn(5, m.points)

    def test_idCustomer(self):
        """ if any idCustomer is given, idCustomer mus be equal to id """
        m = solver.create_model()
        m.add_Customer(5, "C1")
        self.assertEqual(5, m.points[5].idCustomer)

    def test_idCustomer_with_id_too_bigger(self):
        """ raise an error if idCustomer is not given by user and id >1022 """
        m = solver.create_model()
        with self.assertRaises(solver.PropertyError):
            m.add_Customer(1025, "C1")

    def test_idCustomer_with_id_different(self):
        """ assert idCustomer is different of id if it's
            given by the user """
        m = solver.create_model()
        m.add_Customer(1025, "C1", idCustomer=5)
        self.assertEqual(m.points[1025].idCustomer, 5)

    def test_add_Depot(self):
        """The idCustomer of depot must be equal to 0. """
        m = solver.create_model()
        m.add_Depot(5, "C1")
        m.add_Depot(9999999, "C1")
        self.assertEqual(0, m.points[5].idCustomer)
        self.assertEqual(0, m.points[9999999].idCustomer)

    def test_Solution(self):
        """ test class solution after resolving a CVRPTW problem """
        dist_max = 15
        time_max = 15
        cost_per_distance = 10
        cost_per_time = 10
        m = solver.create_model()
        m.add_VehicleType(
            1,
            0,
            0,
            "VEH1",
            capacity=100,
            maxNumber=3,
            varCostDist=cost_per_distance,
            varCostTime=cost_per_time,
            twBegin=0,
            twEnd=200)
        m.add_Depot(id=0, name="D1", twEnd=200)

        for i in range(1, 5):
            m.add_Customer(id=i, name="C" + str(i), demand=20, twEnd=200)

        # Here the arcs of solutions
        m.add_Link("arc1", startPointId=0, endPointId=1, distance=1, time=1)
        m.add_Link("arc2", startPointId=1, endPointId=2, distance=2, time=2)
        m.add_Link("arc3", startPointId=2, endPointId=3, distance=3, time=3)
        m.add_Link("arc4", startPointId=3, endPointId=4, distance=4, time=4)
        m.add_Link("arc5", startPointId=4, endPointId=0, distance=5, time=5)

        # Here the available arcs but more expensive
        for i in range(25):
            m.add_Link(name="arc_forbidden" + str(i),
                       startPointId=random.randint(0, 4),
                       endPointId=random.randint(0, 4),
                       distance=dist_max, time=time_max)

        # solve model
        m.solve()
        cost = sum(i * cost_per_distance for i in range(1, 6)) * 2

        # test status
        self.assertEqual(constants.OPTIMAL_SOL_FOUND, m.solution.status)

        # test solution value
        self.assertAlmostEqual(
            cost, m.solution.statistics.solutionValue, places=5)

        # test ids
        self.assertIn(m.solution.routes[0].pointIds, [[0, 1, 2, 3, 4, 0],
                                                      [0, 4, 3, 2, 1, 0]])

        # test arcs names
        self.assertIn(m.solution.routes[0].incomingArcNames,
                      [["", "arc1", "arc2", "arc3", "arc4", "arc5"],
                       ["", "arc5", "arc4", "arc3", "arc2", "arc1"]])

        # test arcs names
        self.assertEqual(m.solution.routes[0].capConsumption,
                         [0,
                          20,
                          40,
                          60,
                          80,
                          80])

        # test vehicle type id
        self.assertEqual(m.solution.routes[0].vehicleTypeId, 1)

        # test time consumption
        self.assertIn(m.solution.routes[0].timeConsumption,
                      [[0, 5, 9, 12, 14, 15],
                      [0, 1, 3, 6, 10, 15]])

    def test_Enumerate(self):
        """ test enumeration of all feasibles solutions """
        cost_per_time = 10
        cost_per_distance = 10
        dist = 5
        m = solver.create_model()
        m.add_VehicleType(
            1,
            0,
            0,
            "VEH1",
            capacity=200,
            maxNumber=3,
            varCostDist=cost_per_distance,
            varCostTime=cost_per_time,
            twEnd=200)
        m.add_Depot(id=0, name="D1", twBegin=0, twEnd=200)
        time_between_points = 4
        begin_time = 0
        for i in range(1, 5):
            m.add_Customer(
                id=i,
                name="C" + str(i),
                demand=20,
                twBegin=begin_time,
                twEnd=begin_time + 5)
            begin_time += 5
        m.add_Link(
            "arc1",
            startPointId=0,
            endPointId=1,
            distance=dist,
            time=time_between_points)
        m.add_Link(
            "arc2",
            startPointId=1,
            endPointId=2,
            distance=dist,
            time=time_between_points)
        m.add_Link(
            "arc3",
            startPointId=2,
            endPointId=3,
            distance=dist,
            time=time_between_points)
        m.add_Link(
            "arc4",
            startPointId=3,
            endPointId=4,
            distance=dist,
            time=time_between_points)
        m.add_Link(
            "arc5",
            startPointId=4,
            endPointId=0,
            distance=dist,
            time=time_between_points)
        m.set_Parameters(action="enumAllFeasibleRoutes")
        m.solve()
        m.export("enumerate-CVRPTW")
        print(m.solution)


class test_all_Demos(unittest.TestCase):
    def test_CVRP_solomon(self):
        # TODO Add here link with CVRP demo
        return None

    def test_HFVRP(self):
        # TODO Add here link with HFVRP demo
        return None

    def test_infeasible(self):
        # TODO Add here link with HFVRP demo
        return None


def VRPSolverEasyTestAll():
    suite_all = unittest.TestSuite()
    suite_all.addTests(
        unittest.TestLoader().loadTestsFromTestCase(test_all_variants))
    suite_all.addTests(
        unittest.TestLoader().loadTestsFromTestCase(test_all_class))
    suite_all.addTests(
        unittest.TestLoader().loadTestsFromTestCase(test_all_Demos))
    result_test = unittest.TextTestRunner().run(suite_all)
    if not result_test.wasSuccessful():
        raise Exception("Tests failed")


if __name__ == '__main__':
    VRPSolverEasyTestAll()
