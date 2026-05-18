##################################################################################################################
# region Titles and Header
# Nature: 'Parameters_Calculations_List' and 'Example_Within_Set_Up' functions
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          28-Fev-2025     Alice Peccini             Original
#   0.2          25-Jun-2025     Mariana Mello             Proposed
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
from Common_Equations_HEX import (
    Calculations_HEX_heatload, 
    Calculations_HEX_LMTD
    )
# endregion
##################################################################################################################
##################################################################################################################
# region Parameters Calculation functions
  
def Set_Up_WC(m_water, m_p_dict):

    # ========================================= Parameters update =========================================
    # m_water

    m_p1 = m_p_dict['m_p1']

    # Calculate the heat load
    Q = Calculations_HEX_heatload.HEX_heat_load(m_p1['mh'], m_p1['Cph'], m_p1['Thi'], m_p1['Tho'])
    m_p1['mc'] = m_water
    m_p1['mt'] = m_water

    # Calculate Tco of Equipment
    T_w_out = Q/(m_water * m_p1['Cpc']) + m_p1['Tci']
    m_p1['Tco'] = T_w_out

    # ==================================== Check LMTD feasibility ====================================
    try:
        # LMTD of Equipment
        lmtd1 = Calculations_HEX_LMTD.HEX_lmtd(m_p1['Thi'], m_p1['Tho'], m_p1['Tci'], m_p1['Tco'])

        feasibility = True

    except (ValueError, ZeroDivisionError):

        feasibility = False

    return m_p_dict, feasibility

# endregion
##################################################################################################################

