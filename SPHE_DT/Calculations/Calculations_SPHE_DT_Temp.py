#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
#   0.2          02-Jul-2026     ChatGPT                     Distributed solver with temperature-dependent properties
##################################################################################################################
#endregion

#region Import Library
from functools import lru_cache

import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import spsolve

from SPHE_DT.Calculations.Calculations_SPHE_DT_Length import SPHE_spiral_length, SPHE_turns_from_length
from SPHE_DT.Calculations.Calculations_SPHE_DT_Reynolds import SPHE_spiral_outer_diameter
from SPHE_DT.Calculations.Calculations_SPHE_DT_Properties import enthalpy_change
#endregion

#region Grid and local coefficients

def build_phi_extended(N, M):
    """Build the extended phi grid for N turns, where N may be non-integer."""
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


def _local_h(D, G, Ds, cp, mu, k):
    """Return the local spiral-channel heat-transfer coefficient."""
    cp = max(float(cp), 1e-12)
    mu = max(float(mu), 1e-12)
    k = max(float(k), 1e-12)

    Re = D * G / mu
    Pr = mu * cp / k
    return (1.0 + 3.54 * D / Ds) * 0.023 * cp * G * (Re ** (-0.2)) * (Pr ** (-2.0 / 3.0))


def _local_U(
    L,
    d_I,
    d_II,
    ds,
    H,
    thk,
    m_I,
    m_II,
    T_I,
    T_II,
    cp_I_func,
    mu_I_func,
    k_I_func,
    cp_II_func,
    mu_II_func,
    k_II_func,
    Rfh,
    Rfc,
    kplate,
):
    """Return local U for one hot/cold temperature pair."""
    Dh = 2.0 * d_I * H / (d_I + H)
    Dc = 2.0 * d_II * H / (d_II + H)
    Ds = SPHE_spiral_outer_diameter(L, d_I, d_II, thk, ds)
    G_I = m_I / (d_I * H)
    G_II = m_II / (d_II * H)

    h_I = _local_h(Dh, G_I, Ds, cp_I_func(T_I), mu_I_func(T_I), k_I_func(T_I))
    h_II = _local_h(Dc, G_II, Ds, cp_II_func(T_II), mu_II_func(T_II), k_II_func(T_II))

    return 1.0 / (1.0 / h_I + Rfh + thk / kplate + 1.0 / h_II + Rfc)

#endregion

#region Linear solve for one fixed-property-profile iteration

def _solve_linear_step(
    N,
    H,
    ds,
    tk,
    d_I,
    d_II,
    m_I,
    m_II,
    T0,
    t_end,
    thk,
    Rfh,
    Rfc,
    kplate,
    cp_I_func,
    rho_I_func,
    mu_I_func,
    k_I_func,
    cp_II_func,
    rho_II_func,
    mu_II_func,
    k_II_func,
    T_old,
    t_old,
    M=8,
):
    """Assemble and solve one fixed-point linearization of the nonlinear model."""
    del rho_I_func, rho_II_func  # Density affects hydraulic constraints, not the energy equation directly.

    L = SPHE_spiral_length(N, ds, d_I, d_II, tk)

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

    n = 2 * J
    A = lil_matrix((n, n), dtype=float)
    bvec = np.zeros(n, dtype=float)

    def idxT(j: int) -> int:
        return j

    def idxt(j: int) -> int:
        return J + j

    def a_I(TI, TII):
        U = _local_U(
            L,
            d_I,
            d_II,
            ds,
            H,
            thk,
            m_I,
            m_II,
            TI,
            TII,
            cp_I_func,
            mu_I_func,
            k_I_func,
            cp_II_func,
            mu_II_func,
            k_II_func,
            Rfh,
            Rfc,
            kplate,
        )
        cp = max(float(cp_I_func(TI)), 1e-12)
        return U * H / (m_I * cp)

    def a_II(TI, TII):
        U = _local_U(
            L,
            d_I,
            d_II,
            ds,
            H,
            thk,
            m_I,
            m_II,
            TI,
            TII,
            cp_I_func,
            mu_I_func,
            k_I_func,
            cp_II_func,
            mu_II_func,
            k_II_func,
            Rfh,
            Rfc,
            kplate,
        )
        cp = max(float(cp_II_func(TII)), 1e-12)
        return U * H / (m_II * cp)

    def add_fT(row: int, j: int, weight: float) -> None:
        if weight == 0.0:
            return

        Sp = S_p[j]
        aIp = a_I(T_old[j], t_old[j])
        A[row, idxT(j)] += weight * (-aIp * Sp)
        A[row, idxt(j)] += weight * (+aIp * Sp)

        if j - s >= 0:
            Ss = S_s[j]
            aIs = a_I(T_old[j], t_old[j - s])
            A[row, idxT(j)] += weight * (-aIs * Ss)
            A[row, idxt(j - s)] += weight * (+aIs * Ss)

    def add_ft(row: int, j: int, weight: float) -> None:
        if weight == 0.0:
            return

        Sp = S_p[j]
        aIIp = a_II(T_old[j], t_old[j])
        A[row, idxT(j)] += weight * (-aIIp * Sp)
        A[row, idxt(j)] += weight * (+aIIp * Sp)

        if j + s <= J - 1:
            SsP = S_s_plus[j]
            aIIs = a_II(T_old[j + s], t_old[j])
            A[row, idxT(j + s)] += weight * (-aIIs * SsP)
            A[row, idxt(j)] += weight * (+aIIs * SsP)

    for j in range(1, J):
        row_T = idxT(j)
        invhj = inv_h[j - 1]
        A[row_T, idxT(j)] += +invhj
        A[row_T, idxT(j - 1)] += -invhj
        add_fT(row_T, j, weight=-1.0)

        row_t = idxt(j - 1)
        hj = h[j - 1]
        A[row_t, idxt(j - 1)] += +1.0
        A[row_t, idxt(j)] += -1.0
        add_ft(row_t, j, weight=+hj)

    row_bc_T0 = idxT(0)
    A[row_bc_T0, :] = 0.0
    A[row_bc_T0, idxT(0)] = 1.0
    bvec[row_bc_T0] = T0

    row_bc_tend = idxt(J - 1)
    A[row_bc_tend, :] = 0.0
    A[row_bc_tend, idxt(J - 1)] = 1.0
    bvec[row_bc_tend] = t_end

    x = spsolve(csr_matrix(A), bvec)
    return phi, x[:J], x[J:]

#endregion

#region Public solver

def solve_output_temperatures(
    N,
    H,
    ds,
    tk,
    d_I,
    d_II,
    m_I,
    T0,
    t_end,
    thk,
    Rfh,
    Rfc,
    kplate,
    cp_I_func,
    rho_I_func,
    mu_I_func,
    k_I_func,
    m_II,
    cp_II_func,
    rho_II_func,
    mu_II_func,
    k_II_func,
    M=8,
    tol=1e-6,
    max_iter=50,
    relaxation=0.7,
):
    """Solve the nonlinear distributed-temperature model.

    The nonlinear part is treated by fixed-point iteration. At each iteration,
    local Cp, viscosity, conductivity and U are calculated from the previous
    temperature profile, then the resulting sparse linear system is solved.
    """
    if M < 2:
        raise ValueError("M must be greater than or equal to 2.")
    if not 0.0 < relaxation <= 1.0:
        raise ValueError("relaxation must be in the interval (0, 1].")

    phi, _ = build_phi_extended(N, M)
    J = len(phi)

    T_old = np.full(J, float(T0), dtype=float)
    t_old = np.full(J, float(t_end), dtype=float)

    converged = False
    error = np.inf

    for iteration in range(1, int(max_iter) + 1):
        phi, T_new, t_new = _solve_linear_step(
            N,
            H,
            ds,
            tk,
            d_I,
            d_II,
            m_I,
            m_II,
            T0,
            t_end,
            thk,
            Rfh,
            Rfc,
            kplate,
            cp_I_func,
            rho_I_func,
            mu_I_func,
            k_I_func,
            cp_II_func,
            rho_II_func,
            mu_II_func,
            k_II_func,
            T_old,
            t_old,
            M=M,
        )

        T_relaxed = relaxation * T_new + (1.0 - relaxation) * T_old
        t_relaxed = relaxation * t_new + (1.0 - relaxation) * t_old

        error = max(
            float(np.max(np.abs(T_relaxed - T_old))),
            float(np.max(np.abs(t_relaxed - t_old))),
        )

        T_old = T_relaxed
        t_old = t_relaxed

        if error <= tol:
            converged = True
            break

    info = {
        "converged": converged,
        "iterations": iteration,
        "max_temperature_change": error,
        "M": int(M),
        "N": float(N),
    }

    return phi, T_old, t_old, info


def solve_output_temperatures_from_length(
    L,
    H,
    ds,
    tk,
    d_I,
    d_II,
    m_I,
    T0,
    t_end,
    thk,
    Rfh,
    Rfc,
    kplate,
    cp_I_func,
    rho_I_func,
    mu_I_func,
    k_I_func,
    m_II,
    cp_II_func,
    rho_II_func,
    mu_II_func,
    k_II_func,
    M=8,
    tol=1e-6,
    max_iter=50,
    relaxation=0.7,
):
    """Solve the distributed-temperature model using L as the external variable."""
    N = SPHE_turns_from_length(L, ds, d_I, d_II, tk)
    phi, T, t, info = solve_output_temperatures(
        N,
        H,
        ds,
        tk,
        d_I,
        d_II,
        m_I,
        T0,
        t_end,
        thk,
        Rfh,
        Rfc,
        kplate,
        cp_I_func,
        rho_I_func,
        mu_I_func,
        k_I_func,
        m_II,
        cp_II_func,
        rho_II_func,
        mu_II_func,
        k_II_func,
        M=M,
        tol=tol,
        max_iter=max_iter,
        relaxation=relaxation,
    )
    info["N"] = float(N)
    return N, phi, T, t, info


@lru_cache(maxsize=100000)
def _SPHE_output_temperatures_from_length_cached(
    L,
    H,
    ds,
    tk,
    d_I,
    d_II,
    m_I,
    T0,
    t_end,
    thk,
    Rfh,
    Rfc,
    kplate,
    cp_I_func,
    rho_I_func,
    mu_I_func,
    k_I_func,
    m_II,
    cp_II_func,
    rho_II_func,
    mu_II_func,
    k_II_func,
    M,
    tol,
    max_iter,
    relaxation,
):
    """Cached scalar outlet-temperature calculation for Set Trimming calls."""
    N, _, T, t, info = solve_output_temperatures_from_length(
        L,
        H,
        ds,
        tk,
        d_I,
        d_II,
        m_I,
        T0,
        t_end,
        thk,
        Rfh,
        Rfc,
        kplate,
        cp_I_func,
        rho_I_func,
        mu_I_func,
        k_I_func,
        m_II,
        cp_II_func,
        rho_II_func,
        mu_II_func,
        k_II_func,
        M=M,
        tol=tol,
        max_iter=max_iter,
        relaxation=relaxation,
    )

    return float(T[-1]), float(t[0]), float(N), bool(info["converged"]), int(info["iterations"]), float(info["max_temperature_change"])


def SPHE_output_temperatures_from_length(
    L,
    H,
    ds,
    tk,
    d_I,
    d_II,
    m_I,
    T0,
    t_end,
    thk,
    Rfh,
    Rfc,
    kplate,
    cp_I_func,
    rho_I_func,
    mu_I_func,
    k_I_func,
    m_II,
    cp_II_func,
    rho_II_func,
    mu_II_func,
    k_II_func,
    M=8,
    tol=1e-6,
    max_iter=50,
    relaxation=0.7,
):
    """Return outlet temperatures for the temperature-dependent distributed SPHE model."""
    scalar_args = tuple(
        float(v)
        for v in (
            L,
            H,
            ds,
            tk,
            d_I,
            d_II,
            m_I,
            T0,
            t_end,
            thk,
            Rfh,
            Rfc,
            kplate,
        )
    )
    solver_args = (int(M), float(tol), int(max_iter), float(relaxation))
    return _SPHE_output_temperatures_from_length_cached(
        *scalar_args,
        cp_I_func,
        rho_I_func,
        mu_I_func,
        k_I_func,
        float(m_II),
        cp_II_func,
        rho_II_func,
        mu_II_func,
        k_II_func,
        *solver_args,
    )


def SPHE_energy_balance_from_length(
    L,
    H,
    ds,
    tk,
    d_I,
    d_II,
    m_I,
    T0,
    t_end,
    thk,
    Rfh,
    Rfc,
    kplate,
    cp_I_func,
    rho_I_func,
    mu_I_func,
    k_I_func,
    m_II,
    cp_II_func,
    rho_II_func,
    mu_II_func,
    k_II_func,
    M=8,
    tol=1e-6,
    max_iter=50,
    relaxation=0.7,
):
    """Return outlet temperatures and enthalpy-based global energy-balance error."""
    N, _, T, t, info = solve_output_temperatures_from_length(
        L,
        H,
        ds,
        tk,
        d_I,
        d_II,
        m_I,
        T0,
        t_end,
        thk,
        Rfh,
        Rfc,
        kplate,
        cp_I_func,
        rho_I_func,
        mu_I_func,
        k_I_func,
        m_II,
        cp_II_func,
        rho_II_func,
        mu_II_func,
        k_II_func,
        M=M,
        tol=tol,
        max_iter=max_iter,
        relaxation=relaxation,
    )

    T_out = float(T[-1])
    t_out = float(t[0])
    Q_hot = float(m_I * enthalpy_change(cp_I_func, T_out, T0))
    Q_cold = float(m_II * enthalpy_change(cp_II_func, t_end, t_out))
    energy_error = Q_hot - Q_cold
    relative_energy_error = energy_error / Q_hot if Q_hot != 0.0 else np.nan

    return {
        "N": float(N),
        "T_out": T_out,
        "t_out": t_out,
        "Q_hot": Q_hot,
        "Q_cold": Q_cold,
        "energy_error": float(energy_error),
        "relative_energy_error": float(relative_energy_error),
        "converged": bool(info["converged"]),
        "iterations": int(info["iterations"]),
        "max_temperature_change": float(info["max_temperature_change"]),
    }

#endregion
