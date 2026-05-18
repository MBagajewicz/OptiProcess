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
from math import pi
import numpy as np
#endregion

#region Calculations

def HEATER_Di_Tube(Do):
    # tube inside diameter
    Di_tube = Do - 0.5/12
    return Di_tube

def HEATER_df(lf, Do):
    # fin diameter
    df = 2 * lf + Do
    return df

def HEATER_dcr(Do, Rpr):
    # distance between tube centers in the radiant section
    #Rpr = np.array(Rpr).astype(np.float64)
    dcr = Do * Rpr
    return dcr

def HEATER_dch(Do, Rph):
    # distance between finned tube centers(horizontal) in the convection section
    dch = Do * Rph
    return dch

def HEATER_dcv(Do, Rpv):
    # distance between finned tube centers(vertical) in the convection section
    dcv = Do * Rpv
    return dcv

def HEATER_Ntshield(Npconv, Npasses):
    # number of shield tubes
    Ntshield = Npconv * Npasses
    return Ntshield

def HEATER_Ntwall(Nprad, Npasses, Ntceil):
    # number of both wall side tubes
    #Nprad = np.array(Nprad).astype(np.float64)
    #Npasses = np.array(Npasses).astype(np.float64)
    #Ntceil = np.array(Ntceil).astype(np.float64)

    Ntwall = Nprad * Npasses - Ntceil
    return Ntwall

def HEATER_Ntrad(Nprad, Npconv, Npasses):
    # number of tubes on radiant section
    Ntshield = HEATER_Ntshield(Npconv, Npasses)
    Ntrad = Nprad * Npasses + Ntshield
    return Ntrad

def HEATER_Ntconv(Npconv, Npasses, Nrconv):
    # number of tubes on convection section
    Ntconv = Npconv * Npasses * Nrconv
    return Ntconv
