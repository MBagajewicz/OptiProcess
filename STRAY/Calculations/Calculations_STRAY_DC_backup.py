###################################################################################################################
#region Titles and Header
# Nature: Sieve Tray Downcomer Backup Model
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          05-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Sieve Tray - Downcomer Backup related functions
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################

##################################################################################################################
#region Import Library
from STRAY.Calculations import (
    Calculations_STRAY_Geometry,
    Calculations_STRAY_Weeping
)
#endregion
##################################################################################################################

##################################################################################################################
#region STRAY_Aline=

# Height of the clearance inder the downcomer (hap) defined by weir height (hw) and difference between weir and clearance height (hdwap):
def f_hap(hw, hdwap):
    hap = hw - hdwap
    #print('hap',hap)
    return hap

# Clearance area under the downcomer (Aap) defined by height of the clearance inder the downcomer (hap = f(hw, hdwap)) and weir length (lw):
def f_Aap(hw, hdwap, lw):
    hap = f_hap(hw, hdwap)
    Aap = hap*lw
    #print('Aap',Aap)
    return Aap

# Pressure drp in the downcomer (hdc) defined by clearance area under the downcomer (Aap = f(hw, hdwap, lw)) and liquid mass flow rate and specific mass (Lw and rol):
def f_hdc(hw, hdwap, lw, Lw, rol):
    Aap = f_Aap(hw, hdwap, lw)
    hdc = 166*0.001*(Lw/(rol*Aap))
    #print('hdc',hdc)
    return hdc

# Orifice coefficient (Co) defined by active area (Aa = f(lw, Dc, wczin, wczout)), hole area (Ah = f(lw, Dc, wczin, wczout, dh, lp, lay)), tray thickness (tt) and hole diameter (dh):
def f_Co(lw, Dc, wczin, wczout, dh, lp, lay, tt):
    Aa = Calculations_STRAY_Geometry.f_Aa(lw, Dc, wczin, wczout)
    Ah = Calculations_STRAY_Geometry.f_Ah(lw, Dc, wczin, wczout, dh, lp, lay)
    Co = 0.6323 - 0.0255*(tt/dh) + 0.1495*((tt/dh)** 2) + 0.777*(Ah/Aa)
    #print('Co',Co)
    return Co

# Dry tray drop (hd) defined by flow velocity throughout the tray holes (uh = f(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov)), orifice coefficient (Co = f(lw, Dc, wczin, wczout, dh, lp, lay, tt)) and vapor and liquid specific masses (rov and rol):
def f_hd(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov, tt, rol):
    uh = Calculations_STRAY_Weeping.f_uh(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov)
    Co = f_Co(lw, Dc, wczin, wczout, dh, lp, lay, tt)
    hd = 51*0.001*((uh/Co)**2)*(rov/rol)
    #print('hd',hd)
    return hd

# Residual pressure drop (hr) defined by liquis specific mass (rol):
def f_hr(rol):
    hr = 12.5/rol
    #print('hr',hr)
    return hr

# Total tray pressure drop (ht) defined by dry tray drop (hd = f(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov, tt, rol)), height of the liquid cres over the weir (how = f(lw, Lw, rol)), residual pressure drop (hr = f(rol)) and weir heigth (hw):
def f_ht(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov, tt, rol, Lw, hw):
    hd = f_hd(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov, tt, rol)
    how = Calculations_STRAY_Weeping.f_how(lw, Lw, rol)
    hr = f_hr(rol)
    ht = hw + how + hd + hr
    #print('ht',ht)
    return ht

# Height of the downcomer backup (hb) defined by total tray pressure drop (ht = f(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov, tt, rol, Lw, hw)), height of the liquid cres over the weir (how = f(lw, Lw, rol)) and pressure drp in the downcomer (hdc = f(hw, hdwap, lw, Lw, rol)):
def f_hb(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov, tt, rol, Lw, hw, hdwap):
    ht = f_ht(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov, tt, rol, Lw, hw)
    how = Calculations_STRAY_Weeping.f_how(lw, Lw, rol)
    hdc = f_hdc(hw, hdwap, lw, Lw, rol)
    hb = hw + how + ht + hdc
    #print('hb',hb)
    return hb
