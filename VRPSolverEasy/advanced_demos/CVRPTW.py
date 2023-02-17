""" This module allows to solve Solomon instances of
Capacitated Vehicle Routing Problem with Time Windows. """

import math
import os
import vroom
import pandas as pd
from VRPSolverEasy.src import solver


def read_instance(name : str):
    """ Read an instance in the folder data from a given name """
    path_project = os.path.abspath(os.getcwd())
    with open (
        path_project +
        os.path.normpath(
            "/VRPSolverEasy/demos/data/" +
            name),
        "r",encoding="UTF-8") as file:
        return [str(element) for element in file.read().split()]


def compute_euclidean_distance(x_i, y_i, x_j, y_j,number_digit=3):
    """Compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), number_digit)


def solve_demo(instance_name,solver_name="CLP",ext_heuristic=False):
    """Return a solution from modelisation"""

    # read instance
    data = read_cvrptw_instances(instance_name,ext_heuristic)

    # get data
    vehicle_type = data["vehicle_type"]
    depot = data["Points"][0]
    customers = data["Points"][1:]
    links = data["Links"]
    upper_bound = data["UB"]

    
    # modelisation of problem
    model = solver.CreateModel()

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
    model.set_parameters(time_limit=30)

    if ext_heuristic:
        model.parameters.upper_bound = upper_bound
    
    model.parameters.solver_name = solver_name

    # if you have cplex 22.1 installed on your laptop you can
    # change the bapcod-shared library and specify the path like this:
    # Here there is an example on windows laptop
    # model.set_parameters(time_limit=30,solver_name="CPLEX",
    # cplex_path="C:\\Program Files\\
    # IBM\\ILOG\\CPLEX_Studio221\\cplex\\bin\\x64_win64\\cplex2210.dll")


    # solve model
    model.solve()

    with open("CVRPTW_result.txt", "a") as f:
        f.write(str([instance_name,solver_name,ext_heuristic,model.solution.statistics.solution_value,
        model.solution.statistics.solution_time,
        model.solution.statistics.best_lb]))
        f.write("\n")

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.solution


def read_cvrptw_instances(instance_name,ext_heuristic=False):
    """Read literature instances of CVRPTW ("Solomon" format) by giving the name of instance,
        compute lower bound and returns dictionary containing all elements of model"""
    instance_iter = iter(read_instance("CVRPTW/" + instance_name))

    for i in range(4):
        next(instance_iter)

    max_number_input = int(next(instance_iter))
    capacity_input = int(next(instance_iter))

    for i in range(13):
        next(instance_iter)

    depot_x = int(next(instance_iter))
    depot_y = int(next(instance_iter))
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
                    "var_cost_time": 1
                    }
    index = 0
    costs_dist = {}
    for i in range(max_number_input):
        vehicles.append(vroom.Vehicle(index,
                                      start=0,
                                      end=0,
                                      capacity=[capacity_input],
                                      time_window=[depot_tw_begin,
                                      depot_tw_end]))
        costs_dist[index] = [1,0] #var_cost_dist, fixed cost
        index += 1

    jobs = []
    # Initialize the points with depot
    points = [{"x": depot_x,
               "y": depot_y,
               "demand": depot_demand,
               "tw_begin": depot_tw_begin,
               "tw_end": depot_tw_end,
               "service_time": depot_service_time,
               "id": id_point
               }]
    # Add the customers in the list of points
    
    while True:
        id_point += 1
        value = next(instance_iter, None)
        if value is None:
            break
        x_coord = int(next(instance_iter))
        y_coord = int(next(instance_iter))
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
        jobs.append(vroom.Job(id_point,
                              location=id_point,
                              delivery=[demand],
                              time_windows=[[tw_begin,tw_end]],
                              service=service_time))

    # compute the links of graph
    links = []
    matrix = [[0 for i in range((len(points)))] for i in range(len(points))]
    nb_link = 0
    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = compute_euclidean_distance(point["x"],
                                              point["y"],
                                              points[j]["x"],
                                              points[j]["y"]
                                              )

            links.append({"name": "L" + str(nb_link),
                          "start_point_id": point["id"],
                          "end_point_id": points[j]["id"],
                          "distance": dist,
                          "time": dist
                          })

            matrix[i][j] = dist
            matrix[j][i] = dist

            nb_link += 1
            
    upper_bound = 0
    if ext_heuristic:
        upper_bound = solve_ext_heuristic(matrix,jobs,vehicles,costs_dist)

    return {"Points": points,
            "vehicle_type": vehicle_type,
            "Links": links,
            "UB": upper_bound
            }
def compute_cost(solution,matrix,costs_dist):
    #total time * var_cost_time + total_distance * var_cost_dist + fixed cost vehicle
    start_point = 0
    total_cost = 0
    dist_cost = 0
    vehicle_type_id = 0
    #ids contains [vehicle id,point id]
    for index,ids in enumerate(solution.routes[["vehicle_id","id"]].values):
        
        if (index ==0):
            vehicle_type_id = ids[0]
        else:
            if(ids[0] != vehicle_type_id):
                dist_cost += costs_dist[ids[0]][1]
                vehicle_type_id = ids[0]
        
        if(pd.isna(ids[1])):
            dist_cost += matrix[start_point][0] * costs_dist[ids[0]][0]
        else:
            dist_cost += matrix[start_point][ids[1]  #var_cost
                        ] * costs_dist[ids[0]][0]
            start_point = ids[1]

    dist_cost += costs_dist[ids[0]][1] #fixed_cost
        
    return dist_cost + solution.summary.cost

def solve_ext_heuristic(matrix,jobs,vehicles,costs_dist):

    problem_instance = vroom.Input()
    problem_instance.set_durations_matrix(
        profile="car",
        matrix_input=matrix
    )
    problem_instance.add_vehicle(vehicles)
    
    problem_instance.add_job(jobs)

    solution = problem_instance.solve(exploration_level=5, nb_threads=4)
    
    return compute_cost(solution,matrix,costs_dist)
    

if __name__ == "__main__":
    solve_demo("R101.txt","CLP",True)
    
