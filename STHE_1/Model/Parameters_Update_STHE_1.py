##################################################################################################################
# region Titles and Header
# Nature: 'Parameters_Calculations_List' and 'Example_Within_Set_Up' functions
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          28-Fev-2025     Alice Peccini             Original
#   0.2          21-Mar-2025     Mariana Mello             Allocation as a parameter
#   0.3          12-May-2025     Mariana Mello             Update data consistency
#   0.4          06-Jun-2025     Mariana Mello             Update to fix error
#   0.5          31-Aug-2025     Diego Oliva               All functions now are in Library 'Common'
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
import sys
# from Common_Equations_HEX import Calculations_HEX_Consistency
from Common.HEX_Calculations import Calculations_HEX_Consistency
from Common.HEX_Calculations import Calculations_HEX_Allocation
from Common.HEX_Calculations import Calculations_HEX_Tho_Tco
from Common.HEX_Calculations import Calculations_HEX_WallTherCond
from Common.Common_Calculations import Calculations_Model_Consistency
# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions

# Adjustment of the data
def allocation(m_p):
    allocation = Calculations_HEX_Allocation.allocation(m_p)

# Basic consistency
def basic_consistency(m_d,m_p,save_result):
    save_result('\n******* Testing basic consistency *******\n')

    verify1 = Calculations_Model_Consistency.variables_bounds(m_d, save_result)
    verify2 = Calculations_Model_Consistency.variables_standard_values(m_d, save_result)

# Model consistency
def model_consistency(m_d, m_p, save_result):
    save_result('\n******* Testing model consistency *******\n')

    verify1 = Calculations_HEX_Consistency.verify_flag_inputs(m_p)
    verify2 = Calculations_HEX_WallTherCond.tube_wall_thermal_conductivity(m_p, save_result)
    verify3 = Calculations_HEX_Tho_Tco.HEX_Tho_Tco(m_p)
    verify4 = Calculations_HEX_Consistency.verification_positive_variables(m_p, save_result)
    verify5 = Calculations_HEX_Consistency.verification_DeltaTmin(m_p, save_result)
    # verify4 = Calculations_HEX_Consistency.verification_heatload(m_p, save_result)
    verify6 = Calculations_HEX_Consistency.verification_Thi_Tho(m_p, save_result)
    verify7 = Calculations_HEX_Consistency.verification_Tco_Tci(m_p, save_result)
    verify8 = Calculations_HEX_Consistency.verification_Tco_Thi_STHE(m_p, m_d, save_result)
    verify9 = Calculations_HEX_Consistency.verification_Tci_Tho(m_p, save_result)
    return m_d, m_p


# endregion
##################################################################################################################

