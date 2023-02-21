""" This module allows to solve Queiroga instances of
Heterogeneous Fleet Vehicle Routing Problem """

from VRPSolverEasy.src import solver
import VRPSolverEasy.demos.CVRPTW as utils
import pandas as pd
import vroom

def solve_demo(instance_name,solver_name="CLP",ext_heuristic=False):
    """return a solution from modelisation"""

    # read instance
    data = read_hfvrp_instances(instance_name,ext_heuristic)

    # get data
    vehicle_types = data["VehicleTypes"]
    depot = data["Points"][0]
    customers = data["Points"][1:]
    links = data["Links"]
    upper_bound = data["UB"]

    # modelisation of problem
    model = solver.CreateModel()

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
    model.set_parameters(time_limit=60)
    # model.set_parameters(upper_bound=3185.2)

    #print(upper_bound) debug mode

    if ext_heuristic:
        model.parameters.upper_bound = upper_bound
    
    model.parameters.solver_name = solver_name

    

    # if you have cplex 22.1 installed on your laptop you can ab i, and x
    # change the bapcod-shared library and specify the path like this:
    # Here there is an example on windows laptop
    # model.set_parameters(time_limit=30,solver_name="CPLEX",
    # cplex_path="C:\\Program Files\\
    # IBM\\ILOG\\CPLEX_Studio221\\cplex\\bin\\x64_win64\\cplex2210.dll")


    # solve model
    model.solve()

    with open("HFVRP_result.txt", "a") as f:
        f.write(str([instance_name,solver_name,ext_heuristic,model.statistics.solution_value,
        model.statistics.solution_time,
        model.statistics.best_lb]))

    # export the result
    model.solution.export()

    return model.solution


def read_hfvrp_instances(instance_name,ext_heuristic=False):
    """Read literature instances of HFVRP by giving the name of instance
        and returns dictionary containing all elements of model"""
    instance_iter = iter(utils.read_instance("HFVRP/" + instance_name))

    nb_points = int(next(instance_iter))

    next(instance_iter) # pass id depot (always 0)
    depot_x = int(next(instance_iter))
    depot_y = int(next(instance_iter))
    depot_demand = int(next(instance_iter))
    id_point = 0
    

    # Initialize the points with depot
    points = [{"x": depot_x,
               "y": depot_y,
               "demand": depot_demand,
               "id": id_point
               }]
    
    jobs = []
    for i in range(nb_points):
        id_point += 1
        next(instance_iter) # pass id point (take index)
        x_coord = int(next(instance_iter))
        y_coord = int(next(instance_iter))
        demand = int(next(instance_iter))
        points.append({"x": x_coord,
                "y": y_coord,
                "demand": demand,
                "id": id_point})

        jobs.append(vroom.Job(id_point,
                    location=id_point,
                    delivery=[demand]))       

    nb_vehicles = int(next(instance_iter))
    vehicle_types = []
    index = 0
    vehicles = []
    costs_dist = {}
    for k in range(1, nb_vehicles+1):
        capacity = int(next(instance_iter))
        fixed_cost = float(next(instance_iter))
        var_cost_dist = float(next(instance_iter))
        next(instance_iter) # pass min number
        max_number = int(next(instance_iter))
        vehicle_type = {"id": k,  # we cannot have an id less than 1
                "start_point_id": 0,
                "end_point_id": 0,
                "capacity": capacity,
                "max_number": max_number,
                "fixed_cost" : fixed_cost,
                "var_cost_dist": var_cost_dist
                }
        vehicle_types.append(vehicle_type)
        for i in range(max_number):
            vehicles.append(vroom.Vehicle(index,
                                      start=0,
                                      end=0,
                                      capacity=[capacity]))
            costs_dist[index] = [var_cost_dist,fixed_cost] #var_cost_dist, fixed cost
            index += 1
        
    # compute the links of graph
    links = []
    matrix = [[0 for i in range((len(points)))] for i in range(len(points))]
    nb_link = 0
    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = utils.compute_euclidean_distance(point["x"],
                                              point["y"],
                                              points[j]["x"],
                                              points[j]["y"]
                                              )

            links.append({"name": "L" + str(nb_link),
                          "start_point_id": point["id"],
                          "end_point_id": points[j]["id"],
                          "distance": dist
                          })

            matrix[i][j] = dist
            matrix[j][i] = dist

            nb_link += 1

    upper_bound = 0
    if ext_heuristic:
        upper_bound = solve_ext_heuristic(matrix,jobs,vehicles,costs_dist)

    return {"Points": points,
            "VehicleTypes": vehicle_types,
            "Links": links,
            "UB": upper_bound
            }
def compute_cost(solution,matrix,costs_dist,time=True):
    """compute total cost of routes """
    start_point = 0
    total_cost = 0
    dist_cost = 0
    vehicle_type_id = 0
    #ids contains [vehicle id,point id]
    print(solution.routes[["vehicle_id","id"]])
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
    if time == True:    
        return dist_cost + solution.summary.cost +1
    else:
        return dist_cost + 1

def solve_ext_heuristic(matrix,jobs,vehicles,costs_dist):

    problem_instance = vroom.Input()
    problem_instance.set_durations_matrix(
        profile="car",
        matrix_input=matrix
    )
    problem_instance.add_vehicle(vehicles)
    
    problem_instance.add_job(jobs)

    solution = problem_instance.solve(exploration_level=5, nb_threads=4)
    
    return compute_cost(solution,matrix,costs_dist,False)

if __name__ == "__main__":
    solve_demo("toy.txt","CLP",True) # optimal cost is 165.86
