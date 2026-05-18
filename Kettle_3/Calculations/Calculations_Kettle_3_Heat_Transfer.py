###################################################################################################################
#region Titles and Header
# Nature: Kettle model equations
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          19-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Kettle model  
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################

##################################################################################################################
#region Import Library
from Kettle_3.Calculations import (
    Calculations_Kettle_3_Area,
    Calculations_Kettle_3_Geometry,Calculations_Kettle_3_Flow
)
from math import pi
import numpy as np
#endregion
##################################################################################################################

##################################################################################################################
#region Kettle from Sales et al 2021=

def Kettle_Nusselt_tubeside(rol,rov,fluid_type, Cpt, mil,miv, kl_t, thk, dte,Ds,Npt, rp, lay, m_t):
    # Tube-side Nusselt number
    Ret = Calculations_Kettle_3_Flow.fun_Ret(Ds, dte,Npt, rp, lay, m_t, rol,rov,fluid_type, mil,miv, thk)
    if fluid_type==1:
        Prt = Cpt * mil / kl_t
    elif fluid_type==2:
        Prt = Cpt * miv / kl_t
        
    
    Nut = 0.023 * Ret**0.8 * Prt**(0.3)
    return Nut


# Correction factor associated to mixture effects
def fun_Fc(q, BR):
    Fc = 1/(1 + 0.023*(q**0.15)*(BR**0.75))
    return Fc

# Nucleate boiling heat transfer coefficient for an isolated tube
def fun_hnb1(Ds, dte, Npt, rp, lay, L, Q, BR, Pc, Fp):
    A = Calculations_Kettle_3_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    q = fun_q(Q, A)
    Fc = fun_Fc(q,BR)
    Pc_kPa = Pc/1000    # Converting Pc from Pa to kPa
    hnb1 = 0.00417*(Pc_kPa**0.69)*(q**0.7)*Fp*Fc
    return hnb1

# The correction factor for the contribution of convective boiling
def fun_Fb(Ds, dte, Npt, rp, lay):
    Db = Calculations_Kettle_3_Geometry.fun_Db(Ds,Npt)
    Klay = Calculations_Kettle_3_Geometry.fun_Klay(lay)
    Fb = 1 + 0.1*(0.785*Db/(Klay*(rp**2)*dte) - 1)**0.75
    return Fb

# Shell side convective heat transfer coefficient
def fun_hs(Ds, dte, Npt, rp, lay, L, Q, BR, Pc, Fp, hnc):
    hnb1 = fun_hnb1(Ds, dte, Npt, rp, lay, L, Q, BR, Pc, Fp)
    Fb = fun_Fb(Ds, dte, Npt, rp, lay)
    hs = hnb1*Fb + hnc
    print('hs = ', hs)
    return hs

# Tube side convective heat transfer coefficient
def fun_ht(L, rol, rov, g, k_t, m_t, mil, miv, fluid_type, dte,thk,kl_t,Ds,Npt, rp, lay,Cpt):
    Ntt=Calculations_Kettle_3_Geometry.fun_Ntt(Ds, dte, Npt, rp, lay)
    if fluid_type == 1:
    
        Nut = Kettle_Nusselt_tubeside( rol,rov,fluid_type, Cpt, mil,miv, kl_t, thk,
                                        dte,Ds,Npt, rp, lay, m_t)
        dti = dte - 2 * thk
        ht = Nut * kl_t / dti
    
    elif fluid_type == 2:

     ht = 0.767*((rol*(rol - rov)*g*k_t**3*L/(m_t*mil/Ntt))**(1/3))

    else:
        print("See fluid type in Examples Kettle 3")

    print('ht = ', ht)
    return ht

# Heat flux
def fun_q(Q,A):
    q = Q/A
   
    return q

# Maximum thermal flux
def fun_qb_max(Ds, dte, Npt, rp, lay, L, q1_max):
    A = Calculations_Kettle_3_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    Db = Calculations_Kettle_3_Geometry.fun_Db(Ds,Npt)
    Psi_b = pi*Db*L/A 
    Phi_b = 3.1*Psi_b 
    qb_max = q1_max*Phi_b 
    return qb_max

# Overall heat transfer coefficient
def fun_U(Ds, dte, Npt, rp, lay, L, thk, rol, rov, g, k_t, m_t,mil, miv, Q, BR, Pc, Fp, hnc, Rft, Rfs, ktube, fluid_type, kl_t, Cpt ):
    dti = Calculations_Kettle_3_Geometry.fun_dti(dte,thk)
    ht = fun_ht(L, rol, rov, g, k_t, m_t, mil, miv, fluid_type, dte,thk,kl_t,Ds,Npt, rp, lay,Cpt)
    hs = fun_hs(Ds, dte, Npt, rp, lay, L, Q, BR, Pc, Fp, hnc)
    U = 1 / (1/ht*(dte/dti) + Rft*(dte/dti) + dte*np.log(dte/dti)/(2*ktube) + Rfs + 1/hs)
    print('U =',U)
    return U

# Required area
def fun_A_req(Ds, dte, Npt, rp, lay, L, thk, rol, rov, g,
               k_t, m_t, mil,miv, Q, BR, Pc, 
               Fp, hnc, Rft, Rfs, ktube, dTLM, fluid_type, 
                kl_t, Cpt):
    U = fun_U(Ds, dte, Npt, rp, lay, L, thk, rol, rov, g, k_t, m_t,mil, miv, Q, BR, Pc, Fp, hnc, Rft, Rfs, ktube, fluid_type, kl_t, Cpt)
    A_req = Q/(U*dTLM)
    return A_req


#endregion