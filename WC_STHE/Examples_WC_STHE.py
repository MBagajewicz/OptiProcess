##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#  0.0         05-Mar-2025       Mariana Mello             Water Cooler Examples Repository
#  0.2         23-Apr-2025       Mariana Mello             Update Water Cooler STHE Model Parameters
#  0.3         06-May-2025       Mariana Mello             Revision from paper
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of Water Cooler in this file
##################################################################################################################

# region INPUT EXAMPLE 1 - Water Cooler

Example1 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'WC_STHE',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [0.2032, 0.254, 0.3048, 0.33655, 0.38735, 0.43815, 0.48895, 0.53975, 0.59055, 0.635, 0.6858, 0.7366,
                 0.7874, 0.8382, 0.8890, 0.9398, 0.9906, 1.0668, 1.143, 1.2192, 1.3716, 1.524, 1.6764, 1.8288, 1.9812,
                 2.1336, 2.286, 2.4384, 2.7432, 3.048],  # Ds

                [0.01905, 0.02540, 0.03175, 0.03810, 0.05080],  # dte

                [1, 2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2, 3],  # lay  -->  1  = 90° and 2 = 30° and 3 = 45°

                [1.2195, 1.524, 1.8288, 2.1336, 2.4384, 2.7432, 3.048, 3.3528, 3.6576, 3.9624, 4.2672, 4.572, 4.8768,
                 5.1816, 5.4864, 5.7912, 6.0976],  # L

                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],  # Nb

                [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45]  # Bc

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
            'DPhdisp': 100e3, # Available pressure drop (Pa)

            # Cold stream
            'roc': 1000,      # Density (kg*m**-3)
            'Cpc': 4184,      # Heat capacity (J*(kg*K)**-1)
            'mic': 0.0008,    # Viscosity (Pa*s)
            'kc': 0.6,        # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.00009,   # Fouling factor (m**2*oC*W**-1)
            'DPcdisp': 100e3, # Available pressure drop (Pa)

            # Heat exchanger
            'ktube': 109,              # Tube wall thermal conductivity (W*(m*K)**-1)
            'thk': 0.001225,           # Tube thickness
            'yfluid': 'cold_stream',   # Allocation of tube side: 'hot_stream' or 'cold_stream'

            # Correlations Tube and Shell Methods
            'Shell_Method': 'Bell',             # Kern or Bell
            'Tube_Method': 'Dittus_Boelter',    # Dittus_Boelter or Dewiit_Saunders or Gnielinski or Hausen or Sieder_Tate

            # Problem
            'Aexc': 10,         # Area excess (%)
            'Tci': 20,          # Inlet temperature of the cold stream (oC)
            'Thi': 190,         # Inlet temperature of the hot stream (oC)
            'Tho': 120,         # Outlet temperature of the hot stream (oC)
            'vsmax': 2,         # Upper bound on the shell-side velocity (m*s**(-1))
            'vsmin': 0.5,       # Lower bound on the shell-side velocity (m*s**(-1))
            'vtmax': 3,         # Upper bound on the tube-side velocity (m*s**(-1))
            'vtmin': 0.5,       # Lower bound on the tube-side velocity (m*s**(-1))
            'Retmin': 2500,     # Lower bound on the tube-side Reynolds number
            'Retmax': 124000,   # Upper bound on the tube-side Reynolds number
            'Resmin': 0,        # Lower bound on the shell-side Reynolds number
            'Resmax': 100000,   # Upper bound on the shell-side Reynolds number
            'LBLD': 3,          # Lower bound on L/D
            'UBLD': 15,         # Upper bound on L/D
            'F_min': 0.75,      # Minimum LMTD Correction Factor
            'DeltaT_min': 5,    # The minimum approach

            # Parameters of Water Cooler model
            'Fw_max': 150,      # Maximum cooling water (kg/s)
            'Tco_max': 50,      # Maximum cooler water outlet temperature (°C)
            'Xp': 0.9,          # Parameter Xp (Smith, 2005)

            # Required parameters for Bell Method
            'Nss': 0,           # Number of sealing strips
            'plbmax1': 52,      # maximum unsupported span of tubes -> 52 for steel and steel alloys and 46 for aluminum and copper alloys
            'plbmax2': 0.532,   # maximum unsupported span of tubes -> 0.532 for steel and steel alloys and 0.436 for aluminum and copper alloys

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

# region INPUT EXAMPLE 2 - Water Cooler

Example2 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'WC_STHE',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [0.2032, 0.254, 0.3048, 0.33655, 0.38735, 0.43815, 0.48895, 0.53975, 0.59055, 0.635, 0.6858, 0.7366,
                 0.7874, 0.8382, 0.8890, 0.9398, 0.9906, 1.0668, 1.143, 1.2192, 1.3716, 1.524, 1.6764, 1.8288, 1.9812,
                 2.1336, 2.286, 2.4384, 2.7432, 3.048],  # Ds

                [0.01905, 0.02540, 0.03175, 0.03810, 0.05080],  # dte

                [1, 2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2, 3],  # lay  -->  1  = 90° and 2 = 30° and 3 = 45°

                [1.2195, 1.524, 1.8288, 2.1336, 2.4384, 2.7432, 3.048, 3.3528, 3.6576, 3.9624, 4.2672, 4.572, 4.8768,
                 5.1816, 5.4864, 5.7912, 6.0976],  # L

                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],  # Nb

                [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45]  # Bc

            ],

            'Selected_OF': ['TAC_OF'],  # TAC_OF

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream
            'mh': 17.36,      # Flow rate (kg*s**-1)
            'roh': 784.714,   # Density (kg*m**-3)
            'Cph': 2279.48,   # Heat capacity (J*(kg*K)**-1)
            'mih': 0.00085,   # Viscosity (Pa*s)
            'kh': 0.07785,    # Thermal conductivity (W*(m*K)**-1)
            'Rfh': 0.00011,   # Fouling factor (m**2*oC*W**-1)
            'DPhdisp': 100e3, # Available pressure drop (Pa)

            # Cold stream
            'roc': 1000,      # Density (kg*m**-3)
            'Cpc': 4184,      # Heat capacity (J*(kg*K)**-1)
            'mic': 0.0008,    # Viscosity (Pa*s)
            'kc': 0.6,        # Thermal conductivity (W*(m*K)**-1)
            'Rfc': 0.00009,   # Fouling factor (m**2*oC*W**-1)
            'DPcdisp': 100e3, # Available pressure drop (Pa)

            # Heat exchanger
            'ktube': 109,              # Tube wall thermal conductivity (W*(m*K)**-1)
            'thk': 0.001225,           # Tube thickness
            'yfluid': 'cold_stream',   # Allocation of tube side: 'hot_stream' or 'cold_stream'

            # Correlations Tube and Shell Methods
            'Shell_Method': 'Bell',             # Kern or Bell
            'Tube_Method': 'Dittus_Boelter',    # Dittus_Boelter or Dewiit_Saunders or Gnielinski or Hausen or Sieder_Tate

            # Problem
            'Aexc': 10,         # Area excess (%)
            'Tci': 20,          # Inlet temperature of the cold stream (oC)
            'Thi': 146.15,      # Inlet temperature of the hot stream (oC)
            'Tho': 40,          # Outlet temperature of the hot stream (oC)
            'vsmax': 2,         # Upper bound on the shell-side velocity (m*s**(-1))
            'vsmin': 0.5,       # Lower bound on the shell-side velocity (m*s**(-1))
            'vtmax': 3,         # Upper bound on the tube-side velocity (m*s**(-1))
            'vtmin': 0.5,       # Lower bound on the tube-side velocity (m*s**(-1))
            'Retmin': 2500,     # Lower bound on the tube-side Reynolds number
            'Retmax': 124000,   # Upper bound on the tube-side Reynolds number
            'Resmin': 0,        # Lower bound on the shell-side Reynolds number
            'Resmax': 100000,   # Upper bound on the shell-side Reynolds number
            'LBLD': 3,          # Lower bound on L/D
            'UBLD': 15,         # Upper bound on L/D
            'F_min': 0.75,      # Minimum LMTD Correction Factor
            'DeltaT_min': 5,    # The minimum approach

            # Parameters of Water Cooler model
            'Fw_max': 150,      # Maximum cooling water (kg/s)
            'Tco_max': 50,      # Maximum cooler water outlet temperature (°C)
            'Xp': 0.9,          # Parameter Xp (Smith, 2005)

            # Required parameters for Bell Method
            'Nss': 0,           # Number of sealing strips
            'plbmax1': 52,      # maximum unsupported span of tubes -> 52 for steel and steel alloys and 46 for aluminum and copper alloys
            'plbmax2': 0.532,   # maximum unsupported span of tubes -> 0.532 for steel and steel alloys and 0.436 for aluminum and copper alloys

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

