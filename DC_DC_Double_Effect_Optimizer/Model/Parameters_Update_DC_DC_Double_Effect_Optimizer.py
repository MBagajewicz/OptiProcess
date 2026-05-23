##################################################################################################################
# region Titles and Header
# Nature: 'Parameters_Calculations_List' and 'Example_Within_Set_Up' functions
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          28-Fev-2025     Alice Peccini             Original
#   0.2          29-Apr-2025     Mariana Mello             Update to fix error
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


    m_p['Aspen_engine'] = Calculations_DC_Aspen.fun_initial_Aspen(file_name, stream_name, block_name, comp_name,  
                                        z_feed, F_feed, Split)

    return m_p


  
def Set_Up_DC_DC_Double_Effect_Optimizer(Split, pd_dict, m_p):

    # ========================================= Parameters update =========================================
    # Tci_n - Inlet temperature of the cold stream of Equipment 1 (°C)
    # m_recirc_n - Mass flow rate of the recirculation stream (kg/s)
    # m_cs_n - Mass flow rate of cold stream (kg/s)

    #TOMAZIM - Escrever o split para as vazões (da coluna de baixa pressão)
    #pd guardar calor do reboiler da coulna de baixa pressão para a coluna de alta pressão
    #pd1 = equipamento 1 - coluna de baixa pressão
    #pd2 - equipamento 2 - coluna de alta pressão


    pd1 = pd_dict['pd1']
    pd2 = pd_dict['pd2']

    # Calculate the split feed
    pd1['Split'] = Split
    pd2['Split'] = (1-Split)

    # TOMAZIM - Como conectar com o Aspen???
    block_name = Calculations_DC_Aspen.fun_initial_Aspen(block_name)
    stream_name = Calculations_DC_Aspen.fun_initial_Aspen(stream_name)
    Aspen = Calculations_DC_Aspen.fun_initial_Aspen(Aspen)

    # Set feed stream data for the Column
    for comp in zip(m_p['Comp_name'], m_p['z_f']):   # Molar fractions for components
        molar_flow = Split * m_p['F_f']*m_p['z_f'] # Calculate molar flow for the component
        Aspen.Tree.FindNode(rf'\Data\Streams\{m_p['stream_name']}\Input\FLOW\MIXED\{comp}').Value = molar_flow     # Input molar flow for each component
        
    # Saving the Q heat load from reboiler to use in the condenser of the other Column
    pd1['reboiler_duty'] = Aspen.Tree.FindNode(rf'\Data\Blocks\{block_name}\Output\REB_DUTY').Value*1000/3600       # kJ/h to W
    pd2['condenser_duty'] = pd1['reboiler_duty']





    '''
    # Calculate the heat load
    Q = Calculations_HEX_heatload.HEX_heat_load(pd1['mh'], pd1['Cph'], pd1['Thi'], pd1['Tho'])
    pd1['Tci'] = Tci_n
    pd2['Tho'] = Tci_n
    pd1['mc'] = m_recirc_n
    pd1['ms'] = m_recirc_n
    pd2['mh'] = m_recirc_n
    pd2['ms'] = m_recirc_n
    #pd2['mc'] = m_cs_n
    #pd2['mt'] = m_cs_n

    # Calculate Tco of Equipment 1
    Tco_Eq1 = Q/(m_recirc_n * pd1['Cpc']) + Tci_n
    pd1['Tco'] = Tco_Eq1
    pd2['Thi'] = Tco_Eq1
    # Calculate Tco of Equipment 2
    #Tco_Eq2 = (Q/(m_cs_n*pd2['Cpc']) + pd2['Tci'])
    #Tco_Eq2 = (Q / (pd2['m_water'] * pd2['Cpc']) + pd2['Tci'])
    #pd2['Tco'] = Tco_Eq2

    # ==================================== Check LMTD feasibility ====================================
    try:
        # LMTD of Equipment1
        lmtd1 = Calculations_HEX_LMTD.HEX_lmtd(pd1['Thi'], pd1['Tho'], pd1['Tci'], pd1['Tco'])

        # LMTD of Equipment2
        lmtd2 = Calculations_HEX_LMTD.HEX_lmtd(pd2['Thi'], pd2['Tho'], pd2['Tci'], pd2['Tco'])

        feasibility = True

    except (ValueError, ZeroDivisionError):

        feasibility = False
    '''
        
# Mariana, eliminamos essa parte pois isso pode ser feito dentro das suas Set_Trimmings_Constraints (é um trimming)
    # ==================================== Check LMTD feasibility ====================================
    # if pd1['Type_Equipment'] == 'STHE':
    # # Calculate the correction factor of Equipment (STHE)
    #     try:
    #         calc_f_STHE1 = Calculations_STHE_correction_factor.STHE_correction_factor_no_npt(pd1['Thi'], pd1['Tho'],
    #                                                                                          pd1['Tci'], pd1['Tco'])
    #         if calc_f_STHE1 < 0.75:
    #             pd1['Nptmax'] = 1
    #
    #     except ValueError:
    #         pd1['Nptmax'] = 1
    # else:
    #     pd1['Nptmax'] = 6
    #
    # if pd2['Type_Equipment'] == 'STHE':
    # # Calculate the correction factor of Equipment (STHE)
    #     try:
    #         calc_f_STHE2 = Calculations_STHE_correction_factor.STHE_correction_factor_no_npt(pd2['Thi'], pd2['Tho'],
    #                                                                                          pd2['Tci'], pd2['Tco'])
    #         if calc_f_STHE2 < 0.75:
    #             pd2['Nptmax'] = 1
    #     except ValueError:
    #         pd2['Nptmax'] = 1
    #
    # else:
    #     pd2['Nptmax'] = 6
   
    #return pd_dict, feasibility
    return pd_dict, Aspen
# endregion
##################################################################################################################

