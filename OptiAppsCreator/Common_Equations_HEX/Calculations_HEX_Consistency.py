#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          08-May-2025     Mariana Mello              Proposed

##################################################################################################################
#endregion

#region Calculations
def consistency_result(test_id, label, passed=True, mandatory=False, message=""):
    return {
        "id": test_id,
        "label": label,
        "passed": passed,
        "mandatory": mandatory,
        "message": message,
    }


def verification_positive_variables(m_p, save_result):
    for key, value in m_p.items():
        if isinstance(value, (int, float)):
            if value < 0:
                message = f"Variable/Parameter '{key}' is not positive = {value}"
                save_result(f"{message}\n")
                return consistency_result("positive_variables", "Positive numeric variables", False, True, message)
        else:
            # ignore string
            continue
    return consistency_result("positive_variables", "Positive numeric variables", True, True)

def verification_DeltaTmin(m_p, save_result):
    if 'DeltaT_min' in m_p:
        pass
    else:
        m_p['DeltaT_min'] = 5
        message = f"DeltaTmin does not exist in the Model_Parameters. A default value of {m_p['DeltaT_min']} °C is adopted."
        save_result(f"{message}\n")
        return consistency_result("delta_t_min", "Minimum temperature difference", False, False, message)
    return consistency_result("delta_t_min", "Minimum temperature difference", True, False)

def verification_Thi_Tho(m_p, save_result):
    if 'Thi' in m_p and 'Tho' in m_p:
        Thi = m_p['Thi']
        Tho = m_p['Tho']
        if Thi > Tho:
            pass
        else:
            message = 'Error data consistency: Tho > Thi'
            save_result(f'{message}\n')
            return consistency_result("thi_tho", "Hot stream cools down (Thi > Tho)", False, True, message)
    return consistency_result("thi_tho", "Hot stream cools down (Thi > Tho)", True, True)


def verification_Tco_Tci(m_p, save_result):
    if 'Tco' in m_p and 'Tci' in m_p:
        Tci = m_p['Tci']
        Tco = m_p['Tco']
        if Tco > Tci:
            pass
        else:
            message = 'Error data consistency: Tci > Tco'
            save_result(f'{message}\n')
            return consistency_result("tco_tci", "Cold stream heats up (Tco > Tci)", False, True, message)
    return consistency_result("tco_tci", "Cold stream heats up (Tco > Tci)", True, True)

def verification_Tco_Thi(m_p, save_result):
    if 'Tco' in m_p and 'Thi' in m_p:
        Thi = m_p['Thi']
        Tco = m_p['Tco']
        deltaTmin = m_p['DeltaT_min']
        if Tco < Thi-deltaTmin:
            pass
        else:
            message = 'Error data consistency: Tco > Thi - deltaTmin'
            save_result(f'{message}\n')
            return consistency_result("tco_thi", "Cold outlet vs hot inlet approach", False, True, message)
    return consistency_result("tco_thi", "Cold outlet vs hot inlet approach", True, True)

def verification_Tci_Tho(m_p, save_result):
    if 'Tci' in m_p and 'Tho' in m_p:
        Tho = m_p['Tho']
        Tci = m_p['Tci']
        deltaTmin = m_p['DeltaT_min']
        if Tci < Tho-deltaTmin:
            pass
        else:
            message = 'Error data consistency: Tci > Tho - deltaTmin'
            save_result(f'{message}\n')
            return consistency_result("tci_tho", "Cold inlet vs hot outlet approach", False, True, message)
    return consistency_result("tci_tho", "Cold inlet vs hot outlet approach", True, True)

def verification_heatload(m_p, save_result):
    try:
        Qh = m_p['mh']*m_p['Cph']*(m_p['Thi']-m_p['Tho'])
        Qc = m_p['mc']*m_p['Cpc']*(m_p['Tco']-m_p['Tci'])
        eps = 1e-4
        # 0.01% difference is tolerated
        if abs((Qh - Qc)/Qh) > eps:
            pass
        else:
            m_p['Tco'] = Qh/(m_p['mc']*m_p['Cpc']) + m_p['Tci']
            message = f"Error data consistency: heat load is inconsistent with the energy balance (within 0.01%). A new value for Tco = {m_p['Tco']} is used."
            save_result(f"{message}\n")
            return consistency_result("heatload", "Heat load balance", False, False, message)
    except:
        pass
    return consistency_result("heatload", "Heat load balance", True, False)


#endregion
