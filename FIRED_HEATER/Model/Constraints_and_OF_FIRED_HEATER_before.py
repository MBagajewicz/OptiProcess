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

from scipy.optimize import minimize, Bounds
from scipy.optimize import newton_krylov
from scipy.optimize import least_squares
from scipy.optimize import NonlinearConstraint
from scipy.optimize import root
from scipy.optimize import fsolve


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

    #calculations for initial values
    OP_cost_I = Calculations_FIRED_HEATER_OP_cost.HEATER_OP_cost_LB(L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Min'], pd['Ti_oil'], pd['T_outside'], pd['Moil'], pd['Flux_Max'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['To_oil'], pd['LHV'], pd['O_uni'], pd['OT'])
    Total_cost_I = OP_cost_I + Capital_cost
    Mfuel_I = Calculations_FIRED_HEATER_OP_cost.HEATER_Mfeul_LB(L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Min'], pd['Ti_oil'], pd['T_outside'], pd['Moil'], pd['Flux_Max'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['To_oil'], pd['LHV'])
    LMTD_I = 800
    Qrad_UB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_UB(L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Max'], pd['percent_loss_Rad']) 
    #Qrad_LB = Calculations_FIRED_HEATER_Q_radiant.HEATER_Qrad_LB(L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], pd['percent_loss_Rad'])
    Qrad_LB = 5000
    Qrad_I = (Qrad_UB + Qrad_LB)/2
    F_ex_I = (0.1 + 2)/2
    F_ex_p_I = (0.1 + 2)/2 
    Tfb_UB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_UB(pd['Tflame'], L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Flux_Max'], pd['Tfb_Max'])
    Tfb_LB = Calculations_FIRED_HEATER_Tfb.HEATER_Tfb_LB(pd['Tflame'], L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Flux_Min'], pd['Tfb_Min'])
    Tfb_I = (Tfb_UB + Tfb_LB)/2
    Tw_I = (400 + 2000)/2
    Ems_I = (0.2 + 2)/2
    Tc_LB = Calculations_FIRED_HEATER_Tc.HEATER_Tc_LB(pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['To_oil'], pd['Moil'], L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Max'], pd['percent_loss_Rad'])
    Tc_UB = Calculations_FIRED_HEATER_Tc.HEATER_Tc_UB(pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['To_oil'], pd['Moil'], L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], pd['percent_loss_Rad'])
    Tc_I = (Tc_LB + Tc_UB)/2
    Mgas_LB = Calculations_FIRED_HEATER_gas_flow.HEATER_Mgas_LB(L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Min'])
    Mgas_UB = Calculations_FIRED_HEATER_gas_flow.HEATER_Mgas_UB(L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'])
    Mgas_I = (Mgas_LB + Mgas_UB)/2

    Ts_LB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_LB(pd['Tflame'], L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Flux_Min'], pd['Tfb_Min'], pd['hflame'], pd['percent_loss_Conv'], pd['Moil'], pd['To_oil'], pd['Ti_oil'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['Tfb_Max'])
    Ts_UB = Calculations_FIRED_HEATER_Ts.HEATER_Ts_UB(pd['Tflame'], L, pd['pk1'], Nprad, Npconv, Npasses, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Flux_Max'], pd['Tfb_Max'], pd['hflame'], pd['percent_loss_Conv'], pd['Moil'], pd['To_oil'], pd['Ti_oil'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['Tfb_Min'])

    # enforce Ts > Tc for LMTD
    eps    = 1e-6
    min_Ts = Tc_UB + eps              # make Ts always exceeds upper bound of Tc
    Ts_LB  = max(Ts_LB, min_Ts)       # clamp lower bound
    Ts_UB  = max(Ts_UB, Ts_LB + eps)  # ensure upper bound strictly above
    Ts_I   = (Ts_LB + Ts_UB) / 2

    Qconv_LB = Calculations_FIRED_HEATER_Q_conv.HEATER_Qconv_LB(pd['Pr_oil'], pd['k_oil'], Do, pd['Moil'], Npasses, pd['mu_oil'], pd['lf'], pd['tf'], pd['Nf'], pd['rf_oil'], pd['ks'], L, pd['pk1'], Nprad, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Rph, pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'], pd['To_oil'], pd['hflame'], pd['percent_loss_Conv'], pd['Ti_oil'])
    Qconv_UB = Calculations_FIRED_HEATER_Q_conv.HEATER_Qconv_UB(pd['Pr_oil'], pd['k_oil'], Do, pd['Moil'], Npasses, pd['mu_oil'], pd['lf'], pd['tf'], pd['Nf'], pd['rf_oil'], pd['ks'], L, pd['pk1'], Nprad, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Rph, pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'], pd['hflame'], pd['percent_loss_Conv'], pd['To_oil'], pd['Ti_oil'], pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'])
    Qconv_I = (Qconv_LB + Qconv_UB)/2
    Uconv_LB = Calculations_FIRED_HEATER_Uconv.HEATER_Uconv_LB(pd['Pr_oil'], pd['k_oil'], Do, pd['Moil'], Npasses, pd['mu_oil'], pd['lf'], pd['tf'], pd['Nf'], pd['rf_oil'], pd['ks'], L, pd['pk1'], Nprad, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Rph, pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'])
    Uconv_UB = Calculations_FIRED_HEATER_Uconv.HEATER_Uconv_UB(pd['Pr_oil'], pd['k_oil'], Do, pd['Moil'], Npasses, pd['mu_oil'], pd['lf'], pd['tf'], pd['Nf'], pd['rf_oil'], pd['ks'], L, pd['pk1'], Nprad, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Rph, pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'])
    Uconv_I = (Uconv_LB + Uconv_UB)/2
    Uc3_LB = Calculations_FIRED_HEATER_Uconv.HEATER_Uc3_LB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'])
    Uc3_UB = Calculations_FIRED_HEATER_Uconv.HEATER_Uc3_UB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'])
    Uc3_I = (Uc3_LB + Uc3_UB)/2
    HTCo_LB = Calculations_FIRED_HEATER_HTCo.HEATER_HTCo_LB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'])
    HTCo_UB = Calculations_FIRED_HEATER_HTCo.HEATER_HTCo_UB(L, pd['pk1'], Nprad, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Min'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Max'], pd['Tfb_Max'], pd['Pr_gas'])
    HTCo_I = (HTCo_LB + HTCo_UB)/2
    nut_LB = Calculations_FIRED_HEATER_fin_overall.HEATER_nut_LB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'])
    nut_UB = Calculations_FIRED_HEATER_fin_overall.HEATER_nut_UB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'])
    nut_I = (nut_LB + nut_UB)/2
    C1_LB = Calculations_FIRED_HEATER_j_factor.HEATER_C1_LB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'])
    C1_UB = Calculations_FIRED_HEATER_j_factor.HEATER_C1_UB(L, pd['pk1'], Nprad, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Min'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'])
    C1_I = (C1_LB + C1_UB)/2
    j_factor_LB = Calculations_FIRED_HEATER_j_factor.HEATER_j_factor_LB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv)
    j_factor_UB = Calculations_FIRED_HEATER_j_factor.HEATER_j_factor_UB(L, pd['pk1'], Nprad, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Min'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv)
    j_factor_I =(j_factor_LB + j_factor_UB)/2
    Ggas_LB = Calculations_FIRED_HEATER_gas_flow.HEATER_Ggas_LB(L, pd['pk1'], Nprad, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Min'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'])
    Ggas_UB = Calculations_FIRED_HEATER_gas_flow.HEATER_Ggas_UB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'])
    Ggas_I = (Ggas_LB + Ggas_UB)/2
    nuf_LB = Calculations_FIRED_HEATER_fin_efficiency.HEATER_nuf_LB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'])
    nuf_UB = Calculations_FIRED_HEATER_fin_efficiency.HEATER_nuf_UB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'])
    nuf_I = (nuf_LB + nuf_UB)/2
    mf_LB = Calculations_FIRED_HEATER_fin_efficiency.HEATER_mf_LB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'])
    mf_UB = Calculations_FIRED_HEATER_fin_efficiency.HEATER_mf_UB(L, pd['pk1'], Nprad, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Min'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Max'], pd['Tfb_Max'], pd['Pr_gas'], pd['rf_gas'], pd['k_fin'])
    mf_I = (mf_LB + mf_UB)/2
    h1_LB = Calculations_FIRED_HEATER_fin_efficiency.HEATER_h1_LB(L, pd['pk1'], Nprad, Do, pd['Flux_Max'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Max'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Min'], pd['Tfb_Min'], pd['Pr_gas'], pd['rf_gas'])
    h1_UB = Calculations_FIRED_HEATER_fin_efficiency.HEATER_h1_UB(L, pd['pk1'], Nprad, Do, pd['Flux_Min'], pd['percent_loss_Rad'], pd['Tflame'], pd['Tfb_Min'], Npconv, Npasses, pd['lf'], Rph, pd['Nf'], pd['tf'], pd['mu_gas'], Nrconv, Rpv, pd['Flux_Max'], pd['Tfb_Max'], pd['Pr_gas'], pd['rf_gas'])
    h1_I = (h1_LB + h1_UB)/2
    Qs_I = Mgas_LB * cp_gas * (Ts_LB - pd['T_outside'])
    Qn_I = Qrad_LB + Qconv_LB + Qs_I

    print("--Urad and Arad--")
    print(Urad)
    print(Arad)
    print("------------------")
    # System of equations for fired heater model
    def HEATER_MODEL(var):
        # list of variables
        LMTD, Qrad, Qconv, Qs, Qn, Mgas, Ggas, Tfb, Tw,  Tc, Ts, F_ex, F_ex_p, Ems, Uconv, HTCo, nut, nuf, mf, h1 = var

        # equations
        UB1 = Qrad*(1-pd['percent_loss_Rad']) - (alpha * Acp * F_ex * pd['sigma'] *(np.power(Tfb+460.67,4)-np.power(Tw+460.67,4)) + Arad * pd['hgr']*(Tfb-Tw))
        UB2 = F_ex_p -  Ems *(A/(alpha*Acp) - 1)
        UB3 = F_ex - (pd['f_c1'] * np.log(Ems) + (pd['f_c2']/Ems+pd['f_c3'])*F_ex_p + pd['f_c4'] * np.exp(Ems) + pd['f_c5']*np.power(F_ex_p,1.5) + pd['f_c6'])
        UB4 = Ems -(pd['e_c1'] * Tfb + pd['e_c2'] * Factor_PL + pd['e_c3'] * np.power(Factor_PL,2) + pd['e_c4'])
        UB5 = Qrad*(1-pd['percent_loss_Rad']) - Calculations_FIRED_HEATER_Q_oil.HEATER_Qoil(pd['Moil'], pd['To_oil'], Tc, pd['Enthoil_c1'], pd['Enthoil_c2'], pd['Enthoil_c3'])
        UB6 = Qrad*(1-pd['percent_loss_Rad']) - Urad * Arad * ( Tw - (pd['To_oil'] + Tc)/2)
        UB7 = Qrad*(1-pd['percent_loss_Rad']) - Mgas * cp_gas*(pd['Tflame']-Tfb) 
        UB8 = Qconv*(1-pd['percent_loss_Conv']) - Mgas * cp_gas*(Tfb - Ts)
        UB9 = Qoil - (Qconv *(1-pd['percent_loss_Conv']) + Qrad*(1-pd['percent_loss_Rad']))
        UB10 = LMTD - Calculations_HEX_LMTD.HEX_lmtd(Tfb, Ts, pd['Ti_oil'], Tc)
        UB11 = Qconv*(1-pd['percent_loss_Conv']) - Uconv * Aconv * LMTD 
        #Uc3 = ( 1 + pd['rf_gas'] * HTCo )/(nut*HTCo)
        UB12 = Uconv - 1/(Uc1 + Uc2 + ( 1 + pd['rf_gas'] * HTCo )/(nut*HTCo))
        #C1 = 0.091 * np.power(Do * Ggas /pd['mu_gas'] , -0.25)
        UB13 = Ggas - Mgas/As
        #j_factor = 0.091 * np.power(Do * Ggas /pd['mu_gas'] , -0.25) * C3 * C5 * np.power(df/Do, 0.5)
        UB14 = HTCo - 0.091 * np.power(Do * Ggas /pd['mu_gas'] , -0.25) * C3 * C5 * np.power(df/Do, 0.5) * cp_gas * Ggas * np.power(pd['Pr_gas'], -0.67)
        UB15 = nut - ((Aot - Aof )/ Aot + nuf *( Aof / Aot))
        UB16 = nuf - (np.exp(2*mf*Lfe) - 1 )/(np.exp(2*mf*Lfe)+1) * (1/(mf*Lfe))
        UB17 = mf - np.power(2*h1 /( pd['k_fin'] * pd['tf']), 0.5)
        #UB18 = h1 - 1 /( (1/HTCo) + pd['rf_gas'] )
        UB18 = HTCo - ( h1 + pd['rf_gas']*HTCo*h1 )
        UB19 = Qs - Mgas * cp_gas * (Ts - pd['T_outside'])
        UB20 = Qn - (Qrad + Qconv + Qs)

        #return [UB1, UB2, UB3, UB4, UB5, UB6, UB7, UB8, UB9, UB10, UB11, UB12, UB13, UB14, UB15, UB16, UB17, UB18]
        # pack into list
        residuals = [UB1, UB2, UB3, UB4, UB5, UB6, UB7, UB8, UB9, UB10,
                    UB11, UB12, UB13, UB14, UB15, UB16, UB17, UB18, UB19, UB20
                    ]
      
        return np.array([float(v) for v in residuals])


    #--------------------------------------------------
    # Initials, Lower and upper bounds of variables
    #--------------------------------------------------
    # initial values
    initial_values = [
        864.3984,   #LMTD_I, 
        14055.8306, #Qrad_I, 
        7194.1696,  #Qconv_I, 
        7245.9005,  #Qs_I, 
        28495.9007, #Qn_I
        24.9125,    #Mgas_I, 
        0.3867,     #Ggas_I, 
        1766.5870,  #Tfb_I, 
        1395.0427,  #Tw_I,  
        491.9876,   #Tc_I, 
        933.3528,   #Ts_I, 
        0.6411,     #F_ex_I,
        0.4408,     #F_ex_p_I, 
        0.5357,     #Ems_I,
        0.0002,     #Uconv_I, 
        0.001,      #HTCo_I, 
        0.9192,     #nut_I, 
        0.9148,     #nuf_I, 
        5.3814,     #mf_I, 
        0.0010,     #h1_I
        ]

    # initial values need to be scalar
    initial_values = [
        x.item() if isinstance(x, _np.ndarray) else x
        for x in initial_values]

    # lower bounds
    lower_bounds = [
        LMTD_I - 400,
        10000,           # Qrad_LB
        Qconv_LB,  
        Qs_I,
        20000,          # Qn_LB 
        Mgas_LB, 
        0.3,            # Ggas_LB
        pd['To_oil']+5, # Tfb_LB,
        800,            # 7 Tw
        Tc_LB, 
        pd['Ti_oil']+5,       # Ts_LB, 
        0,              # 4 F_ex
        0,              # 5 F_ex_p
        0.01,           # 8 Ems
        Uconv_LB, 
        HTCo_LB,
        nut_LB,      
        nuf_LB, 
        mf_LB, 
        h1_LB
        ]
    
    lower_bounds = [
        x.item() if isinstance(x, _np.ndarray) else x
        for x in lower_bounds]
    
   # upper bounds
    upper_bounds = [
        1200,        # 3 LMTD
        20000,      # Qrad_UB,     
        np.inf,      # Qconv_UB,    #13 Qconv
        Qrad_UB+Qconv_UB,      #24 Qs
        60000,        # Qn_UB
        Mgas_UB,     # Mgas
        0.4,         # Ggas_UB
        np.inf,      # Tfb_UB,      # 7 Tfb
        2000,        # 8 Tw
        Ts_UB,       # 12 Ts
        pd['To_oil'],# Tc_UB,       #10  Tc
        np.inf,      # 5 F_ex
        np.inf,      # 6 F_ex_p
        1,           # 9 Ems
        np.inf,      # Uconv_UB,    #14 Uconv
        np.inf,      # HTCo_UB,     #16 HTCo
        np.inf,      # nut_UB,      #17 nut
        np.inf,      # nuf_UB,      #21 nuf
        np.inf,      # mf_UB,       #22 mf
        np.inf      # h1_UB,       #23 h1
        ]
    
    upper_bounds = [
        x.item() if isinstance(x, _np.ndarray) else x
        for x in upper_bounds]

    # variable names
    var_names = [
        'LMTD', 'Qrad', 'Qconv', 'Qs', 'Qn', 
        'Mgas', 'Ggas', 'Tfb', 'Tw', 'Tc', 'Ts',
        'F_ex', 'F_ex_p', 'Ems',  'Uconv',
        'HTCo', 'nut', 'nuf', 'mf', 'h1'
    ]

    # EXPERIMENT : FIXING variables for checking the HEATER_MODEL
    # -----------------------------------------
    LMTD_fixed = 864.3984
    Qrad_fixed = 14055.8306 
    Qconv_fixed = 7194.1696 
    Qs_fixed = 7245.9005
    Qn_fixed = 28495.9007
    Mgas_fixed = 24.9125 
    Tfb_fixed = 1766.5870 
    Tw_fixed = 1395.0427  
    Tc_fixed = 491.9876 
    Ts_fixed = 933.3528 
    mf_fixed = 5.3814   

    eps = 1e-8
    
    lower_bounds[0] = LMTD_fixed - eps
    lower_bounds[0] = LMTD_fixed + eps
    lower_bounds[1] = Qrad_fixed - eps
    upper_bounds[1] = Qrad_fixed + eps
    lower_bounds[2] = Qconv_fixed - eps
    upper_bounds[2] = Qconv_fixed + eps
    lower_bounds[3] = Qs_fixed - eps
    upper_bounds[3] = Qs_fixed + eps
    lower_bounds[4] = Qn_fixed - eps
    upper_bounds[4] = Qn_fixed + eps
    lower_bounds[5] = Mgas_fixed - eps
    upper_bounds[5] = Mgas_fixed + eps
    lower_bounds[7] = Tfb_fixed - eps
    upper_bounds[7] = Tfb_fixed + eps
    #lower_bounds[8] = Tw_fixed - eps
    #upper_bounds[8] = Tw_fixed + eps
    lower_bounds[9] = Tc_fixed - eps
    upper_bounds[9] = Tc_fixed + eps
    lower_bounds[10] = Ts_fixed - eps
    upper_bounds[10] = Ts_fixed + eps
    lower_bounds[18] = mf_fixed - eps
    upper_bounds[18] = mf_fixed + eps
    #-----------------------------------------------------



    #-----------------------------------------------------
    # Solve the system of equation using Scipy optimize
    #-----------------------------------------------------

    # Clip the initial guess to ensure it lies within the specified lower and upper bounds
    x0 = np.clip(initial_values, lower_bounds, upper_bounds) 

    min_result = least_squares(
        HEATER_MODEL,
        x0=x0,                                  # clipped initial guess for the variables
        bounds=(lower_bounds, upper_bounds),    # enforce variable bounds during the solve
        xtol=1e-12,                             # tolerance for changes in the solution vector x
        ftol=1e-12,                             # tolerance for changes in the cost function (sum of squares)
        gtol=1e-12,                             # tolerance for the gradient norm (first-order optimality)
        #jac='2-point',                          # use a two-point finite-difference approximation for the Jacobian
        verbose=0                               # suppress iteration output
        )


    print("|-------------:|--------------:|-------------:|")
    print("|     least_squares result  (Scipy)           |")
    print("|-------------:|--------------:|-------------:|")
    print(min_result)
    print(min_result.fun)
    print(min_result.cost)

    # Define Bounded HEATE_MODEL 
    def Bounded_HEATER(x):
        x_bounded = np.minimum(np.maximum(x, lower_bounds), upper_bounds)
        return np.asarray(HEATER_MODEL(x_bounded))
    
    # Using root
    root_result = root(
        Bounded_HEATER,     # HEATER_MODEL(x) -> residual 벡터 반환
        min_result.x,       # least_squares 해를 초기 guess로
        method='lm', #'hybr',
        options={'xtol': 1e-5, 'maxfev': 1000}
    )

    solution = root_result.x
    
    print("|-------------:|--------------:|-------------:|")
    print("|     root result (Scipy)                     |")
    print("|-------------:|--------------:|-------------:|")
    print(root_result)
    print(root_result.fun)
    print(Bounded_HEATER(solution))

    # Print variable solutions
    # 1. Print Markdown header
    print("|-------------:|--------------:|--------------:|--------------:|-------------:|")
    print("| Variable     | Lower Bound   | Upper Bound   | Initial Value |    Result    |")
    print("|-------------:|--------------:|--------------:|--------------:|-------------:|")
    # 2. Print each row in aligned columns
    for name, lb, ub, iv, res in zip(var_names, lower_bounds, upper_bounds, initial_values , solution):
        print(f"| {name:<12s} | {lb:13.6g} | {ub:13.6g} | {iv:13.6g} | {res:12.6g} |")
    print("|-------------:|--------------:|--------------:|--------------:|-------------:|")

    # store the variable results for the constraints of the smart enumeration
    pd['Result_Qrad'] = solution[1]

    # Calculate the operating cost and total cost
    Mfuel = solution[4]/pd['LHV']
    OP_cost = pd['O_uni'] * Mfuel * pd['OT']
    Total_cost = (OP_cost + Capital_cost)
    print("Mfuel : ", Mfuel)
    print("OP_cost : ", OP_cost)

    OF_Solution = Total_cost

    return [float(OF_Solution)]




'''
    # newton_krylov
    #root_result = newton_krylov(
    #    Bounded_HEATER,
    #    min_result.x,
    #    method='lgmres',      # 또는 선호하는 Krylov solver
    #    inner_tol=1e-5,      # Krylov 내부 루프 수렴 허용오차
    #   inner_maxiter=200     # Krylov 내부 반복 최대 횟수
    #   #outer_maxiter=50     # (선택) 외부 Newton–Krylov 반복 최대 횟수
    #)



        # -----------------------------------------------------------------------
        # Safe numerical functions to avoid overflow, division by zero, and NaNs
        # -----------------------------------------------------------------------
        def safe_exp(x, maxval=700): # Safe exponential function to prevent overflow
            return np.exp(np.clip(x, None, maxval))

        def safe_log(x, minval=1e-6): # Safe logarithm function to avoid log(0) or log of negative values
            return np.log(np.clip(x, minval, None))

        def safe_div(num, denom, minval=1e-6): # Safe division function to prevent division by zero or near-zero values
            return num / np.clip(denom, minval, None)
        # -----------------------------------------------------------------------

        # Stabilized UB3 – Prevents overflow and log(0) errors via safe_log and safe_exp
        #UB3 = F_ex - (pd['f_c1'] * safe_log(Ems) + (pd['f_c2']/safe_div(1, Ems) + pd['f_c3']) * F_ex_p +
        #        pd['f_c4'] * safe_exp(Ems) + pd['f_c5'] * np.power(F_ex_p, 1.5) + pd['f_c6'])
        
        # Stabilized UB16 – Prevents division by zero or overflow in exponential terms
        mf_Lfe = safe_div(mf * Lfe, 1)
        exp2mfLfe = safe_exp(2 * mf * Lfe)
        #UB16 = nuf - ((exp2mfLfe - 1) / (exp2mfLfe + 1)) * (1 / mf_Lfe)

        # Stabilized UB17 – Prevents division by zero inside square root
        #UB17 = mf - np.sqrt(safe_div(2 * h1, (pd['k_fin'] * pd['tf'])))

        # Stabilized UB18 – Prevents division by zero in HTCo calculation
        #UB18 = h1 - 1 / (safe_div(1, HTCo) + pd['rf_gas'])

        # Stabilized UB19 –  Uses relative error form to improve numerical stability
        #ideal_Qs = Mgas * cp_gas * (Ts - pd['T_outside'])
        #UB19 = (Qs - ideal_Qs) / (abs(ideal_Qs) + 1e-6)




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
    flux = pd['Result_Qrad']/Arad
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
    flux = pd['Result_Qrad']/Arad
    fun_val = pd['Flux_Max'] - flux
    return fun_val
'''

# endregion
##################################################################################################################

