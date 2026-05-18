###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          2024            Diego Oliva               Original
#   0.2          01-Dec-2024     Mariana Mello             Add constraints
#   0.3          03-Mar-2025     Mariana Mello             Changes after add options of tube and shell methods
#   0.4          23-Apr-2025     Mariana Mello             Update to fix error and add constraint Fmin
#   0.5          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
#   0.6          01-Jul-2025     Augusto Vieira            Changed constraints to include fouling dynamics

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



# Thermal and hydraulic calculations
from STHE.Calculations import (
    Calculations_STHE_area,
    Calculations_STHE_U,
    Calculations_STHE_TAC,
    Calculations_STHE_CAPEX,
    Calculations_STHE_velocity_shellside,
    Calculations_STHE_velocity_tubeside,
    Calculations_STHE_Reynolds_shellside,
    Calculations_STHE_Reynolds_tubeside,
    Calculations_STHE_DeltaPshellside,
    Calculations_STHE_DeltaPtubeside,
    Calculations_STHE_correction_factor,
    Calculations_STHE_Fouling_DAE_solver,


)

# Common calculations
from Common_Equations_HEX import (
    Calculations_HEX_LMTD,
    Calculations_HEX_heatload
)

# endregion
################################################################################################################## 

# region Notes for Last Update


"""
Notes for last update:
- Lower bounds for vt_lb and Ret_lb are intrinsically calculated at initial (clean) conditions,
  thus not affected by fouling. Therefore, no fouled condition is used, and I added a `_c` notation
  to indicate this.

- Upper bounds for vt_ub, Ret_ub, and DPt_ub are intrinsically calculated at final (dirtier) conditions
  due to fouling accumulation. I added a `_d` notation to indicate these constraints are based on fouled state.

- Additionally, upper bounds for vt_ub, Ret_ub, and DPt_ub are also calculated at clean conditions 
  as a preprocessing step. I added a `_c` notation to indicate these constraints are based on clean state.
 This eliminates candidates that would clearly violate constraints even before 
  running full fouling dynamics, thereby reducing the number of expensive simulations needed.
"""

# endregion
##################################################################################################################

##################################################################################################################
# region Constraints


def LD_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on L/Ds
    fun_val = m_p['LBLD'] - L / Ds
    return fun_val

def LD_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on L/Ds
    fun_val = L / Ds - m_p['UBLD']
    return fun_val

def lbc_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on lbc
    lbc = (L / (Nb + 1))
    fun_val = 0.2 * Ds - lbc
    return fun_val

def lbc_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on lbc
    lbc = (L / (Nb + 1))
    fun_val = lbc - 1 * Ds
    return fun_val

def lbmax(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    lbc = (L / (Nb + 1))
    if m_p['Shell_Method'] == 'Bell':
        lbmax = (m_p['plbmax1']*dte + m_p['plbmax2'])*0.5
    elif m_p['Shell_Method'] == 'Kern':
        lbmax = lbc*1e10
    fun_val = lbc - lbmax
    return fun_val

def vs_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on vs
    vs = Calculations_STHE_velocity_shellside.STHE_shellside_velocity(m_p['ms'], m_p['ros'], Ds, rp, L, Nb, dte, lay, m_p)
    fun_val = m_p['vsmin'] - vs
    return fun_val

def vs_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on vs
    vs = Calculations_STHE_velocity_shellside.STHE_shellside_velocity(m_p['ms'], m_p['ros'], Ds, rp, L, Nb, dte, lay, m_p)
    fun_val = vs - m_p['vsmax']
    return fun_val

def vt_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on vt is set at clean condition ft_thk = 0
    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(m_p['mt'], m_p['rot'], m_p['thk'], Ds, dte, Npt, rp,
                                                                    lay, m_p,0)
    fun_val = m_p['vtmin'] - vt
    return fun_val

def vt_ub_c(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    
    # upper bound on vt at clean condition ft_thk = 0
    # this constraint will be used only to reduce search space to be submmitted to fouling dynamics calculations

    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(m_p['mt'], m_p['rot'], m_p['thk'], Ds, dte, Npt, rp,
                                                                    lay, m_p,0)
    fun_val = vt - m_p['vtmax']
    return fun_val

def vt_ub_d(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):

    # upper bound on vt at final dirt condition ft_thk = ft_thk at t = campaign time

    mt = m_p['mt']
    rot = m_p['rot']
    Cpt = m_p['Cpt']
    mit = m_p['mit']
    kt = m_p['kt']
    ms = m_p['ms']
    ros = m_p['ros']
    Cps = m_p['Cps']
    mis = m_p['mis']
    ks = m_p['ks']
    Rfs = m_p['Rfs']
    ktube = m_p['ktube']
    yfluid = m_p['yfluid']
    thk = m_p['thk']

    Rft, ft_thk = Calculations_STHE_Fouling_DAE_solver.final_fouling_condition(
        mt, rot, Cpt, mit, kt, ms, ros, Cps, mis, ks, Rfs,
        thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    
    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(m_p['mt'], m_p['rot'], m_p['thk'], Ds, dte, Npt, rp,
                                                                    lay, m_p,ft_thk)
    fun_val = vt - m_p['vtmax']
    return fun_val

def Ret_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # lower bound on Ret at initial clean condition ft_thk = 0
    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(m_p['mt'], m_p['rot'], m_p['mit'], m_p['thk'], Ds,dte, Npt, rp, lay, m_p,0)
    fun_val = m_p['Retmin'] - Ret
    return fun_val

def Ret_ub_c(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    
    # upper bound on Ret at initial clean condition ft_thk = 0
    # this constraint will be used only to reduce search space to be submmitted to fouling dynamics calculations

    
    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(m_p['mt'], m_p['rot'], m_p['mit'], m_p['thk'], Ds,dte, Npt, rp, lay, m_p,0)
    fun_val = Ret - m_p['Retmax']
    return fun_val


def Ret_ub_d(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):

    # upper bound on Ret at final dirt condition ft_thk = ft_thk at t = campaign time
    
    mt = m_p['mt']
    rot = m_p['rot']
    Cpt = m_p['Cpt']
    mit = m_p['mit']
    kt = m_p['kt']
    ms = m_p['ms']
    ros = m_p['ros']
    Cps = m_p['Cps']
    mis = m_p['mis']
    ks = m_p['ks']
    Rfs = m_p['Rfs']
    ktube = m_p['ktube']
    yfluid = m_p['yfluid']
    thk = m_p['thk']

    Rft, ft_thk = Calculations_STHE_Fouling_DAE_solver.final_fouling_condition(
        mt, rot, Cpt, mit, kt, ms, ros, Cps, mis, ks, Rfs,
        thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    
    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(mt, rot, mit, thk, Ds,dte, Npt, rp, lay, m_p,ft_thk)
    fun_val = Ret - m_p['Retmax']
    return fun_val


def Res_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Lower bound on Res
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(m_p['ms'], m_p['ros'], m_p['mis'], Ds, dte, rp,
                                                                       lay, L, Nb, m_p)
    if Res is None:
        return -1e10  # Trim candidate safely

    fun_val = m_p['Resmin'] - Res
    return fun_val


def Res_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on Res
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(m_p['ms'], m_p['ros'], m_p['mis'], Ds, dte, rp,lay, L, Nb, m_p)
    fun_val = Res - m_p['Resmax']
    return fun_val

def DPs_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Upper bound on DPs
    DPs = Calculations_STHE_DeltaPshellside.STHE_shellside_DeltaP(m_p['ms'], m_p['ros'], m_p['mis'], Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    fun_val = DPs - m_p['DPsdisp']
    return fun_val


def DPt_ub_c(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):

    # upper bound on Dpt at initial clean condition ft_thk = 0
    # this constraint will be used only to reduce search space to be submmitted to fouling dynamics calculations
    
    DPt = Calculations_STHE_DeltaPtubeside.STHE_tubeside_DeltaP(m_p['mt'], m_p['rot'], m_p['mit'], m_p['thk'], Ds, dte, Npt, rp, lay, L, m_p,0)
    fun_val = DPt - m_p['DPtdisp']
    return fun_val


def DPt_ub_d(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    
    # upper bound on Dpt at final dirt condition ft_thk = ft_thk at t = campaign time

    
    mt = m_p['mt']
    rot = m_p['rot']
    Cpt = m_p['Cpt']
    mit = m_p['mit']
    kt = m_p['kt']
    ms = m_p['ms']
    ros = m_p['ros']
    Cps = m_p['Cps']
    mis = m_p['mis']
    ks = m_p['ks']
    Rfs = m_p['Rfs']
    ktube = m_p['ktube']
    yfluid = m_p['yfluid']
    thk = m_p['thk']

    Rft, ft_thk = Calculations_STHE_Fouling_DAE_solver.final_fouling_condition(
        mt, rot, Cpt, mit, kt, ms, ros, Cps, mis, ks, Rfs,
        thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    DPt = Calculations_STHE_DeltaPtubeside.STHE_tubeside_DeltaP(mt, rot, mit, thk, Ds, dte,Npt, rp, lay, L, m_p,ft_thk)
    fun_val = DPt - m_p['DPtdisp']
    return fun_val


def F_min(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    F = Calculations_STHE_correction_factor.STHE_correction_factor(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'], Npt,m_p['Xp'])
    fun_val = m_p['F_min'] - F
    return fun_val

def Areq_c(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    
    # upper bound on Dpt at initial clean condition ft_thk = 0
    # this constraint will be used only to reduce search space to be submmitted to fouling dynamics calculations
    
    mt = m_p['mt']
    rot = m_p['rot']
    Cpt = m_p['Cpt']
    mit = m_p['mit']
    kt = m_p['kt']
    ms = m_p['ms']
    ros = m_p['ros']
    Cps = m_p['Cps']
    mis = m_p['mis']
    ks = m_p['ks']
    Rfs = m_p['Rfs']
    ktube = m_p['ktube']
    yfluid = m_p['yfluid']
    thk = m_p['thk']


    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'])
    U = Calculations_STHE_U.STHE_overall_coefficient(
        mt, rot, Cpt, mit, kt, 0,
        ms, ros, Cps, mis, ks, Rfs,
        thk, ktube, yfluid,
        Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, 0)
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'])
    F = Calculations_STHE_correction_factor.STHE_correction_factor(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'], Npt,
                                                                   m_p['Xp'])
    A = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)
    Areq = Q / (U * LMTD * F)
    fun_val = (Areq * (1 + m_p['Aexc'] / 100)) - A
    return fun_val

def Areq_d(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):

    # upper bound on Dpt at final dirt condition ft_thk = ft_thk at t = campaign time


    mt = m_p['mt']
    rot = m_p['rot']
    Cpt = m_p['Cpt']
    mit = m_p['mit']
    kt = m_p['kt']
    ms = m_p['ms']
    ros = m_p['ros']
    Cps = m_p['Cps']
    mis = m_p['mis']
    ks = m_p['ks']
    Rfs = m_p['Rfs']
    ktube = m_p['ktube']
    yfluid = m_p['yfluid']
    thk = m_p['thk']

    Rft, ft_thk = Calculations_STHE_Fouling_DAE_solver.final_fouling_condition(
        mt, rot, Cpt, mit, kt, ms, ros, Cps, mis, ks, Rfs,
        thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)

    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['mh'], m_p['Cph'], m_p['Thi'], m_p['Tho'])
    U = Calculations_STHE_U.STHE_overall_coefficient(
        mt, rot, Cpt, mit, kt, Rft,
        ms, ros, Cps, mis, ks, Rfs,
        thk, ktube, yfluid,
        Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk)
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'])
    F = Calculations_STHE_correction_factor.STHE_correction_factor(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'], Npt,
                                                                   m_p['Xp'])
    A = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)
    Areq = Q / (U * LMTD * F)
    fun_val = (Areq * (1 + m_p['Aexc'] / 100)) - A
    return fun_val

def TAC_OF(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    mt = m_p['mt']
    rot = m_p['rot']
    Cpt = m_p['Cpt']
    mit = m_p['mit']
    kt = m_p['kt']
    ms = m_p['ms']
    ros = m_p['ros']
    Cps = m_p['Cps']
    mis = m_p['mis']
    ks = m_p['ks']
    Rfs = m_p['Rfs']
    thk = m_p['thk']
    ktube = m_p['ktube']
    yfluid = m_p['yfluid']

    Rft, ft_thk = Calculations_STHE_Fouling_DAE_solver.final_fouling_condition(
        mt, rot, Cpt, mit, kt, ms, ros, Cps, mis, ks, Rfs,
        thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p
    )

    TAC = Calculations_STHE_TAC.STHE_TAC(
        m_p['int_rate'], m_p['n'], m_p['par_a'], m_p['par_b'], m_p['Nop'], m_p['pc'],
        m_p['eta'], Ds, dte, Npt, rp, lay, L, ms, mt, ros, rot, mis, mit, thk, Nb, Bc, m_p, ft_thk
    )
    return TAC


def LB_TAC(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    TAC = TAC_OF(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    return TAC, None, None

    
def AREA_OF(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    Area = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)
    return Area
    
def CAPEX_OF(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    CAPEX = Calculations_STHE_CAPEX.STHE_CAPEX(m_p['par_a'], m_p['par_b'], Ds, dte, Npt, rp, lay, L, m_p)
    return CAPEX


# endregion
##################################################################################################################
