import numpy as np

##### SET 1 #################
m_gas = 47.04            # Flow rate (kg*s**-1)
Cp_gas = 1300            # Heat capacity (J*(kg*K)**-1)

m_air = 91.27           # Flow rate (kg*s**-1)
Cp_air = 1005            # Heat capacity (J*(kg*K)**-1)

Tair_in = 305          # Inlet temperature of the cold stream (K)
Tair_out = 438.893          # Outlet temperature of the cold stream (K)
Tgas_in = 657.35       # Inlet temperature of the hot stream (K)
Tgas_out = 456.511     # Outlet temperature of the hot stream (K)

Q = m_gas*Cp_gas*(Tgas_in-Tgas_out)
C_air = Cp_air * m_air
C_gas = Cp_gas * m_gas
C_min = min(C_air, C_gas)
C_max = max(C_air, C_gas)
Cr = C_min/C_max

Qmax = C_min * (Tgas_in - Tair_in)

eff = Q/Qmax
print("SET 1 =======================")
print("Cr            = ", Cr)
print("effectiveness = ", eff)

if Cr > 0.3 and eff > 0.52:
    NTU_a = (1+0.44*(1-Cr))/(1-eff+0.44*(1-Cr))
    NTU_b = (np.power(NTU_a,2.5)-0.92)
    NTU = (1/(np.pi*np.power(Cr,0.15)))*np.power(NTU_b,1/1.25)
else:
    NTU = -np.log(1+np.power(Cr,1.15)*np.log(1-eff))/np.power(Cr,1.15)

    
print("NTU           = ", NTU)

delta1 = Tgas_in  - Tair_out
delta2 = Tgas_out - Tair_in
LMTD = (delta1 - delta2) / np.log(delta1 / delta2)
print("LMTD          = ", LMTD)
print("                      ")

R = (Tgas_in - Tgas_out)/(Tair_out - Tair_in)
P = (Tair_out - Tair_in)/(Tgas_in - Tair_in)
F = (eff/NTU)*(Tgas_in-Tair_in)/LMTD
print("-----------------------------")
print("R             = ", R)
print("P             = ", P)
print("F             = ", F)
print("=============================")

