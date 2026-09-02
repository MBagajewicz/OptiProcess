# ==================================================================================================
# region Import Library
# ==================================================================================================

from Common.Standards.Tubes.Tables.TEMA import TEMA

# endregion


# ==================================================================================================
# region Common_Tube
# ==================================================================================================

class Common_Tube:

    # ==============================================================================================
    # region Get Standard
    # ==============================================================================================

    @staticmethod
    def get_tube_standard(
            tube_source,
            tube_standard
    ):

        # ------------------------------------------------------------------------------------------
        # Verify Tube Source
        # ------------------------------------------------------------------------------------------

        if tube_source != TEMA['Source']['Organization']:

            raise ValueError(
                f"Tube source '{tube_source}' "
                f"is not available."
            )

        # ------------------------------------------------------------------------------------------
        # Verify Tube Standard
        # ------------------------------------------------------------------------------------------

        if tube_standard not in TEMA['Standards']:

            raise ValueError(
                f"Tube standard '{tube_standard}' "
                f"was not found in {tube_source}."
            )

        # ------------------------------------------------------------------------------------------
        # Return Tube Standard
        # ------------------------------------------------------------------------------------------

        return TEMA['Standards'][tube_standard]

    # endregion


    # ==============================================================================================
    # region Get Tube Properties
    # ==============================================================================================

    @staticmethod
    def get_tube_properties(
            tube_source,
            tube_standard,
            tube_outside_diameter,
            tube_bwg
    ):

        # ------------------------------------------------------------------------------------------
        # Get Standard
        # ------------------------------------------------------------------------------------------

        standard = Common_Tube.get_tube_standard(
            tube_source=tube_source,
            tube_standard=tube_standard
        )

        # ------------------------------------------------------------------------------------------
        # Get Outside Diameter
        # ------------------------------------------------------------------------------------------

        outside_diameters = standard[
            'Tube_Outside_Diameter'
        ]

        if tube_outside_diameter not in outside_diameters:

            raise ValueError(
                f"Tube outside diameter "
                f"'{tube_outside_diameter}' "
                f"was not found in "
                f"{tube_source} {tube_standard}."
            )

        # ------------------------------------------------------------------------------------------
        # Get BWG
        # ------------------------------------------------------------------------------------------

        bwg_values = outside_diameters[
            tube_outside_diameter
        ]['Tube_BWG']

        if tube_bwg not in bwg_values:

            raise ValueError(
                f"Tube BWG '{tube_bwg}' "
                f"was not found for tube outside diameter "
                f"'{tube_outside_diameter}'."
            )

        # ------------------------------------------------------------------------------------------
        # Get Tube Wall Thickness
        # ------------------------------------------------------------------------------------------

        tube_wall_thickness = bwg_values[
            tube_bwg
        ]['Tube_Wall_Thickness']

        # ------------------------------------------------------------------------------------------
        # Return Tube Properties
        # ------------------------------------------------------------------------------------------

        return {

            'Tube_Outside_Diameter':
                tube_outside_diameter,

            'Tube_BWG':
                tube_bwg,

            'Tube_Wall_Thickness':
                tube_wall_thickness
        }

    # endregion

    # ==============================================================================================
    # region Get only one tube per diameter if it exists and fullfils minimum wall thickness 
    # ==============================================================================================

    @staticmethod
    def select_standard_tubes(
            tube_source,
            tube_standard,
            tube_outside_diameter=[],
            minimum_wall_thickness=0.0
    ):

        standard = Common_Tube.get_tube_standard(
            tube_source=tube_source,
            tube_standard=tube_standard
        )

        tube_candidates = []

        # If no outside diameter is specified,
        # use all outside diameters available in the standard.

        if tube_outside_diameter == []:

            tube_outside_diameter = list(
                standard['Tube_Outside_Diameter'].keys()
            )

        # Check each selected outside diameter.

        for tube_od in tube_outside_diameter:

            if tube_od not in standard['Tube_Outside_Diameter']:
                raise ValueError(
                    f"Tube outside diameter '{tube_od}' "
                    f"was not found in {tube_source} {tube_standard}."
                )

            tube_od_data = standard['Tube_Outside_Diameter'][tube_od]

            # Find all available BWG / thickness combinations
            # for the current outside diameter.

            available_tubes = []

            for tube_bwg, tube_data in tube_od_data['Tube_BWG'].items():

                tube_wall_thickness = tube_data[
                    'Tube_Wall_Thickness'
                ]

                if tube_wall_thickness >= minimum_wall_thickness:

                    available_tubes.append(
                        (
                            tube_wall_thickness,
                            tube_bwg
                        )
                    )

            # If no standard tube satisfies the minimum thickness,
            # no candidate is generated for this outside diameter.

            if not available_tubes:
                continue

            # Select the smallest standard wall thickness
            # that satisfies the minimum required thickness.

            selected_thickness, selected_bwg = min(
                available_tubes,
                key=lambda x: x[0]
            )

            # Generate the Tube_ID.

            tube_id = (
                f"{tube_standard}"
                f"_OD{tube_od}"
                f"_BWG{selected_bwg}"
                f"_t{selected_thickness}"
            )

            tube_candidates.append(tube_id)

        return tube_candidates
    # endregion

    # ==============================================================================================
    # region Get dte BWG and thk values from names in list created with selected_standard_tubes
    # ==============================================================================================
    @staticmethod
    def get_tube_values(tube):
        """
        Extract tube values directly from Tube_ID.

        Tube_ID format:
            D7M_OD19.05_BWG18_t1.245

        Returns:
            dte  -> Tube outside diameter
            bwg  -> Tube BWG
            thk  -> Tube wall thickness
        """

        try:
            tube_standard, od_part, bwg_part, thk_part = tube.split('_')

            dte = float(od_part.replace('OD', ''))
            bwg = int(bwg_part.replace('BWG', ''))
            thk = float(thk_part.replace('t', ''))

        except (ValueError, AttributeError):
            raise ValueError(
                f"Invalid Tube_ID format: '{tube}'. "
                "Expected format: "
                "'D7M_OD19.05_BWG18_t1.245'."
            )

        return dte, bwg, thk
    # endregion

# ==================================================================================================
# endregion
# ==================================================================================================