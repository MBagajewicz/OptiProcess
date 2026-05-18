##################################################################################################################
# region Titles and Header
# Nature: 'Parameters_Calculations_List' and 'Example_Within_Set_Up' functions
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR              DESCRIPTION OF CHANGES MADE
#   0.0       28-Fev-2025     Alice Peccini             Original
#   0.1       17-Jun-2025     Miguel Bagajewicz         Rearrange from Ditillation File
##################################################################################################################
# INPUT: Define Functions for 'Parameters_Calculations_List' and 'Example_Within_Set_Up'
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def)
# For 'Parameters_Calculations_List':
#   def fun(model_parameters)
#       return model_parameters
# For 'Example_Within_Set_Up':
#   def fun(results,model_parameters)
#       return model_parameters
# endregion
##################################################################################################################

##################################################################################################################
# region Import Library
from Commom_Equations_DC import Calculations_DC_Param_Set_Up
import os
# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions


# Initialize Aspen
def par_start_Aspen(m_p):

    ####### CHANGE NEEDED #######
    # This is the function called to initialize Aspen for DC model (it sets parameters for a distillation column for connection with Aspen)
    # A similar one made for an absorber column must be included in Calculations_DC_Param_Set_Up file, and then called here
    m_p = Calculations_DC_Param_Set_Up.call_initial_Aspen(m_p)

    return m_p


# endregion
##################################################################################################################

