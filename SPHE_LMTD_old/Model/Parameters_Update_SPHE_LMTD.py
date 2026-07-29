##################################################################################################################
# region Titles and Header
# Nature: 'Parameters_Calculations_List' and 'Example_Within_Set_Up' functions
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          28-Fev-2025     Alice Peccini             Original
#   0.2          21-Mar-2025     Mariana Mello             Allocation as a parameter
#   0.3          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
###################################################################################################################
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
import math
from SPHE_LMTD.Model.Model_Def_SPHE_LMTD import Model_SPHE_LMTD
# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions
#
# Adjustment of the data

def Parameter_Bounds(m_p):
    save_result('\n******* Testing consistency *******\n')
    m_p['romax']= -0.0031 * m_p['Tci'] * m_p['Tci'] -0.1354*m_p['Tci'] + 1002.4 
    m_p['romin']= -0.0031 * m_p['Thi'] * m_p['Thi'] -0.1354*m_p['Thi'] + 1002.4 
    m_p['kmax'] =  0.0012 * m_p['Thi'] + 0.5804
    m_p['Cpmax']=  -0.000213*m_p['Thi']*m_p['Thi']*m_p['Thi']+0.0383*m_p['Thi']*m_p['Thi']-1.87*m_p['Thi']+4206
    m_p['mimim']=  0.001445 * math.exp(-0.01927*m_p['Thi'])

    return m_p
# endregion
##################################################################################################################

