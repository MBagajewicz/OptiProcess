###################################################################################################################
#region Titles and Header
# Nature: Kettle model equations
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          19-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Kettle shell-side model  
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################

##################################################################################################################
#region Import Library
import numpy as np
from math import sqrt, pi
#endregion
##################################################################################################################

##################################################################################################################
#region Kettle from Sales et al 2021=

# Internal diameter
def fun_dti(dte,thk):
    dti = dte - 2*thk
    return dti

# Layout constant Klay (Layout 1 = Square e 2 = Triangle )
def fun_Klay(lay):
    Klay = np.ones(lay.shape)
    Klay[lay == 2] = 0.866
    return Klay

# Number of passes per tube constant KNpt
def fun_KNpt(Npt):
    KNpt = np.sqrt(0.9) 
    return KNpt

# Bundle diameter 
def fun_Db(Ds,Npt):
    KNpt = fun_KNpt(Npt)
    Db = Ds*KNpt
    return Db

# Tube pitch
def fun_ltp(rp,dte):
    ltp = rp*dte
    return ltp

# Total number of tubes
def fun_Ntt(Ds, dte, Npt, rp, lay):
    Klay = fun_Klay(lay)
    Db = fun_Db(Ds,Npt)
    ltp = fun_ltp(rp, dte)
    Ntt = np.round((pi*Db**2)/(4*ltp**2*Klay))
    
    return Ntt

#endregion