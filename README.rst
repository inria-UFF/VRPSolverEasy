VRPSolverEasy 
==============================
.. image:: https://github.com/inria-UFF/VRPSolverEasy/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/inria-UFF/VRPSolverEasy/actions/workflows/python-package.yml

VRPSolverEasy is a Python package which provides a **simple interface
for** `VRPSolver <https://vrpsolver.math.u-bordeaux.fr/>`__, which is a
state-of-the-art Branch-Cut-and-Price exact solver for vehicle routing
problems (VRPs). The simplified interface is accessible for **users
without operations research background**, i.e., you do not need to know
how to model your problem as an Integer Programming problem. As a price
to pay for the simplicity, this interface is restricted to some standard
VRP variants, which involve the following features and their
combinations:

* capacitated vehicles, 
* customer time windows, 
* heterogeneous fleet,
* multiple depots,
* open routes,
* optional customers with penalties,
* parallel links to model transition time/cost trade-off,
* incompatibilities between vehicles and customers,
* customers with alternative locations and/or time windows.

To our knowledge, VRPSolver is the most efficient **exact** solver
available for VRPs. Its particularity is to focus on finding and
improving a **lower bound** on the optimal solution value of your
instance. It is less efficient in finding feasible solutions but still
can be better than available heuristic solvers for non-classic VRP
variants. One can expect to find **provably optimal solutions** for
most instances with up to 100 customers. A significant number of instances 
in the range of 101-200 customers may be solved too. A few even larger 
instances may be solved, but usually, this requires very long runs.
The performance of VRPSolver improves when very good initial upper bounds, 
obtained by an external heuristic solver, are provided. 

VRPSolver is based on a research proof-of-concept code prone to issues.
Use it only for research, teaching, testing, and R&D purposes at your
own risk. It is not suited for use in production. Please use Issues
section in this repository to report bugs and issues, and to give
suggestions.

License
-------

The VRPSolverEasy package itself is open-source and free to use. It
includes compiled libraries of
`BaPCod <https://bapcod.math.u-bordeaux.fr/>`__, its VRPSolver
extension, and COIN-OR CLP solver. These libraries are also free to use.

For better performance, it is possible to use VRPSolverEasy together
with CPLEX MIP solver. This combination called *academic version*
requires an access to the source code of BaPCod available with an
`academic-use-only
license <https://bapcod.math.u-bordeaux.fr/#licence>`__. The academic
version of VRPSolverEasy additionally includes a MIP-based (slow)
heuristic which is useful for finding feasible solutions in the absence
of an external heuristic solver.

Accompanying paper
------------------

The paper presents the motivation to create VRPSolverEasy, the interface of 
the package, the solution approach (optional to read), the computational 
results for the three classic VRP variants (CVRP, VRPTW, HFVRP), and possible
future extensions of the model. 
For the moment, the paper is available as a preprint :
    
    \N. Errami, E. Queiroga, R. Sadykov, E. Uchoa. "VRPSolverEasy: a Python 
    library for the exact solution of a rich vehicle routing problem", 
    `Technical report HAL-04057985 <https://hal.inria.fr/hal-04057985/document>`__, 2023.

Please cite it if you use VRPSolverEasy in your research.

Installation
------------

.. image:: https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg

``VRPSolverEasy`` requires a version of python >= 3.6

.. warning::
    Before starting the installation, we invite you to update 
    your version of pip by running this command: ::

        python -m pip install --upgrade pip

There is two different way to install ``VRPSolverEasy`` :

The first way is to install it with ``pip``::

   python -m pip install VRPSolverEasy

The second way is to follow these steps:

-  Download the package and extract it into a local directory
-  Move to this local directory and enter : ::

    python pip install .

Installation instructions for Mac computers with Apple ARM processors,
as well as for the academic version, are given in the documentation.

Example
-------

A simple example that shows how to use the VRPSolverEasy package:

.. code:: python


   import math
   import VRPSolverEasy as vrpse

   def compute_euclidean_distance(x_i, y_i, x_j, y_j):
       """compute the euclidean distance between 2 points from graph"""
       return round(math.sqrt((x_i - x_j)**2 +
                              (y_i - y_j)**2), 3)

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
   model = vrpse.Model()

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

   # solve model
   model.solve()
   model.export()

   if model.solution.is_defined():
       print(model.solution)

Documentation
-------------

Documentation, explanation of demos (CVRP, VRPTW, HFVRP, and MDVRP), and
the solver API are accessible here: https://vrpsolvereasy.readthedocs.io/en/latest/.

You can also build the documentation locally by following this
instructions from the source folder : ::

   cd docs
   python -m pip install -r requirements.txt
   cd ..
   make html

The HTML pages will be in the folder ``build\html``.

