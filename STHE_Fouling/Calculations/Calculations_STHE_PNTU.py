#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          02-Jul-2025     Augusto Vieira            Original


##################################################################################################################
#endregion

#region Import Library
import numpy as np
from STHE.Calculations import Calculations_STHE_U, Calculations_STHE_area
#endregion



##################################################################################################################
#region NTU and PNTU Functions

def STHE_NTU(mt, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs,
             thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk):
    # Calculates the Number of Transfer Units (NTU) for the STHE
    # It is based on overall U value (accounting fouling) and effective heat transfer area

    A = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)  # Heat transfer area [m²]
    U = Calculations_STHE_U.STHE_overall_coefficient(
        mt, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs,
        thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk
    )  # Overall heat transfer coefficient [W/m².K]

    Ct = mt * Cpt   # Tube-side heat capacity rate [W/K]
    Cs = ms * Cps   # Shell-side heat capacity rate [W/K]
    Cmin = np.minimum(Ct, Cs)  # Minimum heat capacity rate

    return U * A / Cmin  # NTU definition

def STHE_PNTU(mt, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs,
              thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, Nps, m_p, ft_thk):
    # Calculates the thermal effectiveness (ε) using the NTU method with correction for multiple passes

    NTU = STHE_NTU(mt, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs,
                   thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk)

    Ct = mt * Cpt   # Tube-side heat capacity rate [W/K]
    Cs = ms * Cps   # Shell-side heat capacity rate [W/K]
    Cmin = np.minimum(Ct, Cs)  # Minimum heat capacity rate
    Cmax = np.maximum(Ct, Cs)  # Maximum heat capacity rate
    Cr = Cmin / Cmax           # Capacity rate ratio

    # Base effectiveness for counter-flow or parallel-flow approximation
    Epsolon = np.where(
        Cr == 1,
        NTU / (1 + NTU),
        (1 - np.exp(-NTU * (1 - Cr))) / (1 - Cr * np.exp(-NTU * (1 - Cr)))
    )

    # Apply correction if number of tube passes is 1 or 2
    if Nps in [1, 2]:
        NTU_mod = NTU / Nps  # NTU corrected for number of passes

        # Base effectiveness expression for 1 or 2 pass exchangers
        Epsolon_base = 2 / (
            1 + Cr + np.sqrt(1 + Cr**2) *
            (1 + np.exp(-NTU_mod * np.sqrt(1 + Cr**2))) /
            (1 - np.exp(-NTU_mod * np.sqrt(1 + Cr**2)))
        )

        # If 2 passes, apply further correction
        if Nps == 2:
            Epsolon_corr = (
                (1 - Epsolon_base * Cr)**Nps - (1 - Epsolon_base)**Nps
            ) / (
                (1 - Epsolon_base * Cr)**Nps - Cr * (1 - Epsolon_base)**Nps
            )
        else:
            Epsolon_corr = Epsolon_base

        # Apply correction only when more than 1 tube pass exists
        Epsolon = np.where(Npt > 1, Epsolon_corr, Epsolon)

    return Epsolon  # Thermal effectiveness

#endregion
##################################################################################################################
