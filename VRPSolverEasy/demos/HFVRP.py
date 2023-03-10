""" This module allows to solve Queiroga instances of
Heterogeneous Fleet Vehicle Routing Problem """

import os, math, sys , getopt
from VRPSolverEasy.src import solver


class DataHfvrp:
    """Contains all data for HFVRP problem
    """
    def __init__(
            self,
            nb_customers: int,
            nb_vehicle_types: int,
            vehicle_capacities=None,
            vehicle_fixed_costs=None,
            vehicle_var_costs=None,
            cust_demands=None,
            cust_coordinates=None,
            depot_coordinates=None):
        self.vehicle_capacities = vehicle_capacities
        self.vehicle_fixed_costs = vehicle_fixed_costs
        self.vehicle_var_costs = vehicle_var_costs
        self.nb_customers = nb_customers
        self.nb_vehicle_types = nb_vehicle_types
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
    
    # modelisation of problem
    model = solver.Model()

    for i in range(data.nb_vehicle_types):
        # add vehicle type
        model.add_vehicle_type(id=i+1,
                            start_point_id=0,
                            end_point_id=0,
                            capacity=data.vehicle_capacities[i],
                            max_number=data.nb_customers,
                            fixed_cost=data.vehicle_fixed_costs[i],
                            var_cost_dist=data.vehicle_var_costs[i]
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
                                          data.depot_coordinates[1])

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
                                              data.cust_coordinates[j][1])

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

    # get demands and coordinates
    cust_coordinates = []
    cust_demands = []
    depot_coordinates = [depot_x,depot_y]

    for i in range(nb_points):
        id_point += 1
        next(instance_iter) # pass id point (take index)
        x_coord = float(next(instance_iter))
        y_coord = float(next(instance_iter))
        demand = int(next(instance_iter))
        cust_coordinates.append([x_coord,y_coord])
        cust_demands.append(demand)

    nb_vehicles = int(next(instance_iter))

    vehicle_capacities = []
    vehicle_fixed_costs = []
    vehicle_var_costs = []

    for k in range(1, nb_vehicles+1):
        capacity = int(next(instance_iter))
        fixed_cost = float(next(instance_iter))
        var_cost_dist = float(next(instance_iter))
        next(instance_iter) # pass min number
        max_number = int(next(instance_iter))

        vehicle_capacities.append(capacity)
        vehicle_fixed_costs.append(fixed_cost)
        vehicle_var_costs.append(var_cost_dist)


    return DataHfvrp(nb_points,
                     nb_vehicles,
                     vehicle_capacities,
                     vehicle_fixed_costs,
                     vehicle_var_costs,
                     cust_demands,
                     cust_coordinates,
                     depot_coordinates
                     )


if __name__ == "__main__":
    if(len(sys.argv)>1):
        solve_demo(sys.argv[1:])
    else:
        print("""Please indicates the parameters of your model like this : \n 
       python HFVRP.py -i INSTANCE_PATH/NAME_INSTANCE \n
       -t TIME_RESOLUTION -s SOLVER_NAME (-p PATH_SOLVER (WINDOWS only))
       """)
       #uncomments for use the file without command line
       # solve_demo("c50_13fsmd.txt")
       
