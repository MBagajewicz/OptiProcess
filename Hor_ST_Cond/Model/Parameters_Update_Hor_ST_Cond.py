##################################################################################################################
# region Titles and Header
# Nature: 'Parameters_Calculations_List' and 'Example_Within_Set_Up' functions
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
<<<<<<< Updated upstream
#   0.0          28-Fev-2025     Alice Peccini              Original
#   0.1          03-Jun-2025     Miguel Bagajewicz          Extension to Intensified Condenser+Desuperheater+Multic
##################################################################################################################
=======
#   0.0          28-Fev-2025     Alice Peccini             Original
#   0.1       03-Jun-2025       Miguel Bagajewicz          First Set up to add Inntensification/Desuperheating 
#                                                          and Multicomponent Condensation
# ##################################################################################################################
>>>>>>> Stashed changes
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
import numpy as np
# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions

def fun_Prt(m_p):
    m_p['Prt'] = m_p['Cp_t']*m_p['mi_t']/m_p['k_t']
    return m_p

# Mean temperature differenc
def fun_LMTD(m_p):

    Thin = m_p['Tin_s']; Thout = m_p['Tout_s']
    Tcin = m_p['Tin_t']; Tcout = m_p['Tout_t']
    
    teta1 = Thout - Tcin
    teta2 = Thin - Tcout

    if abs(teta1 - teta2) <= 1e-3:
        m_p['dTLM'] = (teta1 + teta2)/2
    else:
        m_p['dTLM'] = (teta1 - teta2)/np.log(teta1/teta2) 
    return m_p

def fun_Q(m_p):
    m_p['Q'] = m_p['m_s']*m_p['Hvap_s']
    return m_p

# endregion
##################################################################################################################

