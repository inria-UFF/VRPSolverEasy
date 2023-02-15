
Installation 
=========================================

This is a guide to install VRPSolverEasy package.

Installation of free version
----------------------------

Free version uses third-party COIN-OR CLP linear programming solver which is included in VRPSolverEasy.

Requirements
^^^^^^^^^^^^^^

You must have installed version of Python >=3.7

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
- (*Linux* or *MacOs*) Move to this local directory and enter::

   sudo python -m pip install .


Installation of academic version 
---------------------------------

Academic version of VRPSolverEasy has better performance and comes with the possibility to use built-in heuristic.
This version uses commercial CPLEX mixed integer programming solver which can be obtained for free for academic purposes.

To install this version, you must :

#. Clone VRPSolverEasy in your local machine
#. Install CPLEX
#. Download Bapcod source code on its `web page <https://bapcod.math.u-bordeaux.fr/>`_. 
#. Install Bapcod using installation instructions in the Bapcod user guide.
#. Compile bapcod-shared library using this command :


.. code-block:: ruby

   cmake --build build --config Release --target bapcod-shared


This will produce shared library file in :

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
  

- Make sure that you have changed `solver_name` in `Parameters` if you want to use CPLEX.
- Note that if you use windows system, you have to indicates the cplex path in Parameters.