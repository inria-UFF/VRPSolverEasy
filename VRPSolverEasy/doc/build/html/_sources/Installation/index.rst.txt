Installation
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


Installation with another solver
--------------------------------
 
After this steps, if you want to use another solver, you must 

* download library `here <https://bapcod.math.u-bordeaux.fr/>`_.

* find old library 
  
   *  `bapcod-shared.dll` (Windows) 
   *  `bapcod-shared.so` (Linux)
   *  `bapcod-shared.dylib` (MacOs)

* replace it by the newest 