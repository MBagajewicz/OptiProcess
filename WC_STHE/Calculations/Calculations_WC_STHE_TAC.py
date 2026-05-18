#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          07-Feb-2024     Mariana Mello             Proposed
#   0.2          06-May-2025     Mariana Mello             Revision from paper
#   0.3          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
##################################################################################################################
#endregion


#region Import Library
from STHE.Calculations import (
    Calculations_STHE_DeltaPtubeside,
    Calculations_STHE_area,
    Calculations_STHE_DeltaPshellside)
#endregion

#region Calculations

def WC_STHE_TAC(Fw, rot, mit, thk, Ds, dte, Npt, rp, lay, L, pcw, pc, roc, eta, cf, cv, alpha, Nop, int_rate, n, m_p, ms, ros, mis, Nb, Bc):
    DPt = Calculations_STHE_DeltaPtubeside.STHE_tubeside_DeltaP(Fw, rot, mit, thk, Ds, dte, Npt, rp, lay, L, m_p)
    #print('DPt',DPt)
    DPs = Calculations_STHE_DeltaPshellside.STHE_shellside_DeltaP(ms, ros, mis, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)
    #print('DPs', DPs)
    A = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)
    #print('A',A)
    Cop_w = ((Fw/rot)*(DPt/1000))/eta
    #print('Cop_w',Cop_w)
    Cop_p = ((ms/ros)*(DPs/1000))/eta
    #print('Cop_p',Cop_p)
    OPEX = Nop*(pcw*Fw*3600 + pc*(Cop_p+Cop_w))
    #print('OPEX',OPEX)
    CAPEX = cf + cv*(A**alpha)
    #print('CAPEX',CAPEX)
    af = ((int_rate*(1+int_rate)**n))/(((1+int_rate)**n) - 1)
    #print('af',af)
    TAC = OPEX + af*CAPEX
    return TAC

#endregion