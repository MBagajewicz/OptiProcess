##################################################################################################################
# region Titles and Header
# Nature: Examples Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025       Diego Oliva                Distillation Examples Repository
#   0.1       23-Mar-2025       Alice Peccini              Instructions
#   0.2       12-May-2025       Mariana Mello              Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples for DC_ST model in this file
##################################################################################################################

##################################################################################################################
####################################### DISTILLATION COLUMN + SIEVE TRAYS ########################################
##################################################################################################################


##################################################################################################################
#region Import Library
import copy
#endregion
##################################################################################################################

##################################################################################################################
#region Example Instructions
''' 
This is a DC_ST Model Examples File, Set Trimming and Enumeration are applied for the main problem, with a next
level optimization for the sieve trays

The main structure of the dictionary is:

ExampleX = {

    'Number_of_Equipment': 1,   

    'Equipment1': {}                    ---> DC_ST

    'Next_Level_Equipments': {

        'Number_of_Equipment': 1,       ---> STRAY

        'Equipment1': {}
    
    }

}
    
For each 'DC' Type_Equipment the following data are required:

'EquipmentN': {

    'Model_Declarations': {

        'Type_Equipment': 'DC',
                                
        'Discrete_Values_of_Variables': [
            [],     # Nf
            []      # Ns       
    
        'Type_Enumeration': 'Smart' (Options are 'Exhaustive', 'Smart' or 'Segmental_Smart' ---> Default is 'Smart')

        # Segmentation parameters - to be used when Segmental Smart Enumeration is true --> Leave it empty otherwise []
        'Segmentation_Parameters' : ['', , ], 
                                # Segmentation_Parameters[0]: The name of the discrete variable needs to mach one of the variables 
                                #                             given in 'List_of_Variables'
                                # Segmentation_Parameters[1]: Increment (n° of values in each segment) 
                                #                             -> If too small --> Excessive n° of intervals
                                #                             -> If too large --> Candidates cutting may not be as effective
                                # Segmentation_Parameters[2]: Correction factor to avoid small interval at the last segment 

        ]
    },

    'Model_Parameters': {

        'Nc' : ,                    # Number of components
        'Nsmin' : ,                 # Minimum number of stages (Condenser + stages within the column + Reboiler)
        'Nfmin' : ,                 # Minimum feed tray
        'Pcol' : ,                  # Column Pressure (Pa) - constant throughout the column --> Pendência: consider some pressure drop
        'z_f' : [ , , ],            # Feed molar composition [COMPONENT1, COMPONENT2, COMPONENT3]
        'F_f' :  ,                  # Feed flow (kmol/h)
        'T_f' :  ,                  # Feed temperature (K)
        'xB_TOP' : ,                # Top benzene purity
        'xB_BOTTOM' : ,             # Bottom benzene purity       
        'Comp_name' : ['', '', ''], # Componentes names (the same as given in Aspen Plus - Case Sensitive), in the same order as componentes feed molar composition     

        'Ur' : ,                    # Reboiler
        'Uc' : ,                    # Condenser
        'Tlpst' : ,                 # Low pressure steam 
        'Tcwin' : ,                 # Cooling water inlet 
        'Tcwout' : ,                # Cooling water outlet 

        'Ccw' : ,                   # Utilities costs ($/kJ) from Turton -> page 245 5ed 
        'Clpst' : ,                 # Utilities costs ($/kJ) from Turton -> page 245 5ed 
        'hours' : ,                 # Number of operation hours in a year (considering 7% of idle capacity)
        'Pb' : ,                    # Payback period (years)
        'lt' : ,                    # Tray spacing
        'roshell' : ,               # roshell (kg/m³)

        'L_D': ,                    #L/D ratio
        'TRL_min': 10,              # Reflux Drum residence time (min)
        
        'file_name' : ['.bkp'],
        'block_name' : [''],
        'stream_names': ['FEED', 'D-TOP', 'B-BOTTOM'],
        'reflux_ratio_bounds': [,],             # Reflux ratio 
        'distillate_rate_bounds': [,]           # Distillate rate 

        'Dcmin' : ,     # For LB_Gen
        'ltmin' : ,     # For LB_Gen
        'roshell' :     # roshell (kg/m3)
    }
}

Next_Level_Equipments dictionary requires the following data:

'Next_Level_Equipments': {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            'Type_Equipment': 'STRAY',
                                
            'Discretized_Values_of_Variables': [
                [],  # Dc (m)
                [],  # dh (m)
                [],  # hdwap (m)
                [],  # hw (m)
                [],  # lt (m)
                [],  # lw (m)
                [],  # lp (m)
                [],  # tt (m)
                []  # Layout 1 = Square e 2 = Triangle          
            ],

        },
        'Model_Parameters': {

            'roshell' : ,   # roshell (kg/m3)
            'wczin' : ,     # wczin (m)
            'wczout' :      # wczout (m)

        }
    }
}

'''
# endregion
##################################################################################################################

###################################################################################################################
# region INPUT EXAMPLE 1 - BTX DISTILLATION COLUMN

Example1 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'DC_ST',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [
    
                            list(range(3, 41)), # Nf (Feed considered from stage 3 to 40, considering there are always a stripping 
                                                # and a rectifying section)
                                                # Nf is interpreted regarding stages and not trays (same as in Aspen Plus)
                            list(range(5, 43))  # Ns (Stages and not trays, as in Aspen Plus)
                                                # Ns = 5 means: condenser + 3 stages within the column + reboiler
                                                # Ns = 42 means: condenser + 40 stages within the column + reboiler                  
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
            'z_f' : [0.14, 0.39, 0.47], # Feed molar composition [Benzene, Toluene, m-Xylene]
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
            'Pb' : 3,                                   # Payback period (years)

            # --------------------------- 
            # Reflux Drum Data
            # ---------------------------
            'L_D': 4,                                   # L/D ratio
            'TRL_min': 5,                              # Reflux Drum residence time (min)

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

        'Number_of_Equipment': 1,

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
        }

    }

}

# endregion
###################################################################################################################
###################################################################################################################

###################################################################################################################
# region INPUT EXAMPLE 2 - BTX DISTILLATION COLUMN WITH SMART ENUMERATION

Example2 = copy.deepcopy(Example1)
Example2['Equipment1']['Model_Declarations']['Type_Enumeration'] = 'Smart'
# endregion
###################################################################################################################


###################################################################################################################
# region INPUT EXAMPLE 3 - OPTIMAL SOLUTION FOR PRINT RESULTS

Example3 = copy.deepcopy(Example1)

Example3['Equipment1']['Model_Declarations']['Type_Enumeration'] = 'Exhaustive'
Example3['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [[13],[32]]
Example3['Next_Level_Equipments']['Equipment1']['Model_Declarations']['Discretized_Values_of_Variables'] = [[0.9144], [0.004], [0.005], [0.0635], [0.4572], [0.6604], [0.009], [0.0034], [1.0]]


# endregion
###################################################################################################################
###################################################################################################################


###################################################################################################################
# region INPUT EXAMPLE 3 - OPTIMAL SOLUTION FOR PRINT RESULTS

Example4 = copy.deepcopy(Example1)

Example4['Equipment1']['Model_Declarations']['Type_Enumeration'] = 'Exhaustive'
Example4['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [[14],[35]]
Example4['Next_Level_Equipments']['Equipment1']['Model_Declarations']['Discrete_Values_of_Variables'] = [[0.9144], [0.004], [0.005], [0.0635], [0.4572], [0.6604], [0.009], [0.0034], [1.0]]


# endregion
###################################################################################################################
###################################################################################################################












