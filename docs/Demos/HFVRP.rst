HFVRP
=========
The Heterogeneous Fleet Vehicle Routing Problem (HFVRP) is a variant of the classical Vehicle Routing Problem (VRP) in which the fleet of vehicles is composed of vehicles with different attributes (capacities, costs..). The objective of the HFVRP is to minimize the total travel time, distance or cost of the vehicles while servicing a set of customers with specific demands and time windows, subject to various constraints

Instance formats
----------------------------

The  **hfvrp.py** file allows you to resolve **queiroga** instances in the following format : 

* The first line indicates the number of points.
* After the number of points, for each point, the following informations are given :
   
    * Index of point
    * X coordinate
    * Y coordinate  
    * Demand

* After these lines, the number of vehicle types is given and the following lines contain for each vehicle :
   
   * Capacity
   * Fixed cost 
   * Variable cost 
   * Minimum number of vehicles 
   * Maximum number of vehicles 

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
You can modify the demos directly in the file **HFVRP.py**, which is included in the folder demos. You can go to the bottom of the file, uncomment, and update this line::
    
    solve_demo("c50_13fsmd.txt")


Demo code
----------------------------

Get data
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
   

    # read instance
    data = read_hfvrp_instances(instance_name,folder_data,type_instance)

In the first time, we read instance and get data with this attributes :

.. code-block:: python

        vehicle_capacities = [300,250]
        vehicle_fixed_costs = [12,24]
        vehicle_var_costs = [12,24]
        nb_customers = 3
        nb_vehicle_types = 2
        cust_demands = [15,52,65]
        cust_coordinates = [[55.21,44.36],[54.31,65.23],[57.81,53.27]]
        depot_coordinates = [54.69,57.36]

Add vehicle types
^^^^^^^^^^^^^^^^^^^^^^
  .. code-block:: python

    # modelisation of problem
    model = solver.Model()

    for i in range(data.nb_vehicle_types):
        # add vehicle type
        model.add_vehicle_type(id=i + 1,
                               start_point_id=0,
                               end_point_id=0,
                               capacity=data.vehicle_capacities[i],
                               max_number=data.nb_customers,
                               fixed_cost=data.vehicle_fixed_costs[i],
                               var_cost_dist=data.vehicle_var_costs[i]
                               )

In this demos, each type of vehicle is characterized by its capacity, its fixed cost and its variable cost.

Add depot and customers 
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # add depot
    model.add_depot(id=0)

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i+1, 
                           demand=data.cust_demands[i]
                           )

Add links
^^^^^^^^^^^^^^^^^^^^^^  

.. code-block:: python

    nb_link = 0

    # Compute the links between depot and other points
    for i,cust_i in enumerate(data.cust_coordinates):
        dist = compute_euclidean_distance(cust_i[0],
                                          cust_i[1],
                                          data.depot_coordinates[0],
                                          data.depot_coordinates[1])
        model.add_link(name="L" + str(nb_link),
                       start_point_id=0,
                       end_point_id=i + 1,
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
                           start_point_id=i + 1,
                           end_point_id=j + 1,
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

   # set parameters
   model.solve()
   
Print solution
^^^^^^^^^^^^^^^^^^^^^^ 

You can print solution with an automatically printing function :

.. code-block:: python

   # print solution
   print(model.solution)

or you can print manually each route, to do this, we invite you to consult the last section of the demo :doc:`/Demos/CVRP` 