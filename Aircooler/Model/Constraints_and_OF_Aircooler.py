###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          2024            Diego Oliva               Original
#   0.2          02-Jan-2025     Mariana Mello             Add constraints aircooler
#   0.3          28-Feb-2025     Alice Peccini             Relocating folders 
#   0.4          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
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
from math import pi
from Aircooler.Calculations import (
    Calculations_aircooler_Aot,
    Calculations_aircooler_Ar,
    Calculations_aircooler_area,
    Calculations_aircooler_areq,
    Calculations_aircooler_ltp,
    Calculations_aircooler_deltaP_tube,
    Calculations_aircooler_TAC,
    Calculations_aircooler_Re_hotstream,
    Calculations_aircooler_Re_coldstream,
    Calculations_aircooler_Gh
)
# endregion
##################################################################################################################

##################################################################################################################
# region calculations

def Reh_lb(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Npt = m_p['ppNpt'][aircoolerconfig.astype(int)]
    Nr = m_p['ppNr'][aircoolerconfig.astype(int)]
    Reh = Calculations_aircooler_Re_hotstream.aircooler_Reynolds_hotstream(Dte, m_p['thk'], Npt, m_p['mh'], Nbay, Nbbay,
                                                                           Ntr, Nr, m_p['mih'])
    #print('Reh',Reh)
    fun_val = m_p['Rehmin'] - Reh
    return fun_val


def L_Dti_ratio_lb(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Dte = m_p['ppDte'][finnedsurface.astype(int)]

    Dti = Dte - 2*m_p['thk']
    L_Dti_ratio = L/Dti
    fun_val = m_p['LDti_lb'] - L_Dti_ratio
    return fun_val


def Rec_lb(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Nf = m_p['ppNf'][finnedsurface.astype(int)]
    Lf = m_p['ppLf'][finnedsurface.astype(int)]
    tf = m_p['pptf'][finnedsurface.astype(int)]

    Rec = Calculations_aircooler_Re_coldstream.aircooler_Reynolds_coldstream(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf,
                                                                             m_p['mh'], m_p['Cph'], m_p['Thi'],
                                                                             m_p['Tho'], m_p['Tco'], m_p['Tci'])
    #print('Rec',Rec)
    fun_val = m_p['Recmin'] - Rec
    return fun_val


def Rec_ub(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Nf = m_p['ppNf'][finnedsurface.astype(int)]
    Lf = m_p['ppLf'][finnedsurface.astype(int)]
    tf = m_p['pptf'][finnedsurface.astype(int)]

    Rec = Calculations_aircooler_Re_coldstream.aircooler_Reynolds_coldstream(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf,
                                                                             m_p['mh'], m_p['Cph'], m_p['Thi'],
                                                                             m_p['Tho'], m_p['Tco'], m_p['Tci'])
    fun_val = Rec - m_p['Recmax']
    return fun_val


def Ltp_lb(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Dte = m_p['ppDte'][finnedsurface.astype(int)]

    Ltp = Calculations_aircooler_ltp.aircooler_calc_ltp(Dte, rp)
    fun_val = m_p['Ltpmin'] - Ltp
    return fun_val


def Ltp_ub(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Dte = m_p['ppDte'][finnedsurface.astype(int)]

    Ltp = Calculations_aircooler_ltp.aircooler_calc_ltp(Dte, rp)
    fun_val = Ltp - m_p['Ltpmax']
    return fun_val


def Aot_Ar_ratio_lb(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Lf = m_p['ppLf'][finnedsurface.astype(int)]
    tf = m_p['pptf'][finnedsurface.astype(int)]
    Nf = m_p['ppNf'][finnedsurface.astype(int)]

    Aot = Calculations_aircooler_Aot.aircooler_Aot(Dte, Lf, tf, Nf)
    Ar = Calculations_aircooler_Ar.aircooler_Ar(Dte)
    AotAr_ratio = Aot/Ar
    fun_val = m_p['AotAr_lb'] - AotAr_ratio
    return fun_val


def Aot_Ar_ratio_ub(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Lf = m_p['ppLf'][finnedsurface.astype(int)]
    tf = m_p['pptf'][finnedsurface.astype(int)]
    Nf = m_p['ppNf'][finnedsurface.astype(int)]

    Aot = Calculations_aircooler_Aot.aircooler_Aot(Dte, Lf, tf, Nf)
    Ar = Calculations_aircooler_Ar.aircooler_Ar(Dte)
    AotAr_ratio = Aot / Ar
    fun_val = AotAr_ratio - m_p['AotAr_ub']
    return fun_val


def Lf_tf_ratio_lb(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Lf = m_p['ppLf'][finnedsurface.astype(int)]
    tf = m_p['pptf'][finnedsurface.astype(int)]

    Lftf_ratio = Lf/tf
    fun_val = m_p['Lftf_lb'] - Lftf_ratio
    return fun_val


def Df_Dte_ratio_ub(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Lf = m_p['ppLf'][finnedsurface.astype(int)]

    Df = Dte + 2*Lf
    DfDte_ratio = Df/Dte
    fun_val = DfDte_ratio - m_p['DfDte_ub']
    return fun_val


def Areq(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    # Required area constraint
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Lf = m_p['ppLf'][finnedsurface.astype(int)]
    tf = m_p['pptf'][finnedsurface.astype(int)]
    Nf = m_p['ppNf'][finnedsurface.astype(int)]
    Nr = m_p['ppNr'][aircoolerconfig.astype(int)]
    Npt = m_p['ppNpt'][aircoolerconfig.astype(int)]
    F = m_p['ppF'][aircoolerconfig.astype(int)]

    A = Calculations_aircooler_area.aircooler_area(Dte, Lf, tf, Nf, Nbay, Nbbay, Nr, Ntr, L)
    #print('Area',A)
    Areq = Calculations_aircooler_areq.aircooler_areq(m_p['Thi'], m_p['Tho'], m_p['Tci'], m_p['Tco'], Npt, Dte, m_p['thk'],
                                                      m_p['mh'], Nbay, Nbbay, Ntr, Nr, m_p['mih'], m_p['Cph'], m_p['kt'],
                                                      m_p['kh'], Lf, tf, Nf, rp, L, m_p['Rfc'], m_p['Rfh'], m_p['kf'], F)
    fun_val = m_p['Aexc'] - (A/Areq)
    return fun_val


def min_gap(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    # The value of the tube pitch ratio must allow a minimum gap between adjacent fin tips
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Lf = m_p['ppLf'][finnedsurface.astype(int)]

    Ltp = Calculations_aircooler_ltp.aircooler_calc_ltp(Dte, rp)
    Df = Dte + 2*Lf
    fun_val = Df + m_p['thk'] - Ltp
    return fun_val


def DPh_ub(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    # Upper bound on DPh
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Nr = m_p['ppNr'][aircoolerconfig.astype(int)]
    Npt = m_p['ppNpt'][aircoolerconfig.astype(int)]

    DPh = Calculations_aircooler_deltaP_tube.aircooler_deltaP_tube(Dte, m_p['thk'], Npt, m_p['mh'], Nbay, Nbbay, Ntr,
                                                                   Nr, m_p['mih'], L, m_p['roh'])
    #print('DPh',DPh)
    fun_val = DPh - m_p['DPhdisp']
    return fun_val


def vt_lb(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    # Tube-side flow velocity lower bound
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Nr = m_p['ppNr'][aircoolerconfig.astype(int)]
    Npt = m_p['ppNpt'][aircoolerconfig.astype(int)]
    Gh = Calculations_aircooler_Gh.aircooler_Gh(Dte, m_p['thk'], m_p['mh'], Npt, Ntr, Nr, Nbay, Nbbay)
    value = Gh/m_p['roh']
    fun_val = m_p['vhmin'] - value
    return fun_val


def vt_ub(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    # Tube-side flow velocity upper bound
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Nr = m_p['ppNr'][aircoolerconfig.astype(int)]
    Npt = m_p['ppNpt'][aircoolerconfig.astype(int)]

    Dti = Dte - 2*m_p['thk']
    Gh = (m_p['mh'] * (Npt / (Ntr*Nr*Nbay*Nbbay))) / (pi*(Dti**2)/4)
    value = Gh/m_p['roh']
    fun_val = value - m_p['vhmax']
    return fun_val


def const_1(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Dte = m_p['ppDte'][finnedsurface.astype(int)]

    Ltp = Calculations_aircooler_ltp.aircooler_calc_ltp(Dte, rp)
    W = Ltp*Ntr
    part1 = Nbbay * W
    part2 = Dfan + 2*m_p['fd']
    fun_val = part2 - part1
    return fun_val


def const_2(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Lfanp = 1.1*Dfan
    fun_val = (Dfan + 2*m_p['fl']) - (L - Lfanp*(Nfanbay - 1))
    return fun_val


def const_3(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    Dte = m_p['ppDte'][finnedsurface.astype(int)]

    Ltp = Calculations_aircooler_ltp.aircooler_calc_ltp(Dte, rp)
    W = Ltp*Ntr
    fun_val = (0.4*Nbbay*W*L) - ((pi/4)*Nfanbay*Dfan**2)
    return fun_val


def TAC_OF(finnedsurface, L, rp, Nbay, Nbbay, Ntr, aircoolerconfig, Nfanbay, Dfan, m_p):
    # Objective function
    Dte = m_p['ppDte'][finnedsurface.astype(int)]
    Lf = m_p['ppLf'][finnedsurface.astype(int)]
    tf = m_p['pptf'][finnedsurface.astype(int)]
    Nf = m_p['ppNf'][finnedsurface.astype(int)]
    Nr = m_p['ppNr'][aircoolerconfig.astype(int)]
    Npt = m_p['ppNpt'][aircoolerconfig.astype(int)]


    TAC = Calculations_aircooler_TAC.aircooler_TAC(m_p['int_rate'], m_p['y'], Ntr, Nr, Nbay, Nbbay, Dte, m_p['thk'], Nf,
                                                   tf, L, Nfanbay, Dfan, rp, Lf, m_p['Tco'], m_p['Tci'], m_p['etafan'],
                                                   m_p['etasr'], m_p['etamotor'], m_p['hop'], m_p['Cen'], m_p['mh'],
                                                   m_p['Cph'], m_p['Thi'], m_p['Tho'])
    return TAC


# endregion
##################################################################################################################

