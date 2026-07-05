#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
#   0.2          02-Jul-2026     ChatGPT                     Fix ghost-boundary heat-transfer terms and add diagnostics
##################################################################################################################
#endregion


#region Import Library
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve
from functools import lru_cache

from SPHE_D.Calculations.Calculations_SPHE_D_Hydraulic_diameter import SPHE_Hydraulic_diameter
from SPHE_D.Calculations.Calculations_SPHE_D_Length import SPHE_spiral_length, SPHE_turns_from_length
from SPHE_D.Calculations.Calculations_SPHE_D_Mass_Flux import SPHE_Mass_Flux
from SPHE_D.Calculations.Calculations_SPHE_D_Nusselt import SPHE_Nusselt
from SPHE_D.Calculations.Calculations_SPHE_D_Prandtl import SPHE_Prandtl
from SPHE_D.Calculations.Calculations_SPHE_D_Reynolds import SPHE_Reynolds
from SPHE_D.Calculations.Calculations_SPHE_D_h import SPHE_h
from SPHE_D.Calculations.Calculations_SPHE_D_U import SPHE_overall_coefficient


#endregion

#region Calculations

def build_phi_extended(N, M): 
    """
    Build the extended phi grid for N turns, where N may be non-integer.

    The base step is dphi = 2*pi/M. If N is not an integer multiple of the
    base grid, the last interval is shortened so that the final node is
    exactly Phi = N*2*pi.
    """
    two_pi = 2.0 * np.pi
    Nf = float(N)

    if Nf <= 0:
        raise ValueError("N must be greater than 0.")
    if M < 2:
        raise ValueError("M must be greater than or equal to 2.")

    dphi = two_pi / M
    Phi = Nf * two_pi

    N_int = int(np.floor(Nf + 1e-15))
    f = Nf - N_int

    n_full = N_int * M
    frac_intervals = f * M
    n_frac = int(np.floor(frac_intervals + 1e-15))
    rem = frac_intervals - n_frac

    eps = 1e-12
    if rem < eps:
        n_intervals = n_full + n_frac
        phi = np.arange(n_intervals + 1) * dphi
        phi[-1] = Phi
        return phi, Phi

    n_intervals = n_full + n_frac + 1
    phi = np.empty(n_intervals + 1, dtype=float)
    phi[:-1] = np.arange(n_intervals) * dphi
    phi[-1] = Phi
    return phi, Phi
 
def solve_output_temperatures(
    N,
    H,
    ds,
    tk,
    d_I,
    d_II,
    m_I,
    Cp_I,
    mu_I,
    k_I,
    m_II,
    Cp_II,
    mu_II,
    k_II,
    T0,
    t_end,
    thk,
    Rfh,
    Rfc,
    kplate,
    M=8,
):
    """
    Solve the coupled linear system using only backward differences.

    Returns
    -------
    phi : np.ndarray
        Grid coordinates.
    T : np.ndarray
        Solution for T_I over the grid.
    t : np.ndarray
        Solution for t_II over the grid.
    info : dict
        Basic metadata of the assembled model.
    """
    if M < 2:
        raise ValueError("M must be greater than or equal to 2.")

    L=SPHE_spiral_length(N, ds, d_I, d_II, tk)
    # Use the same geometry-based heat-transfer correlation used by the
    # length-based SPHE_D constraints and objective. This keeps the
    # distributed-temperature constraints thermally consistent with the rest
    # of the model while N is still calculated internally from L.
    U = SPHE_overall_coefficient(
        L,
        d_I,
        d_II,
        ds,
        H,
        thk,
        m_I,
        m_II,
        mu_I,
        mu_II,
        Cp_I,
        Cp_II,
        k_I,
        k_II,
        Rfh,
        Rfc,
        kplate,
    )
    
    r_p0 = ds / 2.0 + tk + d_I + tk / 2.0
    b = (d_I + d_II + 2.0 * tk) / (2.0 * np.pi)
    r_s0 = ds / 2.0 + tk / 2.0

    phi, Phi = build_phi_extended(N, M)
    J = len(phi)
    s = M

    h = np.diff(phi)
    inv_h = 1.0 / h

    two_pi = 2.0 * np.pi
    rp = r_p0 + b * phi
    rs = r_s0 + b * phi
    rs_plus = r_s0 + b * (phi + two_pi)

    S_p = np.sqrt(rp**2 + b**2)
    S_s = np.sqrt(rs**2 + b**2)
    S_s_plus = np.sqrt(rs_plus**2 + b**2)

    aI = (U * H) / (m_I * Cp_I)
    aII = (U * H) / (m_II * Cp_II)

    n = 2 * J
    A = lil_matrix((n, n), dtype=float)
    bvec = np.zeros(n, dtype=float)

    def idxT(j: int) -> int:
        return j

    def idxt(j: int) -> int:
        return J + j

    def add_fT(row: int, j: int, weight: float) -> None:
        """
        Add weight*f_T(j) to one matrix row.

        f_T(j) = -aI * [
            S_p(j) * (T_j - t_j)
            + S_s(j) * (T_j - t_{j-s})
        ]

        If j-s is outside the computational domain, that coupling term is
        omitted.
        """
        if weight == 0.0:
            return

        Sp = S_p[j]
        Ss = S_s[j]

        A[row, idxT(j)] += weight * (-aI * Sp)
        A[row, idxt(j)] += weight * (+aI * Sp)

        if j - s >= 0:
            A[row, idxT(j)] += weight * (-aI * Ss)
            A[row, idxt(j - s)] += weight * (+aI * Ss)

    def add_ft(row: int, j: int, weight: float) -> None:
        """
        Add weight*f_t(j) to one matrix row.

        f_t(j) = -aII * [
            S_p(j)      * (T_j - t_j)
            + S_s_plus(j) * (T_{j+s} - t_j)
        ]

        If j+s is outside the computational domain, that coupling term is
        omitted.
        """
        if weight == 0.0:
            return

        Sp = S_p[j]
        SsP = S_s_plus[j]

        A[row, idxT(j)] += weight * (-aII * Sp)
        A[row, idxt(j)] += weight * (+aII * Sp)

        if j + s <= J - 1:
            A[row, idxT(j + s)] += weight * (-aII * SsP)
            A[row, idxt(j)] += weight * (+aII * SsP)

    for j in range(1, J):
        # T equation:
        #   (T_j - T_{j-1})/h_j - f_T(j) = 0
        row_T = idxT(j)
        invhj = inv_h[j - 1]

        A[row_T, idxT(j)] += +invhj
        A[row_T, idxT(j - 1)] += -invhj
        add_fT(row_T, j, weight=-1.0)

        # t equation:
        #   (t_j - t_{j-1})/h_j - f_t(j) = 0
        # The row is multiplied by -h_j and stored at idxt(j-1):
        #   t_{j-1} - t_j + h_j*f_t(j) = 0
        # This leaves idxt(J-1) free for the final boundary condition.
        row_t = idxt(j - 1)
        hj = h[j - 1]

        A[row_t, idxt(j - 1)] += +1.0
        A[row_t, idxt(j)] += -1.0
        add_ft(row_t, j, weight=+hj)

    # Boundary condition: T(0) = T0.
    row_bc_T0 = idxT(0)
    A[row_bc_T0, :] = 0.0
    A[row_bc_T0, idxT(0)] = 1.0
    bvec[row_bc_T0] = T0

    # Boundary condition: t(Phi) = t_end.
    row_bc_tend = idxt(J - 1)
    A[row_bc_tend, :] = 0.0
    A[row_bc_tend, idxt(J - 1)] = 1.0
    bvec[row_bc_tend] = t_end

    A_csr = csr_matrix(A)
    x = spsolve(A_csr, bvec)

    T = x[:J]
    t = x[J:]


    return phi, T, t


def SPHE_energy_balance_from_length(
    L,
    H,
    ds,
    tk,
    d_I,
    d_II,
    m_I,
    Cp_I,
    mu_I,
    k_I,
    m_II,
    Cp_II,
    mu_II,
    k_II,
    T0,
    t_end,
    thk,
    Rfh,
    Rfc,
    kplate,
    M=8,
):
    """
    Return outlet temperatures and the global energy-balance error.

    The distributed solver uses constant heat capacities. Therefore, for a
    conservative temperature solution, the hot-stream heat loss and the
    cold-stream heat gain should match within the finite-difference error.
    """
    N, phi, T, t = solve_output_temperatures_from_length(
        L,
        H,
        ds,
        tk,
        d_I,
        d_II,
        m_I,
        Cp_I,
        mu_I,
        k_I,
        m_II,
        Cp_II,
        mu_II,
        k_II,
        T0,
        t_end,
        thk,
        Rfh,
        Rfc,
        kplate,
        M=M,
    )

    T_out = float(T[-1])
    t_out = float(t[0])
    Q_hot = float(m_I * Cp_I * (T0 - T_out))
    Q_cold = float(m_II * Cp_II * (t_out - t_end))
    energy_error = Q_hot - Q_cold
    relative_energy_error = energy_error / Q_hot if Q_hot != 0.0 else np.nan
    t_out_balance = t_end + Q_hot / (m_II * Cp_II)

    return {
        "N": float(N),
        "T_out": T_out,
        "t_out": t_out,
        "Q_hot": Q_hot,
        "Q_cold": Q_cold,
        "energy_error": float(energy_error),
        "relative_energy_error": float(relative_energy_error),
        "t_out_balance": float(t_out_balance),
        "t_out_minus_balance": float(t_out - t_out_balance),
    }


def solve_output_temperatures_from_length(
    L,
    H,
    ds,
    tk,
    d_I,
    d_II,
    m_I,
    Cp_I,
    mu_I,
    k_I,
    m_II,
    Cp_II,
    mu_II,
    k_II,
    T0,
    t_end,
    thk,
    Rfh,
    Rfc,
    kplate,
    M=8,
):
    """
    Solve the distributed-temperature model using L as the external variable.

    Returns
    -------
    N : float
        Number of spiral turns calculated from L.
    phi : np.ndarray
        Angular grid.
    T : np.ndarray
        Channel-I temperature profile.
    t : np.ndarray
        Channel-II temperature profile.
    """
    N = SPHE_turns_from_length(L, ds, d_I, d_II, tk)
    phi, T, t = solve_output_temperatures(
        N,
        H,
        ds,
        tk,
        d_I,
        d_II,
        m_I,
        Cp_I,
        mu_I,
        k_I,
        m_II,
        Cp_II,
        mu_II,
        k_II,
        T0,
        t_end,
        thk,
        Rfh,
        Rfc,
        kplate,
        M=M,
    )
    return N, phi, T, t


@lru_cache(maxsize=100000)
def _SPHE_output_temperatures_from_length_cached(
    L,
    H,
    ds,
    tk,
    d_I,
    d_II,
    m_I,
    Cp_I,
    mu_I,
    k_I,
    m_II,
    Cp_II,
    mu_II,
    k_II,
    T0,
    t_end,
    thk,
    Rfh,
    Rfc,
    kplate,
    M,
):
    """Cached scalar outlet-temperature calculation for Set Trimming calls."""
    N, _, T, t = solve_output_temperatures_from_length(
        L,
        H,
        ds,
        tk,
        d_I,
        d_II,
        m_I,
        Cp_I,
        mu_I,
        k_I,
        m_II,
        Cp_II,
        mu_II,
        k_II,
        T0,
        t_end,
        thk,
        Rfh,
        Rfc,
        kplate,
        M=M,
    )

    # Channel I is specified with its inlet at phi = 0, so its outlet is T[-1].
    # Channel II is specified with its inlet at phi = Phi, so its outlet is t[0].
    return float(T[-1]), float(t[0]), float(N)


def SPHE_output_temperatures_from_length(
    L,
    H,
    ds,
    tk,
    d_I,
    d_II,
    m_I,
    Cp_I,
    mu_I,
    k_I,
    m_II,
    Cp_II,
    mu_II,
    k_II,
    T0,
    t_end,
    thk,
    Rfh,
    Rfc,
    kplate,
    M=8,
):
    """
    Return outlet temperatures for the distributed SPHE model.

    Returns
    -------
    T_out : float
        Outlet temperature of channel I, whose inlet is T0 at phi = 0.
    t_out : float
        Outlet temperature of channel II, whose inlet is t_end at phi = Phi.
    N : float
        Number of turns calculated from L.
    """
    args = tuple(
        float(v)
        for v in (
            L,
            H,
            ds,
            tk,
            d_I,
            d_II,
            m_I,
            Cp_I,
            mu_I,
            k_I,
            m_II,
            Cp_II,
            mu_II,
            k_II,
            T0,
            t_end,
            thk,
            Rfh,
            Rfc,
            kplate,
        )
    ) + (int(M),)
    return _SPHE_output_temperatures_from_length_cached(*args)