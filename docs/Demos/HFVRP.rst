HFVRP
=========
The Heterogeneous Fleet Vehicle Routing Problem (HFVRP) is a variant of the CVRP in which vehicles have different capacity, fixed cost and unitary traveling costs. 

Instances format
----------------

The demo read the instances in the following format (standard in the academic literature for the HFVRP): 

* The first line indicates the number of points (depot and customers).
* The, for each point, the following information is given :
   
    * Index of the point
    * X coordinate
    * Y coordinate  
    * Demand

* Afterwards, the number of vehicle types is given and the following lines contain for each vehicle type:
   
   * Capacity
   * Fixed cost 
   * Variable cost (cost traveling each unit distance) 
   * Minimum number of vehicles to use (always zero) 
   * Maximum number of vehicles to use 

Run instances
-------------
There are two ways to run a specific instance:

Command line
^^^^^^^^^^^^^^^^^^^^^^

You can solve an instance by specifying different parameters directly in the command line, like this::

    python HFVRP.py -i <instance path> -t <time limit> -s <solver_name>

CPLEX solver can be used only with the :doc:`academic version </Installation/index>`. When using CPLEX solver on a Windows computer, one should give its path: :code:`-p <path to CPLEX>`.

Python file
^^^^^^^^^^^^^^^^^^^^^^
You can specify the instance name directly in the demo file **HFVRP.py**, by uncommenting the last line::
    
    solve_demo("c50_13fsmd.txt")


Demo code
----------------------------

Get data
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
   

    # read instance
    data = read_hfvrp_instance(instance_name,folder_data)

An example of the contents of :code:`data` :

.. code-block:: python

        nb_vehicle_types = 2
        nb_customers = 3
        vehicle_capacities = [300,250]
        vehicle_fixed_costs = [12,24]
        vehicle_var_costs = [12,24]
        vehicle_max_numbers = [3,3]
        cust_demands = [15,52,65]
        cust_coordinates = [[55.21,44.36],[54.31,65.23],[57.81,53.27]]
        depot_coordinates = [54.69,57.36]

Add vehicle types
^^^^^^^^^^^^^^^^^
  .. code-block:: python

    # create the model
    model = solver.Model()

    for i in range(data.nb_vehicle_types):
        # add vehicle type
        model.add_vehicle_type(id=i + 1,
                               start_point_id=0,
                               end_point_id=0,
                               capacity=data.vehicle_capacities[i],
                               max_number=data.vehicle_max_numbers[i],
                               fixed_cost=data.vehicle_fixed_costs[i],
                               var_cost_dist=data.vehicle_var_costs[i])

Add depot and customers 
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # add depot
    model.add_depot(id=0)

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i+1, 
                           demand=data.cust_demands[i])

Add links
^^^^^^^^^^^^^^^^^^^^^^  

.. code-block:: python


    # Compute the links between depot and other points
    for i,cust_i in enumerate(data.cust_coordinates):
        dist = compute_euclidean_distance(cust_i[0],
                                          cust_i[1],
                                          data.depot_coordinates[0],
                                          data.depot_coordinates[1])
        model.add_link(start_point_id=0,
                       end_point_id=i + 1,
                       distance=dist)

    # Compute the links between points
    for i,cust_i in enumerate(data.cust_coordinates):
        for j in range(i + 1, len(data.cust_coordinates)):
            dist = compute_euclidean_distance(cust_i[0],
                                              cust_i[1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1])
            model.add_link(start_point_id=i + 1,
                           end_point_id=j + 1,
                           distance=dist)                 
    }

Set parameters
^^^^^^^^^^^^^^^^^^^^^^ 

.. code-block:: python

    # set parameters
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