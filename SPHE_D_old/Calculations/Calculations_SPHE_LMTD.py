#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          29-10-2025      Javier Francesconi        Original
##################################################################################################################
#endregion

#region Import Library
import numpy as np
#endregion

#region Calculations
def SPHE_area(L,H):
    # Spiral Plate Heat exchanger area
    A = 2*H*L
    return A

def SPHE_Hydraulic_Diameter(d_channel,H):
    Dh = 2 * d_channel * H / (d_channel + H) # the hydraulic diameter of any side  (m)
    return Dh

def SPHE_Spiral_Outer_Diameter(L,dh,dc, thk, ds):
    Ds = np.sqrt(1.28 * L * (dh + dc + 2 * thk) + ds**2)  # the spiral outer diameter (m)
    return Ds

def SPHE_Mass_Flux(m,d_channel,H):
    G = m/(d_channel  * H)  # The mass flux     kg/(s*m2)
    return G

def SPHE_velocity(m,H,d_channel,ro):
    # Channel velocity
  
    A = H * d_channel 
    v = m / (ro*A)

    return float(v)

def SPHE_Reynolds(Dh,G,mu):
    # Channel Reynolds number
    Re = Dh * G / mu    
    return Re
    
def SPHE_Critical_Reynolds(Dh,Ds):
    Ree = 20000 * ((Dh / Ds) ** 0.32)
    return Ree

def SPHE_h(Dh, Ds, Cp, G, Re, Pr):
    h = (1 + 3.54 * Dh / Ds) * 0.023 (Cp) * G * (Re ** (-0.2)) * (Pr ** (-2/3)) # 
    return h
    
