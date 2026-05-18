# ##################################################################################################################
# region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
###################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          02-Jul-2025     Augusto Vieira            Original
###################################################################################################################
#endregion


# region Import Library
import numpy as np
from STHE.Calculations import Calculations_STHE_Layers_temperature
from STHE.Calculations import Calculations_STHE_Reynolds_tubeside
from STHE.Calculations import Calculations_STHE_velocity_tubeside
#endregion


###################################################################################################################
# Polley Fouling Model Region


def Polley_dRft_dt (t, Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
                    Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk):

    Rgas = 8.314  # [J/mol·K] universal gas constant

    # Model exponents
    nt_power = 0.8
    mt_power = 0.8
    rt_power = 0.33

    # Fouling parameters
    Eat = m_p['Eat']     # Activation energy [J/mol]
    alpha = m_p['alpha'] # Deposition constant
    gamma = m_p['gamma'] # Removal constant

    # Interface temperature between fluid and fouling layer [°C]

    Tf = Calculations_STHE_Layers_temperature.STHE_Tft_in(Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
        Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk)   

    # Tube-side Reynolds number [-]

    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside( mt, rot, mit, thk, Ds, dte, Npt, rp, lay, m_p, ft_thk )

    # Tube-side Prandtl number [-]

    Prt = Cpt * mit / kt                 

    # Deposition term based on flow and temperature conditions [m²·K/W·s]

    deposition = alpha * Ret**(-nt_power) * Prt**(-rt_power) * np.exp(-Eat / (Rgas * (Tf + 273.15)))

    # Removal term based on shear or fluid turbulence [m²·K/W·s]

    removal = gamma * Ret**(mt_power)

    # Net growth rate, constrained to non-negative values [m²·K/W·s]
    
    dRft_dt = np.maximum(deposition - removal, 0)
    
    return dRft_dt

###################################################################################################################
#endregion


###################################################################################################################
# Wu_Chremasci Fouling Model Region

def Wu_dRft_dt (t, Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
                    Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk):
    
    # Tube-side fouling parameters for Wu and Cremaschi
    P_amb = 1           # Pressure in atm
    ksp = 4.9e-9        # solubility product (mol/L)² 
    K1 = 4.47e-7        # equilibrium constant for CO2_aq -> HCO3- in mol/L
    K2 = 4.68e-11       # equilibrium constant for HCO3- -> CO3-- in mol/L
    C_Henry =  29.5     # Henry consntant for CO2/water equilibrium (mol/atm.L)
    psi = 0.01          # Temperature exponent in fouling model (tube side)
    y_CO2 =  314e-6     # CO2 (molar fraction)
    Rgas = 8.314        # Universal Gas Constant [J/mol·K]

    # === Retrieve Parameters ===
    kft = m_p['kft']
    roft = m_p['roft']
    calcium  = m_p['calcium'] # Ca2+ concentration mol/L 
    pH = m_p['pH']      # cooling water pH

    # === Chemical Equilibrium: Carbonate Ion Concentration ===

    Hidronium = (10 ** (-pH))  # Convert pH to [H3O+] in mol/L
    carbonate = K1 * K2 * P_amb * y_CO2 * C_Henry / (Hidronium ** 2) # CO3-- in mol/L


    # Interface temperature between wall and fouling layer [°C]

    Tw = Calculations_STHE_Layers_temperature.STHE_Tw_in(Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
        Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk)                

   
    # Tube-side Reynolds number [-]

    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(mt, rot, mit, thk, Ds, dte, Npt, rp, lay, m_p, ft_thk)


    # Tube-side velocity

    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay, m_p,ft_thk)

   
    # === Diffusivity and Schmidt Number ===
    Dab = 3.07e-15 * (Tw+273.15) / mit
    Sc = mit / (rot * Dab)

    # === Mass Transfer Coefficient (kd) ===
    kd = 0.023 * vt * Ret**(-0.17) * Sc**(-0.67)

    # === Surface Reaction Rate Constant (kr) ===
    kr = np.exp(38.74 - (20700 / (Rgas * (Tw+273.15))))

    # === Deposition Rate per Area ===
    phi_d = kd * carbonate * (1 - ksp / (carbonate * calcium)) / (1 + kd / (kr * carbonate) + carbonate / calcium)

    # === Shear-Based Removal Rate ===
    phi_r = 0.00212 * (vt**2) * phi_d / ((kft**0.5) * psi)

    # === Final Rate of Change of Fouling Resistance ===
    dRft_dt = (phi_d - phi_r) / (roft * kft)

    dRft_dt = np.maximum(dRft_dt, 0.0)
    
    
    return dRft_dt
###################################################################################################################
#endregion



###################################################################################################################
# Souza Fouling Model Region

# --------------------------------------------------------------

# Auxiliary Fucntions


def sigmoidal_func(A, B):
    # Sigmoidal shape activation function
    return 1 / (1 + np.exp(-A * B))

def Ef_roughness(m_p, ft_thk):  
    
# Computes the effect of biofilm on roughness as desribed on the ref paper

    E = m_p['roughness']
    
    return E + 0.2 * ft_thk


#   Microbial Growth Rate Function 
def mi_gr(T):
    # A,B,C parameters estimation come from experimental growth rate data fit #
    R = 8.314  # J/mol·K
    A, B, C = np.array([ 2.95522667e+03,  5.58690569e+04, -6.44229732e-01]) 
    mi_gr = A *(T)* np.exp(-B / (R * T)) * sigmoidal_func(C, T - 315.4)
    return  mi_gr

# --------------------------------------------------------------

# Main Functions

def dmf_dt_model(t, Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
                    Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk):
    
    # Mass rate change of biofilm layer computed including temperature effects on growth rate,
    # and flow velocity effects on production and detachment of biofilm layer
    
    # A,B,C,D parameters estimation come from experimental biofilm mass rate data fit 

    A, B, C, D = np.array([ 2.8057315980019872, 1.3602707306279231, 2.029789601426903, 2.448003192994685]) 
    
    # === Retrieve Parameters ===
    roft = m_p['roft']
    Cs = m_p['Cs']

    # Tube-side fouling parameters 
    lim_vel = 1.59 # limiting velocity
    mi_gr_Tref =  0.5991/(60*60)  # growth rate in s^-1
    S_ref = 0.02 # reference substrate concentration in terms of kg of glucose per cubic meter
    td =  73780 # lag time for growth rate model in s


    
    # Interface temperature between wall and fouling layer [°C]
    
    Tw = Calculations_STHE_Layers_temperature.STHE_Tw_in(Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
        Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk)                                

    # Tube-side velocity
    
    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(mt, rot, thk, Ds, dte, Npt, rp, lay, m_p,ft_thk)
    
    # biofilm growth must only start after lag time - td
    
    if t < td:
        return 0.0
    
    else : 
        
        b = 1 / (86400 * (A - B * vt)) # velocity paremeter
        
        # Reference production mass flux
        Jp_star = (-C * vt + D) * sigmoidal_func(S_ref/1000, vt - lim_vel) / 86400
    
        # Temperature and substrate concentration correction factors
        f_temp = mi_gr(Tw+273.15) / mi_gr_Tref
        f_sub = Cs / S_ref
        
        # biofilm mass per surface area (kg /m²)
        mf = ft_thk * roft 
        
        # Mass Flux of Production and Removal (kg/m².s)
        Jp = f_temp * f_sub * Jp_star  #
        Jr = b * mf
        
        return Jp - Jr

# ==============================================================
def Souza_dRft_dt(t, Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
                    Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk):

    # === Retrieve Parameters ===
    kft = m_p['kft']
    roft = m_p['roft']
    

    # Compute dm_f/dt from biofilm model
    dmf_dt = dmf_dt_model(t, Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
                        Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk)
    
    
    # Calculating flow diameter
    dti = dte - 2*thk
    df = dti - 2* ft_thk


    # Converting mass derivative into Fouling resistance derivative 
    # From Rf definition -----
    # Rf = ln(dti / df) * dti / (2 * kft)
    # dRf/dt = (dti / (kft * df)) * d(ft_thk)/dt --- assuming ft_thk << dti
    
    # From curved surface approximation -----
    # mf = rho_ft * (ft_thk - ft_thk^2 / dti)  
    # dm_f/dt = rho_ft * (1 - 2 * ft_thk / dti) * d(ft_thk)/dt
    
    # Rearranging both equations
    # dRf/dt = (dti / (kft * df)) * [1 / (rho_ft * (1 - 2 * ft_thk / dti))] * dm_f/dt
    
    dRft_dt = dmf_dt * dti / (kft * roft * (1 - 2 * ft_thk / dti) * df)
    dRft_dt = np.maximum(dRft_dt, 0)

    return dRft_dt

###################################################################################################################
#endregion



###################################################################################################################
# Fouling Model Selector Region

# Compute the rate of fouling resistance increase in tube side [m²·K/W·s]
def Fouling_dRft_dt(t, Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
                    Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk):


    if m_p['Fouling_Method'] == "Polley":
        dRft_dt = Polley_dRft_dt (t, Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
                            Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk)        

    elif m_p['Fouling_Method'] == "Wu_Chremasci":
        dRft_dt = Wu_dRft_dt (t, Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
                            Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk) 
    
    elif m_p['Fouling_Method'] == "Souza":
        dRft_dt = Souza_dRft_dt (t, Tti, mt, rot, Cpt, mit, kt, Rft, Tsi, ms, ros, Cps, mis, ks,
                            Rfs, thk, ktube, yfluid, Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p, ft_thk) 

    elif m_p['Fouling_Method'] == "constant":
        dRft_dt = 0  # No change in Rft over time for constant fouling
    
    return dRft_dt

###################################################################################################################
#endregion





