##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         22-Aug-2025     Sung Young Kim             Copy from GPHE folder
#   0.1         20-Oct-2025     Sung Young Kim             Add APH example
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# region INSTRUCTIONS
# Add Examples of Airpreheater in this file

# region Import Library
import numpy as np
#import copy
# endregion

####################################################################################################################
####################################################################################################################

# region INPUT EXAMPLE 1 - APH

Example1 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'APH',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                ["(0.0889,0.0056)", "(0.1016,0.0058)", "(0.1143,0.0061)", "(0.1413,0.0066)", "(0.1683,0.0071)"], #tuples for Do and td

                [1, 2, 3, 4, 5],  # L : tube length

                [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],     # Nr : number of tube rows
                
                [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],     # Nc : number of tube columns

                [1, 2, 3, 4, 5],        # Ncross : number of cross flow

                [1.5, 1.55, 1.60],      # rph : Transverse tube pitch ratio (horizontal)

                [1.4, 1.45, 1.50]       # rpv : Longitudinal pitch ratio (vertical)              

            ],

            'Selected_OF': ['AREA_OF'],  # TAC_OF or AREA_OF or CAPEX_OF
            
        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        # in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Tube side - Flue gas - Hot stream
            'm_gas': 47.04,            # Flow rate (kg*s**-1)
            'rho_gas': 0.4773485,      # Density (kg*m**-3)
            'Cp_gas': 1300,            # Heat capacity (J*(kg*K)**-1)
            'mu_gas': 0.0000248,       # Viscosity (Pa*s)
            'k_gas': 0.0363211,        # Thermal conductivity (W*(m*K)**-1)
            'Rf_gas': 0.0005,          # Fouling factor (m**2*oC*W**-1)
            'DPgasdisp': 500,         # Available pressure drop (Pa)

            # Air side - Cold stream
            'm_air': 15.732,           # Flow rate (kg*s**-1)
            'rho_air': 1.013,           # Density (kg*m**-3)
            'Cp_air': 1005,            # Heat capacity (J*(kg*K)**-1)
            'mu_air': 0.00001789,      # Viscosity (Pa*s)
            'k_air': 0.024,            # Thermal conductivity (W*(m*K)**-1)
            'Rf_air': 0.0002,          # Fouling Factor (m**2*oC*W**-1)
            'DPairdisp': 150,          # Available pressure drop (Pa)

            # Data of Air Preheater
            'ktube': 50,             # Thermal conductivity of plate (W*(m*K)**-1)
            'tf': 0.00275844,        # fin thinkness [m]
            'lf': 0.02538984,        # fin height [ft]
            'Nf': 48,                # number of fins per unit length

            # Problem data
            'Aexc': 11,             # Area excess (%)
            'Tair_in': 305,         # Inlet temperature of the cold stream (K)
            'Tair_out': 348,        # Outlet temperature of the cold stream (K)
            'Tgas_in': 657.35,      # Inlet temperature of the hot stream (K)
            'Tgas_out': 644.039,    # Outlet temperature of the hot stream (K)
            'v_gas_max': 20,       # Upper bound on the hot stream velocity (m*s**(-1))
            'v_gas_min': 4,         # Lower bound on the hot stream velocity (m*s**(-1))
            'v_air_max': 15,        # Upper bound on the cold stream velocity (m*s**(-1))
            'v_air_min': 3,         # Lower bound on the cold stream velocity (m*s**(-1))
            'F_min': 0.75,          # Minimum LMTD Correction Factor
            'Re_tube_min': 1e4,     # Lower bound on the tube-side Reynolds number
            'Re_air_min': 2e3,      # Lower bound on the air-side Reynolds number
            'Re_tube_max': 5e6,     # Upper bound on the tube-side Reynolds number
            'Re_air_max': 1e5,      # Upper bound on the air-side Reynolds number

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

# region INPUT EXAMPLE 2 - APH

Example2 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'APH',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                ["(0.0889,0.0056)", "(0.1016,0.0058)", "(0.1143,0.0061)", "(0.1413,0.0066)", "(0.1683,0.0071)"], #tuples for Do and td

                [2, 3, 4, 5, 6, 7],  # L : tube length

                [2, 3, 4, 5, 6, 7],     # Nr : number of tube rows
                
                [2, 3, 4, 5, 6, 7],     # Nc : number of tube columns

                [1, 2, 3],              # Ncross : number of cross flow

                [1.5, 1.55, 1.60],      # rph : Transverse tube pitch ratio (horizontal)

                [1.4, 1.45, 1.50]       # rpv : Longitudinal pitch ratio (vertical)              

            ],

            'Selected_OF': ['TAC_OF'],  # TAC_OF or AREA_OF or CAPEX_OF
            
        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        # in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Tube side - Flue gas - Hot stream
            'm_gas': 23.611,           # Flow rate (kg*s**-1)
            'rho_gas': 0.833,          # Density (kg*m**-3)
            'Cp_gas': 1120,            # Heat capacity (J*(kg*K)**-1)
            'mu_gas': 0.00003,         # Viscosity (Pa*s)
            'k_gas': 0.037,            # Thermal conductivity (W*(m*K)**-1)
            'Rf_gas': 0.0005,          # Fouling factor (m**2*oC*W**-1)
            'DPgasdisp': 9500,         # Available pressure drop (Pa)

            # Air side - Cold. stream
            'm_air': 28.889,           # Flow rate (kg*s**-1)
            'rho_air': 1.10,           # Density (kg*m**-3)
            'Cp_air': 1005,            # Heat capacity (J*(kg*K)**-1)
            'mu_air': 0.000019,        # Viscosity (Pa*s)
            'k_air': 0.026,            # Thermal conductivity (W*(m*K)**-1)
            'Rf_air': 0.0003,          # Fouling Factor (m**2*oC*W**-1)
            'DPairdisp': 9400,         # Available pressure drop (Pa)

            # Data of Air Preheater
            'ktube': 16.0,           # Thermal conductivity of plate (W*(m*K)**-1)
            'tf': 0.00275844,        # fin thinkness [m]
            'lf': 0.02538984,        # fin height [ft]
            'Nf': 48,                # number of fins per unit length

            # Problem data
            'Aexc': 5,             # Area excess (%)
            'Tair_in': 308,         # Inlet temperature of the cold stream (K)
            'Tair_out': 393,        # Outlet temperature of the cold stream (K)
            'Tgas_in': 473,         # Inlet temperature of the hot stream (K)
            'Tgas_out': 407,        # Outlet temperature of the hot stream (K)
            'v_gas_max': 100,        # Upper bound on the hot stream velocity (m*s**(-1))
            'v_gas_min': 4,         # Lower bound on the hot stream velocity (m*s**(-1))
            'v_air_max': 20,        # Upper bound on the cold stream velocity (m*s**(-1))
            'v_air_min': 3,         # Lower bound on the cold stream velocity (m*s**(-1))
            'F_min': 0.75,          # Minimum LMTD Correction Factor
            'Re_tube_min': 1e4,     # Lower bound on the tube-side Reynolds number
            'Re_air_min': 2e3,      # Lower bound on the air-side Reynolds number
            'Re_tube_max': 5e6,     # Upper bound on the tube-side Reynolds number
            'Re_air_max': 1e5,      # Upper bound on the air-side Reynolds number

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

