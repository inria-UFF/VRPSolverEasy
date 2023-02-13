Free Installation
=========================================

This is a guide to install VRPSolverEasy package.
If you work on *Windows*, you can run the same commands without sudo

Requirements
------------------

You must have installed version of Python >=3.7

If you have an old version of package setuptools(*Linux* or *MacOs*), it's recommanded to upgrade version. you can
run this command line on terminal::

   sudo python -m pip install --upgrade setuptools



Installation using pip
----------------------

you can run this command line (*Linux* or *MacOs*)::

   sudo python -m pip install VRPSolverEasy

*Windows*::

   python -m pip install VRPSolverEasy


Installation using git
----------------------

- Download the package and extract it into a local directory
- (*Linux* or *MacOs*) Move to this local directory and enter::

   sudo python -m pip install .


Academic Installation using CPLEX
=========================================
 
If you want to use another solver, you must :

  
* Download Bapcod source code on its `web page <https://bapcod.math.u-bordeaux.fr/>`_. Then request the RCSP (resource constrained shortest path) compiled library from Ruslan.Sadykov@inria.fr. 
* Please specify your OS in your request. 
* Install Bapcod together with the RCSP library using installation instructions in the Bapcod user guide.
* Install CPLEX
   
Then run the following command from the folder you have installed Bapcod.

.. code-block:: ruby

   cmake --build build --config Release --target bapcod-shared


This will produce shared library file in :

.. code-block:: ruby

   "Bapcod-path/build/Bapcod/libbapcod-shared.so" // Linux
   "Bapcod-path/build/Bapcod/libbapcod-shared.dylib" // MacOs
   "Bapcod-path/build/Bapcod/Release/bapcod-shared.dll" // Windows

Note that if you use windows system, you have to indicates the cplex path in Parameters.

* Replace the old library in the folder **lib/your-system** by the newest
  
   *  `bapcod-shared.dll` (Windows) 
   *  `libbapcod-shared.so` (Linux)
   *  `libbapcod-shared.dylib` (MacOs)

* re-run installation using pip