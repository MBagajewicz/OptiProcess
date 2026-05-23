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
from HSTC.Calculations import (
    Calculations_HSTC_DeltaP,
    Calculations_HSTC_Geometry,
    Calculations_HSTC_Heat_transfer,
    Calculations_HSTC_Shell_Flow,
    Calculations_HSTC_Tube_Flow
)

# endregion
##################################################################################################################

##################################################################################################################
# region Horizontal Shell and Tube Condenser

# ----------------------------------------------------------------------------------------------------------------
# Trimming Functions
# ----------------------------------------------------------------------------------------------------------------

def LD_lb(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Lower bound on L/Ds
    fun_val = m_p['LBLD'] - L/Ds
    return fun_val

def LD_ub(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Upper bound on L/Ds
    fun_val = L/Ds - m_p['UBLD']
    return fun_val

def lbc_lb(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Lower bound on lbc
    lbc = (L/(Nb + 1))
    fun_val = m_p['LBlbcD'] - lbc/Ds
    return fun_val

def lbc_ub(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Upper bound on lbc
    lbc = (L/(Nb + 1))
    fun_val = lbc/Ds - m_p['UBlbcD']
    return fun_val

def vs_lb(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Lower bound on vs
    vs = Calculations_HSTC_Shell_Flow.fun_vs(Ds, rp, L, Nb, m_p['m_s'], m_p['rov_s'])
    print(vs)
    fun_val = m_p['vsmin'] - vs
    return fun_val

def vs_ub(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Upper bound on vs
    vs = Calculations_HSTC_Shell_Flow.fun_vs(Ds, rp, L, Nb, m_p['m_s'], m_p['rov_s'])
    fun_val = vs - m_p['vsmax']
    return fun_val

def vt_lb(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Lower bound on vt
    vt = Calculations_HSTC_Tube_Flow.fun_vt(Ds, dte, Npt, rp, lay, m_p['m_t'], m_p['ro_t'], m_p['thk'], m_p['Fsc'])
    fun_val = m_p['vtmin'] - vt
    return fun_val

def vt_ub(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Upper bound on vt
    vt = Calculations_HSTC_Tube_Flow.fun_vt(Ds, dte, Npt, rp, lay, m_p['m_t'], m_p['ro_t'], m_p['thk'], m_p['Fsc'])
    fun_val = vt - m_p['vtmax']
    return fun_val

def Ret_lb(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Lower bound on Ret
    Ret = Calculations_HSTC_Tube_Flow.fun_Ret(Ds, dte, Npt, rp, lay, m_p['m_t'], m_p['ro_t'], m_p['mi_t'], m_p['thk'], m_p['Fsc'])
    fun_val = m_p['Retmin'] - Ret
    return fun_val

def Res_lb(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Lower bound on Ret
    Res = Calculations_HSTC_Shell_Flow.fun_Res(Ds, dte, rp, lay, L, Nb, m_p['m_s'], m_p['rov_s'], m_p['miv_s'])
    fun_val = m_p['Resmin'] - Res
    return fun_val

def dPt_ub(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    dPt = Calculations_HSTC_DeltaP.fun_dPt(Ds, dte, Npt, rp, lay, L, m_p['m_t'], m_p['ro_t'], m_p['mi_t'], m_p['thk'], m_p['Fsc'])
    fun_val = dPt - m_p['dPt_disp']
    return fun_val

def dPs_ub(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    dPs = Calculations_HSTC_DeltaP.fun_dPs(Ds, dte, rp, lay, L, Nb, m_p['m_s'], m_p['rov_s'], m_p['miv_s'])
    dPs_c = Calculations_HSTC_DeltaP.fun_dPs_corr(dPs)
    fun_val = dPs_c - m_p['dPs_disp']
    return fun_val

def Aexc(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Required area constraint
    U = Calculations_HSTC_Heat_transfer.fun_U(Ds, dte, Npt, rp, lay, L, m_p['m_t'], m_p['ro_t'], m_p['mi_t'], m_p['k_t'], m_p['Rf_t'],
                                                     m_p['m_s'], m_p['ro_s'], m_p['rov_s'], m_p['mi_s'], m_p['k_s'], m_p['Rf_s'],
                                                     m_p['thk'], m_p['ktube'], m_p['Prt'], m_p['Fsc'])
    A = Calculations_HSTC_Geometry.fun_A(Ds, dte, Npt, rp, lay, L, m_p['Fsc'])
    Areq = Calculations_HSTC_Heat_transfer.fun_A_req(U, m_p['Q'], m_p['dTLM'])
    fun_val = (Areq*(1 + m_p['Aexc'])) - A
    return fun_val

# ----------------------------------------------------------------------------------------------------------------
# Objective Function
# ----------------------------------------------------------------------------------------------------------------

def Area_OF(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    # Objective function
    HE_Area = Calculations_HSTC_Geometry.fun_A(Ds, dte, Npt, rp, lay, L, m_p['Fsc'])
    return HE_Area

def Cost_OF(Ds, dte, Npt, rp, lay, L, Nb, m_p):
    Area = Calculations_HSTC_Geometry.fun_A(Ds, dte, Npt, rp, lay, L, m_p['Fsc'])
    HE_CAPEX = 28000 + 54*Area**1.2
    return HE_CAPEX

# endregion
##################################################################################################################

