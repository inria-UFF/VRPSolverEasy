""" This module allows to solve Cordeau’s instances of
Multi Depot Vehicle Routing Problem """

import os
import math
import sys
import getopt
from VRPSolverEasy.src import solver


class DataMdvrp:
    """Contains all data for MDVRP problem
    """

    def __init__(
            self,
            nb_customers: int,
            nb_depots: int,
            vehicle_capacity: int,
            cust_demands=None,
            cust_coordinates=None,
            depot_coordinates=None):
        self.nb_customers = nb_customers
        self.nb_depots = nb_depots
        self.vehicle_capacity = vehicle_capacity
        self.cust_demands = cust_demands
        self.cust_coordinates = cust_coordinates
        self.depot_coordinates = depot_coordinates


def compute_euclidean_distance(x_i, y_i, x_j, y_j, number_digit=3):
    """Compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), number_digit)


def read_instance(name: str, folder_data="/data/"):
    """ Read an instance in the folder data from a given name """
    path_project = os.path.join(os.path.dirname
                                (os.path.realpath(__file__)))
    if folder_data != "/data/":
        path_project = ""

    with open(
            path_project +
            os.path.normpath(
                folder_data +
                name),
            "r", encoding="UTF-8") as file:
        return [str(element) for element in file.read().split()]


def solve_demo(instance_name, folder_data="/data/",
               time_resolution=30,
               solver_name_input="CLP",
               solver_path=""):
    """return a solution from modelisation"""

    # read parameters given in command line
    type_instance = "MDVRP/"
    if len(sys.argv) > 1:
        print(instance_name)
        opts = getopt.getopt(instance_name, "i:t:s:p:")
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
    data = read_mdvrp_instances(instance_name, folder_data, type_instance)

    # modelisation of problem
    model = solver.Model()

    # add vehicle types
    for i in range(data.nb_depots):
        model.add_vehicle_type(id=i + 1,
                               start_point_id=i,
                               end_point_id=i,
                               capacity=data.vehicle_capacity,
                               max_number=data.nb_customers,
                               var_cost_dist=1
                               )
    # add depots
    for i in range(data.nb_depots):
        model.add_depot(id=i)

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i + data.nb_depots + 1,
                           demand=data.cust_demands[i]
                           )

    nb_link = 0

    # Compute the links between depots and other points
    for depot_id in range(data.nb_depots):
        for i, cust_i in enumerate(data.cust_coordinates):
            dist = compute_euclidean_distance(
                cust_i[0],
                cust_i[1],
                data.depot_coordinates[depot_id][0],
                data.depot_coordinates[depot_id][1])
            model.add_link(name="L" + str(nb_link),
                           start_point_id=depot_id,
                           end_point_id=i + data.nb_depots + 1,
                           distance=dist
                           )
            nb_link += 1

    # Compute the links between points
    for i,cust_i in enumerate(data.cust_coordinates):
        for j in range(i + 1, len(data.cust_coordinates)):
            dist = compute_euclidean_distance(cust_i[0],
                                              cust_i[1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1])
            model.add_link(name="L" + str(nb_link),
                           start_point_id=i + data.nb_depots + 1,
                           end_point_id=j + data.nb_depots + 1,
                           distance=dist
                           )
            nb_link += 1

    # set parameters
    model.set_parameters(time_limit=time_resolution,
                         solver_name=solver_name_input)

    ''' If you have cplex 22.1 installed on your laptop windows you have to specify
        solver path'''
    if (solver_name_input == "CPLEX" and solver_path != ""):
        model.parameters.cplex_path = solver_path

    # solve model
    model.solve()

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.statistics.solution_value


def read_mdvrp_instances(instance_name, name_folder, type_instance):
    """Read literature instances of MDVRP by giving the name of instance
        and returns dictionary containing all elements of model"""
    instance_iter = iter(
        read_instance(
            type_instance +
            instance_name,
            name_folder))

    # pass type instance
    next(instance_iter)

    next(instance_iter)

    nb_customers = int(next(instance_iter))
    nb_depots = int(next(instance_iter))

    vehicle_capacities = []
    for _ in range(nb_depots):
        # pass max duration
        next(instance_iter)
        vehicle_capacities.append(int(next(instance_iter)))

    cust_demands = []
    cust_coordinates = []
    for _ in range(nb_customers):
        next(instance_iter)
        cust_x = int(next(instance_iter))
        cust_y = int(next(instance_iter))
        cust_coordinates.append([cust_x, cust_y])
        # pass duration
        next(instance_iter)

        cust_demand = int(next(instance_iter))
        cust_demands.append(cust_demand)
        for _ in range(6):
            next(instance_iter)

    depot_coordinates = []
    # add depots and vehicle types
    for _ in range(nb_depots):
        next(instance_iter)
        cust_x = int(next(instance_iter))
        cust_y = int(next(instance_iter))
        depot_coordinates.append([cust_x, cust_y])

        for _ in range(4):
            next(instance_iter)

    return DataMdvrp(nb_customers,
                     nb_depots,
                     vehicle_capacities[0],
                     cust_demands,
                     cust_coordinates,
                     depot_coordinates
                     )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_demo(sys.argv[1:])
    else:
        print("""Please indicates the parameters of your model like this : \n
       python MDVRP.py -i INSTANCE_PATH/NAME_INSTANCE \n
       -t TIME_RESOLUTION -s SOLVER_NAME (-p PATH_SOLVER (WINDOWS only))
       """)
       # uncomments for use the file without command line
       # solve_demo("p02")
