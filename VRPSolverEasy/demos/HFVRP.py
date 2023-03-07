""" This module allows to solve Queiroga instances of
Heterogeneous Fleet Vehicle Routing Problem """

import os, math, sys , getopt
from VRPSolverEasy.src import solver

def compute_euclidean_distance(x_i, y_i, x_j, y_j,number_digit=3):
    """Compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), number_digit)

def read_instance(name : str,folder_data="/data/"):
    """ Read an instance in the folder data from a given name """
    path_project = os.path.join(os.path.dirname
                                            (os.path.realpath(__file__)))
    if(folder_data != "/data/"):
        path_project = ""

    with open (
        path_project +
        os.path.normpath(
            folder_data +
            name),
        "r",encoding="UTF-8") as file:
        return [str(element) for element in file.read().split()]

def solve_demo(instance_name,folder_data="/data/",
               time_resolution=30,
               solver_name_input="CLP",
               solver_path=""):
    """return a solution from modelisation"""

    #read parameters given in command line
    type_instance = "HFVRP/"     
    if len(sys.argv) > 1:
        print(instance_name)
        opts, args = getopt.getopt(instance_name,"i:t:s:p:")
        for opt, arg in opts:
            if opt in ["-i"]:
                instance_name = arg
                folder_data = ""
                type_instance = ""
            if opt in ["-t"]:
                time_resolution = float(arg)
            if opt in ["-s"]:
                solver_name_input = arg
            if opt in ["-p"]:
                solver_path = arg 
    
    # read instance
    data = read_hfvrp_instances(instance_name,folder_data,type_instance)

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
    model.set_parameters(time_limit=time_resolution,
                         solver_name=solver_name_input)
    

    ''' If you have cplex 22.1 installed on your laptop windows you have to specify
        solver path'''
    if (solver_name_input == "CPLEX" and solver_path != "" ):
        model.parameters.cplex_path=solver_path


    # solve model
    model.solve()

    # export the result
    model.solution.export(instance_name.split(".")[0] + "_result")

    
    return model.statistics.solution_value


def read_hfvrp_instances(instance_name, name_folder,type_instance):
    """Read literature instances of HFVRP by giving the name of instance
        and returns dictionary containing all elements of model"""
    instance_iter = iter(read_instance(type_instance + instance_name,name_folder))

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
            dist = compute_euclidean_distance(point["x"],
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
    if(len(sys.argv)>1):
        solve_demo(sys.argv[1:])
    else:
        print("""Please indicates the path of your instance like this : \n 
       python -m VRPSolverEasy.demos.HFVRP -i INSTANCE_PATH/NAME_INSTANCE \n
       -t TIME_RESOLUTION -s SOLVER_NAME (-p PATH_SOLVER (WINDOWS only))
       """)
       #uncomments for use the file without command line
       # solve_demo("c50_13fsmd.txt")
       
