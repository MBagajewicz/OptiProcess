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
##################################################################################################################

import numpy as np
from STHE.Calculations import  Calculations_STHE_htubeside
from scipy.optimize import root_scalar
##################################################################################################################
#endregion

##################################################################################################################
#region Fouling Thickness from Resistance (Inverse Calculation)

# Compute residual for fouling thickness function from a given thermal resistance Rft [m²·K/W]
def Rft_thk_t_func_residue(mt, rot, Cpt, mit, kt, thk, yfluid,
                           Ds, dte, Npt, rp, lay, L, m_p, Rft, ft_thk):

    kft = m_p["kft"]                            # Fouling thermal conductivity [W/m·K]
    dti = dte - 2 * thk                         # Tube internal diameter after wall thickness
    df = dti - 2 * ft_thk                       # Flow diameter with fouling deposit

    htf = Calculations_STHE_htubeside.STHE_h_tubeside(
        mt, rot, Cpt, mit, kt, thk, yfluid,
        Ds, dte, Npt, rp, lay, L, m_p, ft_thk ) # Fouled tube-side heat transfer coefficient

    htc = Calculations_STHE_htubeside.STHE_h_tubeside(
        mt, rot, Cpt, mit, kt, thk, yfluid,
        Ds, dte, Npt, rp, lay, L, m_p, 0)       # Clean tube-side heat transfer coefficient

    term_fouling = dti / (2 * kft) * np.log(dti / df)       # fouling_conductive_resistance
    term_conv_fouled = dti / (df * htf)                          # dirt_convective_resistance
    term_conv_clean = 1 / htc                                  # clean_convective_resistance

    residual = Rft - (term_fouling + term_conv_fouled - term_conv_clean)
    # Residual = actual Rft - modeled Rft for a given ft_thk

    return residual

# Solve for fouling thickness ft_thk from known Rft using Brent method [m]
def solve_ft_thk(mt, rot, Cpt, mit, kt, thk, yfluid,
                 Ds, dte, Npt, rp, lay, L, m_p, Rft):

    epsilon = 1e-10                                # Minimum Numerical thickness - to avoid division by zero
    lower_bound = epsilon                          # Minimum fouling thickness [m]
    upper_bound = ((dte - 2 * thk) / 2) - epsilon  # Maximum physically feasible ft_thk [m]

    # Define residual function to find root
    def residual(x):
        return Rft_thk_t_func_residue(mt, rot, Cpt, mit, kt, thk, yfluid, Ds, dte, Npt, rp, lay, L, m_p, Rft, x)

    f_lo = residual(lower_bound)
    f_hi = residual(upper_bound)

    if f_lo * f_hi > 0:
        print("Invalid interval for Brent")
        return np.nan                           # No sign change → no root in bracket

    try:
        result = root_scalar(
            residual,
            method='brentq',
            bracket=[lower_bound, upper_bound],
            xtol=1e-8,                          # absolute tolerance on ft_thk convergence
            rtol=1e-4,                          # relative tolerance on ft_thk convergence
            maxiter=100
        )
        if result.converged:
            return result.root                 # Return converged root
        else:
            print("Brent method did not converge.")
            return np.nan
    except Exception as e:                     # handling errors to avoid crash
        print(f"Error while solving ft_thk: {e}") 
        return np.nan

#endregion
##################################################################################################################
