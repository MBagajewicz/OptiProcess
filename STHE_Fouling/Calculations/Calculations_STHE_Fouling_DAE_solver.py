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

from STHE.Calculations import Calculations_STHE_Fouling_thickness_tubeside,Calculations_STHE_Fouling_tubeside 
from assimulo.problem import Implicit_Problem
from assimulo.solvers import IDA
##################################################################################################################
#endregion

    
##################################################################################################################
#region Final Fouling Condition with Assimulo (DAE Solver)


def final_fouling_condition_0(mt, rot, Cpt, mit, kt, ms, ros, Cps, mis, ks,
                              Rfs, thk, ktube, yfluid,
                              Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):

    n_cand = len(Ds)  # Number of candidates

    # ===============================
    # Constant fouling (no DAE needed)
    # ===============================
    if m_p.get('Fouling_Method') == 'constant' and 'Rft' in m_p:
        Rft_val = m_p['Rft']
        Rft_final = np.full(n_cand, Rft_val)
        ft_thk_final = np.zeros(n_cand)

        for i in range(n_cand):
            ft_thk_final[i] = Calculations_STHE_Fouling_thickness_tubeside. solve_ft_thk(mt, rot, Cpt, mit, kt, thk, yfluid,
            Ds[i], dte[i], Npt[i], rp[i], lay[i], L[i], m_p, Rft_val)

        print(f" Constant fouling applied: Rft = {Rft_val:.3e}")
        print(f" Final candidate: Rft_final = {Rft_final[-1]:.3e}, ft_thk_final = {ft_thk_final[-1]:.3e}")
        return Rft_final, ft_thk_final

    # =======================================================
    # All other models → Use DAE to solve dynamic fouling
    # =======================================================

    Rft_final = np.zeros(n_cand)
    ft_thk_final = np.zeros(n_cand)
    tfinal = m_p["final_time"]
    tinit = m_p["initial_time"]

    print(f"▶️ Starting DAE fouling simulation with {n_cand} candidates")
    step = max(n_cand // 100, 1)

    for i in range(n_cand):
        if (i + 1) % step == 0 or i == 0 or i == n_cand - 1:
            print(f" Candidate {i+1} of {n_cand}")

        # Residual function for the DAE
        def residual(t, y, ydot):
            Rft, ft_thk = y
            dRft_dt = ydot[0]
            res = np.zeros(2)

            res[0] = dRft_dt - Calculations_STHE_Fouling_tubeside.Fouling_dRft_dt(
                t, m_p['Tti'], mt, rot, Cpt, mit, kt, Rft,
                m_p['Tsi'], ms, ros, Cps, mis, ks, Rfs,
                thk, ktube, yfluid,
                Ds[i], dte[i], Npt[i], rp[i], lay[i], L[i], Nb[i], Bc[i],
                m_p, ft_thk
            )

            res[1] = Calculations_STHE_Fouling_thickness_tubeside.Rft_thk_t_func_residue(
                mt, rot, Cpt, mit, kt, thk, yfluid,
                Ds[i], dte[i], Npt[i], rp[i], lay[i], L[i], m_p,
                Rft, ft_thk
            )

            return res

        # Initial condition for DAE
        Rft0 = 1e-20
        ft_thk0 = 1e-20
        y0 = np.array([Rft0, ft_thk0])
        yd0 = np.array([1e-20, 0.0])  # Only Rft is differential

        # DAE solver configuration
        model = Implicit_Problem(residual, y0, yd0, tinit)
        solver = IDA(model)
        solver.atol = 1e-8
        solver.rtol = 1e-4
        solver.suppress_alg = False
        solver.verbosity = 50
        solver.report_continuously = False

        # Run DAE simulation
        t, y, yd = solver.simulate(tfinal, 2)

        Rft_val = y[-1, 0]
        ft_thk_val = y[-1, 1]

        # Apply numerical floor
        Rft_final[i] = 0.0 if Rft_val < 1e-8 else Rft_val
        ft_thk_final[i] = 0.0 if ft_thk_val < 1e-8 else ft_thk_val

    print(f" Final candidate: Rft_final = {Rft_final[-1]:.3e}, ft_thk_final = {ft_thk_final[-1]:.3e}")
    return Rft_final, ft_thk_final


#endregion

##################################################################################################################
#region Cached Fouling Wrapper

# Cached wrapper to avoid recomputation of final fouling condition
_cached_fouling = {}

def final_fouling_condition(mt, rot, Cpt, mit, kt, ms, ros, Cps, mis, ks,
                            Rfs, thk, ktube, yfluid,
                            Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):

    # Check for incorrect call signature (fallback for invalid inputs)
    if isinstance(Ds, list) and not isinstance(Ds, np.ndarray):
        print(" Invalid call to final_fouling_condition. Please check import and arguments.")
        return np.array([np.nan]), np.array([np.nan])

    # Build hashable key for candidate combination
    key = (
        tuple(Ds.round(6)), tuple(dte.round(6)), tuple(Npt.round(6)), tuple(rp.round(6)),
        tuple(lay.round(6)), tuple(L.round(6)), tuple(Nb.round(6)), tuple(Bc.round(6))
    )

    # Run simulation only if not cached
    if key not in _cached_fouling:
        mt     = m_p['mt']
        rot    = m_p['rot']
        Cpt    = m_p['Cpt']
        mit    = m_p['mit']
        kt     = m_p['kt']
        ms     = m_p['ms']
        ros    = m_p['ros']
        Cps    = m_p['Cps']
        mis    = m_p['mis']
        ks     = m_p['ks']
        Rfs    = m_p['Rfs']
        thk    = m_p['thk']
        ktube  = m_p['ktube']
        yfluid = m_p['yfluid']

        Rft, ft_thk = final_fouling_condition_0(
            mt, rot, Cpt, mit, kt, ms, ros, Cps, mis, ks,
            Rfs, thk, ktube, yfluid,
            Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p
        )
        _cached_fouling[key] = (Rft, ft_thk)

    return _cached_fouling[key]

#endregion
##################################################################################################################
