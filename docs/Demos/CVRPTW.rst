CVRPTW
=======
CVRPTW (Capacitated Vehicle Routing Problem with Time Windows) is a variant of the classical Vehicle Routing Problem (VRP) in which a fleet of vehicles with limited capacities is assigned to serve a set of customers with specific demands and time windows, subject to various constraints

Instance formats
----------------------------

The **cvrptw.py** file allows you to resolve **solomon** instances in the following format : 

* The first line indicates the name of instance.
* The fifth line gives the number of vehicles and the capacity. 
* From the 10th line, we have the following informations for each point of graph.

   * Index of the point (0 corresponds to the depot)
   * X coordinate
   * Y coordinate
   * Demand
   * Time windows begin
   * Time windows End
   * Service Time

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
You can modify the demo directly in the file **CVRPTW.py**, which is included in the folder demos. You can go to the bottom of the file, uncomment, and update this line::
    
    solve_demo("R101.txt")


Demo code
----------------------------

Get data
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
   

    # read instance
    data = read_cvrptw_instances(instance_name,folder_data,type_instance)

In the first time, we read the instance and get data with these attributes :

.. code-block:: python

        vehicle_capacity = 300
        max_number = 2 #maximum number of vehicles
        nb_customers = 3       
        cust_demands = [15,52,65]
        cust_coordinates = [[55.21,44.36],[54.31,65.23],[57.81,53.27]]
        depot_coordinates = [54.69,57.36]
        depot_service_time = 0
        depot_tw_end = 1
        depot_tw_begin = 5
        cust_tw_begin = [2,3,5]
        cust_tw_end = [4,8,10]
        cust_service_time = [1,1,1.3]

Add vehicle types
^^^^^^^^^^^^^^^^^^^^^^
  .. code-block:: python

    # add vehicle type
    model.add_vehicle_type(id=1,
                           start_point_id=0,
                           end_point_id=0,
                           max_number=data.max_number,
                           capacity=data.vehicle_capacity,
                           tw_begin=data.depot_tw_begin,
                           tw_end=data.depot_tw_end,
                           var_cost_dist=1
                           )

Here, the start point id and the end point id = 0 because we have only one depot from which all the vehicles start and return.

Add depot and customers 
^^^^^^^^^^^^^^^^^^^^^^^^  

.. code-block:: python

    # add depot
    model.add_depot(id=0,
                    service_time=data.depot_service_time,
                    tw_begin=data.depot_tw_begin,
                    tw_end=data.depot_tw_end
                    )

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i + 1,
                           service_time=data.cust_service_time[i],
                           tw_begin=data.cust_tw_begin[i],
                           tw_end=data.cust_tw_end[i],
                           demand=data.cust_demands[i]
                           )

.. note::
   If want to put an optional customer you can add penalty parameter > 0.
        .. code-block:: python
           :emphasize-lines: 7

            # add an optional customers
                model.add_customer(id=3,
                                service_time=data.cust_service_time[i],
                                tw_begin=data.cust_tw_begin[i],
                                tw_end=data.cust_tw_end[i],
                                demand=data.cust_demands[i]
                                penalty = 5
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
                                          data.depot_coordinates[1]
                                          )
        model.add_link(name="L" + str(nb_link),
                       start_point_id=0,
                       end_point_id=i + 1,
                       distance=dist,
                       time=dist
                       )
        nb_link += 1

    # Compute the links between points
    for i,cust_i in enumerate(data.cust_coordinates):
        for j in range(i + 1, len(data.cust_coordinates)):
            dist = compute_euclidean_distance(cust_i[0],
                                              cust_i[1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1]
                                              )
            model.add_link(name="L" + str(nb_link),
                           start_point_id=i + 1,
                           end_point_id=j + 1,
                           distance=dist,
                           time=dist
                           )

            nb_link += 1
                     
    }

.. note::
   You can also define parallel arcs in the graph, this can be useful if 2 arcs do not have the same time or the same cost.
   This makes the model more complex while getting closer to a realistic model.

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

You can print the solution with an automatic printing function :

.. code-block:: python

   # print solution
   print(model.solution)

or you can print manually each route, to do this, we invite you to consult the last section of the demo :doc:`/Demos/CVRP` 