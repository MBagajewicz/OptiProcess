#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
##################################################################################################################
#endregion


#region Import Library
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve

from SPHE_D.Calculations.Calculations_SPHE_D_Hydraulic_diameter import SPHE_Hydraulic_diameter
from SPHE_D.Calculations.Calculations_SPHE_D_Length import SPHE_spiral_length
from SPHE_D.Calculations.Calculations_SPHE_D_Mass_Flux import SPHE_Mass_Flux
from SPHE_D.Calculations.Calculations_SPHE_D_Nusselt import SPHE_Nusselt
from SPHE_D.Calculations.Calculations_SPHE_D_Prandtl import SPHE_Prandtl
from SPHE_LMTD.Calculations.Calculations_SPHE_LMTD import SPHE_Reynolds, SPHE_h
from SPHE_LMTD.Calculations.Calculations_SPHE_LMTD_U import SPHE_overall_coefficient


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
 
def solve_output_temperatures(N,H,ds,tk,d_I,d_II,m_I,Cp_I,mu_I,k_I,m_II,Cp_II,mu_II,k_II,T0,t_end, thk, Rfh, Rfc, kplate):
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
    M=8
    if M < 2:
        raise ValueError("M must be greater than or equal to 2.")

    L=SPHE_spiral_length(N, ds, d_I, d_II, tk)
    Dh_I=SPHE_Hydraulic_diameter(d_I, H)
    Dh_II=SPHE_Hydraulic_diameter(d_II, H)
    G_I=SPHE_Mass_Flux(m_I, d_I, H)
    G_II=SPHE_Mass_Flux(m_II, d_II, H)
    Re_I=SPHE_Reynolds(Dh_I, G_I, mu_I)
    Re_II=SPHE_Reynolds(Dh_II, G_II, mu_II)
    Prandtl_I=SPHE_Prandtl(Cp_I, mu_I, k_I)
    Prandtl_II=SPHE_Prandtl(Cp_II, mu_II, k_II)
    Nusselt_I=SPHE_Nusselt(Re_I, Prandtl_I, d_I, Dh_I, L)
    Nusselt_II=SPHE_Nusselt(Re_II, Prandtl_II, d_II, Dh_II, L)
    h_I=SPHE_h(Nusselt_I, k_I, Dh_I)
    h_II=SPHE_h(Nusselt_II, k_II, Dh_II)

    U=SPHE_overall_coefficient(h_I, h_II, thk, Rfh, Rfc, kplate)
    
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

        A[row, idxT(j)] += weight * (-aI * Ss)
        if j - s >= 0:
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