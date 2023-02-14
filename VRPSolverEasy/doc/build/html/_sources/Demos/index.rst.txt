Demos
=========================================
.. toctree::
   :maxdepth: 1

If you want to use literature instances for testing the solver, you can 
find 3 files allow you to resolve variants VRP problem.


CVRPTW
------------------
The **cvrptw.py** file allows you to resolve **solomon** instances in the following format : 

* The first line indicates the name of instance.
* The fifth line gives the number of vehicles and the capacity. 
* From the 10th line, we have the following informations for each point of graph.

   * Index of point (0 correspond to the depot)
   * X coordinate
   * Y coordinate
   * Demand
   * Time windows begin
   * Time windows End
   * Service Time




CVRP
------------------
The **cvrp.py** file allows you to resolve **augerat** instances in the following format : 

* The first line indicates the name of the instance.
* The second line gives a comment about the data, for example, the optimal value expected.
* The third line gives the type of instance.
* The fourth line gives the dimension of the problem
* The fifth line indicates the technique used for calculating the distance between 2 points.
* the 6th line indicates the capacity of vehicle.  
* After the keyword *NODE_COORD_SECTION*, for each point, the following informations are given :

    * Index of point
    * X coordinate
    * Y coordinate  

After the keyword *DEMAND_SECTION*, for each point the following informations are given :
   
    * Index of point
    * Demand

After the keyword *DEPOT_SECTION*, we retrieve the index of depot.
   

HFVRP
------------------
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