###################################################################################################################
#region Titles and Header
# Nature: Sieve Tray Geometry Model
# Methodology: Set trimming 
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          05-Fev-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Sieve Tray Geometry related functions
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def), input parameters and variables are defined in the "Examples_Repository.py" dictionary
#                          named Model_Declarations['Discretized_Values_of_Variables'] or in the one
#                          named Model_Parameters
#endregion
##################################################################################################################

##################################################################################################################
#region Import Library
import numpy as np
from math import pi
#endregion
##################################################################################################################

##################################################################################################################
#region Sieve_Tray_Aline=



# Weir angle (teta), function do weir length (lw) and column diameter (Dc):
def f_teta(lw, Dc):
    teta = 2*np.arcsin(lw/Dc)
    return teta

# Area of the sector (Asector) defined by the weir angle (teta = f(lw,Dc)), and column diameter (Dc):
def f_Asector(lw, Dc):
    teta = f_teta(lw, Dc)
    Asector = ((Dc**2)*teta)/8
    return Asector

# Isosceles triangle area (Atriangle) defined by the weir length (lw) and column diameter (Dc):
def f_Atriangle(lw, Dc):
    Atriangle = (lw/2)*((Dc/2)**2 - (lw/2)**2)**(1/2)
    return Atriangle

# Total column area (Ac) as a function of column diameter (Dc):
def f_Ac(Dc):
    Ac = (pi*Dc**2)/4
    return Ac

# Downcomer area (Adc) as a function of the the isosceles triangle area (Atriangle = f(lw,Dc)) and the area of the sector (Asector = f(lw,Dc))
def f_Adc(lw, Dc):
    Asector = f_Asector(lw, Dc)
    Atriangle = f_Atriangle(lw, Dc)
    Adc = Asector - Atriangle
    return Adc

# Vapor flow area (An) defined by the total column area (Ac = f(lw,Dc)) and the downcomer area (Adc = f(lw,Dc)): 
def f_An(lw, Dc):
    Ac = f_Ac(Dc)
    Adc = f_Adc(lw, Dc)
    An = Ac - Adc
    return An

# Calming zone angle (beta) defined by the weir angle (teta = f(lw,Dc))
def f_beta(lw, Dc):
    teta = f_teta(lw, Dc)
    beta = (pi - teta)/2
    return beta

# Calming zone length defined by weir length (lw), calming zone angle (beta = f(lw,Dc)) and calming zone  width (wcz):
def f_lcz(lw, Dc, wcz):
    beta = f_beta(lw, Dc)
    lcz = lw - 2*(wcz/np.tan(beta))
    return lcz

# Calming zone area (Az) defined by wier length (lw), inlet and outlet calming zone lengths (lczin = f(lw, Dc, wczin) and lczout) = f(lw, Dc, wczout)) and widths (wczin and wczout):
def f_Acz(lw, Dc, wczin, wczout):
    lczin = f_lcz(lw, Dc, wczin)
    lczout = f_lcz(lw, Dc, wczout)
    Acz = ((lczin + lw)/2)*wczin + ((lczout + lw)/2)*wczout
    return Acz

# Active area angle (alfa) defined by weir angle (teta = f(lw,Dc)):
def f_alfa(lw, Dc):
    teta = f_teta(lw, Dc)
    alfa = pi - teta
    return alfa

# Width of unperforated strip (wus), that varies according to column diameter (Dc):
def f_wus(Dc):
    if isinstance(Dc,float) or isinstance(Dc,int):
        vwus = 0.0381
        if Dc > 0.7620: vwus = 0.0508
        elif Dc > 1.6764: vwus = 0.0635
        elif Dc > 3.8100: vwus = 0.0762
        elif Dc > 5.9436: vwus = 0.0889
        elif Dc > 7.4676: vwus = 0.1143
    else:
        vwus = 0.0381*np.ones(Dc.shape)
        vwus[Dc > 0.7620] = 0.0508
        vwus[Dc > 1.6764] = 0.0635
        vwus[Dc > 3.8100] = 0.0762
        vwus[Dc > 5.9436] = 0.0889
        vwus[Dc > 7.4676] = 0.1143
    return vwus

# Unperforated strip area (Aus) defined by the active area angle (alfa=f(lw,Dc)) and the width of the inperforated strip (wus=f(Dc)):
def f_Aus(lw, Dc):
    alfa = f_alfa(lw, Dc)
    wus = f_wus(Dc)
    Aus = wus*alfa*(Dc - wus)
    return Aus

# Active area (Aa) defined by column area (Ac=f(lw, Dc)), downcomer area (Adc=f(lw, Dc)), Unperforated strip area (Aus=f(lw, Dc)) and Calming zone area (Acz=f(lw, Dc,wczin, wczout)):
def f_Aa(lw, Dc, wczin, wczout):
    Ac = f_Ac(Dc)
    Adc = f_Adc(lw, Dc)
    Aus = f_Aus(lw, Dc)
    Acz = f_Acz(lw, Dc, wczin, wczout)
    Aa = Ac - 2*Adc - Aus - Acz
    #print('Aa',Aa)
    return Aa

# k parameter, depending on type of hole layout (lay = 1 for square or lay = 0 for triangle)
def f_k(lay):
    vk = 0.785*np.ones(lay.shape)
    if isinstance(lay,float) or isinstance(lay,int):
        if lay == 2: vk = 0.905
    else: 
        vk[lay == 2] = 0.905
    #print('vk',vk)
    return vk

# Hole area (Ah) defined by active area (Aa=f(lw, Dc, wczin, wczout)), hole diameter (dh), hole pitch (lp) and k = f(lay):
def f_Ah(lw, Dc, wczin, wczout, dh, lp, lay):
    Aa = f_Aa(lw, Dc, wczin, wczout)
    k = f_k(lay)
    Ah = k*((dh/lp)**2)*Aa
    #print('Ah',Ah)
    return Ah

