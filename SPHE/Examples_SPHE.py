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
#   0.5         30-Jun-2025     Mariana Mello              Add examples with larger search space
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of STHE in this file
'''
This is a STHE Model Examples File, Set Trimming is applied.

The main structure of the dictionary is:

ExampleX = {

    'Number_of_Equipment': N,

    'Equipment1': {}

    'Equipment2': {}

         ...

    'EquipmentN': {}

}

For each 'STHE' Type_Equipment the following data are required:

'EquipmentN': {

    'Model_Declarations': {

        'Type_Equipment': 'STHE',

        'Discrete_Values_of_Variables': [
                [],  # Ds

                [],  # dte

                [],  # Npt

                [],  # rp

                [],  # lay    (1  = 90° ;  2 = 30° ; 3 = 45°)

                [],  # L

                [],  # Nb

                []  # Bc
    },

    'Model_Parameters': {

           # Hot stream
            'mh': ,         # Flow rate (kg*s**-1)
            'roh': ,        # Density (kg*m**-3)
            'Cph': ,        # Heat capacity (J*(kg*K)**-1)
            'mih': ,        # Viscosity (Pa*s)
            'kh': ,         # Thermal conductivity (W*(m*K)**-1)
            'Rfh': ,        # Fouling factor (m**2*oC*W**-1)
            'DPhdisp': ,    # Available pressure drop (Pa)

            # Cold stream
            'mc': ,        # Flow rate (kg*s**-1)
            'roc': ,       # Density (kg*m**-3)
            'Cpc': ,       # Heat capacity (J*(kg*K)**-1)
            'mic': ,       # Viscosity (Pa*s)
            'kc': ,        # Thermal conductivity (W*(m*K)**-1)
            'Rfc': ,       # Fouling factor (m**2*oC*W**-1)
            'DPcdisp': ,   # Available pressure drop (Pa)

            # Heat exchanger
            'ktube': ,            # Tube wall thermal conductivity (W*(m*K)**-1)
            'thk': ,              # Tube thickness
            'yfluid': ,           # Allocation of tube side: 'hot_stream' or 'cold_stream'. Entry is optional.
                                  # If entry is given as '' or if entry is completly skipped, both options will be evaluated

            # Correlations Tube and Shell Methods
            'Shell_Method': '',      # Kern or Bell
            'Tube_Method': '',       # Dittus_Boelter or Dewiit_Saunders or Gnielinski or Hausen or Sieder_Tate

            # Problem
            'Objective_Function': '',    # Objective Functions: 'TAC' or 'Area' or 'CAPEX'
            'Aexc': ,                    # Area excess (%)
            'Tci': ,                     # Inlet temperature of the cold stream (oC)
            'Tco': ,                     # Outlet temperature of the cold stream (oC)
            'Thi': ,                     # Inlet temperature of the hot stream (oC)
            'Tho': ,                     # Outlet temperature of the hot stream (oC)
            'vsmax': ,                   # Upper bound on the shell-side velocity (m*s**(-1))
            'vsmin': ,                   # Lower bound on the shell-side velocity (m*s**(-1))
            'vtmax': ,                   # Upper bound on the tube-side velocity (m*s**(-1))
            'vtmin': ,                   # Lower bound on the tube-side velocity (m*s**(-1))
            'Retmin': ,                  # Lower bound on the tube-side Reynolds number
            'Resmin': ,                  # Lower bound on the shell-side Reynolds number
            'Retmax': ,                  # Upper bound on the tube-side Reynolds number
            'Resmax': ,                  # Upper bound on the shell-side Reynolds number
            'LBLD': ,                    # Lower bound on L/D
            'UBLD': ,                    # Upper bound on L/D

            # Required parameters for Bell Method
            'Nss': ,                   # Number of sealing strips
            'plbmax1': ,               # maximum unsupported span of tubes -> 52 for steel and steel alloys and 46 for aluminum and copper alloys
            'plbmax2': ,               # maximum unsupported span of tubes -> 0.532 for steel and steel alloys and 0.436 for aluminum and copper alloys


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

##################################################################################################################

# region Import Library
import numpy as np
import copy
# endregion

####################################################################################################################
####################################################################################################################

# region INPUT EXAMPLE 1 - SPHE

Example1 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'SPHE',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [0.7874, 0.8382, 0.889, 0.9398, 0.9906, 1.0668, 1.143, 1.2192, 1.3716, 1.524],  # Ds

                [0.01905, 0.02540, 0.03175, 0.03810, 0.05080],  # dte

                [1, 2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay  (1 = 90° ;  2 = 30° ; 3 = 45°)

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0976],  # L

                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],  # Nb

                [0.25] # Bc

            ],

            'Selected_OF': ['TAC_OF'],

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream
            'mh': 20,           # Flow rate (kg*s**-1)
            'roh': 750,         # Density (kg*m**-3)
            'Cph': 2840,        # Heat capacity (J*(kg*K)**-1)
            'mih': 0.002,       # Viscosity (Pa*s)
            'kh': 0.19,         # Thermal conductivity (W*(m*K)**-1)
            'Rfh': 0.0002,      # Fouling factor (m**2*oC*W**-1)
            'DPhdisp': 100e3,   # Available pressure drop (Pa)

            # Cold stream
            'mc': 60,           # Flow rate (kg*s**-1)
            'roc': 995,         # Density (kg*m**-3)
            'Cpc': 4187,        # Heat capacity (J*(kg*K)**-1)
            'mic': 0.0005,      # Viscosity (Pa*s)
            'kc': 0.6,          # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.0007,      # Fouling factor (m**2*oC*W**-1)
            'DPcdisp': 100e3,   # Available pressure drop (Pa)

            # Heat exchanger
            'ktube': 50,                  # Tube wall thermal conductivity (W*(m*K)**-1)
            'thk': 1.65e-3,               # Tube thickness
            'yfluid': 'hot_stream',       # Allocation of tube side: 'hot_stream' or 'cold_stream'

            # Correlations Tube and Shell Methods
            'Tube_Method': 'Dittus_Boelter',  # Dittus_Boelter or Dewiit_Saunders or Gnielinski or Hausen or Sieder_Tate
            'Shell_Method': 'Kern',           # Kern or Bell

            # Problem
            'Aexc': 11,                   # Area excess (%)
            'Tci': 47,                    # Inlet temperature of the cold stream (oC)
            'Tco': 56,                    # Outlet temperature of the cold stream (oC)
            'Thi': 120,                   # Inlet temperature of the hot stream (oC)
            'Tho': 80,                    # Outlet temperature of the hot stream (oC)
            'vsmax': 2,                   # Upper bound on the shell-side velocity (m*s**(-1))
            'vsmin': 0.5,                 # Lower bound on the shell-side velocity (m*s**(-1))
            'vtmax': 3,                   # Upper bound on the tube-side velocity (m*s**(-1))
            'vtmin': 1,                   # Lower bound on the tube-side velocity (m*s**(-1))
            'Retmin': 1e4,                # Lower bound on the tube-side Reynolds number
            'Resmin': 2e3,                # Lower bound on the shell-side Reynolds number
            'Retmax': 5e6,                # Upper bound on the tube-side Reynolds number
            'Resmax': 1e5,                # Upper bound on the shell-side Reynolds number
            'LBLD': 3,                    # Lower bound on L/D
            'UBLD': 15,                   # Upper bound on L/D
            'Xp': 0.9,                    # Parameter Xp (Smith, 2005)
            'F_min': 0.75,                # Minimum LMTD Correction Factor


            # Data Economic
            'par_a': 635.14,    # Cost model parameter
            'par_b': 0.778,     # Cost model parameter
            'pc': 0.15,         # Energy price ($)
            'int_rate': 0.1,    # Interest rate
            'n': 10,            # Project horizon (years)
            'eta': 0.6,         # Pump efficiency
            'Nop': 7500         # Number of hours of operation per year (h/y)

        }
    },
}

# endregion

####################################################################################################################
