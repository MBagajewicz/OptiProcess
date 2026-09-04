# ##################################################################################################################
# region Titles and Header
# Nature: Common HEX Calculations
# Methodology: Tube standard selection and minimum wall thickness calculation
# ##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         03-Sep-2026     Diego Oliva               TEMA tube discrete-set generation
# ##################################################################################################################
# endregion
# ##################################################################################################################

# ##################################################################################################################
# region Import Library
from Common.Standards.Tubes.Tube import Common_Tube
# endregion
# ##################################################################################################################


# ##################################################################################################################
# region Tube Calculations
# ==================================================================================================================


def Calculated_from_TEMA(m_p, parameters):
    """Generate the tube discrete set from a TEMA tube standard."""

    # --------------------------------------------------------------------------------------------------------------
    # Generator parameters
    # --------------------------------------------------------------------------------------------------------------
    tube_source = parameters['Tube_Source']
    tube_standard = parameters['Tube_Standard']
    tube_outside_diameter = parameters.get('Tube_Outside_Diameter', [])

    # --------------------------------------------------------------------------------------------------------------
    # Design pressure and allowable stress
    # --------------------------------------------------------------------------------------------------------------
    design_pressure = max(
        m_p['hot_pressure'],
        m_p['cold_pressure']
    )

    allowable_stress = m_p['Stube']

    if design_pressure <= 0.0:
        raise ValueError(
            "Design pressure must be greater than zero."
        )

    if allowable_stress <= 0.0:
        raise ValueError(
            "Tube allowable stress 'Stube' must be greater than zero."
        )

    # --------------------------------------------------------------------------------------------------------------
    # Get the selected TEMA standard
    # --------------------------------------------------------------------------------------------------------------
    standard = Common_Tube.get_tube_standard(
        tube_source=tube_source,
        tube_standard=tube_standard
    )

    # --------------------------------------------------------------------------------------------------------------
    # If no OD is specified, use all ODs available in the standard.
    # --------------------------------------------------------------------------------------------------------------
    if tube_outside_diameter == []:

        tube_outside_diameter = sorted(
            {
                tube_data['Tube_Outside_Diameter']
                for tube_data in standard['Tube_Index'].values()
            }
        )

    # --------------------------------------------------------------------------------------------------------------
    # Calculate minimum wall thickness and select the first standard
    # thickness satisfying the requirement for each outside diameter.
    #
    # TEMA D-9A relation:
    #
    #     t = P * Do / (2*S + 0.4*P)
    #
    # P  -> design pressure [Pa]
    # Do -> tube outside diameter [m]
    # S  -> allowable stress [Pa]
    # t  -> required wall thickness [m]
    # --------------------------------------------------------------------------------------------------------------

    tube_candidates = []

    for tube_od in tube_outside_diameter:

        # ----------------------------------------------------------------------------------------------------------
        # Calculate required wall thickness
        # ----------------------------------------------------------------------------------------------------------

        minimum_wall_thickness = (
            design_pressure * (tube_od / 1000.0)
            / (2.0 * allowable_stress + 0.4 * design_pressure)
        )

        minimum_wall_thickness_mm = (
            minimum_wall_thickness * 1000.0
        )

        # ----------------------------------------------------------------------------------------------------------
        # Select the first standard tube whose wall thickness
        # satisfies the calculated minimum thickness.
        #
        # The function returns Tube_Index values.
        # ----------------------------------------------------------------------------------------------------------

        selected_tubes = Common_Tube.select_standard_tubes(
            tube_source=tube_source,
            tube_standard=tube_standard,
            tube_outside_diameter=[tube_od],
            minimum_wall_thickness=minimum_wall_thickness_mm
        )

        tube_candidates.extend(selected_tubes)

    return tube_candidates


# endregion
# ==================================================================================================================
# ##################################################################################################################