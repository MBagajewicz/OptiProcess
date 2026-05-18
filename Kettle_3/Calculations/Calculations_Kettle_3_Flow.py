###################################################################################################################
#region Titles and Header
# Nature: Kettle model equations
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          19-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Kettle tube-side model  
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################

##################################################################################################################
#region Import Library
from Kettle_3.Calculations import Calculations_Kettle_3_Geometry
from math import pi
import numpy as np
#endregion
##################################################################################################################

##################################################################################################################
#region Kettle from Sales et al 2021=

# Tube side velocity
def fun_vt(Ds, dte, Npt, rp, lay, m_t,rol,rov,fluid_type, thk):
    dti = Calculations_Kettle_3_Geometry.fun_dti(dte,thk)
    Ntt = Calculations_Kettle_3_Geometry.fun_Ntt(Ds,dte,Npt,rp,lay)
    Ntp = Ntt/Npt
    if fluid_type == 1:
        qt = m_t/rol
    elif fluid_type == 2:
        qt = m_t/rov
    vt = (qt/Ntp)/(pi*dti**2/4)
    return vt

# Tube side Reynolds number
def fun_Ret(Ds, dte,Npt, rp, lay, m_t, rol,rov,fluid_type, mil,miv, thk):
    vt=fun_vt(Ds, dte, Npt, rp, lay, m_t,rol,rov,fluid_type, thk)
    dti = Calculations_Kettle_3_Geometry.fun_dti(dte,thk)
    if fluid_type == 1:
        Ret = (dti*vt*rol)/mil
    elif fluid_type == 2:
        Ret = (dti*vt*rol)/miv
    return Ret

# Friction factor
def fun_f(Ret):
    ft = 0.014 + 1.056/(Ret**0.42)
    return ft


# Tube side pressure drop
def fun_dPt(Ds, dte, Npt, rp, lay, L, m_t,  rol,rov,fluid_type, mil,miv, thk):
    vt = fun_vt(Ds, dte, Npt, rp, lay, m_t,rol,rov,fluid_type, thk)
    Ret = fun_Ret(Ds, dte,Npt, rp, lay, m_t, rol,rov,fluid_type, mil,miv, thk)
    ft = fun_f(Ret)
    K = 1.6
    dti = Calculations_Kettle_3_Geometry.fun_dti(dte,thk)

    if fluid_type ==1:
        dPt = (rol*ft*Npt*L*vt**2)/(2*dti) + rol*K*Npt*vt**2/2

    # Two phase correction for pressure drop on the tube side  
    elif fluid_type == 2: 
        dPt = 0.5*((rov*ft*Npt*L*vt**2)/(2*dti) + rov*K*Npt*vt**2/2)
        
    print('deltaP = ', dPt)
    return dPt
 
#endregion