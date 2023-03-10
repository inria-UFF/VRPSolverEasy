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



.. list-table:: solution.status
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
       
  

Route
-----------

.. autoclass:: Route
    :members:
    :member-order:
    :special-members:




