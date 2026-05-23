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
    KNpt = np.sqrt(0.9)*np.ones(Npt.shape)
    KNpt[Npt == 1] = np.sqrt(0.93)
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
#########################################################################################################

#folga inferior entre feixe de tubos e e casco
def fun_folga(Ds,Npt):
    Db =fun_Db(Ds,Npt)
    folga = (Ds-Db)/2
    

    return folga

def fun_W(Ds,Npt):
    Db = fun_Db(Ds,Npt)
    folga = fun_folga(Ds,Npt)
    W = Db + folga
    
    return W


# largura do vertedouro(W)
def fun_largura_W(Ds,Ds2,Npt):
    
    W = fun_W(Ds,Npt)
    B = 2*np.sqrt(((Ds2/2)**2)-(W-(Ds2/2))**2)
    
    return B

 #liquid flow
def fun_Ql(task,m_s,rol,Fv,Q2,Hvap_s):
    if task ==1:
        Ql= m_s/(rol*Fv) 
    else:
        Ql= Q2/(Hvap_s*rol*Fv) 
    



    return Ql

#Carga vapor

def fun_VL(rov,rol,sig):
    VL = 16*2290 * rov * np.sqrt(sig / (rol - rov))
     
    return VL
#Altura lámina dágua
def fun_h(Ds, Ds2,Npt ,m_s,rol,Fv, task, Q2, Hvap_s):

    B= fun_largura_W(Ds,Ds2,Npt)
    Q= fun_Ql(task,m_s,rol,Fv,Q2,Hvap_s)
    h = (Q/(1.838*B))**(2/3)
     
    return h

#Altura líquido
def fun_H(Ds, Ds2,Npt ,m_s,rol,Fv, task, Q2, Hvap_s):
    h= fun_h(Ds, Ds2,Npt ,m_s,rol,Fv, task, Q2, Hvap_s)
    W =fun_W(Ds,Npt)
    H = h + W
    
    return H

#área transversal
def fun_SA(Ds, Ds2,Npt,m_s,rol,Fv, task, Q2, Hvap_s):
    
    H = fun_H(Ds, Ds2,Npt ,m_s,rol,Fv, task, Q2, Hvap_s)
    SA = (Ds2**2 / 4) * np.arccos((2*H / Ds2) - 1)  - (H - Ds2/2) * np.sqrt(H * (Ds2 - H))
    
    
   
    return SA

def fun_Ls(Ds, Ds2,Npt,m_s,rol,Fv,f,tr, task, Q2, Hvap_s):
    SA = fun_SA(Ds, Ds2,Npt,m_s,rol,Fv, task, Q2, Hvap_s)
    if task ==1:
        m_l = m_s*(1-f)
        q_l = m_l/rol
        Ls = q_l *tr/((np.pi*((Ds2/2)**2))-SA)
    else:
        m_l = Q2*(1-f)/(Hvap_s)
        q_l = m_l/rol
        Ls = q_l *tr/((np.pi*((Ds2/2)**2))-SA)
    
    return Ls
         
#endregion