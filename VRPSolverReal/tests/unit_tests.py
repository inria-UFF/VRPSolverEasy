from VRPSolverReal.src import solver
import unittest



class test_all_variants(unittest.TestCase):


    def test_CVRP(self):
        m=solver.create_model()
        m.add_VehicleType(1,0,0,"VEH1",capacity=100,maxNumber=3,varCostDist=10)
        m.add_Depot(id=0,name="D1")
        for i in range(1,5):
            m.add_Customer(id=i,name="C"+str(i),demand=20)
        m.add_Link("arc1",startPointId=0,endPointId=1,distance=5)
        m.add_Link("arc2",startPointId=1,endPointId=2,distance=6)
        m.add_Link("arc3",startPointId=2,endPointId=3,distance=4)
        m.add_Link("arc4",startPointId=3,endPointId=4,distance=4)
        m.add_Link("arc5",startPointId=4,endPointId=0,distance=4)
        #m.export("CVRP")
        m.solve()
        print(m.solution)
        return None
        #TODO ASSERTIONS

    def test_CVRP_noFeasible(self):
        m=solver.create_model()
        m.add_VehicleType(1,0,0,"VEH1",capacity=50,maxNumber=3,varCostDist=10)
        m.add_Depot(id=0,name="D1")
        for i in range(1,5):
            m.add_Customer(id=i,name="C"+str(i),demand=20)
        m.add_Link("arc1",startPointId=0,endPointId=1,distance=5)
        m.add_Link("arc2",startPointId=1,endPointId=2,distance=6)
        m.add_Link("arc3",startPointId=2,endPointId=3,distance=4)
        m.add_Link("arc4",startPointId=3,endPointId=4,distance=4)
        m.add_Link("arc5",startPointId=4,endPointId=0,distance=4)
        m.solve()
        #m.export()
        print(m.solution)
        return None
        #TODO ASSERTIONS

    def test_CVRPTW(self):
        m=solver.create_model()
        m.add_VehicleType(1,0,0,"VEH1",capacity=200,maxNumber=3,varCostDist=10,varCostTime=10)
        m.add_Depot(id=0,name="D1",TWbegin=0,TWend=200)
        time_between_points=4
        begin_time=0
        for i in range(1,5):
            m.add_Customer(id=i,name="C"+str(i),demand=20,TWbegin=begin_time,TWend=begin_time+5)
            begin_time+=5
        m.add_Link("arc1",startPointId=0,endPointId=1,distance=5,time=time_between_points)
        m.add_Link("arc2",startPointId=1,endPointId=2,distance=6,time=time_between_points)
        m.add_Link("arc3",startPointId=2,endPointId=3,distance=4,time=time_between_points)
        m.add_Link("arc4",startPointId=3,endPointId=4,distance=4,time=time_between_points)
        m.add_Link("arc5",startPointId=4,endPointId=0,distance=4,time=time_between_points)
        m.solve()
        #m.export("CVRPTW")
        print(m.solution)
        return None

    def test_CVRPTW_nofeasible_on_time(self):
        m=solver.create_model()
        m.add_VehicleType(1,0,0,"VEH1",capacity=200,maxNumber=3,varCostDist=10,varCostTime=10)
        m.add_Depot(id=0,name="D1")
        time_between_points=6
        begin_time=0
        for i in range(1,5):
            m.add_Customer(id=i,name="C"+str(i),demand=20,TWbegin=begin_time,TWend=begin_time+5)
            begin_time+=5
        m.add_Link("arc1",startPointId=0,endPointId=1,distance=5,time=time_between_points)
        m.add_Link("arc2",startPointId=1,endPointId=2,distance=6,time=time_between_points)
        m.add_Link("arc3",startPointId=2,endPointId=3,distance=4,time=time_between_points)
        m.add_Link("arc4",startPointId=3,endPointId=4,distance=4,time=time_between_points)
        m.add_Link("arc5",startPointId=4,endPointId=0,distance=4,time=time_between_points)
        m.solve()
        #m.export("CVRPTW_noFeasible")
        print(m.solution)
        return None
        #TODO ASSERTIONS

class test_all_class(unittest.TestCase):
    
    def test_add_VehicleType_with_wrong_properties(self):
        m=solver.create_model()
        #check three non-optional parameters 
        with self.assertRaises(Exception):
            m.add_VehicleType(1,2)

        #check id point >1
        with self.assertRaises(solver.PropertyError):
            m.add_VehicleType(0,2,6) 
        
        #check start point >0
        with self.assertRaises(solver.PropertyError):
            m.add_VehicleType(3,-2,6)

        #check end point >0
        with self.assertRaises(solver.PropertyError):
            m.add_VehicleType(4,2,-6)

        #check type name
        with self.assertRaises(solver.PropertyError):
            m.add_VehicleType(4,2,3,5)

        #check maxNumber>0
        with self.assertRaises(solver.PropertyError):
            m.add_VehicleType(4,2,6,"veh1",-5,fixedCost=5,maxNumber=-8)



        #TODO ASSERTION EQUAL
        #TODO ASSERTION EQUAL DEFAULT VALUES

    def test_Point(self):
        m=solver.create_model()
        
        #check id non optional parameter
        with self.assertRaises(Exception):
            m.add_Point()

        #check type name
        with self.assertRaises(solver.PropertyError):
            m.add_Point(1,name=5)
        
        #check idCustomer >0
        with self.assertRaises(solver.PropertyError):
             m.add_Point(5,idCustomer=-5)
        

        #check idCustomer <1022
        with self.assertRaises(solver.PropertyError):
            m.add_Point(5,idCustomer=1054)

        #check demandOrCapacity is integer
        with self.assertRaises(solver.PropertyError):
            m.add_Point(5,demandOrCapacity=3.5)

        #check demandOrCapacity>0
        with self.assertRaises(solver.PropertyError):
            m.add_Point(5,demandOrCapacity=-20)

        #TODO ASSERTION EQUAL
        #TODO ASSERTION EQUAL DEFAULT VALUES

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
    suite_all.addTests(unittest.TestLoader().loadTestsFromTestCase(test_all_variants))
    suite_all.addTests(unittest.TestLoader().loadTestsFromTestCase(test_all_class))
    suite_all.addTests(unittest.TestLoader().loadTestsFromTestCase(test_all_status))
    unittest.TextTestRunner().run(suite_all)

if __name__ == '__main__':
    VRPSolverRealTestAll()
