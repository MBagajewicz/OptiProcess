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
from math import pi
import numpy as np


#endregion

#region Calculations

def SPHE_Mass_Flux(m, d, H):
    G = (m ) / ((d ) * (H ))  # The mass flux 

    return G
