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

    # Running Aspen simulation:
    print(f'Running Aspen simulation for candidate with Ns = {Ns_c[0]} and Nf = {Nf_c[0]}')
    results = Calculations_DC_Aspen.fun_run_Aspen(Ns_c[0], Nf_c[0], m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'],m_p)

    # If candidate was successfully solved:
    if results:
       
        # Heat Exchanger Areas and CAPEX:
        Tcin_reb = results['temperatures'][-2]
        Tcout_reb = results['temperatures'][-1]
        Reb_area = Calculations_DC_HEs.fun_HE_areas(m_p['Tlpst'], m_p['Tlpst'], Tcin_reb, Tcout_reb, results['reboiler_duty'], m_p['Ur']) 
        Thin_cond = m_p['Tlpst'] 
        Thout_cond = m_p['Tlpst'] 
        #Thin_cond = results['temperatures'][1] 
        #Thout_cond = results['temperatures'][0] 
        Cond_area = Calculations_DC_HEs.fun_HE_areas(Thin_cond, Thout_cond, m_p['Tcwin'], m_p['Tcwout'], -m_p['SPEC_1']*1000/3600, m_p['Uc'])
        #Cond_area = Calculations_DC_HEs.fun_HE_areas(Thin_cond, Thout_cond, m_p['Tcwin'], m_p['Tcwout'], results['condenser_duty'], m_p['Uc'])
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
        Cooling_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Ccw'],results['condenser_duty'],m_p['hours'])
        Heating_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Clpst'],results['reboiler_duty'],m_p['hours'])
        OPEX_COL = Cooling_Cost + Heating_Cost

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

    return TAC

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

    # Solving guide line (where Ns = Nsmax)
    print(f'Starting to solve line of candidates with Ns = {Nsmax}')
    for Nf in range(Nfmin, Nfmax+1):  

        #Add check for Condenser_duty constraint: 
        #call Set_Up_HPCol
        from DC_Condenser.Model import Parameters_Update_DC_Condenser
        min_condenser_duty = Parameters_Update_DC_Condenser.Set_Up_HPCOL(Nsmax, Nf, m_p['Aspen_engine'],m_p)
        if abs(m_p['SPEC_1']) > min_condenser_duty :
            print(f'Candidate with Nf = {Nf} rejected due to insufficient condenser duty: SPEC_1 = {abs(m_p["SPEC_1"]):.4f} > {min_condenser_duty:.4f}')
            GD_TAC[Nf] = 1e20
            GD_HE_TAC[Nf] = 1e20
        else:    

            GD_results[Nf] = Calculations_DC_Aspen.fun_run_Aspen(Nsmax, Nf, m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'], m_p)

            # Checking feasibility:
            if GD_results[Nf]:
                
                #Tomazim --excluir
                #Add check for x_top constraint:
                results = Calculations_DC_Aspen.fun_getfromAspen_x_Top( m_p['Aspen_engine'], m_p['stream_names'][1],m_p['Comp_name'][0])
                x_top_val = results['Mole_Fraction_TOP']
                if x_top_val < m_p['Purity']: #comparar cond_duty
                    print(f'Candidate with Nf = {Nf} rejected due to insufficient purity: x_top = {x_top_val:.4f} < {m_p["Purity"]:.4f}')
                    GD_TAC[Nf] = 1e20
                    GD_HE_TAC[Nf] = 1e20
                    continue
                
                # Heat Exchanger Areas:
                Tcin_reb = GD_results[Nf]['temperatures'][-2]
                Tcout_reb = GD_results[Nf]['temperatures'][-1]
                Reb_area = Calculations_DC_HEs.fun_HE_areas(m_p['Tlpst'], m_p['Tlpst'], Tcin_reb, Tcout_reb, GD_results[Nf]['reboiler_duty'], m_p['Ur'])
                Thin_cond = m_p['Tlpst'] 
                Thout_cond = m_p['Tlpst'] 
                #Thin_cond = GD_results[Nf]['temperatures'][1] 
                #Thout_cond = GD_results[Nf]['temperatures'][0]
                Cond_area = Calculations_DC_HEs.fun_HE_areas(Thin_cond, Thout_cond, m_p['Tcwin'], m_p['Tcwout'], -m_p['SPEC_1'], m_p['Uc']) 
                #Cond_area = Calculations_DC_HEs.fun_HE_areas(Thin_cond, Thout_cond, m_p['Tcwin'], m_p['Tcwout'], GD_results[Nf]['condenser_duty'], m_p['Uc'])
                CAPEX_COND = Calculations_DC_Costs.CAPEX_Shell_and_Tube(Cond_area)
                CAPEX_REB = Calculations_DC_Costs.CAPEX_Kettle(Reb_area)
                
                # Column CAPEX:
                GD_Dc[Nf] = Calculations_DC_Column_Sizing.f_Diameter(m_p['lt'], GD_results[Nf]['liquid_mass_density'], GD_results[Nf]['vapor_mass_density'],GD_results[Nf]['maximum_vapor_flow'])
                Ntmax = (Nsmax - 2)
                Wshell = Calculations_DC_Column_Sizing.f_Wshell(m_p['lt'], Ntmax, GD_Dc[Nf], m_p['roshell'] )
                CAPEX_COL = Calculations_DC_Costs.fun_CAPEX_Col(Wshell, GD_Dc[Nf], Ntmax)

                # Reflux Drum CAPEX:
                RD_L_mass_flow = GD_results[Nf]['liquid_mass_flows'][0] + GD_results[Nf]['mass_distillate_rate']
                RD_L_mass_density = GD_results[Nf]['distillate_liquid_mass_density'] 
                RD_Volume = Calculations_DC_Reflux_Drum.fun_RD_Vol(RD_L_mass_flow, RD_L_mass_density, m_p['TRL_min'])
                RD_D, RD_L = Calculations_DC_Reflux_Drum.fun_L_D(RD_Volume,m_p['L_D'])
                CAPEX_RD = Calculations_DC_Costs.fun_CAPEX_Reflux_Drum(RD_L, RD_D, m_p['roshell'])
                
                # Calculating OPEX Cost:
                Cooling_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Ccw'],GD_results[Nf]['condenser_duty'],m_p['hours'])
                Heating_Cost = Calculations_DC_Costs.fun_Utility_Costs(m_p['Clpst'],GD_results[Nf]['reboiler_duty'],m_p['hours'])
                OPEX_COL = Cooling_Cost + Heating_Cost

                # TAC:
                GD_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_COL + CAPEX_COND + CAPEX_REB + CAPEX_RD) + OPEX_COL
                GD_HE_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_COND + CAPEX_REB + CAPEX_RD) + OPEX_COL
                print(f'TAC = {GD_TAC[Nf]:.2f}')

    # Handles the case when there are no valid candidates
    if not GD_TAC:
        GD_TAC[Nf] = 0
        GD_HE_TAC[Nf] = 0

    # Selecting best result found within the guide line:
    TAC_best = min(GD_TAC.values())
    Arg_best = [min(GD_TAC, key=GD_TAC.get), Nsmax]

    print(f'\n **Generating lower bounds for candidates with Ns = {Nsmin} to Ns = {Nsmax - 1}** \n')
    # Using the guide line results to generate candidate's lower bounds:

    LB_sol = np.array([
        GD_HE_TAC[Nf] + (1/m_p['Pb'])*Calculations_DC_Costs.fun_CAPEX_Col(
            Calculations_DC_Column_Sizing.f_Wshell(m_p['lt'], Ns-2, GD_Dc[Nf], m_p['roshell']), GD_Dc[Nf], Ns-2) 
        if Nf in GD_HE_TAC and Nf in GD_Dc else 1e20
        for Nf, Ns in zip(Nf_c, Ns_c)
    ])

    return [LB_sol, TAC_best, Arg_best]

#endregion
##################################################################################################################
