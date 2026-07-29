#region Titles and Header
# Nature: Calculation
# Methodology: SPHE
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Javier Francesconi        Original Version
#   
##################################################################################################################
#endregion


#region Import Library
import numpy as np
#endregion

#region Calculations
def SPHE_Nusselt(Re, Pr, De, Dh, L):
    """
    Calculate the Nusselt number for scalar or NumPy array inputs.
    """

    Re, Pr, De, Dh, L = np.broadcast_arrays(
        np.asarray(Re, dtype=float),
        np.asarray(Pr, dtype=float),
        np.asarray(De, dtype=float),
        np.asarray(Dh, dtype=float),
        np.asarray(L, dtype=float),
    )

    if np.any(Dh <= 0):
        raise ValueError("Dh must be greater than zero.")
    if np.any(De <= 0):
        raise ValueError("De must be greater than zero.")
    if np.any(L <= 0):
        raise ValueError("L must be greater than zero.")
    if np.any(Re < 0):
        raise ValueError("Re must be non-negative.")
    if np.any(Pr <= 0):
        raise ValueError("Pr must be greater than zero.")

    Reynolds_Critical = 20000.0 * (De / Dh) ** 0.32

    Nu = np.empty_like(Re, dtype=float)

    turbulent = Re >= Reynolds_Critical
    laminar = ~turbulent

    Nu[turbulent] = (
        0.023
        * (1.0 + 3.54 * De[turbulent] / Dh[turbulent])
        * Re[turbulent] ** (4.0 / 5.0)
        * Pr[turbulent] ** (1.0 / 3.0)
    )

    Nu[laminar] = (
        1.86
        * Re[laminar] ** (1.0 / 3.0)
        * Pr[laminar] ** (1.0 / 3.0)
        * (L[laminar] / De[laminar]) ** (-1.0 / 3.0)
    )

    return Nu.item() if Nu.ndim == 0 else Nu

#endregion
