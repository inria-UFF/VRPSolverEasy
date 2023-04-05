CVRPTW
=======
The capacitated vehicle routing problem with time windows (CVRPTW) is a variant of the CVRP in which each customer has a time window during which it should be visited. 

Instances format
----------------------------

The demo reads instances in the standard Solomon format.

* The first line indicates the name of instance.
* The fifth line gives the number of vehicles and the capacity. 
* From the 10th line, we have the following information for each point of graph:

   * Index of the point (0 corresponds to the depot)
   * X coordinate
   * Y coordinate
   * Demand
   * Time window begin
   * Time window end
   * Service time

Run instances
----------------------------
There are two ways to run a specific instance:

Command line
^^^^^^^^^^^^^^^^^^^^^^

After the installation, you can run an instance by specifying different parameters directly in the command line, like this::

    python CVRPTW.py -i <instance path> -t <time limit> -s <solver_name>

CPLEX solver can be used only with the :doc:`academic version </Installation/index>`. When using CPLEX solver on a Windows computer, one should give its path: :code:`-p <path to CPLEX>`.


Python file
^^^^^^^^^^^^^^^^^^^^^^

You can specify the instance name directly in the demo file **CVRPTW.py**, by uncommenting the last line::
    
    solve_demo("R101.txt")


Demo code
----------------------------

Get data
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
   

    # read instance
    data = read_cvrptw_instance(instance_name,folder_data)

An example of the contents of :code:`data` :

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

Add vehicle type
^^^^^^^^^^^^^^^^
  .. code-block:: python

    # create model
    model = solver.Model()

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

As there is only one depot with id 0, the vehicle start and end in the point with id 0.

Add depot and customers 
^^^^^^^^^^^^^^^^^^^^^^^^  

.. code-block:: python

    # add depot
    model.add_depot(id=0,
                    service_time=data.depot_service_time,
                    tw_begin=data.depot_tw_begin,
                    tw_end=data.depot_tw_end)

    # add all customers
    for i in range(data.nb_customers):
        model.add_customer(id=i + 1,
                           service_time=data.cust_service_time[i],
                           tw_begin=data.cust_tw_begin[i],
                           tw_end=data.cust_tw_end[i],
                           demand=data.cust_demands[i])

.. note::
   If want to put an optional customer you can specify a positive :code:`penalty` attribute:

    .. code-block:: python
        :emphasize-lines: 7

        # add an optional customers
        model.add_customer(id=3,
                           service_time=data.cust_service_time[i],
                           tw_begin=data.cust_tw_begin[i],
                           tw_end=data.cust_tw_end[i],
                           demand=data.cust_demands[i]
                           penalty = 5)

Add links
^^^^^^^^^

.. code-block:: python


    # Compute the links between depot and other points
    for i,cust_i in enumerate(data.cust_coordinates):
        dist = compute_euclidean_distance(cust_i[0],
                                          cust_i[1],
                                          data.depot_coordinates[0],
                                          data.depot_coordinates[1])
        model.add_link(start_point_id=0,
                       end_point_id=i + 1,
                       distance=dist,
                       time=dist)

    # Compute the links between points
    for i,cust_i in enumerate(data.cust_coordinates):
        for j in range(i + 1, len(data.cust_coordinates)):
            dist = compute_euclidean_distance(cust_i[0],
                                              cust_i[1],
                                              data.cust_coordinates[j][0],
                                              data.cust_coordinates[j][1])
            model.add_link(start_point_id=i + 1,
                           end_point_id=j + 1,
                           distance=dist,
                           time=dist)

    }

.. note::
   You can define parallel links between the same pair of customers or between a customer and a depot. This my be useful if there is a trade-off between traveling time and distance.

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