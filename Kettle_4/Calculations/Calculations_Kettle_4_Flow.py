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
from Kettle_4.Calculations import (
    Calculations_Kettle_4_Flow,
    Calculations_Kettle_4_Heat_Transfer,
    Calculations_Kettle_4_Area,
    Calculations_Kettle_4_Geometry
)
from math import (pi,ceil)
import numpy as np
#endregion
##################################################################################################################

##################################################################################################################
#region Kettle from Sales et al 2021=

# Tube side velocity
def fun_vt(Ds, dte, Npt, rp, lay, m_t,rol,rov,fluid_type, thk):
    dti = Calculations_Kettle_4_Geometry.fun_dti(dte,thk)
    Ntt = Calculations_Kettle_4_Geometry.fun_Ntt(Ds,dte,Npt,rp,lay)
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
    dti = Calculations_Kettle_4_Geometry.fun_dti(dte,thk)
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
    dti = Calculations_Kettle_4_Geometry.fun_dti(dte,thk)

    if fluid_type ==1:
        dPt = (rol*ft*Npt*L*vt**2)/(2*dti) + rol*K*Npt*vt**2/2

    # Two phase correction for pressure drop on the tube side  
    elif fluid_type == 2: 
        dPt = 0.5*((rov*ft*Npt*L*vt**2)/(2*dti) + rov*K*Npt*vt**2/2)
        
    print('deltaP = ', dPt)
    return dPt
 
 ####################################################################################### Definido DFS E DRS


def D_FS(Ds,Npt,L,D_FF):
    Db = Calculations_Kettle_4_Geometry.fun_Db(Ds,Npt)
    N = np.ceil(L/(5*Db))
    DFS = np.sqrt(D_FF/N)
    return DFS


def D_RS(Ds,Npt,L,D_RF):
    Db = Calculations_Kettle_4_Geometry.fun_Db(Ds,Npt)
    N = np.ceil(L/(5*Db))
    DFS = np.sqrt(D_RF/N)
    return DFS
##################################################################### Perda de carga FF


def V_FF( D_FF,msh, rol_s):
    V_FF =4 * msh / (np.pi * rol_s * D_FF**2)
    return V_FF

def deltaP_FF( D_FF,msh, mil_s,rol_s, L_FF):
    SG = rol_s/1000
    Re_FF =4 * msh / (np.pi * mil_s * D_FF)
    f_FF = 0.3673 * Re_FF**(-0.2314)
    G_FF= 4 * msh / (np.pi * D_FF**2)
    deltaP_FF= (f_FF * L_FF * G_FF**2) / (2000 * D_FF * SG)

    return deltaP_FF

##################################################################### Perda de carga FS
def V_FS( Ds,Npt,L,D_FF,msh, rol_s):
    DFS =D_FS(Ds,Npt,L,D_FF)
    V_FS =4 * msh / (np.pi * rol_s * DFS**2)
    return V_FS

def deltaP_FS( Ds,Npt,L,D_FF,msh, mil_s,rol_s, L_FS):
    DFS =D_FS(Ds,Npt,L,D_FF)
    SG = rol_s/1000
    Re_FS =4 * msh / (np.pi * mil_s * DFS)
    f_FS = 0.3673 * Re_FS**(-0.2314)
    G_FS= 4 * msh / (np.pi * DFS**2)
    deltaP_FS= (f_FS * L_FS * G_FS**2) / (2000 * DFS * SG)

    return deltaP_FS




################################################################# Fatores de correção para duas fases




# 12. Correlação de Lockhart-Martinelli modificada
def phi_LO(rol_s, rov_s, miv_s, mil_s, f_v):
    Y_MSH =(rol_s / rov_s)**0.5 * (miv_s/ mil_s)**0.1157
    phi_LO= Y_MSH**2 * f_v**3 + (1 + 2 * f_v * (Y_MSH**2 - 1)) * (1 - f_v)**(1/3)
    return phi_LO

def ro_tp1(f_v, rov_s, rol_s):
    fv1=f_v/2
    ro_tp1 = 1 / (fv1 / rov_s + (1 - fv1) / rol_s)
    return ro_tp1

def ro_tp2(f_v, rov_s, rol_s):
    fv2=f_v
    ro_tp2 = 1 / (fv2 / rov_s + (1 - fv2) / rol_s)
    return ro_tp2

#################################################################### perda de carga no reboiler

def PT_c(dte, rp, lay):
    lay = np.asarray(lay)
    PTC = np.where(
        lay == 1, dte * rp,
        np.where(lay == 2, dte * rp * 0.866, 0)
    )
    return PTC

import numpy as np

def fun_Re_shell(Ds,dte,Npt,rp,L,msh,Fv,rol_s,mil_s):
    Db = Calculations_Kettle_4_Geometry.fun_Db(Ds,Npt)
    pt = dte*rp
    Sm = L*((Ds-Db)+((Db-dte)*(pt - dte))/pt)
    Vsl = (msh*(1-Fv))/(rol_s*Sm)
    Re = (rol_s*Vsl*dte)/mil_s

    return Re
def F_reb(Ds, dte, Npt, rp, lay, L, msh, f_v, rol_s, mil_s):
    Re = fun_Re_shell(Ds, dte, Npt, rp, L, msh, f_v, rol_s, mil_s)

    # inicializa arrays vazios com o mesmo formato de Re
    b1 = np.zeros_like(Re, dtype=float)
    b2 = np.zeros_like(Re, dtype=float)
    b3 = np.zeros_like(Re, dtype=float)
    b4 = np.zeros_like(Re, dtype=float)

    # Máscaras de condição
    mask_lay1_high = (lay == 1) & (Re >= 10000)
    mask_lay1_low  = (lay == 1) & (Re < 10000)
    mask_lay2_high = (lay == 2) & (Re >= 10000)
    mask_lay2_low  = (lay == 2) & (Re < 10000)

    # Atribuições vetorizadas
    b1[mask_lay1_high] = 0.391
    b2[mask_lay1_high] = -0.148
    b3[mask_lay1_high] = 6.3
    b4[mask_lay1_high] = 0.378

    b1[mask_lay1_low] = 0.0815
    b2[mask_lay1_low] = -0.22
    b3[mask_lay1_low] = 6.3
    b4[mask_lay1_low] = 0.378

    b1[mask_lay2_high] = 0.371
    b2[mask_lay2_high] = -0.123
    b3[mask_lay2_high] = 7
    b4[mask_lay2_high] = 0.5

    b1[mask_lay2_low] = 0.486
    b2[mask_lay2_low] = -0.152
    b3[mask_lay2_low] = 7
    b4[mask_lay2_low] = 0.5

    # Cálculo final
    b0 = b3 / (1 + 0.14 * Re**b4)
    f_reb = (b1 * (1.33 / rp)**b0) * Re**b2

    return f_reb

def deltaP_Reb(Ds,dte,Npt,rp,lay,L, msh, rol_s, rov_s, miv_s, mil_s, f_v):
    phi = phi_LO(rol_s, rov_s, miv_s, mil_s, f_v)
    Db = Calculations_Kettle_4_Geometry.fun_Db(Ds,Npt)
    pt = dte*rp
    Sm = L*((Ds-Db)+((Db-dte)*(pt - dte))/pt)
    Ptc =PT_c(dte,rp,lay)
    N_c = Db/Ptc
    f_reb = F_reb(Ds,dte,Npt,rp,lay,L,msh,f_v,rol_s,mil_s)
    
    deltaP_Reb = phi * (2 * f_reb * N_c * (msh/ Sm)**2 / rol_s)
    return deltaP_Reb

def deltaP_mo(Ds,dte,Npt,rp,L,msh,f_v, rol_s, rov_s, miv_s, mil_s):
   n =0.2
   rotp1= ro_tp1(f_v, rov_s, rol_s)
   rotp2 = ro_tp2(f_v, rov_s, rol_s)
   Db = Calculations_Kettle_4_Geometry.fun_Db(Ds,Npt)
   pt = dte*rp
   Sm = L*((Ds-Db)+((Db-dte)*(pt - dte))/pt)
   Xtt_p1 =(((1-0.01)/0.01)**((2-n)/n))*((mil_s/miv_s)**(n/2))*((rov_s/rol_s)**0.5)

   if Xtt_p1 <= 1:
       SR_p1 = (rol_s/rov_s)**0.25
   else:
       SR_p1 = (rol_s/rotp1)**0.5 
    
   ev_p1 = 0.01/(0.01+SR_p1*(1-0.01)*(rov_s/rol_s))

   P_p1=((msh/Sm)**2)*(((1-0.01)**2)/(rol_s*(1-ev_p1))+((0.01**2)/(rov_s*ev_p1)))

   Xtt_p2 =(((1-f_v)/f_v)**((2-n)/n))*((mil_s/miv_s)**(n/2))*((rov_s/rol_s)**0.5)

   if Xtt_p2 <= 1:
       SR_p2 = (rol_s/rov_s)**0.25
   else:
       SR_p2 = (rol_s/rotp2)**0.5 
    
   ev_p2 = f_v/(f_v+SR_p2*(1-f_v)*(rov_s/rol_s))

   P_p2=((msh/Sm)**2)*(((1-f_v)**2)/(rol_s*(1-ev_p2))+((f_v**2)/(rov_s*ev_p2)))
    

   deltaP_mo = P_p2 - P_p1
   return deltaP_mo


##################################################################### Perda de carga RF
def V_RF( D_RF,msh, rov_s,):
    
    V_RF =4 * msh / (np.pi * rov_s * D_RF**2)
    return V_RF

def deltaP_RF( D_RF,msh, rov_s, mil_s, L_RF):

    
    SG2 =rov_s/1000
    

    Re_RF =4 * msh / (np.pi * mil_s * D_RF)
    f_RF = 0.3673 * Re_RF**(-0.2314)
    G_RF= 4 * msh / (np.pi * D_RF**2)
    deltaP_RF= (f_RF * L_RF * G_RF**2) / (2000 * D_RF * SG2)

    return deltaP_RF


##################################################################### Perda de carga RS
def V_RS( Ds,Npt,L,D_FF,msh, rov_s):
    DRS =D_RS(Ds,Npt,L,D_FF)
    
    V_RS =4 * msh / (np.pi * rov_s * DRS**2)
    return V_RS

def deltaP_RS(Ds,Npt,L,D_FF,msh,rov_s, mil_s, L_RS ):
    DRS =D_RS(Ds,Npt,L,D_FF)
    
    
    SG2 =rov_s/1000
    Re_RS =4 * msh / (np.pi * mil_s * DRS)
    f_RS = 0.3673 * Re_RS**(-0.2314)
    G_RS= 4 * msh / (np.pi * DRS**2)
    deltaP_RS= (f_RS * L_RS * G_RS**2) / (2000 * DRS * SG2)

    return deltaP_RS



 ######################################################################Balanço de pressões




def deltaH_L(Ds,dte,Npt,rp,lay,L, D_FF,D_RF,msh, mil_s, L_FF,f_v,rol_s, rov_s, miv_s,L_FS,L_RS,L_RF,g):
    a = deltaP_FF( D_FF,msh, mil_s,rol_s, L_FF)
    b = deltaP_FS( Ds,Npt,L,D_FF,msh, mil_s,rol_s, L_FS)
    c =deltaP_Reb(Ds,dte,Npt,rp,lay,L,msh, rol_s, rov_s, miv_s, mil_s, f_v)
    d = deltaP_RF( D_RF,msh, rov_s, mil_s, L_RF)
    e = deltaP_RS(Ds,Npt,L,D_FF,msh,rov_s, mil_s, L_RS )
    f = deltaP_mo(Ds,dte,Npt,rp,L,msh,f_v, rol_s, rov_s, miv_s, mil_s)
    X = a + b + c +d + e+ f
    rho_tp1 =ro_tp1(f_v, rov_s, rol_s)
    
    deltaH_L =(X +Ds*g*(rho_tp1-rov_s))/(g*(rol_s-rov_s))
    print('hl = ', deltaH_L)
    return deltaH_L
#endregion