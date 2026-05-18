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

def HEATER_cp_gas(Tflame):
    # haet capacity of gas
    Tflame_SI = (Tflame - 32)*(5/9)+273.15
    cp_gas_SI = (336 + 0.0798 * Tflame_SI + 2.81E-05 * np.power(Tflame_SI,2) - 1.7E-08*np.power(Tflame_SI,3))/329.680708
    cp_gas = cp_gas_SI * 0.23884599999736
    return cp_gas
