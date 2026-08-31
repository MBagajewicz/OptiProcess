#
#region Titles and Header
# Nature: Consistency calculations
# Methodology: Methods to verify HEX consistency
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          08-May-2025     Mariana Mello              Proposed
#   0.1          31-Aug-2026     Diego Oliva                Verifications of HEX consistency
##################################################################################################################
#endregion

# region Import
import sys
# endregion

#region Calculations
def verification_positive_variables(m_p, save_result):
    for key, value in m_p.items():
        if isinstance(value, (int, float)):
            if value < 0:
                save_result(f"Variable/Parameter '{key}' is not positive = {value}\n")
                sys.exit()
        else:
            # ignore string
            continue
    return m_p

def verification_DeltaTmin(m_p, save_result):
    if 'DeltaT_min' in m_p:
        pass
    else:
        m_p['DeltaT_min'] = 5
        save_result(f"DeltaTmin does not exist in the Model_Parameters. A default value of {m_p['DeltaT_min']} °C is adopted.\n")
    return m_p

def verification_Thi_Tho(m_p, save_result):
    if 'Thi' in m_p and 'Tho' in m_p:
        Thi = m_p['Thi']
        Tho = m_p['Tho']
        if Thi > Tho:
            pass
        else:
            save_result('Error data consistency: Tho > Thi\n')
            sys.exit()
        return m_p


def verification_Tco_Tci(m_p, save_result):
    if 'Tco' in m_p and 'Tci' in m_p:
        Tci = m_p['Tci']
        Tco = m_p['Tco']
        if Tco > Tci:
            pass
        else:
            save_result('Error data consistency: Tci > Tco\n')
            sys.exit()
        return m_p

def verification_Tco_Thi(m_p, save_result):
    if 'Tco' in m_p and 'Thi' in m_p:
        Thi = m_p['Thi']
        Tco = m_p['Tco']
        deltaTmin = m_p['DeltaT_min']
        if Tco < Thi-deltaTmin:
            pass
        else:
            save_result('Error data consistency: Tco > Thi - deltaTmin\n')
            sys.exit()
        return m_p

def verification_Tci_Tho(m_p, save_result):
    if 'Tci' in m_p and 'Tho' in m_p:
        Tho = m_p['Tho']
        Tci = m_p['Tci']
        deltaTmin = m_p['DeltaT_min']
        if Tci < Tho-deltaTmin:
            pass
        else:
            save_result('Error data consistency: Tci > Tho - deltaTmin\n')
            sys.exit()
        return m_p

def verification_heatload(m_p, save_result):
    try:
        Qh = m_p['mh'] * m_p['Cph'] * (m_p['Thi'] - m_p['Tho'])
        Qc = m_p['mc'] * m_p['Cpc'] * (m_p['Tco'] - m_p['Tci'])

        eps = 1e-4
        relative_error = abs((Qh - Qc) / Qh)

        # Calculate the corrected Tco required to close the energy balance
        Tco_old = m_p['Tco']
        Tco_new = Qh / (m_p['mc'] * m_p['Cpc']) + m_p['Tci']

        # Always update Tco so that Qh = Qc
        m_p['Tco'] = Tco_new

        if relative_error > eps:
            save_result(
                "\n"
                "============================================================\n"
                "WARNING: HEAT LOAD INCONSISTENCY DETECTED\n"
                "============================================================\n"
                f"Hot-side heat load  (Qh): {Qh:.6f} W\n"
                f"Cold-side heat load (Qc): {Qc:.6f} W\n"
                f"Relative difference       : {relative_error * 100:.6f} %\n"
                "\n"
                "The energy balance is outside the allowed tolerance.\n"
                "\n"
                f"Tco original: {Tco_old:.6f} °C\n"
                f"Tco corrected: {Tco_new:.6f} °C\n"
                "\n"
                "Tco has been modified to close the energy balance.\n"
                "The execution is paused for user verification.\n"
                "============================================================\n"
            )

            input("Press ENTER to continue...")

        else:
            save_result(
                "Heat load consistency verified within tolerance.\n"
                # f"Tco original: {Tco_old:.6f} °C\n"
                # f"Tco corrected: {Tco_new:.6f} °C\n"
            )

        return m_p

    except Exception as e:
        save_result(
            f"ERROR in verification_heatload: {e}\n"
        )
        return m_p

def verification_Tco_Thi_STHE(m_p, m_d, save_result):
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


#endregion