##################################################################################################################
# region Titles and Header
# Nature: 'Parameters_Calculations_List' and 'Example_Within_Set_Up' functions
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          28-Fev-2025     Alice Peccini             Original
#   0.2          29-Apr-2025     Mariana Mello             Update to fix error
#   0.3          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
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
#from 

# endregion
##################################################################################################################



##################################################################################################################
# region Parameters Calculation functions
  
def Set_Up_Thermal_Loop(xD1, xD2, m_p_dict):

    # Here, all parameters that change with xD1 and xD2 must be updated for each equipment Model_Parameters dictionary

    m_p1 = m_p_dict['m_p1']     # Equipment1['Model_Parameters']
    m_p2 = m_p_dict['m_p2']     # Equipment2['Model_Parameters']

# CONTINUE WITH UPDATES.....

    feasibility = True  # you can return a feasibility of True or False if depending on xD1 and xD2 it changes
    # if no feasibility check is done here, return it as True

    return m_p_dict, feasibility


def fun_m_t(m_p):

    m_p['m_t'] = m_p['Q']/(m_p['Cp_t']*(m_p['Tout_t'] - m_p['Tin_t']))

    return m_p
# endregion
##################################################################################################################

