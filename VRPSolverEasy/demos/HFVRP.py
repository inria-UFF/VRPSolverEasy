""" This module allows to solve Queiroga instances of
Heterogeneous Fleet Vehicle Routing Problem """

from VRPSolverEasy.src import solver
import VRPSolverEasy.demos.cvrptw as utils


def solve_demo(instance_name):
    """return a solution from modelisation"""

    # read instance
    data = read_hfvrp_instances(instance_name)

    # get data
    vehicle_types = data["VehicleTypes"]
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
    model.solution.export(instance_name.split(".")[0] + "_result")

    return model.solution


def read_hfvrp_instances(instance_name):
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

    nb_vehicles = int(next(instance_iter))
    vehicle_types = []
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

    # compute the links of graph
    links = []
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

            nb_link += 1

    return {"Points": points,
            "VehicleTypes": vehicle_types,
            "Links": links
            }

if __name__ == "__main__":
    solve_demo("toy.txt") # optimal cost is 165.86
