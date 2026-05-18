#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion

##################################################################################
#region Import Library
from Aircooler.Calculations import Calculations_aircooler_prop_cpc
from Common_Equations_HEX import Calculations_HEX_heatload

#endregion
################################################################################

#region Calculations

def aircooler_mc(mh, Cph, Thi, Tho, Tco, Tci):
    Q = Calculations_HEX_heatload.HEX_heat_load(mh, Cph, Thi, Tho)
    Cpc = Calculations_aircooler_prop_cpc.aircooler_calc_prop_air_Cpc(Tco, Tci)
    mc = Q/(Cpc*(Tco-Tci))
    return mc

#endregion

