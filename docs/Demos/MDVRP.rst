MDVRP
=========
The Multi-Depot Vehicle Routing Problem (MDVRP) is a variant of the CVRP in which vehicles are based in different depots.

Instance formats
----------------------------

The demo reads instances in the standard "Cordeaux" format. See `this repository <https://github.com/fboliveira/MDVRP-Instances>`_ for details.

The first line contains the following information:

type m n t

* **type**: it's equal to 2 for the MDVRP
* **m**: number of vehicles
* **n**: number of customers
* **t**: number of depots 

The next *t* lines contain, for each depot , the following information:

D Q:

* **D**: maximum duration of a route (not supported in this demo)
* **Q**: maximum load of a vehicle

The next lines contain, for each customer, the following information:

i x y d q f a list e l

* **i**: customer id
* **x**: x coordinate
* **y**: y coordinate
* **d**: service duration (not supported in this demo)
* **q**: demand
* **f**: frequency of visit (not used in MDVRP)
* **a**: number of possible visit combinations (not used in MDVRP)
* **list**: list of all possible visit combinations (not used in MDVRP)
* **e**: beginning of time window (not supported in this demo)
* **l**: end of time window (not supported in this demo)

Run instances
----------------------------
There are two ways to run a specific instance:

Command line
^^^^^^^^^^^^^^^^^^^^^^

You can solve an instance by specifying different parameters directly in the command line, like this::

    python MDVRP.py -i <instance path> -t <time limit> -s <solver_name>

CPLEX solver can be used only with the :doc:`academic version </Installation/index>`. When using CPLEX solver on a Windows computer, one should give its path: :code:`-p <path to CPLEX>`.


Demo code
----------------------------

Get data
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
   
    data = read_instance(instance_name,folder_data)

An example of the contents of :code:`data` :

.. code-block:: python

        nb_depots = 2 
        nb_customers = 3   
        vehicle_capacity = 60    
        cust_demands = [15,52,65]
        cust_coordinates = [[55.21,44.36],[57.81,53.27]]
        depot_coordinates = [[54.69,57.36],[54.31,65.23]]

Add vehicle types
^^^^^^^^^^^^^^^^^

Here we define a separate vehicle type for each depot. Each vehicle type is characterized by a depot where vehicles of this type start and end. 

.. code-block:: python

    # add vehicle types
    for i in range(data.nb_depots):
        model.add_vehicle_type(id=i + 1,
                               start_point_id=i,
                               end_point_id=i,
                               capacity=data.vehicle_capacity,
                               max_number=data.nb_customers,
                               var_cost_dist=1)

Here the start point id and the end point id corresponds to the id of depot assigned. Moreover, the maximum number of vehicle cannot be less than number of customers.

Add depots and customers 
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # add depots
    for i in range(data.nb_depots):
        model.add_depot(id=i)

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i + data.nb_depots + 1,
                           demand=data.cust_demands[i])

.. note::
   IDs of depots and customers should be different.  

Add links
^^^^^^^^^^^^^^^^^^^^^^  

.. code-block:: python

    # Compute the links between depots and other points
    for depot_id in range(data.nb_depots):
        for i, cust_i in enumerate(data.cust_coordinates):
            dist = compute_euclidean_distance(
                cust_i[0],
                cust_i[1],
                data.depot_coordinates[depot_id][0],
                data.depot_coordinates[depot_id][1])
                
            model.add_link(start_point_id=depot_id,
                           end_point_id=i + data.nb_depots + 1,
                           distance=dist
                           )

    # Compute the links between points
    for i,cust_i in enumerate(data.cust_coordinates):
        for j in range(i + 1, len(data.cust_coordinates)):
            dist = compute_euclidean_distance(cust_i[0],
                                              cust_i[1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1])

            model.add_link(start_point_id=i + data.nb_depots + 1,
                           end_point_id=j + data.nb_depots + 1,
                           distance=dist
                           )
                     
    }

Set parameters
^^^^^^^^^^^^^^^^^^^^^^ 

.. code-block:: python

    model.set_parameters(time_limit=30, solver_name="CLP")

                     
Solve model
^^^^^^^^^^^^^^^^^^^^^^ 

.. code-block:: python

   model.solve()

Print solution
^^^^^^^^^^^^^^^^^^^^^^ 

You can output the solution using the :code:`print()` function

.. code-block:: python

    if (model.solution.is_defined())
        print(model.solution)

or you can analyze the solution manually by retrieving each route. For and example, consult the last section of the demo :doc:`/Demos/CVRP`. 