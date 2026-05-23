#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          21-Oct-2025     Sung Young Kim            Copy from STHE folder

##################################################################################################################
#endregion


#region Import Library
from APH.Calculations import Calculations_APH_pressure_drop, Calculations_APH_area
#endregion

#region Calculations

def APH_TAC(int_rate, n, Do, td, lf, Nc, Nr, L, Nf, tf, Ncross, par_a, par_b, rpv, rph, m_air, rho_air, mu_air, m_gas, rho_gas, mu_gas, Nop, pc, eta):
    r = ((int_rate*(1+int_rate)**n))/(((1+int_rate)**n) - 1)
    area_tot = Calculations_APH_area.APH_area_tot(Do, lf, Nc, Nr, L, Nf, tf, Ncross)
    Cap = par_a*area_tot**par_b                         # Capital cost
    DeltaP_air  = Calculations_APH_pressure_drop.APH_DeltaP_air(Nr, Do, rpv, lf, rph, L, Ncross, m_air, rho_air, mu_air)
    DeltaP_tube = Calculations_APH_pressure_drop.APH_DeltaP_tube(Do, td, Nc, Nr, m_gas, rho_gas, mu_gas, L, Ncross)

    Cop_air  = Nop*(pc/1000)*((DeltaP_air*m_air)/(eta*rho_air))    # Operating cost on a yearly fot the air side stream
    Cop_tube = Nop*(pc/1000)*((DeltaP_tube*m_gas)/(eta*rho_gas))   # Operating cost on a yearly fot the tube side stream
    TAC = r*Cap + Cop_air + Cop_tube
    return TAC

#endregion