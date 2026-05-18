#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          02-Jan-2025     Mariana Mello               Original

##################################################################################################################
#endregion


#region Import Library
from Aircooler.Calculations import Calculations_aircooler_w_used, Calculations_aircooler_mc
#endregion

#region Calculations

def aircooler_TAC(int_rate, y, Ntr, Nr, Nbay, Nbbay, Dte, thk, Nf, tf, L, Nfanbay, Dfan, rp, Lf, Tco, Tci, etafan,
                  etasr, etamotor, hop, Cen, mh, Cph, Thi, Tho):
    Dti = Dte - 2*thk
    Df = Dte + 2*Lf
    # CRF - the capital recovery factor
    #CRF = (int_rate*(1+int_rate)*y) / ((1+int_rate)*y) - 1
    CRF = int_rate * ((1 + int_rate)**y) / (((1 + int_rate)**y) - 1)

    # Che - finned tube bundle cost
    Che = Ntr*Nr*Nbay*Nbbay*((10010*(Dte**2 - Dti**2) + 17193*(Df**2 - Dte**2)*Nf*tf + 1.27*Dte*Nf + 4.06)*L + 32.5)
    #Che = ((9988*((Dte**2)-(Dti**2))+17242*((Df**2)-(Dte**2))*Nf*tf + 1.27*Dte*Nf + 4.06)*L+32.5)*Ntr*Nr*Nbay

    wused = Calculations_aircooler_w_used.aircooler_w_used(mh, Cph, Thi, Tho, Nbay, Nfanbay, Dfan, rp, Ntr, Nbbay, L,
                                                           Dte, Nf, Lf, tf, Tco, Tci, Nr, etafan, etasr, etamotor)
    #print('W_USED',wused)

    # Cfs - the fan system investment cost
    Cfs = Nfanbay*Nbay*(1887.5 + 163.49*(Dfan**2) + 281.25*wused)
    #Cfs = (1887.5 + 159.95*(Dfan**2) + 3.5343*Dfan + 281.25*wused)*Nfanbay*Nbay

    # Cinv - capital cost
    Cinv = Che + Cfs
    #print('Cinv',Cinv*CRF)

    # Cmai - the yearly maintenance cost
    Cmai = 0.01*Che + 0.03*Cfs
    #print('Cmai',Cmai)

    # Cop - the operational cost
    Cop = hop*Cen*wused*Nbay*Nfanbay
    #Cop = (hop * Cen / 1000 / 0.7 / 0.95 / 1) * (DPc * pqfan * Nfanbay * Nbay) + (RoC / 2) * ((vfan ** 2) * pqfan * pNfanbay * pNbay)
    #print('Cop',Cop)

    # TAC - total annualized cost
    TAC = CRF*Cinv + Cmai + Cop

    return TAC

#endregion


# from Aircooler.Calculations import (
#     Calculations_aircooler_deltaP_air,
#     Calculations_aircooler_prop_rocout,
#     Calculations_aircooler_mc,
#     Calculations_aircooler_prop_roc)
# from math import pi
# hop = 7920
# Cen = 0.068
# rp = 2.5
# Nfanbay = 2
# Nbay = 2
# Ntr = 56
# L = 10.973
# Dte = 0.0254
# Nbbay = 1
# Nf = 393
# Lf = 0.015875
# tf = 0.000330
# Nr = 3
# mh = 31.5  # Flow rate (kg*s**-1)
# Cph = 2303.18258  # Heat capacity (J*(kg*K)**-1)
# Tci = 35.05  # Inlet temperature of the cold stream (oC)
# Tco = 65.65  # Outlet temperature of the cold stream (oC)
# Thi = 121.15  # Inlet temperature of the hot stream (oC)
# Tho = 65.65  # Outlet temperature of the hot stream (oC)
# Dfan = 3.2
# RoC = Calculations_aircooler_prop_roc.aircooler_calc_prop_air_roc(Tco, Tci)
# DPc = Calculations_aircooler_deltaP_air.aircooler_deltaP_air(rp, Ntr, Nbay, Nbbay, L, Dte, Nf, Lf, tf, Tco, Tci, Nr, mh, Cph, Thi, Tho)
# mc = Calculations_aircooler_mc.aircooler_mc(mh,Cph,Thi,Tho,Tco,Tci)
# rocout = Calculations_aircooler_prop_rocout.aircooler_calc_rocout(Tco)
# qfan = (mc / rocout) / (Nbay * Nfanbay)
# vfr = qfan / ((pi / 4) * (Dfan ** 2))
# dPfan = DPc + (RoC*(vfr**2))/2
# #print('Dpfan',dPfan)
#
# Cop = (hop * Cen / 1000 / 0.7 / 0.95 / 1) * (DPc * qfan * Nfanbay * Nbay) + ((RoC / 2) * ((vfr ** 2) * qfan * Nfanbay * Nbay))
# print('Cop',Cop)