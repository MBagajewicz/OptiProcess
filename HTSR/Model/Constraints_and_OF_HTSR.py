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
from HTSR.Calculations import (
    Calculations_HTSR_Flow,
    Calculations_HTSR_Heat_Transfer,
    Calculations_HTSR_Area ,Calculations_HTSR_Geometry
)

# endregion
##################################################################################################################

##################################################################################################################
# region Kettle model from Sales et al 2021

# ----------------------------------------------------------------------------------------------------------------
# Trimming Functions
# ----------------------------------------------------------------------------------------------------------------

# Lower bound on L/Ds
def LD_lb(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    fun_val = m_p['LBLD'] - L/Ds
    return fun_val

# Upper bound on L/Ds
def LD_ub(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    fun_val = L/Ds - m_p['UBLD']
    return fun_val

# Lower bound on vt
def vt_lb(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    vt = Calculations_HTSR_Flow.fun_vt(Ds, dte, Npt, rp, lay, m_p['m_t'],m_p['rol_t'],m_p['rov_t'],m_p['fluid_type'],m_p['thk'])
    fun_val = m_p['vtmin'] - vt
    return fun_val

# Upper bound on vt
def vt_ub(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    vt = Calculations_HTSR_Flow.fun_vt(Ds, dte, Npt, rp, lay, m_p['m_t'],m_p['rol_t'],m_p['rov_t'],m_p['fluid_type'],m_p['thk'])
    fun_val = vt - m_p['vtmax']
    return fun_val

# Lower bound on Ret
def Ret_lb(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):

    Ret = Calculations_HTSR_Flow.fun_Ret(Ds,dte,Npt,rp,lay,m_p['m_t'],m_p['rol_t'],m_p['rov_t'],m_p['fluid_type']
                                             ,m_p['mil_t'],m_p['miv_t'],m_p['thk'])
    fun_val = m_p['Retmin'] - Ret
    return fun_val

# Maximum heat flux
def q_ub(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    A = Calculations_HTSR_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    q = Calculations_HTSR_Heat_Transfer.fun_q(m_p['Q'], A)
    qb_max = Calculations_HTSR_Heat_Transfer.fun_qb_max(Ds, dte, Npt, rp, lay, L, m_p['q1_max'])
    fun_val = q - 0.7*qb_max
    return fun_val

# Maximum pressure drop
def dPt_up(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    dPt = Calculations_HTSR_Flow.fun_dPt(Ds, dte, Npt, rp, lay, L, m_p['m_t'],m_p['rol_t'],m_p['rov_t'],m_p['fluid_type']
                                             ,m_p['mil_t'],m_p['miv_t'],m_p['thk'])
    fun_val = dPt - m_p['dPt_disp']

    
 
    return fun_val

# Excess area
def A_exc(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    Areq = Calculations_HTSR_Heat_Transfer.fun_A_req(Ds, dte, Npt, rp, lay, L, m_p['thk'], m_p['rol_t'], m_p['rov_t'], m_p['g'], 
                                                         m_p['kl_t'], m_p['m_t'], m_p['mil_t'],m_p['miv_t'], m_p['Q'], m_p['BR'], m_p['Pc'], 
                                                         m_p['Fp'], m_p['hnc'], m_p['Rf_t'], m_p['Rf_s'], m_p['ktube'], m_p['dTLM'],m_p['fluid_type'],
                                                           m_p['kl_t'],m_p['Cp_t'],m_p['m_s'],m_p['Fv'],m_p['rol_s'],m_p['Cpl_s'],m_p['mil_s'],m_p['kl_s'],m_p['miv_s'],m_p['rov_s'])
    
    A = Calculations_HTSR_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    fun_val = (1 + m_p['Aexc'])*Areq - A
    
    return fun_val


def VRS_ub(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
     V_RS = Calculations_HTSR_Flow.V_RS(Ds,Npt,L,D_RF,m_p['m_s'],m_p['Fv'], m_p['rov_s'], m_p['rol_s'])
     rho_tp2 = Calculations_HTSR_Flow.ro_tp2(m_p['Fv'], m_p['rov_s'], m_p['rol_s'])
     fun_val = V_RS -77.15 * rho_tp2**(-0.5)
     return fun_val 

def VRF_ub(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
     V_RF = Calculations_HTSR_Flow.V_RF( D_RF,m_p['m_s'],m_p['Fv'], m_p['rov_s'], m_p['rol_s'])
     rho_tp2 = Calculations_HTSR_Flow.ro_tp2(m_p['Fv'], m_p['rov_s'], m_p['rol_s'])
     fun_val = V_RF -77.15 * rho_tp2**(-0.5)
     return fun_val 



def Hl_ub(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    Hl  = Calculations_HTSR_Flow.deltaH_L(Ds,dte,Npt,rp,lay,L, D_FF, D_RF,m_p['m_s'], m_p['mil_s'],
                                                    m_p['L_FF'],m_p['Fv'],m_p['rol_s'], m_p['rov_s'], m_p['miv_s'],
                                                    m_p['L_FS'],m_p['L_RS'],m_p['L_RF'],m_p['g'])
    fun_val = Hl - m_p['Hl_max']
    return fun_val


# ----------------------------------------------------------------------------------------------------------------
# Objective Function
# ----------------------------------------------------------------------------------------------------------------

def Area_OF(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    HE_Area = Calculations_HTSR_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    return HE_Area



def Cost_OF(Ds, dte, Npt, rp, lay, L,D_FF,D_RF,m_p):
    Area = Calculations_HTSR_Area.fun_A(Ds, dte, Npt, rp, lay, L)
    DFS = Calculations_HTSR_Flow.D_FS(Ds,Npt,L,D_FF)
    DRS = Calculations_HTSR_Flow.D_FS(Ds,Npt,L,D_RF)
    cost_pipe = 100* (D_FF + DFS + D_RF + DRS)
    DeltaHL = Calculations_HTSR_Flow.deltaH_L(Ds,dte,Npt,rp,lay,L, D_FF, D_RF,m_p['m_s'], m_p['mil_s'],
                                                    m_p['L_FF'],m_p['Fv'],m_p['rol_s'], m_p['rov_s'], m_p['miv_s'],
                                                    m_p['L_FS'],m_p['L_RS'],m_p['L_RF'],m_p['g'])
    
    HE_CAPEX = 29000 + 400*Area**0.9 + cost_pipe + (DeltaHL+ m_p['Z'])
    return HE_CAPEX


# endregion
##################################################################################################################

