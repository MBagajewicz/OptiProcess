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
from HTSR.Calculations import (
    Calculations_HTSR_Area,
    Calculations_HTSR_Geometry,Calculations_HTSR_Flow
)
from math import pi
import numpy as np
#endregion
##################################################################################################################

##################################################################################################################
#region Kettle from Sales et al 2021=

def Kettle_Nusselt_tubeside(rol,rov,fluid_type, Cpt, mil,miv, kl_t, thk, dte,Ds,Npt, rp, lay, m_t):
    # Tube-side Nusselt number
    Ret = Calculations_HTSR_Flow.fun_Ret(Ds, dte,Npt, rp, lay, m_t, rol,rov,fluid_type, mil,miv, thk)
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
    A = Calculations_HTSR_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    q = fun_q(Q, A)
    Fc = fun_Fc(q,BR)
    Pc_kPa = Pc/1000    # Converting Pc from Pa to kPa
    hnb1 = 0.00417*(Pc_kPa**0.69)*(q**0.7)*Fp*Fc
    return hnb1

# The correction factor for the contribution of convective boiling
def fun_Fb(Ds, dte, Npt, rp, lay):
    Db = Calculations_HTSR_Geometry.fun_Db(Ds,Npt)
    Klay = Calculations_HTSR_Geometry.fun_Klay(lay)
    Fb = 1 + 0.1*(0.785*Db/(Klay*(rp**2)*dte) - 1)**0.75
    return Fb


def fun_Flm(Fv,mil_s,miv_s,rov_s,rol_s):
    Xtt = ((1-Fv)/Fv)**((0.9))+((mil_s/miv_s)**(0.1)) + (rov_s/rol_s)**0.5
    if Xtt < 10:
        Flm = 2.35*((Xtt**(-1))+0.213)**0.736
    else:
        Flm = 1
    

    return Flm

def fun_Re_shell(Ds,dte,Npt,rp,L,msh,Fv,rol_s,mil_s):
    Db = Calculations_HTSR_Geometry.fun_Db(Ds,Npt)
    pt = dte*rp
    Sm = L*((Ds-Db)+((Db-dte)*(pt - dte))/pt)
    Vsl = (msh*(1-Fv))/(rol_s*Sm)
    Re = (rol_s*Vsl*dte)/mil_s

    return Re

def fun_Cs(lay):
    Cs = np.where(lay == 1, 0.158, 0.196)
    
    return Cs

def fun_hsc(Ds,dte,Npt,rp,lay,L,Cpl_s,mil_s,kl_s,msh,Fv,rol_s):
    Re = fun_Re_shell(Ds,dte,Npt,rp,L,msh,Fv,rol_s,mil_s)
    Pr = Cpl_s*mil_s/kl_s
    Cs = fun_Cs(lay)
    hsc = Cs*(Re**(0.6))*(Pr**(0.33)) *(kl_s/dte)
    
    
    

    
    

    return hsc


def fun_Sch(Ds,dte,Npt,rp,L,msh,Fv,rol_s,mil_s,miv_s,rov_s):

    Re = fun_Re_shell(Ds,dte,Npt,rp,L,msh,Fv,rol_s,mil_s)
    Flm = fun_Flm(Fv,mil_s,miv_s,rov_s,rol_s)

    Sch = (1+(2.53*10**(-6))*(Re*Flm**1.25)**1.17)**(-1)
   

    return Sch
    

# Shell side convective heat transfer coefficient
def fun_hs(Ds, dte, Npt, rp, lay, L, Q, BR, Pc, Fp, hnc,msh,Fv,rol_s,Cpl_s,mil_s,kl_s,miv_s,rov_s):
    hnb1 = fun_hnb1(Ds, dte, Npt, rp, lay, L, Q, BR, Pc, Fp)
    Fb = fun_Fb(Ds, dte, Npt, rp, lay)
    hnb = hnb1*Fb + hnc
    hsc = fun_hsc(Ds,dte,Npt,rp,lay,L,Cpl_s,mil_s,kl_s,msh,Fv,rol_s)
    Flm =fun_Flm(Fv,mil_s,miv_s,rov_s,rol_s)
    Sch = fun_Sch(Ds,dte,Npt,rp,L,msh,Fv,rol_s,mil_s,miv_s,rov_s)
    hs = Flm*hsc + Sch*hnb
    print("hnb=",hnb)
    
    return hs

# Tube side convective heat transfer coefficient
def fun_ht(Ds, dte, Npt, rp, lay, L, rol, rov, g, k_t, m_t, mil, miv, fluid_type,thk,kl_t,Cpt):
    Ntt=Calculations_HTSR_Geometry.fun_Ntt(Ds, dte, Npt, rp, lay)
    if fluid_type == 1:
    
        Nut = Kettle_Nusselt_tubeside( rol,rov,fluid_type, Cpt, mil,miv, kl_t, thk,
                                        dte,Ds,Npt, rp, lay, m_t)
        dti = dte - 2 * thk
        ht = Nut * kl_t / dti
    
    elif fluid_type == 2:

     ht = 0.767*((rol*(rol - rov)*g*k_t**3*L/(m_t*mil/Ntt))**(1/3))

    else:
        print("See fluid type in Examples Kettle 3")


    return ht

# Heat flux
def fun_q(Q,A):
    q = Q/A
     
    return q

# Maximum thermal flux
def fun_qb_max(Ds, dte, Npt, rp, lay, L, q1_max):
    A = Calculations_HTSR_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    Db = Calculations_HTSR_Geometry.fun_Db(Ds,Npt)
    Psi_b = pi*Db*L/A 
    Phi_b = 3.1*Psi_b 
    qb_max = q1_max*Phi_b 
    return qb_max

# Overall heat transfer coefficient
def fun_U(Ds, dte, Npt, rp, lay, L, thk, rol, rov, g, k_t, m_t,mil, miv, Q, BR, Pc, Fp, hnc, Rft, Rfs, ktube, fluid_type, kl_t, Cpt,msh,Fv,rol_s,Cpl_s,mil_s,kl_s,miv_s,rov_s):
    dti = Calculations_HTSR_Geometry.fun_dti(dte,thk)
    ht = fun_ht(Ds, dte, Npt, rp, lay, L, rol, rov, g, k_t, m_t, mil, miv, fluid_type,thk,kl_t,Cpt)
    hs = fun_hs(Ds, dte, Npt, rp, lay, L, Q, BR, Pc, Fp, hnc,msh,Fv,rol_s,Cpl_s,mil_s,kl_s,miv_s,rov_s)
    U = 1 / (1/ht*(dte/dti) + Rft*(dte/dti) + dte*np.log(dte/dti)/(2*ktube) + Rfs + 1/hs)
    print('ht =',ht)
    print('hs =',hs)
    print('U =',U)
    return U

# Required area
def fun_A_req(Ds, dte, Npt, rp, lay, L, thk, rol, rov, g,
               k_t, m_t, mil,miv, Q, BR, Pc, 
               Fp, hnc, Rft, Rfs, ktube, dTLM, fluid_type, 
                kl_t, Cpt,msh ,Fv,rol_s,Cpl_s,mil_s,kl_s,miv_s,rov_s ):
    U = fun_U(Ds, dte, Npt, rp, lay, L, thk, rol, rov, g, k_t, m_t,mil, miv, Q,
               BR, Pc, Fp, hnc, Rft, Rfs, ktube, fluid_type, kl_t, Cpt,
               msh,Fv,rol_s,Cpl_s,mil_s,kl_s,miv_s,rov_s)
    A_req = Q/(U*dTLM)
    return A_req


#endregion