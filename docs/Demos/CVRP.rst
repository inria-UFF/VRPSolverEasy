CVRP
================

The Capacitated Vehicle Routing Problem (CVRP) is a well-known optimization problem in operations research, where a set of vehicles with limited capacities is tasked with servicing a set of customers, located at different points in a geographic area, with minimum cost. The objective of the problem is to find the optimal route for each vehicle such that all customers are visited, and the total distance traveled is minimized, while respecting the capacity constraints of the vehicles.

Instance formats
----------------------------

The **cvrp.py** file allows you to resolve **augerat** instances in the following format : 

* The first line indicates the name of the instance.
* The second line gives a comment about the data, for example, the optimal value expected.
* The third line gives the type of the instance.
* The fourth line gives the dimension of the problem
* The fifth line indicates the technique used for calculating the distance between 2 points.
* the 6th line indicates the capacity of the vehicle.  
* After the keyword *NODE_COORD_SECTION*, for each point, the following informations are given :

    * Index of the point
    * X coordinate
    * Y coordinate  

After the keyword *DEMAND_SECTION*, for each point the following informations are given :
   
    * Index of the point
    * Demand

After the keyword *DEPOT_SECTION*, we retrieve the index of the depot.
   
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
You can modify the demos directly in the file **CVRP.py**, which is included in the folder demos. You can go to the bottom of the file, uncomment, and update this line::
    
    solve_demo("A-n36-k5.vrp")


Demo code
----------------------------

Get data
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
   

    # read instance
    data = read_cvrp_instances(instance_name,folder_data,type_instance)

In the first time, we read instance and get data with this attributes :

.. code-block:: python

        vehicle_capacity = 300
        nb_customers = 3
        cust_demands = [15,52,65]
        cust_coordinates = [[55.21,44.36],[54.31,65.23],[57.81,53.27]]
        depot_coordinates = [54.69,57.36]

.. note::
   You can also enumerate all feasible routes by changing the parameter action but this parameter works only for small instances ::

     model.parameters.action = "enumAllFeasibleRoutes"


Add vehicle type
^^^^^^^^^^^^^^^^^^^^^^
  .. code-block:: python

    # modelisation of problem
    model = solver.Model()

    # add vehicle type
    model.add_vehicle_type(id=1, #id cannot be less than 1
                           start_point_id=0,
                           end_point_id=0,
                           max_number=data.nb_customers,
                           capacity=data.vehicle_capacity,
                           var_cost_dist=1
                           )

.. note::
   You can also resolve an OVRP(Open Vehicle Routing Problem) problem if you put **start_point_id=-1** or **end_point_id=-1**.
   The characteristic of the OVRP problem is that the vehicle is not required to return to the depot.


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
                                          data.depot_coordinates[1],
                                          0)

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
                                              data.cust_coordinates[j][1],
                                              0)
            model.add_link(name="L" + str(nb_link),
                           start_point_id=i + 1,
                           end_point_id=j + 1,
                           distance=dist
                           )

            nb_link += 1
                     
    }

In this demo, we have only one vehicle type and the distances are computing by using eucledian distance.


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
.. _target to paragraph:

* The first command will print solution with an automatically printing function :

.. code-block:: python

   # print solution
   print(model.solution)

.. code-block:: python

    Route for vehicle 1:
    ID : 0 --> 30 --> 16 --> 1 --> 12 --> 0
    Load : 0.0 --> 14.0 --> 32.0 --> 51.0 --> 72.0 --> 72.0
    Total cost : 73.0

    Route for vehicle 1:
    ID : 0 --> 27 --> 24 --> 0
    Load : 0.0 --> 20.0 --> 44.0 --> 44.0
    Total cost : 59.0

    ...

* The second way will print manually solution like this :

.. code-block:: python

    if model.solution.is_defined :
        print(f"""Statistics :
        best lower bound : { model.statistics.best_lb } 
        
        solution time : {model.statistics.solution_time}
        
        solution value : {model.statistics.solution_value}

        root lower bound : {model.statistics.solution_value}

        root root time : {model.statistics.root_time}.
        """)
        print(f"Status : {model.status}.\n")
        print(f"Message : {model.message}.\n")   
        for route in model.solution.routes:            
            print(f"Vehicle Type id : {route.vehicle_type_id}.")
            print(f"Ids : {route.point_ids}.")
            print(f"Load : {route.cap_consumption}.\n")


.. code-block:: python

        Statistics :
            best lower bound : 784.0

            solution time : 1.1036816

            solution value : 784.0000000000484

            root lower bound : 784.0000000000484

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