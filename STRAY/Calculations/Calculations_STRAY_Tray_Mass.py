###################################################################################################################
#region Titles and Header
# Nature: Sieve Tray Tray mass Calculation
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          05-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Sieve Tray -Residence Time related functions
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
    Calculations_STRAY_DC_backup,
    Calculations_STRAY_Geometry
)
#endregion
##################################################################################################################

##################################################################################################################
#region STRAY_Aline=

# Height of the downcomer:
def f_Hdc(lt, hw, hdwap):
    hap = Calculations_STRAY_DC_backup.f_hap(hw, hdwap)
    Hdc = lt - hap
    return Hdc

# Volume of the combination weir/downcomer:
def f_Vwdc(hw,tt,lt,hdwap,lw):
    Hdc = f_Hdc(lt, hw, hdwap)
    Vwdc = (hw + tt + Hdc)*tt*lw
    return Vwdc

# Volume of the tray:
def f_Vt(lw, Dc, wczin, wczout, dh, lp, lay, tt):   
    Ac = Calculations_STRAY_Geometry.f_Ac(Dc)      
    Adc = Calculations_STRAY_Geometry.f_Adc(lw, Dc)
    Ah = Calculations_STRAY_Geometry.f_Ah(lw, Dc, wczin, wczout, dh, lp, lay)
    Vt = (Ac - Adc - Ah)*tt
    return Vt

# Mass of the tray:
def f_Wtray(lw, Dc, wczin, wczout, dh, lp, lay, tt, rotray, hw, lt, hdwap):   
    Vt = f_Vt(lw, Dc, wczin, wczout, dh, lp, lay, tt)
    Vwdc = f_Vwdc(hw,tt,lt,hdwap,lw)
    Wtray = (Vt + Vwdc)*rotray
    return Wtray

