###################################################################################################################
# region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          2024            Diego Oliva               Original
#   0.1          24-Mar-2024     Sung Young Kim            Add fired heater case

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

#from scipy.optimize import minimize, Bounds
#from scipy.optimize import newton_krylov
#from scipy.optimize import least_squares
#from scipy.optimize import NonlinearConstraint
#from scipy.optimize import root
from scipy.optimize import fsolve
from scipy.optimize import brentq


import numpy as np
import numpy as _np
import math
import ast
from FIRED_HEATER.Calculations import (
    Calculations_FIRED_HEATER_Aconv,
    Calculations_FIRED_HEATER_Acp,
    Calculations_FIRED_HEATER_Aot,
    Calculations_FIRED_HEATER_area_flow,
    Calculations_FIRED_HEATER_Q_conv,
    Calculations_FIRED_HEATER_Q_oil,
    Calculations_FIRED_HEATER_Q_radiant,
    Calculations_FIRED_HEATER_Urad,
    Calculations_FIRED_HEATER_Uconv,
    Calculations_FIRED_HEATER_Tc,
    Calculations_FIRED_HEATER_Tfb,
    Calculations_FIRED_HEATER_Ts,
    Calculations_FIRED_HEATER_area_radiant,
    Calculations_FIRED_HEATER_boxsize,
    Calculations_FIRED_HEATER_cp_gas,
    Calculations_FIRED_HEATER_HTCo,
    Calculations_FIRED_HEATER_pressure,
    Calculations_FIRED_HEATER_j_factor,
    Calculations_FIRED_HEATER_fin_overall,
    Calculations_FIRED_HEATER_fin_efficiency,
    Calculations_FIRED_HEATER_draft,
    Calculations_FIRED_HEATER_friction_losses,
    Calculations_FIRED_HEATER_gas_flow,
    Calculations_FIRED_HEATER_oil_velocity,
    Calculations_FIRED_HEATER_pressure,
    Calculations_FIRED_HEATER_tubes,
    Calculations_FIRED_HEATER_OP_cost
)
from Common_Equations_HEX import Calculations_HEX_LMTD, Calculations_HEX_heatload
# endregion
##################################################################################################################

##################################################################################################################
# region Example 1

# def HW_lb((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def HW_lb(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):

    Npasses = Npasses.astype(np.float64)
    Ntceil = Ntceil.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Rpr = Rpr.astype(np.float64)
    Rph = Rph.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Lower bound on H/W
    Hrad = Calculations_FIRED_HEATER_boxsize.HEATER_Hrad(Do, Nprad, Npasses, Ntceil, Rpr)
    Wrad = Calculations_FIRED_HEATER_boxsize.HEATER_Wrad(Ntceil, Do, Rpr, Npconv, Npasses, pd['lf'], Rph)
    fun_val = pd['HW_Min'] - Hrad/Wrad
    return fun_val


# def HW_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def HW_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):

    Npasses = Npasses.astype(np.float64)
    Ntceil = Ntceil.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Rpr = Rpr.astype(np.float64)
    Rph = Rph.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # upper bound on H/W
    Hrad = Calculations_FIRED_HEATER_boxsize.HEATER_Hrad(Do, Nprad, Npasses, Ntceil, Rpr)
    Wrad = Calculations_FIRED_HEATER_boxsize.HEATER_Wrad(Ntceil, Do, Rpr, Npconv, Npasses, pd['lf'], Rph)
    fun_val = Hrad/Wrad - pd['HW_Max']
    return fun_val


# def LW_lb((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def LW_lb(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):

    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Ntceil = Ntceil.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Rpr = Rpr.astype(np.float64)
    Rph = Rph.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Lower bound on L/W

    Wrad = Calculations_FIRED_HEATER_boxsize.HEATER_Wrad(Ntceil, Do, Rpr, Npconv, Npasses, pd['lf'], Rph)
    fun_val = pd['LW_Min'] - L/Wrad
    return fun_val


# def LW_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def LW_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
 
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Ntceil = Ntceil.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Rpr = Rpr.astype(np.float64)
    Rph = Rph.astype(np.float64)    
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Upper bound on L/W
    Wrad = Calculations_FIRED_HEATER_boxsize.HEATER_Wrad(Ntceil, Do, Rpr, Npconv, Npasses, pd['lf'], Rph)
    fun_val = L/Wrad - pd['LW_Max']
    return fun_val


# def BOX_lb((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def BOX_lb(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Ntceil = Ntceil.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Rpr = Rpr.astype(np.float64)
    Rph = Rph.astype(np.float64)    
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Lower bound on Boxsize
    Boxsize = Calculations_FIRED_HEATER_boxsize.HEATER_Boxsize(L,Do, Nprad, Npasses, Ntceil, Rpr, pd['pk1'], Npconv, pd['lf'], Rph)
    fun_val = pd['BOX_Min'] - Boxsize
    return fun_val


# def BOX_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def BOX_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Ntceil = Ntceil.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Rpr = Rpr.astype(np.float64)
    Rph = Rph.astype(np.float64)    
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Upper bound on Boxsize
    Boxsize = Calculations_FIRED_HEATER_boxsize.HEATER_Boxsize(L,Do, Nprad, Npasses, Ntceil, Rpr, pd['pk1'], Npconv, pd['lf'], Rph)
    fun_val =  Boxsize - pd['BOX_Max']
    return fun_val


# def dcr_lb((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def dcr_lb(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    Rph = Rph.astype(np.float64)    
    Rpr = Rpr.astype(np.float64)    
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Lower bound on dcr
    dcr = Calculations_FIRED_HEATER_tubes.HEATER_dcr(Do, Rpr)
    fun_val = (Do + 0.01) - dcr
    return fun_val

# def dch_lb((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def dch_lb(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    Rph = Rph.astype(np.float64)    
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Lower bound on dch
    dch = Calculations_FIRED_HEATER_tubes.HEATER_dch(Do, Rph)
    fun_val = ( 2*pd['lf'] + Do )- dch
    return fun_val


# def Tube_lb((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def Tube_lb(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    Rph = Rph.astype(np.float64)    
    Rpv = Rpv.astype(np.float64)    
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Lower bound on Tube
    dcv = Calculations_FIRED_HEATER_tubes.HEATER_dcv(Do, Rpv)
    dch = Calculations_FIRED_HEATER_tubes.HEATER_dch(Do, Rph)
    fun_val = ( 2*pd['lf'] + Do )- np.sqrt(np.power(dcv,2)+np.power(dch,2))
    return fun_val


# def Ds_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def Ds_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    Npasses = Npasses.astype(np.float64)    
    Npconv = Npconv.astype(np.float64)    
    Rph = Rph.astype(np.float64)    
    Rpv = Rpv.astype(np.float64)    
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Ds_ts_list = [ast.literal_eval(t) for t in Ds_ts]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)
    Ds = np.array([t[0] for t in Ds_ts_list],dtype=np.float64)

    # Upeer bound on stack diameter
    Wconv = Calculations_FIRED_HEATER_boxsize.HEATER_Wconv(Npconv, Npasses, pd['lf'], Do, Rph )
    fun_val =  Ds - Wconv
    return fun_val


# def Vo_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def Vo_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    Npasses = Npasses.astype(np.float64)    
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Upeer bound on oil velocity in the tube 
    Voil_Tube = Calculations_FIRED_HEATER_oil_velocity.HEATER_Voil_Tube(Do, pd['Moil'], Npasses, pd['rho_oil'])
    fun_val =  Voil_Tube - pd['Voil_tube_Max']
    return fun_val

# def Po_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def Po_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)  
    Ntceil = Ntceil.astype(np.float64)
    Nrconv = Nrconv.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Upper bound on pressure drop in the oil tube
    PDrop_Tube = Calculations_FIRED_HEATER_pressure.HEATER_PDrop_Tube(Do, pd['Moil'], Npasses, pd['rho_oil'], pd['mu_oil'], L, pd['pk1'], Npconv, Nprad, Ntceil, Nrconv )
    fun_val =  PDrop_Tube - pd['Pd_tube_Max']
    return fun_val


# def glb_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def glb_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Rph = Rph.astype(np.float64) 
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Proxy Set Trimming : upper bound on gas mass flux_LB
    Ggas_LB = Calculations_FIRED_HEATER_gas_flow.HEATER_Ggas_LB(L, pd['pk1'], Nprad, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Tflame'], 
                                                          pd['Tfb_Min'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'])
    fun_val =  Ggas_LB - pd['G_Max']
    return fun_val

# def glb_lb((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def gub_lb(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):    
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Rph = Rph.astype(np.float64) 
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Proxy Set Trimming : upper bound on gas mass flux_LB
    Ggas_UB = Calculations_FIRED_HEATER_gas_flow.HEATER_Ggas_UB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], 
                                                          pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf']) 
    fun_val =  pd['G_Min'] - Ggas_UB  
    return fun_val


# def tc_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def tc_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64) 
    Npasses = Npasses.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Proxy Set Trimming : upper bound on Tc_LB
    Tc_LB = Calculations_FIRED_HEATER_Tc.HEATER_Tc_LB(pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['To_oil'], pd['Moil'], 
                                                L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Max'], pd['percent_loss_Rad'])

    fun_val =  Tc_LB - (pd['Tfb_Max']-5)
    return fun_val

# def tc_lb((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def tc_lb(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64) 
    Npasses = Npasses.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Proxy Set Trimming : upper bound on Tc_LB
    Tc_UB = Calculations_FIRED_HEATER_Tc.HEATER_Tc_UB(pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['To_oil'], pd['Moil'], 
                                                L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], pd['percent_loss_Rad'])

    fun_val = pd['Ti_oil'] - Tc_UB 
    return fun_val



# def tfb_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def tfb_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Proxy Set Trimming : upper bound on Tfb_LB
    Tfb_LB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_LB(pd['Tflame'], L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Max'], 
                                                   pd['percent_loss_Rad'], pd['Flux_Min'], pd['Tfb_Min'])
    fun_val =  Tfb_LB - pd['Tfb_Max']
    return fun_val

# def tfb_lb1((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def tfb_lb1(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Proxy Set Trimming : lower bound on Tfb_UB
    Tfb_UB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_UB(pd['Tflame'], L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], 
                                                   pd['percent_loss_Rad'], pd['Flux_Max'], pd['Tfb_Max'])
    fun_val = pd['Tfb_Min'] - Tfb_UB
    return fun_val


# def tfb_lb2((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def tfb_lb2(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Proxy Set Trimming : lower bound on Tfb_UB
    Tfb_UB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_UB(pd['Tflame'], L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], 
                                                   pd['percent_loss_Rad'], pd['Flux_Max'], pd['Tfb_Max'])
    Tc_LB = Calculations_FIRED_HEATER_Tc.HEATER_Tc_LB(pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['To_oil'], pd['Moil'], 
                                                L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Max'], pd['percent_loss_Rad'])
    fun_val = Tc_LB - Tfb_UB
    return fun_val


# def ts_lb((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def ts_lb(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Proxy Set Trimming : Lower bound on Ts_UB
    Ts_UB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_UB(pd['Tflame'], L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Flux_Max'], pd['Tfb_Max'], pd['hflame'], pd['percent_loss_Conv'], pd['Moil'], pd['To_oil'], pd['Ti_oil'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['Tfb_Min'])
    fun_val = (pd['Ti_oil']+5) - Ts_UB
    return fun_val



# def ts_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def ts_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Proxy Set Trimming : Upper bound on Ts_LB
    Ts_LB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_LB(pd['Tflame'],L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Flux_Min'], pd['Tfb_Min'], pd['hflame'], pd['percent_loss_Conv'], pd['Moil'], pd['To_oil'], pd['Ti_oil'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['Tfb_Max'])
    Tfb_UB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_UB(pd['Tflame'], L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Flux_Max'], pd['Tfb_Max'])
    fun_val = Ts_LB - Tfb_UB
    return fun_val



# def Qconv_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def Qconv_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Nrconv = Nrconv.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Rph = Rph.astype(np.float64)
    Rpv = Rpv.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)

    # Proxy Set Trimming : Upper bound on Qconv\
    Qconv_LB = Calculations_FIRED_HEATER_Q_conv.HEATER_Qconv_LB(pd['Pr_oil'], pd['k_oil'], Do, pd['Moil'], Npasses, pd['mu_oil'], pd['lf'], pd['tf'], pd['Nf'], pd['rf_oil'], pd['ks'], L, pd['pk1'], Nprad, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Rph, pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['To_oil'], pd['hflame'], pd['percent_loss_Conv'], pd['Ti_oil'])
    Qconv_UB = Calculations_FIRED_HEATER_Q_conv.HEATER_Qconv_UB(pd['Pr_oil'], pd['k_oil'], Do, pd['Moil'], Npasses, pd['mu_oil'], pd['lf'], pd['tf'], pd['Nf'], pd['rf_oil'], pd['ks'], L, pd['pk1'], Nprad, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Rph, pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'], pd['hflame'], pd['percent_loss_Conv'], pd['To_oil'], pd['Ti_oil'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'])
    fun_val = Qconv_LB - Qconv_UB
    return fun_val


# def DE_ub((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def DE_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Ntceil = Ntceil.astype(np.float64)
    Nrconv = Nrconv.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Hs = Hs.astype(np.float64)
    Rpr = Rpr.astype(np.float64)
    Rph = Rph.astype(np.float64)
    Rpv = Rpv.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Ds_ts_list = [ast.literal_eval(t) for t in Ds_ts]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)
    Ds = np.array([t[0] for t in Ds_ts_list],dtype=np.float64)

    # Set Trimming : draft effect
    Draft = Calculations_FIRED_HEATER_draft.HEATER_Draft(pd['Tflame'], Hs, Do, Nprad, Npasses, Ntceil, Rpr, pd['lf'], Rpv, Nrconv)
    Fsum_LB = Calculations_FIRED_HEATER_friction_losses.HEATER_Fsum_LB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Rpv, Nrconv, pd['Flux_Min'], pd['hflame'], pd['percent_loss_Conv'], pd['Moil'], pd['To_oil'], pd['Ti_oil'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['Tfb_Min'], Hs, Ds)

    fun_val = (1+0.05) * (83.69 + Fsum_LB) - Draft
    return fun_val
 

#--------------------------------------------------
# Lower bound model for smart enumeration
#--------------------------------------------------

def FIRED_HEATER_LB(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Nrconv = Nrconv.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Hs = Hs.astype(np.float64)
    Rph = Rph.astype(np.float64)
    Rpv = Rpv.astype(np.float64)
    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Ds_ts_list = [ast.literal_eval(t) for t in Ds_ts]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    #td = np.array([t[1] for t in Do_td_list],dtype=np.float64)
    Ds = np.array([t[0] for t in Ds_ts_list],dtype=np.float64)
    ts = np.array([t[1] for t in Ds_ts_list],dtype=np.float64)


    # Objective function of Lower Bound
    Arad = Calculations_FIRED_HEATER_area_radiant.HEATER_ARad(L, pd['pk1'], Nprad, Npconv, Npasses, Do)
    Rad_cost  = pd['R_uni'] * Arad * pd['CRF']

    Aconv = Calculations_FIRED_HEATER_Aconv.HEATER_Aconv(Npconv, Npasses, Nrconv, pd['lf'], Do, pd['tf'], pd['Nf'], L, pd['pk1'])
    Conv_cost = pd['C_uni'] * Aconv * pd['CRF']

    FB_cost = (pd['FK1'] + pd['FK2']*(Arad + Aconv )) * pd['CRF']

    Stack_cost = pd['S_uni'] * Hs * 3.141516 * Ds * ts * pd['CRF']

    OP_cost_LB = Calculations_FIRED_HEATER_OP_cost.HEATER_OP_cost_LB(L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Min'], pd['Ti_oil'], pd['T_outside'], pd['Moil'], pd['Flux_Max'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['To_oil'], pd['LHV'], pd['O_uni'], pd['OT'])

    OF_Solution_LB = Rad_cost + Conv_cost + FB_cost + Stack_cost + OP_cost_LB
    return OF_Solution_LB

#--------------------------------------------------
# Objective function
#--------------------------------------------------

def FIRED_HEATER_OF(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    # Setting : variable type
    L = L.astype(np.float64)
    Npasses = Npasses.astype(np.float64)
    Ntceil = Ntceil.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Nrconv = Nrconv.astype(np.float64)
    Rpr = Rpr.astype(np.float64)
    Rph = Rph.astype(np.float64)
    Rpv = Rpv.astype(np.float64)
    Hs = Hs.astype(np.float64)

    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Ds_ts_list = [ast.literal_eval(t) for t in Ds_ts]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)
    td = np.array([t[1] for t in Do_td_list],dtype=np.float64)
    Ds = np.array([t[0] for t in Ds_ts_list],dtype=np.float64)
    ts = np.array([t[1] for t in Ds_ts_list],dtype=np.float64)
    # floats, not 1-element arrays
    if Do.size == 1: Do = Do.item()
    if td.size == 1: td = td.item()
    if Ds.size == 1: Ds = Ds.item()
    if ts.size == 1: ts = ts.item()

    #calculations with the fixed geometry from set trimming result 
    alpha = Calculations_FIRED_HEATER_Acp.HEATER_alpha(Do, Rpr)
    Acp = Calculations_FIRED_HEATER_Acp.HEATER_Acp(L, pd['pk1'], Nprad, Npconv, Npasses, Do, Rpr)
    Arad = Calculations_FIRED_HEATER_area_radiant.HEATER_ARad(L, pd['pk1'], Nprad, Npconv, Npasses, Do)
    A = Calculations_FIRED_HEATER_Acp.HEATER_A(L, pd['pk1'], Ntceil, Do, Rpr, Npconv, Npasses, pd['lf'], Rph, Nprad)
    Factor_PL = Calculations_FIRED_HEATER_Acp.HEATER_Factor_PL(pd['excess_air'], L, pd['pk1'], Ntceil, Do, Rpr, Npconv, Npasses, pd['lf'], Rph, Nprad)
    Urad = Calculations_FIRED_HEATER_Urad.HEATER_Urad(Do, pd['Moil'], Npasses, pd['rho_oil'], pd['mu_oil'], pd['Pr_oil'], pd['k_oil'], pd['rf_gas'], pd['ks'], pd['rf_oil'])    
    cp_gas = Calculations_FIRED_HEATER_cp_gas.HEATER_cp_gas(pd['Tflame'])
    Aconv = Calculations_FIRED_HEATER_Aconv.HEATER_Aconv(Npconv, Npasses, Nrconv, pd['lf'], Do, pd['tf'], pd['Nf'], L, pd['pk1'])
    C3 = Calculations_FIRED_HEATER_j_factor.HEATER_C3(pd['lf'], Do, pd['Nf'], pd['tf'])
    C5 = Calculations_FIRED_HEATER_j_factor.HEATER_C5(Nrconv, Do, Rpv, Rph)
    Uc1 = Calculations_FIRED_HEATER_Uconv.HEATER_Uc1(pd['Pr_oil'], pd['k_oil'], Do, pd['Moil'], Npasses, pd['mu_oil'], pd['lf'], pd['tf'], pd['Nf'], pd['rf_oil'])
    Uc2 = Calculations_FIRED_HEATER_Uconv.HEATER_Uc2(pd['lf'], Do, pd['tf'], pd['Nf'], pd['ks'])
    df = Calculations_FIRED_HEATER_tubes.HEATER_df(pd['lf'], Do)
    As = Calculations_FIRED_HEATER_area_flow.HEATER_As(L, pd['pk1'], Npconv, Npasses, pd['lf'], Do, Rph, pd['Nf'], pd['tf'])
    Aot = Calculations_FIRED_HEATER_Aot.HEATER_Aot(pd['lf'], Do, pd['tf'], pd['Nf'])
    Aof = Calculations_FIRED_HEATER_Aot.HEATER_Aof(pd['lf'], Do, pd['tf'], pd['Nf'])
    Qoil = Calculations_FIRED_HEATER_Q_oil.HEATER_Qoil(pd['Moil'], pd['To_oil'], pd['Ti_oil'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'])
    Lfe = Calculations_FIRED_HEATER_fin_efficiency.HEATER_Lfe(pd['lf'], pd['tf'], Do)
    # capital cost
    Rad_cost  = pd['R_uni'] * Arad * pd['CRF']
    Conv_cost = pd['C_uni'] * Aconv * pd['CRF']
    FB_cost = (pd['FK1'] + pd['FK2']*(Arad + Aconv )) * pd['CRF']
    Stack_cost = pd['S_uni'] * Hs * 3.141516 * Ds * ts * pd['CRF']
    Capital_cost = Rad_cost + Conv_cost + FB_cost + Stack_cost

    #---------------------------------
    # BISECTION METHOD
    #---------------------------------
    
    # Initial bounds for Tc
    Tc_low = 400
    Tc_high = 600
    tol = 1e-6
    max_iter = 100

    for i in range(max_iter):
        # Step 1: Assume Tc
        Tc = (Tc_low + Tc_high) / 2

        # Step 2: Qrad
        Qrad = Calculations_FIRED_HEATER_Q_oil.HEATER_Qoil(pd['Moil'], pd['To_oil'], Tc, pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3']) / (1 - pd['percent_loss_Rad'])
 
        # Step 3: Tw
        Tw = Qrad * (1 - pd['percent_loss_Rad']) / (Urad * Arad) + (pd['To_oil'] + Tc) / 2

        # Step 4: Tfb
        def f_Tfb_rad(Tfb):
            Ems = (pd['e_c1'] * Tfb + pd['e_c2'] * Factor_PL + pd['e_c3'] * np.power(Factor_PL,2) + pd['e_c4'])
            F_ex_p = Ems *(A/(alpha*Acp) - 1)
            F_ex = (pd['f_c1'] * np.log(Ems) + (pd['f_c2']/Ems+pd['f_c3'])*F_ex_p + pd['f_c4'] * np.exp(Ems) + pd['f_c5']*np.power(F_ex_p,1.5) + pd['f_c6'])

            return alpha * Acp * pd['sigma'] * (np.power(Tfb+460.67,4)-np.power(Tw+460.67,4)) * F_ex + pd['hgr'] * Arad * (Tfb - Tw) - Qrad * (1 - pd['percent_loss_Rad'])

        Tfb_rad = fsolve(f_Tfb_rad, Tw + 150, xtol=1e-12)[0]    

        # Step 5: M_gas
        Mgas = Qrad * (1 - pd['percent_loss_Rad']) / (cp_gas * (pd['Tflame'] - Tfb_rad))

        # Step 6: Ts
        #Ts = Tfb_rad - (Qoil - Qrad * (1 - pd['percent_loss_Rad'])) / (Mgas * cp_gas)
        Qconv = (Qoil - Qrad * (1 - pd['percent_loss_Rad']))/(1 - pd['percent_loss_Conv'])
        Ts = Tfb_rad - Qconv * (1 - pd['percent_loss_Conv']) / (Mgas * cp_gas)
        #Ts = Tfb_rad - (Qoil - Qrad * (1 - pd['percent_loss_Rad'])) / (Mgas * cp_gas)

        # Step 7: Tfb (convection side)
        def f_Tfb_conv(Tfb):
            Ggas = Mgas/As
            HTCo = 0.091 * np.power(Do * Ggas /pd['mu_gas'] , -0.25) * C3 * C5 * np.power(df/Do, 0.5) * cp_gas * Ggas * np.power(pd['Pr_gas'], -0.67)
            h1 = 1 /( (1/HTCo) + pd['rf_gas'] )
            mf = np.power(2*h1 /( pd['k_fin'] * pd['tf']), 0.5)
            nuf = (np.exp(2*mf*Lfe) - 1 )/(np.exp(2*mf*Lfe)+1) * (1/(mf*Lfe)) 
            nut = ((Aot - Aof )/ Aot + nuf *( Aof / Aot))
            Uconv = 1/(Uc1 + Uc2 + ( 1 + pd['rf_gas'] * HTCo )/(nut*HTCo))

            delta1 = Tfb - Tc
            delta2 = Ts - pd['Ti_oil']
            if delta1 <= 0 or delta2 <= 0:
                return 1e6
            log_term = np.log(delta1 / delta2)
            #Qconv_expected = (Qoil - Qrad * (1 - pd['percent_loss_Rad']))/(1 - pd['percent_loss_Conv'])
            #Qconv_calc = (Uconv * Aconv * (delta1 - delta2) / log_term)/(1 - pd['percent_loss_Conv'])
            #return Qconv_expected - Qconv_calc
            return (Uconv * Aconv * (delta1 - delta2) / log_term) - Qconv*(1 - pd['percent_loss_Conv'])

        Tfb_conv = fsolve(f_Tfb_conv, (Ts + Tc) + 50, xtol=1e-12)[0]

        #print("-------------------------")
        #print("---Iteration---", i)
        #print("Tc_B         : ", Tc)
        #print("Qrad_B       : ", Qrad)
        #print("Tfb_rad_B    : ", Tfb_rad)
        #print("Ts_B         : ", Ts)
        #print("Tfb_conv_B   : ", Tfb_conv)
        #print("                         ")

        # Convergence check
        if abs(Tfb_rad - Tfb_conv) < tol:
        #if abs(Tc_low - Tc_high) < tol:
            break

        # Update Tc bounds
        if Tfb_rad < Tfb_conv: # Tc is too high, so Tfb_conv is greater
            Tc_high = Tc       # Tc should be decreased : Tc_high = Tc
        else:                  # Tc is too low, so Tfb_rad is greater
            Tc_low = Tc        # Tc should be increased : Tc_low = Tc

    #-----------------------------------------------------------
    # Ineqaulity Constraints for SMART ENUMERATION
    flux = Qrad / Arad
    if flux > pd['Flux_Max'] or flux < pd['Flux_Min']:
        return [1e20]  # Flux constraint violated, return large penalty cost
        
    Ggas = Mgas/As
    if Ggas > pd['G_Max'] or Ggas < pd['G_Min']:
        return [1e20]  # gas mass flux constraint violated, return large penalty cost

    Draft = Calculations_FIRED_HEATER_draft.HEATER_Draft(pd['Tflame'], Hs, Do, Nprad, Npasses, Ntceil, Rpr, pd['lf'], Rpv, Nrconv)
    Fsum = Calculations_FIRED_HEATER_friction_losses.HEATER_Fsum_LB(L, pd['pk1'], Nprad, Do, flux, pd['percent_loss_Rad'], pd['Tflame'], Tfb_rad, Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Rpv, Nrconv, flux, pd['hflame'], pd['percent_loss_Conv'], pd['Moil'], pd['To_oil'], pd['Ti_oil'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['Tfb_Min'], Hs, Ds)
    Draft_MIN =  (1+0.05)*(83.69 + Fsum)
    if Draft < Draft_MIN:
        return [1e20]  # Draft constraint violated, return large penalty cost
    #-----------------------------------------------------------

    # Final values after convergence
    #print("----------RESULT----------")
    #print("Tc         : ", Tc)
    #print("Tfb        : ", Tfb_rad)
    #print("Tw         : ", Tw)
    #print("Ts         : ", Ts)
    #print("Mgas       : ", Mgas)
    #print("Qrad       : ", Qrad)

    # Calculate solutions
    Qconv = (Qoil - Qrad * (1 - pd['percent_loss_Rad']))/(1 - pd['percent_loss_Conv'])
    delta1 = Tfb_rad - Tc
    delta2 = Ts - pd['Ti_oil']
    log_term = np.log(delta1 / delta2)
    LMTD = (delta1 - delta2)/log_term
    Qs = Mgas * cp_gas * (Ts - pd['T_outside'])
    Qn = Qrad + Qconv + Qs
    Mfuel = Qn/pd['LHV']
    OP_cost = pd['O_uni'] * Mfuel * pd['OT']
    Total_cost = (OP_cost + Capital_cost)
    #print("Qconv      : ", Qconv)
    #print("Qs         : ", Qs)
    #print("Qn         : ", Qn)
    #print("LMTD       : ", LMTD)   
    #print("Mfuel      : ", Mfuel)
    #print("OP_cost    : ", OP_cost)
    #print("Total_cost : ", Total_cost)

    #print("----Inequality constraint----")
    #print("Ggas       : ", Ggas)
    #print("Flux       : ", flux)
    #print("Draft      : ", Draft)
    #print("Draft_MIN  : ", Draft_MIN)

    #print("---------Paramaters----------")
    #print("Urad     : ", Urad)
    #print("Arad     : ", Arad)
    #print("Aconv    : ", Aconv)

    #print("-----------------------------")

    OF_solution = Total_cost
    return OF_solution


# endregion
##################################################################################################################


'''
#------------------------------------------------------------------
# Constraints for SMART ENUMERATION
#------------------------------------------------------------------

# def FLUX_lb((Do, td), (Ds, ts), L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv):
def FLUX_lb(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Npasses = Npasses.astype(np.float64)

    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Ds_ts_list = [ast.literal_eval(t) for t in Ds_ts]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)

    # lower limit flux
    Arad = Calculations_FIRED_HEATER_area_radiant.HEATER_ARad(L, pd['pk1'], Nprad, Npconv, Npasses, Do)
    Qrad = Calculations_FIRED_HEATER_Q_oil.HEATER_Qoil(pd['Moil'], pd['To_oil'], Tc, pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3']) / (1 - pd['percent_loss_Rad'])
    flux = Qrad/Arad
    fun_val = flux - pd['Flux_Min']
    return fun_val

def FLUX_ub(Do_td, Ds_ts, L, Npasses, Ntceil, Nrconv, Nprad, Npconv, Hs, Rpr, Rph, Rpv, pd):
    L = L.astype(np.float64)
    Nprad = Nprad.astype(np.float64)
    Npconv = Npconv.astype(np.float64)
    Npasses = Npasses.astype(np.float64)

    # Tuples extraction    
    Do_td_list = [ast.literal_eval(t) for t in Do_td]
    Ds_ts_list = [ast.literal_eval(t) for t in Ds_ts]
    Do = np.array([t[0] for t in Do_td_list],dtype=np.float64)

    # lower limit flux
    Arad = Calculations_FIRED_HEATER_area_radiant.HEATER_ARad(L, pd['pk1'], Nprad, Npconv, Npasses, Do)
    Qrad = Calculations_FIRED_HEATER_Q_oil.HEATER_Qoil(pd['Moil'], pd['To_oil'], Tc, pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3']) / (1 - pd['percent_loss_Rad'])
    flux = Qrad/Arad
    fun_val = pd['Flux_Max'] - flux
    return fun_val


    #-------------------------
    # brentq method in Scipy
    #-------------------------
    def Tfb_diff(Tc):
        global Qrad_final, Tfb_final, Tw_final, Ts_final, Mgas_final

        Qrad = Calculations_FIRED_HEATER_Q_oil.HEATER_Qoil(pd['Moil'], pd['To_oil'], Tc, pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3']) / (1 - pd['percent_loss_Rad'])
        Tw = Qrad * (1 - pd['percent_loss_Rad']) / (Urad * Arad) + (pd['To_oil'] + Tc) / 2

        def f_Tfb_rad(Tfb):
            Ems = (pd['e_c1'] * Tfb + pd['e_c2'] * Factor_PL + pd['e_c3'] * Factor_PL**2 + pd['e_c4'])
            F_ex_p = Ems * (A / (alpha * Acp) - 1)
            F_ex = (
                pd['f_c1'] * np.log(Ems) +
                (pd['f_c2'] / Ems + pd['f_c3']) * F_ex_p +
                pd['f_c4'] * np.exp(Ems) +
                pd['f_c5'] * (F_ex_p)**1.5 +
                pd['f_c6']
            )   
            return alpha * Acp * pd['sigma'] * ((Tfb + 460.67)**4 - (Tw + 460.67)**4) * F_ex + pd['hgr'] * Arad * (Tfb - Tw) - Qrad * (1 - pd['percent_loss_Rad'])

        Tfb_rad = fsolve(f_Tfb_rad, Tw + 150)[0]

        Mgas = Qrad / (cp_gas * (pd['Tflame'] - Tfb_rad))
        Ts = Tfb_rad - (Qoil - Qrad * (1 - pd['percent_loss_Conv'])) / (Mgas * cp_gas)

        def f_Tfb_conv(Tfb):
            Ggas = Mgas / As
            HTCo = 0.091 * (Do * Ggas / pd['mu_gas'])**(-0.25) * C3 * C5 * (df / Do)**0.5 * cp_gas * Ggas * pd['Pr_gas']**(-0.67)
            h1 = 1 / ((1 / HTCo) + pd['rf_gas'])
            mf = (2 * h1 / (pd['k_fin'] * pd['tf']))**0.5
            nuf = (np.exp(2 * mf * Lfe) - 1) / (np.exp(2 * mf * Lfe) + 1) * (1 / (mf * Lfe))
            nut = ((Aot - Aof) / Aot + nuf * (Aof / Aot))
            Uconv = 1 / (Uc1 + Uc2 + (1 + pd['rf_gas'] * HTCo) / (nut * HTCo))

            delta1 = Tfb - Tc
            delta2 = Ts - pd['Ti_oil']
            if delta1 <= 0 or delta2 <= 0:
                return 1e6
            log_term = np.log(delta1 / delta2)
            Qconv_expected = (Qoil - Qrad * (1 - pd['percent_loss_Rad'])) / (1 - pd['percent_loss_Conv'])
            Qconv_calc = (Uconv * Aconv * (delta1 - delta2) / log_term) / (1 - pd['percent_loss_Conv'])
            return Qconv_expected - Qconv_calc

        Tfb_conv = fsolve(f_Tfb_conv, (Ts + Tc) + 50)[0]
        
        # Save final results
        Qrad_final = Qrad
        Tfb_final = Tfb_rad
        Tw_final = Tw
        Ts_final = Ts
        Mgas_final = Mgas

        if Tc == 400 or Tc == 600:
            print(f"[DEBUG] Tc = {Tc}")
            print(f"Tfb_rad  = {Tfb_rad}")
            print(f"Tfb_conv = {Tfb_conv}")
            print("----------")

        return Tfb_rad + Tfb_conv
 
    print("Tfb_diff(400) =", Tfb_diff(400))
    print("Tfb_diff(600) =", Tfb_diff(600))

    # Brentq method to find root (Tc where Tfb_rad = Tfb_conv)
    Tc = brentq(Tfb_diff, 400, 600, xtol=1e-2)

    # Final values after convergence
    print("Tc         : ", Tc)
    print("Tfb        : ", Tfb_final)
    print("Tw         : ", Tw_final)
    print("Ts         : ", Ts_final)
    print("Mgas       : ", Mgas_final)
    print("Qrad       : ", Qrad_final)

    # Calculate solutions
    Qconv = (Qoil - Qrad_final * (1 - pd['percent_loss_Rad']))/(1 - pd['percent_loss_Conv'])
    Qs = Mgas_final * cp_gas * (Ts_final - pd['T_outside'])
    Qn = Qrad_final + Qconv + Qs
    Mfuel = Qn/pd['LHV']
    OP_cost = pd['O_uni'] * Mfuel * pd['OT']
    Total_cost = (OP_cost + Capital_cost)
    print("Qconv      : ", Qconv)
    print("Qs         : ", Qs)
    print("Qn         : ", Qn)    
    print("Mfuel      : ", Mfuel)
    print("OP_cost    : ", OP_cost)
    print("Total_cost : ", Total_cost) 

    return [float(Total_cost)]
   

'''