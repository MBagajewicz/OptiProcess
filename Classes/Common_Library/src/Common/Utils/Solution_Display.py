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