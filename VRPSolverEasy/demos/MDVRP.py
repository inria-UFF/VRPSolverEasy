""" This module allows to solve Cordeau’s instances of
Multi Depot Vehicle Routing Problem """

from VRPSolverEasy.src import solver
import os,sys,getopt
import math

class DataMDVRP:
    """Contains all data for MDVRP problem
    """

    def __init__(
            self,
            nb_customers: int,
            nb_depots: int,
            vehicle_capacity: int,
            cust_demands=None,
            cust_coordinates=None,
            depot_coordinates=None):
        self.nb_customers = nb_customers
        self.nb_depots = nb_depots
        self.vehicle_capacity = vehicle_capacity
        self.cust_demands = cust_demands
        self.cust_coordinates = cust_coordinates
        self.depot_coordinates = depot_coordinates

def compute_euclidean_distance(x_i, y_i, x_j, y_j, number_digit=3):
    """Compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), number_digit)

def read_mdvrp_instances(instance_path):
    """Read literature instances of MDVRP by giving the name of instance
        and returns dictionary containing all elements of model"""
    
    try:
        with open (instance_path,
            "r",encoding="UTF-8" )as file:
            elements = [str(element) for element in file.read().split()]
    except FileNotFoundError:
        print(f"Error: The file '{instance_path}' was not found.")
        exit(0)

    instance_iter = iter(elements)

    # pass type instance
    next(instance_iter)

    next(instance_iter)

    nb_customers = int(next(instance_iter))
    nb_depots = int(next(instance_iter))

    vehicle_capacities = []
    for _ in range(nb_depots):
        # pass max duration
        next(instance_iter)
        vehicle_capacities.append(int(next(instance_iter)))

    cust_demands = []
    cust_coordinates = []
    for _ in range(nb_customers):
        next(instance_iter)
        cust_x = int(next(instance_iter))
        cust_y = int(next(instance_iter))
        cust_coordinates.append([cust_x, cust_y])
        # pass duration
        next(instance_iter)

        cust_demand = int(next(instance_iter))
        cust_demands.append(cust_demand)
        for _ in range(6):
            next(instance_iter)

    depot_coordinates = []
    # add depots and vehicle types
    for _ in range(nb_depots):
        next(instance_iter)
        cust_x = int(next(instance_iter))
        cust_y = int(next(instance_iter))
        depot_coordinates.append([cust_x, cust_y])

        for _ in range(4):
            next(instance_iter)

    return DataMDVRP(nb_customers,
                     nb_depots,
                     vehicle_capacities[0],
                     cust_demands,
                     cust_coordinates,
                     depot_coordinates
                     )

def solve_mdvrp(argv,
                instance_path='',
                time_limit=1e+10,
                upper_bound=1e+5,
                solver_name="CLP",
                solver_path=""):
    """It solves the MDVRP and returns a solution"""

    # read parameters given in command line
    opts, args = getopt.getopt(argv,"i:t:u:s:p:")
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
    data = read_mdvrp_instances(instance_path)

    # VRPSolverEasy model
    model = solver.Model()

    # add vehicle types
    for i in range(data.nb_depots):
        model.add_vehicle_type(id=data.nb_customers + i,
                               start_point_id=data.nb_customers + i,
                               end_point_id=data.nb_customers + i,
                               capacity=data.vehicle_capacity,
                               max_number=data.nb_customers,
                               var_cost_dist=1)

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i,
                           id_customer=i+1,
                           demand=data.cust_demands[i])

    # add depots
    for i in range(data.nb_customers,data.nb_customers + data.nb_depots):
        model.add_depot(id=i)

    nb_link = 0

    # Compute the links between depots and other points
    for index,coord_depot in enumerate(data.depot_coordinates):
        for i, cust_i in enumerate(data.cust_coordinates):
            dist = compute_euclidean_distance(
                cust_i[0],
                cust_i[1],
                coord_depot[0],
                coord_depot[1])
            model.add_link(start_point_id=index+data.nb_customers,
                           end_point_id=i,
                           distance=dist)

    # Compute the links between points
    for i,cust_i in enumerate(data.cust_coordinates):
        for j in range(i + 1, len(data.cust_coordinates)):
            dist = compute_euclidean_distance(cust_i[0],
                                              cust_i[1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1])
            model.add_link(start_point_id=i,
                           end_point_id=j,
                           distance=dist)

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
        solve_mdvrp(sys.argv[1:])
    else:
        print(
            """
            Usage:
                python MDVRP.py -i <INSTANCE_PATH>
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