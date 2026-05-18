###################################################################################################################
#region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming 
# methodology 
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.1          20-Nov-2024     Miguel Bagajewicz         Proposed 
#   0.2          05-Fev-2025     Alice Peccini             Sieve Tray
#   0.3          28-Feb-2025     Alice Peccini             Relocating folders 
##################################################################################################################
# INPUT: Define Constraints as def and return + or - values depending the > or < inequality
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def) that need to be declared on Example_Repository in 
# ExampleX['EquipmentY']['Model_Declarations']
#endregion
############################################################################################

##################################################################################################################
#region Import Library
import numpy as np
from math import pi
from STRAY.Calculations import (
Calculations_STRAY_Col_Mass,
Calculations_STRAY_Geometry,
Calculations_STRAY_DC_backup,
Calculations_STRAY_Entrainment,
Calculations_STRAY_Flooding,
Calculations_STRAY_Residence_time,
Calculations_STRAY_Weeping,
Calculations_STRAY_Tray_Mass
)

from Commom_Equations_DC import (
    Calculations_DC_Column_Sizing,
    Calculations_DC_Costs
)

#endregion
##################################################################################################################

##################################################################################################################
#region BTEX_Column_1=

# ---------------------------------------------------------------------------------------------------------------- 
# Trimming Functions - Geometric Constraints
# ----------------------------------------------------------------------------------------------------------------

# The weir legnth must be limited to the column diameter:
def f_lw_Dc(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    fun_val = lw - Dc + 1e-5
    return fun_val

# The hole pitch must be equal to or greater than twice the hole diameter: 
def f_lp_dh(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    fun_val = 2*dh - lp + 1e-5
    return fun_val

# The thickness must be limited by the hole diamete:
def f_dh_tt(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    fun_val = 1 - (dh/tt)
    return fun_val

# The ratio of the hole area to the active area is bounded (upper bound):
def f_Ah_Aa_UB(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    Ah = Calculations_STRAY_Geometry.f_Ah(lw, Dc, pd['wczin'], pd['wczout'], dh, lp, lay)
    Aa = Calculations_STRAY_Geometry.f_Aa(lw, Dc, pd['wczin'], pd['wczout'])
    fun_val = (Ah/Aa) - 0.16
    return fun_val

# The ratio of the hole area to the active area is bounded (lower bound):
def f_Ah_Aa_LB(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    Ah = Calculations_STRAY_Geometry.f_Ah(lw, Dc, pd['wczin'], pd['wczout'], dh, lp, lay)
    Aa = Calculations_STRAY_Geometry.f_Aa(lw, Dc, pd['wczin'], pd['wczout'])
    fun_val = 0.06 - (Ah/Aa)
    return fun_val

# To use the Fair flooding correlation, the following constraint holds:
def f_hw_lt(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    fun_val = hw - (0.15*lt)
    return fun_val

# ---------------------------------------------------------------------------------------------------------------- 
# Trimming Functions - Operational Constraints
# ----------------------------------------------------------------------------------------------------------------

# Operational Constraints need to pass for each tray, for a candidate to pass fun_val needs to be <= 0
# So I kind of did a ST here inside each function. 

# First I generate a boolean array of the length of the number of candidates, filled with 'True' values 
# aux1 = np.ones(X.shape,dtype=bool)
# Then, I check each candidate for the first tray
# aux2 = fun_val for a given tray
# Then I update aux1 leaving True only for candidates that are feasible for that tray
# aux1 *= (aux2 <=0)
# Then, I run a loop for all the remaing trays and do the same, but only checking still remaining viable candidates
# At the end, aux1 is only True for candidates which were viable at all trays

# FLOODING
def f_un_uflood(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    un = Calculations_STRAY_Flooding.f_un(lw, Dc, pd['Vw'][0], pd['rov'][0])
    uflood = Calculations_STRAY_Flooding.f_uflood(lw, Dc, pd['wczin'], pd['wczout'], dh, lp, lay, pd['Lw'][0], pd['Vw'][0], pd['rol'][0], pd['rov'][0], lt, pd['sig'][0])
    aux1 = np.ones(un.shape,dtype=bool) # Create a boolean array of the same shape as 'un', filled with 'True' values
    aux2 = un - 0.85*uflood
    aux1 *= (aux2 <=0)
    for i in range(1,len(pd['Lw'])):
        un[aux1] = Calculations_STRAY_Flooding.f_un(lw[aux1], Dc[aux1], pd['Vw'][i], pd['rov'][i])
        uflood[aux1] = Calculations_STRAY_Flooding.f_uflood(lw[aux1], Dc[aux1], pd['wczin'], pd['wczout'], dh[aux1], lp[aux1], lay[aux1], pd['Lw'][i], pd['Vw'][i], pd['rol'][i], pd['rov'][i], lt[aux1], pd['sig'][i])
        aux2[aux1] = un[aux1] - 0.85*uflood[aux1]
        aux1 *= (aux2 <= 0)
    fun_val = np.ones(un.shape)
    fun_val[aux1] = -1
    return fun_val

# ENTRAINMENT
def f_psi_snt(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    psi = Calculations_STRAY_Entrainment.f_Psi(lw, Dc, pd['Vw'][0], pd['rov'][0], pd['wczin'], pd['wczout'], dh, lp, lay, pd['Lw'][0], pd['rol'][0], lt, pd['sig'][0])
    aux1 = np.ones(psi.shape,dtype=bool)
    aux2 = psi - 0.1
    aux1 *= (aux2 <= 0)
    for i in range(1,len(pd['Lw'])):
        psi[aux1] = Calculations_STRAY_Entrainment.f_Psi(lw[aux1], Dc[aux1], pd['Vw'][i], pd['rov'][i], pd['wczin'], pd['wczout'], dh[aux1], lp[aux1], lay[aux1], pd['Lw'][i], pd['rol'][i], lt[aux1], pd['sig'][i])
        aux2[aux1] = psi[aux1] - 0.1
        aux1 *= (aux2 <= 0)
    fun_val = np.ones(psi.shape)
    fun_val[aux1] = -1
    return fun_val

# WEEPING
def f_uh_uhmin(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    uh = Calculations_STRAY_Weeping.f_uh(lw, Dc, pd['wczin'], pd['wczout'], dh, lp, lay, pd['Vw'][0], pd['rov'][0])
    uhmin = Calculations_STRAY_Weeping.f_uhmin(lw, pd['Lw'][0], pd['rol'][0], hw, dh, pd['rov'][0])
    aux1 = np.ones(uh.shape,dtype=bool)
    aux2 = uhmin - uh
    aux1 *= (aux2 <= 0)
    for i in range(1,len(pd['Lw'])):
        uh[aux1] = Calculations_STRAY_Weeping.f_uh(lw[aux1], Dc[aux1], pd['wczin'], pd['wczout'], dh[aux1], lp[aux1], lay[aux1], pd['Vw'][i], pd['rov'][i])
        uhmin[aux1] = Calculations_STRAY_Weeping.f_uhmin(lw[aux1], pd['Lw'][i], pd['rol'][i], hw[aux1], dh[aux1], pd['rov'][i])
        aux2[aux1] = uhmin[aux1] - uh[aux1]
        aux1 *= (aux2 <= 0)
    fun_val = np.ones(uh.shape)
    fun_val[aux1] = -1
    return fun_val

# DOWNCOMER
def f_hb_lt_hw(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    hb = Calculations_STRAY_DC_backup.f_hb(lw, Dc, pd['wczin'], pd['wczout'], dh, lp, lay, pd['Vw'][0], pd['rov'][0], tt, pd['rol'][0], pd['Lw'][0], hw, hdwap)
    aux1 = np.ones(hb.shape,dtype=bool)
    aux2 = hb - (1/2)*(lt + hw)
    aux1 *= (aux2 <= 0)
    for i in range(1,len(pd['Lw'])):
        hb[aux1] = Calculations_STRAY_DC_backup.f_hb(lw[aux1], Dc[aux1], pd['wczin'], pd['wczout'], dh[aux1], lp[aux1], lay[aux1], pd['Vw'][i], pd['rov'][i], tt[aux1], pd['rol'][i], pd['Lw'][i], hw[aux1], hdwap[aux1])
        aux2[aux1] = hb[aux1] - (1/2)*(lt[aux1] + hw[aux1])
        aux1 *= (aux2 <= 0)
    fun_val = np.ones(hb.shape)
    fun_val[aux1] = -1
    return fun_val

# RESIDENCE TIME
def f_rtime(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    time = Calculations_STRAY_Residence_time.f_time(lw, Dc, pd['wczin'], pd['wczout'], dh, lp, lay, pd['Vw'][0], pd['rov'][0], tt, pd['rol'][0], pd['Lw'][0], hw, hdwap)
    aux1 = np.ones(time.shape,dtype=bool)
    aux2 = 3 - time
    aux1 *= (aux2 <= 0)
    for i in range(1,len(pd['Lw'])):
        time[aux1] = Calculations_STRAY_Residence_time.f_time(lw[aux1], Dc[aux1], pd['wczin'], pd['wczout'], dh[aux1], lp[aux1], lay[aux1], pd['Vw'][i], pd['rov'][i], tt[aux1], pd['rol'][i], pd['Lw'][i], hw[aux1], hdwap[aux1])
        aux2[aux1] = 3 - time[aux1]
        aux1 *= (aux2 <= 0)
    fun_val = np.ones(time.shape)
    fun_val[aux1] = -1
    return fun_val


# ---------------------------------------------------------------------------------------------------------------- 
# Objective Function
# ----------------------------------------------------------------------------------------------------------------

# Option 1: Total cost assuming carbon steel column (minCtotal) 
def Cost_OF(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    Wshell = Calculations_DC_Column_Sizing.f_Wshell(lt, pd['Nt'], Dc, pd['roshell'])
    COL_CAPEX = Calculations_DC_Costs.fun_CAPEX_Col(Wshell, Dc, pd['Nt'])
    return COL_CAPEX

# Option 2: Total mass assuming carbon steel column (minCtotal) 
def Wtotal_OF(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    WColumn = Calculations_STRAY_Col_Mass.f_WColumn(pd['Cw'],pd['roshell'],Dc,lt,pd['Nt'])
    Wtray = Calculations_STRAY_Tray_Mass.f_Wtray(lw, Dc, pd['wczin'], pd['wczout'], dh, lp, lay, tt, pd['rotray'], hw, lt, hdwap)
    Wtotal = WColumn + Wtray*pd['Nt']
    return Wtotal

# Option 3:
def Wshell_OF(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    Wshell = Calculations_DC_Column_Sizing.f_Wshell(lt, pd['Nt'], Dc, pd['roshell'])
    return Wshell

# Option 4:
def dPtotal_OF(Dc, dh, hdwap, hw, lt, lw, lp, tt, lay, pd):
    N_trays = len(pd['Lw'])
    N_candidates = Dc.shape[0]
    ht_tray = np.empty((N_candidates,N_trays))
    for i in range (N_trays):
        ht_tray[:,i] = Calculations_STRAY_DC_backup.f_ht(lw, Dc, pd['wczin'], pd['wczout'], dh, lp, lay, pd['Vw'][i], pd['rov'][i], tt, pd['rol'][i], pd['Lw'][i], hw)
    ht_total = np.sum(ht_tray, axis=1)
    return ht_total
