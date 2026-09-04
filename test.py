from Common.Utils.Solution_Display import display_solution


# ============================================================
# SOLUTION
# ============================================================

Solution = {

    'Equipment1': {

        'TAC_OF': 4230.4914,
        'Ds': 0.7874,
        'Tube': 30.0,
        'Npt': 6.0,
        'rp': 1.5,
        'L': 2.439,
    },

    'Equipment2': {

        'Ds': 0.5000,
        'Npt': 4.0,
        'L': 2.000,
    }
}


# ============================================================
# ACTIVE EXAMPLE
# ============================================================

Active_Example = {

    'Number_of_Equipment': 2,

    'Equipment1': {

        'Model_Declarations': {
            'Type_Equipment': 'STHE_1'
        }
    },

    'Equipment2': {

        'Model_Declarations': {
            'Type_Equipment': 'MODEL_2'
        }
    }
}


# ============================================================
# MODEL DEFINITIONS
# ============================================================

Active_Models = {

    'STHE_1': {

        'Model_Info': {

            'Solution_Display': {
                'Tube': 'display_tube'
            }
        }
    },

    'MODEL_2': {

        'Model_Info': {

            'Solution_Display': {}
        }
    }
}


# ============================================================
# TEST
# ============================================================

display_solution(
    Solution,
    Active_Example,
    Active_Models
)