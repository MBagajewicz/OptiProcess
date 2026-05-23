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
from Commom_Equations_DC import Calculations_DC_Aspen

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
   
   return m_p

#gERAR LB_Gen para HPCol com x_top e Nsmáx
#Capex(min pratos) + energia(máx pratos)


# endregion
##################################################################################################################
