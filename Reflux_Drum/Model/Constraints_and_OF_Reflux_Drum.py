###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          20-Fev-2025     Alice Peccini             Original
#   0.1          28-Feb-2025     Alice Peccini             Relocating folders
##################################################################################################################
# INPUT: Define Constraints as def and return + or - values depending the > or < inequality
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def)  for each constraint defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Active_Constraints_List']
# Then add an Objective Function to be minimized before declared in:
#                            Model_Declarations['Standard_Objective_Function']['Equation_Name']
# Finally, add the Lower Bound x
# endregion
############################################################################################

##################################################################################################################
# region Import Library
from Reflux_Drum.Calculations import (
    Calculations_Reflux_Drum_Areas,
    Calculations_Reflux_Drum_Cost,
    Calculations_Reflux_Drum_Heights,
    Calculations_Reflux_Drum_Residence_time
)

# endregion
##################################################################################################################

##################################################################################################################
# region Horizontal Shell and Tube Condenser

# ----------------------------------------------------------------------------------------------------------------
# Trimming Functions
# ----------------------------------------------------------------------------------------------------------------

def ST_LD_LB(D, L, m_p):
    fun_val = m_p['LD_LB'] - L/D 
    return fun_val

def ST_LD_UB(D, L, m_p):
    fun_val = L/D - m_p['LD_UB']
    return fun_val

def ST_hL(D, L, m_p):
    hL = Calculations_Reflux_Drum_Heights.fun_hL(D)
    fun_val = 0.35 - hL
    return fun_val

def ST_A_CS_L(D, L, m_p):
    A_CS_L = Calculations_Reflux_Drum_Areas.fun_A_CS_L(D)
    TR_L = Calculations_Reflux_Drum_Residence_time.fun_TR_L(L, A_CS_L, m_p['V_L'])
    fun_val = m_p['TRL_min']*60 - TR_L
    return fun_val

# ----------------------------------------------------------------------------------------------------------------
# Objective Function
# ----------------------------------------------------------------------------------------------------------------

def Cost_OF(D, L, m_p):
    # Objective function
    Wshell = Calculations_Reflux_Drum_Cost.f_Wshell(D, L, m_p['roshell'])
    RD_CAPEX = Calculations_Reflux_Drum_Cost.fun_CAPEX(Wshell)
    return RD_CAPEX

# endregion
##################################################################################################################

