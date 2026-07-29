##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         05-Jul-2026      ChatGPT                   Add SPHE_D_N examples with N as variable
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################

import copy
from SPHE_D import Examples_SPHE_D as _SPHE_D_examples


Example1 = {
    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'SPHE_D_N',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],  # N

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

            # Distributed temperature solver
            'SPHE_D_solver_M': 32,
            'Temp_tol': 0.0,

        }
    },
}
########################################################################
Example2 = {
    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'SPHE_D_N',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],  # N

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
            'Type_Equipment': 'SPHE_D_N',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],  # N

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
            'Type_Equipment': 'SPHE_D_N',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],  # N

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
            'Type_Equipment': 'SPHE_D_N',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],  # N

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
            'Type_Equipment': 'SPHE_D_N',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],  # N

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
