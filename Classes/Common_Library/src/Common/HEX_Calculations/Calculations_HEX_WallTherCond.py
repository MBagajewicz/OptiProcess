##################################################################################################################
#region Titles and Header
# Nature: Tube wall thermal conductivity
# Methodology: Definition of tube wall thermal conductivity for HEX calculations
##################################################################################################################
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.1          31-Aug-2026     Diego Oliva                ktube selector
#################################################################################################################
#endregion


#region Calculations

def tube_wall_thermal_conductivity(m_p, save_result):
    """
    Define the tube wall thermal conductivity, ktube, in W/(m*K).

    The 'ktube' parameter can be defined by the user as a numerical
    thermal conductivity value or as a predefined tube wall material.

    Predefined materials:
        - Copper            : 385 W/(m*K)
        - CarbonSteel       : 50 W/(m*K)
        - StainlessSteel304 : 15 W/(m*K)

    If 'ktube' does not exist in m_p, CarbonSteel is adopted as the
    default material and a warning message is stored using save_result.

    If 'ktube' is defined using a predefined material name, the material
    name is replaced in m_p by its corresponding thermal conductivity.

    If 'ktube' is already defined as a numerical value, it is kept
    unchanged.

    If an unknown material name is provided, CarbonSteel is adopted and
    a warning message is stored using save_result.

    Parameters
    ----------
    m_p : dict
        Model parameters containing the 'ktube' definition.

    save_result : function
        Function used to store calculation messages and warnings.

    Returns
    -------
    dict
        Updated model parameters containing numerical 'ktube'.
    """

    # ------------------------------------------------------------------
    # Default tube wall thermal conductivity
    # CarbonSteel
    # Units: W/(m*K)
    # ------------------------------------------------------------------
    default_ktube = 50

    # ------------------------------------------------------------------
    # Check whether ktube has been defined in the Model_Parameters
    # ------------------------------------------------------------------
    if 'ktube' not in m_p:

        m_p['ktube'] = default_ktube

        save_result(
            "Tube wall thermal conductivity 'ktube' does not exist "
            "in the Model_Parameters. Default CarbonSteel value "
            "(50 W/(m*K)) is adopted.\n"
        )

    # ------------------------------------------------------------------
    # Predefined tube wall materials
    # ------------------------------------------------------------------
    elif m_p['ktube'] == 'CarbonSteel':

        m_p['ktube'] = 50

    elif m_p['ktube'] == 'Copper':

        m_p['ktube'] = 385

    elif m_p['ktube'] == 'StainlessSteel304':

        m_p['ktube'] = 15

    # ------------------------------------------------------------------
    # Unknown tube wall material
    #
    # Numerical values are intentionally left unchanged.
    # ------------------------------------------------------------------
    elif not isinstance(m_p['ktube'], (int, float)):

        save_result(
            f"Unknown tube wall material '{m_p['ktube']}'. "
            "Default CarbonSteel value (50 W/(m*K)) is adopted.\n"
        )

        m_p['ktube'] = default_ktube

    return m_p

#endregion