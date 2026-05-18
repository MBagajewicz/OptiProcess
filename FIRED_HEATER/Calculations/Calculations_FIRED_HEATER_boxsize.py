#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          24-Mar-2025     Sung Young Kim            Original

##################################################################################################################
#endregion

#region Import Library
from FIRED_HEATER.Calculations import Calculations_FIRED_HEATER_tubes
from math import pi
#endregion


#region Calculations

def HEATER_Wconv(Npconv, Npasses, lf, Do, Rph):
    # width of convection section
    delta_Wconv = 1/12 + 0 * Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)
    df = Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)
    dch= Calculations_FIRED_HEATER_tubes.HEATER_dch(Do, Rph)
    Wconv = (Npconv * Npasses-1)*dch + dch/2 + df + 2* delta_Wconv
    return Wconv

def HEATER_Wrad(Ntceil, Do, Rpr, Npconv, Npasses, lf, Rph ):
    # width of radiant section
    delta_Wrad = 1/12
    # delta_Wrad = 1/12 + 0 * Do

    dcr = Calculations_FIRED_HEATER_tubes.HEATER_dcr(Do, Rpr)
    Wconv = HEATER_Wconv(Npconv, Npasses, lf, Do, Rph )
    Wrad = 2*( (Ntceil/2) * dcr+ Do + delta_Wrad ) + Wconv
    return Wrad

def HEATER_Hrad(Do, Nprad, Npasses, Ntceil, Rpr):
    # height of radiant section
    delta_Hrad = 1/12
    #delta_Hrad = 1/12 + 0 * Do
    Ntwall = Calculations_FIRED_HEATER_tubes.HEATER_Ntwall(Nprad, Npasses, Ntceil)
    dcr = Calculations_FIRED_HEATER_tubes.HEATER_dcr(Do, Rpr)
    Hrad = (Ntwall/2)* dcr + Do + 2*delta_Hrad
    return Hrad

def HEATER_Hconv(lf, Do, Rpv, Nrconv):
    # height of convection section
    delta_Hconv = 1/12 + 0 * Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)
    df = Calculations_FIRED_HEATER_tubes.HEATER_df(lf, Do)
    dcv= Calculations_FIRED_HEATER_tubes.HEATER_dch(Do, Rpv)
    Hconv = (Nrconv + 1) * dcv + Do/2  + df/2 + delta_Hconv
    return Hconv

def HEATER_Htotal(Hs, Do, Nprad, Npasses, Ntceil, Rpr, lf, Rpv, Nrconv):
    # total height of heater
    Hrad = HEATER_Hrad(Do, Nprad, Npasses, Ntceil, Rpr)
    Hconv = HEATER_Hconv(lf, Do, Rpv, Nrconv)
    H_total = Hrad + Hconv + Hs
    return H_total

def HEATER_El(L, pk1):
    # exposed length
    El = L - pk1
    return El

def HEATER_Boxsize(L,Do, Nprad, Npasses, Ntceil, Rpr, pk1, Npconv, lf, Rph):
    # boxsize
    Hrad = HEATER_Hrad(Do, Nprad, Npasses, Ntceil, Rpr)
    Wrad = HEATER_Wrad(Ntceil, Do, Rpr, Npconv, Npasses, lf, Rph)
    El = HEATER_El(L, pk1)
    Ntrad = Calculations_FIRED_HEATER_tubes.HEATER_Ntrad(Nprad, Npconv, Npasses)
    Boxsize = L * Hrad * Wrad /(3.141516 *Do * El * Ntrad)
    return Boxsize

