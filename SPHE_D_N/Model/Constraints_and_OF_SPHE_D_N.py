##################################################################################################################
# region Titles and Header
# Nature: Constraints and objective function for the turn-based SPHE_D_N model
# Methodology: Set trimming and enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         05-Jul-2026      ChatGPT                   Add N-based wrapper around SPHE_D model
##################################################################################################################
# INPUT: Define constraints and objective function using N as optimization variable
##################################################################################################################

# region Import Library
import numpy as np

from SPHE_D.Model import Constraints_and_OF_SPHE_D as SPHE_D_base
# endregion


def _length_from_turns(N, ds, dh, dc, m_p):
    """Return the spiral channel length corresponding to N turns.

    The original SPHE_D model uses L as the first optimization variable.
    SPHE_D_N exposes N as the first optimization variable and converts N to
    L before reusing the validated SPHE_D constraints and objective function.
    The implementation is vectorized because the Set Trimming engine may pass
    either scalar candidates or NumPy arrays of candidates.
    """
    thk = m_p['thk']
    N_arr, ds_arr, dh_arr, dc_arr = np.broadcast_arrays(N, ds, dh, dc)

    a = ds_arr / 2.0 + thk + dh_arr + thk / 2.0
    b = (dh_arr + dc_arr + 2.0 * thk) / (2.0 * np.pi)
    theta = N_arr * 2.0 * np.pi

    u0 = a
    u1 = a + b * theta

    def primitive(u):
        return (
            u * np.sqrt(u**2 + b**2)
            + b**2 * np.log(u + np.sqrt(u**2 + b**2))
        )

    L = (primitive(u1) - primitive(u0)) / (2.0 * b)

    if np.ndim(L) == 0:
        return float(L)

    return L


def _as_length_arguments(N, H, ds, dh, dc, m_p):
    """Return the length-based argument tuple expected by SPHE_D."""
    L = _length_from_turns(N, ds, dh, dc, m_p)
    return L, H, ds, dh, dc, m_p


def LH_lb(N, H, ds, dh, dc, m_p):
    """Lower bound on L/H, with L calculated from N."""
    return SPHE_D_base.LH_lb(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def LH_ub(N, H, ds, dh, dc, m_p):
    """Upper bound on L/H, with L calculated from N."""
    return SPHE_D_base.LH_ub(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def vh_lb(N, H, ds, dh, dc, m_p):
    """Lower bound on hot-channel velocity."""
    return SPHE_D_base.vh_lb(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def vh_ub(N, H, ds, dh, dc, m_p):
    """Upper bound on hot-channel velocity."""
    return SPHE_D_base.vh_ub(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def vc_lb(N, H, ds, dh, dc, m_p):
    """Lower bound on cold-channel velocity."""
    return SPHE_D_base.vc_lb(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def vc_ub(N, H, ds, dh, dc, m_p):
    """Upper bound on cold-channel velocity."""
    return SPHE_D_base.vc_ub(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def Reh_lb(N, H, ds, dh, dc, m_p):
    """Lower bound on hot-channel Reynolds number."""
    return SPHE_D_base.Reh_lb(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def Rec_lb(N, H, ds, dh, dc, m_p):
    """Lower bound on cold-channel Reynolds number."""
    return SPHE_D_base.Rec_lb(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def dltph_ub(N, H, ds, dh, dc, m_p):
    """Upper bound on hot-channel pressure drop."""
    return SPHE_D_base.dltph_ub(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def dltpc_ub(N, H, ds, dh, dc, m_p):
    """Upper bound on cold-channel pressure drop."""
    return SPHE_D_base.dltpc_ub(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def Areq(N, H, ds, dh, dc, m_p):
    """Required heat-transfer-area constraint, with L calculated from N."""
    return SPHE_D_base.Areq(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def Tho_ub(N, H, ds, dh, dc, m_p):
    """Upper bound on calculated hot-stream outlet temperature."""
    return SPHE_D_base.Tho_ub(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def Tco_lb(N, H, ds, dh, dc, m_p):
    """Lower bound on calculated cold-stream outlet temperature."""
    return SPHE_D_base.Tco_lb(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def SPHE_OF(N, H, ds, dh, dc, m_p):
    """Objective function, with L calculated from N."""
    return SPHE_D_base.SPHE_OF(*_as_length_arguments(N, H, ds, dh, dc, m_p))


def SPHE_length(N, H, ds, dh, dc, m_p):
    """Auxiliary output: calculated spiral length from N."""
    return _length_from_turns(N, ds, dh, dc, m_p)
