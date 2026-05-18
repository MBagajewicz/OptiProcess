##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025       Diego Oliva                Aircooler Examples Repository
#   0.2       12-May-2025       Mariana Mello              Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of Aircoolers in this file
##################################################################################################################

# region Import Library
import numpy as np
# endregion

###################################################################################################################
###################################################################################################################
# region INPUT EXAMPLE 1 - AIRCOOLER

Example1 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'Aircooler',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [0, 1, 2, 3, 4],                        # finnedsurface
                #[0],

                [4.572, 6.096, 7.315, 9.114, 10.973],   # L
                #[10.973],

                [2, 2.5],                               # rp
                #[2.5],

                [1, 2],                                 # Nbay
                #[2],

                [1, 2, 3],                              # Nbbay
                #[1],

                [35, 38, 41, 44, 47, 50, 53, 56],       # Ntr
                #[56],

                [0, 1, 2, 3, 4, 5, 6, 7, 8],            # aircoolerconfig
                #[0],

                [1, 2],                                 # Nfanbay
                #[2],

                [1.2, 2.2, 3.2, 4.2, 5.2]               # Dfan
                #[3.2]

            ],

            'Selected_OF': ['TAC_OF'],

        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream
            'mh': 31.5,             # Flow rate (kg*s**-1)
            'roh': 799.9359282,     # Density (kg*m**-3)
            'Cph': 2303.18258,      # Heat capacity (J*(kg*K)**-1)
            'mih': 0.000500207,     # Viscosity (Pa*s)
            'kh': 0.141917619,      # Thermal conductivity (W*(m*K)**-1)
            'Rfh': 0.00017611,      # Fouling factor (m**2*oC*W**-1)
            'DPhdisp': 105000,      # Available pressure drop (Pa)

            # Cold stream
            'Rfc': 0.0,             # Fouling Factor (m**2*oC*W**-1)

            # Data of material
            'kt': 44.998,           # Thermal conductivity of material (W*(m*K)**-1)
            'kf': 237.97,           # Fins thermal conductivity
            'thk': 0.002413,        # Tube thickness (m)

            # Selection
            'draft': 1,             # 1 = induced draft - 2 = forced draft

            # Fan system
            'etafan': 0.7,          # Efficiency of fan
            'etasr': 0.95,          # Speed reducer
            'etamotor': 1,          # Efficiency of motor

            'alphat': 0.003175,     # Minimum spacing between the fins of adjacent tubes (m)
            'fd': 0.1524,           # Minimum distance between the fan and the bay width (m)
            'fl': 0.1524,           # Minimum distance between the fan and the bay length (m)

            # Problem data
            'Aexc': 1.1,        # Area excess (%)
            'Tci': 35.05,       # Inlet temperature of the cold stream (oC)
            'Tco': 65.65,       # Outlet temperature of the cold stream (oC)
            'Thi': 121.15,      # Inlet temperature of the hot stream (oC)
            'Tho': 65.65,       # Outlet temperature of the hot stream (oC)
            'vhmax': 3,         # Upper bound on the hot stream velocity (m*s**(-1))
            'vhmin': 1,         # Lower bound on the hot stream velocity (m*s**(-1))
            'Rehmin': 10000,    # Upper bound on the Reynolds number of hot stream
            'Recmin': 1800,     # Lower bound on the Reynolds number of cold stream
            'Recmax': 1e5,      # Upper bound on the Reynolds number of cold stream
            'LDti_lb': 10,      # Lower bound on the L/Dti
            'Ltpmin': 0.0274,   # Pitch ratio bounds
            'Ltpmax': 0.0986,   # Pitch ratio bounds
            'AotAr_lb': 1,      # Aot/Ar ratio bounds
            'AotAr_ub': 50,     # Aot/Ar ratio bounds
            'Lftf_lb': 3,       # Lower bound on the Lf/tf ratio
            'DfDte_ub': 3,      # Upper bound on the Df/Dte ratio


            'ppNpt': np.array([1, 1, 1, 1, 3, 4, 5, 6, 2]),
            #'ppNpt': np.array([3]),
            #
            'ppNr': np.array([3, 4, 5, 6, 3, 4, 5, 6, 4]),
            #'ppNr': np.array([3]),
            #
            'ppDte': np.array([0.0254, 0.0254, 0.0254, 0.0254, 0.0254]),
            #'ppDte': np.array([0.0254]),
            #
            'ppLf': np.array([0.00635, 0.00635, 0.009525, 0.009525, 0.015875]),
            #'ppLf': np.array([0.015875]),
            #
            'ppNf': np.array([275, 393, 275, 393, 393]),
            #'ppNf': np.array([393]),
            #
            'pptf': np.array([0.000381, 0.000381, 0.000381, 0.000381, 0.000330]),
            #'pptf': np.array([0.000330]),
            #
            'ppF': np.array([]), # This parameter will be calculate by Parameters_Calculations_List

            # Economic data
            'int_rate': 0.15,  # Interest rate
            'y': 10,           # Project horizon (years)
            'hop': 7920,       # Number of operating hours per year (h/year)
            'Cen': 0.0680      # Average industrial electricity price ($/kWh)
        }
    },
    
}

# endregion
###################################################################################################################
###################################################################################################################
