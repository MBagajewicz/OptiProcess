#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          27-Jan-2025     Miguel Bagajewicz              Original

##################################################################################################################
#endregion


#region Import Library
from Kettle.Calculations import Calculations_Kettle_DeltaPtubeside, Calculations_Kettle_DeltaPshellside, Calculations_Kettle_area
#endregion

#region Calculations

def Kettle_OF(int_rate, n, par_a, par_b, Nop, pc, eta, Ds, dte, Npt, rp, lay, L, ms, mt, ros, rot, mis, mit, thk, Nb):
    r = ((int_rate*(1+int_rate)**n))/(((1+int_rate)**n) - 1)
    Atot = Calculations_Kettle_area.Kettle_area(Ds, dte, Npt, rp, lay, L)
    Cap = par_a*Atot**par_b                             # Capital cost
    deltaPs = Calculations_Kettle_DeltaPshellside.Kettle_shellside_DeltaP(ms, ros, mis, Ds, dte, rp, lay, L, Nb)
    deltaPt = Calculations_Kettle_DeltaPtubeside.Kettle_tubeside_DeltaP(mt, rot, mit, thk, Ds, dte, Npt, rp, lay, L)
    Cop_s = Nop*(pc/1000)*((deltaPs*ms)/(eta*ros))      # Operating cost on a yearly fot the shell side stream
    Cop_t = Nop*(pc/1000)*((deltaPt*mt)/(eta*rot))      # Operating cost on a yearly fot the tube side stream
    TAC = r*Cap + Cop_s + Cop_t
    return TAC

#endregion