#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          24-Mar-2025     Sung Young Kim            Original

##################################################################################################################
#endregion

#region Import Library
import numpy as np
#endregion


#region Calculations

def HEATER_excess_mol(excess_air):
    # mol of excess air
    excess_mol = 2 * excess_air/100
    return excess_mol

def HEATER_h_product(h_methane):
    # enthalpy of product in methane combustion reaction (Btu/mol)
    h_product = h_methane
    return h_product

def HEATER_mw_product(excess_air):
    # molecular weight of product (lb/mol)
    excess_mol = HEATER_excess_mol(excess_air)
    mw_product =(1*44.01 + 2*18.01528 + excess_mol*31.9988 + 9.3209*28.0134)/(3 + excess_mol + (2+excess_mol)*(0.78094/0.20946))
    return mw_product

def HEATER_h_gas(excess_air, h_methane):
    # enthalpy of gas with excess air (btu/lb) 
    mw_product = HEATER_mw_product(excess_air)
    h_product = HEATER_h_product(h_methane)
    h_gas = (1/mw_product) * h_product
    return h_gas
 