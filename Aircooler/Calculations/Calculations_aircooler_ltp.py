#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion

#region Calculations

def aircooler_calc_ltp(Dte, rp):
    # Ltp = tube pitch ratio
    Ltp = Dte*rp
    return Ltp

#endregion