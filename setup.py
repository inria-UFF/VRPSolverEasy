# import setup function from 
# python distribution utilities
from setuptools import setup,Extension
import sysconfig

# read the version number safely from the constants.py file
version_dict = {}
exec(open("VRPSolverEasy/src/constants.py").read(), version_dict)
VERSION = version_dict["VERSION"]
readme_name = "README.md"
Description = open(readme_name).read()

# Calling the setup function
setup(
        name = 'VRPSolverEasy',
        version = VERSION,
        author = "ERRAMI Najib SADYKOV Ruslan UCHOA Eduardo QUEIROGA Eduardo",
        author_email="najib.errami@inria.fr",
        url="https://vrpsolvereasy.readthedocs.io/en/latest/",
        description = 'VRPSolverEasy is a simplified modeler solving routing problems by using Branch-Cut-and-Price approach on solver like CLP or CPLEX',
        long_description = Description,
        long_description_content_type='text/markdown',
        python_requires = ">=3.7",
        keywords=['VRP','Branch-Cut&Price','Linear Programming','routing problems','solver','Linear Programming'],
        install_requires=[
           'setuptools>=58.1.0'
        ],
        packages=[
            "VRPSolverEasy",
            "VRPSolverEasy.src",
            "VRPSolverEasy.tests",
            "VRPSolverEasy.demos",
            "VRPSolverEasy.lib.Windows",
            "VRPSolverEasy.lib.Linux",
            "VRPSolverEasy.lib.Darwin",
        ],
        package_data={
            "VRPSolverEasy.lib.Windows": ["*", "*.*"],
            "VRPSolverEasy.lib.Linux": ["*", "*.*"],
            "VRPSolverEasy.lib.Darwin": ["*", "*.*"]
        },
        include_package_data=True,
        entry_points=(
        """
        [console_scripts]
        VRPSolverEasyTest = VRPSolverEasy.tests.unit_tests:VRPSolverEasyTestAll
        """
    ),

)

