#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original

##################################################################################################################
#endregion


#region Import Library
from Airpreheater.Calculations import Calculations_Airpreheater_Reynolds
import numpy as np
#endregion

#region Calculations

def Airpreheater_Nusselt(Ntp, Lw, Np, Sa, Cps, mis, ks, bp, phi, ros, ms):
    #Nusselt
    Nc = Ntp - 1
    Red = Calculations_Airpreheater_Reynolds.Airpreheater_Reynolds(Ntp, Lw, Np, bp, phi, ros, mis, ms)
    Prt = (Cps*mis)/ks

    par_C = np.zeros(Red.shape)
    par_A = np.zeros(Red.shape)

    CONDA = Sa == 30
    par_C[CONDA] = 0.718
    par_A[CONDA] = 0.349

    CONDB = Red > 10
    CONDf = np.logical_and(CONDA, CONDB)
    par_C[CONDA] = 0.348
    par_A[CONDf] = 0.663

    # ÂNGULO = 45
    CONDA = Sa == 45
    par_C[CONDA] = 0.718
    par_A[CONDA] = 0.349

    CONDB = Red > 10
    CONDC = Red <= 100
    CONDf1 = np.logical_and(CONDA, CONDB, CONDC)
    par_C[CONDf1] = 0.4
    par_A[CONDf1] = 0.598

    CONDD = Red > 100
    CONDf2 = np.logical_and(CONDA, CONDD)
    par_C[CONDf2] = 0.3
    par_A[CONDf2] = 0.663

    # ÂNGULO = 50
    CONDA = Sa == 50
    par_C[CONDA] = 0.63
    par_A[CONDA] = 0.333

    CONDB = Red > 20
    CONDC = Red <= 300
    CONDf1 = np.logical_and(CONDA, CONDB, CONDC)
    par_C[CONDf1] = 0.291
    par_A[CONDf1] = 0.591

    CONDD = Red > 300
    CONDf2 = np.logical_and(CONDA, CONDD)
    par_C[CONDf2] = 0.13
    par_A[CONDf2] = 0.732

    # ÂNGULO = 60
    CONDA = Sa == 60
    par_C[CONDA] = 0.562
    par_A[CONDA] = 0.326

    CONDB = Red > 20
    CONDC = Red <= 400
    CONDf1 = np.logical_and(CONDA, CONDB, CONDC)
    par_C[CONDf1] = 0.306
    par_A[CONDf1] = 0.529

    CONDD = Red > 400
    CONDf2 = np.logical_and(CONDA, CONDD)
    par_C[CONDf2] = 0.108
    par_A[CONDf2] = 0.703

    # ÂNGULO = 65
    CONDA = Sa == 65
    par_C[CONDA] = 0.562
    par_A[CONDA] = 0.326

    CONDB = Red > 20
    CONDC = Red <= 500
    CONDf1 = np.logical_and(CONDA, CONDB, CONDC)
    par_C[CONDf1] = 0.331
    par_A[CONDf1] = 0.503

    CONDD = Red > 500
    CONDf2 = np.logical_and(CONDA, CONDD)
    par_C[CONDf2] = 0.087
    par_A[CONDf2] = 0.718

    Nuss = par_C*Red**par_A*Prt**0.33
    return Nuss

#endregion
