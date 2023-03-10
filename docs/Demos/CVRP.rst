CVRP
================


Instance formats
----------------------------

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

In the first time, we read instance and get data in this format :

.. code-block:: python

    {
        #TODO
                    
    }

In this demo, we have only one vehicle type and the distances are computing by using eucledian distance.


Modelisation
^^^^^^^^^^^^^^^^^^^^^^

#TODO


