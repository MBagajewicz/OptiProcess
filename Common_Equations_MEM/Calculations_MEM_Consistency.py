#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          08-May-2025     Mariana Mello              Proposed

##################################################################################################################
#endregion

# region Import
import sys
from math import pi
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

def verification_Pfeed_Pperm(m_p, save_result):
    if 'Pf' in m_p and 'Pperm' in m_p:
        Pf = m_p['Pf']
        Pperm = m_p['Pperm']
        if Pf > Pperm:
            pass
        else:
            save_result('Error data consistency: Pf > Pperm\n')
            sys.exit()
        return m_p

def verification_Cross_Sectional_Area_Shell(m_p, save_result):
    if 'D' in m_p and 'D_o' in m_p and 'Ntf' in m_p:
        D = m_p['D']
        D_o = m_p['D_o']
        Ntf = m_p['Ntf']

        S = (pi / 4) * (D ** 2 - Ntf * D_o ** 2)
        if S > 0:
            pass
        else:
            save_result("Error data consistency: Cross-sectional area < 0 i.e. Fibers don't fit in shell\n")
            sys.exit()
        return m_p


#endregion