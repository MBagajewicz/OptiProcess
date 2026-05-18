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

def HEATER_Qoil(Moil, To_oil, Ti_oil, Enthoil_c1, Enthoil_c2, Enthoil_c3):
    # Q for oil
    Oil_Entho = Enthoil_c1*np.power(To_oil,2) + Enthoil_c2*To_oil + Enthoil_c3
    Oil_Enthi = Enthoil_c1*np.power(Ti_oil,2) + Enthoil_c2*Ti_oil + Enthoil_c3
    Qoil = Moil*(Oil_Entho - Oil_Enthi)
    return Qoil
