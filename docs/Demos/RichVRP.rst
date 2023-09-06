RichVRP
=========

The RichVRP is a demo that combines multiple elements supported by VRPSolverEasy. It has open routes, multiple depots, multiple time windows, two types of vehicles (small and big), optional customers, and incompatible vehicles (some customers can be served only by small vehicles).
 
Instance format
----------------------------

The demo reads instances in the following format\:

.. code-block:: text

   <M> # Number of depots
   0 <xCoordDepot0> <yCoordDepot0> <beginTwDepot0> <endTwDepot0>
   ...
   M-1 <xCoordDepotM-1> <yCoordDepotM-1> <beginTwDepotM-1> <endTwDepotM-1>
   <bigVehicleCapacity> <bigVehicleFixedCost> <bigVehicleVariableCost> <bigVehicleMaxNumber>
   <smallVehicleCapacity> <smallVehicleFixedCost> <smallVehicleVariableCost> <smallVehicleMaxNumber>
   <N> # Number of customers
   M <xCoordCustomerM> <yCoordCustomerM> <beginTwCustomerM> <endTwCustomerM>
   ...
   M+N-1 <xCoordCustomerM+N-1> <yCoordCustomerM+N-1> <beginTwCustomerM+N-1> <endTwCustomerM+N-1>

For example, the example instance at demos/data/RichVRP/toy.txt has the following content\:

.. code-block:: text

   2
   0 0 0 0 1000
   1 100 100 0 500
   200 400 3.2 1
   50 20 1.0 4
   6
   2 5 15 35 50 0 1 1 20 100
   3 5 25 15 50 1 1 1 0 100
   4 15 15 100 50 0 0 1 180 250
   5 75 60 20 50 0 1 3 0 100 200 300 400 500
   6 50 50 80 50 0 0 1 80 130
   7 35 75 30 50 0 0 2 0 50 500 600

which is read as follows\:

.. code-block:: text

   Depots:
   Depot(id: 0, x: 0, y: 0, tw_begin: 0, tw_end: 1000)
   Depot(id: 1, x: 100, y: 100, tw_begin: 0, tw_end: 500)

   Big Vehicle:
   Vehicle(capacity: 200, fixed_cost: 400, var_cost: 3.2, max_number: 1)

   Small Vehicle:
   Vehicle(capacity: 50, fixed_cost: 20, var_cost: 1.0, max_number: 4)

   Customers:
   Customer(id: 2, x: 5, y: 15, demand: 35, service_time: 50, optional: False, only_small_veh: True, time_windows: [(20, 100)])
   Customer(id: 3, x: 5, y: 25, demand: 15, service_time: 50, optional: True, only_small_veh: True, time_windows: [(0, 100)])
   Customer(id: 4, x: 15, y: 15, demand: 100, service_time: 50, optional: False, only_small_veh: False, time_windows: [(180, 250)])
   Customer(id: 5, x: 75, y: 60, demand: 20, service_time: 50, optional: False, only_small_veh: True, time_windows: [(0, 100), (200, 300), (400, 500)])
   Customer(id: 6, x: 50, y: 50, demand: 80, service_time: 50, optional: False, only_small_veh: False, time_windows: [(80, 130)])
   Customer(id: 7, x: 35, y: 75, demand: 30, service_time: 50, optional: False, only_small_veh: False, time_windows: [(0, 50), (500, 600)])

Run instances
----------------------------

You can solve an instance by specifying different parameters directly in the command line, like this::

   python RichVRP.py -i <instance path> -t <time limit> -s <solver_name>

CPLEX solver can be used only with the :doc:`academic version </Installation/index>`. When using CPLEX solver on a Windows computer, one should give its path: :code:`-p <path to CPLEX>`.

Demo code
----------------------------

Get data and create the model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
 
   data = read_richvrp_instance(instance_name)
   model = solver.Model()

``data`` is an object of class ``DataRichVrp`` that keeps a list of objects from classes ``Depot``, ``Vehicle``, and ``Customer``.

Add depots and vehicle types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We define two types of vehicles—big and small—for each depot.
Each type of vehicle is characterized by the depot from which it starts its route.
We use odd indexes for big vehicles and even indexes for small vehicles.
Note that the ``end_point_id`` is set to -1 for these vehicle types, as we are requesting open routes.
Additionally, all vehicle types share the same time window from their respective starting depots.

.. code-block:: python

    big_vehicle_id = 1 # Big vehicles have odd ids
    big_vehicle_ids = [] # Store all the ids for big vehicles
    small_vehicle_id = 2 # Small vehicles have even ids
    # Add depots and vehicles
    for depot in data.depots:
        # Add the depot
        model.add_depot(id = depot.id,
                        tw_begin = depot.tw_begin,
                        tw_end = depot.tw_end)
        # Add the big vehicle to this depot
        model.add_vehicle_type(id = big_vehicle_id,
                                start_point_id = depot.id,
                                end_point_id = -1, # A vehicle may end anywhere 
                                capacity = data.big_vehicle.capacity,
                                max_number = data.big_vehicle.max_number,
                                fixed_cost = data.big_vehicle.fixed_cost,
                                var_cost_dist = data.big_vehicle.var_cost,
                                tw_begin = depot.tw_begin,
                                tw_end = depot.tw_end)
        # Add the small vehicle to this depot
        model.add_vehicle_type(id = small_vehicle_id,
                                start_point_id = depot.id,
                                end_point_id = -1, # A vehicle may end anywhere 
                                capacity = data.small_vehicle.capacity,
                                max_number = data.small_vehicle.max_number,
                                fixed_cost = data.small_vehicle.fixed_cost,
                                var_cost_dist = data.small_vehicle.var_cost,
                                tw_begin = depot.tw_begin,
                                tw_end = depot.tw_end)
        big_vehicle_ids.append(big_vehicle_id)
        big_vehicle_id += 2
        small_vehicle_id += 2

Add customers
^^^^^^^^^^^^^

.. code-block:: python

    # ID for alternative points of a customer with multiple time windows
    next_id = max([customer.id for customer in data.customers]) + 1
    # IDs of a customer, including the alternative ones
    customer_ids = {customer.id : [customer.id] for customer in data.customers}
    # Add customers
    for customer in data.customers:
        # Add a point for each time window of a customer
        for i, tw in enumerate(customer.time_windows):
            point_id = customer.id
            if i > 0: # Is it an alternative point?
                point_id = next_id
                customer_ids[customer.id].append(next_id)
                next_id += 1 # Get the next alternative ID
            model.add_customer(id = point_id,
                                id_customer = customer.id,
                                demand = customer.demand,
                                service_time = customer.service_time,
                                tw_begin = tw[0],
                                tw_end = tw[1],
                                penalty = 1.0 if customer.optional else 0.0,
                                incompatible_vehicles = big_vehicle_ids if customer.only_small_veh else [])
.. note::
  Given the instance format, the IDs of depots and customers will never overlap (which is not allowed by VRPSolverEasy). 

Add links
^^^^^^^^^^^^^^^^^^^^^^ 

.. code-block:: python

    # Compute the links between depots and other points
    for depot in data.depots:
        for customer in data.customers:
            dist = compute_euclidean_distance(customer.x, customer.y, depot.x, depot.y)
            for point_id in customer_ids[customer.id]:
                model.add_link(start_point_id = depot.id,
                                end_point_id = point_id,
                                distance = dist,
                                time = dist)
                
    # Compute the links between customer points
    for i, c1 in enumerate(data.customers):
        for j, c2 in enumerate(data.customers):
            if j <= i:
                continue
            dist = compute_euclidean_distance(c1.x, c1.y, c2.x, c2.y)
            # Add a link for each pair of points from c1 to c2
            for point_id_c1 in customer_ids[c1.id]:
                for point_id_c2 in customer_ids[c2.id]:
                    model.add_link(start_point_id = point_id_c1,
                                    end_point_id = point_id_c2,
                                    distance = dist,
                                    time = dist)

Set parameters
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   model.set_parameters(time_limit=time_resolution,
                        solver_name=solver_name_input)
                   
Solve model
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  model.solve()

Print solution
^^^^^^^^^^^^^^^^^^^^^^

To understand the solution, we need the alternative IDs and their time windows for each customer\:

.. code-block:: python

   print("\nCustomer IDs and time windows:")
   for customer in data.customers:
       ids_and_tws = []
       for i, point_id in enumerate(customer_ids[customer.id]):
           ids_and_tws.append(f"(id: {point_id}, tw: {list(customer.time_windows[i])})")
       print(f"Customer {customer.id}: {', '.join(ids_and_tws)}")

So, you can print the solution using the :code:`print()` function

.. code-block:: python

   if (model.solution.is_defined())
       print(model.solution)

For the toy instance, it produces\:

.. code-block:: text

    Customer IDs and time windows:
    Customer 2: (id: 2, tw: [20, 100])
    Customer 3: (id: 3, tw: [0, 100])
    Customer 4: (id: 4, tw: [180, 250])
    Customer 5: (id: 5, tw: [0, 100]), (id: 8, tw: [200, 300]), (id: 9, tw: [400, 500])
    Customer 6: (id: 6, tw: [80, 130])
    Customer 7: (id: 7, tw: [0, 50]), (id: 10, tw: [500, 600])

    Solution cost : 980.2435999992152 
    
    Route for vehicle 2:
    ID : 0 --> 8 --> 10
    End time : 0.0 --> 250.0 --> 550.0
    Load : 0.0 --> 20.0 --> 50.0
    Total cost : 158.767
    
    Route for vehicle 2:
    ID : 0 --> 2
    End time : 0.0 --> 70.0
    Load : 0.0 --> 35.0
    Total cost : 35.811
    
    Route for vehicle 3:
    ID : 1 --> 6 --> 4
    End time : 0.0 --> 130.0 --> 230.0
    Load : 0.0 --> 80.0 --> 180.0
    Total cost : 784.6656

You can also analyze the solution manually by retrieving each route. For example, consult the last section of the demo :doc:`/Demos/CVRP`.
