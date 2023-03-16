Important notes
======================================



Improve performances
------------------

You can improve the performance of the solver if you set the upper bound parameter : ::
        
        model.parameters.upper_bound

Before using the VRPSolverEasy package, you can start by generating an upper bound using an external package.
Here's a list of python packages than you can use for compute a upper bound :

    * `or-tools <https://developers.google.com/optimization/install/python>`_
    * `pyVRP <https://github.com/N-Wouda/PyVRP>`_
    * `pyHegese <https://github.com/chkwon/PyHygese>`_
  
You can also use CPLEX in academic version and the internal heuristic to improve results.
For up to 100 customer, the VRPSolverEasy package computes very fast but after 200 customers, it can get slow to resolve instances. 


Debug 
------------------

If you have trouble solving your problems, you can :

* Check the compatibility of your system and your Python (VRPSolverEasy works only in x64 architecture with Python >= 3.7)
* If it's compatible, you can check your model by exporting it like this::
  
        model.export(instanceName)
  
* If there is no problem in the model, you can reduce the instance by putting a very low number of points and running the enumeration of all feasible solutions::

        model.parameters.action = "enumAllFeasibleRoutes"  
  
* If the enumeration is infeasible, you can send us the exported model by mail and we will respond to you as soon as possible.