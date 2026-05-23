###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          27-Jan-2025     Alice Peccini             Original
#   0.1          28-Feb-2025     Alice Peccini             Relocating folders
##################################################################################################################
# INPUT: Define Constraints as def and return + or - values depending the > or < inequality
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def)  for each constraint defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Active_Constraints_List']
# Then add an Objective Function to be minimized before declared in:
#                            Model_Declarations['Standard_Objective_Function']['Equation_Name']
# Finally, add the Lower Bound x
# endregion
############################################################################################

##################################################################################################################
# region Import Library
from Kettle_4.Calculations import (
    Calculations_Kettle_4_Flow,
    Calculations_Kettle_4_Heat_Transfer,
    Calculations_Kettle_4_Area,
    Calculations_Kettle_4_Geometry
)

# endregion
##################################################################################################################

##################################################################################################################
# region Kettle model from Sales et al 2021

# ----------------------------------------------------------------------------------------------------------------
# Trimming Functions
# ----------------------------------------------------------------------------------------------------------------

# Lower bound on L/Ds
def LD_lb(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    fun_val = m_p['LBLD'] - L/Ds
    return fun_val

# Upper bound on L/Ds
def LD_ub(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    fun_val = L/Ds - m_p['UBLD']
    return fun_val

def Ds_ub(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):

    fun_val = Ds - Ds2
    return fun_val



# Lower bound on vt
def vt_lb(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    vt = Calculations_Kettle_4_Flow.fun_vt(Ds, dte, Npt, rp, lay, m_p['m_t'],m_p['rol_t'],m_p['rov_t'],m_p['fluid_type'],m_p['thk'])
    fun_val = m_p['vtmin'] - vt
    return fun_val

# Upper bound on vt
def vt_ub(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    vt = Calculations_Kettle_4_Flow.fun_vt(Ds, dte, Npt, rp, lay, m_p['m_t'],m_p['rol_t'],m_p['rov_t'],m_p['fluid_type'],m_p['thk'])
    fun_val = vt - m_p['vtmax']
    return fun_val

# Lower bound on Ret
def Ret_lb(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):

    Ret = Calculations_Kettle_4_Flow.fun_Ret(Ds,dte,Npt,rp,lay,m_p['m_t'],m_p['rol_t'],m_p['rov_t'],m_p['fluid_type']
                                             ,m_p['mil_t'],m_p['miv_t'],m_p['thk'])
    fun_val = m_p['Retmin'] - Ret
    return fun_val

# Maximum heat flux
def q_ub(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    A = Calculations_Kettle_4_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    q = Calculations_Kettle_4_Heat_Transfer.fun_q(m_p['Q'], A)
    qb_max = Calculations_Kettle_4_Heat_Transfer.fun_qb_max(Ds, dte, Npt, rp, lay, L, m_p['q1_max'])
    fun_val = q - 0.7*qb_max
    return fun_val

# Maximum pressure drop
def dPt_up(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    dPt = Calculations_Kettle_4_Flow.fun_dPt(Ds, dte, Npt, rp, lay, L, m_p['m_t'],m_p['rol_t'],m_p['rov_t'],m_p['fluid_type']
                                             ,m_p['mil_t'],m_p['miv_t'],m_p['thk'])
    fun_val = dPt - m_p['dPt_disp']

    return fun_val


def VL_lb(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
     VL = Calculations_Kettle_4_Geometry.fun_VL(m_p['rov_s'],m_p['rol_s'],m_p['sig'])
     SA =Calculations_Kettle_4_Geometry.fun_SA(Ds,Ds2,Npt,m_p['m_s'],m_p['rol_s'],m_p['fv'],m_p['task'],m_p['Q2'],m_p['Hvap_s'])
     fun_val =  (m_p['m_s']/(L*SA)) -VL
     return fun_val

def H_lb(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    Db = Calculations_Kettle_4_Geometry.fun_Db(Ds,Npt)
    folga = Calculations_Kettle_4_Geometry.fun_folga(Ds,Npt)
    H = Calculations_Kettle_4_Geometry.fun_H(Ds, Ds2,Npt ,m_p['m_s'],m_p['rol_s'],m_p['fv'],m_p['task'],m_p['Q2'],m_p['Hvap_s'])
    fun_val =  (Db+ folga)-  H
    return fun_val



# Excess area
def A_exc(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    Areq = Calculations_Kettle_4_Heat_Transfer.fun_A_req(Ds, dte, Npt, rp, lay, L, m_p['thk'], m_p['rol_t'], m_p['rov_t'], m_p['g'], 
                                                         m_p['kl_t'], m_p['m_t'], m_p['mil_t'],m_p['miv_t'], m_p['Q'], m_p['BR'], m_p['Pc'], 
                                                         m_p['Fp'], m_p['hnc'], m_p['Rf_t'], m_p['Rf_s'], m_p['ktube'], m_p['dTLM'],m_p['fluid_type'],
                                                           m_p['kl_t'],m_p['Cp_t'])
    A = Calculations_Kettle_4_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    fun_val = (1 + m_p['Aexc'])*Areq - A
    
    return fun_val






def Hl_ub(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    Hl = DeltaHL = Calculations_Kettle_4_Flow.deltaH_L(Ds,dte,Npt,rp,lay,L, D_FF, D_RF,m_p['m_s'], m_p['mil_s'],
                                                    m_p['L_FF'],m_p['fv'],m_p['rol_s'], m_p['rov_s'], m_p['miv_s'],
                                                    m_p['L_FS'],m_p['L_RS'],m_p['L_RF'],m_p['g'])
    fun_val = Hl - m_p['Hl_max']
    return fun_val
# ----------------------------------------------------------------------------------------------------------------
# Objective Function
# ----------------------------------------------------------------------------------------------------------------

def Area_OF(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    HE_Area = Calculations_Kettle_4_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    return HE_Area

def Cost_OF(Ds,Ds2, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    Area = Calculations_Kettle_4_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    Ls = Calculations_Kettle_4_Geometry.fun_Ls(Ds,Ds2,Npt,m_p['m_s'],m_p['rol_s'],m_p['fv'],m_p['fv'],m_p['tr'],m_p['task'],m_p['Q2'],m_p['Hvap_s'])
    DFS = Calculations_Kettle_4_Flow.D_FS(Ds,Npt,L,D_FF)
    

    DRS = Calculations_Kettle_4_Flow.D_RS(Ds,Npt,L,D_FF)
    W = Calculations_Kettle_4_Geometry.fun_W(Ds,Npt)
    cost_pipe = 100* (D_FF + DFS + D_RF + DRS)
    DeltaHL = Calculations_Kettle_4_Flow.deltaH_L(Ds,dte,Npt,rp,lay,L, D_FF, D_RF,m_p['m_s'], m_p['mil_s'],
                                                    m_p['L_FF'],m_p['fv'],m_p['rol_s'], m_p['rov_s'], m_p['miv_s'],
                                                    m_p['L_FS'],m_p['L_RS'],m_p['L_RF'],m_p['g'])
    HE_CAPEX = 29000 + 400*Area**0.9 + 50*Ds2 + 5*W  + cost_pipe + (DeltaHL- m_p['Z'])
    return HE_CAPEX


# endregion
##################################################################################################################

