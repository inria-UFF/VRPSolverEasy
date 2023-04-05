"""This module solves vehicle routing problems using branch&cut&price methods"""

import ctypes as _c
import json
import platform
import os
import sys
from VRPSolverEasy.src import constants
if sys.version_info > (3, 7):
    import collections.abc as collections
else:
    import collections

########
__version__ = "0.1.2"
__author__ = "Najib ERRAMI Ruslan SADYKOV Eduardo UCHOA Eduardo QUEIROGA"
__copyright__ = "Copyright VRPYSolver, all rights reserved"
__email__ = "najib.errami@inria.fr"


class PropertyError(Exception):
    """Exception raised for errors in the input property.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, prefix=str(), code=0, str_list=""):
        self.message = prefix + constants.ERRORS_PROPERTY[code] + str_list
        super().__init__(self.message)


class ModelError(Exception):
    """ Exception raised for errors in the model.

    Attributes:
        message -- explanation of the error
   """

    def __init__(self, code=0):
        self.message = constants.ERRORS_MODEL[code]
        super().__init__(self.message)


class VehicleTypesDict(dict,collections.MutableMapping):
    """Dictionary of vehicle types

    key (int): Id of vehicle type
    value: class Vehicle type

    """

    def __getitem__(self, key):
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if not isinstance(key, (int)):
            raise PropertyError(constants.KEY_STR, constants.INTEGER_PROPERTY)
        if not isinstance(value, (VehicleType)):
            raise PropertyError(str(), constants.VEHICLE_TYPE_PROPERTY)
        if value.id != key:
            raise PropertyError(str(), constants.DICT_PROPERTY)
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)

    def __iter__(self):
        return dict.__iter__(self)

    def __len__(self):
        return dict.__len__(self)

    def __contains__(self, x):
        return dict.__contains__(self, x)

    def values(self, debug=False):
        if len(dict.values(self)) == 0:
            raise ModelError(constants.MIN_VEHICLE_TYPES_ERROR)
        return list(value.get_vehicle_type(debug)
                    for value in dict.values(self))


class PointsDict(dict,collections.MutableMapping):
    """Dictionary of points ( depots and customers)

    key (int): Id of point
    value: class Customer or Depot

    """

    def __getitem__(self, key):
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if not isinstance(key, (int)):
            raise PropertyError(constants.KEY_STR, constants.INTEGER_PROPERTY)
        if not isinstance(value, (Point)):
            raise PropertyError(str(), constants.POINT_PROPERTY)
        if value.id != key:
            raise PropertyError(str(), constants.DICT_PROPERTY)
        if dict.__len__(self) + 1 > 1022:
            raise PropertyError(
                constants.NB_POINTS_STR,
                constants.LESS_MAX_POINTS_PROPERTY)
        dict.__setitem__(self, key, value)

            
    def __delitem__(self, key):
        dict.__delitem__(self, key)

    def __iter__(self):
        return dict.__iter__(self)

    def __len__(self):
        return dict.__len__(self)

    def __contains__(self, x):
        return dict.__contains__(self, x)

    def values(self, debug=False):
        if len(dict.values(self)) == 0:
            raise ModelError(constants.MIN_POINTS_ERROR)
        return list(value.get_point(debug) for value in dict.values(self))


class LinksDict(dict,collections.MutableMapping):
    """Dictionary of links

    key (str): name of link
    value: class Customer or Depot

    """

    def __getitem__(self, key):
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if not isinstance(value, list):
            raise ModelError(constants.ADD_LINK_ERROR)
        for i in value:
            if not isinstance(i,Link):
                raise PropertyError(str(), 12)
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)

    def __iter__(self):
        return dict.__iter__(self)

    def __len__(self):
        return dict.__len__(self)

    def __contains__(self, x):
        return dict.__contains__(self, x)

    def values(self, debug=False):
        if len(dict.values(self)) == 0:
            raise ModelError(constants.MIN_LINKS_ERROR)
        return list(value.get_link(debug) for list_ in dict.values(self) for value in list_ )


class VehicleType:
    """Define a vehicle type with different attributes.
    """

    def __init__(
            self,
            id: int,
            start_point_id=-1,
            end_point_id=-1,
            name=str(),
            capacity=0,
            fixed_cost=0.0,
            var_cost_dist=0.0,
            var_cost_time=0.0,
            max_number=1,
            tw_begin=0,
            tw_end=0):
        self.name = name
        self.id = id
        self.capacity = capacity
        self.fixed_cost = fixed_cost
        self.var_cost_dist = var_cost_dist
        self.var_cost_time = var_cost_time
        self.max_number = max_number
        self.start_point_id = start_point_id
        self.end_point_id = end_point_id
        self.tw_begin = tw_begin
        self.tw_end = tw_end

    # a getter function of id
    @property
    def id(self):
        """int : cannot be less than 1 """
        return self._id

    # a setter function of id
    @id.setter
    def id(self, id):
        if not isinstance(id, (int)):
            raise PropertyError(constants.ID_STR, constants.INTEGER_PROPERTY)
        if id < 1:
            raise PropertyError(
                constants.ID_STR,
                constants.GREATER_ONE_PROPERTY)
        self._id = id

    @property
    def name(self):
        """str : name of vehicle type"""
        return self._name

    @name.setter
    def name(self, name):
        """setter function of name"""
        if not isinstance(name, (str)):
            raise PropertyError(constants.VEHICLE_TYPE.NAME.value,
                                constants.STRING_PROPERTY)
        self._name = name

    @property
    def capacity(self):
        """--int : capacity of vehicle type"""
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """setter function of capacity"""
        if not isinstance(capacity, (int)):
            raise PropertyError(constants.VEHICLE_TYPE.CAPACITY.value,
                                constants.INTEGER_PROPERTY)
        if capacity < 0:
            raise PropertyError(constants.VEHICLE_TYPE.CAPACITY.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._capacity = capacity

    @property
    def fixed_cost(self):
        """float : fixed cost of using vehicle type"""
        return self._fixed_cost

    @fixed_cost.setter
    def fixed_cost(self, fixed_cost):
        """setter function of fixed_cost"""
        if not isinstance(fixed_cost, (int, float)):
            raise PropertyError(constants.VEHICLE_TYPE.FIXED_COST.value,
                                constants.NUMBER_PROPERTY)
        self._fixed_cost = fixed_cost

    @property
    def var_cost_dist(self):
        """variable cost per unit of distance
           :type var_cost_dist : float : """
        return self._var_cost_dist

    @var_cost_dist.setter
    def var_cost_dist(self, var_cost_dist):
        """setter function of var_cost_dist"""
        if not isinstance(var_cost_dist, (int, float)):
            raise PropertyError(constants.VEHICLE_TYPE.VAR_COST_DIST.value,
                                constants.NUMBER_PROPERTY)
        self._var_cost_dist = var_cost_dist

    @property
    def var_cost_time(self):
        """variable cost per unit of time"""
        return self._var_cost_time

    @var_cost_time.setter
    def var_cost_time(self, var_cost_time):
        """setter function of var_cost_time"""
        if not isinstance(var_cost_time, (int, float)):
            raise PropertyError(constants.VEHICLE_TYPE.VAR_COST_TIME.value,
                                constants.NUMBER_PROPERTY)
        self._var_cost_time = var_cost_time

    # a getter function of max_number
    @property
    def max_number(self):
        """number of vehicles available"""
        return self._max_number

    @max_number.setter
    def max_number(self, max_number):
        """setter function of max_number"""
        if not isinstance(max_number, (int)):
            raise PropertyError(constants.VEHICLE_TYPE.MAX_NUMBER.value,
                                constants.INTEGER_PROPERTY)
        if max_number < 0:
            raise PropertyError(constants.VEHICLE_TYPE.MAX_NUMBER.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._max_number = max_number

    @property
    def start_point_id(self):
        """the id of the starting point"""
        return self._start_point_id

    @start_point_id.setter
    def start_point_id(self, start_point_id):
        """setter function of start_point_id"""
        if not isinstance(start_point_id, (int)):
            raise PropertyError(constants.VEHICLE_TYPE.START_POINT_ID.value,
                                constants.INTEGER_PROPERTY)
        if start_point_id < -1:
            raise PropertyError(constants.VEHICLE_TYPE.START_POINT_ID.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._start_point_id = start_point_id

    @property
    def end_point_id(self):
        """the id of the end point"""
        return self._end_point_id

    @end_point_id.setter
    def end_point_id(self, end_point_id):
        """setter function of end_point_id"""
        if not isinstance(end_point_id, (int)):
            raise PropertyError(constants.VEHICLE_TYPE.END_POINT_ID.value,
                                constants.INTEGER_PROPERTY)
        if end_point_id < -1:
            raise PropertyError(constants.VEHICLE_TYPE.END_POINT_ID.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._end_point_id = end_point_id

    @property
    def tw_begin(self):
        """time windows begin of vehicle type"""
        return self._tw_begin

    @tw_begin.setter
    def tw_begin(self, tw_begin):
        """setter function of tw_begin"""
        if not isinstance(tw_begin, (int, float)):
            raise PropertyError(
                constants.VEHICLE_TYPE.TIME_WINDOWS_BEGIN.value,
                constants.NUMBER_PROPERTY)
        self._tw_begin = tw_begin

    @property
    def tw_end(self):
        """time windows end of vehicle type"""
        return self._tw_end

    @tw_end.setter
    def tw_end(self, tw_end):
        """setter function of tw_end"""
        if not isinstance(tw_end, (int, float)):
            raise PropertyError(
                constants.VEHICLE_TYPE.TIME_WINDOWS_END.value,
                constants.NUMBER_PROPERTY)
        self._tw_end = tw_end

    def get_vehicle_type(self, debug=False):
        """Get all components of a vehicle type which are differents of
        default value"""
        veh_type = {}
        veh_type[constants.VEHICLE_TYPE.ID.value] = self.id
        veh_type[constants.VEHICLE_TYPE.
                 START_POINT_ID.value] = self.start_point_id
        veh_type[constants.VEHICLE_TYPE.END_POINT_ID.value] = self.end_point_id
        if self._name != str() or debug:
            veh_type[constants.VEHICLE_TYPE.NAME.value] = self.name
        if self._capacity != 0 or debug:
            veh_type[constants.VEHICLE_TYPE.CAPACITY.value] = self.capacity
        if self._fixed_cost != 0 or debug:
            veh_type[constants.VEHICLE_TYPE.FIXED_COST.value] = self.fixed_cost
        if self._var_cost_dist != 0 or debug:
            veh_type[constants.VEHICLE_TYPE.
                     VAR_COST_DIST.value] = self.var_cost_dist
        if self._var_cost_time != 0 or debug:
            veh_type[constants.VEHICLE_TYPE.
                     VAR_COST_TIME.value] = self.var_cost_time
        if self._max_number != 0 or debug:
            veh_type[constants.VEHICLE_TYPE.MAX_NUMBER.value] = self.max_number
        if self._tw_begin != 0 or debug:
            veh_type[constants.VEHICLE_TYPE.
                     TIME_WINDOWS_BEGIN.value] = self.tw_begin
        if self._tw_end != 0 or debug:
            veh_type[constants.VEHICLE_TYPE.
                     TIME_WINDOWS_END.value] = self.tw_end
        return veh_type

    def __repr__(self):
        return repr(self.get_vehicle_type())


class Point:
    """Define a point of graph (customer or depot).
       
        Additional informations:
           - service_time : It can represent the time of
             loading or unloading.
           - penalty_or_cost : If the point is a customer
             we can specify a penalty for not
             visiting the customer
             otherwise, if the point is a depot
             we can specify a cost to using the depot.
           - tw_begin : time windows begin
           - tw_end : time windows end 
           - incompatible_vehicles : id of vehicles that cannot serve
             the customer or are not accepted in a depot.
    """

    def __init__(self, id, name=str(), id_customer=0, penalty_or_cost=0.0,
                 service_time=0, tw_begin=0, tw_end=0, demand=0,
                 incompatible_vehicles=[]):
        self.name = name
        self.id_customer = id_customer
        self.id = id
        self.service_time = service_time
        self.tw_begin = tw_begin
        self.tw_end = tw_end
        self.time_windows = (self.tw_begin, self.tw_end)
        self.penalty_or_cost = penalty_or_cost
        self.demand = demand
        self.incompatible_vehicles = incompatible_vehicles

    # using property decorator
    @property
    def id(self):
        """getter function of id"""
        return self._id

    @id.setter
    def id(self, id):
        """setter function of id"""
        if not isinstance(id, (int)):
            raise PropertyError(constants.POINT.ID.value,
                                constants.INTEGER_PROPERTY)
        if id < 0:
            raise PropertyError(constants.POINT.ID.value,
                                constants.GREATER_ZERO_PROPERTY)
        if id > 10000:
            raise PropertyError(constants.POINT.ID.value,
                                constants.LESS_MAX_POINTS_ID_PROPERTY)

        self._id = id

    @property
    def name(self):
        """getter function of name"""
        return self._name

    @name.setter
    def name(self, name):
        """setter function of name"""
        if not isinstance(name, (str)):
            raise PropertyError(constants.POINT.NAME.value,
                                constants.STRING_PROPERTY)
        self._name = name

    @property
    def id_customer(self):
        """getter function of id customer"""
        return self._id_customer

    @id_customer.setter
    def id_customer(self, id_customer):
        """setter function of id customer"""
        if not isinstance(id_customer, (int)):
            raise PropertyError(constants.POINT.ID_CUSTOMER.value,
                                constants.INTEGER_PROPERTY)
        if id_customer < 0:
            raise PropertyError(constants.POINT.ID_CUSTOMER.value,
                                constants.GREATER_ZERO_PROPERTY)
        if id_customer > 1022:
            raise PropertyError(constants.POINT.ID_CUSTOMER.value,
                                constants.LESS_MAX_POINTS_PROPERTY)
        self._id_customer = id_customer

    @property
    def penalty(self):
        """getter function of penalty"""
        return self._penalty_or_cost

    @penalty.setter
    def penalty(self, penalty):
        """setter function of penalty"""
        if not isinstance(penalty, (int, float)):
            raise PropertyError(constants.POINT.PENALTY.value,
                                constants.INTEGER_PROPERTY)
        self._penalty_or_cost = penalty

    @property
    def cost(self):
        """getter function of cost"""
        return self._penalty_or_cost

    @cost.setter
    def cost(self, cost):
        """setter function of cost"""
        if not isinstance(cost, (int, float)):
            raise PropertyError(constants.POINT.COST.value,
                                constants.INTEGER_PROPERTY)
        self._penalty_or_cost = cost

    @property
    def service_time(self):
        """getter function of service_time"""
        return self._service_time

    @service_time.setter
    def service_time(self, service_time):
        """setter function of service_time"""
        if not isinstance(service_time, (int, float)):
            raise PropertyError(constants.POINT.SERVICE_TIME.value,
                                constants.NUMBER_PROPERTY)
        self._service_time = service_time

    @property
    def tw_begin(self):
        """getter function of time windows begin"""
        return self._tw_begin

    @tw_begin.setter
    def tw_begin(self, tw_begin):
        """setter function of time windows begin"""
        if not isinstance(tw_begin, (int, float)):
            raise PropertyError(constants.POINT.TIME_WINDOWS_BEGIN.value,
                                constants.NUMBER_PROPERTY)
        self._tw_begin = tw_begin

    @property
    def tw_end(self):
        """getter function of time windows end"""
        return self._tw_end

    @tw_end.setter
    def tw_end(self, tw_end):
        """setter function of time windows end"""
        if not isinstance(tw_end, (int, float)):
            raise PropertyError(constants.POINT.TIME_WINDOWS_END.value,
                                constants.NUMBER_PROPERTY)
        self._tw_end = tw_end

    @property
    def time_windows(self):
        """getter function of time windows"""
        return self._time_windows

    @time_windows.setter
    def time_windows(self, timeWindow):
        """setter function of time windows"""
        if not isinstance(timeWindow, (tuple)):
            raise PropertyError(
                constants.POINT.TIME_WINDOWS.value,
                constants.TUPLE_PROPERTY)
        else:
            if len(timeWindow) != 2:
                raise PropertyError(
                    constants.POINT.TIME_WINDOWS.value,
                    constants.TUPLE_PROPERTY)
            if not isinstance(timeWindow[0], (int, float)
                              ) or not isinstance(timeWindow[1], (int, float)):
                raise PropertyError(constants.POINT.TIME_WINDOWS_BEGIN.value,
                                    constants.NUMBER_PROPERTY)

        self._tw_begin = timeWindow[0]
        self._tw_end = timeWindow[1]
        self._time_windows = timeWindow

    @property
    def demand(self):
        """getter function of demand"""
        return self._demand

    # a setter function of demand
    @demand.setter
    def demand(self, demand):
        """setter function of demand"""
        if not isinstance(demand, (int)):
            raise PropertyError(constants.POINT.DEMAND.value,
                                constants.INTEGER_PROPERTY)
        if demand < 0:
            raise PropertyError(constants.POINT.DEMAND.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._demand = demand


    @property
    def incompatible_vehicles(self):
        """getter function of incompatible_vehicles"""
        return self._incompatible_vehicles

    @incompatible_vehicles.setter
    def incompatible_vehicles(self, incompatible_vehicles_in):
        """setter function of incompatible_vehicles"""
        if not isinstance(incompatible_vehicles_in, (list)):
            raise PropertyError(constants.POINT.INCOMPATIBLE_VEHICLES.value,
                                constants.LIST_INTEGER_PROPERTY)
        if len(incompatible_vehicles_in) > 0:
            if not all(isinstance(x, int) for x in incompatible_vehicles_in):
                raise PropertyError(
                    constants.POINT.INCOMPATIBLE_VEHICLES.value,
                    constants.LIST_INTEGER_PROPERTY)
        self._incompatible_vehicles = incompatible_vehicles_in

    def get_point(self, debug=False):
        """Get all components of a Point which are
         different of default value"""
        point = {}
        point["id"] = self.id
        if self.name != str() or debug:
            point[constants.POINT.NAME.value] = self.name
        if self.id_customer != 0 or debug:
            point[constants.POINT.ID_CUSTOMER.value] = self.id_customer
        if self.service_time != 0 or debug:
            point[constants.POINT.SERVICE_TIME.value] = self.service_time
        if self.tw_begin != 0 or debug:
            point[constants.POINT.TIME_WINDOWS_BEGIN.value] = self.tw_begin
        if self.tw_end != 0 or debug:
            point[constants.POINT.TIME_WINDOWS_END.value] = self.tw_end
        if self.penalty_or_cost != 0 or debug:
            point[constants.POINT.PENALTY_OR_COST.value] = self.penalty_or_cost
        if self.demand != 0 or debug:
            point[constants.POINT.DEMAND_OR_CAPACITY
                  .value] = self.demand
        if self.incompatible_vehicles != [] or debug:
            point[constants.POINT.INCOMPATIBLE_VEHICLES
                  .value] = self.incompatible_vehicles
        return point

    def __repr__(self):
        return repr(self.get_point())


class Customer(Point):
    """Define a point customer of graph.

    Additional informations:
       - id_customer(int): must be inferior or equal to 1022
       - penalty(float): represents the penalty of non visited customer
       - tw_begin(float): time window begin
       - tw_end(float): time window end
       - demand(int): must be an integer
    """

    def __init__(
            self,
            id,
            name=str(),
            id_customer=0,
            penalty=0.0,
            service_time=0,
            tw_begin=0,
            tw_end=0,
            demand=0,
            incompatible_vehicles=[]):
        
        if  id < 1:
                raise PropertyError(constants.POINT.ID.value,
                                constants.GREATER_ONE_PROPERTY)
        id_cust = id_customer
        if id_cust == 0:
            id_cust = id 

        super().__init__(
            id,
            name,
            id_cust,
            penalty,
            service_time,
            tw_begin,
            tw_end,
            demand,
            incompatible_vehicles)


class Depot(Point):
    """Define a point depot of graph.

    Additional informations:
        capacity: must be an integer
    """

    def __init__(
            self,
            id,
            name=str(),
            cost=0,
            service_time=0,
            tw_begin=0,
            tw_end=0,
            incompatible_vehicles=[]):
        super().__init__(id, name, 0, cost, service_time, tw_begin, tw_end,
                         0, incompatible_vehicles)


class Link:
    """Define a link of graph.

    Additional informations:
        is_directed -- it's equal to True if we cannot return at
        start point with the same time and distance
    """

    def __init__(self, start_point_id, end_point_id, name=str(), is_directed=False,
                 distance=0.0, time=0.0, fixed_cost=0.0):
        self.name = name
        self.is_directed = is_directed
        self.start_point_id = start_point_id
        self.end_point_id = end_point_id
        self.distance = distance
        self.time = time
        self.fixed_cost = fixed_cost

    @property
    def name(self):
        """getter function of name"""
        return self._name

    @name.setter
    def name(self, name):
        """setter function of name"""
        if not isinstance(name, (str)):
            raise PropertyError(constants.LINK.NAME.value,
                                constants.STRING_PROPERTY)
        self._name = name

    @property
    def is_directed(self):
        """getter function of is_directed"""
        return self._is_directed

    @is_directed.setter
    def is_directed(self, is_directed):
        """setter function of is_directed"""
        if not isinstance(is_directed, (bool)):
            raise PropertyError(constants.LINK.NAME.value,
                                constants.BOOLEAN_PROPERTY)
        self._is_directed = is_directed

    @property
    def start_point_id(self):
        """getter function of start_point_id"""
        return self._start_point_id

    @start_point_id.setter
    def start_point_id(self, start_point_id):
        """setter function of start_point_id"""
        if not isinstance(start_point_id, (int)):
            raise PropertyError(constants.LINK.START_POINT_ID.value,
                                constants.INTEGER_PROPERTY)
        if start_point_id < 0:
            raise PropertyError(constants.LINK.START_POINT_ID.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._start_point_id = start_point_id

    @property
    def end_point_id(self):
        """getter function of end_point_id"""
        return self._end_point_id

    @end_point_id.setter
    def end_point_id(self, end_point_id):
        """setter function of end_point_id"""
        if not isinstance(end_point_id, (int)):
            raise PropertyError(constants.LINK.END_POINT_ID.value,
                                constants.INTEGER_PROPERTY)
        if end_point_id < 0:
            raise PropertyError(constants.LINK.END_POINT_ID.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._end_point_id = end_point_id

    @property
    def distance(self):
        """getter function of distance"""
        return self._distance

    @distance.setter
    def distance(self, distance):
        """setter function of distance"""
        if not isinstance(distance, (int, float)):
            raise PropertyError(constants.LINK.DISTANCE.value,
                                constants.NUMBER_PROPERTY)
        if distance < 0:
            raise PropertyError(constants.LINK.DISTANCE.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._distance = distance

    @property
    def time(self):
        """getter function of time"""
        return self._time

    @time.setter
    def time(self, time):
        """setter function of time"""
        if not isinstance(time, (int, float)):
            raise PropertyError(constants.LINK.TIME.value,
                                constants.NUMBER_PROPERTY)
        if time < 0:
            raise PropertyError(constants.LINK.TIME.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._time = time

    @property
    def fixed_cost(self):
        """getter function of fixed_cost"""
        return self._fixed_cost

    @fixed_cost.setter
    def fixed_cost(self, fixed_cost):
        """setter function of fixed_cost"""
        if not isinstance(fixed_cost, (int, float)):
            raise PropertyError(constants.LINK.FIXED_COST.value,
                                constants.NUMBER_PROPERTY)
        self._fixed_cost = fixed_cost

    def get_link(self, debug=False):
        """Get all components of a Link which are different of
        default value"""
        link = {}
        link[constants.LINK.START_POINT_ID.value] = self._start_point_id
        link[constants.LINK.END_POINT_ID.value] = self._end_point_id
        if self._name != str() or debug:
            link[constants.LINK.NAME.value] = self._name
        if self._is_directed or debug:
            link[constants.LINK.IS_DIRECTED.value] = self._is_directed
        if self._distance != 0 or debug:
            link[constants.LINK.DISTANCE.value] = self._distance
        if self._time != 0 or debug:
            link[constants.LINK.TIME.value] = self._time
        if self._fixed_cost != 0 or debug:
            link[constants.LINK.FIXED_COST.value] = self._fixed_cost
        return link

    def __repr__(self):
        return repr(self.get_link())


class Parameters:
    """Define all parameters from model
    """

    def __init__(
            self,
            time_limit=300.0,
            upper_bound=1000000,
            heuristic_used=False,
            time_limit_heuristic=20.0,
            config_file=str(),
            solver_name="CLP",
            print_level=-1,
            action="solve",
            cplex_path=""):
        self.time_limit = time_limit
        self.upper_bound = upper_bound
        self.heuristic_used = heuristic_used
        self.time_limit_heuristic = time_limit_heuristic
        self.config_file = config_file
        self.solver_name = solver_name
        self.print_level = print_level
        self.action = action
        self.cplex_path = cplex_path

    @property
    def time_limit(self):
        """float : represents the limit time of resolution"""
        return self._time_limit

    @time_limit.setter
    def time_limit(self, time_limit):
        """setter function of time_limit"""
        if not isinstance(time_limit, (int, float)):
            raise PropertyError(constants.PARAMETERS.TIME_LIMIT.value,
                                constants.NUMBER_PROPERTY)
        if time_limit < 0:
            raise PropertyError(constants.PARAMETERS.TIME_LIMIT.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._time_limit = time_limit

    @property
    def upper_bound(self):
        """float : represents the cost we want to reach """
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, upper_bound):
        """setter function of upper_bound"""
        if not isinstance(upper_bound, (int, float)):
            raise PropertyError(constants.PARAMETERS.UPPER_BOUND.value,
                                constants.NUMBER_PROPERTY)
        self._upper_bound = upper_bound

    # a getter function of heuristic_used

    @property
    def heuristic_used(self):
        """bool : getter function of heuristic_used"""
        return self._heuristic_used

    @heuristic_used.setter
    def heuristic_used(self, heuristic_used):
        """setter function of heuristic_used"""
        if not isinstance(heuristic_used, (bool)):
            raise PropertyError(constants.PARAMETERS.
                                HEURISTIC_USED.value,
                                constants.BOOLEAN_PROPERTY)
        self._heuristic_used = heuristic_used

    @property
    def time_limit_heuristic(self):
        """float : getter function of time_limit_heuristic"""
        return self._time_limit_heuristic

    @time_limit_heuristic.setter
    def time_limit_heuristic(self, time_limit_heuristic):
        """setter function of time_limit_heuristic"""
        if not isinstance(time_limit_heuristic, (int, float)):
            raise PropertyError(constants.PARAMETERS.
                                TIME_LIMIT_HEURISTIC.value,
                                constants.NUMBER_PROPERTY)
        if time_limit_heuristic < 0:
            raise PropertyError(constants.PARAMETERS.
                                TIME_LIMIT_HEURISTIC.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._time_limit_heuristic = time_limit_heuristic

    @property
    def config_file(self):
        """str : indicates the path of the config file for
                            more advanced settings"""
        return self._config_file

    @config_file.setter
    def config_file(self, config_file):
        """setter function of config_file"""
        if not isinstance(config_file, (str)):
            raise PropertyError(constants.PARAMETERS.CONFIG_FILE.value,
                                constants.STRING_PROPERTY)
        self._config_file = config_file

    @property
    def solver_name(self):
        """str : indicates the solver used during the resolution,
                            we can choose "CLP" or "CPLEX" solver"""
        return self._solver_name

    @solver_name.setter
    def solver_name(self, solver_name):
        """setter function of solver_name"""
        if not isinstance(solver_name, (str)):
            raise PropertyError(constants.PARAMETERS.SOLVER_NAME.value,
                                constants.STRING_PROPERTY)
        if solver_name not in constants.SOLVERS:
            raise PropertyError(constants.PARAMETERS.SOLVER_NAME.value,
                                constants.ENUM_STR_PROPERTY,
                                str(constants.SOLVERS))
        self._solver_name = solver_name

    @property
    def print_level(self):
        """indicates the level of print from Bapcod
                            during the resolution, we can choose (-2,-1,0)"""
        return self._print_level

    @print_level.setter
    def print_level(self, print_level):
        """setter function of print_level"""
        if not isinstance(print_level, (int)):
            raise PropertyError(constants.PARAMETERS.PRINT_LEVEL.value,
                                constants.NUMBER_PROPERTY)
        if print_level not in constants.PRINT_LEVEL_LIST:
            raise PropertyError(constants.PARAMETERS.PRINT_LEVEL.value,
                                constants.ENUM_INT_PROPERTY,
                                str(constants.PRINT_LEVEL_LIST))
        self._print_level = print_level

    @property
    def action(self):
        """str : indicates if we want to solve the problem ("solve")
                     or enumerate all feasible routes("enumAllFeasibleRoutes")"""
        return self._action

    @action.setter
    def action(self, action):
        """setter function of action """
        if not isinstance(action, (str)):
            raise PropertyError(constants.PARAMETERS.ACTION.value,
                                constants.STRING_PROPERTY)
        if action not in constants.ACTIONS:
            raise Exception(constants.PARAMETERS.ACTION.value,
                            constants.ENUM_STR_PROPERTY,
                            str(constants.ACTIONS))
        self._action = action

    @property
    def cplex_path(self):
        """str : path of library cplex 22.1.
           You can specify a path if you want to use cplex and 
           replace the bapcod-shared library by the library using cplex"""
        return self._cplex_path

    @cplex_path.setter
    def cplex_path(self, cplex_path):
        """setter function of cplex_path"""
        if not isinstance(cplex_path, (str)):
            raise PropertyError(constants.PARAMETERS.CPLEX_PATH.value,
                                constants.STRING_PROPERTY)
        self._cplex_path = cplex_path

    def get_parameters(self, debug=False):
        """Get all parameters which are different of
        default value"""
        param = {}
        param[constants.PARAMETERS.TIME_LIMIT.value] = self.time_limit
        param[constants.PARAMETERS.ACTION.value] = self.action
        if self.upper_bound != 1000000 or debug:
            param[constants.PARAMETERS.
                  UPPER_BOUND.value] = self.upper_bound
        if self.heuristic_used or debug:
            param[constants.PARAMETERS.
                  HEURISTIC_USED.value] = self.heuristic_used
        if self.time_limit_heuristic != 20 or debug:
            param[constants.PARAMETERS.
                  TIME_LIMIT_HEURISTIC.value] = self.time_limit_heuristic
        if self.config_file != str() or debug:
            param[constants.PARAMETERS.CONFIG_FILE.value] = self.config_file
        if self.solver_name != "CLP" or debug:
            param[constants.PARAMETERS.SOLVER_NAME.value] = self.solver_name
        if self.print_level != -1 or debug:
            param[constants.PARAMETERS.PRINT_LEVEL.value] = self.print_level
        return param

    def __repr__(self):
        return repr(self.get_parameters())


class Statistics:
    """Define a statistics from solution"""

    def __init__(self, json_input=str()):
        self.__solution_time = 0
        self.__best_lb = 0
        self.__root_lb = 0
        self.__root_time = 0
        self.__nb_branch_and_bound_nodes = 0
        if json_input != str():
            self.__json_input = json_input
            self.__solution_time = json_input[constants.STATISTICS.
                                              SOLUTION_TIME.value]
            self.__best_lb = json_input[constants.STATISTICS.
                                        BEST_LOWER_BOUND.value]
            self.__root_lb = json_input[constants.STATISTICS.
                                        ROOT_LOWER_BOUND.value]
            self.__root_time = json_input[constants.STATISTICS.
                                          ROOT_TIME.value]
            self.__nb_branch_and_bound_nodes = json_input[
                constants.STATISTICS. NB_BRANCH_AND_BOUND_NODES. value]

    @property
    def json_input(self):
        """str : formatted string to print statistics in json format"""
        return self.__json_input

    @property
    def nb_branch_and_bound_nodes(self):
        """int : number of branch and bound nodes from tree structure."""
        return self.__nb_branch_and_bound_nodes

    @property
    def root_time(self):
        """float : getter function of root_time"""
        return self.__root_time

    @property
    def root_lb(self):
        """float : the root lower bound find during the resolution"""
        return self.__root_lb

    @property
    def best_lb(self):
        """float : best lower bound find during the resolution"""
        return self.__best_lb


    @property
    def solution_time(self):
        """float : time computed to find the solution"""
        return self.__solution_time

    def __repr__(self):
        return repr(self.__json_input)


class Route:
    """Define a route from solution"""

    def __init__(self, json_input):
        self.__route = json_input
        self.__vehicle_type_id = json_input[constants.ROUTE.VEHICLE_TYPE_ID.value]
        self.__route_cost = json_input[constants.ROUTE.ROUTE_COST.value]
        self.__point_ids = []
        self.__point_names = []
        self.__cap_consumption = []
        self.__time_consumption = []
        self.__incoming_arc_names = []
        for point in json_input[constants.ROUTE.VISITED_POINTS.value]:
            self.__point_ids.append(point[constants.ROUTE.POINT_ID.value])
            self.__point_names.append(point[constants.ROUTE.POINT_NAME.value])
            self.__cap_consumption.append(point[constants.ROUTE.LOAD.value])
            self.__time_consumption.append(point[constants.ROUTE.TIME.value])
            self.__incoming_arc_names.append(point[
                constants.ROUTE.INCOMING_ARC_NAME.value])

    @property
    def route(self):
        """str : formatted string to print route in json format"""
        return self.__route

    @property
    def vehicle_type_id(self):
        """int : id of vehicle type making the trip"""
        return self.__vehicle_type_id

    @property
    def route_cost(self):
        """float : cost incurred by variable and fixed costs"""
        return self.__route_cost

    @property
    def point_ids(self):
        """list(int) : if of each point visited"""
        return self.__point_ids

    @property
    def point_names(self):
        """list(str) : names of visited points"""
        return self.__point_names

    @property
    def cap_consumption(self):
        """list(float) : the loads at each point """
        return self.__cap_consumption

    @property
    def time_consumption(self):
        """list(float) : the time at each point"""
        return self.__time_consumption

    @property
    def incoming_arc_names(self):
        """list(str) : the names of incoming arc"""
        return self.__incoming_arc_names
    
    def __str__(self):
        route_str = ""
        time_is_used = sum(self.__time_consumption) > 0
        capacity_is_used = sum(self.__cap_consumption) > 0
        name_is_used = all(i != "" for i in self.__point_names)
        if (len(self.__point_ids))>0 :
            id_veh = self.__vehicle_type_id
            route_str += 'Route for vehicle ' + str(id_veh) + ':\n'
            route_str += ' ID : ' + str(self.__point_ids[0])
            for i in range (1,len(self.__point_ids)):
                route_str +=' --> ' + str(self.__point_ids[i]) 
            
            if name_is_used:
                route_str += '\n'
                route_str += ' Name : ' + str(self.__point_names[0])
                for i in range (1,len(self.__point_names)):
                    route_str +=' --> ' + str(self.__point_names[i]) 

            if time_is_used:
                route_str += '\n'
                route_str += ' End time : ' + str(self.__time_consumption[0])
                for i in range (1,len(self.__time_consumption)):
                    route_str += ' --> ' + str(self.__time_consumption[i]) 
            
            if capacity_is_used:
                route_str += '\n'
                route_str += ' Load : ' + str(self.__cap_consumption[0])
                for i in range (1,len(self.__cap_consumption)):
                    route_str += ' --> ' + str(self.__cap_consumption[i]) 

            if self.__route_cost != 0 :
                route_str += "\nTotal cost : " + str(self.__route_cost) 
            route_str += '\n \n'
        return route_str

    def __repr__(self):
        return repr(self.__str__())


class Solution:
    """Contains all elements of solution after running model.solve()."""

    def __init__(self, json_input=None, status=constants.MODEL_NOT_SOLVED):
        self.__json = {}
        self.__routes = []
        self.__value = 0

        if json_input != None:
            self.__json = json_input
            if (status > -1 and status < 4) or status == 8:
                self.__value = self.__json["Solution"][
                                        constants.STATISTICS.
                                        SOLUTION_VALUE.value]
                if len(self.__json["Solution"]["Routes"]) > 0:
                    for route in self.__json["Solution"]["Routes"]:
                        self.__routes.append(Route(route))


    def __str__(self):
        route_str =f'\nSolution cost : {self.__value} \n \n'
        for route in self.__routes:
            route_str += str(route)
        return route_str

    def __repr__(self):
        return repr(self.__str__())

    def is_defined(self):
        """ return true if a solution is defined"""
        return self.__routes != []

    @property
    def value(self):
        """float : return the total cost of the solution"""
        return self.__value

    @property
    def json(self):
        """str : formatted string to print statistics in json format"""
        return self.__json

    @property
    def routes(self):
        """list(Route) : contains the set of routes"""
        return self.__routes

    def export(self, name="instance"):
        """Export solution for sharing or debugging model,
        we can specify the name of the file"""
        with open(name + ".json", "w") as outfile:
            outfile.write(json.dumps(self.json, indent=1))


class Model:
    """Define a routing model."""

    def __init__(self):
        self.__json = {}
        self.vehicle_types = VehicleTypesDict()
        self.points = PointsDict()
        self.__customers = dict()
        self.links = LinksDict()
        self.max_total_vehicles_number = 10000
        self.parameters = Parameters()
        self.__output = str()
        self.solution = Solution()
        self.statistics = Statistics()
        self.status = int(constants.MODEL_NOT_SOLVED)
        self.message = constants.ERRORS_MODEL[self.status]

    @property
    def vehicle_types(self):
        """contains the set of vehicle types

        Type:

            VehicleTypesDict : dictionary contains only vehicle type

        Informations:

            - For academic version, with CLP it's possible to resolve the
              problem with only one vehicle type.

            - Ids of vehicle types must be greater than one
        """
        return self._vehicle_types

    @vehicle_types.setter
    def vehicle_types(self, vehicle_types):
        """setter function of vehicle_types"""
        if not isinstance(vehicle_types, (VehicleTypesDict)):
            raise PropertyError(constants.JSON_OBJECT.VEHICLE_TYPES.value,
                                constants.LIST_INTEGER_PROPERTY)
        self._vehicle_types = vehicle_types

    @property
    def points(self):
        """contains the set of customers and depots

            Type:
                - PointsDict : dictionary contains only points
            Informations:
                - It's possible to resolve the problem until 1022 points.
                - For the moment, the capacity of depot is not considered
        """
        return self._points

    # a setter function of points
    @points.setter
    def points(self, points):
        """setter function of points"""
        if not isinstance(points, (PointsDict)):
            raise PropertyError(constants.JSON_OBJECT.POINTS.value, 0)
        self._points = points

    @property
    def links(self):
        """contains the set of links"""
        return self._links

    # a setter function of links
    @links.setter
    def links(self, links):
        """setter function of links"""
        if not isinstance(links, (LinksDict)):
            raise PropertyError(constants.JSON_OBJECT.LINKS.value, 0)
        self._links = links

    @property
    def max_total_vehicles_number(self):
        """the maximum total vehicles number"""
        return self._max_total_vehicles_number

   
    @max_total_vehicles_number.setter
    def max_total_vehicles_number(self, number):
        """setter function of max number of vehicles"""
        if not isinstance(number, (int)):
            raise PropertyError(constants.JSON_OBJECT.MAXNUMBER,
                               constants.INTEGER_PROPERTY)     
        if number < 1:
            raise PropertyError(
                constants.JSON_OBJECT.MAXNUMBER,
                constants.GREATER_ONE_PROPERTY)
        self._max_total_vehicles_number = number

    @property
    def parameters(self):
        """getter function of parameters"""
        return self._parameters

    @property
    def status(self):
        """int : indicates the status of solution"""
        return self._status

    # a setter function of status
    @status.setter
    def status(self, status):
        """setter function of status"""
        if not isinstance(status, (int)):
            raise PropertyError(constants.STATUS, constants.INTEGER_PROPERTY)
        self._status = status

    @property
    def message(self):
        """int : indicates the message associated with status"""
        return self._message

    # a setter function of message
    @message.setter
    def message(self, message):
        """setter function of message"""
        if not isinstance(message, (str)):
            raise PropertyError(constants.MESSAGE, constants.STRING_PROPERTY)
        self._message = message

    # a setter function of parameters
    @parameters.setter
    def parameters(self, parameters):
        """setter function of parameters"""
        if not isinstance(parameters, (Parameters)):
            raise PropertyError(constants.JSON_OBJECT.PARAMETERS.value, 0)
        self._parameters = parameters

    def add_vehicle_type(
            self,
            id: int,
            start_point_id=-1,
            end_point_id=-1,
            name=str(),
            capacity=0,
            fixed_cost=0.0,
            var_cost_dist=0.0,
            var_cost_time=0.0,
            max_number=1,
            tw_begin=0.0,
            tw_end=0.0):
        """Add VehicleType in dictionary :py:attr:`vehicle_types`"""
        if id in self.vehicle_types:
            raise ModelError(constants.ADD_VEHICLE_TYPE_ERROR)
        self.vehicle_types[id] = VehicleType(
            id,
            start_point_id,
            end_point_id,
            name,
            capacity,
            fixed_cost,
            var_cost_dist,
            var_cost_time,
            max_number,
            tw_begin,
            tw_end)

    def delete_vehicle_type(self, id: int):
        """ Delete a vehicle type by giving his id """
        if id not in self.vehicle_types:
            raise ModelError(constants.DEL_VEHICLE_TYPE_ERROR)
        del self.vehicle_types[id]

    def add_link(
            self,
            start_point_id=0,
            end_point_id=0,
            name=str(),
            is_directed=False,
            distance=0.0,
            time=0.0,
            fixed_cost=0.0):
        """Add Link in dictionary :py:attr:`links`"""
        if (start_point_id,end_point_id) in self.links : 
            self.links[(start_point_id,end_point_id)].append(Link(
                start_point_id,
                end_point_id,
                name,
                is_directed,
                distance,
                time,
                fixed_cost))
        else :
            self.links[(start_point_id,end_point_id)] = [Link(
                start_point_id,
                end_point_id,  
                name,
                is_directed,
                distance,
                time,
                fixed_cost)]
                

    def delete_link(self, start_point_id : int,end_point_id : int):
        """ Delete a link by giving start point id and end point id """
        if (start_point_id,end_point_id) not in self.links:
            raise ModelError(constants.DEL_LINK_ERROR)
        else :
            del self.links[(start_point_id,end_point_id)]

    def __propagate_penalties(self,id_customer,id,penalty_or_cost=0):
        """ Updates the penalties of the same cluster of customers """
        if id_customer not in self.__customers:
            self.__customers[id_customer] = [id]
            
        else:
            if(penalty_or_cost != 0):
                for point_id in self.__customers[id_customer]:
                    if point_id in self.points:
                        self.points[point_id].penalty_or_cost = penalty_or_cost
                self.__customers[id_customer].append(id)
            else:
                point_id = self.__customers[id_customer][0]
                self.points[id].penalty_or_cost = self.points[point_id].penalty_or_cost
                self.__customers[id_customer].append(id)
        
    def add_point(
            self,
            id,
            name=str(),
            id_customer=0,
            service_time=0.0,
            penalty_or_cost=0.0,
            tw_begin=0.0,
            tw_end=0.0,
            demand=0,
            incompatible_vehicles=[]):
        """Add Point in dictionary :py:attr:`points`, if we want to add Depot,
           id_customer must be equal to 0, otherwise it cannot be greater
           than 1022 for a Customer"""

        if id in self.points:
            raise ModelError(constants.ADD_POINT_ERROR)

        self.points[id] = Point(
            id,
            name,
            id_customer,
            penalty_or_cost,
            service_time,
            tw_begin,
            tw_end,
            demand,
            incompatible_vehicles)

        if id_customer>0:
            self.__propagate_penalties(id_customer,id,penalty_or_cost)

    def add_depot(
            self,
            id,
            name=str(),
            service_time=0.0,
            cost=0.0,
            tw_begin=0.0,
            tw_end=0.0,
            incompatible_vehicles=[]):
        """Add depot in dictionary :py:attr:`points`"""
        if id in self.points:
            raise ModelError(constants.ADD_POINT_ERROR)
        self.add_point(id=id, name=name, id_customer=0,
                       service_time=service_time, penalty_or_cost=cost,
                       tw_begin=tw_begin, tw_end=tw_end,
                       incompatible_vehicles=incompatible_vehicles)

    def delete_depot(self, id: int):
        """ Delete a depot by giving his id """
        self.delete_customer(id)

    def add_customer(
            self,
            id,
            name=str(),
            id_customer=0,
            service_time=0.0,
            penalty=0.0,
            tw_begin=0.0,
            tw_end=0.0,
            demand=0,
            incompatible_vehicles=[]):
        """Add customer in dictionary :py:attr:`points`"""
        if id in self.points:
            raise ModelError(constants.ADD_POINT_ERROR)
        id_cust = id_customer
        if id_cust == 0:
            id_cust = id 
            if  id < 1:
                raise PropertyError(constants.POINT.ID.value,
                                constants.GREATER_ONE_PROPERTY)

        self.add_point(id=id, name=name, id_customer=id_cust,
                       service_time=service_time, penalty_or_cost=penalty,
                       tw_begin=tw_begin, tw_end=tw_end,
                       demand=demand,
                       incompatible_vehicles=incompatible_vehicles)


    def delete_customer(self, id: int):
        """ Delete a customer by giving his id """
        if id not in self.points:
            raise ModelError(constants.DEL_POINT_ERROR)
        del self.points[id]
        if id in self.__customers:
            del self.__customers[id]

    def set_parameters(self, time_limit=300, upper_bound=1000000,
                       heuristic_used=False, time_limit_heuristic=20,
                       config_file=str(), solver_name="CLP",
                       print_level=-1, action="solve", cplex_path=""):
        """Set parameters of the model. For more advanced parameters please
       indicates a configuration file on config_file variable.
       solver_name : [CLP,CPLEX]
       action : [solve,enumAllFeasibleRoutes],
       print_level = [-2,-1,0]"""

        self.parameters = Parameters(
            time_limit,
            upper_bound,
            heuristic_used,
            time_limit_heuristic,
            config_file,
            solver_name,
            print_level,
            action,
            cplex_path)

    def set_max_total_vehicles_number(self, number=10000):
        self.max_total_vehicles_number = number


    def check_depots(self):
        """Update the model if there are defined intermediate 
        depots not used by vehicles"""

        depots_ids_defined = set()
        for id in self.points:
            if self.points[id].id_customer == 0:
                depots_ids_defined.add(id) 

        
        ids_vehicles_types = list(self.vehicle_types.keys())
        for id_veh in ids_vehicles_types:
            depots_ids_used = set()
            depots_ids_used.add(self.vehicle_types[id_veh].start_point_id)
            depots_ids_used.add(self.vehicle_types[id_veh].end_point_id)
            depot_not_used = depots_ids_defined.difference(depots_ids_used)
            for id_depot in depot_not_used:
                values = self.points[id_depot].incompatible_vehicles + [id_veh]
                self.points[id_depot].incompatible_vehicles = list(set(values))
        


    def set_json(self):
        """Set model in json format with all elements of model"""
        self.__json = json.dumps({constants.JSON_OBJECT.MAXNUMBER.value:
                                  self.max_total_vehicles_number,
                                  constants.JSON_OBJECT.POINTS.value:
                                  list(self.points.values()),
                                  constants.JSON_OBJECT.
                                  VEHICLE_TYPES.value:
                                  list(self.vehicle_types.values()),
                                  constants.JSON_OBJECT.LINKS.value:
                                  list(self.links.values()),
                                  constants.JSON_OBJECT.
                                  PARAMETERS.value:
                                  self.parameters.get_parameters()},
                                 indent=1)

    def __str__(self):
        self.set_json()
        return self.__json

    def __repr__(self):
        return self.__str__()

    def export(self, name="instance",all_elements=False):
        """Export the model for debugging model,
           we can specify the file name.
           If you put all_elements to True, 
           it exports the model with preprocessing elements."""

        #add preprocessing elements in model
        if all_elements:
            self.check_depots()

        model = json.dumps({constants.JSON_OBJECT.MAXNUMBER.value:
                            self.max_total_vehicles_number,
                            constants.JSON_OBJECT.POINTS.
                            value: list(self.points.values(True)),
                            constants.JSON_OBJECT.VEHICLE_TYPES.value:
                           list(self.vehicle_types.values(True)),
                            constants.JSON_OBJECT.LINKS.value:
                           list(self.links.values(True)),
                            constants.JSON_OBJECT.PARAMETERS.value:
                           self.parameters.get_parameters(True)},
                           indent=1)
        # Writing to sample.json
        with open(name + ".json", "w") as outfile:
            outfile.write(model)
   
    def solve(self):
        """
        Solve the routing problem by using the shared library bapcod.
           

        Additional informations:
            VRPSolverEasy is compatible with Windows 64x,  Linux and macOS only
        """
        _lib_bapcod = None
        _lib_name = None
        _lib_candidates = []


        if platform.system() == constants.WINDOWS_PLATFORM:
            _lib_name = constants.LIBRARY_WINDOWS
        elif platform.system() == constants.LINUX_PLATFORM:
            _lib_name = constants.LIBRARY_LINUX
        elif platform.system() == constants.MAC_PLATFORM:
            _lib_name = constants.LIBRARY_MAC

        else:
            raise ModelError(constants.PLATFORM_ERROR)

        # Load solver
        if self.parameters.cplex_path != str():
            try:
                _c.cdll.LoadLibrary(
                    os.path.realpath(
                        self.parameters.cplex_path))
            except BaseException:
                raise ModelError(constants.BAPCOD_ERROR)

        # Try three different locations to load the native library:
        # 1. The current folder
        # 2. The platform folder (lib/Windows for example)
        # 3. The system folders (delegates the loading behavior to the system)

        _lib_candidates.append(os.path.join(os.path.dirname
                                            (os.path.realpath(__file__)),
                                            _lib_name))

        _lib_candidates.append(os.path.join(
            os.path.join(os.path.realpath(__file__ + "/../../lib/"),
                         platform.system()), _lib_name))

        _lib_candidates.append(_lib_name)

        _loaded_library = None
        for candidate in _lib_candidates:
            try:
                # Python 3.8 has changed the behavior of CDLL on Windows.
                if hasattr(os, 'add_dll_directory'):
                    _lib_bapcod = _c.CDLL(candidate, winmode=0)
                else:
                    _lib_bapcod = _c.CDLL(candidate)
                _loaded_library = candidate
                break
            except BaseException:
                pass

        if _loaded_library is None:
            raise ModelError(constants.LOAD_LIB_ERROR)
        self.check_depots()
        self.set_json()

        input = _c.c_char_p(self.__json.encode('UTF-8'))
        solve = _lib_bapcod.solveModel
        solve.argtypes = [_c.c_char_p]
        solve.restype = _c.POINTER(_c.c_char_p)
        free_memory = _lib_bapcod.freeMemory
        free_memory.argtypes = [_c.POINTER(_c.c_char_p)]
        free_memory.restype = _c.c_void_p

        try:
            output = solve(input)
            self.__output = json.loads((_c.c_char_p.from_buffer(output)).value)
            self.status = self.__output["Status"]["code"]
            self.message = self.__output["Status"]["message"]
            self.solution = Solution(self.__output,self.status)

            if self.status > -1 and self.status < 4 and self.parameters.action != "enumAllFeasibleRoutes":
                self.statistics = Statistics(self.solution.json["Statistics"])
                
            free_memory(output)
        except BaseException:
            raise ModelError(constants.BAPCOD_ERROR)

