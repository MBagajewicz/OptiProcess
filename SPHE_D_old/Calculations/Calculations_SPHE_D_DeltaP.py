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
from SPHE_LMTD.Calculations import Calculations_SPHE_LMTD_Reynolds
from math import pi
import numpy as np
#endregion

#region Calculations
def SPHE_DeltaP(L, roh, roc, mh, mc, H, dh, dc, mih, mic):
    # pressure drop
    L_pies=L/0.3048
    mih_cp=mih * 1000
    mic_cp=mic * 1000
    dh_in=dh / 0.0254
    dc_in=dh / 0.0254
    H_in=H / 0.0254
    mh_m_klbhr= mh / 0.125998 # (3600*2.2046244202/1000)
    mc_m_klbhr= mc / 0.125998 # (3600*2.2046244202/1000)

    dltph = (0.001 * (L_pies / (roh / 998.2063)) * ((mh_m_klbhr/(H_in * dh_in)) ** 2) * 
             ((1.3 * mih_cp**(1/3)) / (dh_in + 0.125) * (H_in / mh_m_klbhr) ** (1 / 3) 
              + 1.5 + 16 / L_pies))*6894.7572932 # Pa
    
    dltpc = (0.001 * (L_pies / ((roc / 998.2063))) * ((mc_m_klbhr / (H_in * dc_in)) ** 2) * 
             (((1.3 * (mic_cp ** (1 / 3))) / (dc_in + 0.125)) * ((H_in / mc_m_klbhr) ** (1 / 3)) 
              + 1.5 + 16 / L_pies))*6894.7572932 # Pa    
    
    return dltph, dltpc





def SPHE_DeltaP_lb(L, romax, mh, mc, H, dh, dc, mimin):
    L_pies=L/0.3048
    H_in=H / 0.0254
    mh_m_klbhr= mh / 0.125998 # (3600*2.2046244202/1000)
    mc_m_klbhr= mc / 0.125998 # (3600*2.2046244202/1000)
    dh_in=dh / 0.0254
    dc_in=dh / 0.0254

    dltphlb = (0.001 * (L_pies / (romax / 998.2063)) * (((mh_m_klbhr) / (H_in * (dh_in))) ** 2) *
             (((1.3 * ((mimin*1000 ) ** (1 / 3))) / ((dh_in) + 0.125)) * (
                         (H_in / (mh_m_klbhr)) ** (1 / 3))
              + 1.5 + 16 / L_pies))*6894.7572932 # Pa 
  
    dltpclb = (0.001 * ((L_pies) / ((romax / 998.2063))) * (((mc_m_klbhr) / ((H_in) * (dc_in))) ** 2) *
             (((1.3 * ((mimin*1000 ) ** (1 / 3))) / ((dc_in) + 0.125)) * (
                         ((H_in) / (mc_m_klbhr)) ** (1 / 3))
              + 1.5 + 16 / (L_pies)))*6894.7572932 # Pa 

    return dltphlb, dltpclb


#endregion