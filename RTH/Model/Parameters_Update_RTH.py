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
import numpy as np
# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions



# Heat transfer rate
def fun_Q(m_p):
    if m_p['Tout_s'] == m_p['Tin_s']:
        if m_p['task']==2:
            m_p['Q']= m_p['multiplier']*m_p['Q2']
        else:
            m_p['Q'] =m_p['multiplier']* m_p['m_s']*m_p['Hvap_s']
    
    else:
        m_p['Q'] = m_p['multiplier']*m_p['m_s']*m_p['Cp_s']*(m_p['Tout_s'] - m_p['Tin_s'])
    return m_p   

# Boiling heat transfer - pressure correction factor
def fun_Fp(m_p):
    if m_p['Pr'] >0.2:
        m_p['Fp'] = 1.8*m_p['Pr']**0.17
    else:
        m_p['Fp'] = 2.1*m_p['Pr']**0.27 + [9+ (1-m_p['Pr']**2)**(-1)]*m_p['Pr']**2
    return m_p

# Maximum flux for a single tube
def fun_q1_max(m_p):
    Pc_kPa = m_p['Pc']/1000
    m_p['q1_max'] = 367*Pc_kPa*m_p['Pr']**0.35*(1-m_p['Pr'])**0.9
    return m_p

# Mean temperature differenc
def fun_LMTD(m_p):

    Thin = m_p['Tin_t']; Thout = m_p['Tout_t']
    Tcin = m_p['Tin_s']; Tcout = m_p['Tout_s']
    
    teta1 = Thout - Tcin
    teta2 = Thin - Tcout

    if abs(teta1 - teta2) <= 1e-3:
        m_p['dTLM'] = (teta1 + teta2)/2
    else:
        m_p['dTLM'] = (teta1 - teta2)/np.log(teta1/teta2) 
    return m_p

# Tube side flow
def fun_m_t(m_p):
    if m_p['Tout_t'] == m_p['Tin_t']:
        m_p['m_t'] = m_p['Q']/m_p['Hvap_t']
    else:
        m_p['m_t'] = m_p['Q']/(m_p['Cp_t']*(m_p['Tin_t'] - m_p['Tout_t']))
    return m_p

# Reduced pressure - shell side
def fun_Pr(m_p):
    m_p['Pr'] = m_p['P_s']/m_p['Pc']
    return m_p

# endregion
##################################################################################################################

