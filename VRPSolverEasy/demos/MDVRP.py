""" This module allows to solve Cordeau’s instances of
Multi Depot Vehicle Routing Problem """

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
    type_instance = "MDVRP/"     
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
    data = read_mdvrp_instances(instance_name,folder_data,type_instance)

    # get data
    vehicle_types = data["VehicleTypes"]
    nb_cust = data["NumberOfCustomers"]
    depots = data["Points"][nb_cust:]
    customers = data["Points"][:nb_cust]
    links = data["Links"]
    
    # modelisation of problem
    model = solver.Model()

    for vehicle_type in vehicle_types:
        # add vehicle type
        model.add_vehicle_type(id=vehicle_type["id"],
                            start_point_id=vehicle_type["start_point_id"],
                            end_point_id=vehicle_type["end_point_id"],
                            capacity=vehicle_type["capacity"],
                            max_number=vehicle_type["max_number"],
                            var_cost_dist=vehicle_type["var_cost_dist"]
                            )
    # add depots
    for depot in depots:
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

    print(model.solution)

    # export the result
    #model.solution.export(instance_name.split(".")[0] + "_result")

    
    return model.statistics.solution_value


def read_mdvrp_instances(instance_name, name_folder,type_instance):
    """Read literature instances of MDVRP by giving the name of instance
        and returns dictionary containing all elements of model"""
    instance_iter = iter(read_instance(type_instance + instance_name,name_folder))

    #pass type instance
    next(instance_iter)

    nb_vehicles = int(next(instance_iter))
    nb_customers = int(next(instance_iter))
    nb_depots = int(next(instance_iter))

    capacities = []
    for i in range(nb_depots):
        #pass max duration
        next(instance_iter)
        capacities.append(int(next(instance_iter))) 
    
    points = []
    for i in range(nb_customers):
        cust_id = int(next(instance_iter))
        cust_x = int(next(instance_iter))
        cust_y = int(next(instance_iter))
        #pass duration
        next(instance_iter)

        cust_demand = int(next(instance_iter))

        for i in range(6):
            next(instance_iter)

        # Initialize the points with customers
        points.append({"x": cust_x,
                       "y": cust_y,
                       "demand": cust_demand,
                       "id": cust_id
                      })

    #add depots and vehicle types
    vehicle_types = []
    for i in range(nb_depots):
        depot_id = int(next(instance_iter))
        cust_x = int(next(instance_iter))
        cust_y = int(next(instance_iter))

        points.append({"x": cust_x,
                       "y": cust_y,
                       "demand": 0,
                       "id": depot_id})

        vehicle_type = {"id": i+1,  # we cannot have an id less than 1
                        "start_point_id": depot_id,
                        "end_point_id": depot_id,
                        "capacity": capacities[i],
                        "max_number": nb_vehicles,
                        "var_cost_dist": 1
                        }
        vehicle_types.append(vehicle_type)
        for i in range(4):
            next(instance_iter)
    

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
            "Links": links,
            "NumberOfCustomers":nb_customers
            }


if __name__ == "__main__":
    if(len(sys.argv)>1):
        solve_demo(sys.argv[1:])
    else:
        print("""Please indicates the path of your instance like this : \n 
       python -m VRPSolverEasy.demos.MDVRP -i INSTANCE_PATH/NAME_INSTANCE \n
       -t TIME_RESOLUTION -s SOLVER_NAME (-p PATH_SOLVER (WINDOWS only))
       """)
       #uncomments for use the file without command line
        solve_demo("p02")
