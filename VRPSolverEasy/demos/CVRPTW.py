""" This module allows to solve Solomon instances of
Capacitated Vehicle Routing Problem with Time Windows. """


import os
import math
import sys
import getopt
from VRPSolverEasy.src import solver


class DataCvrptw:
    """Contains all data for CVRPTW problem
    """

    def __init__(
            self,
            vehicle_capacity: int,
            nb_customers: int,
            max_number: int,
            cust_demands=None,
            cust_coordinates=None,
            depot_coordinates=0,
            cust_tw_begin=None,
            cust_tw_end=None,
            cust_service_time=None,
            depot_tw_begin=0,
            depot_tw_end=0,
            depot_service_time=0):

        self.vehicle_capacity = vehicle_capacity
        self.nb_customers = nb_customers
        self.max_number = max_number
        self.cust_demands = cust_demands
        self.cust_coordinates = cust_coordinates
        self.depot_coordinates = depot_coordinates
        self.cust_tw_begin = cust_tw_begin
        self.cust_tw_end = cust_tw_end
        self.cust_service_time = cust_service_time
        self.depot_tw_begin = depot_tw_begin
        self.depot_tw_end = depot_tw_end
        self.depot_service_time = depot_service_time


def read_instance(name: str):
    """ Read an instance in the folder data from a given name """

    with open(
            os.path.normpath(name),
            "r", encoding="UTF-8") as file:
        return [str(element) for element in file.read().split()]



def compute_euclidean_distance(x_i, y_i, x_j, y_j, number_digit=3):
    """Compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), number_digit)


def solve_demo(instance_name,
               time_resolution=30,
               solver_name_input="CLP",
               solver_path=""):
    """return a solution from modelisation"""

    # read parameters given in command line
    type_instance = "CVRPTW/"
    if len(sys.argv) > 1:
        print(instance_name)
        opts = getopt.getopt(instance_name, "i:t:s:p:")
        for opt, arg in opts[0]:
            if opt in ["-i"]:
                instance_name = arg
            if opt in ["-t"]:
                time_resolution = float(arg)
            if opt in ["-s"]:
                solver_name_input = arg
            if opt in ["-p"]:
                solver_path = arg

    # read instance
    data = read_cvrptw_instances(instance_name)

    # modelisation of problem
    model = solver.Model()

    # add vehicle type
    model.add_vehicle_type(id=1,
                           start_point_id=0,
                           end_point_id=0,
                           max_number=data.max_number,
                           capacity=data.vehicle_capacity,
                           tw_begin=data.depot_tw_begin,
                           tw_end=data.depot_tw_end,
                           var_cost_dist=1
                           )
    # add depot
    model.add_depot(id=0,
                    service_time=data.depot_service_time,
                    tw_begin=data.depot_tw_begin,
                    tw_end=data.depot_tw_end
                    )

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i + 1,
                           service_time=data.cust_service_time[i],
                           tw_begin=data.cust_tw_begin[i],
                           tw_end=data.cust_tw_end[i],
                           demand=data.cust_demands[i]
                           )


    # Compute the links between depot and other points
    for i,cust_i in enumerate(data.cust_coordinates):
        dist = compute_euclidean_distance(cust_i[0],
                                          cust_i[1],
                                          data.depot_coordinates[0],
                                          data.depot_coordinates[1]
                                          )
        model.add_link(start_point_id=0,
                       end_point_id=i + 1,
                       distance=dist,
                       time=dist
                       )

    # Compute the links between points
    for i,cust_i in enumerate(data.cust_coordinates):
        for j in range(i + 1, len(data.cust_coordinates)):
            dist = compute_euclidean_distance(cust_i[0],
                                              cust_i[1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1]
                                              )
            model.add_link(start_point_id=i + 1,
                           end_point_id=j + 1,
                           distance=dist,
                           time=dist
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

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.solution.value


def read_cvrptw_instances(instance_full_path):
    """Read literature instances of CVRPTW ("Solomon" format) by giving the name of instance
        and returns dictionary containing all elements of model"""
    instance_iter = iter(
        read_instance(instance_full_path))

    for i in range(4):
        next(instance_iter)

    max_number_input = int(next(instance_iter))
    capacity_input = int(next(instance_iter))

    for i in range(13):
        next(instance_iter)

    depot_x = int(next(instance_iter))
    depot_y = int(next(instance_iter))
    next(instance_iter) #depot demand
    depot_tw_begin = int(next(instance_iter))
    depot_tw_end = int(next(instance_iter))
    depot_service_time = int(next(instance_iter))
    id_point = 0

    vehicle_capacity = capacity_input
    vehicle_max_number = max_number_input

    depot_coordinates = [depot_x, depot_y]

    cust_coordinates = []
    cust_demands = []
    cust_tw_begin = []
    cust_tw_end = []
    cust_service_time = []

    # Add the customers in the list of points
    while True:
        id_point += 1
        value = next(instance_iter, None)
        if value is None:
            break
        x_coord = float(next(instance_iter))
        y_coord = float(next(instance_iter))
        demand = int(next(instance_iter))
        tw_begin = int(next(instance_iter))
        tw_end = int(next(instance_iter))
        service_time = int(next(instance_iter))

        cust_coordinates.append([x_coord, y_coord])
        cust_tw_begin.append(tw_begin)
        cust_tw_end.append(tw_end + service_time)
        cust_service_time.append(service_time)
        cust_demands.append(demand)

    return DataCvrptw(vehicle_capacity,
                      id_point - 1,
                      vehicle_max_number,
                      cust_demands,
                      cust_coordinates,
                      depot_coordinates,
                      cust_tw_begin,
                      cust_tw_end,
                      cust_service_time,
                      depot_tw_begin,
                      depot_tw_end,
                      depot_service_time
                      )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_demo(sys.argv[1:])
    else:
        print("""Please indicates the path of your instance like this : \n
       python CVRPTW.py -i INSTANCE_PATH/NAME_INSTANCE \n
       -t TIME_RESOLUTION -s SOLVER_NAME (-p PATH_SOLVER (WINDOWS only))
       """)

