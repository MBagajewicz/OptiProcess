#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
#   0.2          02-Jul-2026     ChatGPT                     Add length-to-turns compatibility function
##################################################################################################################
#endregion


#region Import Library
import numpy as np
#endregion

#region Calculations

def _spiral_arc_length(theta, a, b):
    """Return the Archimedean spiral arc length from 0 to theta."""
    u0 = a
    u1 = a + b * theta

    def F(u):
        return (
            u * np.sqrt(u**2 + b**2)
            + b**2 * np.log(u + np.sqrt(u**2 + b**2))
        )

    return (F(u1) - F(u0)) / (2.0 * b)


def SPHE_spiral_length(N, ds, d_I, d_II, tk):
    """Return the spiral channel length for a given number of turns."""
    if N <= 0:
        raise ValueError("N must be greater than zero.")
    if ds <= 0 or d_I <= 0 or d_II <= 0 or tk <= 0:
        raise ValueError("ds, d_I, d_II, and tk must be greater than zero.")

    a = ds / 2.0 + tk + d_I + tk / 2.0
    b = (d_I + d_II + 2.0 * tk) / (2.0 * np.pi)
    theta2 = N * 2.0 * np.pi

    return _spiral_arc_length(theta2, a, b)


def SPHE_turns_from_length(L, ds, d_I, d_II, tk, *, tol=1e-10, max_iter=30):
    """
    Return the number of spiral turns that gives the specified channel length.

    This function preserves compatibility with the length-based design variable
    used by the Set Trimming model. The distributed-temperature model uses N
    internally, but the external optimization variables can remain
    (L, H, ds, dh, dc).
    """
    if L <= 0:
        raise ValueError("L must be greater than zero.")
    if ds <= 0 or d_I <= 0 or d_II <= 0 or tk <= 0:
        raise ValueError("ds, d_I, d_II, and tk must be greater than zero.")

    a = ds / 2.0 + tk + d_I + tk / 2.0
    b = (d_I + d_II + 2.0 * tk) / (2.0 * np.pi)

    # Initial guess from the asymptotic integral without the b**2 term.
    theta = max((np.sqrt(a * a + 2.0 * b * L) - a) / b, 1e-12)

    for _ in range(max_iter):
        length = _spiral_arc_length(theta, a, b)
        residual = length - L
        if abs(residual) <= tol * max(1.0, L):
            break

        derivative = np.sqrt((a + b * theta) ** 2 + b**2)
        theta_new = theta - residual / derivative
        if theta_new <= 0 or not np.isfinite(theta_new):
            theta_new = 0.5 * theta
        theta = theta_new

    # Guard against rare Newton drift by doing a short monotonic correction.
    if not np.isfinite(theta) or theta <= 0:
        theta = 1e-12

    length = _spiral_arc_length(theta, a, b)
    if abs(length - L) > 10.0 * tol * max(1.0, L):
        lo = 0.0
        hi = max(theta, 1.0)
        while _spiral_arc_length(hi, a, b) < L:
            hi *= 2.0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if _spiral_arc_length(mid, a, b) < L:
                lo = mid
            else:
                hi = mid
        theta = 0.5 * (lo + hi)

    return theta / (2.0 * np.pi)

#endregion
