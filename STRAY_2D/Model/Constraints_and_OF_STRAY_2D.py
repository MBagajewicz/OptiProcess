###################################################################################################################
#region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming 
# methodology 
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.1          20-Nov-2024     Miguel Bagajewicz         Proposed 
#   0.2          05-Fev-2025     Alice Peccini             Sieve Tray
#   0.3          28-Feb-2025     Alice Peccini             Relocating folders 
##################################################################################################################
# INPUT: Define Constraints as def and return + or - values depending the > or < inequality
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def) that need to be declared on Example_Repository in 
# ExampleX['EquipmentY']['Model_Declarations']
#endregion
############################################################################################

##################################################################################################################
#region Import Library

import numpy as np
from Commom_Equations_DC import (
    Calculations_DC_Costs,
    Calculations_DC_Column_Sizing
)
from STRAY_2D.Calculations import Calculations_STRAY_transition

#endregion
##################################################################################################################

# ---------------------------------------------------------------------------------------------------------------- 
# Trimming Functions - Geometric Constraints
# ----------------------------------------------------------------------------------------------------------------

import numpy as np

def f_viable_DRECT(DRECT, DSTRIP, m_p):
    # For each DRECT[i], check if it exists (approximately) in m_p['Viable_DRECT']
    fun_val = np.array([
        -1 if np.any(np.isclose(dc, m_p['Viable_DRECT'])) else 1
        for dc in DRECT
    ])
    return fun_val

def f_viable_DSTRIP(DRECT, DSTRIP, m_p):
    # For each DSTRIP[i], check if it exists (approximately) in m_p['Viable_DSTRIP']
    fun_val = np.array([
        -1 if np.any(np.isclose(dc, m_p['Viable_DSTRIP'])) else 1
        for dc in DSTRIP
    ])
    return fun_val

# ---------------------------------------------------------------------------------------------------------------- 
# Objective Function
# ----------------------------------------------------------------------------------------------------------------

def Cost_OF(DRECT, DSTRIP, m_p):

    # Find WRECT[i] such that DRECT[i] == m_p['Viable_DRECT'][j], and return m_p['Wshell_rect'][j]
    WRECT = np.array([
        m_p['Wshell_rect'][np.where(np.isclose(m_p['Viable_DRECT'], dc))[0][0]]
        for dc in DRECT
    ])
    # Find WSTRIP[i] such that DSTRIP[i] == m_p['Viable_DSTRIP'][j], and return m_p['Wshell_strip'][j]
    WSTRIP = np.array([
        m_p['Wshell_strip'][np.where(np.isclose(m_p['Viable_DSTRIP'], dc))[0][0]]
        for dc in DSTRIP
    ])

    # Compute transition mass
    WTRANS = Calculations_STRAY_transition.f_Wshell_trans(DSTRIP, DRECT,m_p['roshell'])

    # Combine WRECT and WSTRIP to compute shell CAPEX
    Wshell = WRECT + WSTRIP + WTRANS
    CAPEX_shell = Calculations_DC_Costs.Towler_and_Sinnot_Cost_Function(11600, 34, 0.85, Wshell)
    
    # Compute trays CAPEX for each section
    CAPEX_trays_rect = Calculations_DC_Costs.Towler_and_Sinnot_Cost_Function(130, 440, 1.8, DRECT)*m_p['Nt_rect']
    CAPEX_trays_strip = Calculations_DC_Costs.Towler_and_Sinnot_Cost_Function(130, 440, 1.8, DSTRIP)*m_p['Nt_strip']

    # Total CAPEX
    COL_CAPEX = CAPEX_shell + CAPEX_trays_rect + CAPEX_trays_strip

    # print('CAPEX_shell', CAPEX_shell)
    # print('CAPEX_trays_rect', CAPEX_trays_rect)
    # print('CAPEX_trays_strip', CAPEX_trays_strip)
    # print('DRECT',DRECT)
    # print('DSTRIP',DSTRIP)
    # print('Nt_RECT',m_p['Nt_rect'])
    # print('Nt_STRIP',m_p['Nt_strip'])
    
    return COL_CAPEX
