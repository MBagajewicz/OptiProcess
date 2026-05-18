##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025       Diego Oliva                Distillation Examples Repository
#   0.2       12-May-2025       Mariana Mello              Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples for DC_ST_HE_RD model in this file
##################################################################################################################
# endregion
##################################################################################################################

##################################################################################################################
#region Import Library
import copy
#endregion
##################################################################################################################


###################################################################################################################
# region Examples Discription
'''
Examples used for Peccini et al (2025):

Example1_Pb_10  (BTX Column - Article Example 1 with Payback period of 10 years)
Example1_Pb_2   (BTX Column - Article Example 1 with Payback period of 2 years)
Example2_Pb_10  (BTX Column - Article Example 2 with Payback period of 10 years)
Example2_Pb_2   (BTX Column - Article Example 2 with Payback period of 2 years)
'''
#endregion
##################################################################################################################


###################################################################################################################
# region INPUT EXAMPLE 1 - BTX DISTILLATION COLUMN FOR PECCINI ET AL 2025 - PAYBACK PERIOD = 10 YEARS

Example1_Pb_10 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'DC_ST_HE_RD',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [
    
                            list(range(3, 51)), # Nf (Feed considered from stage 3 to 50, considering there are always a stripping 
                                                # and a rectifying section)
                                                # Nf is interpreted regarding stages and not trays (same as in Aspen Plus)
                            list(range(5, 53))  # Ns (Stages and not trays, as in Aspen Plus)
                                                # Ns = 5 means: condenser + 3 stages within the column + reboiler
                                                # Ns = 52 means: condenser + 50 stages within the column + reboiler                  
                                    ],

            # Enumeration type (Options are 'Exhaustive', 'Smart' or 'Segmental_Smart' ---> Default is 'Smart')
            'Type_Enumeration': 'Smart',  
            
            # Segmentation parameters - to be used when Segmental Smart Enumeration is true --> Leave it empty otherwise []
            'Segmentation_Parameters' : ['Ns', 6, 0.5], 
                                    # Segmentation_Parameters[0]: The name of the discrete variable needs to mach one of the variables 
                                    #                             given in 'List_of_Variables'
                                    # Segmentation_Parameters[1]: Increment (n° of values in each segment) 
                                    #                             -> If too small --> Excessive n° of intervals
                                    #                             -> If too large --> Candidates cutting may not be as effective
                                    # Segmentation_Parameters[2]: Correction factor to avoid small interval at the last segment


        },

         # These Problem_Parameters are used for the computation of Constraint and Objective function values
         #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {


            # --------------------------- 
            # Problem Data
            # ---------------------------
            # General Data
            'Nc' : 3,                   # Number of components
            'Nsmin' : 13,               # Minimum number of stages (Condenser + 11 stages within the column + Reboiler)
            'Nfmin' : 3,                # Minimum feed tray
            'Pcol' : 1e5,               # Column Pressure (Pa) - constant throughout the column --> Pendência: consider some pressure drop
            # Feed Data 
            'z_f' : [0.35, 0.25, 0.4],  # Feed molar composition [Benzene, Toluene, m-Xylene]
            'F_f' :  100,               # Feed flow (kmol/h)
            'T_f' :  113.4 + 273.15,    # Feed temperature (K)
            # Separation Task Specification 
            'xB_TOP' : 0.99,                    # Top benzene purity
            'xB_BOTTOM' : 0.005,                # Bottom benzene purity       
            # Components - NAMES MUST BE THE SAME AS SET IN ASPEN PLUS (if Aspen is to be used)!! CASE SENSITIVE 
            'Comp_name' : ['BENZENE', 'TOLUENE', 'M-XYLENE'],      

            # --------------------------- 
            # Thermal Utilities Data
            # ---------------------------
            # Global heat exchange coefficient (W/m²K) - Cheng - 2009 and Douglas book
            'Ur' : 1050,                # Reboiler
            'Uc' : 850,                 # Condenser
            # Utilities temperatures (K)
            'Tlpst' : 160 + 273.15,     # Low pressure steam 
            'Tcwin' : 303.15,           # Cooling water inlet 
            'Tcwout' : 323.15,          # Cooling water outlet 

            # --------------------------- 
            # Costing Data
            # ---------------------------
            'Ccw' : 0.378e-6,                           # Utilities costs ($/kJ) from Turton -> page 245 5ed 
            'Clpst' : 2.78e-6,                          # Utilities costs ($/kJ) from Turton -> page 245 5ed 
            'hours' : 8150,                             # Number of operation hours in a year (considering 7% of idle capacity)
            'Pb' : 10,                                   # Payback period (years)

            # --------------------------- 
            # Aspen Related Data
            # ---------------------------
            # File, block and streams - ATTENTION: THIS NAMES ARE CASE SENSITIVE, MUST BE THE SAME AS IN ASPEN FILE
            'file_name' : ['BTX Column.bkp'],
            'block_name' : ['COLUMN1'],
            'stream_names': ['FEED', 'D-TOP', 'B-BOTTOM'],
            # Bounds for manipulated variables within Aspen Active Specs
            'reflux_ratio_bounds': [0,100],             # Reflux ratio 
            'distillate_rate_bounds': [0,100],           # Distillate rate 

            # --------------------------- 
            # Lower Bound Generation Data
            # ---------------------------
            'Dcmin' : 0.6096,
            'ltmin' : 0.1524,
            'roshell' : 7900  # roshell (kg/m3)


        }
    },
#######################################################################

    'Next_Level_Equipments': {

        'Number_of_Equipment': 4,

        'Equipment1': {

            'Model_Declarations': {

                # Type of Equipment - Models_List
                'Type_Equipment': 'STRAY',
                                   
                # Discrete_Values_of_Variables
                # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
                'Discrete_Values_of_Variables': [
                    [0.6096, 0.762, 0.9144, 1.0668, 1.27, 1.4732, 1.6764, 1.9304, 2.1844, 2.4384, 2.7432, 3.048, 3.3528, 3.7084, 4.064, 4.4196, 4.826],  # Dc (m)
                    [0.0036, 0.004, 0.0044, 0.0048, 0.0052, 0.0056, 0.006, 0.0064],  # dh (m)
                    [0.005, 0.006, 0.007, 0.008, 0.009, 0.010],  # hdwap (m)
                    [0.0381, 0.04445, 0.0508, 0.05715, 0.0635, 0.06985, 0.0762, 0.08255, 0.0889],  # hw (m)
                    [0.1524, 0.2286, 0.3048, 0.4572, 0.6096, 0.9144],  # lt (m)
                    [0.4064, 0.6604, 0.9144, 1.1684, 1.4224, 1.6764, 1.9304, 2.1844, 2.4384, 2.6924, 2.9464, 3.2004, 3.4544, 3.7084, 3.9624],  # lw (m)
                    [0.009, 0.012, 0.015, 0.018, 0.021, 0.024],  # lp (m)
                    [0.0034],  # tt (m)
                    [1, 2]  # Layout 1 = Square e 2 = Triangle          
                ],

                'Selected_OF' : ['Cost_OF', 'dPtotal_OF']

            },

            # These Problem_Parameters are used for the computation of Constraint and Objective function values
            #                                                                      in "Constraints_and_OF.py"
            'Model_Parameters': {

                # Sieve Tray information:
                'wczin' : 0.05,                                                                             # wczin (m)
                'wczout' : 0.05,                                                                            # wczout (m)

                # Ctotal Fobj required data:
                'roshell' : 7900,                                                                           # roshell (kg/m3)

                # Wtotal Fobj required data:
                'Cw': 1.15, 
                'rotray': 7900 

            }
        },

        'Equipment2': {

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

            },
            # These Problem_Parameters are used for the computation of Constraint and Objective function values
            #                                                                      in "Constraints_and_OF.py"
            'Model_Parameters': {

                # Hot stream - Shell side
                'Rf_s': 9e-5,       # Fouling factor (m**2*oC*W**-1)

                # Cold stream - Tube side
                'Tin_t': 30,        # Inlet temperature of the cold stream (oC)
                'Tout_t': 50,       # Outlet temperature of the cold stream (oC)
                'Rf_t': 2e-4,       # Fouling factor (m**2*oC*W**-1)
                'ro_t': 996,        # Density (kg*m**-3)
                'Cp_t': 4180,       # Heat capacity (J*(kg*K)**-1)
                'mi_t': 7.97e-4,    # Viscosity (Pa*s)
                'k_t': 0.618,       # Thermal conductivity (W*(m*K)**-1)

                # Lower and upper bounds
                'vsmax': 30,        # Upper bound on the shell-side velocity (m*s**(-1))
                'vsmin': 10,        # Lower bound on the shell-side velocity (m*s**(-1))
                'dPs_disp': 2e4,    # Available pressure drop (Pa)
                'vtmax': 3,         # Upper bound on the tube-side velocity (m*s**(-1))
                'vtmin': 1,         # Lower bound on the tube-side velocity (m*s**(-1))
                'dPt_disp': 7e4,    # Available pressure drop (Pa)
                'Aexc': 0,          # Area excess (%)
                'Retmin': 1e4,      # Lower bound on the tube-side Reynolds number
                'Resmin': 500,      # Lower bound on the shell-side Reynolds number
                'LBLD': 3,          # Lower bound on L/D
                'UBLD': 15,         # Upper bound on L/D
                'LBlbcD': 0.2,      # Lower bound on lbc/D
                'UBlbcD': 1,        # Upper bound on lbc/D

                # Heat exchanger
                'ktube': 45,        # Tube wall thermal conductivity (W*(m*K)**-1)
                'thk': 2e-3,        # Tube thickness
                'Fsc': 1.15         

            }

        },

        'Equipment3': {

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

            },
            # These Problem_Parameters are used for the computation of Constraint and Objective function values
            #                                                                      in "Constraints_and_OF.py"
            'Model_Parameters': {

                # Example 6 from Sales et al 2021
                # Hot stream - Tube side
                'Tin_t': 160,       # Inlet temperature (°C)
                'Tout_t': 160,      # Outlet temperature (°C)
                'Rf_t': 0.000088,   # Fouling factor (m**2*oC*W**-1)
                'rol_t': 922.8,     # Condensate density (kg*m**-3)
                'rov_t': 2.1,       # Steam density (kg*m**-3)
                'mil_t': 1.91e-4,   # Viscosity (Pa*s)
                'miv_t': 1.36e-5,   # Viscosity (Pa*s)
                'kl_t': 0.688,      # Thermal conductivity (W*(m*K)**-1)
                'Hvap_t': 2.1e6,    # Vaporization enthalpy (J/kg)

                # Cold stream - Shell side
                'Rf_s': 0.0004,     # Fouling factor (m**2*oC*W**-1)

                # General data
                'thk': 0.00165,     # Tube thickness (m)
                'ktube': 45,        # Thermal conductivity of material (W*(m*°C)**-1)
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

        'Equipment4' : {

            'Model_Declarations': {
                
                # Type of Equipment - Models_List
                'Type_Equipment': 'Reflux_Drum',

                # Discrete_Values_of_Variables
                # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
                'Discrete_Values_of_Variables': [

                [1.0668, 1.143, 1.2192, 1.3716, 1.524, 1.6764, 1.8288, 1.9812, 2.1336, 2.286, 2.4384, 2.7432, 3.048],  # D (m) 
                [1.2195, 1.524, 1.8288, 2.1336, 2.4384, 2.7432, 3.048, 3.3528, 3.6576, 3.9624, 4.2672, 4.572, 4.8768, 5.1816, 5.4864, 5.7912, 6.0976]  # L (m)

                ],
            },
            # These Problem_Parameters are used for the computation of Constraint and Objective function values
            #                                                                      in "Constraints_and_OF.py"
            'Model_Parameters': {

                'TRL_min': 5,      # Minimum liquid residence time (min)
                'roshell' : 7900,   # roshell (kg/m3)
                'LD_LB' : 1,
                'LD_UB' : 3

            }
        },
        
    }

}


# endregion
###################################################################################################################
###################################################################################################################

###################################################################################################################
# region INPUT EXAMPLE 1 - BTX DISTILLATION COLUMN FOR PECCINI ET AL 2025 - PAYBACK PERIOD = 2 YEARS

Example1_Pb_2 = copy.deepcopy(Example1_Pb_10)
Example1_Pb_2['Equipment1']['Model_Parameters']['Pb'] = 2

# endregion
###################################################################################################################
###################################################################################################################

###################################################################################################################
# region INPUT EXAMPLE 2 - BTX DISTILLATION COLUMN FOR PECCINI ET AL 2025 - PAYBACK PERIOD = 10 YEARS

Example2_Pb_10 = copy.deepcopy(Example1_Pb_10)
Example2_Pb_10['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [list(range(3, 41)),list(range(5, 43))]
Example2_Pb_10['Equipment1']['Model_Parameters']['z_f'] = [0.10, 0.25, 0.65]
Example2_Pb_10['Equipment1']['Model_Parameters']['F_f'] = 50

# endregion
###################################################################################################################
###################################################################################################################

###################################################################################################################
# region INPUT EXAMPLE 2 - BTX DISTILLATION COLUMN FOR PECCINI ET AL 2025 - PAYBACK PERIOD = 2 YEARS

Example2_Pb_2 = copy.deepcopy(Example2_Pb_10)
Example2_Pb_2['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [list(range(3, 41)),list(range(5, 43))]
Example2_Pb_2['Equipment1']['Model_Parameters']['Pb'] = 2


# endregion
###################################################################################################################
###################################################################################################################







###################################################################################################################
# region INPUT EXAMPLE 1 WITH FIXED SOLUTION TO PRINT RESULTS (uncomment prints on TAC_OF in file Model>Constraints_and_OF)

Example1_Pb_10_Fix = copy.deepcopy(Example1_Pb_10)

Example1_Pb_10_Fix['Equipment1']['Model_Declarations']['Type_Enumeration'] = 'Exhaustive'
Example1_Pb_10_Fix['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [[16],[34]]
# Example1_Pb_10_Fix['Next_Level_Equipments']['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [[0.9144], [0.004], [0.01], [0.0381], [0.9144], [0.6604], [0.009], [0.0034], [1.0]]
# Example1_Pb_10_Fix['Next_Level_Equipments']['Equipment2']['Model_Declarations']['Discrete_Values_of_Variables'] = [[0.43815], [0.038], [4.0], [1.5], [2.0], [1.8293], [4]]
# Example1_Pb_10_Fix['Next_Level_Equipments']['Equipment3']['Model_Declarations']['Discrete_Values_of_Variables'] = [[0.203], [0.0508], [2.0], [1.33], [1.0], [1.2195]]
# Example1_Pb_10_Fix['Next_Level_Equipments']['Equipment4']['Model_Declarations']['Discrete_Values_of_Variables'] = [[1.2192], [1.524]]

Example1_Pb_2_Fix = copy.deepcopy(Example1_Pb_2)

Example1_Pb_2_Fix['Equipment1']['Model_Declarations']['Type_Enumeration'] = 'Exhaustive'
Example1_Pb_2_Fix['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [[13],[27]]
# Example1_Pb_2_Fix['Next_Level_Equipments']['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [[0.9144], [0.0036], [0.01], [0.0381], [0.9144], [0.6604], [0.009], [0.0034], [2.0]]
# Example1_Pb_2_Fix['Next_Level_Equipments']['Equipment2']['Model_Declarations']['Discrete_Values_of_Variables'] = [[0.43815], [0.038], [4.0], [1.5], [2.0], [1.8293], [4]]
# Example1_Pb_2_Fix['Next_Level_Equipments']['Equipment3']['Model_Declarations']['Discrete_Values_of_Variables'] = [[0.203], [0.0508], [2.0], [1.33], [1.0], [1.2195]]
# Example1_Pb_2_Fix['Next_Level_Equipments']['Equipment4']['Model_Declarations']['Discrete_Values_of_Variables'] = [[1.2192], [1.524]]

# endregion
###################################################################################################################
###################################################################################################################


###################################################################################################################
# region INPUT EXAMPLE 2 WITH FIXED SOLUTION FOR PRINT RESULTS (uncomment prints on TAC_OF in file Model>Constraints_and_OF)

Example2_Pb_10_Fix = copy.deepcopy(Example2_Pb_10)
Example2_Pb_10_Fix['Equipment1']['Model_Declarations']['Type_Enumeration'] = 'Exhaustive'
Example2_Pb_10_Fix['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [[9],[28]]

Example2_Pb_2_Fix = copy.deepcopy(Example2_Pb_2)
Example2_Pb_2_Fix['Equipment1']['Model_Declarations']['Type_Enumeration'] = 'Exhaustive'
Example2_Pb_2_Fix['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [[9],[20]]
# endregion
###################################################################################################################
###################################################################################################################



# Example6_Fix = copy.deepcopy(Example6)
# Example6_Fix['Equipment1']['Model_Declarations']['Type_Enumeration'] = 'Exhaustive'
# Example6_Fix['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [[9],[20]]
# Example6_Fix['Next_Level_Equipments']['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [[0.762], [0.004], [0.005], [0.0381], [0.4572], [0.6604], [0.009], [0.0034], [1.0]]
# Example6_Fix['Next_Level_Equipments']['Equipment2']['Model_Declarations']['Discrete_Values_of_Variables'] = [[0.43815], [0.07], [6.0], [1.5], [1.0], [1.8293], [11]]
# Example6_Fix['Next_Level_Equipments']['Equipment3']['Model_Declarations']['Discrete_Values_of_Variables'] = [[0.203], [0.0508], [2.0], [1.5], [1.0], [1.2195]]
# Example6_Fix['Next_Level_Equipments']['Equipment4']['Model_Declarations']['Discrete_Values_of_Variables'] = [[1.0668], [1.2195]]
