#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          2025            Andre Nahes               Original
#   0.2          28-Feb-2025     Mariana Mello             Proposed
#   0.3          07-May-2025     Mariana Mello             Update to fix error in Ntcc/Jr
#   0.4          12-May-2025     Mariana Mello             Changed name from 'pd' to 'm_p'
#   0.5          01-Jul-2025     Augusto Vieira            Fixed scalar assignment error by forcing array logic

##################################################################################################################
#endregion


#region Import Library
import numpy as np
from STHE.Calculations import Calculations_STHE_Reynolds_shellside, Calculations_STHE_countingtable
from math import pi
# endregion
###################################################################################################################

# region Calculations: Parameters

#region Function: STHE_shellside_Nusseltparameters
def STHE_shellside_Nusseltparameters(Ds, dte, rp, lay, L, Nb, ms, ros, mis, m_p):
    # Force inputs as arrays to prevent scalar indexing errors
    lay = np.atleast_1d(lay)
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p)
    Res = np.atleast_1d(Res)

    # Initialize condition masks
    CondLay30 = np.zeros_like(Res, dtype=bool)
    CondLay45 = np.zeros_like(Res, dtype=bool)
    CondLay90 = np.zeros_like(Res, dtype=bool)
    CondRes   = np.zeros_like(Res, dtype=bool)

    CondInter30 = np.zeros_like(Res, dtype=bool)
    CondInter45 = np.zeros_like(Res, dtype=bool)
    CondInter90 = np.zeros_like(Res, dtype=bool)

    # Set layout masks
    CondLay30[lay == 2] = True
    CondLay45[lay == 3] = True
    CondLay90[lay == 1] = True

    pa_1 = np.ones_like(Res)
    pa_2 = np.ones_like(Res)
    pa_3 = np.ones_like(Res)
    pa_4 = np.ones_like(Res)

    # Region 1
    pa_1[CondLay30] = 1.4
    pa_1[CondLay45] = 1.55
    pa_1[CondLay90] = 0.97
    pa_2[:] = -0.667

    # Region 2
    CondRes[Res > 10] = True
    CondInter30 = np.logical_and(CondRes, CondLay30)
    CondInter45 = np.logical_and(CondRes, CondLay45)
    CondInter90 = np.logical_and(CondRes, CondLay90)

    pa_1[CondInter30] = 1.36
    pa_1[CondInter45] = 0.498
    pa_1[CondInter90] = 0.9

    pa_2[CondInter30] = -0.657
    pa_2[CondInter45] = -0.656
    pa_2[CondInter90] = -0.631

    # Region 3
    CondRes[:] = False
    CondRes[Res > 1e2] = True
    CondInter30 = np.logical_and(CondRes, CondLay30)
    CondInter45 = np.logical_and(CondRes, CondLay45)
    CondInter90 = np.logical_and(CondRes, CondLay90)

    pa_1[CondInter30] = 0.593
    pa_1[CondInter45] = 0.73
    pa_1[CondInter90] = 0.408

    pa_2[CondInter30] = -0.477
    pa_2[CondInter45] = -0.5
    pa_2[CondInter90] = -0.46

    # Region 4
    CondRes[:] = False
    CondRes[Res > 1e3] = True
    CondInter30 = np.logical_and(CondRes, CondLay30)
    CondInter45 = np.logical_and(CondRes, CondLay45)
    CondInter90 = np.logical_and(CondRes, CondLay90)

    pa_1[CondInter30] = 0.321
    pa_1[CondInter45] = 0.37
    pa_1[CondInter90] = 0.107

    pa_2[CondInter30] = -0.388
    pa_2[CondInter45] = -0.396
    pa_2[CondInter90] = -0.266

    # Region 5
    CondRes[:] = False
    CondRes[Res > 1e4] = True
    CondInter30 = np.logical_and(CondRes, CondLay30)
    CondInter45 = np.logical_and(CondRes, CondLay45)
    CondInter90 = np.logical_and(CondRes, CondLay90)

    pa_1[CondInter30] = 0.321
    pa_1[CondInter45] = 0.37
    pa_1[CondInter90] = 0.37

    pa_2[CondInter30] = -0.388
    pa_2[CondInter45] = -0.396
    pa_2[CondInter90] = -0.395

    # pa_3 and pa_4 are layout-dependent
    pa_3[CondLay30] = 1.45
    pa_3[CondLay45] = 1.93
    pa_3[CondLay90] = 1.187

    pa_4[CondLay30] = 0.519
    pa_4[CondLay45] = 0.5
    pa_4[CondLay90] = 0.37

    return pa_1, pa_2, pa_3, pa_4

#endregion

def STHE_shellside_DeltaPparameters(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p):

    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p)

    CondLay30 = Res < -10e10 # conjunto dos elementos triangulares (lay = 2)
    CondLay45 = Res < -10e10 # conjunto dos elementos quadrados (lay = 1)
    CondLay90 = Res < -10e10 # conjunto dos elementos quadrados rodado (lay = 3)
    CondRes   = Res < -10e10

    CondInter30 = Res < -10e10
    CondInter45 = Res < -10e10
    CondInter90 = Res < -10e10

    CondLay30[lay == 2] = True
    CondLay45[lay == 3] = True
    CondLay90[lay == 1] = True

    pb_1 = np.ones(Res.shape)
    pb_2 = np.ones(Res.shape)
    pb_3 = np.ones(Res.shape)
    pb_4 = np.ones(Res.shape)

    # 1° faixa de reynolds
    pb_1[CondLay30] = 48
    pb_1[CondLay45] = 32
    pb_1[CondLay90] = 35

    pb_2[:] = -1

    # 2° faixa de reynolds
    CondRes[Res > 10] = True
    CondInter30 = np.logical_and(CondRes,CondLay30)
    CondInter45 = np.logical_and(CondRes, CondLay45)
    CondInter90 = np.logical_and(CondRes, CondLay90)

    pb_1[CondInter30] = 45.1
    pb_1[CondInter45] = 26.2
    pb_1[CondInter90] = 32.1

    pb_2[CondInter30] = -0.973
    pb_2[CondInter45] = -0.913
    pb_2[CondInter90] = -0.963

    # 3° faixa de reynolds
    CondRes   = Res < -10e10
    CondRes[Res > 1e2] = True
    CondInter30 = np.logical_and(CondRes,CondLay30)
    CondInter45 = np.logical_and(CondRes, CondLay45)
    CondInter90 = np.logical_and(CondRes, CondLay90)

    pb_1[CondInter30] = 4.57
    pb_1[CondInter45] = 3.5
    pb_1[CondInter90] = 6.09

    pb_2[CondInter30] = -0.476
    pb_2[CondInter45] = -0.476
    pb_2[CondInter90] = -0.602

    # 4° faixa de reynolds
    CondRes   = Res < -10e10
    CondRes[Res > 1e3] = True
    CondInter30 = np.logical_and(CondRes,CondLay30)
    CondInter45 = np.logical_and(CondRes, CondLay45)
    CondInter90 = np.logical_and(CondRes, CondLay90)

    pb_1[CondInter30] = 0.486
    pb_1[CondInter45] = 0.333
    pb_1[CondInter90] = 0.0815

    pb_2[CondInter30] = -0.152
    pb_2[CondInter45] = -0.136
    pb_2[CondInter90] = -0.022

    # 5° faixa de reynolds
    CondRes   = Res < -10e10
    CondRes[Res > 1e4] = True
    CondInter30 = np.logical_and(CondRes, CondLay30)
    CondInter45 = np.logical_and(CondRes, CondLay45)
    CondInter90 = np.logical_and(CondRes, CondLay90)

    pb_1[CondInter30] = 0.372
    pb_1[CondInter45] = 0.303
    pb_1[CondInter90] = 0.391

    pb_2[CondInter30] = -0.123
    pb_2[CondInter45] = -0.126
    pb_2[CondInter90] = -0.148

    pb_3[CondLay30] = 7
    pb_3[CondLay45] = 6.59
    pb_3[CondLay90] = 6.3

    pb_4[CondLay30] = 0.5
    pb_4[CondLay45] = 0.52
    pb_4[CondLay90] = 0.378

    return pb_1, pb_2, pb_3, pb_4



# endregion

###################################################################################################

# region Calculations: General
def STHE_Lbb_func(Ds, m_p):

    #if len(m_p['Lbb_g']) == 0:
    Lbb = 0.0048*Ds + 0.0128
    #else:
    #    Lbb = np.array(m_p['Lbb_g'])

    return Lbb

def STHE_Ltb_func(Ds, dte, m_p):
    # Ensure arrays for broadcast-safe operations
    Ds = np.atleast_1d(Ds)
    dte = np.atleast_1d(dte)

    Ltb = np.ones(Ds.shape) * 0.8e-3

    # Define masking conditions as arrays
    Cond_1 = np.zeros_like(dte, dtype=bool)
    Cond_2 = np.zeros_like(dte, dtype=bool)
    CondInter = np.zeros_like(dte, dtype=bool)

    # Assign conditions safely
    Cond_1[dte <= 31.75e-3] = True
    Cond_2[(52e3 * dte + 532) > 0.9] = True
    CondInter = np.logical_and(Cond_1, Cond_2)

    Ltb[CondInter] = 0.4e-3

    # Return scalar if inputs were scalar
    return Ltb


def STHE_Lsb_func(Ds, m_p):

    #if len(m_p['Lsb_g']) == 0:
    Lsb = 3.1e-3 + (0.004*Ds)
    #else:
    #    Lsb = np.array(m_p['Lsb_g'])

    return Lsb

def STHE_shellside_Sm(Ds, dte, rp, lay, L, Nb, m_p):
    # Description // Descrição
    # Cross flow area // Área de escoamento cruzado

    # Shell - bundle leakage // Folga casco - matriz tubular
    Lbb = STHE_Lbb_func(Ds, m_p)

    # Circumference of tube bundle // Circunferencia da matriz tubular
    Dotl = Ds - Lbb

    # Circumference of the centers of the external tubes // Circunferência dos centros dos tubos externos(Dctl)
    Dctl = Dotl - dte

    # Tube pitch // passo nos tubos
    Ltp = np.atleast_1d(rp) * np.atleast_1d(dte)  # Ensure array for safe indexing

    # Layout as array for robust indexing
    lay = np.atleast_1d(lay)

    # Effective pitch // Ltp efetivo
    Ltpeff = np.copy(Ltp)  # ← Update: avoid item assignment on scalar
    Ltpeff[lay == 2] = 0.866 * Ltp[lay == 2]
    Ltpeff[lay == 3] = 0.707 * Ltp[lay == 3]
    # ↑ Change added on 01-Jul-2025 by Augusto Vieira to prevent assignment error on scalar input

    # Baffle spacing // Espaçamento entre as chicanas
    lbc = (L / (Nb + 1))

    # Cross flow area whitout considering the hydraulic impact // Área de escoamento cruzado sem consider o impacto hidráulico da deposição
    Sm = lbc * (Lbb + Dctl * ((Ltp - dte) / Ltpeff))

    return Sm


def STHE_shellside_Ssb(Ds, Bc, m_p):
    # Description // Descrição
    # By-pass area between the shell and baffles // Área de by-pass entre o casco e as chicanas

    #fts_thk = fts_thk * 0
    # Central angle of the rope relative to the cutting of the baffle in relation to the diameter of the hull // Ângulo central da corda relativa ao corte da chicana em relação ao diâmetro do casco (tetads)
    teta_Ds = 2*np.arccos((1 - (2*Bc)))

    # Shell - baffle leakage // Folga casco-chicana
    Lsb = STHE_Lsb_func(Ds, m_p)

    # By-pass area considering the fouling thickness // Cálculo da área podendo considerar a espessura de depósito
    #Ssb = pi * Ds * ( ( Lsb - 2 * fts_thk) / 2) * (((2 * pi) - teta_Ds) / (2 * pi))

    # # By-pass area considering the fouling thickness // Cálculo da área podendo considerar a espessura de depósito
    #Ssb = pi * Ds * (Lsb/2) * (((2 * pi) - teta_Ds) / (2 * pi))

    #Ssb[Ssb < 0] = 1e-15

    # No fouling model equation (original one) // Equação sem o modelo de depósição (original)
    Ssb = pi * Ds * (Lsb/2) * (((2 * pi) - teta_Ds) / (2 * pi))

    return Ssb

def STHE_shellside_Stb(Ds, dte, Npt, rp, lay, Bc, m_p):
    # Description // Descrição
    # Leakage area between the tube and the baffles // Área de vazamento entre o tubo e as chicanas

    #fts_thk = fts_thk * 0

    # Number of tubes (counting table) // Número de tubos

    Ntt = Calculations_STHE_countingtable.STHE_counting_table(Ds, dte, Npt, rp, lay, m_p)
    # Tube - baffle leakage // Folga tubo-chicana
    Ltb = STHE_Ltb_func(Ds, dte, m_p)

    # Shell - bundle leakage // Folga casco - matriz tubular
    Lbb = STHE_Lbb_func(Ds, m_p)

    # Circumference of tube bundle // Circunferencia da matriz tubular
    Dotl = Ds - Lbb

    # Circumference of the centers of the external tubes // Circunferência dos centros dos tubos externos(Dctl)
    Dctl = Dotl - dte

    # Central angle of the intersection of the baffle cut with the circumference of the centers of the external tubes // Ângulo central da interseção do corte da chicana com a circunf. dos centros dos tubos externos (tetactl)
    teta_ctl = 2 * np.arccos((Ds/Dctl) * (1 - 2 * Bc))

    # Tube fraction in the window // Fração de tubos na região das janelas(Fw)
    Fw = (teta_ctl - np.sin(teta_ctl)) / (2 * pi)

    # dte + Ltb é o buraco da chicana, esse não mexe. O que muda é dte + 2 * fts

    # Fouling model
    #Stb = Ntt * (1 - Fw) * ((pi / 4) * ((dte + Ltb) ** 2 - (dte + 2 * fts_thk) ** 2))

    # # Fouling model
    Stb = Ntt * (1 - Fw) * ((pi / 4) * (((dte + Ltb)**2) - (dte ** 2)))

    Stb[Stb < 0] = 0

    # No fouling model
    #Stb = max(0,Ntt * (1 - Fw) * ((pi / 4) * ((dte + Ltb) ** 2 - (dte ** 2))))

    return Stb

def STHE_shellside_Sb(Ds, L, Nb, m_p):
    # Description // Descrição
    # By-pass area between the shell and tube bundle // Área de by-pass entre o casco e a matriz tubular

    #fts_thk = fts_thk * 0
    # Shell - bundle leakage // Folga casco - matriz tubular
    Lbb = STHE_Lbb_func(Ds, m_p)

    # Circumference of tube bundle // Circunferencia da matriz tubular
    Dotl = Ds - Lbb

    # Baffle spacing // Espaçamento entre as chicanas
    lbc = (L / (Nb + 1))

    # By pass area considering the hydraulic impact with the fouling model // Área de by-pass considerando a espessura de depósito
    #Sb = (lbc) * ((Lbb - 4 * fts_thk))

    # # By pass area considering the hydraulic impact with the fouling model // Área de by-pass considerando a espessura de depósito
    # Sb = (lbc) * ((Lbb - 2 * fts_thk))

    #Sb[Sb < 0] = 0

    # By pass area without considering the hydraulic impact with the fouling model // Área de by-pass sem consider a espessura de depósito
    Sb = lbc*(Ds - Dotl)
    #print('Sb',Sb)

    return Sb

def STHE_shellside_Ntcc(Ds, dte, rp, lay, Bc):

    # Tube pitch
    Ltp = rp * dte

    # Distance between tubes in flow direction
    Lpp = np.copy(Ltp)
    Lpp[lay == 2] = 0.866 * Ltp[lay == 2]
    Lpp[lay == 3] = 0.707 * Ltp[lay == 3]

    Ntcc = (Ds / Lpp) * (1 - (2 * Bc))

    return Ntcc

def STHE_shellside_Ntcw(Ds, dte, Npt, rp, lay, L):
    # Garantir arrays para operações seguras
    Ds = np.atleast_1d(Ds)
    dte = np.atleast_1d(dte)
    Npt = np.atleast_1d(Npt)
    rp = np.atleast_1d(rp)
    lay = np.atleast_1d(lay)

    # Tube pitch
    Ltp = rp * dte

    # Inicializa Lpp como cópia de Ltp
    Lpp = np.copy(Ltp)
    Lpp[lay == 2] = 0.866 * Ltp[lay == 2]
    Lpp[lay == 3] = 0.707 * Ltp[lay == 3]

    # Número de tubos cruzados em um caminho de fluxo
    Ntcw = L / Lpp

    return Ntcw


def STHE_shellside_WindowAreas(Ds, dte, Npt, rp, lay, Bc, m_p):
    # Description // Descrição
    # Window areas - Area occupied by the tubes (Swt), Total window area (Swg), Free window area (Sw)  // Áreas da região das janelas

    # Number of tubes (Counting table) // Número total de tubos
    Ntt = Calculations_STHE_countingtable.STHE_counting_table(Ds, dte, Npt, rp, lay, m_p)
    # Central angle of the rope relative to the cutting of the baffle in relation to the diameter of the hull // Ângulo central da corda relativa ao corte da chicana em relação ao diâmetro do casco (tetads)
    teta_Ds = 2 * np.arccos((1 - (2 * Bc)))

    # Shell - bundle leakage // Folga casco - matriz tubular
    Lbb = STHE_Lbb_func(Ds, m_p)

    # Circumference of tube bundle // Circunferencia da matriz tubular
    Dotl = Ds - Lbb

    # Circumference of the centers of the external tubes // Circunferência dos centros dos tubos externos(Dctl)
    Dctl = Dotl - dte

    # Central angle of the intersection of the baffle cut with the circumference of the centers of the external tubes // Ângulo central da interseção do corte da chicana com a circunf. dos centros dos tubos externos (tetactl)
    teta_ctl = 2 * np.arccos((Ds / Dctl) * (1 - 2 * Bc))

    # Tube fraction in the window // Fração de tubos na região das janelas(Fw)
    Fw = (teta_ctl - np.sin(teta_ctl)) / (2 * pi)

    # Number of tubes in the window // Número de tubos na região das janelas (Ntw)
    Ntw = (Ntt * Fw)

    # Area occupied by the tubes // Área na região da janela ocupadas pelos tubos (Swt) (como se o tubo aumentasse)
    #Swt = Ntw * (pi / 4) * (dte + 2 * fts_thk) ** 2
    Swt = Ntw * (pi / 4) * (dte**2)

    # Window area // Área na região das janelas (Swg)  (área de um segmento circular)
    # Fouling model
    #Swg = (pi / 4) * (Ds - 2 * fts_thk) ** 2 * ((teta_Ds - np.sin(teta_Ds)) / (2 * pi))

    # No fouling
    Swg = (pi / 4) * (Ds**2) * ((teta_Ds - np.sin(teta_Ds)) / (2 * pi))

    # Window free area // Área livre de escoamento na região das janelas (Sw)
    Sw = Swg - Swt

    return Swt, Swg, Sw

def STHE_shellside_Dw(Ds, dte, Npt, rp, lay, Bc, m_p):
    # Description // Descrição
    # Hydraulic diameter  // Diâmetro hidráulico

    # Total number of tubes (Counting table) // Número total de tubos
    Ntt = Calculations_STHE_countingtable.STHE_counting_table(Ds, dte, Npt, rp, lay, m_p)
    # Central angle of the rope relative to the cutting of the baffle in relation to the diameter of the hull // Ângulo central da corda relativa ao corte da chicana em relação ao diâmetro do casco (tetads)
    teta_Ds = 2 * np.arccos((1 - (2 * Bc)))

    # Shell - bundle leakage // Folga casco - matriz tubular
    Lbb = STHE_Lbb_func(Ds, m_p)

    # Circumference of tube bundle // Circunferencia da matriz tubular
    Dotl = Ds - Lbb

    # Circumference of the centers of the external tubes // Circunferência dos centros dos tubos externos(Dctl)
    Dctl = Dotl - dte

    # Central angle of the intersection of the baffle cut with the circumference of the centers of the external tubes // Ângulo central da interseção do corte da chicana com a circunf. dos centros dos tubos externos (tetactl)
    teta_ctl = 2 * np.arccos((Ds / Dctl) * (1 - 2 * Bc))

    # Tube fraction in the window // Fração de tubos na região das janelas(Fw)
    Fw = (teta_ctl - np.sin(teta_ctl)) / (2 * pi)

    # Number of tubes in the window // Número de tubos na região das janelas (Ntw)
    Ntw = (Ntt * Fw)

    # Window areas // Áreas da janela
    Swt, Swg, Sw = STHE_shellside_WindowAreas(Ds, dte, Npt, rp, lay, Bc, m_p)

    # Fouling model // Modelo novo
    #Dw = (4 * Sw) / ((pi * (dte + 2 * fts_thk) * Ntw) + (pi * (Ds - 2 * fts_thk) * (teta_Ds / (2 * pi))))

    # # Fouling model // Modelo novo
    # Dw = (4 * Sw) / ((pi * (dte + 2 * fts_thk) * Ntw) + (pi * (Ds) * (teta_Ds / (2 * pi))))

    # No fouling model
    Dw = (4*Sw) / ((pi*dte*Ntw) + (pi*Ds*(teta_Ds/(2*pi))))

    return Dw

def STHE_shellside_Rl(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Description // Descrição
    # Correction factor for baffle leakage effects // Fator de correção para a folga nas chicanas - > Perda de carga

    # Cross flow area // Área de escoamento cruzado
    Sm = STHE_shellside_Sm(Ds, dte, rp, lay, L, Nb, m_p)

    # By-pass area between the shell and baffle // Área de by-pass entre o casco e as chicanas
    Ssb = STHE_shellside_Ssb(Ds, Bc, m_p)

    # Tube and baffle leakage area // Área de vazamento entre os tubos e as chicanas (Stb)
    Stb = STHE_shellside_Stb(Ds, dte, Npt, rp, lay, Bc, m_p)

    # Razão entre a área de vazamento casco-chicana e a soma das área de vazamento
    rs = Ssb / (Ssb + Stb)

    # Razão entre as áreas de vazamentos e a área de escoamento cruzado
    rlm = (Ssb + Stb) / Sm

    p = (-0.15*(1+rs)) + 0.8

    Rl = np.exp(-1.33 * (1 + rs) * (rlm**p))

    return Rl

def STHE_shellside_Rb(ms, ros, mis, Ds, dte, rp, lay, L, Nb, Bc, m_p):
    # Description // Descrição
    # Correction factor for bundle bypass // Fator de correção para o by-pass do feixe - > Perda de carga

    # Reynolds Number // Número de Reynolds
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p)

    # Cbp parameters // Parâmetro Cbp
    Cbp = np.ones(Ds.shape)*4.5
    Cbp[Res > 100] = 3.7

    # Tube rows in cross flow // Filas de tubos em escoamento cruzado (sem os tubos nas janelas)
    Ntcc = STHE_shellside_Ntcc(Ds, dte, rp, lay, Bc)

    # Razão entre número de tiras de selagem e filas de tubos
    rss = m_p['Nss'] / Ntcc

    # Cross flow area // Área de escoamento cruzado
    Sm = STHE_shellside_Sm(Ds, dte, rp, lay, L, Nb, m_p)

    # By-pass area between the shell and bundle // Área de by-pass entre o casco e a matriz tubular
    Sb = STHE_shellside_Sb(Ds, L, Nb, m_p)

    # By-pass area between the shell and bundle and the cross flow area ratio // Razão entre a área de by-pass casco-matriz tubular e a área de escoamento cruzado (Fsbp)
    Fsbp = Sb / Sm

    Rb = np.exp(- Cbp * Fsbp * (1 - ((2*rss)**(1/3))))

    return Rb

# endregion

################################################################################################################

# region Calculations: Convective Coefficient shell-side
def STHE_shellside_Idealcrossflowh(Ds, dte, rp, lay, L, Nb, ms, ros, mis, Cps, ks, m_p):
    # Description // Descrição
    # Convective heat transfer coefficient // Coeficiente de convecção

    # Reynolds Number // Número de Reynolds
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p)

    # Prandtl number // Número de Prandtl
    #Prs = m_p['Cps'] * m_p['mis'] / m_p['ks']
    Prs = Cps*mis / ks

    # Cross flow area // Área de escoamento cruzado
    Sm = STHE_shellside_Sm(Ds, dte, rp, lay, L, Nb, m_p)

    # Mass flux // Fluxo mássico
    #Gs = m_p['ms'] / Sm
    Gs = ms / Sm

    # Model parameters // Parâmetros do modelo
    pa1, pa2, pa3, pa4 = STHE_shellside_Nusseltparameters(Ds, dte, rp, lay, L, Nb, ms, ros, mis, m_p)

    # Tube pitch // Passo dos tubos
    Ltp = rp * dte

    par_a = pa3 / (1 + (0.14*(Res**pa4)))
    #pji = pa1 * (1.33 / (Ltp / (dte + 2 * fts_thk))) ** ( pa3 / (1 + 0.14 * Res ** pa4)) * Res ** pa2  #MUDAAAAR#################
    #pji = pa1 * (1.33/(Ltp/dte))**(pa3 / (1 + 0.14*Res**pa4)) * Res**pa2
    pji = pa1 * ((1.33 / (Ltp / dte))**par_a) * (Res**pa2)

    #phi = pji * m_p['Cps'] * Gs * (Prs ** (-2 / 3))
    phi = pji*Cps*Gs*(Prs**(-2/3))

    return phi

def STHE_shellside_Jc(Ds, dte, Bc, m_p):
    # Description // Descrição
    # Segmental baffle window correction // Fator de correção proveniente da janela

    # Shell - bundle leakage // Folga casco - matriz tubular
    Lbb = STHE_Lbb_func(Ds, m_p)

    # Circumference of tube bundle // Circunferencia da matriz tubular
    Dotl = Ds - Lbb

    # Circumference of the centers of the external tubes // Circunferência dos centros dos tubos externos(Dctl)
    Dctl = Dotl - dte

    # Central angle of the intersection of the baffle cut with the circumference of the centers of the external tubes // Ângulo central da interseção do corte da chicana com a circunf. dos centros dos tubos externos (tetactl)
    teta_ctl = 2 * np.arccos((Ds/Dctl) * (1 - 2*Bc))

    # Tube fraction in window region // Fração de tubos na região das janelas(Fw)
    Fw = (teta_ctl - np.sin(teta_ctl)) / (2*pi)

    # Tube fraction in cross flow // Fração de tubos na região escoamento cruzado(Fw)
    Fc = 1 - (2*Fw)

    Jc = 0.55 + (0.72*Fc)

    return Jc

def STHE_shellside_Jl(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Description // Descrição
    # Correction factor for baffle leakeage effects // Fator de correção proveniente das folgas na chicana

    # Cross flow area // Área de escoamento cruzado
    Sm = STHE_shellside_Sm(Ds, dte, rp, lay, L, Nb, m_p)

    # By-pass area between the shell and baffle // Área de by-pass entre o casco e as chicanas
    Ssb = STHE_shellside_Ssb(Ds, Bc, m_p)

    # Tube and baffle leakage area // Área de vazamento entre os tubos e as chicanas (Stb)
    Stb = STHE_shellside_Stb(Ds, dte, Npt, rp, lay, Bc, m_p)

    # Razão entre a área de vazamento casco-chicana e a soma das área de vazamento
    rs = Ssb / (Ssb + Stb)

    # Razão entre as áreas de vazamentos e a área de escoamento cruzado
    rlm = (Ssb + Stb) / Sm

    Jl = (0.44*(1-rs)) + ((1-(0.44*(1-rs)))*np.exp(-2.2*rlm))

    return Jl

def STHE_shellside_Jb1(Ds, dte, Npt, rp, lay, ms, ros, mis, L, Nb, Bc, m_p):
    # Description // Descrição
    # Correction factor for bundle bypass // Fator de correção proveniente do by-pass do feixe

    # Reynolds Number // Número de Reynolds
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p)
    Res = np.atleast_1d(Res)  # ← Ensure array for safe indexing

    # Cbp parameter // Parâmetro Cbp
    Cbh = np.ones_like(Res) * 1.35
    Cbh[Res > 100] = 1.25

    # Tube rows in the cross flow region // Filas de tubos em escoamento cruzado (sem os tubos nas janelas)
    Ntcc = STHE_shellside_Ntcc(Ds, dte, rp, lay, Bc)

    # Razão entre número de tiras de selagem e filas de tubos
    rss = m_p['Nss'] / Ntcc

    # Cross flow area // Área de escoamento cruzado
    Sm = STHE_shellside_Sm(Ds, dte, rp, lay, L, Nb, m_p)

    # Shell and bundle by-pass area // Área de by-pass entre o casco e a matriz tubular
    Sb = STHE_shellside_Sb(Ds, L, Nb, m_p)

    # Razão entre a área de by-pass casco-matriz tubular e a área de escoamento cruzado (Fsbp)
    Fsbp = Sb / Sm

    Jb1 = np.exp(- Cbh * Fsbp * (1 - ((2*rss)**(1/3))))

    return Jb1


def STHE_shellside_Jr(Ds, dte, Npt, rp, lay, L, Nb, ms, ros, mis, Bc, m_p):
    # Description // Descrição
    # Correction factor for laminar flow // Fator de correção para escoamento laminar

    # Reynolds Number //  Número de Reynolds
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p)

    # Tube rows in cross flow region // Filas de tubos em escoamento cruzado (sem os tubos nas janelas)
    #Ntcc = STHE_shellside_Ntcc(Ds, dte, Npt, rp, lay)
    Ntcc = STHE_shellside_Ntcc(Ds, dte, rp, lay, Bc)
    #print('Ntcc',Ntcc)


    # Tube rows in window region // Filas de tubos na janela
    Ntcw = STHE_shellside_Ntcw(Ds, dte, Npt, rp, lay, L)
    #print('Ntcw',Ntcw)

    # Total number of tubes rows crossed in the entire exchanger //
    Nc = (Ntcc + Ntcw) * (Nb + 1)
    #print('Nc', Nc)

    Jr1 = (10/Nc)**0.18
    #print(Jr1)
    Jr2 = Jr1 + (((20-Res)/80) * (Jr1 - 1))

    Jr = Jr1

    Jr[Res > 20] = Jr2[Res > 20]
    Jr[Res > 100] = 1

    return Jr

# endregion

#####################################################################################################################

# region Calculations: Friction Factor
def STHE_shellside_IdealcrossflowFrictionFactor(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p):
    # Description // Descrição
    # Ideal shell-side cross flow friction factor // Fator de atrito para o escoamento cruzado ideal

    # Reynolds number // Número de Reynolds
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p)

    # Friction factor parameters // Parâmetros do modelo de fator de atrito
    pb_1, pb_2, pb_3, pb_4 = STHE_shellside_DeltaPparameters(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p)

    # Tube pitch // Passo nos tubos
    Ltp = rp * dte

    # Model considering the fouling layer // Modelo considerando a camada de deposição
    #fs = pb_1 * (1.33 / (Ltp / (dte + 2 * fts_thk))) ** (pb_3 / (1 + 0.14 * Res ** pb_4)) * Res ** pb_2

    # Model without considering the fouling layer // Modelo sem consider a camada de deposição
    par_b = pb_3 / (1 + (0.14*(Res**pb_4)))
    #fs = pb_1 * (1.33 / (Ltp/dte)) ** (pb_3 / (1 + 0.14 * Res ** pb_4)) * Res ** pb_2
    fs = pb_1 * ((1.33 / (Ltp/dte))**par_b) * (Res**pb_2)

    return fs

# endregion

#################################################################################################################

# region Calculations: Pressure Drop shell-side

def STHE_shellside_IdealcrossflowDeltaP(ms, ros, mis, Ds, dte, rp, lay, L, Nb, Bc, m_p):
    # Description // Descrição
    # Ideal shell-side cross flow pressure drop // Perda de carga para o escoamento cruzado ideal

    # Cross flow area // Área de escoamento cruzado
    Sm = STHE_shellside_Sm(Ds, dte, rp, lay, L, Nb, m_p)

    # ideal cross flow friction factor // Fator de atrito para escoamento ideal
    fs = STHE_shellside_IdealcrossflowFrictionFactor(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p)

    # Tube row in cross flow // Filas de tubos em escoamento cruzado (sem os tubos nas janelas)
    Ntcc = STHE_shellside_Ntcc(Ds, dte, rp, lay, Bc)

    # Mass flux // Fluxo mássico
    #Gs = m_p['ms'] / Sm
    Gs = ms / Sm

    #DeltaPbi = 2 * fs * Ntcc * (1 / m_p['ros']) * (Gs ** 2)
    DeltaPbi = 2 * fs * Ntcc * (1 / ros) * (Gs ** 2)
    #print('DeltaPbi', DeltaPbi)

    return DeltaPbi

def STHE_shellside_crossflowDeltaP(ms, ros, mis, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Description // Descrição
    # Cross flow pressure drop // Perda de carga no escoamento cruzado

    # Correction factor for bundle bypass // Feixe by-pass fator de correção
    Rb = STHE_shellside_Rb(ms, ros, mis, Ds, dte, rp, lay, L, Nb, Bc, m_p)

    # Correction factor for baffle leakeage effects // Fator de correção devido às folgas na chicana
    Rl = STHE_shellside_Rl(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)

    # Ideal cross flow pressure drop // Perda de carga em um escoamento cruzado ideal
    DPbi = STHE_shellside_IdealcrossflowDeltaP(ms, ros, mis, Ds, dte, rp, lay, L, Nb, Bc, m_p)

    DeltaPc = DPbi * (Nb - 1) * Rb * Rl

    return DeltaPc

def STHE_shellside_BaffleWidownDeltaP(ms, ros, mis, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    # Description // Descrição
    # Baffle window pressure drop // Perda de carga na região da janela

    # Reynolds number // Reynolds Number
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(ms, ros, mis, Ds, dte, rp, lay, L, Nb, m_p)

    # Cross flow area // Área de escoamento cruzado
    Sm = STHE_shellside_Sm(Ds, dte, rp, lay, L, Nb, m_p)

    # Area occupied by the tubes (Swt), Total window area (Swg), Free window area (Sw)
    # Área na região da janela ocupadas pelos tubos (Swt); Área na região das janelas (Swg); Área livre de escoamento na região das janelas (Sw)
    Swt, Swg, Sw = STHE_shellside_WindowAreas(Ds, dte, Npt, rp, lay, Bc, m_p)

    # Mass flux in window // Fluxo na região da janela
    #Gw = m_p['ms'] / ((Sm * Sw) ** (1 / 2))
    Gw = ms / ((Sm * Sw) ** (1 / 2))

    # Hydraulic diameter // Diâmetro hidráulico
    Dw = STHE_shellside_Dw(Ds, dte, Npt, rp, lay, Bc, m_p)

    # Tube pitch // Passo dos tubos
    Ltp = rp * dte

    # Effective number of tube rows in the window // Número efetivo de filas de tubos na região das janelas (Ntcw)
    Ntcw = STHE_shellside_Ntcw(Ds, dte, Npt, rp, lay, L)

    # Baffle spacing // espaçamento entre as chicanas
    lbc = (L / (Nb + 1))

    # Correction factor for baffle leakeage effects // Fator de correção devido aos efeitos da chicana
    Rl = STHE_shellside_Rl(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)

    # Window pressure drop for laminar flow // Perda de carga na janela para regime laminar
    #DPwlam = Nb * Rl * (
    #            ((26 * Gw * m_p['ms']) / m_p['ros']) * ((Ntcw / (Ltp - dte - 2 * fts_thk)) + (lbc / (Dw ** 2))) + (
    #                (2 / m_p['ros']) * (Gw ** 2)))

    # Without considering fouling model
    # Window pressure drop for laminar flow // Perda de carga na janela para regime laminar
    DPwlam = Nb * Rl * (((26 * Gw * ms) / ros) * ((Ntcw / (Ltp - dte)) + (lbc / (Dw ** 2))) + ((2 / ros) * (Gw**2)))

    # Window pressure drop for turbulent flow // Perda de carga na janela para regime turbulento
    #DPwturb = Nb * Rl * (2 + (0.6 * Ntcw)) * ((1) / (2 * m_p['ros'])) * (Gw**2)
    DPwturb = Nb * Rl * (2 + (0.6 * Ntcw)) * (1 / (2 * ros)) * (Gw ** 2)

    # Window pressure drop // Perda de carga na janela
    Delta_Pw = DPwlam
    Delta_Pw[Res >= 100] = DPwturb[Res >= 100]

    return Delta_Pw

def STHE_shellside_EndZonesDeltaP(ms, ros, mis, Ds, dte,Npt, rp, lay, L, Nb, Bc, m_p):
    # Description // Descrição
    # End zone pressure drop // Perda de carga na zona morta

    # Number of tube rows in cross flow // Filas de tubos em escoamento cruzado (sem os tubos nas janelas)
    Ntcc = STHE_shellside_Ntcc(Ds, dte, rp, lay, Bc)

    # Effective number of tube rows in window // Número efetivo de filas de tubos na região das janelas (Ntcw)
    Ntcw = STHE_shellside_Ntcw(Ds, dte, Npt, rp, lay, L)

    # Correction factor for bundle bypass // Fator de correção devido ao by-pass do feixe
    Rb = STHE_shellside_Rb(ms, ros, mis, Ds, dte, rp, lay, L, Nb, Bc, m_p)

    # Ideal cross flow pressure drop // Perda de carga em um escoamento cruzado ideal
    DPbi = STHE_shellside_IdealcrossflowDeltaP(ms, ros, mis, Ds, dte, rp, lay, L, Nb, Bc, m_p)

    DeltaPe = 2 * DPbi * Rb * (1 + (Ntcw / Ntcc))

    return DeltaPe

# endregion

#####################################################################################################################


