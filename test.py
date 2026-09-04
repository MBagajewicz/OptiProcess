from Common.Utils.Solution_Display import (
    get_solution_variable,
    display_tube
)


solution = {
    'Equipment1': {
        'Ds': 0.7874,
        'Tube': 30.0,
        'Npt': 6.0
    }
}


tube_index = get_solution_variable(
    solution,
    'Equipment1',
    'Tube'
)

tube_information = display_tube(tube_index)

print("Tube:")
print(tube_information)