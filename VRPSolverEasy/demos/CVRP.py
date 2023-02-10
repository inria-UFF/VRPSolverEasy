import math
import os
import VRPSolverEasy.src.solver as solver
import vrplib

def compute_euclidean_distance(x_i, y_i, x_j, y_j):
    """compute the euclidean distance between 2 points from graph"""
    return math.floor(math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2) + 0.5)


def solve_demo(instance_name):
    """return a solution from modelisation"""

    # read instance
    data = read_cvrp_instances(instance_name)

    # get data
    vehicle_type = data["vehicle_type"]
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
    model.set_parameters(time_limit=30)

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


def read_cvrp_instances(instance_name):
    """Read literature instances from CVRPLIB by giving the name of instance
        and returns dictionary containing all elements of model"""

    # Read VRPLIB formatted instances (default)
    instance = vrplib.read_instance("VRPSolverEasy/src/data/CVRP/" + instance_name)

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
            dist = compute_euclidean_distance(points[i]["x"],
                                              points[j]["x"],
                                              points[i]["y"],
                                              points[j]["y"]
                                              )

            links.append({"name": "L" + str(nb_link),
                          "start_point_id": point["id"],
                          "end_point_id": points[j]["id"],
                          "distance": dist
                          })

            nb_link += 1

    return {"Points": points,
            "vehicle_type": vehicle_type,
            "Links": links
            }


if __name__ == "__main__":
    solve_demo("A-n37-k6.vrp")
