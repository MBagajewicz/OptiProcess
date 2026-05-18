##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025       Alice Peccini              Horizontal Shell and Tube Condenser Examples Repository
#   0.2       12-May-2025       Mariana Mello              Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of Distillation in this file
##################################################################################################################

##################################################################################################################
# region Import Library
import copy
# endregion
##################################################################################################################

###################################### HORIZONTAL SHELL-AND-TUBE CONDENSER #######################################

##################################################################################################################
# region Examples Description

# endregion
##################################################################################################################

##################################################################################################################
# region INPUT EXAMPLE 1 - Reflux_Drum


Example1 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'Reflux_Drum',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [1.0668, 1.143, 1.2192, 1.3716, 1.524, 1.6764, 1.8288, 1.9812, 2.1336, 2.286, 2.4384, 2.7432, 3.048],  # D (m) 
                [1.2195, 1.524, 1.8288, 2.1336, 2.4384, 2.7432, 3.048, 3.3528, 3.6576, 3.9624, 4.2672, 4.572, 4.8768, 5.1816, 5.4864, 5.7912, 6.0976]  # L (m)

            ],

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            'm_L': 10000,       # Liquid mass flow rate (kg/h)
            'rho_L': 962,       # Liquid density (kg/m³)
            'TRL_min': 5,      # Minimum liquid residence time (min)
            'roshell' : 7900,   # roshell (kg/m3)
            'LD_LB' : 1,
            'LD_UB' : 3

        }
    }

}

# endregion
###################################################################################################################
###################################################################################################################


###################################################################################################################
# region INPUT EXAMPLE 2

Example2 = copy.deepcopy(Example1)
Example2['Equipment1']['Model_Parameters']['m_L'] = 5373.320503439785
Example2['Equipment1']['Model_Parameters']['rho_L'] = 814.5686586688059

# endregion
###################################################################################################################
###################################################################################################################

###################################################################################################################
# region INPUT EXAMPLE 3

Example3 = copy.deepcopy(Example1)
Example3['Equipment1']['Model_Parameters']['m_L'] = 9788.777500923567
Example3['Equipment1']['Model_Parameters']['rho_L'] = 814.5692081095991

# endregion
###################################################################################################################
###################################################################################################################


Example2_DC_validation = copy.deepcopy(Example1)
Example2_DC_validation['Equipment1']['Model_Parameters'] = {'TRL_min': 5, 'roshell': 7900, 'LD_LB': 3, 'LD_UB': 5, 'm_L': 9788.777500923567, 'rho_L': 814.5692081095991, 'V_L': 0.0033380894272666954}
