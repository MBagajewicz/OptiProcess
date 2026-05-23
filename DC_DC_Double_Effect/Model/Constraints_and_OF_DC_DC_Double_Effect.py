###################################################################################################################
#region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming
# methodology
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.1          03-Fev-2025     Alice Peccini             BTX Column
#   0.2          28-Feb-2025     Alice Peccini             Relocating folders
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
from Commom_Equations_DC import (
    Calculations_DC_Aspen,
    Calculations_DC_Column_Sizing,
    Calculations_DC_HEs,
    Calculations_DC_Costs
)

from OptiCode import Next_Level_Organizer
#endregion
##################################################################################################################

##################################################################################################################
#region BTX_Column_1 (Example 5) - Column Design

# ----------------------------------------------------------------------------------------------------------------
# Trimming Functions
# ----------------------------------------------------------------------------------------------------------------
def ST_Triang(Nf_c,Ns_c,m_p): # Allows only candidates with Nf <= Ns-2 = Nt-1
    fun_val = Nf_c - Ns_c + 2
    return fun_val

def ST_Ns0(Nf_c,Ns_c,m_p): # Allows only candidates with Ns >= Nsmin (where Nsmin is the minimum of the search, not necessarily the minimum required for the separation task)
    fun_val = m_p['Nsmin'] - Ns_c
    return fun_val

# Tomazim

def HPCOL_Feasibility (Nf_c,results,m_p):

    # Problems Within Solutions:
    Solution_HPCOL = Next_Level_Organizer.Next_Level(results, m_p)

    m_p1 = Solution_HPCOL['Equipment1'] # equipament 1 - Low Pressure Column
    m_p2 = Solution_HPCOL['Equipment2'] # equipament 2 - High Pressure Column
    fun_val = m_p1['reboiler_duty'] - m_p2['condenser_duty']

    return fun_val



'''
def HPCOL_Feasibility (Nf_c,results,m_p):

    # Problems Within Solutions:
    Solution_HPCOL = Next_Level_Organizer.Next_Level(results, m_p)

    m_p1 = Solution_HPCOL['Equipment1'] # equipament 1 - Low Pressure Column
    m_p2 = Solution_HPCOL['Equipment2'] # equipament 2 - High Pressure Column
   
    #fun_val = reboiler_duty_mp1 + condenser_duty_mp2 = <0  teria que ser >=0
    #fun_val = (reboiler_duty_mp1 + condenser_duty_mp2)*(-1)
    
    if (m_p1['reboiler_duty'] == (m_p2['condenser_duty']*(-1))) :
        fun_val = m_p1['reboiler_duty'] + m_p2['condenser_duty']
    else :
        fun_val = 1e20  # high value penalizing

    return fun_val
'''

# ----------------------------------------------------------------------------------------------------------------
# Objective Function
# ----------------------------------------------------------------------------------------------------------------
# Column Design + Plate Design
def OF_BTX_Column(Nf_c,Ns_c,m_p):

    # Running Aspen simulation:
    print(f'Running Aspen simulation for candidate with Ns = {Ns_c[0]} and Nf = {Nf_c[0]}')
    results = Calculations_DC_Aspen.fun_run_Aspen(Ns_c[0], Nf_c[0], m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'][0], m_p['Comp_name'], m_p['Nc'])

    # If candidate was successfully solved:
    if results:

        # Heat Exchanger Areas:
        Tcin_reb = results['temperatures'][-2]
        Tcout_reb = results['temperatures'][-1]
        Reb_area = Calculations_DC_HEs.fun_HE_areas(m_p['Tlpst'], m_p['Tlpst'], Tcin_reb, Tcout_reb, results['reboiler_duty'], m_p['Ur']) 
        Thin_cond = results['temperatures'][1] 
        Thout_cond = results['temperatures'][0] 
        Cond_area = Calculations_DC_HEs.fun_HE_areas(Thin_cond, Thout_cond, m_p['Tcwin'], m_p['Tcwout'], results['condenser_duty'], m_p['Uc'])

        CAPEX_COND = Calculations_DC_Costs.CAPEX_Shell_and_Tube(Cond_area)
        CAPEX_REB = Calculations_DC_Costs.CAPEX_Kettle(Reb_area)

        # Tray Design solver:
        results['hydraulics'] = Calculations_DC_Aspen.fun_getfromAspen_hydraulics(Ns_c[0], m_p['Aspen_engine'], m_p['block_name'][0])
        Solution_within = Next_Level_Organizer.Next_Level(results, m_p)
        Sieve_Tray_Solution = Solution_within['Equipment1']
        CAPEX_COL = Sieve_Tray_Solution['Cost_OF']['Ctotal']

        # Calculating OPEX Cost:
        Cooling_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Ccw'],results['condenser_duty'],m_p['hours'])
        Heating_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Clpst'],results['reboiler_duty'],m_p['hours'])
        OPEX_COL = Cooling_Cost + Heating_Cost

        # Caculting Candidate TAC:
        OF_Solution = [(1/m_p['Pb'])*(CAPEX_COL + CAPEX_COND + CAPEX_REB) + OPEX_COL]

    else:
        OF_Solution = [np.nan]
    print(f'TAC = {OF_Solution[0]:.2f}')

    return [OF_Solution, Solution_within]

# ----------------------------------------------------------------------------------------------------------------
# Lower Bound Function
# ----------------------------------------------------------------------------------------------------------------
def LB_Gen(Nf_c,Ns_c,m_p):

    # Guide line results and LB storage
    GD_results = {}
    GD_HE_TAC = {}
    GD_TAC = {}
    GD_Sieve_Tray_Solution = {}
    GD_Solution_Within = {}

    # Identifying search space:
    Nsmax = np.nanmax(Ns_c)
    Nsmin = np.nanmin(Ns_c)
    Nfmin = np.nanmin(Nf_c)
    Nfmax = np.nanmax(Nf_c)

    # Solving guide line (where Ns = Nsmax)
    print(f'Starting to solve line of candidates with Ns = {Nsmax}')
    for Nf in range(Nfmin,Nfmax+1):    # For Nf from Nfmin to Nsmax - 2

        # Solve candidate on Aspen Plus:
        GD_results[Nf] = Calculations_DC_Aspen.fun_run_Aspen(Nsmax, Nf, m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'][0], m_p['Comp_name'], m_p['Nc'])

        # Checking feasibility:
        if GD_results[Nf]:

            # Heat Exchanger Areas:
            Tcin_reb = GD_results[Nf]['temperatures'][-2]
            Tcout_reb = GD_results[Nf]['temperatures'][-1]
            Reb_area = Calculations_DC_HEs.fun_HE_areas(m_p['Tlpst'], m_p['Tlpst'], Tcin_reb, Tcout_reb, GD_results[Nf]['reboiler_duty'], m_p['Ur']) 
            Thin_cond = GD_results[Nf]['temperatures'][1] 
            Thout_cond = GD_results[Nf]['temperatures'][0] 
            Cond_area = Calculations_DC_HEs.fun_HE_areas(Thin_cond, Thout_cond, m_p['Tcwin'], m_p['Tcwout'], GD_results[Nf]['condenser_duty'], m_p['Uc'])

            # Heat exchangers costs:
            CAPEX_COND = Calculations_DC_Costs.CAPEX_Shell_and_Tube(Cond_area)
            CAPEX_REB = Calculations_DC_Costs.CAPEX_Kettle(Reb_area)

            # Calculating OPEX Cost:
            Cooling_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Ccw'],GD_results[Nf]['condenser_duty'],m_p['hours'])
            Heating_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Clpst'],GD_results[Nf]['reboiler_duty'],m_p['hours'])
            OPEX_COL = Cooling_Cost + Heating_Cost

            # Retrieving hydraulic results from Aspen:
            GD_results[Nf]['hydraulics'] = Calculations_DC_Aspen.fun_getfromAspen_hydraulics(Nsmax, m_p['Aspen_engine'], m_p['block_name'][0])

            # Running Sieve Tray Design:
            GD_Solution_Within[Nf] = Next_Level_Organizer.Next_Level(GD_results[Nf],m_p)
            GD_Sieve_Tray_Solution[Nf] = GD_Solution_Within[Nf]['Equipment1']
            CAPEX_COL = GD_Sieve_Tray_Solution[Nf]['Cost_OF']['Ctotal']

            # Calculating Candidate TAC:
            GD_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_COL + CAPEX_COND + CAPEX_REB) + OPEX_COL
            GD_HE_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_COND + CAPEX_REB) + OPEX_COL
            print(f'TAC = {GD_TAC[Nf]:.2f}')

        else:
            GD_TAC[Nf] = 1e20

    # Selecting best result found within the guide line:
    TAC_best = min(GD_TAC.values())
    Arg_best = [min(GD_TAC, key=GD_TAC.get), Nsmax]
    Solution_Within_best = GD_Solution_Within.get(Arg_best[0], None)

    print(f'\n **Generating lower bounds for candidates with Ns = {Nsmin} to Ns = {Nsmax - 1}** \n')
    # Using the guide line results to generate candidate's lower bounds:
    Ns_unique = np.unique(Ns_c)  # Get all unique values of Ns_c

    # Dictionaries to store precomputed values
    Wshellmin_dict = {}
    CAPEX_Colmin_dict = {}

    for Ns in Ns_unique:
        Wshellmin_dict[Ns] = Calculations_DC_Column_Sizing.f_Wshell(m_p['ltmin'], Ns-2, m_p['Dcmin'], m_p['roshell'])
        CAPEX_Colmin_dict[Ns] = (1/m_p['Pb'])*Calculations_DC_Costs.fun_CAPEX_Col(Wshellmin_dict[Ns], m_p['Dcmin'], Ns-2)

    # Using the guide line results to generate candidate's lower bounds:
    LB_sol = np.array([
        GD_TAC[Nf] if Ns == Nsmax else
        GD_HE_TAC[Nf] + CAPEX_Colmin_dict[Ns]
        if Nf in GD_HE_TAC and Nf in GD_TAC else 1e20
        for Nf, Ns in zip(Nf_c, Ns_c)
    ])

    return [LB_sol, TAC_best, Arg_best, Solution_Within_best]

#endregion
##################################################################################################################
