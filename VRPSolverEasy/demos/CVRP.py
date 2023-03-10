""" This module allows to solve CVRPLIB instances of
Capacitated Vehicle Routing Problem """

import os, math, sys, getopt
from VRPSolverEasy.src import solver

class DataCvrp:
    """Contains all data for CVRP problem
    """
    def __init__(
            self,
            vehicle_capacity: int,
            nb_customers: int,
            cust_demands=None,
            cust_coordinates=None,
            depot_coordinates=None):
        self.vehicle_capacity = vehicle_capacity
        self.nb_customers = nb_customers
        self.cust_demands = cust_demands
        self.cust_coordinates = cust_coordinates
        self.depot_coordinates = depot_coordinates
        

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
    type_instance = "CVRP/"     
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
    data = read_cvrp_instances(instance_name,folder_data,type_instance)



    # modelisation of problem
    model = solver.Model()

    # add vehicle type
    model.add_vehicle_type(id=1,
                           start_point_id=0,
                           end_point_id=0,
                           max_number=data.nb_customers,
                           capacity=data.vehicle_capacity,
                           var_cost_dist=1
                           )
    # add depot
    model.add_depot(id=0)

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i+1, 
                           demand=data.cust_demands[i]
                           )

    links = []
    nb_link = 0

    # Compute the links between depot and other points
    for i in range(len(data.cust_coordinates)):
        dist = compute_euclidean_distance(data.cust_coordinates[i][0],
                                          data.cust_coordinates[i][1],
                                          data.depot_coordinates[0],
                                          data.depot_coordinates[1],
                                          0)

        links.append({"name": "L" + str(nb_link),
                        "start_point_id": 0,
                        "end_point_id": i+1,
                        "distance": dist
                        })
        nb_link += 1

    # Compute the links between points
    for i in range(len(data.cust_coordinates)):
        for j in range(i + 1,len(data.cust_coordinates)):
            dist = compute_euclidean_distance(data.cust_coordinates[i][0],
                                              data.cust_coordinates[i][1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1],
                                              0)

            links.append({"name": "L" + str(nb_link),
                          "start_point_id": i+1,
                          "end_point_id": j+1,
                          "distance": dist
                          })

            nb_link += 1

    # add all links in the model
    for link in links:
        model.add_link(name=link["name"],
                       start_point_id=link["start_point_id"],
                       end_point_id=link["end_point_id"],
                       distance=link["distance"]
                       )

    # set parameters
    model.set_parameters(time_limit=time_resolution,
                         solver_name=solver_name_input)
    

    ''' If you have cplex 22.1 installed on your laptop windows you have to specify
        solver path'''
    if (solver_name_input == "CPLEX" and solver_path != "" ):
        model.parameters.cplex_path=solver_path
  
    model.export()

    # solve model
    model.solve()

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.statistics.solution_value

def read_cvrp_instances(instance_name, name_folder,type_instance):
    """Read literature instances from CVRPLIB by giving the name of instance
       and returns dictionary containing all elements of model"""

    instance_iter = iter(read_instance(type_instance + instance_name,name_folder))
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

    vehicle_capacity = capacity_input
    vehicle_max_number = dimension_input

    # get demands and coordinates
    cust_coordinates = []
    depot_coordinates = []

    for current_id in range(dimension_input):
        point_id = int(next(instance_iter))
        if point_id != current_id + 1:
            raise Exception("Unexpected index")
        x_coord = float(next(instance_iter))
        y_coord = float(next(instance_iter))
        if id_point == 0 :
            depot_coordinates = [x_coord,y_coord]
        else:
            cust_coordinates.append([x_coord,y_coord])
        id_point += 1


    element = next(instance_iter)
    if element != "DEMAND_SECTION":
        raise Exception("Expected line DEMAND_SECTION")

    # Get the demands
    cust_demands = []
    for current_id in range(dimension_input):
        point_id = int(next(instance_iter))
        if point_id != current_id + 1:
            raise Exception("Unexpected index")
        demand = int(next(instance_iter))
        if current_id > 0:
            cust_demands.append(demand)

    element = next(instance_iter)
    if element != "DEPOT_SECTION":
        raise Exception("Expected line DEPOT_SECTION")
    next(instance_iter) # pass id depot

    end_depot_section = int(next(instance_iter))
    if end_depot_section != -1:
        raise Exception("Expected only one depot.")

    

    return DataCvrp(vehicle_capacity,
                    dimension_input-1,
                    cust_demands,
                    cust_coordinates,
                    depot_coordinates
                    )

if __name__ == "__main__":
    if(len(sys.argv)>1):
        solve_demo(sys.argv[1:])
    else:
        print("""Please indicates the path of your instance like this : \n 
       python CVRP.py -i INSTANCE_PATH/NAME_INSTANCE \n
       -t TIME_RESOLUTION -s SOLVER_NAME (-p PATH_SOLVER (WINDOWS only))
       """)
       # uncomment for use the file without command line
       # solve_demo("A-n32-k5.vrp")
