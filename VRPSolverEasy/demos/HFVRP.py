import math
import os
import VRPSolverEasy.src.solver as solver


def read_instance(name):
    path_project = os.path.abspath(os.getcwd())
    file = open(
        path_project +
        os.path.normpath(
            "/VRPSolverEasy/src/data/" +
            name),
        "r")
    return [str(element) for element in file.read().split()]


def compute_euclidean_distance(x_i, y_i, x_j, y_j):
    """compute the euclidean distance between 2 points from graph"""
    return math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2)


def solve_demo(instance_name):
    """return a solution from modelisation"""

    # read instance
    data = read_hfvrp_instances(instance_name)

    # get data
    vehicle_types = data["vehicle_types"]
    depot = data["Points"][0]
    customers = data["Points"][1:]
    links = data["Links"]

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

    # if you have cplex 22.1 installed on your laptop you can
    # change the bapcod-shared library and specify the path like this:
    # Here there is an example on windows laptop
    # model.set_parameters(time_limit=30,solver_name="CPLEX",
    # cplex_path="C:\\Program Files\\
    # IBM\\ILOG\\CPLEX_Studio221\\cplex\\bin\\x64_win64\\cplex2210.dll")


    # solve model
    model.solve()

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.solution


def read_hfvrp_instances(instance_name):
    """Read literature instances of HFVRP by giving the name of instance
        and returns dictionary containing all elements of model"""
    instance_iter = iter(read_instance("HFVRP/" + instance_name))

    n = int(next(instance_iter))

    depot_id = int(next(instance_iter))
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

    for i in range(n):
        id_point += 1
        id = int(next(instance_iter))
        x = int(next(instance_iter))
        y = int(next(instance_iter))
        d = int(next(instance_iter))
        points.append({"x": x,
                "y": y,
                "demand": d,
                "id": id_point})

    K = int(next(instance_iter))
    vehicle_types = []
    for k in range(1, K+1):
        Q = int(next(instance_iter))
        fixed = float(next(instance_iter))
        factor = float(next(instance_iter))
        l = int(next(instance_iter))
        u = int(next(instance_iter))
        vehicle_type = {"id": k,  # we cannot have an id less than 1
                "start_point_id": 0,
                "end_point_id": 0,
                "capacity": Q,
                "max_number": u,
                "fixed_cost" : fixed,
                "var_cost_dist": factor
                }
        vehicle_types.append(vehicle_type)

    # compute the links of graph
    links = []
    nb_link = 0
    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = compute_euclidean_distance(points[i]["x"],
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
            "vehicle_types": vehicle_types,
            "Links": links
            }


if __name__ == "__main__":
    solve_demo("toy.txt") # optimal cost is 3185.09
