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
   
    # Update RadFrac inputs for current candidate:
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\NSTAGE').Value = v_Ns
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\FEED_STAGE\{m_p['feed_name'][0]}').Value = v_Nf
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\PRES1').Value = m_p['Pcol']           # Column pressure (Pa)
    Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Input\VALUE\1').Value = m_p['Purity']  # Update SPEC_1 as x_top
    # Running Aspen simulation:
    Aspen.Engine.Run2()
    min_condenser_duty = abs(Aspen.Tree.FindNode(rf'\Data\Blocks\{m_p['block_name_2'][0]}\Output\COND_DUTY').Value)#1000/3600       # kJ/h
    
    return min_condenser_duty
# endregion
##################################################################################################################

