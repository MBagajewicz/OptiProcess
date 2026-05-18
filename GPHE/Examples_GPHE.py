##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         17-Feb-2025     Diego Oliva                GPHE Examples Repository
#   0.2         28-Feb-2025     Alice Peccini              Relocating folders
#   0.3         26-Mar-2025     Mariana Mello              Update examples
#   0.4         12-May-2025     Mariana Mello              Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# region INSTRUCTIONS
# Add Examples of GPHE in this file
'''
This is a GPHE Model Examples File, Set Trimming is applied.

The main structure of the dictionary is:

ExampleX = {

    'Number_of_Equipment': N,

    'Equipment1': {}

    'Equipment2': {}

         ...

    'EquipmentN': {}

}

For each 'GPHE' Type_Equipment the following data are required:

'EquipmentN': {

    'Model_Declarations': {

        'Type_Equipment': 'GPHE',

        'Discrete_Values_of_Variables': [
                list(range(NumbPlatesMin, NumbPlatesMax + 1)),   # Ntp - total number of plates
                                                                 # (minimum number of plates -> maximum number of plates)

                [],            # Pl - Plate size (options of Lp, Lw, Dp)

                [],            # Sa - Chevron angle

                [],            # Nph - Number of passes of hot stream

                []             # Npc - number of passes of cold stream
    },

    'Model_Parameters': {

            # Hot stream
            'mh': ,              # Flow rate (kg*s**-1)
            'roh': ,             # Density (kg*m**-3)
            'Cph': ,             # Heat capacity (J*(kg*K)**-1)
            'mih': ,             # Viscosity (Pa*s)
            'kh': ,              # Thermal conductivity (W*(m*K)**-1)
            'Rfh': ,             # Fouling factor (m**2*oC*W**-1)
            'DPhdisp': ,         # Available pressure drop (Pa)

            # Cold stream
            'mc': ,              # Flow rate (kg*s**-1)
            'roc': ,             # Density (kg*m**-3)
            'Cpc': ,             # Heat capacity (J*(kg*K)**-1)
            'mic': ,             # Viscosity (Pa*s)
            'kc': ,              # Thermal conductivity (W*(m*K)**-1)
            'Rfc': ,             # Fouling Factor (m**2*oC*W**-1)
            'DPcdisp': ,         # Available pressure drop (Pa)

            # Data of heat exchanger
            'kplate': ,          # Thermal conductivity of plate (W*(m*K)**-1)
            'thk': ,             # Thickness
            'phi': ,             # The surface enlargement factor
            'bp': ,              # Plate gap

            # Problem data
            'Aexc': ,            # Area excess (%)
            'Tci': ,             # Inlet temperature of the cold stream (oC)
            'Tco': ,             # Outlet temperature of the cold stream (oC)
            'Thi': ,             # Inlet temperature of the hot stream (oC)
            'Tho': ,             # Outlet temperature of the hot stream (oC)
            'vhmax': ,           # Upper bound on the hot stream velocity (m*s**(-1))
            'vhmin': ,           # Lower bound on the hot stream velocity (m*s**(-1))
            'vcmax': ,           # Upper bound on the cold stream velocity (m*s**(-1))
            'vcmin': ,           # Lower bound on the cold stream velocity (m*s**(-1))

            'ppLp': np.array([ , , , , , , , , , ]),  # Plate length (m)
            'ppLw': np.array([ , , , , , , , , , ]),  # Plate width (m)
            'ppDp': np.array([ , , , , , , , , , ]),  # Port diameter (m)

            # Economic data
            'par_a': ,           # Cost model parameter
            'par_b': ,           # Cost model parameter
            'pc': ,              # Energy price ($)
            'int_rate': ,        # Interest rate
            'n': ,               # Project horizon (years)
            'eta': ,             # Pump efficiency
            'Nop':               # Number of hours of operation per year (h/y)

    }
}
'''
# endregion
##################################################################################################################

# region Import Library
import numpy as np
#import copy
# endregion

####################################################################################################################
####################################################################################################################

# region INPUT EXAMPLE 1 - GPHE

Example1 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'GPHE',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                list(range(10, 800 + 1)),        # Ntp - total number of plates
                                                 # (minimum number of plates -> maximum number of plates)
                                                 # NumbPlatesMin = 10
                                                 # NumbPlatesMax = 800

                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # Pl - Plate size (options of Lp, Lw, Dp)

                [30, 45, 50, 60, 65],            # Sa - Chevron angle

                [1, 2],                          # Nph - Number of passes of hot stream

                [1, 2]                           # Npc - number of passes of cold stream

            ],

            'Selected_OF': ['TAC_OF'],  # TAC_OF or AREA_OF or CAPEX_OF
            
        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        # in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream
            'mh': 60,               # Flow rate (kg*s**-1)
            'roh': 995,             # Density (kg*m**-3)
            'Cph': 4187,            # Heat capacity (J*(kg*K)**-1)
            'mih': 0.0005,          # Viscosity (Pa*s)
            'kh': 0.6,              # Thermal conductivity (W*(m*K)**-1)
            'Rfh': 0.0007,          # Fouling factor (m**2*oC*W**-1)
            'DPhdisp': 0.7,         # Available pressure drop (Pa)

            # Cold stream
            'mc': 80,               # Flow rate (kg*s**-1)
            'roc': 985,             # Density (kg*m**-3)
            'Cpc': 4183,            # Heat capacity (J*(kg*K)**-1)
            'mic': 0.005,           # Viscosity (Pa*s)
            'kc': 0.6,              # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.0006,          # Fouling Factor (m**2*oC*W**-1)
            'DPcdisp': 0.7,         # Available pressure drop (Pa)

            # Data of heat exchanger
            'kplate': 16.2,         # Thermal conductivity of plate (W*(m*K)**-1)
            'thk': 0.0008,          # Thickness
            'phi': 1.15,            # The surface enlargement factor
            'bp': 0.003,            # Plate gap

            # Problem data
            'Aexc': 11,             # Area excess (%)
            'Tci': 25,              # Inlet temperature of the cold stream (oC)
            'Tco': 31.8,            # Outlet temperature of the cold stream (oC)
            'Thi': 56,              # Inlet temperature of the hot stream (oC)
            'Tho': 47,              # Outlet temperature of the hot stream (oC)
            'vhmax': 0.9,           # Upper bound on the hot stream velocity (m*s**(-1))
            'vhmin': 0.3,           # Lower bound on the hot stream velocity (m*s**(-1))
            'vcmax': 0.9,           # Upper bound on the cold stream velocity (m*s**(-1))
            'vcmin': 0.3,           # Lower bound on the cold stream velocity (m*s**(-1))

            'ppLp': np.array([0.743, 0.978, 1.281, 1.50, 1.835, 2.092, 1.551, 0.400, 1.845, 1.543]),
            # Plate length (m)
            'ppLw': np.array([0.845, 0.812, 1.200, 1.22, 0.945, 1.200, 0.909, 0.125, 0.450, 0.812]),
            # Plate width (m)
            'ppDp': np.array([0.3, 0.288, 0.4, 0.35, 0.3, 0.4, 0.285, 0.03, 0.155, 0.283]),
            # Port diameter (m)

            # Economic data
            'par_a': 635.14,        # Cost model parameter
            'par_b': 0.778,         # Cost model parameter
            'pc': 0.15,             # Energy price ($)
            'int_rate': 0.1,        # Interest rate
            'n': 10,                # Project horizon (years)
            'eta': 0.6,             # Pump efficiency
            'Nop': 7500             # Number of hours of operation per year (h/y)
        }
    }
    
}

# endregion

###################################################################################################################
###################################################################################################################

# region INPUT EXAMPLE 2 - GPHE Example 6 from NAHES et al ()

Example2 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'GPHE',

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

            'Selected_OF': ['TAC_OF'],  # TAC_OF or AREA_OF or CAPEX_OF

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        # in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream
            'mh': 55.6,         # Flow rate (kg*s**-1)
            'roh': 789,         # Density (kg*m**-3)
            'Cph': 2470,        # Heat capacity (J*(kg*K)**-1)
            'mih': 0.00067,     # Viscosity (Pa*s)
            'kh': 0.17,         # Thermal conductivity (W*(m*K)**-1)
            'Rfh': 0.0002,      # Fouling factor (m**2*oC*W**-1)
            'DPhdisp': 0.7,     # Available pressure drop (Pa)

            # Cold stream
            'mc': 295,         # Flow rate (kg*s**-1)
            'roc': 995,         # Density (kg*m**-3)
            'Cpc': 4187,        # Heat capacity (J*(kg*K)**-1)
            'mic': 0.00072,     # Viscosity (Pa*s)
            'kc': 0.59,         # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.0004,      # Fouling factor (m**2*oC*W**-1)
            'DPcdisp': 0.7,     # Available pressure drop (Pa)

            # Data of heat exchanger
            'kplate': 16.2,     # Thermal conductivity of plate (W*(m*K)**-1)
            'thk': 0.0008,      # Thickness
            'phi': 1.15,        # The surface enlargement factor
            'bp': 0.003,        # Plate gap

            # Problem data
            'Aexc': 11,         # Area excess (%)
            'Tci': 30,          # Inlet temperature of the cold stream (oC)
            'Tco': 40,          # Outlet temperature of the cold stream (oC)
            'Thi': 150,         # Inlet temperature of the hot stream (oC)
            'Tho': 60,          # Outlet temperature of the hot stream (oC)
            'vhmax': 0.9,       # Upper bound on the hot stream velocity (m*s**(-1))
            'vhmin': 0.3,       # Lower bound on the hot stream velocity (m*s**(-1))
            'vcmax': 0.9,       # Upper bound on the cold stream velocity (m*s**(-1))
            'vcmin': 0.3,       # Lower bound on the cold stream velocity (m*s**(-1))

            'ppLp': np.array([0.743, 0.978, 1.281, 1.50, 1.835, 2.092, 1.551, 0.400, 1.845, 1.543]),
            # Plate length (m)
            'ppLw': np.array([0.845, 0.812, 1.200, 1.22, 0.945, 1.200, 0.909, 0.125, 0.450, 0.812]),
            # Plate width (m)
            'ppDp': np.array([0.3, 0.288, 0.4, 0.35, 0.3, 0.4, 0.285, 0.03, 0.155, 0.283]),
            # Port diameter (m)

            # Economic data
            'par_a': 635.14,  # Cost model parameter
            'par_b': 0.778,   # Cost model parameter
            'pc': 0.15,       # Energy price ($)
            'int_rate': 0.1,  # Interest rate
            'n': 10,          # Project horizon (years)
            'eta': 0.6,       # Pump efficiency
            'Nop': 7500       # Number of hours of operation per year (h/y)
        }
    }

}

# endregion