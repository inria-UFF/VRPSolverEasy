""" This module allows to solve Augerat et al. instances of
Capacitated Vehicle Routing Problem """

import os
import sys
import getopt
import math
from VRPSolverEasy.src import solver
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import hygese as hgs
import numpy as np


def read_instance(name: str):
    """ Read an instance in the folder data from a given name """
    with open(name,
              "r", encoding="UTF-8")as file:
        elements = [str(element) for element in file.read().split()]
    file.close()
    return elements


def compute_euclidean_distance(x_i, y_i, x_j, y_j, number_digit=3):
    """Compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), number_digit)


def solve_demo(
        instance_name,
        solver_name="CLP",
        ext_heuristic=False,
        time_resolution=30,
        hgs=False):
    """return a solution from modelisation"""

    # read instance
    data = read_cvrp_instances(instance_name, ext_heuristic, hgs)

    # get data
    vehicle_type = data["VehicleTypes"]
    depot = data["Points"][0]
    customers = data["Points"][1:]
    links = data["Links"]
    upper_bound = data["UB"]

    # modelisation of problem
    model = solver.Model()

    # add vehicle type
    model.add_vehicle_type(id=vehicle_type["id"],
                           start_point_id=vehicle_type["start_point_id"],
                           end_point_id=vehicle_type["end_point_id"],
                           max_number=vehicle_type["max_number"],
                           capacity=vehicle_type["capacity"],
                           var_cost_dist=vehicle_type["var_cost_dist"]
                           )

    # add depot
    model.add_depot(id=depot["id"])

    # add all customers
    for customer in customers:
        model.add_customer(id=customer["id"],
                           demand=customer["demand"]
                           )
    # add all links
    for link in links:
        model.add_link(name=link["name"],
                       start_point_id=link["start_point_id"],
                       end_point_id=link["end_point_id"],
                       distance=link["distance"]
                       )

    # set parameters
    model.set_parameters(time_limit=time_resolution, heuristic_used=True)
    # print(upper_bound)
    # model.set_parameters(upper_bound=950)

    if ext_heuristic:
        model.parameters.upper_bound = upper_bound
    model.parameters.solver_name = solver_name
    model.parameters.print_level = 0

    # if you have cplex 22.1 installed on your laptop you can
    # change the bapcod-shared library and specify the path like this:
    # Here there is an example on windows laptop
    # model.set_parameters(time_limit=30,solver_name="CPLEX",cplex_path="C:\\Program Files\\
    # IBM\\ILOG\\CPLEX_Studio221\\cplex\\bin\\x64_win64")

    # solve model
    model.solve()

    path_instance_name = instance_name.split(".")[0]
    name_instance = path_instance_name.split("\\")[
        len(path_instance_name.split("\\")) - 1]
    print('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n'.format(
        "instance_name", "solver_name", "ext_heuristic",
        "solution_value",
        "solution_time",
        "best_lb",
        "root_lb",
        "root_time",
        "nb_branch_and_bound_nodes",
        "status"
    ), end='')
    print('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n'.format(
        name_instance, solver_name, ext_heuristic,
        model.solution.value,
        model.statistics.solution_time,
        model.statistics.best_lb,
        model.statistics.root_lb,
        model.statistics.root_time,
        model.statistics.nb_branch_and_bound_nodes,
        model.status
    ))
    """
    if(os.path.isfile("CVRP_Results.txt")):
        with open("CVRP_Results.txt", "a") as f:
            f.write('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n'.format(
            name_instance,solver_name,ext_heuristic,
            model.solution.value,
            model.statistics.solution_time,
            model.statistics.best_lb,
            model.statistics.root_lb,
            model.statistics.root_time,
            model.statistics.nb_branch_and_bound_nodes,
            model.status
            ))
    else:
        with open("CVRP_Results.txt", "a") as f:
           f.write('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n'.format(
            "instance_name","solver_name","ext_heuristic",
            "solution_value",
            "solution_time",
            "best_lb",
            "root_lb",
            "root_time",
            "nb_branch_and_bound_nodes",
            "status"
            ))
           f.write('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n'.format(
            name_instance,solver_name,ext_heuristic,
            model.solution.value,
            model.statistics.solution_time,
            model.statistics.best_lb,
            model.statistics.root_lb,
            model.statistics.root_time,
            model.statistics.nb_branch_and_bound_nodes,
            model.status
            ))
    """

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.solution


def read_cvrp_instances(instance_name, ext_heuristic=False, hgs=False):
    """Read literature instances from CVRPLIB by giving the name of instance
       and returns dictionary containing all elements of model"""

    instance_iter = iter(read_instance(instance_name))
    points = []
    id_point = 0
    dimension_input = -1
    capacity_input = -1
    # Instantiate the data problem.
    data = {}

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

    # Initialize vehicle type
    vehicle_type = {"id": 1,  # we cannot have an id less than 1
                    "start_point_id": id_point,
                    "end_point_id": id_point,
                    "capacity": capacity_input,
                    "max_number": dimension_input,
                    "var_cost_dist": 1
                    }

    vehicles = []
    index = 0
    for i in range(dimension_input):
        vehicles.append(capacity_input)

    data['vehicle_capacities'] = vehicles
    data['vehicle_capacity'] = capacity_input
    data['num_vehicles'] = dimension_input
    data['depot'] = 0

    # Create points
    for current_id in range(dimension_input):
        point_id = int(next(instance_iter))
        if point_id != current_id + 1:
            raise Exception("Unexpected index")
        x_coord = float(next(instance_iter))
        y_coord = float(next(instance_iter))
        points.append({"x": x_coord,
                       "y": y_coord,
                       "demand": -1,
                       "id": id_point})
        id_point += 1

    element = next(instance_iter)
    if element != "DEMAND_SECTION":
        raise Exception("Expected line DEMAND_SECTION")
    jobs = []
    # Get the demands
    for current_id in range(dimension_input):
        point_id = int(next(instance_iter))
        if point_id != current_id + 1:
            raise Exception("Unexpected index")
        demand = int(next(instance_iter))
        points[current_id]["demand"] = demand
        jobs.append(demand)

    data['demands'] = jobs

    element = next(instance_iter)
    if element != "DEPOT_SECTION":
        raise Exception("Expected line DEPOT_SECTION")
    next(instance_iter)  # pass id depot

    end_depot_section = int(next(instance_iter))
    if end_depot_section != -1:
        raise Exception("Expected only one depot.")

    # Compute the links of graph
    links = []
    matrix = [[0 for i in range((len(points)))] for i in range(len(points))]
    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = compute_euclidean_distance(point["x"],
                                              point["y"],
                                              points[j]["x"],
                                              points[j]["y"],
                                              0)
            links.append({"start_point_id": point["id"],
                          "end_point_id": points[j]["id"],
                          "distance": dist
                          })

            matrix[i][j] = dist
            matrix[j][i] = dist


    data['distance_matrix'] = matrix

    upper_bound = 0
    if ext_heuristic:
        if hgs:
            upper_bound = solve_ext_heuristic_hgs(data)
        else:  # OR Tools
            upper_bound = solve_ext_heuristic(data)

    return {"Points": points,
            "VehicleTypes": vehicle_type,
            "Links": links,
            "UB": upper_bound
            }


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))


def solve_ext_heuristic(data):
    """Solve the CVRP problem."""

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.

    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(len(data['demands']))

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        # print_solution(data, manager, routing, solution)
        return solution.ObjectiveValue() + 0.1

    return 100000


def solve_ext_heuristic_hgs(data):
    """Solve the CVRP problem."""

    # Solver initialization
    ap = hgs.AlgorithmParameters(timeLimit=len(data['demands']))  # seconds
    hgs_solver = hgs.Solver(parameters=ap, verbose=False)
    data['service_times'] = np.zeros(len(data['demands']))

    result = hgs_solver.solve_cvrp(data)
    print(result.cost)
    print(result.routes)

    return  result.cost + 0.1


def main(argv):
    instance = ''
    type_problem = ''
    solver_name = ''
    heuristic_used = False
    hgs = False
    time_resolution = 30
    opts, args = getopt.getopt(argv, "i:t:s:h:H:e:")

    for opt, arg in opts:
        if opt in ["-i"]:
            instance = arg
        elif opt == "-t":
            type_problem = arg
        elif opt == "-s":
            solver_name = arg
        elif opt == "-h":
            heuristic_used = arg == "yes"
        elif opt == "-H":
            hgs = arg == "yes"
        elif opt == "-e":
            time_resolution = float(arg)

    solve_demo(instance, solver_name, heuristic_used, time_resolution, hgs)


if __name__ == "__main__":
    #main(sys.argv[1:])
    # uncomment for use the file without command line
    path_project = os.path.join(os.path.dirname
                                        (os.path.realpath(__file__)))

    path_demo = path_project + os.path.normpath(
                            "/data/CVRP/A-n32-k5.vrp" )

    solve_demo(path_demo)
