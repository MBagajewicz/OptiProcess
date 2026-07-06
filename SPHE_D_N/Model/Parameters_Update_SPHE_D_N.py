##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         05-Jul-2026      ChatGPT                   Turn-based wrapper for SPHE_D parameters
##################################################################################################################
# INPUT: Parameters update functions for SPHE_D_N
##################################################################################################################

# The turn-based SPHE_D_N model uses the same model parameters as SPHE_D.
# Parameter update functions are re-exported to keep the dynamic import
# convention: SPHE_D_N.Model.Parameters_Update_SPHE_D_N.

from SPHE_D.Model.Parameters_Update_SPHE_D import *  # noqa: F401,F403
