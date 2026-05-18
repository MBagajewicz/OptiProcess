##################################################################################################################
# region Titles and Header
# Nature: 'Parameters_Calculations_List' and 'Example_Within_Set_Up' functions
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          28-Fev-2025     Alice Peccini             Original
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


# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions


# Initialize Aspen
def par_start_Aspen(m_p):

    m_p = Calculations_DC_Param_Set_Up.call_initial_Aspen(m_p)

    return m_p


# Sieve Tray (Problem Within) set up
def Set_Up_Sieve_Tray(results, m_p):
    
    m_p = Calculations_DC_Param_Set_Up.SU_Sieve_Tray(results, m_p)
    
    return m_p


# HSTC set up
def Set_Up_HSTC(results, m_p):
    
    m_p = Calculations_DC_Param_Set_Up.SU_HSTC(results, m_p)

    return m_p

# Kettle Set up
def Set_Up_Kettle(results, m_p):

    m_p = Calculations_DC_Param_Set_Up.SU_Kettle(results, m_p)

    return m_p

# Reflux Drum Set Up
def Set_Up_Reflux_Drum(results, m_p):
    m_p = Calculations_DC_Param_Set_Up.SU_Reflux_Drum(results, m_p)

    return m_p

# endregion
##################################################################################################################

