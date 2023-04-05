Important notes
===============

Solver performance
------------------

The solver is focused on improving **lower bounds** and **proving optimality** of a known feasible solution. Feasible solutions are obtained only when the solution of the linear programming (LP) relaxation becomes integer (after addition cuts and branching). Performance of the solver may be greatly improved by setting the upper bound parameter to the value of a known feasible solution::
        
        model.parameters.upper_bound = <known_feasible_solution_value>

The better is the known feasible solution, the better will be performance of the solver. Thus, we advice to run a (good) external heuristic before launching the solver. Here's a list of Python packages we are aware of, which can be useful for computing an upper bound :

    * `OR-Tools <https://developers.google.com/optimization/install/python>`_
    * `pyVRP <https://github.com/N-Wouda/PyVRP>`_
    * `pyHegese <https://github.com/chkwon/PyHygese>`_
    * `vrp-cli <https://github.com/reinterpretcat/vrp>`_
  
When using the academic version of VRPSolverEasy, one can activate the built-in MIP-based heuristic. However, this heuristic is slow (launched the first time only at the end of the root node). Moreover, the performance of this heuristic may be not good for large instances and instances with long routes. 

One can reasonably expect to solve to optimality instances with up to 100 customers. Sometimes, optimal or good solutions may be found for instances with 200-250 customers, usually in long runs. 

Issues and debugging 
--------------------

If the output of the solver is not as expected, you may need to verify that your model is correct for your instances. For that, you can use enumeration feature of the solver. To use this feature, take a very small instance (up to 5-10 customers), and activate the solver enumeration mode::

        model.parameters.action = "enumAllFeasibleRoutes"  
  
In this mode, the solver will return all feasible routes for your instance (or inform you that no feasible route exists). You then may analyze the routes to check whether your model is correct.   

If the solution status of the model is non-negative, then unexpected results generally come from non-correct model. If the solution status is negative then there might be an issue with the solver. 

To report an issue, you should export you model into a JSON file::

        model.export(<JSON file name>)

and then open an issue on the `VRPSolverEasy Github repository <https://github.com/inria-UFF/VRPSolverEasy>`_ with the JSON file attached. 

Accompanying paper
------------------

The paper presents the motivation to create VRPSolverEasy, the interface of 
the package, the solution approach (optional to read), the computational 
results for the three classic VRP variants (CVRP, VRPTW, HFVRP), and possible
future extensions of the model. 
For the moment, the paper is available as a preprint :
    
    \N. Errami, E. Queiroga, R. Sadykov, E. Uchoa. "VRPSolverEasy: a Python 
    library for the exact solution of a rich vehicle routing problem", 
    `Technical report HAL-04057985 <https://hal.inria.fr/hal-04057985/document>`__, 2023.

Please cite it if you use VRPSolverEasy in your research.
