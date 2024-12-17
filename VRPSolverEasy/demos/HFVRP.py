""" This module allows to solve Heterogeneous Fleet Vehicle Routing Problem """

from VRPSolverEasy.src import solver
import os,sys,getopt
import math

class DataHFVRP:
    """Contains all data for HFVRP problem
    """

    def __init__(
            self,
            nb_customers: int,
            nb_vehicle_types: int,
            vehicle_capacities=None,
            vehicle_fixed_costs=None,
            vehicle_var_costs=None,
            vehicle_max_numbers=None,
            cust_demands=None,
            cust_coordinates=None,
            depot_coordinates=None):
        self.vehicle_capacities = vehicle_capacities
        self.vehicle_fixed_costs = vehicle_fixed_costs
        self.vehicle_var_costs = vehicle_var_costs
        self.vehicle_max_numbers = vehicle_max_numbers
        self.nb_customers = nb_customers
        self.nb_vehicle_types = nb_vehicle_types
        self.cust_demands = cust_demands
        self.cust_coordinates = cust_coordinates
        self.depot_coordinates = depot_coordinates

def compute_euclidean_distance(x_i, y_i, x_j, y_j):
    """Compute the euclidean distance between 2 points from graph"""
    return math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2)

def read_hfvrp_classic_instances(instance_path):
    """Read literature instances of HFVRP by giving the name of instance
        and returns dictionary containing all elements of model"""
    try:
        with open (instance_path,
            "r",encoding="UTF-8" )as file:
            elements = [str(element) for element in file.read().split()]
    except FileNotFoundError:
        print(f"Error: The file '{instance_path}' was not found.")
        exit(0)

    instance_iter = iter(elements)

    nb_points = int(next(instance_iter))

    next(instance_iter)  # pass id depot (always 0)
    depot_x = int(next(instance_iter))
    depot_y = int(next(instance_iter))
    next(instance_iter) #depot demand
    id_point = 0

    # get demands and coordinates
    cust_coordinates = []
    cust_demands = []
    depot_coordinates = [depot_x, depot_y]

    for _ in range(nb_points):
        id_point += 1
        next(instance_iter)  # pass id point (take index)
        x_coord = float(next(instance_iter))
        y_coord = float(next(instance_iter))
        demand = int(next(instance_iter))
        cust_coordinates.append([x_coord, y_coord])
        cust_demands.append(demand)

    nb_vehicles = int(next(instance_iter))

    vehicle_capacities = []
    vehicle_fixed_costs = []
    vehicle_var_costs = []
    vehicle_max_numbers = []

    for _ in range(1, nb_vehicles + 1):
        capacity = int(next(instance_iter))
        fixed_cost = float(next(instance_iter))
        var_cost_dist = float(next(instance_iter))
        next(instance_iter)  # pass min number
        max_number = int(next(instance_iter))

        vehicle_capacities.append(capacity)
        vehicle_fixed_costs.append(fixed_cost)
        vehicle_var_costs.append(var_cost_dist)
        vehicle_max_numbers.append(max_number)

    return DataHFVRP(nb_points,
                     nb_vehicles,
                     vehicle_capacities,
                     vehicle_fixed_costs,
                     vehicle_var_costs,
                     vehicle_max_numbers,
                     cust_demands,
                     cust_coordinates,
                     depot_coordinates)

def read_hfvrp_XH_instances(instance_path):
    """Read new format instances of HFVRP by giving the path of the instance
       and returns a DataHFVRP object containing all elements of the model."""
    
    with open(instance_path, 'r') as f:
        lines = f.readlines()

    vehicle_capacities = []
    vehicle_fixed_costs = []
    vehicle_var_costs = []
    vehicle_max_numbers = []
    cust_coordinates = []
    cust_demands = []
    depot_coordinates = None

    reading_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("NAME") or line.startswith("COMMENT") or line.startswith("TYPE") or line.startswith("EDGE_WEIGHT_TYPE"):
            continue
        elif line.startswith("DIMENSION"):
            nb_points = int(line.split(":")[1].strip()) - 1 
        elif line.startswith("VEHICLE_KINDS"):
            nb_vehicle_types = int(line.split(":")[1].strip())
        elif line.startswith("CAPACITIES"):
            reading_section = "CAPACITIES"
            continue
        elif line.startswith("FIXED_COSTS"):
            reading_section = "FIXED_COSTS"
            continue
        elif line.startswith("VARIABLE_COSTS"):
            reading_section = "VARIABLE_COSTS"
            continue
        elif line.startswith("NUMBER_OF_VEHICLES"):
            reading_section = "NUMBER_OF_VEHICLES"
            continue
        elif line.startswith("NODE_COORD_SECTION"):
            reading_section = "NODE_COORD_SECTION"
            continue
        elif line.startswith("DEMAND_SECTION"):
            reading_section = "DEMAND_SECTION"
            continue
        elif line.startswith("DEPOT_SECTION"):
            reading_section = "DEPOT_SECTION"
            continue
        elif line.startswith("EOF"):
            break

        if reading_section == "CAPACITIES":
            vehicle_capacities = list(map(int, line.split()))
        elif reading_section == "FIXED_COSTS":
            vehicle_fixed_costs = list(map(float, line.split()))
        elif reading_section == "VARIABLE_COSTS":
            vehicle_var_costs = list(map(float, line.split()))
        elif reading_section == "NUMBER_OF_VEHICLES":
            vehicle_max_numbers = list(map(int, line.split()))
        elif reading_section == "NODE_COORD_SECTION":
            parts = line.split()
            node_id = int(parts[0]) - 1  # Adjusting index to start from 0
            x_coord = float(parts[1])
            y_coord = float(parts[2])
            if node_id == 0:
                depot_coordinates = [x_coord, y_coord]
            else:
                cust_coordinates.append([x_coord, y_coord])
        elif reading_section == "DEMAND_SECTION":
            parts = line.split()
            node_id = int(parts[0]) - 1  # Adjusting index to start from 0
            demand = int(parts[1])
            if node_id != 0:
                cust_demands.append(demand)
        elif reading_section == "DEPOT_SECTION":
            depot_id = int(line) - 1  # Adjusting index to start from 0
            if depot_id == -2:  # Depot end signal
                break

    return DataHFVRP(nb_points,
                     nb_vehicle_types,
                     vehicle_capacities,
                     vehicle_fixed_costs,
                     vehicle_var_costs,
                     vehicle_max_numbers,
                     cust_demands,
                     cust_coordinates,
                     depot_coordinates)

def solve_hfvrp(argv,
                instance_path='',
                time_limit=1e+10,
                upper_bound=1e+5,
                instance_format=0,
                solver_name="CLP",
                solver_path=""):
    """It solves the HFVRP and returns a solution"""

    # read parameters given in command line
    opts, args = getopt.getopt(argv,"i:t:u:f:s:p:")
    for opt, arg in opts:
        if opt == "-i":
            instance_path = os.path.abspath(arg)
        elif opt == "-t":
            time_limit = float(arg)
        elif opt == "-u":
            upper_bound = float(arg)
        elif opt == "-f":
            instance_format = int(arg)
        elif opt == "-s":
            solver_name = arg
        if opt in ["-p"]:
            solver_path = os.path.abspath(arg)

    # read instance
    if instance_format == 0:
        data = read_hfvrp_classic_instances(instance_path)
    elif instance_format == 1:
        data = read_hfvrp_XH_instances(instance_path)
    else:
        print("Instance format is not valid!")
        exit(0)

    # VRPSolverEasy model
    model = solver.Model()

    # add vehicles
    for i in range(data.nb_vehicle_types):
        # add vehicle type
        model.add_vehicle_type(id=i + 1,
                               start_point_id=0,
                               end_point_id=0,
                               capacity=data.vehicle_capacities[i],
                               max_number=data.vehicle_max_numbers[i],
                               fixed_cost=data.vehicle_fixed_costs[i],
                               var_cost_dist=data.vehicle_var_costs[i])

    # add depot
    model.add_depot(id=0)

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i + 1,
                           demand=data.cust_demands[i])

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
        solve_hfvrp(sys.argv[1:])
    else:
        print(
            """
            Usage:
                python HFVRP.py -i <INSTANCE_PATH>
                            -t <TIME_LIMIT>            # In seconds
                            -u <UPPER_BOUND> 
                            -f <INSTANCE_FORMAT>]        
                            -s <SOLVER_NAME>      
                            [-p <PATH_SOLVER>]         # Optional, Windows only

            Parameters:
                -i   Path to the instance file
                -t   Execution time limit in seconds (default: 1e+10)
                -u   Upper bound (default: 1e+5)
                -f   Instance format (0 for classic and 1 for XH, default: 0)
                -s   Name of the MIP/LP solver used by VRPSolver (CLP or CPLEX, default: CLP)
                -p   Path to the MIP/LP solver used by VRPSolver (optional, Windows only)
            """
        )