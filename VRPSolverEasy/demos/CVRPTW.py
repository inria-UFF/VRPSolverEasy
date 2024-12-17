""" This module allows to solve Solomon instances of
Capacitated Vehicle Routing Problem with Time Windows. """

from VRPSolverEasy.src import solver
import os,sys,getopt
import math

class DataCVRPTW:
    """Contains all data for CVRPTW problem
    """

    def __init__(
            self,
            vehicle_capacity: int,
            nb_customers: int,
            max_number: int,
            cust_demands=None,
            cust_coordinates=None,
            depot_coordinates=0,
            cust_tw_begin=None,
            cust_tw_end=None,
            cust_service_time=None,
            depot_tw_begin=0,
            depot_tw_end=0,
            depot_service_time=0):

        self.vehicle_capacity = vehicle_capacity
        self.nb_customers = nb_customers
        self.max_number = max_number
        self.cust_demands = cust_demands
        self.cust_coordinates = cust_coordinates
        self.depot_coordinates = depot_coordinates
        self.cust_tw_begin = cust_tw_begin
        self.cust_tw_end = cust_tw_end
        self.cust_service_time = cust_service_time
        self.depot_tw_begin = depot_tw_begin
        self.depot_tw_end = depot_tw_end
        self.depot_service_time = depot_service_time

def compute_euclidean_distance(x_i, y_i, x_j, y_j):
    """Compute the euclidean distance between 2 points from graph"""
    return math.floor(math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2) * 10) / 10

def read_cvrptw_instances(instance_path):
    """Read literature instances of CVRPTW ("Solomon" format) by giving the name of instance
        and returns dictionary containing all elements of model"""

    try:
        with open (instance_path,
            "r",encoding="UTF-8" )as file:
            instance_iter = iter([str(element) for element in file.read().split()])
    except FileNotFoundError:
        print(f"Error: The file '{instance_path}' was not found.")
        exit(0)

    for i in range(4):
        next(instance_iter)

    max_number_input = int(next(instance_iter))
    capacity_input = int(next(instance_iter))

    for i in range(13):
        next(instance_iter)

    depot_x = int(next(instance_iter))
    depot_y = int(next(instance_iter))
    next(instance_iter) #depot demand
    depot_tw_begin = int(next(instance_iter))
    depot_tw_end = int(next(instance_iter))
    depot_service_time = int(next(instance_iter))
    id_point = 0

    vehicle_capacity = capacity_input
    vehicle_max_number = max_number_input

    depot_coordinates = [depot_x, depot_y]

    cust_coordinates = []
    cust_demands = []
    cust_tw_begin = []
    cust_tw_end = []
    cust_service_time = []

    # Add the customers in the list of points
    while True:
        id_point += 1
        value = next(instance_iter, None)
        if value is None:
            break
        x_coord = float(next(instance_iter))
        y_coord = float(next(instance_iter))
        demand = int(next(instance_iter))
        tw_begin = int(next(instance_iter))
        tw_end = int(next(instance_iter))
        service_time = int(next(instance_iter))

        cust_coordinates.append([x_coord, y_coord])
        cust_tw_begin.append(tw_begin)
        cust_tw_end.append(tw_end + service_time)
        cust_service_time.append(service_time)
        cust_demands.append(demand)

    return DataCVRPTW(vehicle_capacity,
                      id_point - 1,
                      vehicle_max_number,
                      cust_demands,
                      cust_coordinates,
                      depot_coordinates,
                      cust_tw_begin,
                      cust_tw_end,
                      cust_service_time,
                      depot_tw_begin,
                      depot_tw_end,
                      depot_service_time)

def solve_cvrptw(argv,
                instance_path='',
                time_limit=1e+10,
                upper_bound=1e+5,
                solver_name="CLP",
                solver_path=""):
    """It solves the CVRPTW and returns a solution"""

    # read parameters given in command line
    opts, args = getopt.getopt(argv,"i:t:u:v:s:p:")
    for opt, arg in opts:
        if opt == "-i":
            instance_path = os.path.abspath(arg)
        elif opt == "-t":
            time_limit = float(arg)
        elif opt == "-u":
            upper_bound = float(arg)
        elif opt == "-s":
            solver_name = arg
        if opt in ["-p"]:
            solver_path = os.path.abspath(arg)

    # read instance
    data = read_cvrptw_instances(instance_path)

    # VRPSolverEasy model
    model = solver.Model()

    # add vehicle type
    model.add_vehicle_type(id=1,
                           start_point_id=0,
                           end_point_id=0,
                           max_number=data.max_number,
                           capacity=data.vehicle_capacity,
                           tw_begin=data.depot_tw_begin,
                           tw_end=data.depot_tw_end,
                           var_cost_dist=1)

    # add depot
    model.add_depot(id=0,
                    service_time=data.depot_service_time,
                    tw_begin=data.depot_tw_begin,
                    tw_end=data.depot_tw_end)

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i + 1,
                           service_time=data.cust_service_time[i],
                           tw_begin=data.cust_tw_begin[i],
                           tw_end=data.cust_tw_end[i],
                           demand=data.cust_demands[i])

    # compute the links between depot and other points
    for i,cust_i in enumerate(data.cust_coordinates):
        dist = compute_euclidean_distance(cust_i[0],
                                          cust_i[1],
                                          data.depot_coordinates[0],
                                          data.depot_coordinates[1])
        model.add_link(start_point_id=0,
                       end_point_id=i + 1,
                       distance=dist,
                       time=dist)

    # compute the links between points
    for i,cust_i in enumerate(data.cust_coordinates):
        for j in range(i + 1, len(data.cust_coordinates)):
            dist = compute_euclidean_distance(cust_i[0],
                                              cust_i[1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1])
            model.add_link(start_point_id=i + 1,
                           end_point_id=j + 1,
                           distance=dist,
                           time=dist)

    # set parameters
    if solver_name == "CPLEX":
        # Set heuristic_used=False to disable CPLEX built-in heuristic
        model.set_parameters(time_limit=time_limit, solver_name=solver_name, 
                            upper_bound=upper_bound, heuristic_used=True)
    else: # CLP solver
        model.set_parameters(time_limit=time_limit, 
                            upper_bound=upper_bound, solver_name=solver_name)

    ''' If you have cplex 22.1 installed on your laptop windows you have to specify
        solver path'''
    if (solver_name == "CPLEX" and solver_path != ""):
        model.parameters.cplex_path = solver_path

    # Uncomment the next line to write a JSON file for the model
    # model.export(instance_path)

    # solve model
    model.solve()

    if model.solution.is_defined :
        print(f"""
        VRPSolver statistics:
        {'-'*30}
        Solution value        : {model.solution.value}
        Best lower bound      : {model.statistics.best_lb}
        Total time            : {model.statistics.solution_time} seconds
        Number of B&B nodes   : {model.statistics.nb_branch_and_bound_nodes}
        Root lower bound      : {model.statistics.root_lb}
        Root time             : {model.statistics.root_time} seconds
        {'-'*30}
        """)
        print(f"Status : {model.status}\n")
        print(f"Message : {model.message}\n")   
        for route in model.solution.routes:            
            print(f"Vehicle Type id : {route.vehicle_type_id}.")
            print(f"Ids : {route.point_ids}.")
            print(f"Load : {route.cap_consumption}.\n")

    # Uncomment the next line to export the result
    # model.solution.export(instance_path.split(".")[0] + "_result")

    return model.solution

if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_cvrptw(sys.argv[1:])
    else:
        print(
            """
            Usage:
                python CVRPTW.py -i <INSTANCE_PATH>
                            -t <TIME_LIMIT>            # In seconds
                            -u <UPPER_BOUND> 
                            -s <SOLVER_NAME>      
                            [-p <PATH_SOLVER>]         # Optional, Windows only

            Parameters:
                -i   Path to the instance file
                -t   Execution time limit in seconds (default: 1e+10)
                -u   Upper bound (default: 1e+5)
                -s   Name of the MIP/LP solver used by VRPSolver (CLP or CPLEX, default: CLP)
                -p   Path to the MIP/LP solver used by VRPSolver (optional, Windows only)
            """
        )