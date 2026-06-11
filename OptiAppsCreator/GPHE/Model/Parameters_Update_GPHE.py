##################################################################################################################
# region Titles and Header
# Nature: 'Parameters_Calculations_List' and 'Example_Within_Set_Up' functions
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          28-Fev-2025     Alice Peccini             Original
#   0.2          12-May-2025     Mariana Mello             Add data consistency
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
from Common_Equations_HEX import Calculations_HEX_Consistency
from consistency_utils import normalize_config, run_test
from GPHE.Model.Model_Def_GPHE import Model_GPHE
# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions

def consistency(m_d, m_p, save_result, consistency_config=None, consistency_report=None):
    save_result('\n******* Testing consistency *******\n')
    config = normalize_config('GPHE', consistency_config)

    def variables_bounds(m_d, test_save_result):
        m_i = Model_GPHE['Model_Info']
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
        m_i = Model_GPHE['Model_Info']
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

    run_test(model='GPHE', test_id='positive_variables', label='Positive numeric variables', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_positive_variables(m_p, sr))
    run_test(model='GPHE', test_id='delta_t_min', label='Minimum temperature difference', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_DeltaTmin(m_p, sr))
    run_test(model='GPHE', test_id='heatload', label='Heat load balance', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_heatload(m_p, sr))
    run_test(model='GPHE', test_id='thi_tho', label='Hot stream cools down (Thi > Tho)', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_Thi_Tho(m_p, sr))
    run_test(model='GPHE', test_id='tco_tci', label='Cold stream heats up (Tco > Tci)', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_Tco_Tci(m_p, sr))
    run_test(model='GPHE', test_id='tci_tho', label='Cold inlet vs hot outlet approach', config=config, report=consistency_report, save_result=save_result, call=lambda sr: Calculations_HEX_Consistency.verification_Tci_Tho(m_p, sr))
    run_test(model='GPHE', test_id='variables_bounds', label='Discrete variables inside standard bounds', config=config, report=consistency_report, save_result=save_result, call=lambda sr: variables_bounds(m_d, sr))
    run_test(model='GPHE', test_id='variables_standard_values', label='Discrete variables match standard values', config=config, report=consistency_report, save_result=save_result, call=lambda sr: variables_standard_values(m_d, sr))

    return m_d, m_p


# endregion
##################################################################################################################
