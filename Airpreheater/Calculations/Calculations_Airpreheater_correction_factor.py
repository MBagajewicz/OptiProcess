#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          04-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion

# region Import Library
from math import log, sqrt
import numpy as np
#endregion


#region Calculations

def Airpreheater_correction_factor(Thi, Tho, Tci, Tco, Nph, Npc, F1_2):
    # LMTD correction factor
    F = np.ones(Nph.shape)
    CONDA = Nph == 2
    CONDB = Npc == 1
    CONDf1 = np.logical_and(CONDA, CONDB)

    CONDA = Nph == 1
    CONDB = Npc == 2
    CONDf2 = np.logical_and(CONDA, CONDB)

    try:
        F[CONDf1] = F1_2
        F[CONDf2] = F1_2

    except:
        F[CONDf1] = F1_2[CONDf1]
        F[CONDf2] = F1_2[CONDf2]

    return F

#endregion