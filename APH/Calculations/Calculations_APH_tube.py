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
import numpy as np
#endregion

#region Calculations

def APH_Di(Do, td):
    # Tube inside diameter
    Di = Do - 2 * td
    return Di

def APH_Df(Do, lf):
    # tube fin diameter
    Df = Do + 2*lf
    return Df

def APH_Nt(Nc, Nr):
    # total number of tubes
    Nt = Nc * Nr
    return Nt

def APH_dch(Do, rph):
    # horizontal distance between finned tube centers
    dch = Do * rph
    return dch

def APH_dcv(Do, rpv):
    # vertical distance between finned tube centers 
    dcv = Do * rpv
    return dcv

def APH_Dhyd(Do, rph):
    # hydraulic diameter
    K_hyd = 3.46 # triangular pitch

    Dhyd = K_hyd * np.power(rph*Do, 2)/(np.pi * Do) - Do
    return Dhyd

def APH_td(Do):
    # tube thickness
    if Do == 0.0889 :
        td = 0.0056
    elif Do == 0.1016 :
        td = 0.0058
    elif Do == 0.0014 :
        td = 0.0061
    elif Do == 0.1413 :
        td = 0.0066
    elif Do == 0.1683 :
        td = 0.0071
    else:
        raise ValueError("Unknown tube Diameter")
    return td


#endregion
