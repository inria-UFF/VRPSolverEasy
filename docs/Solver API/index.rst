:mod:`src`:  solver API
=====================================
 
.. automodule:: src.solver


.. currentmodule:: src.solver

.. autosummary::
    Model
    Point
    Customer
    Depot
    Link
    VehicleType
    Parameters
    Solution
    Route


Model
-----------

.. autoclass:: Model
    :members:
    :member-order:

After you finish solving, you can find the status of the model and know whether you have reached optimality or not using the status attribute.

.. list-table:: model.status
   :widths: 25 25 
   :header-rows: 1

   * - Status
     - numerical value
   * - :data:`INFEASIBLE` 
     - -2
   * - :data:`INTERRUPTED_BY_ERROR`
     - -1
   * - :data:`OPTIMAL_SOL_FOUND` 
     - 0 
   * - :data:`BETTER_SOL_FOUND`
     - 1 
   * - :data:`BETTER_SOL_DOES_NOT_EXISTS` 
     - 2
   * - :data:`BETTER_SOL_NOT_FOUND` 
     - 3    

If you change the parameters to run an enumeration of all feasible solutions, the interpretation of status is different : 

.. list-table:: model.status
   :widths: 25 25 
   :header-rows: 1

   * - Status
     - numerical value
   * - :data:`ENUMERATION_SUCCEEDED` 
     - 0
   * - :data:`ENUMERATION_NOT_SUCCEEDED`
     - 1
   * - :data:`ENUMERATION_INFEASIBLE` 
     - 2 



Point
-----------

.. autoclass:: Point
    :members:
    :member-order:
    :special-members:

Customer
-----------

.. autoclass:: Customer
    :members:
    :member-order:
    :special-members:

Depot
-----------

.. autoclass:: Depot
    :members:
    :member-order:
    :special-members:

Link
-----------

.. autoclass:: Link
    :members:
    :member-order:
    :special-members:

VehicleType
-----------

.. autoclass:: VehicleType
    :members:
    :member-order:
    :special-members:

Parameters
-----------

.. autoclass:: Parameters
    :members:
    :member-order:
    :special-members:

Solution
-----------

.. autoclass:: Solution
    :members:
    :member-order:
    :special-members:



Statistics 
-----------

.. autoclass:: Statistics
    :members:
    :member-order:
    :special-members:
       
  

Route
-----------

.. autoclass:: Route
    :members:
    :member-order:
    :special-members:




