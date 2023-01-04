import unittest
import src.VRPSolverPy as solver

def VRPSolverPyTestAll():
    unittest.main()

class Test_all_variants(unittest.TestCase):
    def test_TSP(self):
        self.fail("Not implemented")
    def test_TSP_2(self):
        self.fail("Not implemented")
    def test_VRP(self):
        self.fail("Not implemented")
    def test_CVRP(self):
        self.fail("Not implemented")
    def test_CVRPTW(self):
        self.fail("Not implemented")
    def test_CVRPTW_TWVehicle(self):
        self.fail("Not implemented")
    def test_CVRPTW_TWVehicle(self):
        self.fail("Not implemented")
    def test_HFCVRPTW_1(self):
        self.fail("Not implemented")
    def test_HFCVRPTW_2(self):
        self.fail("Not implemented")
    def test_HFCLPRTW_3(self):
        self.fail("Not implemented")
class Test_all_class(unittest.TestCase):
    def test_VehicleType(self):
        m=solver.create_model()
        m.add_VehicleType()

    def test_Point(self):
        self.fail("Not implemented")
    def test_Link(self):
        self.fail("Not implemented")
    def test_Customer(self):
        self.fail("Not implemented")
    def test_Depot(self):
        self.fail("Not implemented")
    def test_Solution(self):
        self.fail("Not implemented")
class Test_all_status(unittest.TestCase):
    def test_optimal(self):
        self.fail("Not implemented")
    def test_feasible(self):
        self.fail("Not implemented")
    def test_infeasible(self):
        self.fail("Not implemented")
    def test_link_error(self):
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
