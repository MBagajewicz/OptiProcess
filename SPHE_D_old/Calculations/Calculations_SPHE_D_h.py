#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
#################################################################################################################
#endregion


#region Import Library
from math import pi
import numpy as np
#endregion
from SPHE_D.Calculations.Calculations_SPHE_D_Mass_Flux import SPHE_Mass_Flux
from SPHE_D.Calculations.Calculations_SPHE_D_Reynolds import SPHE_Reynolds
from SPHE_D.Calculations.Calculations_SPHE_D_Hydraulic_diameter import SPHE_Hydraulic_diameter

#region Calculations

def SPHE_h(Nu,k,Dh):
    
    h = Nu*k/Dh
    return h

#endregion