import ctypes as _c
import json
from VRPSolverReal.src import constants
import platform
import os
import sys
import time
import math
if sys.version_info > (3, 7):
    import collections.abc as collections
else:
    import collections
    

########
__version__ = "0.0.1"
__author__ = "Najib ERRAMI Ruslan SADYKOV Eduardo Uchoa"
__copyright__ = "Copyright VRPYSolver, all rights reserved"
__email__ = "najib.errami@inria.fr"


class PropertyError(Exception):
    """Exception raised for errors in the input property.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, property="", code=0,str_list=""):
        self.message = property+ constants.ERRORS_PROPERTY[code] + str_list
        super().__init__(self.message)

class ModelError(Exception):
    """ Exception raised for errors in the model.

    Attributes:
        message -- explanation of the error
   """

    def __init__(self, code=0):
        self.message = constants.ERRORS_MODEL[code]
        super().__init__(self.message)

class VehicleTypesDict(collections.MutableMapping,dict):
    """Dictionary of vehicle types
    
    key (int): Id of vehicle type
    value: class Vehicle type
    
    """
    def __getitem__(self,key):
        return dict.__getitem__(self,key)
    def __setitem__(self, key, value):
        if not isinstance(key,(int)):
            raise PropertyError(constants.KEY_STR,constants.INTEGER_PROPERTY)
        if not isinstance(value,(VehicleType)):
            raise PropertyError(str(),constants.VEHICLE_TYPE_PROPERTY)
        if value.id != key:
            raise PropertyError(str(),constants.DICT_PROPERTY)
        dict.__setitem__(self,key,value)
    def __delitem__(self, key):
        dict.__delitem__(self,key)
    def __iter__(self):
        return dict.__iter__(self)
    def __len__(self):
        return dict.__len__(self)
    def __contains__(self, x):
        return dict.__contains__(self,x)
    def values(self,debug=False):
       return list( value.get_VehicleType(debug) 
                   for value in dict.values(self))

class PointsDict(collections.MutableMapping,dict):
    """Dictionary of points ( depots and customers)
    
    key (int): Id of point
    value: class Customer or Depot
    
    """
    def __getitem__(self,key):
        return dict.__getitem__(self,key)
    def __setitem__(self, key, value):
        if not isinstance(key,(int)):
            raise PropertyError(constants.KEY_STR,constants.INTEGER_PROPERTY)
        if not isinstance(value,(Point)):
            raise PropertyError(str(),constants.POINT_PROPERTY)
        if value.id != key:
            raise PropertyError(str(),constants.DICT_PROPERTY)
        if dict.__len__(self)+1>1022:
            raise PropertyError(constants.NB_POINTS_STR,constants.LESS_MAX_POINTS_PROPERTY)
        dict.__setitem__(self,key,value)
    def __delitem__(self, key):
        dict.__delitem__(self,key)
    def __iter__(self):
        return dict.__iter__(self)
    def __len__(self):
        return dict.__len__(self)
    def __contains__(self, x):
        return dict.__contains__(self,x)
    def values(self,debug=False):
       return list( value.get_Point(debug) for value in dict.values(self))
            

class LinksDict(collections.MutableMapping,dict):
    """Dictionary of links
    
    key (str): name of link
    value: class Customer or Depot
    
    """
    def __getitem__(self,key):
        return dict.__getitem__(self,key)
    def __setitem__(self, key, value):
        if not isinstance(key,(str)):
            raise PropertyError(constants.KEY_STR,3)
        if not isinstance(value,(Link)):
            raise PropertyError(str(),12)
        if value.name != key:
            raise PropertyError(str(),constants.DICT_PROPERTY)
        dict.__setitem__(self,key,value)
    def __delitem__(self, key):
        dict.__delitem__(self,key)
    def __iter__(self):
        return dict.__iter__(self)
    def __len__(self):
        return dict.__len__(self)
    def __contains__(self, x):
        return dict.__contains__(self,x)
    def values(self,debug=False):
       return list( value.get_Link(debug) for value in dict.values(self))

class VehicleType:
    """Define a vehicle type with different attributes.

    Additional informations:
        maxNumber ---- number of vehicles available
        varCostDist -- variable cost per unit of distance
        varCostTime -- variable cost per unit of time
        TWbegin -- time windows begin 
        TWend -- time windows end 
    """
    def __init__(self,id:int,startPointId:int,endPointId:int, name=str(),
                 capacity=0,fixedCost=0,varCostDist=0,varCostTime=0,
                 maxNumber=1,TWbegin=0,TWend=0):
        self.name = name
        self.id = id
        self.capacity = capacity
        self.fixedCost = fixedCost
        self.varCostDist = varCostDist
        self.varCostTime = varCostTime
        self.maxNumber = maxNumber
        self.startPointId = startPointId
        self.endPointId = endPointId
        self.TWbegin = TWbegin
        self.TWend = TWend
    


    # a getter function of id
    @property
    def id(self):
        return self._id
       
    # a setter function of id
    @id.setter
    def id(self, id):
        if not isinstance(id, (int)):
            raise PropertyError(constants.ID_STR,constants.INTEGER_PROPERTY)
        if id<1:
            raise PropertyError(constants.ID_STR,constants.GREATER_ONE_PROPERTY)
        self._id = id

    # a getter function of name
    @property
    def name(self):
        return self._name
       
    # a setter function of name
    @name.setter
    def name(self, name):
        if not isinstance(name, (str)):
            raise PropertyError(constants.VEHICLE_TYPE.NAME.value,
                                constants.STRING_PROPERTY)
        self._name = name

    # a getter function of capacity
    @property
    def capacity(self):
        return self._capacity
       
    # a setter function of capacity
    @capacity.setter
    def capacity(self, capacity):
        if not isinstance(capacity, (int)):
            raise PropertyError(constants.VEHICLE_TYPE.CAPACITY.value,
                                constants.INTEGER_PROPERTY)
        if capacity < 0:
            raise PropertyError(constants.VEHICLE_TYPE.CAPACITY.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._capacity = capacity

    # a getter function of fixedCost
    @property
    def fixedCost(self):
        return self._fixedCost
    
    # a setter function of fixedCost
    @fixedCost.setter
    def fixedCost(self, fixedCost):
        if not isinstance(fixedCost, (int,float)):
            raise PropertyError(constants.VEHICLE_TYPE.FIXED_COST.value,
                                constants.NUMBER_PROPERTY)
        self._fixedCost = fixedCost

    # a getter function of varCostDist
    @property
    def varCostDist(self):
        return self._varCostDist
    
    # a setter function of varCostDist
    @varCostDist.setter
    def varCostDist(self, varCostDist):
        if not isinstance(varCostDist, (int,float)):
            raise PropertyError(constants.VEHICLE_TYPE.VAR_COST_DIST.value ,
                                constants.NUMBER_PROPERTY)
        self._varCostDist = varCostDist

    # a getter function of varCostTime
    @property
    def varCostTime(self):
        return self._varCostTime
    
    # a setter function of varCostTime
    @varCostTime.setter
    def varCostTime(self, varCostTime):
        if not isinstance(varCostTime, (int,float)):
            raise PropertyError(constants.VEHICLE_TYPE.VAR_COST_TIME.value,
                                constants.NUMBER_PROPERTY)
        self._varCostTime = varCostTime


    # a getter function of maxNumber
    @property
    def maxNumber(self):
        return self._maxNumber
       
    # a setter function of maxNumber
    @maxNumber.setter
    def maxNumber(self, maxNumber):
        if not isinstance(maxNumber, (int)):
            raise PropertyError(constants.VEHICLE_TYPE.MAX_NUMBER.value,
                                constants.INTEGER_PROPERTY)
        if maxNumber < 0:
            raise PropertyError(constants.VEHICLE_TYPE.MAX_NUMBER.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._maxNumber = maxNumber

    # a getter function of startPointId
    @property
    def startPointId(self):
        return self._startPointId
       
    # a setter function of startPointId
    @startPointId.setter
    def startPointId(self, startPointId):
        if not isinstance(startPointId, (int)):
            raise PropertyError(constants.VEHICLE_TYPE.START_POINT_ID.value,
                                constants.INTEGER_PROPERTY)
        if startPointId < 0:
            raise PropertyError(constants.VEHICLE_TYPE.START_POINT_ID.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._startPointId = startPointId

    # a getter function of endPointId
    @property
    def endPointId(self):
        return self._endPointId
       
    # a setter function of endPointId
    @endPointId.setter
    def endPointId(self, endPointId):
        if not isinstance(endPointId, (int)):
            raise PropertyError(constants.VEHICLE_TYPE.END_POINT_ID.value,
                                constants.INTEGER_PROPERTY)
        if endPointId < 0:
            raise PropertyError(constants.VEHICLE_TYPE.END_POINT_ID.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._endPointId = endPointId


    # a getter function of TWbegin
    @property
    def TWbegin(self):
        return self._TWbegin
    
    # a setter function of TWbegin
    @TWbegin.setter
    def TWbegin(self, TWbegin):
        if not isinstance(TWbegin, (int,float)):
            raise PropertyError(constants.VEHICLE_TYPE.TIME_WINDOWS_BEGIN.value
                                ,constants.NUMBER_PROPERTY)
        self._TWbegin = TWbegin

    # a getter function of TWend
    @property
    def TWend(self):
        return self._TWend
    
    # a setter function of TWend
    @TWend.setter
    def TWend(self, TWend):
        if not isinstance(TWend, (int,float)):
            raise PropertyError(constants.VEHICLE_TYPE.TIME_WINDOWS_END.value
                                ,constants.NUMBER_PROPERTY)
        self._TWend = TWend

    def get_VehicleType(self,debug=False):
        #Get all components of a VehicleType which are different of
        # default value 
        vehType = {}
        vehType[constants.VEHICLE_TYPE.ID.value] = self.id
        vehType[constants.VEHICLE_TYPE.START_POINT_ID.value] = self.startPointId
        vehType[constants.VEHICLE_TYPE.END_POINT_ID.value]=self.endPointId
        if(self._name != str() or debug): 
            vehType[constants.VEHICLE_TYPE.NAME.value] = self.name
        if(self._capacity != 0 or debug): 
            vehType[constants.VEHICLE_TYPE.CAPACITY.value] = self.capacity
        if(self._fixedCost != 0 or debug): 
            vehType[constants.VEHICLE_TYPE.FIXED_COST.value] = self.fixedCost
        if(self._varCostDist != 0 or debug): 
            vehType[constants.VEHICLE_TYPE.VAR_COST_DIST.value] = self.varCostDist
        if(self._varCostTime !=0 or debug): 
            vehType[constants.VEHICLE_TYPE.VAR_COST_TIME.value] = self.varCostTime
        if(self._maxNumber != 0 or debug): 
            vehType[constants.VEHICLE_TYPE.MAX_NUMBER.value] = self.maxNumber
        if(self._TWbegin != 0 or debug): 
            vehType[constants.VEHICLE_TYPE.TIME_WINDOWS_BEGIN.value] = self.TWbegin
        if(self._TWend != 0 or debug): 
            vehType[constants.VEHICLE_TYPE.TIME_WINDOWS_END.value] = self.TWend
        return vehType


    def __repr__(self):
        return repr(self.get_VehicleType())

class Point:
    """Define a point of graph(customer or depot).

    Additional informations:
        serviceTime -- It can represent the time of 
            loading or unloading.
        penaltyOrCost -- if the point is a customer
            we can specify penalty for not visiting the customer
        ---------------- otherwise, if the point is a depot we can 
            specify a cost to using the depot
        TWbegin -- time windows begin 
        TWend -- time windows end 
        incompatibleVehicles -- id of vehicles that cannot deliver 
            the customer or not accepted in a depot 
    """
    def __init__(self,id,name=str(),idCustomer=0,penaltyOrCost=0.0,
                 serviceTime=0,TWbegin=0,TWend=0,demandOrCapacity=0,
                 incompatibleVehicles=[]):
        self.name = name
        self.idCustomer = idCustomer
        self.id = id
        self.serviceTime = serviceTime
        self.TWbegin = TWbegin
        self.TWend = TWend
        self.penaltyOrCost = penaltyOrCost
        self.demandOrCapacity = demandOrCapacity
        self.incompatibleVehicles = incompatibleVehicles

    # using property decorator
    # a getter function of id
    @property
    def id(self):
        return self._id
       
    # a setter function of id
    @id.setter
    def id(self, id):
        if not isinstance(id, (int)):
            raise PropertyError(constants.POINT.ID.value,
                                constants.INTEGER_PROPERTY)        
        if id<0:
            raise PropertyError(constants.POINT.ID.value,
                                constants.GREATER_ZERO_PROPERTY)
        if self._idCustomer>0:
            if id>1022:
                raise PropertyError(constants.POINT.ID.value,
                                    constants.LESS_MAX_POINTS_PROPERTY)
        self._id = id


    # a getter function of name
    @property
    def name(self):
        return self._name
       
    # a setter function of name
    @name.setter
    def name(self, name):
        if not isinstance(name, (str)):
            raise PropertyError(constants.POINT.NAME.value,
                                constants.STRING_PROPERTY)
        self._name = name
    
    # a getter function of capacity
    @property
    def idCustomer(self):
        return self._idCustomer
       
    # a setter function of capacity
    @idCustomer.setter
    def idCustomer(self, idCustomer):
        if not isinstance(idCustomer, (int)):
            raise PropertyError(constants.POINT.ID_CUSTOMER.value,
                                constants.INTEGER_PROPERTY)
        if idCustomer < 0:
            raise PropertyError(constants.POINT.ID_CUSTOMER.value,
                                constants.GREATER_ZERO_PROPERTY)
        if idCustomer > 1022:
            raise PropertyError(constants.POINT.ID_CUSTOMER.value,
                                constants.LESS_MAX_POINTS_PROPERTY)
        self._idCustomer = idCustomer


    # a getter function of penalty
    @property
    def penalty(self):
        return self._penaltyOrCost
       
    # a setter function of penalty
    @penalty.setter
    def penalty(self, penalty):
        if not isinstance(penalty, (int,float)):
            raise PropertyError(constants.POINT.PENALTY.value,
                                constants.INTEGER_PROPERTY)
        self._penaltyOrCost = penalty
       
     # a getter function of cost
    @property
    def cost(self):
        return self._penaltyOrCost
       
    # a setter function of capacity
    @cost.setter
    def cost(self, cost):
        if not isinstance(cost, (int,float)):
            raise PropertyError(constants.POINT.COST.value,
                                constants.INTEGER_PROPERTY)
        self._penaltyOrCost = cost

    # a getter function of varCostDist
    @property
    def serviceTime(self):
        return self._serviceTime
    
    # a setter function of varCostDist
    @serviceTime.setter
    def serviceTime(self, serviceTime):
        if not isinstance(serviceTime, (int,float)):
            raise PropertyError(constants.POINT.SERVICE_TIME.value,
                                constants.NUMBER_PROPERTY)
        self._serviceTime = serviceTime

    # a getter function of varCostDist
    @property
    def TWbegin(self):
        return self._TWbegin
    
    # a setter function of varCostDist
    @TWbegin.setter
    def TWbegin(self, TWbegin):
        if not isinstance(TWbegin, (int,float)):
            raise PropertyError(constants.POINT.TIME_WINDOWS_BEGIN.value,
                                constants.NUMBER_PROPERTY)
        self._TWbegin = TWbegin

    # a getter function of varCostDist
    @property
    def TWend(self):
        return self._TWend
    
    # a TWend function of varCostDist
    @TWend.setter
    def TWend(self, TWend):
        if not isinstance(TWend, (int,float)):
            raise PropertyError(constants.POINT.TIME_WINDOWS_END.value,
                                constants.NUMBER_PROPERTY)
        self._TWend = TWend


    # a getter function of time windows
    @property
    def timeWindows(self):
        return (self._TWbegin,self._TWend)
    
    # a TWend function of time windows
    @TWend.setter
    @TWbegin.setter
    def timeWindows(self,TWbegin, TWend):
        if not isinstance(TWend, (int,float)):
            raise PropertyError(constants.POINT.TIME_WINDOWS.value,
                                constants.NUMBER_PROPERTY)
        self._TWbegin = TWbegin
        self._TWend = TWend

    # a getter function of demand
    @property
    def demand(self):
        return self._demandOrCapacity
       
    # a setter function of demand
    @demand.setter
    def demand(self, demand):
        if not isinstance(demand, (int)):
            raise PropertyError(constants.POINT.DEMAND.value,
                                constants.INTEGER_PROPERTY)
        if demand < 0:
            raise PropertyError(constants.POINT.DEMAND.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._demandOrCapacity = demand
        
    # a getter function of capacity
    @property
    def capacity(self):
        return self._demandOrCapacity
       
    # a setter function of capacity
    @capacity.setter
    def capacity(self, capacity):
        if not isinstance(capacity, (int)):
            raise PropertyError(constants.POINT.CAPACITY.value,
                                constants.INTEGER_PROPERTY)
        if capacity < 0:
            raise PropertyError(constants.POINT.CAPACITY.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._demandOrCapacity = capacity

    @property
    def incompatibleVehicles(self):
        return self._incompatibleVehicles
       
    # a setter function of capacity
    @incompatibleVehicles.setter
    def incompatibleVehicles(self, incompatibleVehicles):
        if not isinstance(incompatibleVehicles, (list)):
            raise PropertyError(constants.POINT.INCOMPATIBLE_VEHICLES.value,
                                constants.LIST_INTEGER_PROPERTY)
        if len(incompatibleVehicles) > 0:
            if not all(isinstance(x, int) for x in incompatibleVehicles):
                raise PropertyError(constants.POINT.INCOMPATIBLE_VEHICLES.value,
                                    constants.LIST_INTEGER_PROPERTY)
        self._incompatibleVehicles = incompatibleVehicles
        
    def get_Point(self,debug=False):
        #Get all components of a Point which are 
        #different of default value 
        point = {}
        point["id"] = self.id
        if(self.name != str() or debug):
           point[constants.POINT.NAME.value] = self.name
        if(self.idCustomer != 0 or debug): 
            point[constants.POINT.ID_CUSTOMER.value] = self.idCustomer
        if(self.serviceTime != 0 or debug): 
            point[constants.POINT.SERVICE_TIME.value] = self.serviceTime
        if(self.TWbegin != 0 or debug): 
            point[constants.POINT.TIME_WINDOWS_BEGIN.value] = self.TWbegin
        if(self.TWend != 0 or debug): 
            point[constants.POINT.TIME_WINDOWS_END.value] = self.TWend
        if(self.penaltyOrCost != 0 or debug): 
            point[constants.POINT.PENALTY_OR_COST.value] = self.penaltyOrCost
        if(self.demandOrCapacity != 0 or debug): 
            point[constants.POINT.DEMAND_OR_CAPACITY
                  .value]=self.demandOrCapacity
        if(self.incompatibleVehicles != [] or debug): 
            point[constants.POINT.INCOMPATIBLE_VEHICLES
                  .value] = self.incompatibleVehicles
        return point


    def __repr__(self):
        return repr(self.get_Point())


class Customer(Point):
    def __init__(self,id, name=str(),idCustomer=id,penalty=0,serviceTime=0,
                 TWbegin=0,TWend=0,demand=0,incompatibleVehicles=[]):
        super().__init__(id,name,idCustomer,penalty,serviceTime,TWbegin,
                 TWend,demand,incompatibleVehicles)

class Depot(Point):
    def __init__(self,id, name=str(),cost=0,serviceTime=0,TWbegin=0,TWend=0,
                 capacity=0,incompatibleVehicles=[]):
        super().__init__(id,name,-1,cost,serviceTime,TWbegin,TWend,
                 capacity,incompatibleVehicles)

class Link:
    """Define a link of graph.

    Additional informations:
        isDirected ---- it's equal to True if we cannot return at 
        startPoint with the same time and distance
    """
    def __init__(self, name=str(),isDirected=False,startPointId=0,
                 endPointId=0,distance=0,time=0,fixedCost=0):
        self.name = name
        self.isDirected = isDirected
        self.startPointId = startPointId
        self.endPointId = endPointId
        self.distance = distance
        self.time = time
        self.fixedCost = fixedCost

    # a getter function of name
    @property
    def name(self):
        return self._name
       
    # a setter function of name
    @name.setter
    def name(self, name):
        if not isinstance(name, (str)):
            raise PropertyError(constants.LINK.NAME.value,
                                constants.STRING_PROPERTY)
        self._name = name

    # a getter function of isDirected
    @property
    def isDirected(self):
        return self._isDirected
       
    # a setter function of isDirected
    @isDirected.setter
    def isDirected(self, isDirected):
        if not isinstance(isDirected, (bool)):
            raise PropertyError(constants.LINK.NAME.value,
                                constants.BOOLEAN_PROPERTY)
        self._isDirected = isDirected

        # a getter function of startPointId
    @property
    def startPointId(self):
        return self._startPointId
       
    # a setter function of startPointId
    @startPointId.setter
    def startPointId(self, startPointId):
        if not isinstance(startPointId, (int)):
            raise PropertyError(constants.LINK.START_POINT_ID.value,
                                constants.INTEGER_PROPERTY)
        if startPointId < 0:
            raise PropertyError(constants.LINK.START_POINT_ID.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._startPointId = startPointId

    # a getter function of endPointId
    @property
    def endPointId(self):
        return self._endPointId
       
    # a setter function of endPointId
    @endPointId.setter
    def endPointId(self, endPointId):
        if not isinstance(endPointId, (int)):
            raise PropertyError(constants.LINK.END_POINT_ID.value,
                                constants.INTEGER_PROPERTY)
        if endPointId < 0:
            raise PropertyError(constants.LINK.END_POINT_ID.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._endPointId= endPointId

    # a getter function of distance
    @property
    def distance(self):
        return self._distance
    
    # a setter function of distance
    @distance.setter
    def distance(self, distance):
        if not isinstance(distance, (int,float)):
            raise PropertyError(constants.LINK.DISTANCE.value,
                                constants.NUMBER_PROPERTY)
        self._distance = distance

    # a getter function of time
    @property
    def time(self):
        return self._time
    
    # a setter function of time
    @time.setter
    def time(self, time):
        if not isinstance(time, (int,float)):
            raise PropertyError(constants.LINK.TIME.value,
                                constants.NUMBER_PROPERTY)
        self._time = time

    # a getter function of fixedCost
    @property
    def fixedCost(self):
        return self._fixedCost
    
    # a setter function of fixedCost
    @fixedCost.setter
    def fixedCost(self, fixedCost):
        if not isinstance(fixedCost, (int,float)):
            raise PropertyError(constants.LINK.FIXED_COST.value,
                                constants.NUMBER_PROPERTY)
        self._fixedCost = fixedCost
    
    def get_Link(self,debug=False):
        """Get all components of a Link which are different of 
        default value""" 
        link = {}
        link[constants.LINK.START_POINT_ID.value] = self._startPointId
        link[constants.LINK.END_POINT_ID.value] = self._endPointId
        if(self._name != str() or debug):
           link[constants.LINK.NAME.value]=self._name
        if(self._isDirected != False or debug): 
            link[constants.LINK.IS_DIRECTED.value] = self._isDirected
        if(self._distance !=0 or debug):
            link[constants.LINK.DISTANCE.value] = self._distance
        if(self._time !=0 or debug):
            link[constants.LINK.TIME.value]=self._time
        if(self._fixedCost!=0 or debug):
            link[constants.LINK.FIXED_COST.value]=self._fixedCost
        return link

    def __repr__(self):
        return repr(self.get_Link())

class Parameters:
    """Define a point of graph(customer or depot).

    Additional informations:
        timeLimit(int) ---- It can represent the limit time of resolution
        upperBound(float) --indicates the cost we want to reach
        configFile(str) -- indicates the path of the config file for 
                            more advanced settings
        solverName(str) -- indicates the solver used during the resolution,
                            we can choose "CLP" or "CPLEX" solver
        printLevel(int) -- indicates the level of print from Bapcod 
                            during the resolution, we can choose (-2,-1,0) 
        action(str) -- indicates if we want to solve the problem ("solve")
                     or enumerate all feasible routes("enumAllFeasibleRoutes")
    """
    def __init__(self, timeLimit=300,upperBound=1000000,heuristicUsed=False,
                 timeLimitHeuristic=20,configFile=str(),solverName="CLP",
                 printLevel=-1,action="solve"):
        self.timeLimit = timeLimit
        self.upperBound = upperBound
        self.heuristicUsed = heuristicUsed
        self.timeLimitHeuristic = timeLimitHeuristic
        self.configFile = configFile
        self.solverName = solverName
        self.printLevel = printLevel
        self.action = action

    # a getter function of timeLimit
    @property
    def timeLimit(self):
        return self._timeLimit
       
    # a setter function of timeLimit
    @timeLimit.setter
    def timeLimit(self, timeLimit):
        if not isinstance(timeLimit, (int,float)):
            raise PropertyError(constants.PARAMETERS.TIME_LIMIT.value,
                                constants.NUMBER_PROPERTY)
        if timeLimit < 0:
            raise PropertyError(constants.PARAMETERS.TIME_LIMIT.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._timeLimit = timeLimit

    # a getter function of upperBound
    @property
    def upperBound(self):
        return self._upperBound
       
    # a setter function of upperBound
    @upperBound.setter
    def upperBound(self, upperBound):
        if not isinstance(upperBound, (int,float)):
            raise PropertyError(constants.PARAMETERS.UPPER_BOUND.value,
                                constants.NUMBER_PROPERTY)
        self._upperBound = upperBound


    # a getter function of heuristicUsed
    @property
    def heuristicUsed(self):
        return self._heuristicUsed
       
    # a setter function of heuristicUsed
    @heuristicUsed.setter
    def heuristicUsed(self, heuristicUsed):
        if not isinstance(heuristicUsed, (bool)):
            raise PropertyError(constants.PARAMETERS.
                                HEURISTIC_USED.value,
                                constants.BOOLEAN_PROPERTY)
        self._heuristicUsed = heuristicUsed

    # a getter function of timeLimitHeuristic
    @property
    def timeLimitHeuristic(self):
        return self._timeLimitHeuristic
       
    # a setter function of timeLimitHeuristic
    @timeLimitHeuristic.setter
    def timeLimitHeuristic(self, timeLimitHeuristic):
        if not isinstance(timeLimitHeuristic, (int,float)):
            raise PropertyError(constants.PARAMETERS.
                                TIME_LIMIT_HEURISTIC.value,
                                constants.NUMBER_PROPERTY)
        if timeLimitHeuristic < 0:
            raise PropertyError(constants.PARAMETERS.
                                TIME_LIMIT_HEURISTIC.value,
                                constants.GREATER_ZERO_PROPERTY)
        self._timeLimitHeuristic = timeLimitHeuristic

    # a getter function of configFile
    @property
    def configFile(self):
        return self._configFile
       
    # a setter function of configFile
    @configFile.setter
    def configFile(self, configFile):
        if not isinstance(configFile, (str)):
            raise PropertyError(constants.PARAMETERS.CONFIG_FILE.value,
                                constants.STRING_PROPERTY)
        self._configFile = configFile

    # a getter function of solverName
    @property
    def solverName(self):
        return self._solverName
       
    # a setter function of solverName
    @solverName.setter
    def solverName(self, solverName):
        if not isinstance(solverName, (str)):
            raise PropertyError(constants.PARAMETERS.SOLVER_NAME.value,
                                constants.STRING_PROPERTY)
        if solverName not in constants.SOLVERS:
            raise PropertyError(constants.PARAMETERS.SOLVER_NAME.value,
                               constants.ENUM_STR_PROPERTY,
                                str(constants.SOLVERS))
        self._solverName = solverName

    # a getter function of printLevel
    @property
    def printLevel(self):
        return self._printLevel
       
    # a setter function of printLevel
    @printLevel.setter
    def printLevel(self, printLevel):
        if not isinstance(printLevel, (int)):
            raise PropertyError(constants.PARAMETERS.PRINT_LEVEL.value,
                                constants.NUMBER_PROPERTY)
        if printLevel not in constants.PRINT_LEVEL_LIST:
            raise PropertyError(constants.PARAMETERS.PRINT_LEVEL.value, 
                                constants.ENUM_INT_PROPERTY,
                                str(constants.PRINT_LEVEL_LIST))
        self._printLevel = printLevel

    # a getter function of action
    @property
    def action(self):
        return self._action
       
    # a setter function of action
    @action.setter
    def action(self, action):
        if not isinstance(action, (str)):
            raise PropertyError(constants.PARAMETERS.ACTION.value,
                                constants.STRING_PROPERTY)
        if action not in constants.ACTIONS:
            raise Exception(constants.PARAMETERS.ACTION.value,
                           constants.ENUM_STR_PROPERTY,
                                str(constants.ACTIONS))
        self._action = action

    def get_Parameters(self,debug=False):
        param = {}
        param[constants.PARAMETERS.TIME_LIMIT.value] = self.timeLimit
        param[constants.PARAMETERS.ACTION.value] = self.action
        if(self.upperBound != 1000000 or debug): 
            param[constants.PARAMETERS.
                  UPPER_BOUND.value] = self.upperBound
        if(self.heuristicUsed != False or debug):
            param[constants.PARAMETERS.
                  HEURISTIC_USED.value] = self.heuristicUsed
        if(self.timeLimitHeuristic != 20 or debug):
            param[constants.PARAMETERS.
                  TIME_LIMIT_HEURISTIC.value] = self.timeLimitHeuristic
        if(self.configFile != str() or debug):
            param[constants.PARAMETERS.CONFIG_FILE.value] = self.configFile
        if(self.solverName != "CLP" or debug):
            param[constants.PARAMETERS.SOLVER_NAME.value] = self.solverName
        if(self.printLevel != -1 or debug):
            param[constants.PARAMETERS.PRINT_LEVEL.value] = self.printLevel
        return param

    def __repr__(self):
        return repr(self.get_Parameters())

class Statistics:

    def __init__(self,jsonInput=str()):
        if (jsonInput != str()):
            self.__jsonInput = jsonInput
            self.__solutionTime = jsonInput[constants.STATISTICS.
                                          SOLUTION_TIME.value]
            self.__solutionValue = jsonInput[constants.STATISTICS.
                                           SOLUTION_VALUE.value]
            self.__bestLB = jsonInput[constants.STATISTICS.
                                           BEST_LOWER_BOUND.value]
            self.__rootLB = jsonInput[constants.STATISTICS.
                                           ROOT_LOWER_BOUND.value]
            self.__rootTime = jsonInput[constants.STATISTICS.
                                           ROOT_TIME.value]
            self.__nbBranchAndBoundNodes = jsonInput[constants.STATISTICS.
                                           NB_BRANCH_AND_BOUND_NODES.value]
    
        
    # getter functions
    @property
    def nbBranchAndBoundNodes(self):
        return self.__nbBranchAndBoundNodes

    @property
    def rootTime(self):
        return self.__rootTime

    @property
    def rootLB(self):
        return self.__rootLB
    
    @property
    def bestLB(self):
        return self.__bestLB
    
    @property
    def solutionValue(self):
        return self.__solutionValue

    
    @property
    def solutionTime(self):
        return self.__solutionTime
    
    def __repr__(self):
        return repr(self.__jsonInput)

class Route:
    def __init__(self,jsonInput):
        self.__route = jsonInput
        self.__vehicleTypeId = jsonInput[constants.ROUTE.VEHICLE_TYPE_ID.value]
        self.__routeCost = jsonInput[constants.ROUTE.ROUTE_COST.value]
        self.__pointIds = []
        self.__pointNames = []
        self.__capConsumption = []
        self.__timeConsumption = []
        self.__incomingArcNames = []
        for point in jsonInput[constants.ROUTE.VISITED_POINTS.value]:
            self.__pointIds.append(point[constants.ROUTE.POINT_ID.value])
            self.__pointNames.append(point[constants.ROUTE.POINT_NAME.value])
            self.__capConsumption.append(point[constants.ROUTE.LOAD.value])
            self.__timeConsumption.append(point[constants.ROUTE.TIME.value])
            self.__incomingArcNames.append(point[
                constants.ROUTE.INCOMING_ARC_NAME.value])  
    
    # a getter function of action
    @property
    def route(self):
        return self.__route          
    
    @property
    def vehicleTypeId(self):
        return self.__vehicleTypeId
    
    @property
    def routeCost(self):
        return self.__routeCost 
    
    @property
    def pointIds(self):
        return self.__pointIds 

    @property
    def pointNames(self):
        return self.__pointNames

    @property
    def capConsumption(self):
        return self.__capConsumption
    
    @property
    def timeConsumption(self):
        return self.__timeConsumption
    
    @property
    def incomingArcNames(self):
        return self.__incomingArcNames

    def __repr__(self):
        return repr(self.jsonInput)
    
class Solution:
    def __init__(self, jsonInput=str()):
        self.solution = dict()
        self.routes = []
        self.statistics = Statistics()
        self.status = 0
        self.message = str()
        if(jsonInput != str()):
            self.solution = json.loads(jsonInput)
            self.status = self.solution["Status"]["code"]
            self.message = self.solution["Status"]["message"]
            if(self.status > 2 and self.status < 6 ):
                self.statistics = Statistics(self.solution["Statistics"])
            if((self.status > 2 and self.status < 6) or self.status == 8):
                if len(self.solution["Solution"]) > 0:
                    for route in self.solution["Solution"]:
                        self.routes.append(Route(route))
    def __str__(self):
        return json.dumps(self.solution,indent=1) 
    def __repr__(self):
        return repr(self.__str__())

class create_model:
    """Define a routing model.

    Additional informations:
        map_model(dict) -- contains the model in json format
        vehicleTypes(dict) -- contains the set of vehicle types
        points(dict) -- contains the set of customers and depots
        links(dict) -- contains the set of links
        output(str) -- defines the json output after solving the problem
    """
    def __init__(self):
        self.__map_model={}
        self.vehicleTypes=VehicleTypesDict()
        self.points=PointsDict()
        self.links=LinksDict()
        self.parameters=Parameters()
        self.__output=str()    
        self.solution=Solution()
    
    @property
    def vehicleTypes(self):
        return self._vehicleTypes
       
    # a setter function of vehicleTypes
    @vehicleTypes.setter
    def vehicleTypes(self, vehicleTypes):
        if not isinstance(vehicleTypes, (VehicleTypesDict)):
            raise PropertyError(constants.JSON_OBJECT.VEHICLE_TYPES.value,
                                constants.LIST_INTEGER_PROPERTY)
        self._vehicleTypes = vehicleTypes


    @property
    def points(self):
        return self._points
       
    # a setter function of points
    @points.setter
    def points(self, points):
        if not isinstance(points, (PointsDict)):
            raise PropertyError(constants.JSON_OBJECT.POINTS.value,0)
        self._points = points

    @property
    def links(self):
        return self._links
       
    # a setter function of links
    @links.setter
    def links(self, links):
        if not isinstance(links, (LinksDict)):
            raise PropertyError(constants.JSON_OBJECT.LINK.value,0)
        self._links = links

    @property
    def parameters(self):
        return self._parameters
       
    # a setter function of parameters
    @parameters.setter
    def parameters(self, parameters):
        if not isinstance(parameters, (Parameters)):
            raise PropertyError(constants.JSON_OBJECT.PARAMETERS.value,0)
        self._parameters = parameters
    
    
    def add_VehicleType(self,id:int,startPointId:int,endPointId:int,name=str(),
                        capacity=0,fixedCost=0,varCostDist=0,varCostTime=0,
                        maxNumber=1,TWbegin=0,TWend=0):
        """Add VehicleType in dictionary self.vehicleTypes"""
        if(id in self.vehicleTypes):
            raise ModelError(constants.ADD_VEHICLE_TYPE_ERROR)
        else:            
            self.vehicleTypes[id]=VehicleType(id,startPointId,endPointId,name,
                                              capacity,fixedCost,varCostDist,
                                              varCostTime,maxNumber,TWbegin,
                                              TWend)
    
 
    def add_Link(self, name=str(),isDirected=False,startPointId=0,endPointId=0,
                 distance=0,time=0,fixedCost=0):
        """Add Link in dictionary self.links"""
        if(name in self.links):
            raise ModelError(constants.ADD_LINK_ERROR)
        else:
            self.links[name]=Link(name,isDirected,startPointId,endPointId,
                                  distance,time,fixedCost)

 
    def add_Point(self,id,name=str(),idCustomer=0,serviceTime=0,penaltyOrCost=0,
                  TWbegin=0,TWend=0,demandOrCapacity=0,
                  incompatibleVehicles=[]):
        """Add Point in dictionary self.points, if we want to add Depot
           idCustomer must be equal to 0 otherwise it cannot be superior 
           to 1022 for a Customer"""
        if(id in self.points):
            raise ModelError(constants.ADD_POINT_ERROR)
        else:
            self.points[id]=Point(id,name,idCustomer,penaltyOrCost,
                                  serviceTime,TWbegin,TWend,demandOrCapacity,
                                  incompatibleVehicles)


    def add_Depot(self,id,name=str(),serviceTime=0,cost=0,TWbegin=0,TWend=0,
                  capacity=0,incompatibleVehicles=[]):
        """Add Depot in dictionary self.points"""
        if(id in self.points):
             raise ModelError(constants.ADD_POINT_ERROR)
        else:
            self.add_Point(id=id,name=name,idCustomer=0,
                           serviceTime=serviceTime,penaltyOrCost=cost,
                           TWbegin=TWbegin,TWend=TWend,
                           demandOrCapacity=capacity,
                           incompatibleVehicles=incompatibleVehicles)

    
    def add_Customer(self,id,name=str(),idCustomer=id,serviceTime=0,penalty=0,
                     TWbegin=0,TWend=0,demand=0,incompatibleVehicles=[]):
        """Add Customer in dictionary self.points , 
           id must be between 0 and 1022 and all id must be different"""
        if(id in self.points):
             raise ModelError(constants.ADD_POINT_ERROR)
        else:
             self.add_Point(id=id,name=name,idCustomer=id,
                            serviceTime=serviceTime,penaltyOrCost=penalty,
                            TWbegin=TWbegin,TWend=TWend,
                            demandOrCapacity=demand,
                            incompatibleVehicles=incompatibleVehicles)
    
    
    def setParameters(self,timeLimit=300,upperBound=1000000,
                      heuristicUsed=False,timeLimitHeuristic=20,
                      configFile=str(),solverName="CLP",
                      printLevel=-1,action="solve"):
        """Set parameters of model. For more advanced parameters please
       indicates a configuration file on configFile variable"""
        self.parameters=Parameters(timeLimit,upperBound,heuristicUsed,
                                   timeLimitHeuristic,configFile,"CLP",
                                   printLevel,action)
                             
    def setModel(self):
        """Set model in json format with all properties of model"""
        self.__map_model=json.dumps({constants.JSON_OBJECT.POINTS.value:
                                    list(self.points.values()),
                                    constants.JSON_OBJECT.VEHICLE_TYPES.value:
                                    list(self.vehicleTypes.values()),
                                    constants.JSON_OBJECT.LINKS.value:
                                    list(self.links.values()),
                                    constants.JSON_OBJECT.PARAMETERS.value:
                                    self.parameters.get_Parameters()},indent=1)
    
    def __str__(self):
        self.setModel()
        return self.__map_model        
    
    def __repr__(self):
        return(self.__str__())
    

    
    def export(self,name="instance"):
        """Export model for debugging model, 
           we can specify the name of file"""
        model=json.dumps({constants.JSON_OBJECT.POINTS.
                          value:list(self.points.values(True)),
                            constants.JSON_OBJECT.VEHICLE_TYPES.value:
                            list(self.vehicleTypes.values(True)),
                            constants.JSON_OBJECT.LINKS.value:
                            list(self.links.values(True)),
                            constants.JSON_OBJECT.PARAMETERS.value:
                            self.parameters.get_Parameters(True)},
                            indent=1)
        # Writing to sample.json
        with open(name + ".json", "w") as outfile:
            outfile.write(model)

    def solve_literature_instances(self,instanceName=str()):
        """Resolve literature instances of VRP by giving the name of instance in input"""
        try :
            m = create_model()
            maxNumberInput = 0
            capacityInput = 0
            listDepot = []
            listCustomers = []
            pathProject = os.path.abspath(os.getcwd())
            file = open(pathProject + os.path.normpath("/VRPSolverReal/src/"+instanceName), "r")
            lines = file.readlines()
            maxNumberInput = -99999
            capacityInput = -99999
            for count,line in enumerate(lines):
                if(count == 4): #line vehicle
                    listInformations=line.split(" ")
                    for info in listInformations:
                        if(maxNumberInput == -99999):
                            try:
                                maxNumberInput = int(info)
                            except:
                                pass
                        else:
                            try:
                                capacityInput = int(info)
                            except:
                                pass
                if(count == 9): #line depot
                    for word in line.rsplit(" "):
                        try:
                            listDepot.append(int(word))
                        except:
                            pass
                if(count > 9): #lines customers
                    cust = []
                    for word in line.rsplit(" "):
                        try:
                            cust.append(int(word))
                        except:
                            pass
                    listCustomers.append(cust)
        
            m.add_VehicleType(1,0,0,capacity=capacityInput,
                                maxNumber=maxNumberInput,varCostDist=1,
                                varCostTime=1) #Add vehicle Type
            m.add_Depot(listDepot[0],TWbegin=listDepot[4],
                        TWend=listDepot[5])
            for customer in listCustomers:
                m.add_Customer(customer[0],idCustomer=customer[0],
                                demand=customer[3],TWbegin=customer[4],
                                TWend=customer[5]+customer[4]+customer[6],
                                serviceTime=customer[6])
        
            listCustomers.append(listDepot)
            nbPoint=len(listCustomers)
            i = 0
            for count,point in enumerate(listCustomers):
                for count_y in range(count+1,nbPoint):
                    dist = round(math.sqrt((point[1]-
                                            listCustomers[count_y][1])**2 +
                                            (point[2]-listCustomers[count_y][2])**2),3)
                    m.add_Link(name=str(i),startPointId=point[0],
                                endPointId=listCustomers[count_y][0],
                                distance=dist,time=dist)
                    i+=1
            m.export(instanceName.replace('/',' ').replace('.',' ').split()[2])
            m.parameters.timeLimit=30
            m.solve()
            print(m.solution)
        except:
            raise Exception("We can't correctly solve the instance")

    def solve(self):
        """Solve the routing problem by using the shared library 
           bapcod and fill the solution.

        Additional informations:
            VRPSolverReal is compatible with Windows 64x, Linux and macOS only
        """
        _lib_bapcod = None
        _lib_name = None
        _lib_candidates = []

        new_lib =os.path.realpath(__file__ + "/../../lib/Dependencies/" )

        if platform.system() == constants.WINDOWS_PLATFORM:
           _lib_name = constants.LIBRARY_WINDOWS
        elif platform.system() == constants.LINUX_PLATFORM:
           _lib_name = constants.LIBRARY_LINUX
        elif platform.system() == constants.MAC_PLATFORM:
           _lib_name = constants.LIBRARY_MAC
           _c.cdll.LoadLibrary(new_lib + "libCoinUtils.0.dylib")
           _c.cdll.LoadLibrary(new_lib + "libClp.0.dylib")
           _c.cdll.LoadLibrary(new_lib + "libOsi.0.dylib")
           _c.cdll.LoadLibrary(new_lib + "libOsiClp.0.dylib")
           
        else: raise ModelError(constants.PLATFORM_ERROR)
        
        # Try three different locations to load the native library:
        # 1. The current folder 
        # 2. The platform folder (lib/Windows for example)
        # 3. The system folders (delegates the loading behavior to the system)
        
        _lib_candidates.append(os.path.join(os.path.dirname
                                            (os.path.realpath(__file__)),
                                           _lib_name))

        _lib_candidates.append(os.path.join(
            os.path.join(os.path.realpath(__file__ + "/../../lib/" ),
                         platform.system()), _lib_name))
        
        _lib_candidates.append(_lib_name)

        print(os.environ)
        
        if not new_lib in os.environ[constants.PATH_SYSTEM[platform.system()]]:
           os.environ[constants.PATH_SYSTEM[platform.system()]] += ':' + new_lib
           try:
                os.execv(sys.argv[0], sys.argv)
           except Exception:
                print('Failed re-exec')
                sys.exit(1)
        print(new_lib)
        _loaded_library = None
        for candidate in _lib_candidates:
            try:
                # Python 3.8 has changed the behavior of CDLL on Windows.
                if hasattr(os, 'add_dll_directory'):
                    _lib_bapcod = _c.CDLL(candidate, winmode = 0)
                else:
                    _lib_bapcod = _c.CDLL(candidate)
                _loaded_library = candidate
                break
            except:
                pass

        if _loaded_library is None:
            raise ModelError(constants.LOAD_LIB_ERROR)
        self.export()
        self.setModel()
        input=_c.c_char_p(self.__map_model.encode('UTF-8'))
        solve = _lib_bapcod.solveModel
        solve.argtypes = [_c.c_char_p]
        solve.restype = _c.c_char_p
        try:
            output=solve(input)
            self.__output=_c.c_char_p(output).value
            self.solution=Solution(_c.c_char_p(output).value)
        except:
            raise ModelError(constants.BAPCOD_ERROR)
            


def main():

    model=create_model()
    model.solve_literature_instances("data/very_easy/RC101.txt")
    

if __name__ == "__main__":
    main()

