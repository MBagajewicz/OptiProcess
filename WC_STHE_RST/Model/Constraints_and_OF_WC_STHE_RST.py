###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          2024            Diego Oliva               Original
#   0.2          02-Jun-2025     Mariana Mello             Constraints
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
from STHE.Model import Constraints_and_OF_STHE
from WC_STHE.Calculations import Calculations_WC_STHE_TAC
from STHE.Calculations import Calculations_STHE_CAPEX

# endregion
##################################################################################################################

##################################################################################################################
# region Constraints


def LD_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on L/Ds
    fun_val = Constraints_and_OF_STHE.LD_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def LD_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on L/Ds
    fun_val = Constraints_and_OF_STHE.LD_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def lbc_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on lbc
    fun_val = Constraints_and_OF_STHE.lbc_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def lbc_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on lbc
    fun_val = Constraints_and_OF_STHE.lbc_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def vs_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on vs
    fun_val = Constraints_and_OF_STHE.vs_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def vs_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on vs
    fun_val = Constraints_and_OF_STHE.vs_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def vt_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on vt
    fun_val = Constraints_and_OF_STHE.vt_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def vt_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on vt
    fun_val = Constraints_and_OF_STHE.vt_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def Ret_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on Ret
    fun_val = Constraints_and_OF_STHE.Ret_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def Ret_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on Ret
    fun_val = Constraints_and_OF_STHE.Ret_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def Res_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on Ret
    fun_val = Constraints_and_OF_STHE.Res_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def Res_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on Res
    fun_val = Constraints_and_OF_STHE.Res_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def DPs_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    fun_val = Constraints_and_OF_STHE.DPs_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def DPt_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    fun_val = Constraints_and_OF_STHE.DPt_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def F_min(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    fun_val = Constraints_and_OF_STHE.F_min(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def Areq(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Required area constraint
    fun_val = Constraints_and_OF_STHE.Areq(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return fun_val

def ST_TAC(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    TAC = Calculations_WC_STHE_TAC.WC_STHE_TAC(m_p['mt'], m_p['rot'], m_p['mit'], m_p['thk'], Ds, dte, Npt, rp,
                                               lay, L, m_p['pcw'], m_p['pc'], m_p['roc'], m_p['eta'], m_p['cf'],
                                               m_p['cv'], m_p['alpha'], m_p['Nop'], m_p['int_rate'], m_p['n'],
                                               m_p, m_p['ms'], m_p['ros'], m_p['mis'], Nb, Bc)
    fun_val = TAC - m_p['TAC_incumbent']
    return fun_val


def TAC_OF(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Objective function
    TAC = Calculations_WC_STHE_TAC.WC_STHE_TAC(m_p['mt'], m_p['rot'], m_p['mit'], m_p['thk'], Ds, dte, Npt, rp,
                                               lay, L, m_p['pcw'], m_p['pc'], m_p['roc'], m_p['eta'], m_p['cf'],
                                               m_p['cv'], m_p['alpha'], m_p['Nop'], m_p['int_rate'], m_p['n'],
                                               m_p, m_p['ms'], m_p['ros'], m_p['mis'], Nb, Bc)
    return TAC

def AREA_OF(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    Area = Constraints_and_OF_STHE.AREA_OF(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return Area


# endregion
##################################################################################################################
