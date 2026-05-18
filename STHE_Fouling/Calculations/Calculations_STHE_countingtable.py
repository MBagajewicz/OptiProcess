###################################################################################################################
#region STHE Counting Table Function
# Purpose: Calculate total number of tubes (Ntt) for a given shell diameter, tube layout, and configuration
# Applies: Bell or Kern methods for bundle geometry estimation
###################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello             Proposed
#   0.2          27-Feb-2025     Mariana Mello             Add options of Shell Method
#   0.3          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
#   0.4          02-Jul-2025     Augusto Vieira            Fix unbound KNPt and structure per method
###################################################################################################################
#endregion

#region Import Library
from math import sqrt, pi
import numpy as np
#endregion

#region Counting Table Main Function
def STHE_counting_table(Ds, dte, Npt, rp, lay, m_p):
    #### Ensure array formatting for element-wise operations
    Ds   = np.atleast_1d(Ds)
    dte  = np.atleast_1d(dte)
    Npt  = np.atleast_1d(Npt)
    rp   = np.atleast_1d(rp)
    lay  = np.atleast_1d(lay)

    if m_p['Shell_Method'] == "Bell":
        #### Calculate shell-to-bundle clearance (Lbb) based on empirical correlation
        Lbb = 0.0048 * Ds + 0.0128

        #### Adjust geometric constant based on layout (1.0 for 90°, 0.866 for 45°)
        C1 = np.ones_like(lay)
        C1[lay == 2] = 0.866

        #### Base tube count estimate (before leakage corrections)
        Ntt1 = (0.78 * (Ds - Lbb - dte)**2) / (C1 * (rp * dte)**2)

        #### Leakage correction factor psi using lookup tables
        ppDs = [0.2050, 0.3048, 0.3874, 0.4890, 0.5906, 0.6858, 0.7874, 0.8382, 0.889,
                0.9398, 0.9906, 1.0668, 1.143, 1.2192, 1.3716, 1.524, 2.0]
        pppsi_1 = [0]*17
        pppsi_2 = [0.18, 0.09, 0.06, 0.046, 0.042, 0.036, 0.034, 0.033, 0.032,
                   0.03, 0.028, 0.025, 0.024, 0.0235, 0.02, 0.018, 0.018]
        pppsi_4 = [0.3, 0.2, 0.16, 0.125, 0.118, 0.11, 0.095, 0.090, 0.085,
                   0.08, 0.075, 0.073, 0.071, 0.0650, 0.06, 0.050, 0.05]
        pppsi_6 = [0.4, 0.22, 0.18, 0.168, 0.158, 0.148, 0.122, 0.118, 0.11,
                   0.105, 0.098, 0.090, 0.088, 0.0870, 0.08, 0.074, 0.074]

        psi = np.zeros_like(Ds)
        for i in range(len(ppDs)):
            match = np.isclose(Ds, ppDs[i], atol=1e-4)
            psi[match & (Npt == 1)] = pppsi_1[i]
            psi[match & (Npt == 2)] = pppsi_2[i]
            psi[match & (Npt == 4)] = pppsi_4[i]
            psi[match & (Npt == 6)] = pppsi_6[i]

        #### Final count after shell-bundle leakage correction
        Ntt = np.round(Ntt1 * (1 - psi))

    elif m_p['Shell_Method'] == "Kern":
        #### Correction factor for number of passes
        KNPt = sqrt(0.9) * np.ones_like(Npt)
        KNPt[Npt == 1] = sqrt(0.93)

        #### Bundle diameter
        Db = Ds * KNPt

        #### Tube pitch
        ltp = rp * dte

        #### Layout correction factor
        Klay = np.ones_like(lay)
        Klay[lay == 2] = 0.866

        #### Tube count for Kern method
        Ntt = np.round((pi * Db**2) / (4 * ltp**2 * Klay))

    return Ntt
#endregion
