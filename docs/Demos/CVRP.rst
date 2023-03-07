CVRP
================

If you want to use literature instances for testing the solver, you can 
find 3 files allow you to resolve variants VRP problem.

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
   
