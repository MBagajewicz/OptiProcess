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
from Kettle_2.Calculations import (
    Calculations_Kettle_2_Area,
    Calculations_Kettle_2_Geometry
)
from math import pi
import numpy as np
#endregion
##################################################################################################################

##################################################################################################################
#region Kettle from Sales et al 2021=

# Correction factor associated to mixture effects
def fun_Fc(q, BR):
    Fc = 1/(1 + 0.023*(q**0.15)*(BR**0.75))
    return Fc

# Nucleate boiling heat transfer coefficient for an isolated tube
def fun_hnb1(Ds, dte, Npt, rp, lay, L, Q, BR, Pc, Fp):
    A = Calculations_Kettle_2_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    q = fun_q(Q, A)
    Fc = fun_Fc(q,BR)
    Pc_kPa = Pc/1000    # Converting Pc from Pa to kPa
    hnb1 = 0.00417*(Pc_kPa**0.69)*(q**0.7)*Fp*Fc
    return hnb1

# The correction factor for the contribution of convective boiling
def fun_Fb(Ds, dte, Npt, rp, lay):
    Db = Calculations_Kettle_2_Geometry.fun_Db(Ds,Npt)
    Klay = Calculations_Kettle_2_Geometry.fun_Klay(lay)
    Fb = 1 + 0.1*(0.785*Db/(Klay*(rp**2)*dte) - 1)**0.75
    return Fb

# Shell side convective heat transfer coefficient
def fun_hs(Ds, dte, Npt, rp, lay, L, Q, BR, Pc, Fp, hnc):
    hnb1 = fun_hnb1(Ds, dte, Npt, rp, lay, L, Q, BR, Pc, Fp)
    Fb = fun_Fb(Ds, dte, Npt, rp, lay)
    hs = hnb1*Fb + hnc
    return hs

# Tube side convective heat transfer coefficient
def fun_ht(L, rol_t, rov_t, g, k_t, m_t, mi_t):
    ht = 0.767*(rol_t*(rol_t - rov_t)*g*k_t**3*L/(m_t*mi_t))
    return ht

# Heat flux
def fun_q(Q,A):
    q = Q/A
    return q

# Maximum thermal flux
def fun_qb_max(Ds, dte, Npt, rp, lay, L, q1_max):
    A = Calculations_Kettle_2_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    Db = Calculations_Kettle_2_Geometry.fun_Db(Ds,Npt)
    Psi_b = pi*Db*L/A
    Phi_b = 3.1*Psi_b
    qb_max = q1_max*Phi_b
    return qb_max

# Overall heat transfer coefficient
def fun_U(Ds, dte, Npt, rp, lay, L, thk, rol_t, rov_t, g, k_t, m_t, mu_t, Q, BR, Pc, Fp, hnc, Rft, Rfs, ktube):
    dti = Calculations_Kettle_2_Geometry.fun_dti(dte,thk)
    ht = fun_ht(L, rol_t, rov_t, g, k_t, m_t, mu_t)
    hs = fun_hs(Ds, dte, Npt, rp, lay, L, Q, BR, Pc, Fp, hnc)
    U = 1 / (1/ht*(dte/dti) + Rft*(dte/dti) + dte*np.log(dte/dti)/(2*ktube) + Rfs + 1/hs)
    return U

# Required area
def fun_A_req(Ds, dte, Npt, rp, lay, L, thk, rol_t, rov_t, g, k_t, m_t, mu_t, Q, BR, Pc, Fp, hnc, Rft, Rfs, ktube, dTLM):
    U = fun_U(Ds, dte, Npt, rp, lay, L, thk, rol_t, rov_t, g, k_t, m_t, mu_t, Q, BR, Pc, Fp, hnc, Rft, Rfs, ktube)
    A_req = Q/(U*dTLM)
    return A_req


#endregion