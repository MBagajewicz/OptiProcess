#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion

#region Import Library
from Aircooler.Calculations import Calculations_aircooler_prop_kc, Calculations_aircooler_Nu_coldstream
#endregion

#region Calculations

def aircooler_coefficient_hc(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf, mh, Cph, Thi, Tho, Tco, Tci):
   # Heat-transfer coefficient of cold stream
   kc = Calculations_aircooler_prop_kc.aircooler_calc_prop_air_kc(Tco, Tci)
   Nuc = Calculations_aircooler_Nu_coldstream.aircooler_Nusselt_coldstream(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf,
                                                                           mh, Cph, Thi, Tho, Tco, Tci)
   hc = (Nuc*kc)/Dte
   return hc

#endregion