MDVRP
=========
The Multi-Depot Vehicle Routing Problem (MDVRP) is a variant of the classic Vehicle Routing Problem (VRP) that involves multiple depots that serve a set of customers with a fleet of vehicles. The objective of the problem is to find a set of vehicle routes that satisfy the demand of all customers, while minimizing the total distance traveled by the vehicles.

Instance formats
----------------------------

The  **mdvrp.py** file allows you to resolve **Cordeau** instances in the following format : 

The first line contains the following information:

type m n t

* **type**: it's always equal to 2 in this variant
* **m**: number of vehicles
* **n**: number of customers
* **t**: number of depots 

The next t lines contain, for each day (or depot or vehicle type), the following information:

D Q:

* **D**: maximum duration of a route (not used)
* **Q**: maximum load of a vehicle

The next lines contain, for each customer, the following information:

i x y d q f a list e l

* **i**: customer number
* **x**: x coordinate
* **y**: y coordinate
* **d**: service duration (not used)
* **q**: demand
* **f**: frequency of visit (not used)
* **a**: number of possible visit combinations (not used)
* **list**: list of all possible visit combinations (not used)
* **e**: beginning of time window (not used)
* **l**: end of time window (not used)

Run instances
----------------------------
There are two ways to run a specific instance:

Command line
^^^^^^^^^^^^^^^^^^^^^^

After the installation, you can run an instance by specifying different parameters directly in the command line, like this::

    python CVRP.py -i INSTANCE_PATH/NAME_INSTANCE 
       -t TIME_RESOLUTION -s SOLVER_NAME (-p PATH_SOLVER (WINDOWS only))

If you want to use CPLEX as solver, you have to install cplex by following the different :doc:`installation </Installation/index>` steps.


Python file
^^^^^^^^^^^^^^^^^^^^^^
You can modify the demo directly in the file **MDVRP.py**, which is included in the folder demos. You can go to the bottom of the file, uncomment, and update this line::
    
    solve_demo("p01")

Demo code
----------------------------

Get data
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
   

    # read instance
    data = read_cvrptw_instances(instance_name,folder_data,type_instance)

In the first time, we read instance and get data with this attributes :

.. code-block:: python


        nb_depots = 2 
        nb_customers = 3       
        cust_demands = [15,52,65]
        cust_coordinates = [[55.21,44.36],[57.81,53.27]]
        depot_coordinates = [[54.69,57.36],[54.31,65.23]]

Add vehicle types
^^^^^^^^^^^^^^^^^^^^^^
  .. code-block:: python

    # add vehicle types
    for i in range(data.nb_depots):
        model.add_vehicle_type(id=i + 1,
                               start_point_id=i,
                               end_point_id=i,
                               capacity=data.vehicle_capacity,
                               max_number=data.nb_customers,
                               var_cost_dist=1
                               )

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
                           demand=data.cust_demands[i]
                           )

.. note::
   You have to put differents id for customers and depots.

Add links
^^^^^^^^^^^^^^^^^^^^^^  

.. code-block:: python

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
                     
    }

Set parameters
^^^^^^^^^^^^^^^^^^^^^^ 

.. code-block:: python

   # set parameters
      model.set_parameters(time_limit=30,
                           solver_name="CLP")

                     
Solve model
^^^^^^^^^^^^^^^^^^^^^^ 

.. code-block:: python

   # solve model
   model.solve()

Print solution
^^^^^^^^^^^^^^^^^^^^^^ 

You can print the solution with an automatic printing function :

.. code-block:: python

   # print solution
   print(model.solution)

or you can print manually each route, to do this, we invite you to consult the last section of the demo :doc:`/Demos/CVRP` 