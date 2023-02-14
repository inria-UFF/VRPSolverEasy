import math
import os
import VRPSolverEasy.src.solver as solver
import VRPSolverEasy.demos.cvrptw as utils




def solve_demo(instance_name):
    """return a solution from modelisation"""

    # read instance
    data = read_cvrp_instances(instance_name)

    # get data
    vehicle_type = data["VehicleTypes"]
    depot = data["Points"][0]
    customers = data["Points"][1:]
    links = data["Links"]

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
    # model.set_parameters(upper_bound=950)

    # if you have cplex 22.1 installed on your laptop you can
    # change the bapcod-shared library and specify the path like this:
    # Here there is an example on windows laptop
    # model.set_parameters(time_limit=30,cplex_path="C:\\Program Files\\
    # IBM\\ILOG\\CPLEX_Studio221\\cplex\\bin\\x64_win64")

    # solve model
    model.solve()

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.solution

def parse_instance_cvrp(instance_name):
    """Return a dictionary with differents elements of model"""
    
    instance_iter = iter(utils.read_instance("CVRP/" + instance_name))
    nb_points = 0
    instance = {"capacity":0,
                "dimension":0,
                "depot":{0:0},
                "node_coord":{},
                "demand":{}}

    while True:
        element = next(instance_iter)
        if element == "DIMENSION":
            next(instance_iter)  # pass ":"
            nb_points = int(next(instance_iter))
            nb_customers = nb_points - 1
            instance["dimension"] = nb_points
        elif element == "CAPACITY":
            next(instance_iter)  # pass ":"
            vehicle_capacity = int(next(instance_iter))
            instance["capacity"] = vehicle_capacity
        elif element == "EDGE_WEIGHT_TYPE":
            next(instance_iter)  # pass ":"
            element = next(instance_iter)
            if element != "EUC_2D":
                raise Exception("EDGE_WEIGHT_TYPE : " + element + """ 
                is not supported (only EUC_2D)""")
        elif element == "NODE_COORD_SECTION":
            break

    for n in range(nb_points):
        point_id = int(next(instance_iter))
        if point_id != n + 1:
            raise Exception("Unexpected index")
        else:
            instance["node_coord"][point_id] = [int(next(instance_iter)),
                                                int(next(instance_iter))]

    element = next(instance_iter)
    if element != "DEMAND_SECTION":
        raise Exception("Expected line DEMAND_SECTION")


    for n in range(nb_points):
        point_id = int(next(instance_iter))
        if point_id != n + 1:
            raise Exception("Unexpected index")
        instance["demand"][point_id] = int(next(instance_iter))

    element = next(instance_iter)
    if element != "DEPOT_SECTION":
        raise Exception("Expected line DEPOT_SECTION")

    depot_id = int(next(instance_iter))
    instance["depot"][0] = depot_id

    end_depot_section = int(next(instance_iter))
    if end_depot_section != -1:
        raise Exception("Expected only one depot.")

    return instance

def read_cvrp_instances(instance_name):
    """Read literature instances from CVRPLIB by giving the name of instance
        and returns dictionary containing all elements of model"""

    # Parse formatted instances (default)
    instance = parse_instance_cvrp(instance_name)

    capacity_input = int(instance['capacity'])
    dimension_input = int(instance['dimension'])

    depot_id = int(instance['depot'][0])
    depot_x = int(instance['node_coord'][depot_id][0])
    depot_y = int(instance['node_coord'][depot_id][1])
    depot_demand = int(instance['demand'][depot_id])
    id_point = 0

    # Initialize vehicle type
    vehicle_type = {"id": 1,  # we cannot have an id less than 1
                    "start_point_id": id_point,
                    "end_point_id": id_point,
                    "capacity": capacity_input,
                    "max_number": dimension_input,
                    "var_cost_dist": 1
                    }

    # Initialize the points with depot
    points = [{"x": depot_x,
               "y": depot_y,
               "demand": depot_demand,
               "id": id_point
               }]

    # Add the customers in the list of points
    while id_point < dimension_input-1:
        id_point += 1
        x = int(instance['node_coord'][id_point][0])
        y = int(instance['node_coord'][id_point][1])
        demand = int(instance['demand'][id_point])
        points.append({"x": x,
                       "y": y,
                       "demand": demand,
                       "id": id_point})

    # compute the links of graph
    links = []
    nb_link = 0
    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = utils.compute_euclidean_distance(points[i]["x"],
                                              points[i]["y"],
                                              points[j]["x"],
                                              points[j]["y"]
                                              )

            links.append({"name": "L" + str(nb_link),
                          "start_point_id": point["id"],
                          "end_point_id": points[j]["id"],
                          "distance": dist
                          })

            nb_link += 1

    return {"Points": points,
            "VehicleTypes": vehicle_type,
            "Links": links
            }


if __name__ == "__main__":
    solve_demo("A-n36-k5.vrp")
