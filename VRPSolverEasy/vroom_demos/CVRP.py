""" This module allows to solve Augerat et al. instances of
Capacitated Vehicle Routing Problem """

from VRPSolverEasy.src import solver
import VRPSolverEasy.demos.CVRPTW as utils
import vroom
import pandas as pd



def solve_demo(instance_name,solver_name="CLP",ext_heuristic=False):
    """return a solution from modelisation"""

    # read instance
    data = read_cvrp_instances(instance_name, ext_heuristic)

    # get data
    vehicle_type = data["VehicleTypes"]
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
    model.set_parameters(time_limit=60)
    #print(upper_bound)
    # model.set_parameters(upper_bound=950)
    
    if ext_heuristic:
        model.parameters.upper_bound = upper_bound
    model.parameters.solver_name = solver_name

    # if you have cplex 22.1 installed on your laptop you can
    # change the bapcod-shared library and specify the path like this:
    # Here there is an example on windows laptop
    # model.set_parameters(time_limit=30,cplex_path="C:\\Program Files\\
    # IBM\\ILOG\\CPLEX_Studio221\\cplex\\bin\\x64_win64")

    # solve model
    model.solve()

    
    with open("CVRP_result.txt", "a") as f:
        f.write(str([instance_name,solver_name,ext_heuristic,model.solution.statistics.solution_value,
        model.solution.statistics.solution_time,
        model.solution.statistics.best_lb]))
                    

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.solution

def read_cvrp_instances(instance_name,ext_heuristic=False):
    """Read literature instances from CVRPLIB by giving the name of instance
       and returns dictionary containing all elements of model"""

    instance_iter = iter(utils.read_instance("CVRP/" + instance_name))
    points = []
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
    costs_dist = {}
    for i in range(dimension_input):
        vehicles.append(vroom.Vehicle(index,
                                      start=0,
                                      end=0,
                                      capacity=[capacity_input]))
        costs_dist[index] = [1,0] #var_cost_dist, fixed cost
        index += 1

    # Create points
    for current_id in range(dimension_input):
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
    for current_id in range(dimension_input):
        point_id = int(next(instance_iter))
        if point_id != current_id + 1:
            raise Exception("Unexpected index")
        demand = int(next(instance_iter))
        points[current_id]["demand"] = demand
        jobs.append(vroom.Job(current_id,
                    location=current_id,
                    delivery=[demand]))

    element = next(instance_iter)
    if element != "DEPOT_SECTION":
        raise Exception("Expected line DEPOT_SECTION")
    next(instance_iter) # pass id depot

    end_depot_section = int(next(instance_iter))
    if end_depot_section != -1:
        raise Exception("Expected only one depot.")

    # Compute the links of graph
    links = []
    nb_link = 0
    matrix = [[0 for i in range((len(points)))] for i in range(len(points))]
    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = utils.compute_euclidean_distance(point["x"],
                                                    point["y"],
                                                    points[j]["x"],
                                                    points[j]["y"],
                                                    0)
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
            "VehicleTypes": vehicle_type,
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
        return dist_cost + solution.summary.cost + 1
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
    solve_demo("A-n37-k6.vrp","CLP",ext_heuristic=True)
