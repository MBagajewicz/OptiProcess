###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          27-Jan-2025     Miguel Bagajewicz         Original
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
from Kettle.Calculations import (
    Calculations_Kettle_Reynolds_tubeside,
    Calculations_Kettle_velocity_tubeside,
    Calculations_Kettle_Reynolds_shellside,
    Calculations_Kettle_velocity_shellside,
    Calculations_Kettle_area,
    Calculations_Kettle_OF,
    Calculations_Kettle_U
)
from Common_Equations_HEX import Calculations_HEX_LMTD, Calculations_HEX_heatload
# endregion
##################################################################################################################

##################################################################################################################
# region Example 1

def LD_lb(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Lower bound on L/Ds
    fun_val = pd['LBLD'] - L / Ds
    return fun_val

def LD_ub(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Upper bound on L/Ds
    fun_val = L / Ds - pd['UBLD']
    return fun_val

def lbc_lb(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Lower bound on lbc
    lbc = (L / (Nb + 1))
    fun_val = 0.2 * Ds - lbc
    return fun_val

def lbc_ub(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Upper bound on lbc
    lbc = (L / (Nb + 1))
    fun_val = lbc - 1 * Ds
    return fun_val

def vs_lb(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Lower bound on vs
    vs = Calculations_Kettle_velocity_shellside.STHE_shellside_velocity(pd['ms'], pd['ros'], Ds, rp, L, Nb)
    fun_val = pd['vsmin'] - vs
    return fun_val

def vs_ub(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Upper bound on vs
    vs = Calculations_Kettle_velocity_shellside.STHE_shellside_velocity(pd['ms'], pd['ros'], Ds, rp, L, Nb)
    fun_val = vs - pd['vsmax']
    return fun_val

def vt_lb(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Lower bound on vt
    vt = Calculations_Kettle_velocity_tubeside.STHE_tubeside_velocity(pd['mt'], pd['rot'], pd['thk'], Ds, dte, Npt, rp,
                                                                    lay)
    fun_val = pd['vtmin'] - vt
    return fun_val

def vt_ub(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Upper bound on vt
    vt = Calculations_Kettle_velocity_tubeside.STHE_tubeside_velocity(pd['mt'], pd['rot'], pd['thk'], Ds, dte, Npt, rp,
                                                                    lay)
    fun_val = vt - pd['vtmax']
    return fun_val

def Ret_lb(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Lower bound on Ret
    Ret = Calculations_Kettle_Reynolds_tubeside.STHE_Reynolds_tubeside(pd['mt'], pd['rot'], pd['mit'], pd['thk'], Ds, dte,
                                                                     Npt, rp, lay)
    fun_val = pd['Retmin'] - Ret
    return fun_val

def Res_lb(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Lower bound on Ret
    Res = Calculations_Kettle_Reynolds_shellside.STHE_Reynolds_shellside(pd['ms'], pd['ros'], pd['mis'], Ds, dte, rp, lay,
                                                                       L, Nb)
    fun_val = pd['Resmin'] - Res
    return fun_val

def Areq(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Required area constraint
    Q = Calculations_HEX_heatload.HEX_heat_load(pd['mh'], pd['Cph'], pd['Thi'], pd['Tho'])
    U = Calculations_Kettle_U.Kettle_overall_coefficient(pd['mt'], pd['rot'], pd['Cpt'], pd['mit'], pd['kt'], pd['Rft'],
                                                     pd['ms'], pd['ros'], pd['Cps'], pd['mis'], pd['ks'], pd['Rfs'],
                                                     pd['thk'], pd['ktube'], pd['yfluid'], Ds, dte, Npt, rp, lay, L, Nb)
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(pd['Thi'], pd['Tho'], pd['Tci'], pd['Tco'])
    A = Calculations_Kettle_area.Kettle_area(Ds, dte, Npt, rp, lay, L)
    Areq = Q / (U * LMTD)
    fun_val = (Areq * (1 + pd['Aexc'] / 100)) - A
    return fun_val

def Kettle_OF(Ds, dte, Npt, rp, lay, L, Nb, pd):
    # Objective function
    OF_Solution = Calculations_Kettle_OF.Kettle_OF(pd['int_rate'], pd['n'], pd['par_a'], pd['par_b'], pd['Nop'], pd['pc'],
                                         pd['eta'], Ds, dte, Npt, rp, lay, L, pd['ms'], pd['mt'], pd['ros'], pd['rot'],
                                         pd['mis'], pd['mit'], pd['thk'], Nb)
    return OF_Solution

# endregion
##################################################################################################################

