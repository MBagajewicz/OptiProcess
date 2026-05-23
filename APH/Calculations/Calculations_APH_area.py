#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-Sep-2025     Sung Young Kim            original
##################################################################################################################
#endregion

#region Import Library
from APH.Calculations import Calculations_APH_boxsize, Calculations_APH_tube
import numpy as np
#endregion


#region Calculations

def APH_Ar(Nr, Do, rpv, lf, rph, L):
    #open flow area
    H = Calculations_APH_boxsize.APH_Height(Nr, Do, rpv, lf)
    FAR = Calculations_APH_boxsize.APH_FAR(rph)
    ##lcs = Calculations_APH_boxsize.APH_lcs(L, Ncross)
    #Ar = H * FAR * lcs

    Ar = H * FAR * L
    return Ar

def APH_A1(Do, td):
    # single tube flow area
    Di = Calculations_APH_tube.APH_Di(Do, td)
    A1 = (np.pi/4)*np.power(Di, 2) 
    return A1

def APH_area(Do, lf, Nc, Nr, L, Nf, tf):
    # total heat transfer area per unit
    Nt = Calculations_APH_tube.APH_Nt(Nc, Nr)
    Df = Calculations_APH_tube.APH_Df(Do, lf)
    area = Nt*(np.pi * Do * L*(1-Nf*tf) + Nf*L*(0.5*np.pi*(np.power(Df,2)-np.power(Do,2))+np.pi*Df*tf))

    return area

def APH_area_tot(Do, lf, Nc, Nr, L, Nf, tf, Ncross):
    # total heat transfer area
    area = APH_area(Do, lf, Nc, Nr, L, Nf, tf)
    
    area_tot = area * Ncross
    return area_tot

#endregion
