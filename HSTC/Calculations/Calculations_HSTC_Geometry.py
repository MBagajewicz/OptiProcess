###################################################################################################################
#region Titles and Header
# Nature: Horizontal Shell and Tube Condenser model equations
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          20-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Kettle Area model  
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################

##################################################################################################################
#region Import Library
from math import sqrt, pi
import numpy as np

#endregion
##################################################################################################################

##################################################################################################################
#region Calculations

# Internal diameter
def fun_dti(dte,thk):
    dti = dte - 2*thk
    return dti

# Layout constant Klay (Layout 1 = Square e 2 = Triangle )
def fun_Klay(lay):
    Klay = np.ones(lay.shape)
    if isinstance(lay,float) or isinstance(lay,int):
        if lay == 2: Klay = 0.866
    else:
        Klay[lay == 2] = 0.866
    return Klay

# Number of passes per tube constant KNpt
def fun_KNpt(Npt):
    KNPt = sqrt(0.9)*np.ones(Npt.shape)
    if isinstance(Npt,float) or isinstance(Npt,int):
        if Npt==1: KNPt = sqrt(0.93)
    else:
        KNPt[Npt == 1] = sqrt(0.93)
    return KNPt

def fun_KDeq(lay):
    K_Deq = 4*np.ones(lay.shape)
    if isinstance(lay,float) or isinstance(lay,int):
        if lay==2: K_Deq = 3.46
    else:
        K_Deq[lay == 2] = 3.46
    return K_Deq

def fun_Deq(KDeq,ltp,dte):
    Deq = (KDeq*ltp**2)/(pi*dte) - dte
    return Deq

# Bundle diameter 
def fun_Db(Ds,Npt):
    KNpt = fun_KNpt(Npt)
    Db = Ds*KNpt
    return Db

# Tube pitch
def fun_ltp(rp,dte):
    ltp = rp*dte
    return ltp

def fun_Ftc(Ds,Npt):
    ftc = np.ones_like(Ds, dtype=float)
    ftc[(Ds > 0.337) & (Npt == 1)] = 1.08
    ftc[(Ds > 0.337) & (Npt == 2)] = 1.11
    ftc[(Ds > 0.337) & ((Npt == 4) | (Npt == 6)) & (Ds <= 0.635)] = 1.45
    ftc[(Ds > 0.635) & ((Npt == 4) | (Npt == 6))] = 1.18  
    return ftc  

def fun_Ntt(Ds, dte, Npt, rp, lay, Fsc):
    ltp = fun_ltp(rp,dte)
    Klay = fun_Klay(lay)
    Ftc = fun_Ftc(Ds, Npt)
    Ntt = np.round((pi*Ds**2)/(4*ltp**2*Klay*Ftc*Fsc))
    return Ntt

def fun_A(Ds, dte, Npt, rp, lay, L, Fsc):
    Ntt = fun_Ntt(Ds, dte, Npt, rp, lay, Fsc)
    A = Ntt*pi*dte*L
    return A

##################################################################################################################
#endregion