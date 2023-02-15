# VRPSolverEasy [![Python package](https://github.com/inria-UFF/VRPSolverEasy/actions/workflows/python-package.yml/badge.svg)](https://github.com/inria-UFF/VRPSolverEasy/actions/workflows/python-package.yml)

This project is an implementation of VRPSolver, a package allows you to resolve routing problems by using the bapCod solver,(COIN-OR) CLP and CPLEX solver.

## Installation 

![Python](https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg)

`VRPSolverEasy` requires a version of python  >= 3.7

There is two differents way to install `VRPSolverEasy` :

The first way is to install it with `pip` 
```
python -m pip install VRPSolverEasy
```
The second way is to following this steps:

- Download the package and extract it into a local directory
- (Windows) Move to this local directory and enter :
```
 python pip install .
```
- (MacOs and Linux):
```
sudo python pip install .
```
If you work on ARM Mac, you must install python in x86-x64 architecture and use the same commands.

## Examples

### Initialisation of model

After installation, if you want to create your first model you have to import the solver like this:
```
import VRPSolverEasy.src.solver as solver
```

#### Create and solve your first model 
```
    """modelisation of small example using solver"""
    # data
    cost_per_time = 10
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
    model = solver.CreateModel()

    # Add vehicle type
    model.add_vehicle_type(
        id=1,
        start_point_id=0,
        end_point_id=0,
        name="VEH1",
        capacity=1100,
        max_number=6,
        var_cost_dist=cost_per_distance,
        var_cost_time=cost_per_time,
        tw_end=5000)

    # Add depot
    model.add_depot(id=0, name="D1", tw_begin=0, tw_end=5000)

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
    enumerate = 1
    for i in range(0, 7):
        for j in range(i + 1, 7):
            dist = compute_euclidean_distance(coordinates_values[i][0],
                                              coordinates_values[j][0],
                                              coordinates_values[i][1],
                                              coordinates_values[j][1])
            model.add_link(
                "arc" + str(enumerate),
                start_point_id=i,
                end_point_id=j,
                distance=dist,
                time=dist)
            enumerate += 1

    # solver model
    model.solve()
    model.export()

    print(model.solution)
```
## Documentation

If you want to know more about the documentation, you can go on https://vrpsolvereasy.readthedocs.io/en/latest/. 
