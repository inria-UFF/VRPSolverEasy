CVRP
================

The Capacitated Vehicle Routing Problem (CVRP) is the most basic VRP, where a set of homogeneous vehicles of limited capacity serves a set of customers, located at different points in a geographic area. The objective of the problem is to minimize the total routing cost, i.e. the total distance traveled by vehicles. 

Instances format
----------------------------

The demo reads instances in the standard `CVRPLIB <http://vrp.galgos.inf.puc-rio.br/index.php/en/>`_ format.

* The first line indicates the name of the instance.
* The second line gives a comment about the data, for example, the optimal value expected.
* The third line gives the type of the instance.
* The fourth line gives the dimension of the instance.
* The fifth line indicates how distances are calculated.
* the 6th line indicates the capacity of the vehicle.  
* After the keyword *NODE_COORD_SECTION*, the following information is given for each point:

    * Index of the point
    * X coordinate
    * Y coordinate  

After the keyword *DEMAND_SECTION*, the following information is given for each point :
   
    * Index of the point
    * Demand

After the keyword *DEPOT_SECTION*, we retrieve the index of the depot.
   
Run instances
-------------
There are two ways to run a specific instance:

Command line
^^^^^^^^^^^^^^^^^^^^^^

You can solve an instance by specifying different parameters directly in the command line, like this::

    python CVRP.py -i <instance path> -t <time limit> -s <solver_name>

CPLEX solver can be used only with the :doc:`academic version </Installation/index>`. When using CPLEX solver on a Windows computer, one should give its path: :code:`-p <path to CPLEX>`.

Python file
^^^^^^^^^^^^^^^^^^^^^^
You can specify the instance name directly in the demo file **CVRP.py**, by uncommenting the last line::
    
    solve_demo("A-n36-k5.vrp")


Demo code
----------------------------

Get data
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
   
    # read instance
    data = read_instance(instance_name,folder_data)

An example of the contents of :code:`data` :

.. code-block:: python

        vehicle_capacity = 300
        nb_customers = 3
        cust_demands = [15,52,65]
        cust_coordinates = [[55.21,44.36],[54.31,65.23],[57.81,53.27]]
        depot_coordinates = [54.69,57.36]


Add vehicle type
^^^^^^^^^^^^^^^^^^^^^^

  .. code-block:: python

    # create model
    model = solver.Model()

    # add vehicle type
    model.add_vehicle_type(id=1, #id cannot be less than 1
                           start_point_id=0,
                           end_point_id=0,
                           max_number=data.nb_customers,
                           capacity=data.vehicle_capacity,
                           var_cost_dist=1)

.. note::
   You can also model the variant with open routes (open vehicle routing problem or ORP) by specifying :code:`start_point_id=-1` and/or :code:`end_point_id=-1`. An open route may start and/or finish at any customer point. 
   

Add depot and customers 
^^^^^^^^^^^^^^^^^^^^^^^^^

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
                                          data.depot_coordinates[1], 0)

        model.add_link(start_point_id=0,
                       end_point_id=i + 1,
                       distance=dist)

    # Compute the links between points
    for i,cust_i in enumerate(data.cust_coordinates):
        for j in range(i + 1, len(data.cust_coordinates)):
            dist = compute_euclidean_distance(cust_i[0],
                                              cust_i[1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1], 0)
            model.add_link(start_point_id=i + 1,
                           end_point_id=j + 1,
                           distance=dist)
                     
    }

In this demo, we have only one vehicle type, and the Eucledian distances are used.


Set parameters
^^^^^^^^^^^^^^^^^^^^^^ 

.. code-block:: python

   # set parameters
      model.set_parameters(time_limit=30,
                           solver_name="CLP")

                     
Solve model
^^^^^^^^^^^^^^^^^^^^^^ 

.. code-block:: python

   model.solve()

.. note::
   You can also enumerate all feasible routes by changing the action parameter (possible only for small instances) ::

     model.parameters.action = "enumAllFeasibleRoutes"

Print solution
^^^^^^^^^^^^^^^^^^^^^^ 
.. _target to paragraph:

* The first command will print solution with an automatically printing function :

.. code-block:: python
   
   # print solution
   print(model.solution)

.. code-block:: text
    :caption: Output
    
    Route for vehicle 1:
    ID : 0 --> 30 --> 16 --> 1 --> 12 --> 0
    Load : 0.0 --> 14.0 --> 32.0 --> 51.0 --> 72.0 --> 72.0
    Total cost : 73.0

    Route for vehicle 1:
    ID : 0 --> 27 --> 24 --> 0
    Load : 0.0 --> 20.0 --> 44.0 --> 44.0
    Total cost : 59.0

    ...

* The second way is to print the solver statistics and solution manually :

.. code-block:: python

    if model.solution.is_defined :
        print(f"""Statistics :
        best lower bound : { model.statistics.best_lb } 
        
        solution time : {model.statistics.solution_time}

        number of nodes : {model.statistics.nb_branch_and_bound_nodes}
        
        solution value : {model.solution.value}

        root lower bound : {model.statistics.root_lb}

        root root time : {model.statistics.root_time}.
        """)
        print(f"Status : {model.status}.\n")
        print(f"Message : {model.message}.\n")   
        for route in model.solution.routes:            
            print(f"Vehicle Type id : {route.vehicle_type_id}.")
            print(f"Ids : {route.point_ids}.")
            print(f"Load : {route.cap_consumption}.\n")


.. code-block:: text
    :caption: Output

        Statistics :
            best lower bound : 784.0

            solution time : 1.1036816

            number of nodes : 1

            solution value : 784.0000000000484

            root lower bound : 784.0

            root root time : 1.0990863.

        Status : 0.

        Message : The solution found is optimal.

        Vehicle Type id : 1.
        Ids : [0, 30, 16, 1, 12, 0].
        Load : [0.0, 14.0, 32.0, 51.0, 72.0, 72.0].

        Vehicle Type id : 1.
        Ids : [0, 27, 24, 0].
        Load : [0.0, 20.0, 44.0, 44.0].

        ...