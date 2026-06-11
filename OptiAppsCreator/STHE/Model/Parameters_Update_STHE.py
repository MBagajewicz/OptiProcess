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
from Common_Equations_HEX import Calculations_HEX_Consistency
from consistency_utils import normalize_config, run_test
from STHE.Model.Model_Def_STHE import Model_STHE
# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions
#
# Adjustment of the data

def allocation(m_p):
    if m_p['yfluid'] == 'cold_stream':
        m_p['mt'] = m_p['mc']
        m_p['rot'] = m_p['roc']
        m_p['Cpt'] = m_p['Cpc']
        m_p['mit'] = m_p['mic']
        m_p['kt'] = m_p['kc']
        m_p['Rft'] = m_p['Rfc']
        m_p['DPtdisp'] = m_p['DPcdisp']

        m_p['ms'] = m_p['mh']
        m_p['ros'] = m_p['roh']
        m_p['Cps'] = m_p['Cph']
        m_p['mis'] = m_p['mih']
        m_p['ks'] = m_p['kh']
        m_p['Rfs'] = m_p['Rfh']
        m_p['DPsdisp'] = m_p['DPhdisp']

    elif m_p['yfluid'] == 'hot_stream':
        m_p['mt'] = m_p['mh']
        m_p['rot'] = m_p['roh']
        m_p['Cpt'] = m_p['Cph']
        m_p['mit'] = m_p['mih']
        m_p['kt'] = m_p['kh']
        m_p['Rft'] = m_p['Rfh']
        m_p['DPtdisp'] = m_p['DPhdisp']

        m_p['ms'] = m_p['mc']
        m_p['ros'] = m_p['roc']
        m_p['Cps'] = m_p['Cpc']
        m_p['mis'] = m_p['mic']
        m_p['ks'] = m_p['kc']
        m_p['Rfs'] = m_p['Rfc']
        m_p['DPsdisp'] = m_p['DPcdisp']
    
    return m_p

def consistency(m_d, m_p, save_result, consistency_config=None, consistency_report=None):
    save_result('\n******* Testing consistency *******\n')
    config = normalize_config('STHE', consistency_config)

    def variables_bounds(m_d, test_save_result):
        m_i = Model_STHE['Model_Info']
        variables = m_i['List_of_Variables']

        discrete_values = m_d['Discrete_Values_of_Variables']
        standard_values = m_i['Standard_Variables_Values']
        tol = 0.001

        out_of_limit = {}

        for name, values in zip(variables, discrete_values):
            standard_values_verif = standard_values.get(name, [])
            if not standard_values_verif:
                continue
            min_val = min(standard_values_verif)
            max_val = max(standard_values_verif)
            for v in values:
                if v < (min_val-tol) or v > (max_val+tol):
                    if name not in out_of_limit:
                        out_of_limit[name] = []
                    out_of_limit[name].append(v)

        if out_of_limit:
            test_save_result("WARNING: Variables out of range:")
            for var, vals in out_of_limit.items():
                test_save_result(f" - {var}: Invalid values {vals}\n")
        else:
            pass
        return m_d

    def variables_standard_values(m_d, test_save_result):
        m_i = Model_STHE['Model_Info']
        variables = m_i['List_of_Variables']

        discrete_values = m_d['Discrete_Values_of_Variables']
        standard_values = m_i['Standard_Variables_Values']
        tol = 0.001
        out = {}
        for name, values in zip(variables, discrete_values):
            standard_values_verif = standard_values.get(name, [])
            for v in values:
                value_c = False
                for std_val in standard_values_verif:
                    if abs(v - std_val) <= tol:
                        value_c = True
                if not value_c:
                    if name not in out:
                        out[name] = []
                    out[name].append(v)
        if out:
            test_save_result("WARNING: Variables do not match standard values")
            for var, vals in out.items():
                test_save_result(f" - {var}: Invalid values {vals}\n")
        else:
            pass
        return m_d

    def verification_Tco_Thi_STHE(m_p, m_d, test_save_result):
        if 'Tco' in m_p and 'Thi' in m_p and 'Tho' in m_p:
            Thi = m_p['Thi']
            Tco = m_p['Tco']
            Tho = m_p['Tho']
            deltaTmin = m_p['DeltaT_min']
            if Tco < Thi - deltaTmin:
                if Tco > Tho - deltaTmin:
                    test_save_result('Exchanger cannot be multipass (Tco > Tho - DeltaTmin). All passes > 1 are excluded.\n')
                    m_d['Discrete_Values_of_Variables'][2] = [1] # Npt = 1
                else:
                    pass
            else:
                test_save_result('Error data consistency: Tco > Thi - DeltaTmin\n')
                sys.exit()
            return m_p

    run_test(model='STHE', test_id='positive_variables', label='Positive numeric variables', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_positive_variables(m_p, sr))
    run_test(model='STHE', test_id='delta_t_min', label='Minimum temperature difference', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_DeltaTmin(m_p, sr))
    run_test(model='STHE', test_id='heatload', label='Heat load balance', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_heatload(m_p, sr))
    run_test(model='STHE', test_id='thi_tho', label='Hot stream cools down (Thi > Tho)', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_Thi_Tho(m_p, sr))
    run_test(model='STHE', test_id='tco_tci', label='Cold stream heats up (Tco > Tci)', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_Tco_Tci(m_p, sr))
    run_test(model='STHE', test_id='tco_thi_sthe', label='STHE cold outlet vs hot inlet approach', config=config, report=consistency_report, save_result=save_result, call=lambda sr: verification_Tco_Thi_STHE(m_p, m_d, sr))
    run_test(model='STHE', test_id='tci_tho', label='Cold inlet vs hot outlet approach', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_Tci_Tho(m_p, sr))
    run_test(model='STHE', test_id='variables_bounds', label='Discrete variables inside standard bounds', config=config, report=consistency_report, save_result=save_result, call=lambda sr: variables_bounds(m_d, sr))
    run_test(model='STHE', test_id='variables_standard_values', label='Discrete variables match standard values', config=config, report=consistency_report, save_result=save_result, call=lambda sr: variables_standard_values(m_d, sr))

    return m_d, m_p


# endregion
##################################################################################################################
