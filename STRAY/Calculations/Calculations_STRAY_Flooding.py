###################################################################################################################
#region Titles and Header
# Nature: Sieve Tray Flooding Model
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          05-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Sieve Tray - Flooding related functions
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################

##################################################################################################################
#region Import Library
import numpy as np
from STRAY.Calculations import Calculations_STRAY_Geometry
#endregion
##################################################################################################################

##################################################################################################################
#region STRAY_Aline=

# K1, depending on Ah/Aa where Aa = f(lw, Dc, wczin, wczout) and Ah = f(lw, Dc, wczin, wczout, dh, lp, lay):
def f_K1(lw, Dc, wczin, wczout, dh, lp, lay):
    Aa = Calculations_STRAY_Geometry.f_Aa(lw, Dc, wczin, wczout)
    Ah = Calculations_STRAY_Geometry.f_Ah(lw, Dc, wczin, wczout, dh, lp, lay)
    Ah_Aa = Ah/Aa
    vK1 = 0.8*np.ones(Ah_Aa.shape)
    if isinstance(Ah_Aa,float) or isinstance(Ah_Aa,int):
        if Ah_Aa >= 0.08: vK1 = 0.9
        elif Ah_Aa >= 0.1: vK1 = 1
    else:
        vK1[Ah_Aa >= 0.08] = 0.9
        vK1[Ah_Aa >= 0.1] = 1
    #print('vK1',vK1)
    return vK1

# Liquid-vapor flow factor (Flv) defined by liquid and vapor mass flow rates (Lw, Vw) and specific masses (rol, rov):
def f_Flv(Lw, Vw, rol, rov):
    Flv = (Lw / Vw) * np.sqrt(rov / rol)
    #print('Flv',Flv)
    return Flv

# Csb, defined by liquid-vapor flow factor (Flv = f(Lw, Vw, rol, rov)) and tray spacing (lt):
def f_Csb(Lw, Vw, rol, rov, lt):
    Flv = f_Flv(Lw, Vw, rol, rov)
    Csb = 0.0129 + 0.1674*lt + 0.0063*Flv - 0.2686*lt*Flv - 0.008*(Flv**2) + 0.01448*lt*(Flv**2)
    #print('Csb',Csb)
    return Csb

# Vapor flow velocity (un), defined by vapor flow area (An = f(lw, Dc)), vapor mass flow rate (Vw) and vapor specific mass (rov):
def f_un(lw, Dc, Vw, rov):
    An = Calculations_STRAY_Geometry.f_An(lw, Dc)
    un = Vw/(rov*An)
    #print('un',un)
    return un

# Flooding velocity (uflood) defined by K1 = f(lw, Dc, wczin, wczout, dh, lp, lay), Csb = f(Lw, Vw, rol, rov, lt), specific mass of liquid and vapor (rol and rov) and surface tension (sig)
def f_uflood(lw, Dc, wczin, wczout, dh, lp, lay, Lw, Vw, rol, rov, lt, sig):
    K1 = f_K1(lw, Dc, wczin, wczout, dh, lp, lay)
    Csb = f_Csb(Lw, Vw, rol, rov, lt)
    uflood = K1*Csb*np.sqrt((rol - rov)/rov)*((sig/0.02)**0.2)
    #print('uflood',uflood)
    return uflood

