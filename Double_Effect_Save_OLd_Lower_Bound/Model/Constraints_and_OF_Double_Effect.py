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
    Calculations_DC_Costs,
    Calculations_DC_Reflux_Drum
)

from OptiCode import Next_Level_Organizer
#endregion
##################################################################################################################

##################################################################################################################
#region Functions

# ----------------------------------------------------------------------------------------------------------------
# Trimming Functions
# ----------------------------------------------------------------------------------------------------------------
def ST_Triang(Nf_c,Ns_c,m_p): # Allows only candidates with Nf <= Ns-2 = Nt-1
    fun_val = Nf_c - Ns_c + 2
    return fun_val

def ST_Ns0(Nf_c,Ns_c,m_p): # Allows only candidates with Ns >= Nsmin (where Nsmin is the minimum of the search, not necessarily the minimum required for the separation task)
    fun_val = m_p['Nsmin'] - Ns_c
    return fun_val

# ----------------------------------------------------------------------------------------------------------------
# Objective Function
# ----------------------------------------------------------------------------------------------------------------
# Column Design + Plate Design
def TAC_OF(Nf_c,Ns_c,m_p):

    # Running Aspen simulation:
    print(f'Running Aspen simulation for candidate with Ns = {Ns_c[0]} and Nf = {Nf_c[0]}')
    results = Calculations_DC_Aspen.fun_run_Aspen(Ns_c[0], Nf_c[0], m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'], m_p)

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
        CAPEX_REB = Calculations_DC_Costs.CAPEX_Shell_and_Tube(Reb_area) 
        #CAPEX_REB = Calculations_DC_Costs.CAPEX_Kettle(Reb_area)  # Originally used Kettle, but now using Shell and Tube for consistency
        print(f'-------CAPEX_REB LPC = {CAPEX_REB:.2f}') 

        # High Pressure Column solver: --> Tomazim
        #results = Calculations_DC_Aspen.fun_getfromAspen(m_p['Aspen_engine'], m_p['block_name'][0], m_p['block_name'][0], m_p['stream_names'][1], Ns_c[0], m_p['Comp_name'],m_p['Nc'])
        Solution_within = Next_Level_Organizer.Next_Level(results, m_p)
        HPCol_Solution = Solution_within['Equipment1']
        TAC_COL_HPCol = HPCol_Solution['TAC_OF']['TAC']
        print(f'-------TAC (HPCol) = {TAC_COL_HPCol:.2f}')

        # Low Pressure Column solver: --> Tomazim
        Dc = Calculations_DC_Column_Sizing.f_Diameter(m_p['lt'], results['liquid_mass_density'], results['vapor_mass_density'],results['maximum_vapor_flow'])
        Nt = (Ns_c[0] - 2)
        Wshell = Calculations_DC_Column_Sizing.f_Wshell(m_p['lt'], Nt, Dc, m_p['roshell'])
        CAPEX_COL_LPCol = Calculations_DC_Costs.fun_CAPEX_Col(Wshell,Dc,Nt)
        
        CAPEX_COL = CAPEX_COL_LPCol 

        # Reflux Drum CAPEX:
        RD_L_mass_flow = results['liquid_mass_flows'][0] + results['mass_distillate_rate']
        RD_L_mass_density = results['distillate_liquid_mass_density'] 
        RD_Volume = Calculations_DC_Reflux_Drum.fun_RD_Vol(RD_L_mass_flow, RD_L_mass_density,m_p['TRL_min'])
        RD_D, RD_L = Calculations_DC_Reflux_Drum.fun_L_D(RD_Volume,m_p['L_D'])
        CAPEX_RD = Calculations_DC_Costs.fun_CAPEX_Reflux_Drum(RD_L, RD_D, m_p['roshell'])

        # Calculating OPEX Cost:
        Cooling_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Ccw'],results['condenser_duty'],m_p['hours'])
        Heating_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Clpst'],results['reboiler_duty'],m_p['hours'])
        OPEX_COL = Cooling_Cost + Heating_Cost

        # Caculting Candidate TAC:
        #TAC = [(1/m_p['Pb'])*(CAPEX_COL + CAPEX_COND + CAPEX_REB + CAPEX_RD) + OPEX_COL] # Low Pressure Column TAC 
        TAC_COL_LPCol = [(1/m_p['Pb'])*(CAPEX_COL + CAPEX_COND + CAPEX_RD) + OPEX_COL] # Low Pressure Column TAC - CAPEX_REB (because is the same as HPCol condenser)
        print(f'-------TAC (LPCol) = {TAC_COL_LPCol[0]:.2f}')
        TAC = [TAC_COL_LPCol[0] + TAC_COL_HPCol]  # Adding High Pressure Column TAC 
        print(f'-------TAC (LPCol + HPCol) = {TAC[0]:.2f}')


    else:
        TAC = [np.nan]
        Solution_within = {}
    print(f'TAC = {TAC[0]:.2f}')

    # print('CAPEX_COND:', CAPEX_COND)
    # print('CAPEX_REB:', CAPEX_REB)
    # print('Cooling_Cost:', Cooling_Cost)
    # print('Heating_Cost:', Heating_Cost)
    # print('OPEX_COL:', OPEX_COL)

    return [TAC, Solution_within]

# ----------------------------------------------------------------------------------------------------------------
# Lower Bound Function
# ----------------------------------------------------------------------------------------------------------------
def LB_Gen(Nf_c,Ns_c,m_p):

    # Guide line results and LB storage
    GD_results = {}
    GD_HE_TAC = {}
    GD_TAC = {}
    GD_HPCol_Solution = {}
    GD_Solution_Within = {}
    GD_Dc = {}

    # Identifying search space:
    Nsmax = np.nanmax(Ns_c)
    Nsmin = np.nanmin(Ns_c)
    Nfmin = np.nanmin(Nf_c)
    Nfmax = np.nanmax(Nf_c)

    # Solving guide line (where Ns = Nsmax)
    print(f'Starting to solve line of candidates with Ns = {Nsmax}')
    for Nf in range(Nfmin,Nfmax+1):    # For Nf from Nfmin to Nsmax - 2

        # Solve candidate on Aspen Plus:
        GD_results[Nf] = Calculations_DC_Aspen.fun_run_Aspen(Nsmax, Nf, m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'],m_p)
        
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

            # Retrieving Low Pressure Column results from Aspen:
            GD_results[Nf] = Calculations_DC_Aspen.fun_getfromAspen(m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'][1], Ns_c[0], m_p['Comp_name'],m_p['Nc'])

            # Running High Pressure Column Design:
            GD_Solution_Within[Nf] = Next_Level_Organizer.Next_Level(GD_results[Nf],m_p)
            GD_HPCol_Solution[Nf] = GD_Solution_Within[Nf]['Equipment1']
            TAC_COL_HPCol = GD_HPCol_Solution[Nf]['TAC_OF']['TAC'] # Old version --- run the entire HPCol
            #Adding minimum CAPEX_REB of Nsmax of HPCol as lower bound TAC of HPCol
            #TAC_COL_HPCol = GD_HPCol_Solution[Nf]['LB_Gen']['TAC_best'] # New version --- run just the Lower Bound of HPCol

        
            # Column CAPEX:
            GD_Dc[Nf] = Calculations_DC_Column_Sizing.f_Diameter(m_p['lt'], GD_results[Nf]['liquid_mass_density'], GD_results[Nf]['vapor_mass_density'],GD_results[Nf]['maximum_vapor_flow'])
            Ntmax = (Nsmax - 2)
            Wshell = Calculations_DC_Column_Sizing.f_Wshell(m_p['lt'], Ntmax, GD_Dc[Nf], m_p['roshell'] )
            CAPEX_COL_LPCol = Calculations_DC_Costs.fun_CAPEX_Col(Wshell, GD_Dc[Nf], Ntmax)
            
            CAPEX_COL = CAPEX_COL_LPCol 

            # Reflux Drum CAPEX:
            RD_L_mass_flow = GD_results[Nf]['liquid_mass_flows'][0] + GD_results[Nf]['mass_distillate_rate']
            RD_L_mass_density = GD_results[Nf]['distillate_liquid_mass_density'] 
            RD_Volume = Calculations_DC_Reflux_Drum.fun_RD_Vol(RD_L_mass_flow, RD_L_mass_density, m_p['TRL_min'])
            RD_D, RD_L = Calculations_DC_Reflux_Drum.fun_L_D(RD_Volume,m_p['L_D'])
            CAPEX_RD = Calculations_DC_Costs.fun_CAPEX_Reflux_Drum(RD_L, RD_D, m_p['roshell'])
            
            # Calculating Candidate TAC:
            #GD_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_COL + CAPEX_COND + CAPEX_REB + CAPEX_RD) + OPEX_COL # Low Pressure Column TAC
            GD_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_COL + CAPEX_COND + CAPEX_RD) + OPEX_COL # Low Pressure Column TAC - CAPEX_REB (because is the same as HPCol condenser)
            GD_TAC[Nf] = GD_TAC[Nf] + TAC_COL_HPCol  # Adding High Pressure Column TAC to the list
            GD_HE_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_COND + CAPEX_REB + CAPEX_RD) + OPEX_COL
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
