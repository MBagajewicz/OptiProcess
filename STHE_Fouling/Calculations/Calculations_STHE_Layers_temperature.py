#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          02-Jul-2025     Augusto Vieira            Original


##################################################################################################################

##################################################################################################################
#endregion


#region Import Library
import numpy as np
from STHE.Calculations import Calculations_STHE_PNTU, Calculations_STHE_htubeside, Calculations_STHE_hshellside
#endregion

##################################################################################################################
#region Thermal Layer Interface Temperatures

def STHE_Tto(Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks, Rfs, thk, ktube, yfluid,
             Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk, Nps=1):
    # Compute tube-side outlet temperature [K] using effectiveness method
    # If yfluid == 1, tube-side is hot stream (counter-current)
    # If yfluid == 2, tube-side is cold stream (co-current)
    Epsolon = Calculations_STHE_PNTU.STHE_PNTU(
        mt, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs,
        thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc,
        Nps, m_p, ft_thk
    )
    Ct = mt * Cpt                                # Tube-side heat capacity rate
    Cs = ms * Cps                                # Shell-side heat capacity rate
    Cmin = np.minimum(Ct, Cs)                    # Minimum capacity rate
    Q = Epsolon * Cmin * np.abs(Tti - Tsi)       # Heat transferred
    Tto = Tti + Q / Ct if yfluid == 1 else Tti - Q / Ct  # Return corrected outlet temperature
    return Tto

def STHE_Tso(Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks, Rfs, thk, ktube, yfluid,
             Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk, Nps=1):
    # Compute shell-side outlet temperature [K] using effectiveness method
    # If yfluid == 1, shell-side is cold stream
    # If yfluid == 2, shell-side is hot stream
    Epsolon = Calculations_STHE_PNTU.STHE_PNTU(
        mt, rot, Cpt, mit, kt, Rft, ms, ros, Cps, mis, ks, Rfs,
        thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc,
        Nps, m_p, ft_thk
    )
    Ct = mt * Cpt                                # Tube-side heat capacity rate
    Cs = ms * Cps                                # Shell-side heat capacity rate
    Cmin = np.minimum(Ct, Cs)                    # Minimum capacity rate
    Q = Epsolon * Cmin * np.abs(Tti - Tsi)       # Heat transferred
    Tso = Tsi - Q / Cs if yfluid == 1 else Tsi + Q / Cs  # corrected outlet temperature
    return Tso

def STHE_Tft_in(Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks, Rfs,
                thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk):
    # Compute temperature at the fouling-fluid interface [K]
    # This is the flow side interface, before entering the fouling layer
    kft = m_p["kft"]                             # Fouling thermal conductivity
    dti = dte - 2 * thk                          # Tube inner diameter
    df = dti - 2 * ft_thk                        # Flow diameter reduced by fouling

    ht = Calculations_STHE_htubeside.STHE_h_tubeside(
        mt, rot, Cpt, mit, kt, thk, yfluid, Ds, dte, Npt, rp, lay, L, m_p, ft_thk
    )  # Tube-side convective coefficient

    hs = Calculations_STHE_hshellside.STHE_h_shellside(
        ms, ros, Cps, mis, ks, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p
    )  # Shell-side convective coefficient

    Rint = 1 / (ht * df)                         # Internal convective resistance
    Rfoul = np.log(dti / df) / (2 * kft)         # Fouling resistance
    Rcond = np.log(dte / dti) / (2 * kt)         # Tube wall conduction resistance
    Rout = Rfs / (np.pi * dte) + 1 / (hs * dte)  # External shell-side resistance

    Tto = STHE_Tto(Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks, Rfs,
                   thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk)
    Tso = STHE_Tso(Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks, Rfs,
                   thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk)

    Tt = (Tti + Tto) / 2                          # Average tube-side temperature
    Ts = (Tsi + Tso) / 2                          # Average shell-side temperature
    Rtotal = Rint + Rfoul + Rcond + Rout          # Total thermal resistance
    dT = Ts - Tt                  
    Tft_in = Tt + dT * Rint / Rtotal              # fouling-fluid interface temperature
    return Tft_in


def STHE_Tw_in(Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks, Rfs,
               thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk):
    # Compute temperature at the tube wall inner interface [K]
    # This is the fouling side interface (tube wall contact with fouling layer)
    kft = m_p["kft"]                             # Fouling thermal conductivity
    dti = dte - 2 * thk                          # Tube inner diameter after wall thickness
    df = dti - 2 * ft_thk                        # Diameter after fouling thickness

    ht = Calculations_STHE_htubeside.STHE_h_tubeside(
        mt, rot, Cpt, mit, kt, thk, yfluid, Ds, dte, Npt, rp, lay, L, m_p, ft_thk
    )  # Tube-side convective coefficient

    hs = Calculations_STHE_hshellside.STHE_h_shellside(
        ms, ros, Cps, mis, ks, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p
    )  # Shell-side convective coefficient

    Rint = 1 / (ht * df)                         # Internal convective resistance
    Rfoul = np.log(dti / df) / (2 * kft)         # Fouling resistance
    Rcond = np.log(dte / dti) / (2 * kt)         # Tube wall conduction resistance
    Rout = Rfs / (np.pi * dte) + 1 / (hs * dte)  # External convective resistance + shell fouling

    Tto = STHE_Tto(Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks, Rfs,
                   thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk)
    Tso = STHE_Tso(Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks, Rfs,
                   thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk)

    Tt = (Tti + Tto) / 2                          # Average tube-side temperature
    Ts = (Tsi + Tso) / 2                          # Average shell-side temperature
    Rtotal = Rint + Rfoul + Rcond + Rout         # Total thermal resistance
    dT = Ts - Tt                                  # Temperature difference across wall + fouling layer
    Tw_in = Tt + dT * (Rint + Rfoul) / Rtotal     # Return wall-tube fouling layer interface temperature
    return Tw_in     


#endregion
##################################################################################################################
