""" This module allows to solve Solomon instances of
Capacitated Vehicle Routing Problem with Time Windows. """

import math
import os
import sys
import getopt
from VRPSolverEasy.src import solver
from functools import partial
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def read_instance(name: str):
    """ Read an instance in the folder data from a given name """
    path_project = os.path.abspath(os.getcwd())
    with open(name,
              "r", encoding="UTF-8")as file:
        elements = [str(element) for element in file.read().split()]
    file.close()
    return elements


def compute_euclidean_distance(x_i, y_i, x_j, y_j, number_digit=3):
    """Compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), number_digit)


def compute_one_decimal_floor_euclidean_distance(x_i, y_i, x_j, y_j):
    """Compute the euclidean distance between 2 points from graph"""
    return math.floor(math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2) * 10) / 10


def solve_demo(
        instance_name,
        solver_name="CLP",
        ext_heuristic=False,
        time_resolution=30):
    """Return a solution from modelisation"""

    # read instance
    data = read_cvrptw_instances(instance_name, ext_heuristic)

    # get data
    vehicle_type = data["vehicle_type"]
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
                           capacity=vehicle_type["capacity"],
                           max_number=vehicle_type["max_number"],
                           tw_begin=vehicle_type["tw_begin"],
                           tw_end=vehicle_type["tw_end"],
                           var_cost_dist=vehicle_type["var_cost_dist"],
                           var_cost_time=vehicle_type["var_cost_time"]
                           )
    # add depot
    model.add_depot(id=depot["id"],
                    service_time=depot["service_time"],
                    tw_begin=depot["tw_begin"],
                    tw_end=depot["tw_end"]
                    )

    # add all customers
    for customer in customers:
        model.add_customer(id=customer["id"],
                           service_time=customer["service_time"],
                           tw_begin=customer["tw_begin"],
                           tw_end=customer["tw_end"],
                           demand=customer["demand"]
                           )
    # add all links
    for link in links:
        model.add_link(name=link["name"],
                       start_point_id=link["start_point_id"],
                       end_point_id=link["end_point_id"],
                       distance=link["distance"],
                       time=link["time"]
                       )

    # set parameters
    model.set_parameters(time_limit=time_resolution, heuristic_used=True)

    if ext_heuristic:
        model.parameters.upper_bound = upper_bound

    model.parameters.solver_name = solver_name
    model.parameters.print_level = 0

    # if you have cplex 22.1 installed on your laptop you can
    # change the bapcod-shared library and specify the path like this:
    # Here there is an example on windows laptop
    # model.set_parameters(time_limit=30,solver_name="CPLEX",
    # cplex_path="C:\\Program Files\\
    # IBM\\ILOG\\CPLEX_Studio221\\cplex\\bin\\x64_win64\\cplex2210.dll")

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
    if(os.path.isfile("CVRPTW_Results.txt")):
        with open("CVRPTW_Results.txt", "a") as f:
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
            f.close()
    else:
        with open("CVRPTW_Results.txt", "a") as f:
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
           f.close()
    """

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.solution


def read_cvrptw_instances(instance_name, ext_heuristic=False):
    """Read literature instances of CVRPTW ("Solomon" format) by giving the name of instance,
        compute lower bound and returns dictionary containing all elements of model"""
    instance_iter = iter(read_instance(instance_name))
    # Instantiate the data problem.
    data = {}

    for i in range(4):
        next(instance_iter)

    max_number_input = int(next(instance_iter))
    capacity_input = int(next(instance_iter))

    for i in range(13):
        next(instance_iter)

    depot_x = float(next(instance_iter))
    depot_y = float(next(instance_iter))
    depot_demand = int(next(instance_iter))
    depot_tw_begin = int(next(instance_iter))
    depot_tw_end = int(next(instance_iter))
    depot_service_time = int(next(instance_iter))
    id_point = 0

    vehicles = []
    # Initialize vehicle type
    vehicle_type = {"id": 1,  # we cannot have an id less than 1
                    "start_point_id": id_point,
                    "end_point_id": id_point,
                    "capacity": capacity_input,
                    "max_number": max_number_input,
                    "tw_begin": depot_tw_begin,
                    "tw_end": depot_tw_end,
                    "service_time": depot_service_time,
                    "var_cost_dist": 1,
                    "var_cost_time": 0
                    }
    index = 0
    time_windows = [(depot_tw_begin, depot_tw_end)]
    service_times = [0]
    for i in range(max_number_input):
        vehicles.append(capacity_input)
        index += 1

    data['vehicle_capacities'] = vehicles
    data['num_vehicles'] = max_number_input
    data['depot'] = 0

    demands = []

    # Initialize the points with depot
    points = [{"x": depot_x,
               "y": depot_y,
               "demand": depot_demand,
               "tw_begin": depot_tw_begin,
               "tw_end": depot_tw_end,
               "service_time": depot_service_time,
               "id": id_point
               }]
    demands.append(depot_demand)
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
        points.append({"x": x_coord,
                       "y": y_coord,
                       "demand": demand,
                       "tw_begin": tw_begin,
                       "tw_end": tw_end + service_time,
                       "service_time": service_time,
                       "id": id_point})
        demands.append(demand)
        time_windows.append((tw_begin, tw_end))
        service_times.append(service_time)

    data['demands'] = demands
    data['time_windows'] = time_windows
    # compute the links of graph
    links = []
    matrix = [[0 for i in range((len(points)))] for i in range(len(points))]
    matrix_time = [[0 for i in range((len(points)))]
                   for i in range(len(points))]

    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = compute_one_decimal_floor_euclidean_distance(
                point["x"], point["y"], points[j]["x"], points[j]["y"])

            links.append({"start_point_id": point["id"],
                          "end_point_id": points[j]["id"],
                          "distance": dist,
                          "time": dist
                          })
            matrix_time[i][j] = dist + service_times[i]
            matrix_time[j][i] = dist + service_times[j]
            matrix[i][j] = dist
            matrix[j][i] = dist

    data['distance_matrix'] = matrix
    data['time_matrix'] = matrix_time
    upper_bound = 0

    if ext_heuristic:
        upper_bound = solve_ext_heuristic(data)

    return {"Points": points,
            "vehicle_type": vehicle_type,
            "Links": links,
            "UB": upper_bound
            }


def compute_cost_solution(data, manager, routing, solution):
    """Prints solution on console."""

    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    total_cost = 0
    arc = (0, 0)
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        index_route = 0
        arc = (0, 0)
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            id = manager.IndexToNode(index)
            index = solution.Value(routing.NextVar(index))
            if (index_route > 0):
                arc = (arc[1], id)
                total_cost += data["distance_matrix"][arc[0]][arc[1]]
            index_route += 1

        total_cost += data["distance_matrix"][arc[1]][0]
        time_var = time_dimension.CumulVar(index)
        begin = solution.Min(time_var)
        end = solution.Max(time_var)
        plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                    solution.Min(time_var),
                                                    solution.Max(time_var))
        plan_output += 'Time of the route: {}min\n'.format(
            solution.Min(time_var))
        print(plan_output)
        total_time += solution.Min(time_var)
    print('Total time of all routes: {}min'.format(total_time))
    return total_cost * 2 + 1


def solve_ext_heuristic(data):
    """Solve the CVRP problem."""

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback for distance.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node] * 10

    transit_callback_index_distance = routing.RegisterTransitCallback(
        distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index_distance)

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

    # Create and register a transit callback for time.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node] * 10

    transit_callback_index_time = routing.RegisterTransitCallback(
        time_callback)

    # Add Time Windows constraint.
    time = 'Time'
    horizon = data['time_windows'][data['depot']][1] * 10
    routing.AddDimension(
        transit_callback_index_time,
        horizon,  # allow waiting time
        horizon,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        begin = time_window[0] * 10
        end = time_window[1] * 10
        time_dimension.CumulVar(index).SetRange(begin, end)

    # Add time window constraints for each vehicle start node.
    depot_idx = data['depot']
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data['time_windows'][depot_idx][0] * 10,
            data['time_windows'][depot_idx][1] * 10)

    # Instantiate route start and end times to produce feasible times.
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(len(data['demands']))

    # Solve the problem.ema
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return solution.ObjectiveValue() / 10 + 0.1

    return 100000


def main(argv):
    instance = ''
    type_problem = ''
    solver_name = ''
    heuristic_used = False
    time_resolution = 30
    opts, args = getopt.getopt(argv, "i:t:s:h:e:")

    for opt, arg in opts:
        if opt in ["-i"]:
            instance = arg
        elif opt == "-t":
            type_problem = arg
        elif opt == "-s":
            solver_name = arg
        elif opt == "-h":
            heuristic_used = arg == "yes"
        elif opt == "-e":
            time_resolution = float(arg)

    solve_demo(instance, solver_name, heuristic_used, time_resolution)


if __name__ == "__main__":
    main(sys.argv[1:])
