## Experiments


### Installation dependencies

This folder includes the files that were used to launch the experiments. However, some packages are required to use these demos, in particular the [ortools](https://pypi.org/project/ortools/).  and 
[hygese](https://pypi.org/project/hygese/) packages.

So, you have to run this following command lines before to run demos :
    
    python -m pip install or-tools 
    python -m pip install hygese

There may be compiling compatibility errors. We invite you to browse the documentation of these packages to see if these packages are compatible with your version of python as well as your system.

### Run demos

Once you have installed dependencies, you can run demos like this :

    python3 /home/VRPSolverEasy/VRPSolverEasy/ortools_demos/CVRP.py -i /home/VRPSolverEasy/VRPSolverEasy/demos/data/CVRP/E-n101-k8.vrp -s CLP -h no -H yes -t 30

* -i : indicates the path of the instance 
* -s : indicates the name of the solver
* -h : indicates if you want to use or not heuristic in Bapcod
* -H : indicates if you want to use Vidalt heuristic to find initial upper bound
* -t : indicates the resolution time limit

