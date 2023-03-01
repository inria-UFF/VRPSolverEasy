import sys, getopt,os
from os import walk


def generate_sh_files(argv):
    time_resolution = 30
    opts, args = getopt.getopt(argv,"t:p:")
   
    for opt, arg in opts:
        if opt == "-t":
            time_resolution = arg
        elif opt == "-p":
            path_project = os.path.abspath(arg)

    type_problem = ["CVRPTW","CVRP","HFVRP"]
    solver_names = ["CLP","CPLEX"]
    time_limits = [time_resolution]
    heuristic_used = ["yes","no"]
    #path_project = os.path.abspath(os.getcwd())
    if not (os.path.exists("jobs")):
        os.mkdir("jobs")
    for type in type_problem:
        path_data = path_project + os.path.normpath(
            "/VRPSolverEasy/demos/data/" + type )
        path_demos = path_project + os.path.normpath(
        "/VRPSolverEasy/ortools_demos/" + type )

        all_filenames = []
        for (dirpath, dirnames, filenames) in walk(path_data):
            all_filenames.extend(filenames)
        for name_file in filenames:
            for solver in solver_names:
                for time in time_limits:
                    for heuristic in heuristic_used :
                        instance_name = '{0}_{1}_{2}_{3}_{4}.sh'.format(
                                        type,
                                        name_file.split(".")[0],
                                        solver,
                                        time,
                                        heuristic)
                        with open("jobs/"+instance_name, "w") as f:
                            f.write(""" python3 {0}.py -i {1} -s {2} -h {3} -e {4} \n""".format(
                            path_demos,
                            os.path.normpath(path_data + "/" + name_file),
                            solver,
                            heuristic,
                            time))


if __name__ == "__main__":
   generate_sh_files(sys.argv[1:])
