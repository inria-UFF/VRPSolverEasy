
Installation 
=========================================

This is a guide to install VRPSolverEasy package.

.. note::
   See below how to install on Mac computers with Apple Silicon ARM processors.

Installation of free version
----------------------------

Free version uses COIN-OR CLP linear programming solver, embedded in the solver.

Requirements
^^^^^^^^^^^^^^

You must have installed version of Python >=3.6

If you have an old version of package setuptools, it's recommanded to upgrade version. You can
run this command line on terminal::

   python -m pip install --upgrade setuptools


Installation using pip
^^^^^^^^^^^^^^^^^^^^^^

You can run this command line::

   python -m pip install VRPSolverEasy


Installation using git
^^^^^^^^^^^^^^^^^^^^^^

- Download the package and extract it into a local directory
- Move to this local directory and enter::

   python -m pip install .

Installation for Apple Silicon ARM processors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

VRPSolverEasy comes with x86_64 BaPCod and VRPSolver libraries only. Therefore, Python for x86_64 architecture should be used with VRPSolverEasy. One way to do it is the following:

- install x86_64 version of Homebrew (see for example `here <https://medium.com/mkdir-awesome/how-to-install-x86-64-homebrew-packages-on-apple-m1-macbook-54ba295230f>`_ for instructions),
- install `python` package via x86_64 Homebrew: ::

   arch -x86_64 /usr/local/homebrew/bin/brew install python

- use :code:`/usr/local/homebrew/bin/python3` executable (or make an alias for it) to install VRPSolverEasy and to run Python code which uses VRPSolverEasy: ::

   /usr/local/homebrew/bin/python3 -m pip install VRPSolverEasy
   /usr/local/homebrew/bin/python3 VRPSolverEasy/demos/CVRP.py -i VRPSolverEasy/demos/data/CVRP/A-n32-k5.vrp

Installation of academic version 
---------------------------------

Academic version of VRPSolverEasy uses commercial CPLEX MIP solver, which can be obtained for free for academic purposes. This version has improved performance and provides a built-in (slow) MIP-based heuristic, which is useful for finding feasible solutions in the absence of an external heuristic solver. 

.. warning:: 
   Academic version is also free but requires an e-mail address from an academic institution to download BaPCod source code.
   If CPLEX is not installed in the default directory, we invite you to add the path to the dynamic libraries in the environment variables. 

To install this version, you must :

#. Clone VRPSolverEasy in your local machine
#. Install CPLEX
#. Download Bapcod source code on its `web page <https://bapcod.math.u-bordeaux.fr/>`_. 
#. Install Bapcod using installation instructions in the Bapcod  :download:`user guide <https://bapcod.math.u-bordeaux.fr/BaPCodUserGuide0.74.pdf>` .
#. Compile bapcod-shared library using this command :


.. code-block:: ruby

   cmake --build build --config Release --target bapcod-shared


This will produce the following shared library file:

.. code-block:: ruby

   "Bapcod-path/build/Bapcod/libbapcod-shared.so" // Linux
   "Bapcod-path/build/Bapcod/libbapcod-shared.dylib" // MacOs
   "Bapcod-path/build/Bapcod/Release/bapcod-shared.dll" // Windows

* Replace the old library inside the VRPSolverEasy folder **lib/your-system** by the newly produced one
  
   *  `libbapcod-shared.so` (Linux)
   *  `libbapcod-shared.dylib` (MacOs)
   *  `bapcod-shared.dll` (Windows) 


* re-install VRPSolverEasy using the command ::
  
      python -m pip install .
  

- Make sure to indicate :code:`solver_name='CPLEX'` when specifying VRPSolverEasy parameters.
- If you use Windows system, you have to indicate the path to CPLEX by specifying :code:`cplex_path='<path>'` in parameters.
- If you want to use build-in heuristic, indicate also :code:`heuristic_used=True` in parameters.