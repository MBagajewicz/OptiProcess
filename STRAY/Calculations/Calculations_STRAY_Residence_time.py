###################################################################################################################
#region Titles and Header
# Nature: Sieve Tray Residence Time Calculation
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
    Calculations_STRAY_Geometry,
    Calculations_STRAY_DC_backup
)
#endregion
##################################################################################################################

##################################################################################################################
#region STRAY_Aline=

# Residence time (time) defined by height of the downcomer backup (hb = f(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov, tt, rol, Lw, hw, hdwap)), downcomer area (Adc = f(lw, Dc)), liquid specific mass and mass flow rate (rol and Lw):
def f_time(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov, tt, rol, Lw, hw, hdwap):
    hb = Calculations_STRAY_DC_backup.f_hb(lw, Dc, wczin, wczout, dh, lp, lay, Vw, rov, tt, rol, Lw, hw, hdwap)
    Adc = Calculations_STRAY_Geometry.f_Adc(lw, Dc)
    time = (Adc*hb*rol)/Lw
    return time
