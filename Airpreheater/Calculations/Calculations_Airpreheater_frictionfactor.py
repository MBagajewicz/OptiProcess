#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          04-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion


#region Import Library
from Airpreheater.Calculations import Calculations_Airpreheater_Reynolds
import numpy as np
#endregion

#region Calculations

def Airpreheater_frictionfactor(Ntp, Lw, Np, Sa, bp, phi, ros, mis, ms):
    #Friction factor
    Nc = Ntp - 1
    Red = Calculations_Airpreheater_Reynolds.Airpreheater_Reynolds(Ntp, Lw, Np, bp, phi, ros, mis, ms)
    par_K = np.zeros(Red.shape)
    par_Z = np.zeros(Red.shape)

    # ÂNGULO = 30
    CONDA = Sa == 30
    par_K[CONDA] = 200
    par_Z[CONDA] = 1

    CONDB = Red > 10
    CONDC = Red <= 100
    CONDf1 = np.logical_and(CONDA, CONDB, CONDC)
    par_K[CONDf1] = 77.6
    par_Z[CONDf1] = 0.589

    CONDD = Red > 100
    CONDf2 = np.logical_and(CONDA, CONDD)
    par_K[CONDf2] = 11.96
    par_Z[CONDf2] = 0.183

    # ÂNGULO = 45
    CONDA = Sa == 45
    par_K[CONDA] = 188
    par_Z[CONDA] =  1

    CONDB = Red > 15
    CONDC = Red <= 300
    CONDf1 = np.logical_and(CONDA, CONDB,CONDC)
    par_K[CONDf1] = 73.16
    par_Z[CONDf1] = 0.652

    CONDD = Red > 300
    CONDf2 = np.logical_and(CONDA, CONDD)
    par_K[CONDf2] = 5.764
    par_Z[CONDf2] = 0.206

    # ÂNGULO = 50
    CONDA = Sa == 50
    par_K[CONDA] = 136
    par_Z[CONDA] =  1

    CONDB = Red > 20
    CONDC = Red <= 300
    CONDf1 = np.logical_and(CONDA, CONDB,CONDC)
    par_K[CONDf1] = 45
    par_Z[CONDf1] = 0.631

    CONDD = Red > 300
    CONDf2 = np.logical_and(CONDA, CONDD)
    par_K[CONDf2] = 3.088
    par_Z[CONDf2] = 0.161

    # ÂNGULO = 60
    CONDA = Sa == 60
    par_K[CONDA] = 96
    par_Z[CONDA] = 1

    CONDB = Red > 40
    CONDC = Red <= 400
    CONDf1 = np.logical_and(CONDA, CONDB,CONDC)
    par_K[CONDf1] = 12.96
    par_Z[CONDf1] = 0.457

    CONDD = Red > 400
    CONDf2 = np.logical_and(CONDA, CONDD)
    par_K[CONDf2] = 3.04
    par_Z[CONDf2] = 0.215

    # ÂNGULO = 65
    CONDA = Sa == 65
    par_K[CONDA] = 96
    par_Z[CONDA] = 1

    CONDB = Red > 50
    CONDC = Red <= 500
    CONDf1 = np.logical_and(CONDA, CONDB,CONDC)
    par_K[CONDf1] = 11.2
    par_Z[CONDf1] = 0.451
    CONDD = Red > 500
    CONDf2 = np.logical_and(CONDA, CONDD)
    par_K[CONDf2] = 2.556
    par_Z[CONDf2] = 0.213
    fat = par_K*(Red**(-par_Z))
    return fat

#endregion
