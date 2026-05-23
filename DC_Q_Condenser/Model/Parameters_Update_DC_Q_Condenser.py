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
from Commom_Equations_DC import Calculations_DC_Param_Set_Up
# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions


# Initialize Aspen
def par_start_Aspen(m_p):

    m_p = Calculations_DC_Param_Set_Up.call_initial_Aspen(m_p)

    return m_p

# High Pressure Column Spec_1 = x_top (Lower Bound Generation)
def Set_Up_HPCOL(v_Ns, v_Nf, Aspen, m_p):

    # Initializing function call count attribute # Tomazim
    if not hasattr(Set_Up_HPCOL, "count_LB_HPC_x_top"):
        Set_Up_HPCOL.count_LB_HPC_x_top = 0
   
    # Update RadFrac inputs for current candidate:
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\NSTAGE').Value = v_Ns
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\FEED_STAGE\{m_p['stream_names_2'][0]}').Value = v_Nf
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\PRES1').Value = m_p['Pcol']           # Column pressure (Pa)
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\VALUE\1').Value = m_p['Purity']  # Update SPEC_1 as x_top


    # Set feed stream data:
    for comp, mole_frac in zip(m_p['Comp_name'], m_p['z_f']):   # Molar fractions for components
        molar_flow = m_p['F_f'] *mole_frac                       # Calculate molar flow for the component
        Aspen.Tree.FindNode(rf'\Data\Streams\{m_p['stream_names_2'][0]}\Input\FLOW\MIXED\{comp}').Value = molar_flow     # Input molar flow for each component
    Aspen.Tree.FindNode(rf'\Data\Streams\{m_p['stream_names_2'][0]}\Input\TEMP\MIXED').Value = m_p['T_f']                    # Input feed stream temperature (K)
    Aspen.Tree.FindNode(rf'\Data\Streams\{m_p['stream_names_2'][0]}\Input\PRES\MIXED').Value = m_p['Pcol']                      # Input feed stream pressure (Pa)
    
    # Set column data that remain the same for every candidate:
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\PRES1').Value = m_p['Pcol']                            # Column pressure (Pa)
    #Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\VALUE\1').Value = m_p['SPEC_1']                       # Specification 1 - Example: Top Fraction Product or Condenser Duty
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\VALUE\2').Value = m_p['SPEC_2']                        # Specification 2 - Example: Bottom Fraction Product or Reboiler Duty

    # Distillate rate and reflux ratio bounds for aspen search:
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\LB\1').Value = m_p['distillate_rate_bounds'][0]                              # Distillare rate lower bound (kmol/h)
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\UB\1').Value = m_p['distillate_rate_bounds'][1]                          # Distillare rate upper bound (kmol/h)
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\LB\2').Value = m_p['reflux_ratio_bounds'][0]                            # Molar reflux ratio lower bound
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\UB\2').Value = m_p['reflux_ratio_bounds'][1]                          # Molar reflux ratio upper bound


    # Running Aspen simulation:
    Aspen.Engine.Run2()

    # Increment function call count # Tomazim
    Set_Up_HPCOL.count_LB_HPC_x_top += 1
    print(f"\033[92m[LB_HPC_x_top Run #{Set_Up_HPCOL.count_LB_HPC_x_top}] Aspen simulation executed.\033[0m")

    # min_condenser_duty = abs(Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Output\COND_DUTY').Value)#1000/3600       # kJ/h
    node = Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p["block_name_2"][0]}\Output\COND_DUTY')
    if node and node.Value is not None:
        min_condenser_duty = abs(node.Value)#1000/3600       # kJ/h
    else:
        min_condenser_duty = float('inf')  # or some other appropriate value or error handling
    
    return min_condenser_duty
# endregion
##################################################################################################################

