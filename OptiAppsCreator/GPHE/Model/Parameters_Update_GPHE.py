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
from GPHE.Model.Model_Def_GPHE import Model_GPHE
# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions

def consistency(m_d, m_p, save_result):
    save_result('\n******* Testing consistency *******\n')

    def build_report(results):
        mandatory_failures = [r for r in results if r.get('mandatory') and not r.get('passed')]
        warnings = [r for r in results if not r.get('mandatory') and not r.get('passed')]
        return {
            'passed': len(mandatory_failures) == 0,
            'results': results,
            'mandatory_failures': mandatory_failures,
            'warnings': warnings,
        }

    def variables_bounds(m_d):
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
            message = "WARNING: Variables out of range:"
            save_result(message)
            for var, vals in out_of_limit.items():
                detail = f" - {var}: Invalid values {vals}"
                message += detail
                save_result(f"{detail}\n")
            return Calculations_HEX_Consistency.consistency_result("variables_bounds", "Discrete variables inside standard bounds", False, False, message)
        else:
            pass
        return Calculations_HEX_Consistency.consistency_result("variables_bounds", "Discrete variables inside standard bounds", True, False)

    def variables_standard_values(m_d):
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
            message = "WARNING: Variables do not match standard values"
            save_result(message)
            for var, vals in out.items():
                detail = f" - {var}: Invalid values {vals}"
                message += detail
                save_result(f"{detail}\n")
            return Calculations_HEX_Consistency.consistency_result("variables_standard_values", "Discrete variables match standard values", False, False, message)
        else:
            pass
        return Calculations_HEX_Consistency.consistency_result("variables_standard_values", "Discrete variables match standard values", True, False)

    results = []
    results.append(Calculations_HEX_Consistency.verification_positive_variables(m_p, save_result))
    results.append(Calculations_HEX_Consistency.verification_DeltaTmin(m_p, save_result))
    results.append(Calculations_HEX_Consistency.verification_heatload(m_p, save_result))
    results.append(Calculations_HEX_Consistency.verification_Thi_Tho(m_p, save_result))
    results.append(Calculations_HEX_Consistency.verification_Tco_Tci(m_p, save_result))
    results.append(Calculations_HEX_Consistency.verification_Tci_Tho(m_p, save_result))
    results.append(variables_bounds(m_d))
    results.append(variables_standard_values(m_d))

    return m_d, m_p, build_report(results)


# endregion
##################################################################################################################
