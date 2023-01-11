# import setup function from 
# python distribution utilities
from setuptools import setup,Extension
import sysconfig

data_path_str = sysconfig.get_path('data')
print("data_path_str", data_path_str)

# read the version number safely from the constants.py file
version_dict = {}
exec(open("VRPSolverReal/src/constants.py").read(), version_dict)
VERSION = version_dict["VERSION"]
readme_name = "README.md"
Description = open(readme_name).read()

# Calling the setup function
setup(
        name = 'VRPSolverReal',
        version = "0.0.1",
        author = "ERRAMI Najib SADYKOV Ruslan UCHOA Eduardo",
        email="najib.errami@inria.fr",
        description = 'VRPSolverReal is a simplified modeler solving routing problems by using Branch-Cut-and-Price approach on solver like CLP or CPLEX',
        long_description = Description,
        long_description_content_type='text/markdown',
        requires_python = ">=3.6",
        keywords=['VRP','Branch-Cut&Price','Linear Programming','routing problems','solver','Linear Programming'],
        packages=[
            "VRPSolverReal",
            "VRPSolverReal.src",
            "VRPSolverReal.tests",
            "VRPSolverReal.demos",
            "VRPSolverReal.doc",
            "VRPSolverReal.lib.Windows",
            "VRPSolverReal.lib.Linux",
            "VRPSolverReal.lib.Darwin",
        ],
        package_data={
            "VRPSolverReal.lib.Windows": ["*", "*.*"],
            "VRPSolverReal.lib.Linux": ["*", "*.*"],
            "VRPSolverReal.lib.Darwin": ["*", "*.*"]
        },
      	data_files={"VRPSolverReal/lib/Dependencies/libClp.so": ["local/libClp.so"],
      	"VRPSolverReal/lib/Dependencies/libClp.so.0": ["local/libClp.so.0"],
      	"VRPSolverReal/lib/Dependencies/libClp.so.0.0.0": ["local/libClp.so.0.0.0"],
      	"VRPSolverReal/lib/Dependencies/libCoinUtils.so": ["local/libCoinUtils.so"],
      	"VRPSolverReal/lib/Dependencies/libCoinUtils.so.0": ["local/libCoinUtils.so.0"],
      	"VRPSolverReal/lib/Dependencies/libCoinUtils.so.0.0.0": ["local/libCoinUtils.so.0.0.0"],
        },
        include_package_data=True,
        ext_modules= [
            Extension(
                'runtime_library_dirs',
                [
                    "VRPSolverReal/lib/Dependencies/",
                ]
            )
        ],
        entry_points=(
        """
        [console_scripts]
        VRPSolverRealTest = VRPSolverReal.tests.unit_tests:VRPSolverRealTestAll
        """
    ),

)

