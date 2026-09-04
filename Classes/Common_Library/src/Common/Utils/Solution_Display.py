from Common.Standards.Tubes.Tube import Common_Tube

def get_solution_variable(
    solution,
    equipment,
    variable
):
    """
    Get a variable from an equipment solution.

    Parameters
    ----------
    solution : dict
        Solution returned by the solver.

    equipment : str
        Equipment key, for example 'Equipment1'.

    variable : str
        Variable name to extract.

    Returns
    -------
    Any
        Value associated with the requested variable.
    """

    return solution[equipment][variable]



def display_tube(tube_index):
    """
    Display the technical information associated with a Tube_Index.

    Parameters
    ----------
    tube_index : int or float
        Numeric Tube_Index used by the optimization model.

    Returns
    -------
    str
        Human-readable tube information.
    """

    dte, bwg, thk = Common_Tube.get_tube_values(tube_index)

    return (
        f"Index = {int(tube_index)}, "
        f"OD = {dte * 1000.0:.3f} mm, "
        f"BWG = {int(bwg)}, "
        f"Thickness = {thk * 1000.0:.3f} mm"
    )


def display_solution(
    solution,
    active_example,
    models_def
):
    """
    Display all equipment solutions.

    The equipment type and its display definition are obtained from
    active_example and models_def. No equipment name or model-specific
    variable is hardcoded here.
    """

    for equipment, equipment_solution in solution.items():

        if not isinstance(equipment_solution, dict):
            continue

        equipment_number = equipment.replace('Equipment', '')

        equipment_data = active_example[
            f'Equipment{equipment_number}'
        ]

        type_equipment = equipment_data[
            'Model_Declarations'
        ]['Type_Equipment']

        display_definition = (
            models_def[type_equipment]
            ['Model_Info']
            .get('Solution_Display', {})
        )

        print(
            f'\nSolution of {equipment} "{type_equipment}":'
        )

        for variable, value in equipment_solution.items():

            display_name = display_definition.get(variable)

            if display_name is None:
                print(f"{variable} = {value}")
                continue

            display_function = globals().get(display_name)

            if display_function is None:
                raise ValueError(
                    f"Display function '{display_name}' "
                    f"not found for variable '{variable}'."
                )

            print(
                f"{variable} = {display_function(value)}"
            )