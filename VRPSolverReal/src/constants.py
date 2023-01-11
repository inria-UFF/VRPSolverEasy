from enum import Enum

#VRPSolverReal informations
VERSION = "0.0.1"

LIBRARY_WINDOWS = "bapcod-shared.dll"
LIBRARY_LINUX = "bapcod-shared.so"
LIBRARY_MAC = "bapcod-shared.dylib"

WINDOWS_PLATFORM = "Windows"
LINUX_PLATFORM = "Linux"
MAC_PLATFORM = "Darwin"

PATH_SYSTEM={"Linux" : "LD_LIBRARY_PATH","Darwin" : "PATH","Windows" : "PATH"}

SOLVERS=["CLP","CPLEX"]
PRINT_LEVEL_LIST=[-2,-1,0]
ACTIONS= ["enumAllFeasibleRoutes","solve"]

# property status
INVALID_PROPERTY = 0
INTEGER_PROPERTY = 1
NUMBER_PROPERTY = 2
STRING_PROPERTY = 3
GREATER_ZERO_PROPERTY = 4
GREATER_ONE_PROPERTY = 5
LESS_MAX_POINTS_PROPERTY = 6
LIST_INTEGER_PROPERTY = 7
BOOLEAN_PROPERTY = 8
VEHICLE_TYPE_PROPERTY = 9
DICT_PROPERTY = 10
POINT_PROPERTY = 11
LINK_PROPERTY = 12
ENUM_STR_PROPERTY = 13
ENUM_INT_PROPERTY = 14
ERRORS_PROPERTY = {INVALID_PROPERTY: " is an invalid property",
                   INTEGER_PROPERTY:" must be an integer",
                   NUMBER_PROPERTY: " must be a number",
                   STRING_PROPERTY: " must be a string",
                   GREATER_ZERO_PROPERTY: " must be greater or equal than 0",
                   GREATER_ONE_PROPERTY: " must be greater or equal than 1",
                   LESS_MAX_POINTS_PROPERTY: " must be less or equal than 1022",
                   LIST_INTEGER_PROPERTY: " must be a list of integers",
                   BOOLEAN_PROPERTY: " must be a boolean",
                   VEHICLE_TYPE_PROPERTY: "The value must be a VehicleType",
                   DICT_PROPERTY: "The key and the id must be the same",
                   POINT_PROPERTY: "The value must be a Point",
                   LINK_PROPERTY: "The value must be a Link",
                   ENUM_STR_PROPERTY: "must be a string in the following list: ",
                   ENUM_INT_PROPERTY: "must be an integer in the following list: "
                   }

# model errors
CUSTOMERS_ERROR = -6
DEPOTS_ERROR = -7
ADD_POINT_ERROR = -7
VEHICLES_ERROR = -8
ADD_VEHICLE_TYPE_ERROR=-9
LINKS_ERROR = -10
ADD_LINK_ERROR=10
PLATFORM_ERROR = -11
LOAD_LIB_ERROR = -12
BAPCOD_ERROR = -13
ERRORS_MODEL={CUSTOMERS_ERROR: "CUSTOMERS ERROR",

              DEPOTS_ERROR: "DEPOTS ERROR",
              ADD_POINT_ERROR: "Cannot add two points with the same id.",
              VEHICLES_ERROR: "VEHICLES ERROR",
              ADD_VEHICLE_TYPE_ERROR: "Cannot add two vehicle Types with the same Id.",
              LINKS_ERROR: "LINKS ERROR",
              ADD_LINK_ERROR: "Cannot add two links with the same name.",
              
              PLATFORM_ERROR: """Cannot determine the underlying platform of 
               your Python distribution. Please note that VRPSolverReal is 
               compatible with Windows, Linux and macOS only. """,
              LOAD_LIB_ERROR: """Cannot load or find library. Please ensure
               that the library bapcod are 
               correctly installed on your system""",
               BAPCOD_ERROR: """ An error occur during modelisation.
               If the solver used is not the default one, 
               make sure you have installed it, 
               if the error persists please contact our support
              for more information"""}

# solution status
BETTER_SOL_DOES_NOT_EXISTS = 0
BETTER_SOL_NOT_FOUND = 1
INFEASIBLE = 2
BETTER_SOL_FOUND = 3
FEASIBLE_SOL_FOUND = 4
OPTIMAL_SOL_FOUND = 5
ENUMERATION_INFEASIBLE = 6	
ENUMERATION_NOT_SUCCEEDED= 7
ENUMERATION_SUCCEEDED = 8

SOLUTION_STATUS = {BETTER_SOL_DOES_NOT_EXISTS: "BETTER_SOL_DOES_NOT_EXISTS",
                BETTER_SOL_NOT_FOUND: "BETTER_SOL_NOT_FOUND",
                INFEASIBLE: "VEHICLES ERROR",LINKS_ERROR: "LINKS ERROR",
                BETTER_SOL_FOUND: "BETTER_SOL_FOUND",
                FEASIBLE_SOL_FOUND: "FEASIBLE_SOL_FOUND",
                OPTIMAL_SOL_FOUND: "OPTIMAL_SOL_FOUND",
                ENUMERATION_INFEASIBLE: "ENUMERATION_INFEASIBLE",
                ENUMERATION_NOT_SUCCEEDED: "ENUMERATION_NOT_SUCCEEDED",
                ENUMERATION_SUCCEEDED: "ENUMERATION_SUCCEEDED"}
#Dictionary
KEY_STR = "key"
ID_STR = "id"
NB_POINTS_STR = "The number of points"

#JSON COMPONENTS
class JSON_OBJECT(Enum):
    POINTS = "Points"
    VEHICLE_TYPES = "VehicleTypes"
    LINKS = "Links"
    PARAMETERS = "Parameters"

class VEHICLE_TYPE(Enum):
    NAME = "name"
    ID = "id"
    CAPACITY = "capacity"
    FIXED_COST = "fixedCost"
    VAR_COST_DIST = "varCostDist"
    VAR_COST_TIME = "varCostTime"
    MAX_NUMBER = "maxNumber"
    START_POINT_ID = "startPointId"
    END_POINT_ID = "endPointId"
    TIME_WINDOWS_BEGIN = "TWbegin"
    TIME_WINDOWS_END= "TWend"

class POINT(Enum):
    NAME = "name"
    ID = "id"
    ID_CUSTOMER = "idCustomer"
    PENALTY = "penalty"
    COST = "cost"
    PENALTY_OR_COST = "penaltyOrCost"
    SERVICE_TIME = "serviceTime"
    DEMAND = "demand"
    CAPACITY = "capacity"
    DEMAND_OR_CAPACITY ="demandOrCapacity"
    INCOMPATIBLE_VEHICLES = "incompatibleVehicles"
    TIME_WINDOWS = "time windows"
    TIME_WINDOWS_BEGIN = "TWbegin"
    TIME_WINDOWS_END = "TWend"


class LINK(Enum):
        NAME = "name"
        IS_DIRECTED = "isDirected"
        START_POINT_ID = "startPointId"
        END_POINT_ID = "endPointId"
        DISTANCE = "distance"
        TIME = "time"
        FIXED_COST = "fixedCost"

class PARAMETERS(Enum):
        TIME_LIMIT = "timeLimit"
        UPPER_BOUND = "upperBound"
        HEURISTIC_USED = "heuristicUsed"
        TIME_LIMIT_HEURISTIC = "timeLimitHeuristic"
        CONFIG_FILE = "configFile"
        SOLVER_NAME = "solverName"
        PRINT_LEVEL = "printLevel"
        ACTION = "action"
        
class STATISTICS(Enum):
        SOLUTION_TIME = "solutionTime"
        SOLUTION_VALUE = "solutionValue"
        BEST_LOWER_BOUND = "bestLB"
        ROOT_LOWER_BOUND = "rootLB"
        ROOT_TIME = "rootTime"
        NB_BRANCH_AND_BOUND_NODES = "nbBranchAndBoundNodes"

class ROUTE(Enum):
        VEHICLE_TYPE_ID = "vehicleTypeId"
        ROUTE_COST = "routeCost"
        VISITED_POINTS = "visitedPoints"
        POINT_ID = "pointId"
        POINT_NAME = "pointName"
        LOAD = "load"
        TIME = "endTime"
        INCOMING_ARC_NAME = "incomingArcName"   

   
