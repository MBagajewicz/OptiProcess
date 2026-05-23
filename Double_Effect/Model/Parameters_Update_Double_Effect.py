##################################################################################################################
# region Titles and Header
# Nature: 'Parameters_Calculations_List' and 'Example_Within_Set_Up' functions
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          28-Fev-2025     Alice Peccini             Original
##################################################################################################################
# INPUT: Define Functions for 'Parameters_Calculations_List' and 'Example_Within_Set_Up'
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def)
# For 'Parameters_Calculations_List':
#   def fun(model_parameters)
#       return model_parameters
# For 'Example_Within_Set_Up':
#   def fun(results,model_parameters)
#       return model_parameters
# endregion
##################################################################################################################

##################################################################################################################
# region Import Library
import numpy as np
import sys
import importlib
from Commom_Equations_DC import Calculations_DC_Param_Set_Up
from Commom_Equations_DC import (
    Calculations_DC_Aspen,
    Calculations_DC_Column_Sizing, 
    Calculations_DC_HEs,
    Calculations_DC_Costs,
    Calculations_DC_Reflux_Drum
)

# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions

# Initialize Aspen
def par_start_Aspen(m_p):
    
    m_p = Calculations_DC_Param_Set_Up.call_initial_Aspen(m_p)
    return m_p


#Tomazim
# High Pressure Column condenser_duty (Problem Within) set up
def Set_Up_HPCOL(results, m_p):
   
   m_p['SPEC_1'] = -results['reboiler_duty']*3600/1000    # Condenser duty (kJ/h) of HPCol  (Value W to kJ/h)
   m_p['Tcwin'] = results['temperatures'][-2]             # Cooling water inlet temperature from reboiler of LPCol
   m_p['Tcwout'] = results['temperatures'][-1]            # Cooling water outlet temperature from reboiler of LPCol
   m_p['TAC_new_file'] = True                             # Save TAC results in Excel file #Tomazim
   
   return m_p


# ---------------------------------------------------------------------------------------------------------------- 
# TAC Lower Bound Function
# ----------------------------------------------------------------------------------------------------------------
def TAC_LB_Gen_HPCol(Nf,Ns, GD_results, m_p):
    # Guide line results and LB storage
    GD_results = {}                  
    GD_TAC = {}
    GD_HE_TAC = {}
    GD_Dc = {}

    # Initializing function call count attribute # Tomazim
    if not hasattr(TAC_LB_Gen_HPCol, "count_LB_LPC_HPCol"):
        TAC_LB_Gen_HPCol.count_LB_LPC_HPCol = 0

    # Solve candidate on Aspen Plus:
    GD_results[Nf] = Calculations_DC_Aspen.fun_run_Aspen(Ns, Nf, m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'],m_p)

    # Increment function call count # Tomazim
    TAC_LB_Gen_HPCol.count_LB_LPC_HPCol += 1
    print(f"\033[92m[LB_LPC(HPCol) Run #{TAC_LB_Gen_HPCol.count_LB_LPC_HPCol}] Aspen simulation executed.\033[0m")


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
        GD_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_COL + CAPEX_REB + CAPEX_RD) + OPEX_COL
        GD_HE_TAC[Nf] = (1/m_p['Pb'])*(CAPEX_REB + CAPEX_RD) + OPEX_COL
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



# High Pressure Column Spec_1 = cond_duty (Lower Bound Generation)
def Set_Up_LB_HPCOL(Ns_c, Nf_c, Aspen, Cond_duty, m_p):
    
    #from Double_Effect import Examples_Double_Effect
    #from Double_Effect_Feed_Split import Examples_Double_Effect_Feed_Split
    
    main_module = sys.modules['__main__']
    Selected_Model = getattr(main_module, 'Selected_Model', None)
    Selected_Example = getattr(main_module, 'Selected_Example', None)

    examples_module_name = f'{Selected_Model}.Examples_{Selected_Model}'
    Examples_Module = importlib.import_module(examples_module_name)
    Active_Example = getattr(Examples_Module, Selected_Example)
    Active_Example = getattr(Examples_Module, Selected_Example)

 
    #m_p = Examples_Double_Effect_Feed_Split.Example1['Next_Level_Equipments']['Equipment1']['Model_Parameters']
    #m_p = Examples_Double_Effect.Example1['Next_Level_Equipments']['Equipment1']['Model_Parameters']
    m_p = Active_Example['Next_Level_Equipments']['Equipment1']['Model_Parameters']
    
    #m_p['SPEC_1'] = m_p['Purity']  # Setting SPEC_1 as x_top
    m_p['SPEC_1'] = -Cond_duty*3600/1000  # Setting SPEC_1 as condenser duty (kJ/h) of HPCol  (Value W to kJ/h)

    # Guide line results and LB storage
    GD_results = {}
    GD_TAC = {}
    GD_HE_TAC = {}
    GD_Dc = {}
    
    # Solve this problem for fixed in EXAMPLE_1 #tOMAZIM
    #Nf_c = Examples_Double_Effect.Example1['Next_Level_Equipments']['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'][0]
    #Ns_c = Examples_Double_Effect.Example1['Next_Level_Equipments']['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'][1]
    
    Nf_c = Active_Example['Next_Level_Equipments']['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'][0]
    Ns_c = Active_Example['Next_Level_Equipments']['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'][1]


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
        results_TAC = TAC_LB_Gen_HPCol(Nf, Nsmin, GD_results, m_p)
        #m_p ['Tempo_Aspen'] = #Tempo para o Aspen rodar cada simula����o #Tomazim

        # Checking feasibility:
        if results_TAC:

            GD_TAC[Nf] = list(results_TAC[0].values())[0]
            GD_HE_TAC[Nf] = list(results_TAC[1].values())[0]
            GD_Dc[Nf] = list(results_TAC[2].values())[0]
            #x_top_val = results_TAC[3]

            # Removing x_top constraint because for another Q_duty it can be feasible
            '''
            #Add check for x_top constraint:
            if x_top_val < m_p['Purity']:
                x_top_val = TAC_LB_Gen_HPCol(Nf,Nsmax, GD_results, m_p)[3] #Get x_top for Nsmax to check if some candidate is feasible in the range
                if x_top_val < m_p['Purity']: #If it has sufficient purity with Nsmax
                    GD_TAC[Nf] = 1e20
                    GD_HE_TAC[Nf] = 1e20
            '''

        # Solving guide line (where Nf > Nsmin)
        for Ns in range(Nsmin+1, Nsmax+1):  
        
            Nf = Ns -2 # Run only for last Nf in the guide line  
            print(f'Running Aspen simulation for candidate with Ns = {Ns} and Nf = {Nf}') 

            #GD_results[Nf] = Calculations_DC_Aspen.fun_run_Aspen(Nsmin, Nf, m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'], m_p)
            results_TAC = TAC_LB_Gen_HPCol(Nf, Ns, GD_results, m_p)

            # Checking feasibility:
            if results_TAC:

                GD_TAC[Nf] = list(results_TAC[0].values())[0]
                GD_HE_TAC[Nf] = list(results_TAC[1].values())[0]
                GD_Dc[Nf] = list(results_TAC[2].values())[0]
                #x_top_val = results_TAC[3]

                # Removing x_top constraint because for another Q_duty it can be feasible
                '''
                #Add check for x_top constraint:
                if x_top_val < m_p['Purity']:
                    x_top_val = TAC_LB_Gen_HPCol(Nf,Nsmax, GD_results, m_p)[3] #Get x_top for Nsmax to check if some candidate is feasible in the range
                    if x_top_val < m_p['Purity']: #If it has sufficient purity with Nsmax
                        GD_TAC[Nf] = 1e20
                        GD_HE_TAC[Nf] = 1e20
                '''


    '''
    # Handles the case when there are no valid candidates
    if not GD_TAC:
        GD_TAC[Nf] = 0
        GD_HE_TAC[Nf] = 0
    '''

    # Selecting best result found within the guide line:
    TAC_best = min(GD_TAC.values())
    Arg_best = [min(GD_TAC, key=GD_TAC.get), Nsmin]


    # 💢 Tomazim: not using this LB_sol for others candidates, only returning TAC_best and Arg_best from Nsmax

    #print(f'\n **Generating lower bounds for candidates with Ns = {Nsmin} to Ns = {Nsmax - 1}** \n')
    # Using the guide line results to generate candidate's lower bounds:
    '''
    LB_sol = np.array([
        GD_HE_TAC[Nf] + (1/m_p['Pb'])*Calculations_DC_Costs.fun_CAPEX_Col(
            Calculations_DC_Column_Sizing.f_Wshell(m_p['lt'], Ns-2, GD_Dc[Nf], m_p['roshell']), GD_Dc[Nf], Ns-2) 
        if Nf in GD_HE_TAC and Nf in GD_Dc else 1e20
        for Nf, Ns in zip(Nf_c, Ns_c)
    ])
    '''
    return [TAC_best, Arg_best]

# endregion
##################################################################################################################
