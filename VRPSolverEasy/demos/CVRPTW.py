""" This module allows to solve Solomon instances of
Capacitated Vehicle Routing Problem with Time Windows. """


import os, math, sys, getopt
from VRPSolverEasy.src import solver


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


def compute_euclidean_distance(x_i, y_i, x_j, y_j,number_digit=3):
    """Compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), number_digit)


def solve_demo(instance_name,folder_data="/data/",
               time_resolution=30,
               solver_name_input="CLP",
               solver_path=""):
    """return a solution from modelisation"""

    #read parameters given in command line
    type_instance = "CVRPTW/"     
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
    data = read_cvrptw_instances(instance_name,folder_data,type_instance)

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
    model.set_parameters(time_limit=time_resolution,
                         solver_name=solver_name_input)
    

    ''' If you have cplex 22.1 installed on your laptop windows you have to specify
        solver path'''
    if (solver_name_input == "CPLEX" and solver_path != "" ):
        model.parameters.cplex_path=solver_path


    # solve model
    model.solve()

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.statistics.solution_value


def read_cvrptw_instances(instance_name, name_folder,type_instance):
    """Read literature instances of CVRPTW ("Solomon" format) by giving the name of instance
        and returns dictionary containing all elements of model"""
    instance_iter = iter(read_instance(type_instance + instance_name,name_folder))

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
                          "distance": dist,
                          "time": dist
                          })

            nb_link += 1

    return {"Points": points,
            "vehicle_type": vehicle_type,
            "Links": links
            }

if __name__ == "__main__":
    if(len(sys.argv)>1):
        solve_demo(sys.argv[1:])
    else:
        print("""Please indicates the path of your instance like this : \n 
       python -m VRPSolverEasy.demos.CVRPTW -i INSTANCE_PATH/NAME_INSTANCE \n
       -t TIME_RESOLUTION -s SOLVER_NAME (-p PATH_SOLVER (WINDOWS only))
       """)
       #uncomments for use the file without command line
       # solve_demo("R101.txt")
