#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
##################################################################################################################
#endregion


#region Import Library

#endregion

#region Calculations
def SPHE_overall_coefficient(h_I, h_II, thk, Rfh, Rfc, kplate):
    # Overall heat transfer coefficient
    U = 1 / (1 / h_I + Rfh + (thk / kplate) + 1 / h_II + Rfc)
    
    return U

