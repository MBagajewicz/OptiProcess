##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         05-Jul-2026      ChatGPT                   Add SPHE_D_N examples with N as variable
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################

import copy
from SPHE_D import Examples_SPHE_D as _SPHE_D_examples


def _convert_to_turn_based_example(base_example):
    """Return a SPHE_D example converted to the turn-based SPHE_D_N model."""
    example = copy.deepcopy(base_example)
    equipment = example['Equipment1']

    # Select the turn-based model. The variable order is now [N, H, ds, dh, dc].
    equipment['Model_Declarations']['Type_Equipment'] = 'SPHE_D_N'

    old_values = equipment['Model_Declarations']['Discrete_Values_of_Variables']
    equipment['Model_Declarations']['Discrete_Values_of_Variables'] = [
        list(range(2, 20 + 1)),  # N - number of spiral turns
        old_values[1],  # H
        old_values[2],  # ds
        old_values[3],  # dh
        old_values[4],  # dc
    ]

    return example


Example1 = _convert_to_turn_based_example(_SPHE_D_examples.Example1)
Example2 = _convert_to_turn_based_example(_SPHE_D_examples.Example2)
Example3 = _convert_to_turn_based_example(_SPHE_D_examples.Example3)
Example4 = _convert_to_turn_based_example(_SPHE_D_examples.Example4)
Example5 = _convert_to_turn_based_example(_SPHE_D_examples.Example5)
Example6 = _convert_to_turn_based_example(_SPHE_D_examples.Example6)
