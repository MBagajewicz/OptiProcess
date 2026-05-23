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
from Commom_Equations_DC import Calculations_DC_Aspen
from DC_DC_Double_Effect_Optimizer.Model import Parameters_Update_DC_DC_Double_Effect_Optimizer

from OptiCode import Next_Level_Organizer
# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions


# Initialize Aspen
def par_start_Aspen(m_p):

    file_name = m_p['file_name'][0]
    stream_name = m_p['stream_names'][0]
    block_name = m_p['block_name'][0]
    comp_name = m_p['Comp_name']
    z_feed = m_p['z_f']         # Feed molar fractions
    F_feed = m_p['F_f']         # Feed molar flow for each component
    Split = m_p['Split']        # Split fraction of the molar flow in the first column
    T_feed = m_p['T_f']         # Feed temperature 
    P_col = m_p['Pcol']         # Column pressure
    x_TOP = m_p['xB_TOP']       # Benzene purity - top product
    x_BOTTOM = m_p['xB_BOTTOM'] # Benzene purity - bottom product
    D_LB = m_p['distillate_rate_bounds'][0]   
    D_UB = m_p['distillate_rate_bounds'][1]
    RR_LB = m_p['reflux_ratio_bounds'][0]
    RR_UB = m_p['reflux_ratio_bounds'][1]

    m_p['Aspen_engine'] = Calculations_DC_Aspen.fun_initial_Aspen(file_name, stream_name, block_name, comp_name,  
                                        z_feed, F_feed, Split, T_feed, P_col, x_TOP, x_BOTTOM, D_LB, D_UB, RR_LB, RR_UB)

    return m_p


# High Pressure Column condenser_duty (Problem Within) set up
def Set_Up_HPCOL(results, m_p):

   Solution_HPCOL = Next_Level_Organizer.Next_Level(results, m_p)

   m_p1 = Solution_HPCOL['Equipment1'] # equipament 1 - Low Pressure Column
   m_p2 = Solution_HPCOL['Equipment2'] # equipament 2 - High Pressure Column
   m_p2['x_TOP'] = m_p1['reboiler_duty'] 
    
   '''
   #ATUALIZA O CALOR DO CONDENSADOR DA COLUNA DE ALTA PRESSÃO
   Solution_within = Next_Level_Organizer.Next_Level(results, m_p)
   m_p2 = Solution_within['Equipment2'] # equipament 2 - High Pressure Column
   m_p2['xB_TOP'] = results['reboiler_duty']   # kJ/h 
   '''
   return m_p


'''

# High Pressure Column condenser_duty (Problem Within) set up
def Set_Up_HPCOL(results, m_p):

    
    #ATUALIZA O CALOR DO CONDENSADOR DA COLUNA DE ALTA PRESSÃO
    #TEM EXEMPLO EM Parameters_Update_Feed_Split_D_Eff_DIST_HPCOL


   # Atualizar Q a partir do resultado salvo no pd2 (condenser da coluna de alta pressão)
   pd_dict = Parameters_Update_DC_DC_Double_Effect_Optimizer.Set_Up_DC_DC_Double_Effect_Optimizer(pd_dict)
    #pd1 = equipamento 1 - coluna de baixa pressão
    #pd2 - equipamento 2 - coluna de alta pressão
   pd_dict['pd2']['Condenser_duty'] = results['reboiler_duty']

   #m_p['x_TOP'] = pd_dict['pd2']['condenser_duty'] 
   # caminho = Application.Tree.FindNode("\Data\Blocks\HPC\Subobjects\Design Specs\1\Input\VALUE\1")
   # Aspen.Tree.FindNode(rf'\Data\Blocks\{block_name}\Input\VALUE\1').Value = x_TOP  
    
   # m_p['reboiler_duty'] = Parameters_Update_DC_DC_Double_Effect_Optimizer.Set_Up_DC_DC_Double_Effect_Optimizer(pd_dict)
   # m_p['reboiler_dut'] = results['condenser_duty']


   return m_p
'''

'''
#Exemplo de Feed Split HPCOL - está no código: (OptiProcessCode-main #62 - Pamela)
#Parameters_Update_Feed_Split_D_Eff_DIST_HPCOL 
def Set_Up_HSTC(results, m_p):

    # Hot stream - shell side
    m_p['m_s'] = results['liquid_mass_flows'][0]/3600                       # Flow rate (kg/s)
    m_p['Tin_s'] = results['temperatures'][1]                               # Inlet temperature of the hot stream (K)
    m_p['Tout_s'] = results['temperatures'][0]                              # Outlet temperature of the hot stream (K)

    m_p['ro_s'] = results['condenser_hot_stream']['liquid_density']         # Liquid density (kg/m³)
    m_p['rov_s'] = results['condenser_hot_stream']['vapor_density']         # Vapor density (kg/m³)
    m_p['mi_s'] = results['condenser_hot_stream']['liquid_viscosity']       # Liquid viscosity (Pa.s)
    m_p['miv_s'] = results['condenser_hot_stream']['vapor_viscosity']       # Vapor viscosity (Pa.s)
    m_p['k_s'] = results['condenser_hot_stream']['thermal_conductivity']    # Thermal conductivity (W/(m.K))
    m_p['Hvap_s'] = results['condenser_duty']/m_p['m_s']                    # Vaporization enthalpy (J/kg)         

    Parameters_Update_HSTC.fun_LMTD(m_p)
    Parameters_Update_HSTC.fun_Prt(m_p)
    m_p['Q'] = results['condenser_duty']

    return m_p
'''



'''
# Sieve Tray (Problem Within) set up
def Set_Up_Sieve_Tray(results, m_p):

    # Liquid and vapor flows (converted from kg/hr to kg/s)
    m_p['Lw'] = (results['liquid_mass_flows'][1:-1]/3600).tolist()
    m_p['Vw'] = (results['vapor_mass_flows'][1:-1]/3600).tolist()

    # Hydraulics:
    m_p['rol'] = results['hydraulics']['density_liquid'].tolist()       # kg/m³
    m_p['rov'] = results['hydraulics']['density_vapor'].tolist()        # kg/m³
    m_p['sig'] = results['hydraulics']['surface_tension'].tolist()      # N/m

    # Number of stages:
    m_p['Nt'] = len(m_p['Lw'])

    return m_p
'''


# endregion
##################################################################################################################

