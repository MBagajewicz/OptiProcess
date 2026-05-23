###################################################################################################################
#region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming 
# methodology 
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.1          20-Nov-2024     Miguel Bagajewicz         Proposed 
#   0.2          03-Fev-2025     Alice Peccini             BTX Column
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
import os
import pandas as pd
from Commom_Equations_DC import (
    Calculations_DC_Aspen,
    Calculations_DC_Column_Sizing, 
    Calculations_DC_HEs,
    Calculations_DC_Costs,
    Calculations_DC_Reflux_Drum
)


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

def x_TOP(Nf_c, Ns_c, m_p): # Allows only candidates with x_TOP >= Purity
    results = Calculations_DC_Aspen.fun_getfromAspen_x_Top( m_p['Aspen_engine'], m_p['stream_names'][1],m_p['Comp_name'][0]) # Get top product mole fraction from Aspen
    fun_val =  m_p['Purity'] - results['Mole_Fraction_TOP']

    return [fun_val]

# ---------------------------------------------------------------------------------------------------------------- 
# Objective Function
# ----------------------------------------------------------------------------------------------------------------
def TAC_OF(Nf_c,Ns_c,m_p):    

    # Initializing function call count attribute # Tomazim
    if not hasattr(TAC_OF, "count_HPC"):
        TAC_OF.count_HPC = 0
    
    # Running Aspen simulation:
    print(f'Running Aspen simulation for candidate with Ns = {Ns_c[0]} and Nf = {Nf_c[0]}')
    results = Calculations_DC_Aspen.fun_run_Aspen(Ns_c[0], Nf_c[0], m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'],m_p)

    # Increment function call count # Tomazim
    TAC_OF.count_HPC += 1
    print(f"\033[92m[HPC Run #{TAC_OF.count_HPC}] Aspen simulation executed.\033[0m")

    # If candidate was successfully solved:
    if results:
       
        # Heat Exchanger Areas and CAPEX:
        Tcin_reb = results['temperatures'][-2]
        Tcout_reb = results['temperatures'][-1]
        Reb_area = Calculations_DC_HEs.fun_HE_areas(m_p['Tlpst'], m_p['Tlpst'], Tcin_reb, Tcout_reb, results['reboiler_duty'], m_p['Ur']) 
        print(f"Reboiler duty: {results['reboiler_duty']}")
        #Thin_cond = m_p['Tlpst'] 
        #Thout_cond = m_p['Tlpst'] 
        Thin_cond = results['temperatures'][1] 
        Thout_cond = results['temperatures'][0] 
        #Cond_area = Calculations_DC_HEs.fun_HE_areas(Thin_cond, Thout_cond, m_p['Tcwin'], m_p['Tcwout'], -m_p['SPEC_1']*1000/3600, m_p['Uc'])
        #print(f"Condenser duty: {-m_p['SPEC_1']*1000/3600}")
        Cond_area = Calculations_DC_HEs.fun_HE_areas(Thin_cond, Thout_cond, m_p['Tcwin'], m_p['Tcwout'], results['condenser_duty'], m_p['Uc'])
        CAPEX_COND = Calculations_DC_Costs.CAPEX_Shell_and_Tube(Cond_area)
        CAPEX_REB = Calculations_DC_Costs.CAPEX_Kettle(Reb_area) 

        print(f'-------CAPEX_COND HPC= {CAPEX_COND:.2f}')

        # Column CAPEX:
        Dc = Calculations_DC_Column_Sizing.f_Diameter(m_p['lt'], results['liquid_mass_density'], results['vapor_mass_density'],results['maximum_vapor_flow'])
        Nt = (Ns_c[0] - 2)
        Wshell = Calculations_DC_Column_Sizing.f_Wshell(m_p['lt'], Nt, Dc, m_p['roshell'])
        CAPEX_COL = Calculations_DC_Costs.fun_CAPEX_Col(Wshell,Dc,Nt)

        # Reflux Drum CAPEX:
        RD_L_mass_flow = results['liquid_mass_flows'][0] + results['mass_distillate_rate']
        RD_L_mass_density = results['distillate_liquid_mass_density'] 
        RD_Volume = Calculations_DC_Reflux_Drum.fun_RD_Vol(RD_L_mass_flow, RD_L_mass_density,m_p['TRL_min'])
        RD_D, RD_L = Calculations_DC_Reflux_Drum.fun_L_D(RD_Volume,m_p['L_D'])
        CAPEX_RD = Calculations_DC_Costs.fun_CAPEX_Reflux_Drum(RD_L, RD_D, m_p['roshell'])

        # Calculating OPEX Cost:
        #Cooling_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Ccw'],results['condenser_duty'],m_p['hours'])
        Heating_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Clpst'],results['reboiler_duty'],m_p['hours'])
        #OPEX_COL = Cooling_Cost + Heating_Cost
        OPEX_COL = Heating_Cost # There is no cooling cost in HPC since we are using water from LPC reboiler
        

        # Caculting Candidate TAC:
        TAC = [(1/m_p['Pb'])*(CAPEX_COL + CAPEX_COND + CAPEX_REB + CAPEX_RD) + OPEX_COL]

    else:
        #TAC = [np.nan]  # If candidate was not solved, return NaN --- NaN causes error
        TAC = np.array([1e20])  # If candidate was not solved, return a very high value
    print(f'TAC = {TAC[0]:.2f}')

    # print('CAPEX_COL:', CAPEX_COL)
    # print('CAPEX_COND:', CAPEX_COND)
    # print('CAPEX_REB:', CAPEX_REB)
    # print('CAPEX_RD:', CAPEX_RD)
    # print('Cooling_Cost:', Cooling_Cost)
    # print('Heating_Cost:', Heating_Cost)
    # print('OPEX_COL:', OPEX_COL)
    # print('Dc:', Dc)  

    
    '''
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

        # Base name for the file and control file
        base_name = "TAC_Matrix_HPC_"
        control_file = os.path.join(folder, "TAC_current_run.txt")

        # Helper: read/write control file (currently stores only the current_num)
        def _write_control(num):
            with open(control_file, "w") as f:
                f.write(str(int(num)))

        def _read_control():
            if not os.path.exists(control_file):
                return None
            with open(control_file, "r") as f:
                txt = f.read().strip()
            return int(txt) if txt.isdigit() else None

        # -------------------------------------------------------
        # Decide whether to create a new file number now.
        # The decision can be forced by the caller by setting:
        #   m_p['TAC_new_file'] = True
        # If that key is True -> increment and create a new numbered file.
        # If absent/False -> reuse current file number (if exists), else create new.
        # After forcing, we reset m_p['TAC_new_file'] = False to avoid repeated creations.
        # -------------------------------------------------------

        force_new = bool(m_p.get('TAC_new_file', False))

        if force_new:
            # create a new file number incrementally
            existing = [f for f in os.listdir(folder) if f.startswith(base_name) and f.endswith(".xlsx")]
            if existing:
                nums = []
                for f in existing:
                    num_part = f.replace(base_name, "").replace(".xlsx", "")
                    if num_part.isdigit():
                        nums.append(int(num_part))
                next_num = max(nums) + 1 if nums else 1
            else:
                next_num = 1
            current_num = next_num
            _write_control(current_num)  # record current number
            # reset flag so subsequent calls in same "logical call" don't force more files
            m_p['TAC_new_file'] = False
        else:
            # Not forced -> try to reuse whatever is in the control file, else create first file
            stored = _read_control()
            if stored is not None:
                current_num = stored
            else:
                # no control file yet -> create first file number (1 or next available)
                existing = [f for f in os.listdir(folder) if f.startswith(base_name) and f.endswith(".xlsx")]
                if existing:
                    nums = []
                    for f in existing:
                        num_part = f.replace(base_name, "").replace(".xlsx", "")
                        if num_part.isdigit():
                            nums.append(int(num_part))
                    next_num = max(nums) + 1 if nums else 1
                else:
                    next_num = 1
                current_num = next_num
                _write_control(current_num)

        # -------------------------------------------------------
        # Work with the corresponding Excel file
        # -------------------------------------------------------
        output_file = f"{base_name}{current_num}.xlsx"

        # Load or create DataFrame
        if os.path.exists(output_file):
            df_matrix = pd.read_excel(output_file, index_col=0)
        else:
            df_matrix = pd.DataFrame()

        # Normalize index/columns read from excel to int where possible (keeps keys consistent)
        try:
            df_matrix.columns = [int(c) if (isinstance(c, (int, float)) or str(c).replace('.0','').isdigit()) else c for c in df_matrix.columns]
        except Exception:
            pass
        try:
            df_matrix.index = [int(i) if (isinstance(i, (int, float)) or str(i).replace('.0','').isdigit()) else i for i in df_matrix.index]
        except Exception:
            pass

        # Ensure the index and columns exist
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
    '''

    return TAC


# ---------------------------------------------------------------------------------------------------------------- 
# TAC Lower Bound Function
# ----------------------------------------------------------------------------------------------------------------
def TAC_LB_Gen(Nf,Ns, GD_results, m_p):
    # Guide line results and LB storage
    GD_results = {}                  
    GD_TAC = {}
    GD_HE_TAC = {}
    GD_Dc = {}

    # Initializing function call count attribute # Tomazim
    if not hasattr(TAC_LB_Gen, "count_LB_HPC"):
        TAC_LB_Gen.count_LB_HPC = 0

    # Solve candidate on Aspen Plus:
    GD_results[Nf] = Calculations_DC_Aspen.fun_run_Aspen(Ns, Nf, m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'],m_p)

    # Increment function call count # Tomazim
    TAC_LB_Gen.count_LB_HPC += 1
    print(f"\033[92m[LB_HPC Run #{TAC_LB_Gen.count_LB_HPC}] Aspen simulation executed.\033[0m")

    # Checking feasibility:
    if GD_results[Nf]:

        # Heat Exchanger Areas:
        Tcin_reb = GD_results[Nf]['temperatures'][-2]
        Tcout_reb = GD_results[Nf]['temperatures'][-1]
        Reb_area = Calculations_DC_HEs.fun_HE_areas(m_p['Tlpst'], m_p['Tlpst'], Tcin_reb, Tcout_reb, GD_results[Nf]['reboiler_duty'], m_p['Ur'])
        #Thin_cond = m_p['Tlpst'] 
        #Thout_cond = m_p['Tlpst'] 
        Thin_cond = GD_results[Nf]['temperatures'][1] 
        Thout_cond = GD_results[Nf]['temperatures'][0]
        #Cond_area = Calculations_DC_HEs.fun_HE_areas(Thin_cond, Thout_cond, m_p['Tcwin'], m_p['Tcwout'], -m_p['SPEC_1'], m_p['Uc']) 
        Cond_area = Calculations_DC_HEs.fun_HE_areas(Thin_cond, Thout_cond, m_p['Tcwin'], m_p['Tcwout'], GD_results[Nf]['condenser_duty'], m_p['Uc'])
        CAPEX_COND = Calculations_DC_Costs.CAPEX_Shell_and_Tube(Cond_area)
        CAPEX_REB = Calculations_DC_Costs.CAPEX_Kettle(Reb_area)
        
        # Column CAPEX:
        GD_Dc[Nf] = Calculations_DC_Column_Sizing.f_Diameter(m_p['lt'], GD_results[Nf]['liquid_mass_density'], GD_results[Nf]['vapor_mass_density'],GD_results[Nf]['maximum_vapor_flow'])
        Ntmin = (Ns - 2) # Discounded trays: reboiler + condenser
        Wshell = Calculations_DC_Column_Sizing.f_Wshell(m_p['lt'], Ntmin, GD_Dc[Nf], m_p['roshell'] )
        CAPEX_COL = Calculations_DC_Costs.fun_CAPEX_Col(Wshell, GD_Dc[Nf], Ntmin)

        # Reflux Drum CAPEX:
        RD_L_mass_flow = GD_results[Nf]['liquid_mass_flows'][0] + GD_results[Nf]['mass_distillate_rate']
        RD_L_mass_density = GD_results[Nf]['distillate_liquid_mass_density'] 
        RD_Volume = Calculations_DC_Reflux_Drum.fun_RD_Vol(RD_L_mass_flow, RD_L_mass_density, m_p['TRL_min'])
        RD_D, RD_L = Calculations_DC_Reflux_Drum.fun_L_D(RD_Volume,m_p['L_D'])
        CAPEX_RD = Calculations_DC_Costs.fun_CAPEX_Reflux_Drum(RD_L, RD_D, m_p['roshell'])
        
        # Calculating OPEX Cost:
        #Cooling_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Ccw'],GD_results[Nf]['condenser_duty'],m_p['hours'])
        Heating_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Clpst'],GD_results[Nf]['reboiler_duty'],m_p['hours'])
        #OPEX_COL = Cooling_Cost + Heating_Cost
        OPEX_COL = Heating_Cost # There is no cooling cost in HPC since we are using water from LPC reboiler
        
        # TAC:
        GD_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_COL + CAPEX_COND + CAPEX_REB + CAPEX_RD) + OPEX_COL
        GD_HE_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_COND + CAPEX_REB + CAPEX_RD) + OPEX_COL
        print(f'TAC = {GD_TAC[Nf]:.2f}')

    # Handles the case when simulation was not successful
    else:
        GD_TAC[Nf] = 0
        GD_HE_TAC[Nf] = 0
        GD_Dc[Nf] = 0
        print(f'TAC = {GD_TAC[Nf]:.2f}')

    #Obtaining x_top constraint:
    results = Calculations_DC_Aspen.fun_getfromAspen_x_Top( m_p['Aspen_engine'], m_p['stream_names'][1],m_p['Comp_name'][0])
    x_top_val = results['Mole_Fraction_TOP']

    return [GD_TAC, GD_HE_TAC, GD_Dc, x_top_val]


# ---------------------------------------------------------------------------------------------------------------- 


# ---------------------------------------------------------------------------------------------------------------- 
# Lower Bound Function
# ----------------------------------------------------------------------------------------------------------------
def LB_Gen(Nf_c,Ns_c,m_p):

    # Guide line results and LB storage
    GD_results = {}                  
    GD_TAC = {}
    GD_HE_TAC = {}
    GD_Dc = {}

    # Identifying search space:
    Nsmax = np.nanmax(Ns_c)
    Nsmin = np.nanmin(Ns_c)
    Nfmin = np.nanmin(Nf_c)
    Nfmax = np.nanmax(Nf_c)

    # Solving guide line (where Nf < Nsmin)
    print(f'Starting to solve line of candidates with Ns = {Nsmin}')
    for Nf in range(Nfmin, Nsmin-1):  

        print(f'Running Aspen simulation for candidate with Ns = {Nsmin} and Nf = {Nf}') 

        #GD_results[Nf] = Calculations_DC_Aspen.fun_run_Aspen(Nsmin, Nf, m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'], m_p)
        results_TAC = TAC_LB_Gen(Nf, Nsmin, GD_results, m_p)
        #m_p ['Tempo_Aspen'] = #Tempo para o Aspen rodar cada simula����o #Tomazim

        # Checking feasibility:
        if results_TAC:

            GD_TAC[Nf] = list(results_TAC[0].values())[0]
            GD_HE_TAC[Nf] = list(results_TAC[1].values())[0]
            GD_Dc[Nf] = list(results_TAC[2].values())[0]
            x_top_val = results_TAC[3]

            #Add check for x_top constraint:
            if x_top_val < m_p['Purity']:
                x_top_val = TAC_LB_Gen(Nf,Nsmax, GD_results, m_p)[3] #Get x_top for Nsmax to check if some candidate is feasible in the range
                if x_top_val > m_p['Purity']: #If it has sufficient purity with Nsmax
                    GD_TAC[Nf] = 1e20
                else:
                    GD_TAC[Nf] = 1e20
                    GD_HE_TAC[Nf] = 1e20

        # Solving guide line (where Nf > Nsmin)
        for Ns in range(Nsmin+1, Nsmax+1):  
        
            Nf = Ns -2 # Run only for last Nf in the guide line  
            print(f'Running Aspen simulation for candidate with Ns = {Ns} and Nf = {Nf}') 

            #GD_results[Nf] = Calculations_DC_Aspen.fun_run_Aspen(Nsmin, Nf, m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'], m_p)
            results_TAC = TAC_LB_Gen(Nf, Ns, GD_results, m_p)

            # Checking feasibility:
            if results_TAC:

                GD_TAC[Nf] = list(results_TAC[0].values())[0]
                GD_HE_TAC[Nf] = list(results_TAC[1].values())[0]
                GD_Dc[Nf] = list(results_TAC[2].values())[0]
                x_top_val = results_TAC[3]

                #Add check for x_top constraint:
                if x_top_val < m_p['Purity']:
                    x_top_val = TAC_LB_Gen(Nf,Nsmax, GD_results, m_p)[3] #Get x_top for Nsmax to check if some candidate is feasible in the range
                    if x_top_val > m_p['Purity']: #If it has sufficient purity with Nsmax
                        GD_TAC[Nf] = 1e20
                    else:
                        GD_TAC[Nf] = 1e20
                        GD_HE_TAC[Nf] = 1e20


    # Handles the case when there are no valid candidates
    if not GD_TAC:
        GD_TAC[Nf] = 0
        GD_HE_TAC[Nf] = 0

    # Selecting best result found within the guide line:
    # Check if there is any feasible solution (x_top >= purity), else 2 menor # Tomazim (talvez não precise mais)
    TAC_best = min(GD_TAC.values())
    Arg_best = [min(GD_TAC, key=GD_TAC.get), Nsmin]

    print(f'\n **Generating lower bounds for candidates with Ns = {Nsmin+1} to Ns = {Nsmax}** \n')
    # Using the guide line results to generate candidate's lower bounds:

    LB_sol = np.array([
        GD_HE_TAC[Nf] + (1/m_p['Pb'])*Calculations_DC_Costs.fun_CAPEX_Col(
            Calculations_DC_Column_Sizing.f_Wshell(m_p['lt'], Ns-2, GD_Dc[Nf], m_p['roshell']), GD_Dc[Nf], Ns-2) 
        if Nf in GD_HE_TAC and Nf in GD_Dc else 1e20
        for Nf, Ns in zip(Nf_c, Ns_c)
        
    ])

    '''
    #Printing info for LB calculations
    for Nf, Ns in zip(Nf_c, Ns_c):
        if Nf in GD_HE_TAC and Nf in GD_Dc:
            Wshell = Calculations_DC_Column_Sizing.f_Wshell(m_p['lt'], Ns-2, GD_Dc[Nf], m_p['roshell'])
            capex_col = Calculations_DC_Costs.fun_CAPEX_Col(Wshell, GD_Dc[Nf], Ns-2)
            total = GD_HE_TAC[Nf] + (1/m_p['Pb']) * capex_col

            print(f"[OK] Nf={Nf}, Ns={Ns}, GD_HE_TAC={GD_HE_TAC[Nf]:.4f}, CAPEX_col={capex_col:.4f}, Total={total:.4f}")
    '''
    
    '''
    #------------------------------
    # Excel Map - Lower Bounds
    # Tomazim
    #------------------------------
    import os
    import pandas as pd

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
        base_name = "LowerBound_Matrix_HPC_"
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
    '''
    
    
 


    return [LB_sol, TAC_best, Arg_best]

#endregion
##################################################################################################################
