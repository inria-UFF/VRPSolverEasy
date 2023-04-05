""" This module allows to solve Queiroga instances of
Heterogeneous Fleet Vehicle Routing Problem """

from VRPSolverEasy.src import solver
import VRPSolverEasy.demos.CVRPTW as utils
import os
import sys
import getopt
import math
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


def compute_euclidean_distance(x_i, y_i, x_j, y_j):
    """Compute the euclidean distance between 2 points from graph"""
    return math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2)


def compute_one_decimal_floor_euclidean_distance(x_i, y_i, x_j, y_j):
    """Compute the euclidean distance between 2 points from graph"""
    return math.floor(math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2) * 10) / 10


def solve_demo(instance_name, solver_name="CLP", ext_heuristic=False,
               time_resolution=30,
               time_resolution_heuristic=30):
    """return a solution from modelisation"""

    # read instance
    data = read_hfvrp_instances(
        instance_name,
        ext_heuristic,
        time_resolution_heuristic)

    # get data
    vehicle_types = data["VehicleTypes"]
    depot = data["Points"][0]
    customers = data["Points"][1:]
    links = data["Links"]
    upper_bound = data["UB"]

    # modelisation of problem
    model = solver.Model()

    for vehicle_type in vehicle_types:
        # add vehicle type
        model.add_vehicle_type(id=vehicle_type["id"],
                               start_point_id=vehicle_type["start_point_id"],
                               end_point_id=vehicle_type["end_point_id"],
                               capacity=vehicle_type["capacity"],
                               max_number=vehicle_type["max_number"],
                               fixed_cost=vehicle_type["fixed_cost"],
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
                       distance=link["distance"])

    # set parameters
    model.set_parameters(time_limit=time_resolution, heuristic_used=True)
    # model.set_parameters(upper_bound=3185.2)

    # print(upper_bound) debug mode

    if ext_heuristic:
        model.parameters.upper_bound = upper_bound
    model.parameters.print_level = 0

    model.parameters.solver_name = solver_name
    # if(solver_name == "CPLEX"):
    # model.parameters.heuristic_used = True   TODO
    # model.parameters.time_limit_heuristic = 5 TODO

    # if you have cplex 22.1 installed on your laptop you can ab i, and x
    # change the bapcod-shared library and specify the path like this:
    # Here there is an example on windows laptop
    # model.set_parameters(time_limit=30,solver_name="CPLEX",
    # cplex_path="C:\\Program Files\\
    # IBM\\ILOG\\CPLEX_Studio221\\cplex\\bin\\x64_win64\\cplex2210.dll")

    # solve model
    # model.export()
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
    if(os.path.isfile("HFVRP_Results.txt")):
        with open("HFVRP_Results.txt", "a") as f:
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
        with open("HFVRP_Results.txt", "a") as f:
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
    # model.solution.export()
    # print(model.parameters.upper_bound)
    return model.solution


def read_hfvrp_instances(
        instance_name,
        ext_heuristic=False,
        time_resolution_heuristic=30):
    """Read literature instances of HFVRP by giving the name of instance
        and returns dictionary containing all elements of model"""
    instance_iter = iter(read_instance(instance_name))
    vehicles_capacities, vehicles_fixed_costs, vehicles_var_costs = [], [], []
    data = {}
    points = []
    firstRead = next(instance_iter)
    index = 0

    if firstRead == 'NAME':  # read XH instances (large instances)
        nb_points, nb_vehicles, max_num_veh = [], [], []
        capacities, fixed_costs, var_costs = [], [], []
        while True:
            element = next(instance_iter)
            if element == "DIMENSION":
                next(instance_iter)  # pass ":"
                nb_points = int(next(instance_iter)) - 1
            elif element == "VEHICLE_KINDS":
                next(instance_iter)  # pass ":"
                nb_vehicles = int(next(instance_iter))
            elif element == "CAPACITIES":
                for k in range(nb_vehicles):
                    capacities.append(int(next(instance_iter)))
            elif element == "FIXED_COSTS":
                for k in range(nb_vehicles):
                    fixed_costs.append(int(next(instance_iter)))
            elif element == "VARIABLE_COSTS":
                for k in range(nb_vehicles):
                    var_costs.append(float(next(instance_iter)))
            elif element == "NUMBER_OF_VEHICLES":
                for k in range(nb_vehicles):
                    max_num_veh.append(int(next(instance_iter)))
            elif element == "EDGE_WEIGHT_TYPE":
                next(instance_iter)  # pass ":"
                element = next(instance_iter)
                if element != "EUC_2D":
                    raise Exception("EDGE_WEIGHT_TYPE : " + element + """
                    is not supported (only EUC_2D)""")
            elif element == "NODE_COORD_SECTION":
                break

        vehicle_types = []
        # Create vehicle types
        for k in range(nb_vehicles):
            vehicle_type = {"id": k + 1,  # we cannot have an id less than 1
                            "start_point_id": 0,
                            "end_point_id": 0,
                            "capacity": capacities[k],
                            "max_number": max_num_veh[k],
                            "fixed_cost": fixed_costs[k],
                            "var_cost_dist": var_costs[k]
                            }
            vehicle_types.append(vehicle_type)

        # create copies of vehicles of the same type to run OR-Tools heuristic
        for k in range(nb_vehicles):
            maxNbVeh = max_num_veh[k]
            vehicles_capacities.extend([capacities[k]
                                       for i in range(maxNbVeh)])
            vehicles_fixed_costs.extend(
                [fixed_costs[k] for i in range(maxNbVeh)])
            vehicles_var_costs.extend([var_costs[k] for i in range(maxNbVeh)])
            index += max_num_veh[k]

        id_point = 0
        # Create points
        for current_id in range(nb_points + 1):
            point_id = int(next(instance_iter))
            if point_id != current_id + 1:
                raise Exception("Unexpected index")
            x_coord = int(next(instance_iter))
            y_coord = int(next(instance_iter))
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
        for current_id in range(nb_points + 1):
            point_id = int(next(instance_iter))
            if point_id != current_id + 1:
                raise Exception("Unexpected index")
            points[current_id]["demand"] = int(next(instance_iter))
            jobs.append(points[current_id]["demand"])
        data["demands"] = jobs

        element = next(instance_iter)
        if element != "DEPOT_SECTION":
            raise Exception("Expected line DEPOT_SECTION")
        next(instance_iter)  # pass id depot

        end_depot_section = int(next(instance_iter))
        if end_depot_section != -1:
            raise Exception("Expected only one depot.")

    else:  # classic instances format

        nb_points = int(firstRead)
        next(instance_iter)  # pass id depot (always 0)
        depot_x = int(next(instance_iter))
        depot_y = int(next(instance_iter))
        depot_demand = int(next(instance_iter))
        id_point = 0

        # Initialize the points with depot
        points.append({"x": depot_x,
                       "y": depot_y,
                       "demand": depot_demand,
                       "id": id_point
                       })

        jobs = [0]
        for i in range(nb_points):
            id_point += 1
            next(instance_iter)  # pass id point (take index)
            x_coord = int(next(instance_iter))
            y_coord = int(next(instance_iter))
            demand = int(next(instance_iter))
            points.append({"x": x_coord,
                           "y": y_coord,
                           "demand": demand,
                           "id": id_point})
            jobs.append(demand)
        data["demands"] = jobs

        nb_vehicles = int(next(instance_iter))
        vehicle_types = []

        for k in range(1, nb_vehicles + 1):
            capacity = int(next(instance_iter))
            fixed_cost = float(next(instance_iter))
            var_cost_dist = float(next(instance_iter))
            next(instance_iter)  # pass min number
            max_number = int(next(instance_iter))
            vehicle_type = {"id": k,  # we cannot have an id less than 1
                            "start_point_id": 0,
                            "end_point_id": 0,
                            "capacity": capacity,
                            "max_number": max_number,
                            "fixed_cost": fixed_cost,
                            "var_cost_dist": var_cost_dist
                            }
            vehicle_types.append(vehicle_type)
            for i in range(max_number):
                vehicles_capacities.append(capacity)
                vehicles_var_costs.append(var_cost_dist)
                vehicles_fixed_costs.append(fixed_cost)
                index += 1

    data['vehicle_capacities'] = vehicles_capacities
    data['var_costs'] = vehicles_var_costs
    data['fixed_costs'] = vehicles_fixed_costs
    data['num_vehicles'] = index
    data['depot'] = 0

    # compute the links of graph
    links = []
    matrix = [[0 for i in range((len(points)))] for i in range(len(points))]
    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = compute_euclidean_distance(point["x"],
                                              point["y"],
                                              points[j]["x"],
                                              points[j]["y"])

            links.append({"start_point_id": point["id"],
                          "end_point_id": points[j]["id"],
                          "distance": dist
                          })

            matrix[i][j] = dist
            matrix[j][i] = dist


    data['distance_matrix'] = matrix

    upper_bound = 0
    if ext_heuristic:
        upper_bound = solve_ext_heuristic(data, time_resolution_heuristic)

    return {"Points": points,
            "VehicleTypes": vehicle_types,
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
    print('Total distance of all routes: {}m'.format(total_distance / 1000))
    print('Total load of all routes: {}'.format(total_load))


def solve_ext_heuristic(data, time_resolution_heuristic=30):

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index, id_vehicle):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return round(1000 *
                     (data['distance_matrix'][from_node][to_node] *
                      data['var_costs'][id_vehicle]))

    transit_callback_index = [routing.RegisterTransitCallback(
        partial(distance_callback, id_vehicle=i),
    ) for i in range(data['num_vehicles'])]

    for id in range(len(data['var_costs'])):
        routing.SetArcCostEvaluatorOfVehicle(
            transit_callback_index[id], int(id))

    # Define cost of each arc.
    # routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

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

    for i, cost in enumerate(data['fixed_costs']):
        routing.SetFixedCostOfVehicle(int(1000 * cost), i)

    # Setting first solution heuristic
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)

    search_parameters.time_limit.FromSeconds(len(data['demands']))

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        # print_solution(data,manager,routing,solution)
        return solution.ObjectiveValue() / 1000 + 0.1

    return 1000000


def main(argv):
    instance = ''
    type_problem = ''
    solver_name = ''
    heuristic_used = False
    time_resolution = 30
    time_resolution_heuristic = 30
    opts, args = getopt.getopt(argv, "i:t:s:h:e:f:")

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
        elif opt == "-f":
            time_resolution_heuristic = int(arg)

    solve_demo(
        instance,
        solver_name,
        heuristic_used,
        time_resolution,
        time_resolution_heuristic)


if __name__ == "__main__":
    main(sys.argv[1:])
