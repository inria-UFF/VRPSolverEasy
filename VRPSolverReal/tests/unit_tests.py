from VRPSolverReal.src import solver, constants
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
        m.export("CVRP")
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
        m.export("CVRP_noFeasible")
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
        m = solver.create_model()
        with self.assertRaises(Exception):
            m.solve()

    def test_solve_without_points_links(self):
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

    def test_dict_VehicleTypes_for_add(self):
        m = solver.create_model()
        m.add_VehicleType(id=5, startPointId=3, endPointId=2)
        self.assertIn(5, m.vehicleTypes)

    def test_dict_VehicleTypes_for_delete(self):
        m = solver.create_model()
        m.add_VehicleType(id=5, startPointId=3, endPointId=2)
        m.delete_VehicleType(5)
        self.assertNotIn(5, m.vehicleTypes)

    def test_add_VehicleTypes_without_function(self):
        m = solver.create_model()
        m.vehicleTypes[1] = solver.VehicleType(1, 2, 3)
        self.assertIn(1, m.vehicleTypes)

    def test_add_bad_VehicleTypes(self):
        m = solver.create_model()
        with self.assertRaises(solver.PropertyError):
            m.vehicleTypes[1] = 5

    def test_Point(self):
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

        # TODO ASSERTION EQUAL
        # TODO ASSERTION EQUAL DEFAULT VALUES

    def test_Link(self):
        return None

    def test_Customer(self):
        return None

    def test_Depot(self):
        return None

    def test_Solution(self):
        return None


class test_all_status(unittest.TestCase):
    def test_optimal(self):
        return None

    def test_feasible(self):
        return None

    def test_infeasible(self):
        return None

    def test_link_error(self):
        return None


def VRPSolverRealTestAll():
    suite_all = unittest.TestSuite()
    suite_all.addTests(
        unittest.TestLoader().loadTestsFromTestCase(test_all_variants))
    suite_all.addTests(
        unittest.TestLoader().loadTestsFromTestCase(test_all_class))
    suite_all.addTests(
        unittest.TestLoader().loadTestsFromTestCase(test_all_status))
    result_test = unittest.TextTestRunner().run(suite_all)
    if not result_test.wasSuccessful():
        raise Exception("Tests failed")


if __name__ == '__main__':
    VRPSolverRealTestAll()
