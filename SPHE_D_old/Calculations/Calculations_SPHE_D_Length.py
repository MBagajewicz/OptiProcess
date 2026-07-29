#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          01-Dec-2024     Mariana Mello               Original
#   0.1          07-Jun-2025     Qiqi Zhang                  Adaptation from original STHE
##################################################################################################################
#endregion


#region Import Library
import numpy as np
#endregion

#region Calculations

def SPHE_spiral_length(N, ds, d_I, d_II, tk):
    
    def spiral_length(a, b, theta2):
        """Longitud entre theta1 y theta2."""
        def F(theta):
            u = a + b * theta
            return (
                u * np.sqrt(u**2 + b**2)
                + b**2 * np.log(u + np.sqrt(u**2 + b**2))
            )
        return (F(theta2) - F(0)) / (2 * b)

    a = ds / 2.0 + tk + d_I + tk / 2.0
    b = (d_I + d_II + 2.0 * tk) / (2.0 * np.pi)
    theta2=N * 2.0 * np.pi

    return spiral_length(a, b, theta2)



