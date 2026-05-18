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

def aircooler_sf(Nf, tf):
    # sf = fin spacing
    sf = (1/Nf) - tf
    return sf

#endregion