###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          22-Aug-2025     Sung Young Kim            copy from GPHE folder
#   0.1          21-Oct-2025     Sung Young Kim            Add Air preheater set trimming procedure
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
import numpy as np
import ast
from scipy import optimize
from APH.Calculations import (
    Calculations_APH_tube,
    Calculations_APH_velocity,
    Calculations_APH_Reynolds,
    Calculations_APH_pressure_drop,
    Calculations_APH_U,
    Calculations_APH_area,
    Calculations_APH_correction_factor,
    Calculations_APH_TAC,
    Calculations_APH_CAPEX
)
from Common_Equations_HEX import Calculations_HEX_heatload, Calculations_HEX_LMTD
# endregion
##################################################################################################################

##################################################################################################################
# region calculations

def dch_lb(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    rph = rph.astype(np.float64)    
    # Tuples extraction   
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Lower bound on dch
    dch = Calculations_APH_tube.APH_dch(Do, rph) 
    fun_val = ( 2*m_p['lf'] + Do )- dch
    return fun_val


def tube_lb(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    rph = rph.astype(np.float64)    
    rpv = rpv.astype(np.float64)    
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Lower bound on Tube
    dcv = Calculations_APH_tube.APH_dcv(Do, rpv)
    dch = Calculations_APH_tube.APH_dch(Do, rph)
    fun_val = ( 2*m_p['lf'] + Do )- np.sqrt(np.power(dcv,2)+np.power(dch,2))
    return fun_val


def vair_lb(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    Nr = Nr.astype(np.float64)  
    L  = L.astype(np.float64)  
    rph = rph.astype(np.float64)            
    rpv = rpv.astype(np.float64)    
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Lower bound on vair
    vair = Calculations_APH_velocity.APH_v_air(Nr, Do, rpv, m_p['lf'], rph, L, m_p['m_air'], m_p['rho_air'])
    fun_val = m_p['v_air_min'] - vair
    return fun_val

def vair_ub(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    Nr = Nr.astype(np.float64)  
    L  = L.astype(np.float64)  
    rph = rph.astype(np.float64)            
    rpv = rpv.astype(np.float64)    
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Upper bound on vair
    vair = Calculations_APH_velocity.APH_v_air(Nr, Do, rpv, m_p['lf'], rph, L, m_p['m_air'], m_p['rho_air'])
    fun_val = vair - m_p['v_air_max']
    return fun_val


def vtube_lb(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    Nr = Nr.astype(np.float64)  
    Nc = Nc.astype(np.float64)  
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Lower bound on vtube
    vtube = Calculations_APH_velocity.APH_v_tube(Do, td, Nc, Nr, m_p['m_gas'], m_p['rho_gas'])
    fun_val = m_p['v_gas_min'] - vtube
    return fun_val

def vtube_ub(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    Nr = Nr.astype(np.float64)  
    Nc = Nc.astype(np.float64)  
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Upper bound on vtube
    vtube = Calculations_APH_velocity.APH_v_tube(Do, td, Nc, Nr, m_p['m_gas'], m_p['rho_gas'])
    fun_val = vtube - m_p['v_gas_max']
    return fun_val

def Reair_lb(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    Nr = Nr.astype(np.float64)  
    rpv = rpv.astype(np.float64)  
    rph = rph.astype(np.float64)
    L = L.astype(np.float64)
    Ncross = Ncross.astype(np.float64)              
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)

    # Lower bound on Re_air
    Re_air = Calculations_APH_Reynolds.APH_Re_air(Nr, Do, rpv, m_p['lf'], rph, L, m_p['m_air'], m_p['rho_air'], m_p['mu_air'])
    fun_val = m_p['Re_air_min'] - Re_air
    return fun_val

def Reair_ub(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    Nr = Nr.astype(np.float64)  
    rpv = rpv.astype(np.float64)  
    rph = rph.astype(np.float64)
    L = L.astype(np.float64)
    Ncross = Ncross.astype(np.float64)              
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)

    # Upper bound on Re_air
    Re_air = Calculations_APH_Reynolds.APH_Re_air(Nr, Do, rpv, m_p['lf'], rph, L, m_p['m_air'], m_p['rho_air'], m_p['mu_air'])
    fun_val = Re_air - m_p['Re_air_max']
    return fun_val

def Retube_lb(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    Nr = Nr.astype(np.float64)  
    Nc = Nc.astype(np.float64)     
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Lower bound on Re_tube
    Re_tube = Calculations_APH_Reynolds.APH_Re_tube(Do, td, Nc, Nr, m_p['m_gas'], m_p['rho_gas'], m_p['mu_gas'])
    fun_val = m_p['Re_tube_min'] - Re_tube
    return fun_val

def Retube_ub(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    Nr = Nr.astype(np.float64)  
    Nc = Nc.astype(np.float64)     
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Upper bound on Re_tube
    Re_tube = Calculations_APH_Reynolds.APH_Re_tube(Do, td, Nc, Nr, m_p['m_gas'], m_p['rho_gas'], m_p['mu_gas'])
    fun_val = Re_tube - m_p['Re_tube_max']
    return fun_val

def DPair_ub(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    L = L.astype(np.float64)  
    Nr = Nr.astype(np.float64)  
    Nc = Nc.astype(np.float64)  
    rph = rph.astype(np.float64)  
    rpv = rpv.astype(np.float64)  
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)

    # Upper bound on DeltaP_air
    DeltaP_air = Calculations_APH_pressure_drop.APH_DeltaP_air(Nr, Do, rpv, m_p['lf'], rph, L, m_p['m_air'], m_p['rho_air'], m_p['mu_air'])

    fun_val = DeltaP_air - m_p['DPairdisp']
    return fun_val

def DPtube_ub(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    L = L.astype(np.float64)  
    Nr = Nr.astype(np.float64)  
    Nc = Nc.astype(np.float64)  
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Upper bound on DeltaP_tube
    DeltaP_tube = Calculations_APH_pressure_drop.APH_DeltaP_tube(Do, td, Nc, Nr, m_p['m_gas'], m_p['rho_gas'], m_p['mu_gas'], L)

    fun_val = DeltaP_tube - m_p['DPgasdisp']
    return fun_val


def F_min(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    # Number of candidates N: Do_td is a list of string tuples
    N = len([ast.literal_eval(t) for t in Do_td])

    # lower bound on F
    F = Calculations_APH_correction_factor.APH_F(m_p['Cp_air'], m_p['m_air'], m_p['Cp_gas'], m_p['m_gas'], m_p['Tgas_in'], m_p['Tair_in'], m_p['Tgas_out'], m_p['Tair_out'])
    
    fun_val = np.full(N, m_p['F_min'] - F, dtype=float)
    return fun_val

def Areq(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    L = L.astype(np.float64)  
    Nr = Nr.astype(np.float64)  
    Nc = Nc.astype(np.float64)  
    Ncross = Ncross.astype(np.float64)  
    rph = rph.astype(np.float64)  
    rpv = rpv.astype(np.float64)  
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    td = np.array([t[1] for t in Do_td_list],dtype=np.float64)
    # floats, not 1-element arrays
    if Do.size == 1: Do = Do.item()
    if td.size == 1: td = td.item()    

    # Required area constraint
    Q = Calculations_HEX_heatload.HEX_heat_load(m_p['m_gas'], m_p['Cp_gas'], m_p['Tgas_in'], m_p['Tgas_out'])
    U = Calculations_APH_U.APH_U(Do, td, Nc, Nr, m_p['m_gas'], m_p['rho_gas'], m_p['mu_gas'], m_p['Cp_gas'], m_p['k_gas'], 
                                 rpv, m_p['lf'], rph, L, m_p['m_air'], m_p['rho_air'], m_p['mu_air'], m_p['Cp_air'], 
                                 m_p['k_air'], m_p['Rf_gas'], m_p['Rf_air'])
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(m_p['Tgas_in'], m_p['Tgas_out'], m_p['Tair_in'], m_p['Tair_out'])
    F = Calculations_APH_correction_factor.APH_F(m_p['Cp_air'], m_p['m_air'], m_p['Cp_gas'], m_p['m_gas'], m_p['Tgas_in'], m_p['Tair_in'], m_p['Tgas_out'], m_p['Tair_out'])
    area_tot = Calculations_APH_area.APH_area_tot(Do, m_p['lf'], Nc, Nr, L, m_p['Nf'], m_p['tf'], Ncross)
    Areq = Q / (U * LMTD * F)
    fun_val = (Areq * (1 + m_p['Aexc'] / 100)) - area_tot
    return fun_val

# --------------------------------------------------------------------------------------------------------------------
# Objective Function
# --------------------------------------------------------------------------------------------------------------------

def TAC_OF(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    L = L.astype(np.float64)  
    Nr = Nr.astype(np.float64)  
    Nc = Nc.astype(np.float64)  
    Ncross = Ncross.astype(np.float64)  
    rph = rph.astype(np.float64)  
    rpv = rpv.astype(np.float64)  
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    td = np.array([t[1] for t in Do_td_list],dtype=np.float64)
    # floats, not 1-element arrays
    if Do.size == 1: Do = Do.item()
    if td.size == 1: td = td.item()

    # Objective function
    TAC = Calculations_APH_TAC.APH_TAC(m_p['int_rate'], m_p['n'], Do, td, m_p['lf'], Nc, Nr, L, m_p['Nf'], m_p['tf'], 
                                       Ncross, m_p['par_a'], m_p['par_b'], rpv, rph, m_p['m_air'], m_p['rho_air'], m_p['mu_air'], 
                                       m_p['m_gas'], m_p['rho_gas'], m_p['mu_gas'], m_p['Nop'], m_p['pc'], m_p['eta'])
    return TAC


def AREA_OF(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    L = L.astype(np.float64)  
    Nr = Nr.astype(np.float64)  
    Nc = Nc.astype(np.float64)  
    Ncross = Ncross.astype(np.float64)  
    rph = rph.astype(np.float64)  
    rpv = rpv.astype(np.float64)  
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    td = np.array([t[1] for t in Do_td_list],dtype=np.float64)
    # floats, not 1-element arrays
    if Do.size == 1: Do = Do.item()
    if td.size == 1: td = td.item()    

    # Objective function
    Area = Calculations_APH_area.APH_area_tot(Do, m_p['lf'], Nc, Nr, L, m_p['Nf'], m_p['tf'], Ncross)
    return Area


def CAPEX_OF(Do_td, L, Nr, Nc,  Ncross, rph, rpv, m_p):
    L = L.astype(np.float64)  
    Nr = Nr.astype(np.float64)  
    Nc = Nc.astype(np.float64)  
    Ncross = Ncross.astype(np.float64)  
    rph = rph.astype(np.float64)  
    rpv = rpv.astype(np.float64)  
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    td = np.array([t[1] for t in Do_td_list],dtype=np.float64)
    # floats, not 1-element arrays
    if Do.size == 1: Do = Do.item()
    if td.size == 1: td = td.item()       

    # Objective function
    CAPEX = Calculations_APH_CAPEX.APH_CAPEX(Do, m_p['lf'], Nc, Nr, L, m_p['Nf'], m_p['tf'], Ncross, m_p['par_a'], m_p['par_b'])
    return CAPEX

# endregion
##################################################################################################################
