##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025        Diego Oliva               Kettle Examples Repository
#   0.2       12-May-2025       Mariana Mello              Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of Kettle in this file
##################################################################################################################

###################################################################################################################
# region Import Library
import copy
# endregion
###################################################################################################################

######################################## Kettle Reboiler - Sales et al 2021 #######################################

###################################################################################################################
# region Examples Description
'''
Example1:  Horizontal Shell and Tube from Sales et al, 2021
Example2:  Example1 with Costa as an Objective Function instead of Area
'''
# endregion
###################################################################################################################

###################################################################################################################
# region INPUT EXAMPLE 1 - KETTLE REBOILER

Example1 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'Kettle_2',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [

                [0.203, 0.254, 0.305, 0.337, 0.387, 0.438, 0.489, 0.540, 0.591, 0.635, 0.686, 0.737, 0.787, 0.838, 
                 0.889, 0.940, 0.991, 1.067, 1.143, 1.219, 1.295, 1.372, 1.448, 1.524],  # Ds (m)

                [0.01905, 0.0254, 0.03175, 0.03810, 0.05080],    # dte (m)

                [2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0960]  # L (m)

            ],

            'Selected_OF': ['Cost_OF','Area_OF'],
            
        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Example 6 from Sales et al 2021
            # Hot stream - Tube side
            'Tin_t': 143,       # Inlet temperature (°C)
            'Tout_t': 143,      # Outlet temperature (°C)
            'Rf_t': 0.000088,   # Fouling factor (m².°C/W)
            'rol_t': 922.8,     # Condensate density (kg/m³)
            'rov_t': 2.1,       # Steam density (kg/m³)
            'mil_t': 1.91e-4,   # Viscosity (Pa.s)
            'miv_t': 1.36e-5,   # Viscosity (Pa.s)
            'kl_t': 0.688,      # Thermal conductivity (W/(m.K))
            'Hvap_t': 2.1e6,    # Vaporization enthalpy (J/kg)

            # Cold stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 112,       # Inlet temperature (°C)
            'Tout_s': 112,      # Outlet temperature (°C)
            'Rf_s': 0.0004,     # Fouling factor (m².°C/W)
            'Pc': 3800000,      # Critical pressure (Pa)
            'P_s': 1925000,     # Pressure (Pa)
            'Hvap_s': 233000,   # Vaporization enthalpy (J/kg)

            # General data
            'thk': 0.00165,     # Tube thickness (m)
            'ktube': 45,        # Thermal conductivity of material (W/(m.°C))
            'Aexc': 0.1,        # Area excess (%)
            'g': 9.81,          # Gravity accelertion (m/s²)
            'BR': 0,            # Boiling range
            'hnc': 250,         # Contribution of the natural convection (W/(m²°C))

            # Bounds
            'dPt_disp': 10e5,   # Available pressure drop (Pa) 
            'Retmin': 3380,     # Minimum reynolds number for condensing stream
            'vtmax': 25,        # Maximum velocity (m/s) 
            'vtmin': 0,         # Minimum velocity (m/s) 
            'LBLD': 3,          # Tube length/shell diameter ratio LB
            'UBLD': 15          # Tube length/shell diameter ratio UB
        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

##################################################################################################################
# region INPUT EXAMPLE 2 - HSTC

Example2 = copy.deepcopy(Example1)
Example2['Equipment1']['Model_Declarations']['Selected_OF'] = ['Area_OF','Cost_OF']

# endregion
###################################################################################################################
###################################################################################################################

Example2_DC_validation = copy.deepcopy(Example1)
Example2_DC_validation['Equipment1']['Model_Parameters'] = {'Tin_t': 160, 'Tout_t': 160, 'Rf_t': 8.8e-05, 'rol_t': 922.8, 'rov_t': 2.1, 'mil_t': 0.000191, 'miv_t': 1.36e-05, 'kl_t': 0.688, 'Hvap_t': 2100000.0, 'Rf_s': 0.0004, 'thk': 0.00165, 'ktube': 
45, 'Aexc': 0.1, 'g': 9.81, 'BR': 0, 'hnc': 250, 'dPt_disp': 1000000.0, 'Retmin': 3380, 'vtmax': 25, 'vtmin': 0, 'LBLD': 3, 'UBLD': 15, 'm_s': 3.2880979166666666, 'Tin_s': 396.433078, 'Tout_s': 398.999211, 'P_s': 100000.0, 'Pc': 3762875.22, 'Hvap_s': 162647.68152644817, 'Q': 534801.5027777777, 'Pr': 0.0265754228225511, 'Fp': 0.9714806085954952, 'm_t': 0.25466738227513225, 'dTLM': -237.71383604308417, 'q1_max': 378639.59049715527}