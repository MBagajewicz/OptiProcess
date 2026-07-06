##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         17-Feb-2025     Diego Oliva                STHE Examples Repository
#   0.2         28-Feb-2025     Alice Peccini              Relocating folders
#   0.3         26-Mar-2025     Mariana Mello              Update STHE examples
#   0.4         23-Apr-2025     Mariana Mello              Update STHE Model Parameters
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################

##################################################################################################################

# region Import Library
import numpy as np
import copy
# endregion

####################################################################################################################
####################################################################################################################

# region INPUT EXAMPLE 1 - SPHE_LMTD

Example1 = {
    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'SPHE_DT',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [6.6599, 6.9740, 7.6080, 8.6970, 9.9450, 10.8491, 12.6668, 15.2160, 16.9185, 17.4625, 21.6013, 25.2016, 30.2419, 36.3897, 40.3714, 46.6374, 51.0371, 56.7476, 65.4844, 74.2546],  # L

                [0.1016, 0.1524, 0.3048, 0.4572, 0.6096, 0.7620, 0.9144, 1.2192, 1.5240, 1.8288],  # H

                [0.2032, 0.3048],  # ds

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dh

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dc


            ],

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream-Case 1
            'Thi': 70,  # Inlet temperature of the hot stream (°C)
            'Tho': 47,  # Outlet temperature of the hot stream (°C)
            'mh': 0.83,           # Flow rate (kg*s**-1)
            'roh': 983.96,         # Density (kg*m**-3)
            'Cph': 4182.4,        # Heat capacity (J*(kg*K)**-1)
            'mih':  0.0004774,       # Viscosity (Pa*s)  1Pa*s = 1 N/m^2 * s = 1 kg*m/s^2/m^2 * s = 1 kg/(m*s)
            'kh': 0.6525,         # Thermal conductivity (W*(m*K)**-1)
            'Rfh':  1/15000,      # Fouling factor (m**2*°C*W**-1)
            'DPhdisp': 100e3,   # Available pressure drop =10e3(Pa)

            # Cold stream-Case 1
            'Tci': 29,  # Inlet temperature of the cold stream (°C)
            'Tco': 51,  # Outlet temperature of the cold stream (°C)
            'mc': 0.83,           # Flow rate (kg*s**-1)
            'roc': 992.22,         # Density (kg*m**-3)
            'Cpc': 4179.0,        # Heat capacity (J*(kg*K)**-1)
            'mic': 0.000653,      # Viscosity (Pa*s)
            'kc': 0.6310,          # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 1/15000,      # Fouling factor (m**2*°C*W**-1)
            'DPcdisp': 100e3,   # Available pressure drop =10e3(Pa)#


            'Thtarget': 46.5,

            # 动态计算的衍生参数（通过立即执行的lambda）
            'romax':0 ,
            'romin':0 ,
            'kmax': 0,
            'Cpmax':0 ,
            'mimin': 0,

            # Heat exchanger
            'kplate': 16.23,        # Tube wall thermal conductivity (W*(m*K)**-1)
            'thk': 2e-3,     # Tube thickness
            'yfluid': 2,        # Allocation, 1 = Cold stream in the tube side - 2 = Hot stream in the tube side

            # Problem
            'Aexc': 10,         # Area excess (%)
            'vhmax': 2,         # Upper bound on the shell-side velocity =2(m*s**(-1))
            'vhmin': 0.2,       # Lower bound on the shell-side velocity =0.2(m*s**(-1))
            'vcmax': 2,         # Upper bound on the tube-side velocity =2(m*s**(-1))
            'vcmin': 0.2,         # Lower bound on the tube-side velocity =0.2(m*s**(-1))
            # 'Recmin': 3.6e4,      # Lower bound on the tube-side Reynolds number
            # 'Rehmin': 3.6e4,      # Lower bound on the shell-side Reynolds number
            'LBLH': 20,          # Lower bound on L/H
            'UBLH': 40,         # Upper bound on L/H

            # Data Economic
            'par_a': 19687,    # Cost model parameter
            'par_b': 0.59,     # Cost model parameter
            'pc': 0.15,         # Energy price ($)
            'int_rate': 0.1,    # Interest rate
            'n': 5,            # Project horizon (years)
            'eta': 0.75,         # Pump efficiency
            'Nop': 8000,         # Number of hours of operation per year (h/y)

            # Distributed temperature solver parameters
            "SPHE_DT_solver_M": 32,
            "SPHE_DT_solver_tol": 1e-6,
            "SPHE_DT_solver_max_iter": 50,
            "SPHE_DT_solver_relaxation": 0.8,
            "SPHE_DT_require_convergence": False,

        }
    },
}
########################################################################
Example2 = {
    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'SPHE_DT',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [6.6599, 6.9740, 7.6080, 8.6970, 9.9450, 10.8491, 12.6668, 15.2160, 16.9185, 17.4625, 21.6013, 25.2016, 30.2419, 36.3897, 40.3714, 46.6374, 51.0371, 56.7476, 65.4844, 74.2546],  # L

                [0.1016, 0.1524, 0.3048, 0.4572, 0.6096, 0.7620, 0.9144, 1.2192, 1.5240, 1.8288],  # H

                [0.2032, 0.3048],  # ds

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dh

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dc


            ],

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream-Case 2
            'Thi': 80,  # Inlet temperature of the hot stream (°C)
            'Tho': 50,  # Outlet temperature of the hot stream (°C)
            'mh': 10.10,           # Flow rate (kg*s**-1)
            'roh': 786,         # Density (kg*m**-3)
            'Cph': 2177,        # Heat capacity (J*(kg*K)**-1)
            'mih':  0.00189,       # Viscosity (Pa*s)  1Pa*s = 1 N/m^2 * s = 1 kg*m/s^2/m^2 * s = 1 kg/(m*s)
            'kh': 0.12,         # Thermal conductivity (W*(m*K)**-1)
            'Rfh':  0.0002,      # Fouling factor (m**2*°C*W**-1)
            'DPhdisp': 1.450326323*6894.7572932,   # Available pressure drop =10e3(Pa)

            # Cold stream-Case 1
            'Tci': 30,  # Inlet temperature of the cold stream (°C)
            'Tco': 40,  # Outlet temperature of the cold stream (°C)
            'mc': 15.8,           # Flow rate (kg*s**-1)
            'roc': 995,         # Density (kg*m**-3)
            'Cpc': 4187.0,        # Heat capacity (J*(kg*K)**-1)
            'mic': 0.00072,      # Viscosity (Pa*s)
            'kc': 0.59,          # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.0003,      # Fouling factor (m**2*°C*W**-1)
            'DPcdisp': 1.450326323*6894.7572932,   # Available pressure drop =10e3(Pa)#


            'Thtarget': 46.5,

            # 动态计算的衍生参数（通过立即执行的lambda）
            'romax':0 ,
            'romin':0 ,
            'kmax': 0,
            'Cpmax':0 ,
            'mimin': 0,

            # Heat exchanger
            'kplate': 16.23,        # Tube wall thermal conductivity (W*(m*K)**-1)
            'thk': 2e-3,     # Tube thickness
            'yfluid': 2,        # Allocation, 1 = Cold stream in the tube side - 2 = Hot stream in the tube side

            # Problem
            'Aexc': 10,         # Area excess (%)
            'vhmax': 2,         # Upper bound on the shell-side velocity =2(m*s**(-1))
            'vhmin': 0.2,       # Lower bound on the shell-side velocity =0.2(m*s**(-1))
            'vcmax': 2,         # Upper bound on the tube-side velocity =2(m*s**(-1))
            'vcmin': 0.2,         # Lower bound on the tube-side velocity =0.2(m*s**(-1))
            # 'Recmin': 3.6e4,      # Lower bound on the tube-side Reynolds number
            # 'Rehmin': 3.6e4,      # Lower bound on the shell-side Reynolds number
            'LBLH': 20,          # Lower bound on L/H
            'UBLH': 40,         # Upper bound on L/H

            # Data Economic
            'par_a': 19687,    # Cost model parameter
            'par_b': 0.59,     # Cost model parameter
            'pc': 0.15,         # Energy price ($)
            'int_rate': 0.1,    # Interest rate
            'n': 5,            # Project horizon (years)
            'eta': 0.75,         # Pump efficiency
            'Nop': 8000         # Number of hours of operation per year (h/y)

        }
    },
}
########################################################################
Example3 = {
    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'SPHE_DT',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [6.6599, 6.9740, 7.6080, 8.6970, 9.9450, 10.8491, 12.6668, 15.2160, 16.9185, 17.4625, 21.6013, 25.2016, 30.2419, 36.3897, 40.3714, 46.6374, 51.0371, 56.7476, 65.4844, 74.2546],  # L

                [0.1016, 0.1524, 0.3048, 0.4572, 0.6096, 0.7620, 0.9144, 1.2192, 1.5240, 1.8288],  # H

                [0.2032, 0.3048],  # ds

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dh

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dc


            ],

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream-Case 3- Methanol
            'Thi': 70,  # Inlet temperature of the hot stream (°C)
            'Tho': 40,  # Outlet temperature of the hot stream (°C)
            'mh': 4.10,           # Flow rate (kg*s**-1)
            'roh': 750,         # Density (kg*m**-3)
            'Cph': 2840,        # Heat capacity (J*(kg*K)**-1)
            'mih':  0.00034,       # Viscosity (Pa*s)  1Pa*s = 1 N/m^2 * s = 1 kg*m/s^2/m^2 * s = 1 kg/(m*s)
            'kh': 0.019,         # Thermal conductivity (W*(m*K)**-1)
            'Rfh':  0.0002,      # Fouling factor (m**2*°C*W**-1)
            'DPhdisp': 1.450326323*6894.7572932,   # Available pressure drop =10e3(Pa)

            # Cold stream-Case 1
            'Tci': 30,  # Inlet temperature of the cold stream (°C)
            'Tco': 40,  # Outlet temperature of the cold stream (°C)
            'mc': 8.3,           # Flow rate (kg*s**-1)
            'roc': 995,         # Density (kg*m**-3)
            'Cpc': 4187.0,        # Heat capacity (J*(kg*K)**-1)
            'mic': 0.00072,      # Viscosity (Pa*s)
            'kc': 0.59,          # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.0002,      # Fouling factor (m**2*°C*W**-1)
            'DPcdisp': 1.450326323*6894.7572932,   # Available pressure drop =10e3(Pa)#


            'Thtarget': 46.5,

            # 动态计算的衍生参数（通过立即执行的lambda）
            'romax':0 ,
            'romin':0 ,
            'kmax': 0,
            'Cpmax':0 ,
            'mimin': 0,

            # Heat exchanger
            'kplate': 16.23,        # Tube wall thermal conductivity (W*(m*K)**-1)
            'thk': 2e-3,     # Tube thickness
            'yfluid': 2,        # Allocation, 1 = Cold stream in the tube side - 2 = Hot stream in the tube side

            # Problem
            'Aexc': 10,         # Area excess (%)
            'vhmax': 2,         # Upper bound on the shell-side velocity =2(m*s**(-1))
            'vhmin': 0.2,       # Lower bound on the shell-side velocity =0.2(m*s**(-1))
            'vcmax': 2,         # Upper bound on the tube-side velocity =2(m*s**(-1))
            'vcmin': 0.2,         # Lower bound on the tube-side velocity =0.2(m*s**(-1))
            # 'Recmin': 3.6e4,      # Lower bound on the tube-side Reynolds number
            # 'Rehmin': 3.6e4,      # Lower bound on the shell-side Reynolds number
            'LBLH': 20,          # Lower bound on L/H
            'UBLH': 40,         # Upper bound on L/H

            # Data Economic
            'par_a': 19687,    # Cost model parameter
            'par_b': 0.59,     # Cost model parameter
            'pc': 0.15,         # Energy price ($)
            'int_rate': 0.1,    # Interest rate
            'n': 5,            # Project horizon (years)
            'eta': 0.75,         # Pump efficiency
            'Nop': 8000         # Number of hours of operation per year (h/y)

        }
    },
}
########################################################################
Example4 = {
    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'SPHE_DT',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [6.6599, 6.9740, 7.6080, 8.6970, 9.9450, 10.8491, 12.6668, 15.2160, 16.9185, 17.4625, 21.6013, 25.2016, 30.2419, 36.3897, 40.3714, 46.6374, 51.0371, 56.7476, 65.4844, 74.2546],  # L

                [0.1016, 0.1524, 0.3048, 0.4572, 0.6096, 0.7620, 0.9144, 1.2192, 1.5240, 1.8288],  # H

                [0.2032, 0.3048],  # ds

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dh

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dc


            ],

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream-Case 4- methanol
            'Thi': 100,  # Inlet temperature of the hot stream (°C)
            'Tho': 40,  # Outlet temperature of the hot stream (°C)
            'mh': 0.66,           # Flow rate (kg*s**-1)
            'roh': 750,         # Density (kg*m**-3)
            'Cph': 2840,        # Heat capacity (J*(kg*K)**-1)
            'mih':  0.00034,       # Viscosity (Pa*s)  1Pa*s = 1 N/m^2 * s = 1 kg*m/s^2/m^2 * s = 1 kg/(m*s)
            'kh': 0.19,         # Thermal conductivity (W*(m*K)**-1)
            'Rfh':  0.0002,      # Fouling factor (m**2*°C*W**-1)
            'DPhdisp': 1.450326323*6894.7572932,   # Available pressure drop =10e3(Pa)

            # Cold stream-Case 4 - Cold Water
            'Tci': 32,  # Inlet temperature of the cold stream (°C)
            'Tco': 40,  # Outlet temperature of the cold stream (°C)
            'mc': 3.3,           # Flow rate (kg*s**-1)
            'roc': 995,         # Density (kg*m**-3)
            'Cpc': 4187.0,        # Heat capacity (J*(kg*K)**-1)
            'mic': 0.00072,      # Viscosity (Pa*s)
            'kc': 0.59,          # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.0004,      # Fouling factor (m**2*°C*W**-1)
            'DPcdisp': 1.450326323*6894.7572932,   # Available pressure drop =10e3(Pa)#


            'Thtarget': 46.5,

            # 动态计算的衍生参数（通过立即执行的lambda）
            'romax':0 ,
            'romin':0 ,
            'kmax': 0,
            'Cpmax':0 ,
            'mimin': 0,

            # Heat exchanger
            'kplate': 16.23,        # Tube wall thermal conductivity (W*(m*K)**-1)
            'thk': 2e-3,     # Tube thickness
            'yfluid': 2,        # Allocation, 1 = Cold stream in the tube side - 2 = Hot stream in the tube side

            # Problem
            'Aexc': 10,         # Area excess (%)
            'vhmax': 2,         # Upper bound on the shell-side velocity =2(m*s**(-1))
            'vhmin': 0.2,       # Lower bound on the shell-side velocity =0.2(m*s**(-1))
            'vcmax': 2,         # Upper bound on the tube-side velocity =2(m*s**(-1))
            'vcmin': 0.2,         # Lower bound on the tube-side velocity =0.2(m*s**(-1))
            # 'Recmin': 3.6e4,      # Lower bound on the tube-side Reynolds number
            # 'Rehmin': 3.6e4,      # Lower bound on the shell-side Reynolds number
            'LBLH': 20,          # Lower bound on L/H
            'UBLH': 40,         # Upper bound on L/H

            # Data Economic
            'par_a': 19687,    # Cost model parameter
            'par_b': 0.59,     # Cost model parameter
            'pc': 0.15,         # Energy price ($)
            'int_rate': 0.1,    # Interest rate
            'n': 5,            # Project horizon (years)
            'eta': 0.75,         # Pump efficiency
            'Nop': 8000         # Number of hours of operation per year (h/y)

        }
    },
}
########################################################################
Example5 = {
    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'SPHE_DT',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [6.6599, 6.9740, 7.6080, 8.6970, 9.9450, 10.8491, 12.6668, 15.2160, 16.9185, 17.4625, 21.6013, 25.2016, 30.2419, 36.3897, 40.3714, 46.6374, 51.0371, 56.7476, 65.4844, 74.2546],  # L

                [0.1016, 0.1524, 0.3048, 0.4572, 0.6096, 0.7620, 0.9144, 1.2192, 1.5240, 1.8288],  # H

                [0.2032, 0.3048],  # ds

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dh

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dc


            ],

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream-Case 5- Hot Water
            'Thi': 220,  # Inlet temperature of the hot stream (°C)
            'Tho': 110.2,  # Outlet temperature of the hot stream (°C)
            'mh': 10.10,           # Flow rate (kg*s**-1)
            'roh': 888,         # Density (kg*m**-3)
            'Cph': 4312,        # Heat capacity (J*(kg*K)**-1)
            'mih':  0.00015,       # Viscosity (Pa*s)  1Pa*s = 1 N/m^2 * s = 1 kg*m/s^2/m^2 * s = 1 kg/(m*s)
            'kh': 0.70,         # Thermal conductivity (W*(m*K)**-1)
            'Rfh':  0.0001,      # Fouling factor (m**2*°C*W**-1)
            'DPhdisp': 1.450326323*6894.7572932,   # Available pressure drop =10e3(Pa)

            # Cold stream-Case 5- Methanol
            'Tci': 30,  # Inlet temperature of the cold stream (°C)
            'Tco': 80,  # Outlet temperature of the cold stream (°C)
            'mc': 2.9,           # Flow rate (kg*s**-1)
            'roc': 750,         # Density (kg*m**-3)
            'Cpc': 2840,        # Heat capacity (J*(kg*K)**-1)
            'mic': 0.00034,      # Viscosity (Pa*s)
            'kc': 0.19,          # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.0001,      # Fouling factor (m**2*°C*W**-1)
            'DPcdisp': 1.450326323*6894.7572932,   # Available pressure drop =10e3(Pa)#


            'Thtarget': 46.5,

            # 动态计算的衍生参数（通过立即执行的lambda）
            'romax':0 ,
            'romin':0 ,
            'kmax': 0,
            'Cpmax':0 ,
            'mimin': 0,

            # Heat exchanger
            'kplate': 16.23,        # Tube wall thermal conductivity (W*(m*K)**-1)
            'thk': 2e-3,     # Tube thickness
            'yfluid': 2,        # Allocation, 1 = Cold stream in the tube side - 2 = Hot stream in the tube side

            # Problem
            'Aexc': 10,         # Area excess (%)
            'vhmax': 2,         # Upper bound on the shell-side velocity =2(m*s**(-1))
            'vhmin': 0.2,       # Lower bound on the shell-side velocity =0.2(m*s**(-1))
            'vcmax': 2,         # Upper bound on the tube-side velocity =2(m*s**(-1))
            'vcmin': 0.2,         # Lower bound on the tube-side velocity =0.2(m*s**(-1))
            # 'Recmin': 3.6e4,      # Lower bound on the tube-side Reynolds number
            # 'Rehmin': 3.6e4,      # Lower bound on the shell-side Reynolds number
            'LBLH': 20,          # Lower bound on L/H
            'UBLH': 40,         # Upper bound on L/H

            # Data Economic
            'par_a': 19687,    # Cost model parameter
            'par_b': 0.59,     # Cost model parameter
            'pc': 0.15,         # Energy price ($)
            'int_rate': 0.1,    # Interest rate
            'n': 5,            # Project horizon (years)
            'eta': 0.75,         # Pump efficiency
            'Nop': 8000         # Number of hours of operation per year (h/y)

        }
    },
}
########################################################################
Example6 = {
    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'SPHE_DT',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [6.6599, 6.9740, 7.6080, 8.6970, 9.9450, 10.8491, 12.6668, 15.2160, 16.9185, 17.4625, 21.6013, 25.2016, 30.2419, 36.3897, 40.3714, 46.6374, 51.0371, 56.7476, 65.4844, 74.2546],  # L

                [0.1016, 0.1524, 0.3048, 0.4572, 0.6096, 0.7620, 0.9144, 1.2192, 1.5240, 1.8288],  # H

                [0.2032, 0.3048],  # ds

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dh

                [0.0048, 0.0064, 0.0079, 0.0095, 0.0127, 0.0159, 0.0191, 0.0254],  # dc


            ],

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream-Case 6-Ethanol
            'Thi': 150,  # Inlet temperature of the hot stream (°C)
            'Tho': 60,  # Outlet temperature of the hot stream (°C)
            'mh': 1.71,           # Flow rate (kg*s**-1)
            'roh': 789,         # Density (kg*m**-3)
            'Cph': 2470,        # Heat capacity (J*(kg*K)**-1)
            'mih':  0.00067,       # Viscosity (Pa*s)  1Pa*s = 1 N/m^2 * s = 1 kg*m/s^2/m^2 * s = 1 kg/(m*s)
            'kh': 0.17,         # Thermal conductivity (W*(m*K)**-1)
            'Rfh':  0.0002,      # Fouling factor (m**2*°C*W**-1)
            'DPhdisp': 1.450326323*6894.7572932*10,   # Available pressure drop =10e3(Pa)

            # Cold stream-Case 6- Cold Water
            'Tci': 30,  # Inlet temperature of the cold stream (°C)
            'Tco': 40,  # Outlet temperature of the cold stream (°C)
            'mc': 9.1,           # Flow rate (kg*s**-1)
            'roc': 995,         # Density (kg*m**-3)
            'Cpc': 4187.0,        # Heat capacity (J*(kg*K)**-1)
            'mic': 0.00072,      # Viscosity (Pa*s)
            'kc': 0.59,          # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.0004,      # Fouling factor (m**2*°C*W**-1)
            'DPcdisp': 1.450326323*6894.7572932*10,   # Available pressure drop =10e3(Pa)#


            'Thtarget': 46.5,

            # 动态计算的衍生参数（通过立即执行的lambda）
            'romax':0 ,
            'romin':0 ,
            'kmax': 0,
            'Cpmax':0 ,
            'mimin': 0,

            # Heat exchanger
            'kplate': 16.23,        # Tube wall thermal conductivity (W*(m*K)**-1)
            'thk': 2e-3,     # Tube thickness
            'yfluid': 2,        # Allocation, 1 = Cold stream in the tube side - 2 = Hot stream in the tube side

            # Problem
            'Aexc': 10,         # Area excess (%)
            'vhmax': 2,         # Upper bound on the shell-side velocity =2(m*s**(-1))
            'vhmin': 0.2,       # Lower bound on the shell-side velocity =0.2(m*s**(-1))
            'vcmax': 2,         # Upper bound on the tube-side velocity =2(m*s**(-1))
            'vcmin': 0.2,         # Lower bound on the tube-side velocity =0.2(m*s**(-1))
            # 'Recmin': 3.6e4,      # Lower bound on the tube-side Reynolds number
            # 'Rehmin': 3.6e4,      # Lower bound on the shell-side Reynolds number
            'LBLH': 20,          # Lower bound on L/H
            'UBLH': 40,         # Upper bound on L/H

            # Data Economic
            'par_a': 19687,    # Cost model parameter
            'par_b': 0.59,     # Cost model parameter
            'pc': 0.15,         # Energy price ($)
            'int_rate': 0.1,    # Interest rate
            'n': 5,            # Project horizon (years)
            'eta': 0.75,         # Pump efficiency
            'Nop': 8000         # Number of hours of operation per year (h/y)

        }
    },
}
########################################################################
####################################################################################################################
# region SPHE_DT temperature-dependent property functions

from SPHE_DT.Calculations.Calculations_SPHE_DT_Properties import (
    conductivity_linear_from_reference,
    cp_linear_from_reference,
    density_linear_from_reference,
    viscosity_exponential_from_reference,
)


def _attach_temperature_dependent_properties(example):
    """Attach property callables to Model_Parameters for the SPHE_DT branch.

    The functions are deliberately passed through Model_Parameters, so each
    example can later replace them with fluid-specific correlations without
    changing the solver or constraints.
    """
    m_p = example["Equipment1"]["Model_Parameters"]
    Th_ref = 0.5 * (m_p["Thi"] + m_p["Tho"])
    Tc_ref = 0.5 * (m_p["Tci"] + m_p["Tco"])

    m_p["hot_cp_func"] = cp_linear_from_reference(m_p["Cph"], Th_ref, slope=1.0, min_value=1.0)
    m_p["hot_density_func"] = density_linear_from_reference(m_p["roh"], Th_ref, slope=-0.6, min_value=1.0)
    m_p["hot_viscosity_func"] = viscosity_exponential_from_reference(m_p["mih"], Th_ref, beta=0.015, min_value=1e-7)
    m_p["hot_conductivity_func"] = conductivity_linear_from_reference(m_p["kh"], Th_ref, slope=0.0002, min_value=1e-4)

    m_p["cold_cp_func"] = cp_linear_from_reference(m_p["Cpc"], Tc_ref, slope=1.0, min_value=1.0)
    m_p["cold_density_func"] = density_linear_from_reference(m_p["roc"], Tc_ref, slope=-0.6, min_value=1.0)
    m_p["cold_viscosity_func"] = viscosity_exponential_from_reference(m_p["mic"], Tc_ref, beta=0.015, min_value=1e-7)
    m_p["cold_conductivity_func"] = conductivity_linear_from_reference(m_p["kc"], Tc_ref, slope=0.0002, min_value=1e-4)

    m_p["SPHE_DT_property_temperature_mode"] = "target_average"
    m_p["SPHE_DT_solver_M"] = 2
    m_p["SPHE_DT_solver_tol"] = 1e-4
    m_p["SPHE_DT_solver_max_iter"] = 10
    m_p["SPHE_DT_solver_relaxation"] = 0.8
    m_p["SPHE_DT_require_convergence"] = False
    m_p["SPHE_DT_use_lmtd_screen"] = True
    m_p["SPHE_DT_use_fast_temperature_screen"] = True
    m_p["SPHE_DT_fast_screen_M"] = 2
    m_p["SPHE_DT_fast_screen_max_iter"] = 1
    m_p["SPHE_DT_screen_temp_tol"] = 10.0


for _example in (Example1, Example2, Example3, Example4, Example5, Example6):
    _attach_temperature_dependent_properties(_example)

# endregion
####################################################################################################################
