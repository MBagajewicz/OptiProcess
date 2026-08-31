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
# from Common_Equations_HEX import Calculations_HEX_Consistency
from Common.HEX_Calculations import Calculations_HEX_Consistency
from Common.HEX_Calculations import Calculations_HEX_Allocation
from Common.HEX_Calculations import Calculations_HEX_Tho_Tco
from STHE.Model.Model_Def_STHE import Model_STHE

# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions
#
# Adjustment of the data
def allocation(m_p):
    allocator = Calculations_HEX_Allocation.HEX_Allocation()
    return allocator.allocation(m_p)


def consistency(m_d, m_p, save_result):
    save_result('\n******* Testing consistency *******\n')

    def variables_bounds(m_d):
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
            save_result("WARNING: Variables out of range:")
            for var, vals in out_of_limit.items():
                save_result(f" - {var}: Invalid values {vals}\n")
        else:
            pass
        return m_d

    def variables_standard_values(m_d):
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
            save_result("WARNING: Variables do not match standard values")
            for var, vals in out.items():
                save_result(f" - {var}: Invalid values {vals}\n")
        else:
            pass
        return m_d

    def verification_Tco_Thi_STHE(m_p, m_d):
        if 'Tco' in m_p and 'Thi' in m_p and 'Tho' in m_p:
            Thi = m_p['Thi']
            Tco = m_p['Tco']
            Tho = m_p['Tho']
            deltaTmin = m_p['DeltaT_min']
            if Tco < Thi - deltaTmin:
                if Tco > Tho - deltaTmin:
                    save_result('Exchanger cannot be multipass (Tco > Tho - DeltaTmin). All passes > 1 are excluded.\n')
                    m_d['Discrete_Values_of_Variables'][2] = [1] # Npt = 1
                else:
                    pass
            else:
                save_result('Error data consistency: Tco > Thi - DeltaTmin\n')
                sys.exit()
            return m_p

    def verify_flag_inputs(m_p):
        if m_p['Property_Source'] not in ('CoolProp', 'User'):
            raise ValueError(
                f"Invalid Property_Source '{m_p['Property_Source']}'. "
                f"Expected 'CoolProp' or 'User'."
            )

        if m_p['Outlet_Temperature_Spec'] not in ('cold', 'hot'):
            raise ValueError(
                f"Invalid Outlet_Temperature_Spec "
                f"'{m_p['Outlet_Temperature_Spec']}'. "
                f"Expected 'cold' or 'hot'."
            )

        if 'Tho' not in m_p and m_p['Outlet_Temperature_Spec'] == 'hot':
            raise ValueError(
                f"You define 'Outlet_Temperature_Spec' as:  "
                f"'{m_p['Outlet_Temperature_Spec']}'. "
                f"You have to input 'Tho'."
            )
        if 'Tco' not in m_p and m_p['Outlet_Temperature_Spec'] == 'cold':
            raise ValueError(
                f"You define 'Outlet_Temperature_Spec' as:  "
                f"'{m_p['Outlet_Temperature_Spec']}'. "
                f"You have to input 'Tco'."
            )
        
    verif0 = verify_flag_inputs(m_p)
    verif1 = Calculations_HEX_Tho_Tco.HEX_Tho_Tco().HEX_Tho_Tco(m_p)
    verif2 = Calculations_HEX_Consistency.verification_positive_variables(m_p, save_result)
    verif3 = Calculations_HEX_Consistency.verification_DeltaTmin(m_p, save_result)
    # verif4 = Calculations_HEX_Consistency.verification_heatload(m_p, save_result)
    verif5 = Calculations_HEX_Consistency.verification_Thi_Tho(m_p, save_result)
    verif6 = Calculations_HEX_Consistency.verification_Tco_Tci(m_p, save_result)
    verif7 = verification_Tco_Thi_STHE(m_p, m_d)
    verif8 = Calculations_HEX_Consistency.verification_Tci_Tho(m_p, save_result)
    verif9 = variables_bounds(m_d)
    verif10 = variables_standard_values(m_d)

    return m_d, m_p


# endregion
##################################################################################################################

