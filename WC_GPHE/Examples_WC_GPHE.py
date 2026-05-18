##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#  0.0         05-Mar-2025       Mariana Mello             Water Cooler Examples Repository
#  0.2         12-May-2025       Mariana Mello             Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
#  0.3         29-Sep-2025       Mariana Mello             Add example 2
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of Water Cooler in this file
##################################################################################################################

# region Import Library
import numpy as np
# endregion

##################################################################################################################
##################################################################################################################

# region INPUT EXAMPLE 1 - Water Cooler GPHE

Example1 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'WC_GPHE',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                list(range(10, 800 + 1)),  # Ntp - total number of plates
                # (minimum number of plates -> maximum number of plates)
                # NumbPlatesMin = 10
                # NumbPlatesMax = 800

                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # Pl - Plate size (options of Lp, Lw, Dp)

                [30, 45, 50, 60, 65],  # Sa - Chevron angle

                [1, 2],  # Nph - Number of passes of hot stream

                [1, 2]  # Npc - number of passes of cold stream

            ],

            'Selected_OF': ['TAC_OF'],  # TAC_OF

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream
            'mh': 30,         # Flow rate (kg*s**-1)
            'roh': 900,       # Density (kg*m**-3)
            'Cph': 2670,      # Heat capacity (J*(kg*K)**-1)
            'mih': 0.00086,   # Viscosity (Pa*s)
            'kh': 0.1,        # Thermal conductivity (W*(m*K)**-1)
            'Rfh': 0.0002,    # Fouling factor (m**2*oC*W**-1)
            'DPhdisp': 1,     # Available pressure drop (Pa)

            # Cold stream
            'roc': 1000,      # Density (kg*m**-3)
            'Cpc': 4184,      # Heat capacity (J*(kg*K)**-1)
            'mic': 0.0008,    # Viscosity (Pa*s)
            'kc': 0.6,        # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.00009,   # Fouling factor (m**2*oC*W**-1)
            'DPcdisp': 1,     # Available pressure drop (Pa)

            # Data of heat exchanger
            'kplate': 16.2,     # Thermal conductivity of plate (W*(m*K)**-1)
            'thk': 0.0008,      # Thickness
            'phi': 1.15,        # The surface enlargement factor
            'bp': 0.003,        # Plate gap

            # Problem
            'Aexc': 10,         # Area excess (%)
            'Tci': 20,          # Inlet temperature of the cold stream (oC)
            'Thi': 190,         # Inlet temperature of the hot stream (oC)
            'Tho': 120,         # Outlet temperature of the hot stream (oC)
            'vhmax': 0.9,       # Upper bound on the hot stream velocity (m*s**(-1))
            'vhmin': 0.3,       # Lower bound on the hot stream velocity (m*s**(-1))
            'vcmax': 0.9,       # Upper bound on the cold stream velocity (m*s**(-1))
            'vcmin': 0.3,       # Lower bound on the cold stream velocity (m*s**(-1))
            'Recmin': 2500,     # Lower bound on the tube-side Reynolds number
            'Recmax': 124000,   # Upper bound on the tube-side Reynolds number
            'Rehmin': 0,        # Lower bound on the shell-side Reynolds number
            'Rehmax': 100000,   # Upper bound on the shell-side Reynolds number

            'ppLp': np.array([0.743, 0.978, 1.281, 1.50, 1.835, 2.092, 1.551, 0.400, 1.845, 1.543]),
            # Plate length (m)
            'ppLw': np.array([0.845, 0.812, 1.200, 1.22, 0.945, 1.200, 0.909, 0.125, 0.450, 0.812]),
            # Plate width (m)
            'ppDp': np.array([0.3, 0.288, 0.4, 0.35, 0.3, 0.4, 0.285, 0.03, 0.155, 0.283]),
            # Port diameter (m)

            # Parameters of Water Cooler model
            'Fw_max': 150,      # Maximum cooling water (kg/s)
            'Tco_max': 50,      # Maximum cooler water outlet temperature (°C)

            # Data Economic
            'cf': 8500,         # The exchanger fixed cost
            'cv': 409,          # The area cost coefficient of the exchanger cost
            'alpha': 0.85,      # Model economic parameter
            'pc': 0.069,        # Energy price ($/kWh)
            'pcw': 0.00002,     # Unit price of cooling water ($/kg)
            'int_rate': 0.02,   # Interest rate
            'n': 20,            # Project horizon (years)
            'eta': 0.6,         # Pump efficiency
            'Nop': 7896         # Number of hours of operation per year (h/y)
        }
    }
}

# endregion

##########################################################################################################

# region INPUT EXAMPLE 2 - Water Cooler GPHE

Example2 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'WC_GPHE',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                list(range(10, 800 + 1)),  # Ntp - total number of plates
                # (minimum number of plates -> maximum number of plates)
                # NumbPlatesMin = 10
                # NumbPlatesMax = 800

                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # Pl - Plate size (options of Lp, Lw, Dp)

                [30, 45, 50, 60, 65],  # Sa - Chevron angle

                [1, 2],  # Nph - Number of passes of hot stream

                [1, 2]  # Npc - number of passes of cold stream

            ],

            'Selected_OF': ['TAC_OF'],  # TAC_OF

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream
            'mh': 17.36,  # Flow rate (kg*s**-1)
            'roh': 784.714,  # Density (kg*m**-3)
            'Cph': 2279.48,  # Heat capacity (J*(kg*K)**-1)
            'mih': 0.00085,  # Viscosity (Pa*s)
            'kh': 0.07785,  # Thermal conductivity (W*(m*K)**-1)
            'Rfh': 0.00011,  # Fouling factor (m**2*oC*W**-1)
            'DPhdisp': 1,     # Available pressure drop (Pa)

            # Cold stream
            'roc': 1000,  # Density (kg*m**-3)
            'Cpc': 4184,  # Heat capacity (J*(kg*K)**-1)
            'mic': 0.0008,  # Viscosity (Pa*s)
            'kc': 0.6,  # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.00009,  # Fouling factor (m**2*oC*W**-1)
            'DPcdisp': 1,     # Available pressure drop (Pa)

            # Data of heat exchanger
            'kplate': 16.2,     # Thermal conductivity of plate (W*(m*K)**-1)
            'thk': 0.0008,      # Thickness
            'phi': 1.15,        # The surface enlargement factor
            'bp': 0.003,        # Plate gap

            # Problem
            'Aexc': 10,         # Area excess (%)
            'Tci': 20,          # Inlet temperature of the cold stream (oC)
            'Thi': 146.15,      # Inlet temperature of the hot stream (oC)
            'Tho': 40,          # Outlet temperature of the hot stream (oC)
            'DeltaT_min': 5,    # The minimum approach
            'vhmax': 0.9,       # Upper bound on the hot stream velocity (m*s**(-1))
            'vhmin': 0.3,       # Lower bound on the hot stream velocity (m*s**(-1))
            'vcmax': 0.9,       # Upper bound on the cold stream velocity (m*s**(-1))
            'vcmin': 0.3,       # Lower bound on the cold stream velocity (m*s**(-1))
            'Recmin': 2500,     # Lower bound on the tube-side Reynolds number
            'Recmax': 124000,   # Upper bound on the tube-side Reynolds number
            'Rehmin': 0,        # Lower bound on the shell-side Reynolds number
            'Rehmax': 100000,   # Upper bound on the shell-side Reynolds number

            'ppLp': np.array([0.743, 0.978, 1.281, 1.50, 1.835, 2.092, 1.551, 0.400, 1.845, 1.543]),
            # Plate length (m)
            'ppLw': np.array([0.845, 0.812, 1.200, 1.22, 0.945, 1.200, 0.909, 0.125, 0.450, 0.812]),
            # Plate width (m)
            'ppDp': np.array([0.3, 0.288, 0.4, 0.35, 0.3, 0.4, 0.285, 0.03, 0.155, 0.283]),
            # Port diameter (m)

            # Parameters of Water Cooler model
            'Fw_max': 150,      # Maximum cooling water (kg/s)
            'Tco_max': 50,      # Maximum cooler water outlet temperature (°C)

            # Data Economic
            'cf': 8500,         # The exchanger fixed cost
            'cv': 409,          # The area cost coefficient of the exchanger cost
            'alpha': 0.85,      # Model economic parameter
            'pc': 0.069,        # Energy price ($/kWh)
            'pcw': 0.00002,     # Unit price of cooling water ($/kg)
            'int_rate': 0.02,   # Interest rate
            'n': 20,            # Project horizon (years)
            'eta': 0.6,         # Pump efficiency
            'Nop': 7896         # Number of hours of operation per year (h/y)
        }
    }
}

# endregion
