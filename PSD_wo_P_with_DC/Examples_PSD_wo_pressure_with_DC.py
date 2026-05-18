##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         17-Feb-2025     Diego Oliva                STHE Examples Repository
#   0.2         28-Feb-2025     Alice Peccini              Relocating folders
#   0.3         29-Apr-2025     Mariana Mello              Update Model Parameters of STHE
#   0.4         12-May-2025     Mariana Mello              Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of PSD without pressure and using DC in this file

# Example1 = {

#     'Number_of_Equipment': 2,

#     'Equipment1': {                   ==> Data for column 1
#         'Model_Declarations': {},
#         'Model_Parameters': {}
#     },

#     'Equipment2': {                   ==> Data for column 2
#         'Model_Declarations': {},
#         'Model_Parameters': {}
#     },

#     'Global_Optimizer': {             ==> Bounds for continuous variables 
#         # Bounds must be given in the same order as model optimization variables ['xD1', 'xD2']
#         'Lower_Bounds': [0.5, 0.7],
#         'Upper_Bounds': [0.5, 0.7]

#     },
# }

##################################################################################################################

# region Import Library
import numpy as np
# endregion

####################################################################################################################
####################################################################################################################

# region INPUT EXAMPLE 1 - STHE + STHE

Example1 = {

    'Number_of_Equipment': 2,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'DC',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [
    
                            list(range(3, 41)), # Nf (Feed considered from stage 3 to 40, considering there are always a stripping 
                                                # and a rectifying section)
                                                # Nf is interpreted regarding stages and not trays (same as in Aspen Plus)
                            list(range(5, 43))  # Ns (Stages and not trays, as in Aspen Plus)
                                                # Ns = 5 means: condenser + 3 stages within the column + reboiler
                                                # Ns = 42 means: condenser + 40 stages within the column + reboiler                
                                    ],

            'Selected_OF': ['TAC_OF'],

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

                   # --------------------------- 
            # Problem Data
            # ---------------------------
            # General Data
            'Nc' : 3,                   # Number of components
            'Nsmin' : 13,               # Minimum number of stages (Condenser + 11 stages within the column + Reboiler)
            'Nfmin' : 3,                # Minimum feed tray
            'Pcol' : 1e5,               # Column Pressure (Pa) - constant throughout the column --> Pendência: consider some pressure drop
            # Feed Data 
            'z_f' : [0.14, 0.39, 0.47], # Feed molar composition [Benzene, Toluene, m-Xylene]
            'F_f' :  100,               # Feed flow (kmol/h)
            'T_f' :  113.4 + 273.15,    # Feed temperature (K)
            # Separation Task Specification 
            'xB_TOP' : 0.99,                    # Top benzene purity
            'xB_BOTTOM' : 0.005,                # Bottom benzene purity       
            # Components - NAMES MUST BE THE SAME AS SET IN ASPEN PLUS (if Aspen is to be used)!! CASE SENSITIVE 
            'Comp_name' : ['BENZENE', 'TOLUENE', 'M-XYLENE'],      

            # --------------------------- 
            # Thermal Utilities Data
            # ---------------------------
            # Global heat exchange coefficient (W/m²K) - Cheng - 2009 and Douglas book
            'Ur' : 1050,                # Reboiler
            'Uc' : 850,                 # Condenser
            # Utilities temperatures (K)
            'Tlpst' : 160 + 273.15,     # Low pressure steam 
            'Tcwin' : 303.15,           # Cooling water inlet 
            'Tcwout' : 323.15,          # Cooling water outlet 

            # --------------------------- 
            # Costing Data
            # ---------------------------
            'Ccw' : 0.378e-6,                           # Utilities costs ($/kJ) from Turton -> page 245 5ed 
            'Clpst' : 2.78e-6,                          # Utilities costs ($/kJ) from Turton -> page 245 5ed 
            'hours' : 8150,                             # Number of operation hours in a year (considering 7% of idle capacity)
            'Pb' : 3,                                   # Payback period (years)
            'lt' : 0.6096,                              # Tray spacing
            'roshell' : 7900,                           # roshell (kg/m³)

            # --------------------------- 
            # Reflux Drum Data
            # ---------------------------
            'L_D': 4,                                   # L/D ratio
            'TRL_min': 5,                              # Reflux Drum residence time (min)

            # --------------------------- 
            # Aspen Related Data
            # ---------------------------
            # File, block and streams - ATTENTION: THIS NAMES ARE CASE SENSITIVE, MUST BE THE SAME AS IN ASPEN FILE
            'file_name' : ['BTX Column.bkp'],
            'block_name' : ['COLUMN1'],
            'stream_names': ['FEED', 'D-TOP', 'B-BOTTOM'],
            # Bounds for manipulated variables within Aspen Active Specs
            'reflux_ratio_bounds': [0,100],             # Reflux ratio 
            'distillate_rate_bounds': [0,100]           # Distillate rate 

        }
    },

########################################################################

    'Equipment2': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'DC',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
           'Discrete_Values_of_Variables': [
    
                            list(range(3, 41)), # Nf (Feed considered from stage 3 to 40, considering there are always a stripping 
                                                # and a rectifying section)
                                                # Nf is interpreted regarding stages and not trays (same as in Aspen Plus)
                            list(range(5, 43))  # Ns (Stages and not trays, as in Aspen Plus)
                                                # Ns = 5 means: condenser + 3 stages within the column + reboiler
                                                # Ns = 42 means: condenser + 40 stages within the column + reboiler                
                                    ],

            'Selected_OF': ['TAC_OF'],

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

               # --------------------------- 
            # Problem Data
            # ---------------------------
            # General Data
            'Nc' : 3,                   # Number of components
            'Nsmin' : 13,               # Minimum number of stages (Condenser + 11 stages within the column + Reboiler)
            'Nfmin' : 3,                # Minimum feed tray
            'Pcol' : 1e5,               # Column Pressure (Pa) - constant throughout the column --> Pendência: consider some pressure drop
            # Feed Data 
            'z_f' : [0.14, 0.39, 0.47], # Feed molar composition [Benzene, Toluene, m-Xylene]
            'F_f' :  100,               # Feed flow (kmol/h)
            'T_f' :  113.4 + 273.15,    # Feed temperature (K)
            # Separation Task Specification 
            'xB_TOP' : 0.99,                    # Top benzene purity
            'xB_BOTTOM' : 0.005,                # Bottom benzene purity       
            # Components - NAMES MUST BE THE SAME AS SET IN ASPEN PLUS (if Aspen is to be used)!! CASE SENSITIVE 
            'Comp_name' : ['BENZENE', 'TOLUENE', 'M-XYLENE'],      

            # --------------------------- 
            # Thermal Utilities Data
            # ---------------------------
            # Global heat exchange coefficient (W/m²K) - Cheng - 2009 and Douglas book
            'Ur' : 1050,                # Reboiler
            'Uc' : 850,                 # Condenser
            # Utilities temperatures (K)
            'Tlpst' : 160 + 273.15,     # Low pressure steam 
            'Tcwin' : 303.15,           # Cooling water inlet 
            'Tcwout' : 323.15,          # Cooling water outlet 

            # --------------------------- 
            # Costing Data
            # ---------------------------
            'Ccw' : 0.378e-6,                           # Utilities costs ($/kJ) from Turton -> page 245 5ed 
            'Clpst' : 2.78e-6,                          # Utilities costs ($/kJ) from Turton -> page 245 5ed 
            'hours' : 8150,                             # Number of operation hours in a year (considering 7% of idle capacity)
            'Pb' : 3,                                   # Payback period (years)
            'lt' : 0.6096,                              # Tray spacing
            'roshell' : 7900,                           # roshell (kg/m³)

            # --------------------------- 
            # Reflux Drum Data
            # ---------------------------
            'L_D': 4,                                   # L/D ratio
            'TRL_min': 5,                              # Reflux Drum residence time (min)

            # --------------------------- 
            # Aspen Related Data
            # ---------------------------
            # File, block and streams - ATTENTION: THIS NAMES ARE CASE SENSITIVE, MUST BE THE SAME AS IN ASPEN FILE
            'file_name' : ['BTX Column.bkp'],
            'block_name' : ['COLUMN1'],
            'stream_names': ['FEED', 'D-TOP', 'B-BOTTOM'],
            # Bounds for manipulated variables within Aspen Active Specs
            'reflux_ratio_bounds': [0,100],             # Reflux ratio 
            'distillate_rate_bounds': [0,100]           # Distillate rate 
        }
    },

#######################################################################

    'Global_Optimizer': {

        # Bounds must be given in the same order as model optimization variables ['xD1', 'xD2']
        
        'Lower_Bounds': [0.5, 0.7],
       
        'Upper_Bounds': [0.5, 0.7]

    },

}


# endregion

######################################################################################################################
######################################################################################################################

###################################################################################################################
###################################################################################################################
