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
import os
import pandas as pd
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
    results = Calculations_DC_Aspen.fun_run_Aspen(Ns_c[0], Nf_c[0], m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'],m_p)

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
        CAPEX_COL = Sieve_Tray_Solution['Cost_OF']['COL_CAPEX']

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
        TAC = [(1/m_p['Pb'])*(CAPEX_COL + CAPEX_COND + CAPEX_REB + CAPEX_RD) + OPEX_COL]

    else:
        TAC = [np.nan]
        Solution_within = {}
    print(f'TAC = {TAC[0]:.2f}')

    # print('CAPEX_COND:', CAPEX_COND)
    # print('CAPEX_REB:', CAPEX_REB)
    # print('Cooling_Cost:', Cooling_Cost)
    # print('Heating_Cost:', Heating_Cost)
    # print('OPEX_COL:', OPEX_COL)

        
    # ------------------------------
    # Excel Map - TAC Results
    # Tomazim
    # ------------------------------

    try:
        # Ensure TAC is a valid number
        TAC_value = float(TAC[0]) if not np.isnan(TAC[0]) else np.nan

        # Define search names and ranges
        Ns_val = int(Ns_c[0])
        Nf_val = int(Nf_c[0])

        # Path to the current folder
        folder = os.getcwd()

        # Base name for the file
        base_name = "TAC_Matrix_DC_"

        # Check if previous TAC files already exist
        existing = [f for f in os.listdir(folder) if f.startswith(base_name) and f.endswith(".xlsx")]

        # Define the number for the new file (does not overwrite)
        if existing:
            nums = []
            for f in existing:
                num_part = f.replace(base_name, "").replace(".xlsx", "")
                if num_part.isdigit():
                    nums.append(int(num_part))
            next_num = max(nums) 
            output_file = f"{base_name}{next_num}.xlsx"
        else:
            next_num = 1
            output_file = f"{base_name}{next_num}.xlsx"

        # If a file already exists, load it; otherwise, create a new DataFrame
        if os.path.exists(output_file):
            df_matrix = pd.read_excel(output_file, index_col=0)
        else:
            df_matrix = pd.DataFrame()

        # Add columns and indices if they do not exist yet
        if Nf_val not in df_matrix.columns:
            df_matrix[Nf_val] = np.nan
        if Ns_val not in df_matrix.index:
            df_matrix.loc[Ns_val] = np.nan

        # Save the calculated TAC value
        df_matrix.at[Ns_val, Nf_val] = TAC_value
        df_matrix.index.name = "Ns\\Nf"

        # Save the updated Excel file
        df_matrix.to_excel(output_file, float_format="%.2f")
        print(f"✅ TAC value saved in: {output_file}")

    except Exception as e:
        print(f"⚠️ Error saving TAC matrix: {type(e).__name__} — {e}")
    # ------------------------------
    
    return [TAC, Solution_within]

# ----------------------------------------------------------------------------------------------------------------
# Lower Bound Function
# ----------------------------------------------------------------------------------------------------------------
def LB_Gen(Nf_c,Ns_c,m_p):

    # Guide line results and LB storage
    GD_results = {}
    GD_TAC = {}
    GD_EX_CAPEX_COL = {}

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
        GD_results[Nf] = Calculations_DC_Aspen.fun_run_Aspen(Nsmax, Nf, m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'], m_p)

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

            # Getting additional results from Aspen:
            GD_results[Nf]['hydraulics'] = Calculations_DC_Aspen.fun_getfromAspen_hydraulics(Nsmax, m_p['Aspen_engine'], m_p['block_name'][0])

            # Problems Within Solutions:
            GD_Solution_Within[Nf] = Next_Level_Organizer.Next_Level(GD_results[Nf],m_p)
            GD_Sieve_Tray_Solution[Nf] = GD_Solution_Within[Nf]['Equipment1']
            CAPEX_COL = GD_Sieve_Tray_Solution[Nf]['Cost_OF']['COL_CAPEX']

            # Reflux Drum CAPEX:
            RD_L_mass_flow = GD_results[Nf]['liquid_mass_flows'][0] + GD_results[Nf]['mass_distillate_rate']
            RD_L_mass_density = GD_results[Nf]['distillate_liquid_mass_density'] 
            RD_Volume = Calculations_DC_Reflux_Drum.fun_RD_Vol(RD_L_mass_flow, RD_L_mass_density, m_p['TRL_min'])
            RD_D, RD_L = Calculations_DC_Reflux_Drum.fun_L_D(RD_Volume,m_p['L_D'])
            CAPEX_RD = Calculations_DC_Costs.fun_CAPEX_Reflux_Drum(RD_L, RD_D, m_p['roshell'])


            # Calculating Candidate TAC:
            GD_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_COL + CAPEX_COND + CAPEX_REB + CAPEX_RD) + OPEX_COL
            GD_EX_CAPEX_COL[Nf] = (1/m_p['Pb'])*(CAPEX_COND + CAPEX_REB + CAPEX_RD) + OPEX_COL

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
        GD_TAC[Nf] if Ns == Nsmax else  # If Ns == Nsmax, use GD_TAC[Nf] if available, otherwise 1e20
        GD_EX_CAPEX_COL[Nf] + CAPEX_Colmin_dict[Ns]  # If Ns != Nsmax, sum GD_EX_CAPEX_COL[Nf] with CAPEX_Colmin[Ns]
        if Nf in GD_EX_CAPEX_COL and Nf in GD_TAC else 1e20
        for Nf, Ns in zip(Nf_c, Ns_c)
    ])


    #------------------------------
    # Excel Map - Lower Bounds
    # Tomazim
    #------------------------------

    try:
        # Convert to DataFrame
        Ns_vals = np.unique(Ns_c)
        Nf_vals = np.unique(Nf_c)
        df_matrix = pd.DataFrame(
            index=Ns_vals, columns=Nf_vals
        ) 
        for nfi, nsi, lb in zip(Nf_c, Ns_c, LB_sol):
            df_matrix.at[nsi, nfi] = lb
        df_matrix.index.name = "Ns\\Nf"

        # Current directory
        folder = os.getcwd()

        # Search for existing files
        base_name = "LowerBound_Matrix_DC_"
        existing = [f for f in os.listdir(folder) if f.startswith(base_name) and f.endswith(".xlsx")]

        # Determine the number for the next file
        if existing:
            # Extract the number from the largest existing file
            nums = []
            for f in existing:
                num_part = f.replace(base_name, "").replace(".xlsx", "")
                if num_part.isdigit():
                    nums.append(int(num_part))
            next_num = max(nums) + 1 if nums else 1
        else:
            next_num = 1

        # Name of the new file
        output_file = f"{base_name}{next_num}.xlsx"

        # Save
        df_matrix.to_excel(output_file, float_format="%.2f")
        print(f"✅ File saved: {output_file}")

    except Exception as e:
        print(f"⚠️ Error saving LB matrix: {type(e).__name__} — {e}")
    #------------------------------

    return [LB_sol, TAC_best, Arg_best, Solution_Within_best]

#endregion
##################################################################################################################
