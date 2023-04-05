""" This module allows to solve CVRPLIB instances of
Capacitated Vehicle Routing Problem """

import os
import math
import sys
import getopt
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


def compute_euclidean_distance(x_i, y_i, x_j, y_j, number_digit=3):
    """Compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), number_digit)


def read_instance(name: str):
    """ Read an instance in the folder data from a given name """

    with open(
            os.path.normpath(name),
            "r", encoding="UTF-8") as file:
        return [str(element) for element in file.read().split()]


def solve_demo(instance_name,
               time_resolution=30,
               solver_name_input="CLP",
               solver_path=""):
    """return a solution from modelisation"""

    # read parameters given in command line
    type_instance = "CVRP/"
    if len(sys.argv) > 1:
        opts = getopt.getopt(instance_name, "i:t:s:p:")
        for opt, arg in opts[0]:
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
    data = read_cvrp_instances(instance_name)

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
        model.add_customer(id=i + 1,
                           demand=data.cust_demands[i]
                           )

    # Compute the links between depot and other points
    for i,cust_i in enumerate(data.cust_coordinates):
        dist = compute_euclidean_distance(cust_i[0],
                                          cust_i[1],
                                          data.depot_coordinates[0],
                                          data.depot_coordinates[1],
                                          0)

        model.add_link(start_point_id=0,
                       end_point_id=i + 1,
                       distance=dist
                       )

    # Compute the links between points
    for i,cust_i in enumerate(data.cust_coordinates):
        for j in range(i + 1, len(data.cust_coordinates)):
            dist = compute_euclidean_distance(cust_i[0],
                                              cust_i[1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1],
                                              0)
            model.add_link(start_point_id=i + 1,
                           end_point_id=j + 1,
                           distance=dist
                           )

    # set parameters
    model.set_parameters(time_limit=time_resolution,
                         solver_name=solver_name_input)

    ''' If you have cplex 22.1 installed on your laptop windows you have to specify
        solver path'''
    if (solver_name_input == "CPLEX" and solver_path != ""):
        model.parameters.cplex_path = solver_path

    #model.export(instance_name)

    # solve model
    model.solve()

    if model.solution.is_defined :
        print(f"""Statistics :
        best lower bound : { model.statistics.best_lb } 
        
        solution time : {model.statistics.solution_time}
        
        number of nodes : {model.statistics.nb_branch_and_bound_nodes}
        
        solution value : {model.solution.value}

        root lower bound : {model.statistics.root_lb}

        root root time : {model.statistics.root_time}.
        """)
        print(f"Status : {model.status}.\n")
        print(f"Message : {model.message}.\n")   
        for route in model.solution.routes:            
            print(f"Vehicle Type id : {route.vehicle_type_id}.")
            print(f"Ids : {route.point_ids}.")
            print(f"Load : {route.cap_consumption}.\n")


    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.solution.value


def read_cvrp_instances(instance_full_path):
    """Read literature instances from CVRPLIB by giving the name of instance
       and returns dictionary containing all elements of model"""

    instance_iter = iter(
        read_instance(instance_full_path))

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

    # get demands and coordinates
    cust_coordinates = []
    depot_coordinates = []

    for current_id in range(dimension_input):
        point_id = int(next(instance_iter))
        if point_id != current_id + 1:
            raise Exception("Unexpected index")
        x_coord = float(next(instance_iter))
        y_coord = float(next(instance_iter))
        if id_point == 0:
            depot_coordinates = [x_coord, y_coord]
        else:
            cust_coordinates.append([x_coord, y_coord])
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
    next(instance_iter)  # pass id depot

    end_depot_section = int(next(instance_iter))
    if end_depot_section != -1:
        raise Exception("Expected only one depot.")

    return DataCvrp(vehicle_capacity,
                    dimension_input - 1,
                    cust_demands,
                    cust_coordinates,
                    depot_coordinates
                    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_demo(sys.argv[1:])
    else:
        print("""Please indicates the path of your instance like this : \n
       python CVRP.py -i INSTANCE_PATH/NAME_INSTANCE \n
       -t TIME_RESOLUTION -s SOLVER_NAME (-p PATH_SOLVER (WINDOWS only))
       """)
