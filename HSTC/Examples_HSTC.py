##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025       Alice Peccini              Horizontal Shell and Tube Condenser Examples Repository
#   0.2       12-May-2025       Mariana Mello              Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of Distillation in this file
##################################################################################################################

##################################################################################################################
# region Import Library
import copy
# endregion
##################################################################################################################

###################################### HORIZONTAL SHELL-AND-TUBE CONDENSER #######################################

##################################################################################################################
# region Examples Description
'''
Example1:  Horizontal Shell and Tube from Pereira et al, 2021
Example2:  Example1 with Cost as an Objective Function instead of Area
'''
# endregion
##################################################################################################################

##################################################################################################################
# region INPUT EXAMPLE 1 - HSTC

Example1 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'HSTC',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [0.43815, 0.48895, 0.53975, 0.59055, 0.635, 0.68580, 0.73660, 0.78740, 0.83820, 0.88900, 0.94000, 0.99100],  # Ds (m)

                [0.016, 0.018, 0.020, 0.022, 0.025, 0.030, 0.032, 0.038, 0.040, 0.070],    # dte (m)

                [1, 2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0976],  # L (m)

                list(range(1, 21))  # Nb

            ],

            # This model allows 2 options for Objective Function ('Cost_OF' or 'Area_OF'), if none is given, default is 'Cost_OF'
            'Selected_OF' : ['Cost_OF', 'Area_OF']
            
        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Hot stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 67,        # Inlet temperature of the hot stream (°C)
            'Tout_s': 67,       # Outlet temperature of the hot stream (°C)
            'Rf_s': 9e-5,       # Fouling factor (m².°C/W)
            'ro_s': 736,        # Density (kg/m³)
            'rov_s': 3.12,      # Vapor density (kg/m³)
            'mi_s': 2.13e-4,    # Viscosity (Pa.s)
            'miv_s': 1.4e-6,    # Vapor Viscosity (Pa.s)
            'k_s': 0.137,       # Thermal conductivity (W/(m.K))
            'Hvap_s': 4.94e5,   # Vaporization enthalpy (J/kg)

            # Cold stream - Tube side
            'Tin_t': 25,        # Inlet temperature of the cold stream (°C)
            'Tout_t': 35,       # Outlet temperature of the cold stream (°C)
            'Rf_t': 2e-4,       # Fouling factor (m².°C/W)
            'ro_t': 996,        # Density (kg/m³)
            'Cp_t': 4180,       # Heat capacity (J/(kg.K))
            'mi_t': 7.97e-4,    # Viscosity (Pa*s)
            'k_t': 0.618,       # Thermal conductivity (W/(m.K))

            # Lower and upper bounds
            'vsmax': 30,        # Upper bound on the shell-side velocity (m/s)
            'vsmin': 10,        # Lower bound on the shell-side velocity (m/s)
            'dPs_disp': 2e4,    # Available pressure drop (Pa)
            'vtmax': 3,         # Upper bound on the tube-side velocity (m/s)
            'vtmin': 1,         # Lower bound on the tube-side velocity (m/s)
            'dPt_disp': 7e4,    # Available pressure drop (Pa)
            'Aexc': 0,          # Area excess (%)
            'Retmin': 1e4,      # Lower bound on the tube-side Reynolds number
            'Resmin': 500,      # Lower bound on the shell-side Reynolds number
            'LBLD': 3,          # Lower bound on L/D
            'UBLD': 15,         # Upper bound on L/D
            'LBlbcD': 0.2,      # Lower bound on lbc/D
            'UBlbcD': 1,        # Upper bound on lbc/D

            # Heat exchanger
            'ktube': 45,        # Tube wall thermal conductivity (W/(m.K))
            'thk': 2e-3,        # Tube thickness (m)
            'Fsc': 1.15         

        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

##################################################################################################################
# region INPUT EXAMPLE 2 - HSTC

Example2 = copy.deepcopy(Example1)
Example2['Equipment1']['Model_Declarations']['Selected_OF'] = ['Area_OF', 'Cost_OF']

# endregion
###################################################################################################################
###################################################################################################################

Example2_DC_validation = copy.deepcopy(Example1)
Example2_DC_validation['Equipment1']['Model_Parameters'] = {'Rf_s': 9e-05, 'Tin_t': 30, 'Tout_t': 50, 'Rf_t': 0.0002, 'ro_t': 996, 'Cp_t': 4180, 'mi_t': 0.000797, 'k_t': 0.618, 'vsmax': 30, 'vsmin': 10, 'dPs_disp': 20000.0, 'vtmax': 3, 'vtmin': 1, 'dPt_disp': 70000.0, 'Aexc': 0, 'Retmin': 10000.0, 'Resmin': 500, 'LBLD': 3, 'UBLD': 15, 'LBlbcD': 0.2, 'UBlbcD': 1, 'ktube': 45, 'thk': 0.002, 'Fsc': 1.15, 'Prt': 5.390711974110032, 'm_s': 1.957750102777778, 'Tin_s': 353.396396, 'Tout_s': 353.071481, 'ro_s': 814.5692081095991, 'rov_s': 2.7428810808548056, 'mi_s': 0.0003206567, 'miv_s': 9.01403263e-06, 'k_s': 0.12431971, 'Hvap_s': 541742.5374303354, 'dTLM': 313.13092421475983, 'Q': 1060596.5083333333, 'm_t': 12.68656110446571}
