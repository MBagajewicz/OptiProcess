#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello              Original
#   0.1          07-Jun-2025     Qiqi Zhang                 Adaptation from original STHE
#   0.2          02-Jul-2026     ChatGPT                    Remove stale import and fix cold-channel diameter conversion
##################################################################################################################
#endregion

#region Calculations

def SPHE_DeltaP(L, roh, roc, mh, mc, H, dh, dc, mih, mic):
    """Return pressure drops for the hot and cold channels in Pa."""
    L_ft = L / 0.3048
    mih_cp = mih * 1000
    mic_cp = mic * 1000
    dh_in = dh / 0.0254
    dc_in = dc / 0.0254
    H_in = H / 0.0254
    mh_klbhr = mh / 0.125998
    mc_klbhr = mc / 0.125998

    dltph = (
        0.001
        * (L_ft / (roh / 998.2063))
        * ((mh_klbhr / (H_in * dh_in)) ** 2)
        * ((1.3 * mih_cp ** (1 / 3)) / (dh_in + 0.125) * (H_in / mh_klbhr) ** (1 / 3) + 1.5 + 16 / L_ft)
    ) * 6894.7572932

    dltpc = (
        0.001
        * (L_ft / (roc / 998.2063))
        * ((mc_klbhr / (H_in * dc_in)) ** 2)
        * ((1.3 * mic_cp ** (1 / 3)) / (dc_in + 0.125) * (H_in / mc_klbhr) ** (1 / 3) + 1.5 + 16 / L_ft)
    ) * 6894.7572932

    return dltph, dltpc


def SPHE_DeltaP_lb(L, romax, mh, mc, H, dh, dc, mimin):
    """Return lower-bound pressure drop estimates in Pa."""
    L_ft = L / 0.3048
    H_in = H / 0.0254
    mh_klbhr = mh / 0.125998
    mc_klbhr = mc / 0.125998
    dh_in = dh / 0.0254
    dc_in = dc / 0.0254
    mimin_cp = mimin * 1000

    dltphlb = (
        0.001
        * (L_ft / (romax / 998.2063))
        * ((mh_klbhr / (H_in * dh_in)) ** 2)
        * ((1.3 * mimin_cp ** (1 / 3)) / (dh_in + 0.125) * (H_in / mh_klbhr) ** (1 / 3) + 1.5 + 16 / L_ft)
    ) * 6894.7572932

    dltpclb = (
        0.001
        * (L_ft / (romax / 998.2063))
        * ((mc_klbhr / (H_in * dc_in)) ** 2)
        * ((1.3 * mimin_cp ** (1 / 3)) / (dc_in + 0.125) * (H_in / mc_klbhr) ** (1 / 3) + 1.5 + 16 / L_ft)
    ) * 6894.7572932

    return dltphlb, dltpclb

#endregion
