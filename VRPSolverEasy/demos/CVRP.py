""" This module allows to solve CVRPLIB instances of
Capacitated Vehicle Routing Problem """

from VRPSolverEasy.src import solver
import os,sys,getopt
import math

class DataCVRP:
    """Contains all data for CVRP problem"""

    def __init__(
            self,
            vehicle_capacity: int,
            nb_customers: int,
            cust_demands=None,
            cust_coordinates=None,
            depot_coordinates=None):
        self.vehicle_capacity = vehicle_capacity
        self.nb_customers = nb_customers
        self.cust_demands = cust_demands
        self.cust_coordinates = cust_coordinates
        self.depot_coordinates = depot_coordinates

def compute_euclidean_distance(x_i, y_i, x_j, y_j):
    """Compute the rounded euclidean distance between 2 points"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2))

def read_cvrp_instances(instance_path):
    """Read literature instances from CVRPLIB by giving the name of instance
       and returns dictionary containing all elements of model"""

    try:
        with open (instance_path,
            "r",encoding="UTF-8" )as file:
            elements = [str(element) for element in file.read().split()]
    except FileNotFoundError:
        print(f"Error: The file '{instance_path}' was not found.")
        exit(0)

    instance_iter = iter(elements)

    id_point = 0
    dimension_input = -1
    capacity_input = -1

    while True:
        element = next(instance_iter)
        if element == "DIMENSION":
            next(instance_iter)  # pass ":"
            dimension_input = int(next(instance_iter))
        elif element == "CAPACITY":
            next(instance_iter)  # pass ":"
            capacity_input = int(next(instance_iter))
        elif element == "EDGE_WEIGHT_TYPE":
            next(instance_iter)  # pass ":"
            element = next(instance_iter)
            if element != "EUC_2D":
                raise Exception("EDGE_WEIGHT_TYPE : " + element + """
                is not supported (only EUC_2D)""")
        elif element == "NODE_COORD_SECTION":
            break

    vehicle_capacity = capacity_input

    # get demands and coordinates
    cust_coordinates = []
    depot_coordinates = []

    for current_id in range(dimension_input):
        point_id = int(next(instance_iter))
        if point_id != current_id + 1:
            raise Exception("Unexpected index")
        x_coord = float(next(instance_iter))
        y_coord = float(next(instance_iter))
        if id_point == 0:
            depot_coordinates = [x_coord, y_coord]
        else:
            cust_coordinates.append([x_coord, y_coord])
        id_point += 1

    element = next(instance_iter)
    if element != "DEMAND_SECTION":
        raise Exception("Expected line DEMAND_SECTION")

    # Get the demands
    cust_demands = []
    for current_id in range(dimension_input):
        point_id = int(next(instance_iter))
        if point_id != current_id + 1:
            raise Exception("Unexpected index")
        demand = int(next(instance_iter))
        if current_id > 0:
            cust_demands.append(demand)

    element = next(instance_iter)
    if element != "DEPOT_SECTION":
        raise Exception("Expected line DEPOT_SECTION")
    next(instance_iter)  # pass id depot

    end_depot_section = int(next(instance_iter))
    if end_depot_section != -1:
        raise Exception("Expected only one depot.")

    return DataCVRP(vehicle_capacity,
                    dimension_input - 1,
                    cust_demands,
                    cust_coordinates,
                    depot_coordinates)

def solve_cvrp(argv,
                instance_path='',
                time_limit=1e+10,
                upper_bound=1e+5,
                fixed_nb_veh=-1,
                solver_name="CLP",
                solver_path=""):
    """It solves the CVRP and returns a solution"""

    # read parameters given in command line
    opts, args = getopt.getopt(argv,"i:t:u:v:s:p:")
    for opt, arg in opts:
        if opt == "-i":
            instance_path = os.path.abspath(arg)
        elif opt == "-t":
            time_limit = float(arg)
        elif opt == "-u":
            upper_bound = float(arg)
        elif opt == "-v":
            fixed_nb_veh = int(arg)
        elif opt == "-s":
            solver_name = arg
        if opt in ["-p"]:
            solver_path = os.path.abspath(arg)

    # read instance
    data = read_cvrp_instances(instance_path)

    # VRPSolverEasy model
    model = solver.Model()

    nbVehicles = data.nb_customers
    if fixed_nb_veh != -1:
        nbVehicles = fixed_nb_veh
    # add vehicle type
    model.add_vehicle_type(id=1,
                        start_point_id=0,
                        end_point_id=0,
                        max_number=nbVehicles,
                        capacity=data.vehicle_capacity,
                        var_cost_dist=1)

    # add depot
    model.add_depot(id=0)

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i + 1, demand=data.cust_demands[i])

    # compute the links between depot and other points
    for i,cust_i in enumerate(data.cust_coordinates):
        dist = compute_euclidean_distance(cust_i[0],
                                          cust_i[1],
                                          data.depot_coordinates[0],
                                          data.depot_coordinates[1])

        model.add_link(start_point_id=0,
                       end_point_id=i + 1,
                       distance=dist)

    # compute the links between points
    for i,cust_i in enumerate(data.cust_coordinates):
        for j in range(i + 1, len(data.cust_coordinates)):
            dist = compute_euclidean_distance(cust_i[0],
                                              cust_i[1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1])
            model.add_link(start_point_id=i + 1,
                           end_point_id=j + 1,
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
        solve_cvrp(sys.argv[1:])
    else:
        print(
            """
            Usage:
                python CVRP.py -i <INSTANCE_PATH>
                            -t <TIME_LIMIT>            # In seconds
                            -u <UPPER_BOUND> 
                            [-v <NUM_VEHICLES>]        # Optional (for fixed fleet)
                            -s <SOLVER_NAME>      
                            [-p <PATH_SOLVER>]         # Optional, Windows only

            Parameters:
                -i   Path to the instance file
                -t   Execution time limit in seconds (default: 1e+10)
                -u   Upper bound (default: 1e+5)
                -v   Number of vehicles for fixed fleet (default: unlimited fleet size)
                -s   Name of the MIP/LP solver used by VRPSolver (CLP or CPLEX, default: CLP)
                -p   Path to the MIP/LP solver used by VRPSolver (optional, Windows only)
            """
        )