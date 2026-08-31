#region Titles and Header
# Nature: General consistency checking with standard values in model
# Methodology: Methods to check consistency between discretizations and standard values
######################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          31-Aug-2026     Diego Oliva               Proposed to check consistency with standard values in Model
#                                                          Methods were taken from generic
######################################################################################################################
#endregion

from Common.Utils.Model_Loader import Model_Loader

def variables_bounds(m_d, save_result):
    Imported_Model = Model_Loader.load(m_d['Type_Equipment'])
    m_i = Imported_Model['Model_Info']
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
        save_result("WARNING: Variables out of range:")
        for var, vals in out_of_limit.items():
            save_result(f" - {var}: Invalid values {vals}\n")
    else:
        pass
    return m_d

def variables_standard_values(m_d, save_result):
    Imported_Model = Model_Loader.load(m_d['Type_Equipment'])
    m_i = Imported_Model['Model_Info']
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
        save_result("WARNING: Variables do not match standard values")
        for var, vals in out.items():
            save_result(f" - {var}: Invalid values {vals}\n")
    else:
        pass
    return m_d
