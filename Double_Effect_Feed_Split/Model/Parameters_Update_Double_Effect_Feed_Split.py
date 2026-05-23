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
from Commom_Equations_DC import Calculations_DC_Aspen

# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions


#Tomazim

# High Pressure Column condenser_duty (Problem Within) set up
def Set_Up_Double_Effect_Optimizer(Split, m_p_dict):

    m_p1 = m_p_dict['m_p1']
    NL_m_p1 = m_p_dict['NL_m_p1']
    m_p1['F_f'] = m_p1['Feed']*Split # Feed flow in the first column (kmol/h)
    NL_m_p1['F_f'] = m_p1['Feed'] * (1 - Split) # Feed flow in the second column (kmol/h) (Next Level Equipment)
    

    print(f'⚪  Split = {Split:.2f}')
    print(f'⚪  F_f 1st Column = {m_p1["F_f"]:.2f} kmol/h')
    print(f'⚪  F_f 2nd Column = {NL_m_p1["F_f"]:.2f} kmol/h')

    feasibility = True
   
    return m_p_dict, feasibility



# endregion
##################################################################################################################
