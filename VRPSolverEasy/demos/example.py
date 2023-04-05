""" This module allows to solve a simple example of routing problem """

import math
from VRPSolverEasy.src import solver


def compute_euclidean_distance(x_i, y_i, x_j, y_j):
    """compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), 3)


def run_example():
    """modelisation of small example using solver"""
    # data
    cost_per_distance = 10
    begin_time = 0
    end_time = 5000
    nb_point = 7

    # map with names and coordinates
    coordinates = {"Wisconsin, USA": (44.50, -89.50),  # depot
                   "West Virginia, USA": (39.000000, -80.500000),
                   "Vermont, USA": (44.000000, -72.699997),
                   "Texas, the USA": (31.000000, -100.000000),
                   "South Dakota, the US": (44.500000, -100.000000),
                   "Rhode Island, the US": (41.742325, -71.742332),
                   "Oregon, the US": (44.000000, -120.500000)
                   }

    # demands of points
    demands = [0, 500, 300, 600, 658, 741, 436]

    # Initialisation
    model = solver.Model()

    # Add vehicle type
    model.add_vehicle_type(
        id=1,
        start_point_id=0,
        end_point_id=0,
        name="VEH1",
        capacity=1100,
        max_number=6,
        var_cost_dist=cost_per_distance,
        tw_end=5000)

    # Add depot
    model.add_depot(id=0, name="DEPOT", tw_begin=0, tw_end=5000)

    coordinates_keys = list(coordinates.keys())
    # Add Customers
    for i in range(1, nb_point):
        model.add_customer(
            id=i,
            name=coordinates_keys[i],
            demand=demands[i],
            tw_begin=begin_time,
            tw_end=end_time)

    # Add links
    coordinates_values = list(coordinates.values())
    for i in range(0, 7):
        for j in range(i + 1, 7):
            dist = compute_euclidean_distance(coordinates_values[i][0],
                                              coordinates_values[j][0],
                                              coordinates_values[i][1],
                                              coordinates_values[j][1])
            model.add_link(
                start_point_id=i,
                end_point_id=j,
                distance=dist,
                time=dist)


    # solver model
    model.solve()
    model.export()

    if model.solution.is_defined():
        print(model.solution)


if __name__ == "__main__":
    run_example()
