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
# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions

# ---------------------------------------------------------------------------------------------------------------- 
# Sequential Calculations List
# ----------------------------------------------------------------------------------------------------------------

def fun_sequential(results, m_p):
    # Extract the result dictionaries for the rectifying and stripping sections
    Rectifying_Results = results['Equipment1']
    Stripping_Results = results['Equipment2']

    # Get the keys (e.g., 'Dc1', 'Dc2', etc.)
    keys_rect = [k for k in Rectifying_Results if k.startswith('Dc') and k[2:].isdigit()]
    keys_strip = [k for k in Stripping_Results if k.startswith('Dc') and k[2:].isdigit()]

    # Extract the Dc values in the same order as the keys
    dc_list_rect = [Rectifying_Results[k]['Dc'] for k in keys_rect]
    dc_list_strip = [Stripping_Results[k]['Dc'] for k in keys_strip]

    # Extract the corresponding Wshell values in the same order
    Wshell_list_rect = [Rectifying_Results[k]['Wshell_OF']['Wshell'] for k in keys_rect]
    Wshell_list_strip = [Stripping_Results[k]['Wshell_OF']['Wshell'] for k in keys_strip]

    # Save the arrays into m_p, ensuring matching positions between Dc and Wshell
    m_p['Viable_DRECT'] = np.array(dc_list_rect)
    m_p['Viable_DSTRIP'] = np.array(dc_list_strip)
    m_p['Wshell_rect'] = np.array(Wshell_list_rect)
    m_p['Wshell_strip'] = np.array(Wshell_list_strip)

    return m_p




# endregion
##################################################################################################################

