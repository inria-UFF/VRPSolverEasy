""" This module allows to solve instances of
a Rich Vehicle Routing Problem """

import os
import math
import sys
import getopt
from VRPSolverEasy.src import solver

class Depot:
    def __init__(self, id, x, y, tw_begin, tw_end):
        self.id = id
        self.x = x
        self.y = y
        self.tw_begin = tw_begin
        self.tw_end = tw_end
    def __str__(self):
        return (f"Depot(id: {self.id}, x: {self.x}, y: {self.y}, "
                f"tw_begin: {self.tw_begin}, tw_end: {self.tw_end})")

class Vehicle:
    def __init__(self, capacity, fixed_cost, var_cost, max_number):
        self.capacity = capacity
        self.fixed_cost = fixed_cost
        self.var_cost = var_cost
        self.max_number = max_number
    def __str__(self):
        return (f"Vehicle(capacity: {self.capacity}, "
                f"fixed_cost: {self.fixed_cost}, var_cost: {self.var_cost}, "
                f"max_number: {self.max_number})")

class Customer:
    def __init__(self, id, x, y, demand, service_time, optional, only_small_veh, time_windows):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.service_time = service_time
        self.optional = optional # Is the customer optional?
        self.only_small_veh = only_small_veh # Can the customer served only by small vehicles? 
        self.time_windows = time_windows # List of time windows (list of pairs)
    def __str__(self):
        tw_str = ', '.join([f"({start}, {end})" for start, end in self.time_windows])
        return (f"Customer(id: {self.id}, x: {self.x}, y: {self.y}, "
                f"demand: {self.demand}, service_time: {self.service_time}, "
                f"optional: {self.optional}, only_small_veh: {self.only_small_veh}, "
                f"time_windows: [{tw_str}])")

class DataRichVrp:
    """Contains all data for RichVRP
    """
    def __init__(
            self,
            depots : None,
            big_vehicle : None,
            small_vehicle : None,
            customers : None):
        self.depots = depots
        self.big_vehicle = big_vehicle
        self.small_vehicle = small_vehicle
        self.customers = customers 
    def __str__(self):
        depots_str = '\n'.join([str(depot) for depot in self.depots])
        big_vehicle_str = str(self.big_vehicle)
        small_vehicle_str = str(self.small_vehicle)
        customers_str = '\n'.join([str(customer) for customer in self.customers])
        return (f"DataRichVrp:\n\nDepots:\n{depots_str}\n\nBig Vehicle:\n{big_vehicle_str}"
                f"\n\nSmall Vehicle:\n{small_vehicle_str}\n\nCustomers:\n{customers_str}")

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
    data = read_richvrp_instance(instance_name)
    print(data)

    # modelisation of problem
    model = solver.Model()

    big_vehicle_id = 1 # Big vehicles have odd ids
    big_vehicle_ids = [] # Store all the ids for big vehicles
    small_vehicle_id = 2 # Small vehicles have even ids
    # Add depots and vehicles
    for depot in data.depots:
        # Add the depot
        model.add_depot(id = depot.id,
                        tw_begin = depot.tw_begin,
                        tw_end = depot.tw_end)
        # Add the big vehicle to this depot
        model.add_vehicle_type(id = big_vehicle_id,
                               start_point_id = depot.id,
                               end_point_id = -1, # A vehicle may end anywhere 
                               capacity = data.big_vehicle.capacity,
                               max_number = data.big_vehicle.max_number,
                               fixed_cost = data.big_vehicle.fixed_cost,
                               var_cost_dist = data.big_vehicle.var_cost,
                               tw_begin = depot.tw_begin,
                               tw_end = depot.tw_end)
        # Add the small vehicle to this depot
        model.add_vehicle_type(id = small_vehicle_id,
                               start_point_id = depot.id,
                               end_point_id = -1, # A vehicle may end anywhere 
                               capacity = data.small_vehicle.capacity,
                               max_number = data.small_vehicle.max_number,
                               fixed_cost = data.small_vehicle.fixed_cost,
                               var_cost_dist = data.small_vehicle.var_cost,
                               tw_begin = depot.tw_begin,
                               tw_end = depot.tw_end)
        big_vehicle_ids.append(big_vehicle_id)
        big_vehicle_id += 2
        small_vehicle_id += 2

    # ID for alternative points of a customer with multiple time windows
    next_id = max([customer.id for customer in data.customers]) + 1
    # IDs of a customer, including the alternative ones
    customer_ids = {customer.id : [customer.id] for customer in data.customers}
    # Add customers
    for customer in data.customers:
        # Add a point for each time window of a customer
        for i, tw in enumerate(customer.time_windows):
            point_id = customer.id
            if i > 0: # Is it an alternative point?
                point_id = next_id
                customer_ids[customer.id].append(next_id)
                next_id += 1 # Get the next alternative ID
            model.add_customer(id = point_id,
                                id_customer = customer.id,
                                demand = customer.demand,
                                service_time = customer.service_time,
                                tw_begin = tw[0],
                                tw_end = tw[1],
                                penalty = 1.0 if customer.optional else 0.0,
                                incompatible_vehicles = big_vehicle_ids if customer.only_small_veh else [])

    # Compute the links between depots and other points
    for depot in data.depots:
        for customer in data.customers:
            dist = compute_euclidean_distance(customer.x, customer.y, depot.x, depot.y)
            for point_id in customer_ids[customer.id]:
                model.add_link(start_point_id = depot.id,
                                end_point_id = point_id,
                                distance = dist,
                                time = dist)
                
    # Compute the links between customer points
    for i, c1 in enumerate(data.customers):
        for j, c2 in enumerate(data.customers):
            if j <= i:
                continue
            dist = compute_euclidean_distance(c1.x, c1.y, c2.x, c2.y)
            # Add a link for each pair of points from c1 to c2
            for point_id_c1 in customer_ids[c1.id]:
                for point_id_c2 in customer_ids[c2.id]:
                    model.add_link(start_point_id = point_id_c1,
                                    end_point_id = point_id_c2,
                                    distance = dist,
                                    time = dist)

    # set parameters
    model.set_parameters(time_limit=time_resolution,
                         solver_name=solver_name_input)

    ''' If you have cplex 22.1 installed on your laptop windows you have to specify
        solver path'''
    if (solver_name_input == "CPLEX" and solver_path != ""):
        model.parameters.cplex_path = solver_path

    # model.export(instance_name)

    # Solve model
    model.solve()

    print("\nCustomer IDs and time windows:")
    for customer in data.customers:
        ids_and_tws = []
        for i, point_id in enumerate(customer_ids[customer.id]):
            ids_and_tws.append(f"(id: {point_id}, tw: {list(customer.time_windows[i])})")
        print(f"Customer {customer.id}: {', '.join(ids_and_tws)}")

    if model.solution.is_defined():
        print(model.solution)

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.solution.value

def read_richvrp_instance(instance_full_path):
    """Read instance of RichVRP by giving the name of instance
        and returns dictionary containing all elements of model"""
    instance_iter = iter(
        read_instance(instance_full_path))

    nb_depots = int(next(instance_iter))

    # Read depots
    depots = []
    for _ in range(nb_depots):
        id = int(next(instance_iter))
        x = int(next(instance_iter))
        y = int(next(instance_iter))
        tw_begin = int(next(instance_iter))
        tw_end = int(next(instance_iter))
        depots.append(Depot(id, x, y, tw_begin, tw_end))

    # Read big vehicle
    capacity_big_veh = int(next(instance_iter))
    fixed_cost_big_veh = int(next(instance_iter))
    var_cost_big_veh = float(next(instance_iter))
    max_numb_big_veh = int(next(instance_iter))
    big_vehicle = Vehicle(capacity_big_veh, fixed_cost_big_veh, var_cost_big_veh, max_numb_big_veh)

    # Read small vehicle
    capacity_small_veh = int(next(instance_iter))
    fixed_cost_small_veh = int(next(instance_iter))
    var_cost_small_veh = float(next(instance_iter))
    max_numb_small_veh = int(next(instance_iter))
    small_vehicle = Vehicle(capacity_small_veh, fixed_cost_small_veh, var_cost_small_veh, max_numb_small_veh)

    # Read customers
    nb_customers = int(next(instance_iter))
    customers = []
    for _ in range(nb_customers):
        id = int(next(instance_iter))
        x = int(next(instance_iter))
        y = int(next(instance_iter))
        demand = int(next(instance_iter))
        service_time = int(next(instance_iter))
        optional = int(next(instance_iter)) == 1 if True else False
        small_vehicle_flag = int(next(instance_iter)) == 1 if True else False
        nb_time_windows = int(next(instance_iter))
        time_windows = []
        for _ in range(nb_time_windows):
            tw_begin = int(next(instance_iter))
            tw_end = int(next(instance_iter))
            time_windows.append((tw_begin, tw_end))
        customers.append(Customer(id, x, y, demand, service_time, optional, small_vehicle_flag, time_windows))

    return DataRichVrp(depots, big_vehicle, small_vehicle, customers)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_demo(sys.argv[1:])
    else:
        print("""Please indicates the parameters of your model like this : \n
       python RichVRP.py -i INSTANCE_PATH/NAME_INSTANCE \n
       -t TIME_RESOLUTION -s SOLVER_NAME (-p PATH_SOLVER (WINDOWS only))
       """)
