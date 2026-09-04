# ==================================================================================================
# region Import Library
# ==================================================================================================

from Common.Standards.Tubes.Tables.TEMA import TEMA
import numpy as np

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
            tube_index
    ):

        # ------------------------------------------------------------------------------------------
        # Get Standard
        # ------------------------------------------------------------------------------------------

        standard = Common_Tube.get_tube_standard(
            tube_source=tube_source,
            tube_standard=tube_standard
        )

        # ------------------------------------------------------------------------------------------
        # Get Tube Index
        # ------------------------------------------------------------------------------------------

        tube_index_data = standard['Tube_Index']

        if tube_index not in tube_index_data:

            raise ValueError(
                f"Tube index '{tube_index}' "
                f"was not found in "
                f"{tube_source} {tube_standard}."
            )

        # ------------------------------------------------------------------------------------------
        # Get Tube Data
        # ------------------------------------------------------------------------------------------

        tube_data = tube_index_data[tube_index]

        # ------------------------------------------------------------------------------------------
        # Return Tube Properties
        # ------------------------------------------------------------------------------------------

        return {

            'Tube_Outside_Diameter':
                tube_data['Tube_Outside_Diameter'],

            'Tube_BWG':
                tube_data['Tube_BWG'],

            'Tube_Wall_Thickness':
                tube_data['Tube_Wall_Thickness']
        }

    # endregion


    # ==============================================================================================
    # region Select Standard Tubes
    # ==============================================================================================

    @staticmethod
    def select_standard_tubes(
            tube_source,
            tube_standard,
            tube_outside_diameter=[],
            minimum_wall_thickness=0.0
    ):

        # ------------------------------------------------------------------------------------------
        # Get Standard
        # ------------------------------------------------------------------------------------------

        standard = Common_Tube.get_tube_standard(
            tube_source=tube_source,
            tube_standard=tube_standard
        )

        tube_index_data = standard['Tube_Index']

        tube_candidates = []

        # ------------------------------------------------------------------------------------------
        # Get Available Outside Diameters
        # ------------------------------------------------------------------------------------------

        available_outside_diameters = sorted(
            {
                tube_data['Tube_Outside_Diameter']
                for tube_data in tube_index_data.values()
            }
        )

        # ------------------------------------------------------------------------------------------
        # If no outside diameter is specified,
        # use all outside diameters available in the standard.
        # ------------------------------------------------------------------------------------------

        if tube_outside_diameter == []:

            tube_outside_diameter = available_outside_diameters

        # ------------------------------------------------------------------------------------------
        # Check each selected outside diameter.
        # ------------------------------------------------------------------------------------------

        for tube_od in tube_outside_diameter:

            if tube_od not in available_outside_diameters:

                raise ValueError(
                    f"Tube outside diameter '{tube_od}' "
                    f"was not found in {tube_source} {tube_standard}."
                )

            # --------------------------------------------------------------------------------------
            # Find all standard tubes for the current outside diameter
            # that satisfy the minimum wall thickness.
            # --------------------------------------------------------------------------------------

            available_tubes = []

            for tube_index, tube_data in tube_index_data.items():

                if tube_data['Tube_Outside_Diameter'] != tube_od:
                    continue

                tube_wall_thickness = tube_data[
                    'Tube_Wall_Thickness'
                ]

                if tube_wall_thickness >= minimum_wall_thickness:

                    available_tubes.append(
                        (
                            tube_wall_thickness,
                            tube_index
                        )
                    )

            # --------------------------------------------------------------------------------------
            # If no standard tube satisfies the minimum thickness,
            # no candidate is generated for this outside diameter.
            # --------------------------------------------------------------------------------------

            if not available_tubes:
                continue

            # --------------------------------------------------------------------------------------
            # Select the smallest standard wall thickness
            # that satisfies the minimum required thickness.
            # --------------------------------------------------------------------------------------

            selected_thickness, selected_index = min(
                available_tubes,
                key=lambda x: x[0]
            )

            # --------------------------------------------------------------------------------------
            # Store Tube Index
            # --------------------------------------------------------------------------------------

            tube_candidates.append(selected_index)

        return tube_candidates

    # endregion


    # ==============================================================================================
    # region Get Tube Values
    # ==============================================================================================

    @staticmethod
    def get_tube_values(
            tube,
            tube_source='TEMA',
            tube_standard='D7M'
    ):

        """
        Get tube values from Tube_Index.

        The method accepts either:

            - a single Tube_Index
            - a numpy array of Tube_Index values

        For a single Tube_Index, scalar values are returned.

        For a numpy array, numpy arrays are returned.

        Returns:

            dte -> Tube outside diameter
            bwg -> Tube BWG
            thk -> Tube wall thickness
        """

        # ------------------------------------------------------------------------------------------
        # Get Standard
        # ------------------------------------------------------------------------------------------

        standard = Common_Tube.get_tube_standard(
            tube_source=tube_source,
            tube_standard=tube_standard
        )

        tube_index_data = standard['Tube_Index']

        # ==========================================================================================
        # Case 1: numpy array
        # ==========================================================================================

        if isinstance(tube, np.ndarray):

            if tube.size == 0:

                return (
                    np.array([], dtype=float),
                    np.array([], dtype=int),
                    np.array([], dtype=float)
                )

            # --------------------------------------------------------------------------------------
            # Convert indices to integer values.
            #
            # This also protects the function if the incoming array happens
            # to have been created as float by numpy.
            # --------------------------------------------------------------------------------------

            tube_indices = tube.astype(int)

            # --------------------------------------------------------------------------------------
            # Only evaluate unique Tube_Index values.
            # --------------------------------------------------------------------------------------

            unique_indices, inverse = np.unique(
                tube_indices,
                return_inverse=True
            )

            # --------------------------------------------------------------------------------------
            # Validate Tube_Index values
            # --------------------------------------------------------------------------------------

            invalid_indices = [
                index
                for index in unique_indices
                if index not in tube_index_data
            ]

            if invalid_indices:

                raise ValueError(
                    f"Tube indices {invalid_indices} "
                    f"were not found in {tube_source} {tube_standard}."
                )

            # --------------------------------------------------------------------------------------
            # Extract values for unique Tube_Index values.
            # --------------------------------------------------------------------------------------

            dte_unique = np.array(
                [
                    tube_index_data[index]['Tube_Outside_Diameter'] / 1000.0
                    for index in unique_indices
                ],
                dtype=float
            )

            bwg_unique = np.array(
                [
                    tube_index_data[index]['Tube_BWG']
                    for index in unique_indices
                ],
                dtype=int
            )

            thk_unique = np.array(
                [
                    tube_index_data[index]['Tube_Wall_Thickness'] / 1000.0
                    for index in unique_indices
                ],
                dtype=float
            )

            # --------------------------------------------------------------------------------------
            # Map unique values back to original array positions.
            # --------------------------------------------------------------------------------------

            return (
                dte_unique[inverse],
                bwg_unique[inverse],
                thk_unique[inverse]
            )

        # ==========================================================================================
        # Case 2: Single Tube_Index
        # ==========================================================================================

        try:

            tube_index = int(tube)

        except (ValueError, TypeError):

            raise ValueError(
                f"Invalid Tube_Index '{tube}'. "
                f"Tube_Index must be a numeric index."
            )

        # ------------------------------------------------------------------------------------------
        # Validate Tube_Index
        # ------------------------------------------------------------------------------------------

        if tube_index not in tube_index_data:

            raise ValueError(
                f"Tube index '{tube_index}' "
                f"was not found in {tube_source} {tube_standard}."
            )

        # ------------------------------------------------------------------------------------------
        # Get Tube Data
        # ------------------------------------------------------------------------------------------

        tube_data = tube_index_data[tube_index]

        dte = float(
            tube_data['Tube_Outside_Diameter'] / 1000 # dte [m]. Converted from [mm] in table TEMA to [m]. 
        )

        bwg = int(
            tube_data['Tube_BWG']
        )

        thk = float(
            tube_data['Tube_Wall_Thickness'] / 1000 # thk [m]. Converted from [mm] in table TEMA to [m].
        )

        return dte, bwg, thk

    # endregion


# ==================================================================================================
# endregion
# ==================================================================================================