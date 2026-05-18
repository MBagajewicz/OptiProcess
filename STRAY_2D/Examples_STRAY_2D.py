##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0        17-Feb-2025      Diego Oliva                Sieve Tray Examples Repository
#   0.1        28-Feb-2025      Alice Peccini              Relocating folders 
#   0.2        11-Mar-2025      Alice Peccini              Separation of Model_Def and Examples files
#   0.3       12-May-2025       Mariana Mello              Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS

''' 
This is a STRAY Model Examples File, Set Trimming and Sorting are applied. 

Required keys are:

ExampleX = {
    'Number_of_Equipment': N,   
    'Equipment1': {}
    'Equipment2': {}
         ...
    'EquipmentN': {}
}
    
For each 'STRAY' Type_Equipment the following data are required:

'EquipmentN': {

    'Model_Declarations': {

        'Type_Equipment': 'STRAY', 
                                
        'Discrete_Values_of_Variables': [
            [],  # Dc (m)
            [],  # dh (m)
            [],  # hdwap (m)
            [],  # hw (m)
            [],  # lt (m)
            [],  # lw (m)
            [],  # lp (m)
            [],  # tt (m)
            []   # Layout 1 = Square e 2 = Triangle          
        ]

        'Selected_OF': '' (This entry is optional, possibilities are 'Cost_OF' (default) and 'Wshell_OF')

    },
    
    'Model_Parameters': {

        'Lw' : [],      # Lw (kg/s)
        'Vw' : [],      # Vw (kg/s)
        'rol' : [],     # rol (kg/m³)
        'rov' : [],     # rov (kg/m³)
        'sig' : [],     # sigma (N/m) 
        'roshell' : ,   # roshell (kg/m³)
        'wczin' : ,     # wczin (m)
        'wczout' : ,    # wczout (m)
        'Nt' :          # Nt   

    }
}

'''
# endregion
###################################################################################################################

##################################################################################################################
# region Import Library
import copy

# endregion
################################################### SIEVE TRAY ###################################################

##################################################################################################################
##################################################################################################################
# region INPUT EXAMPLE 1 - SIEVE TRAYS - EXAMPLE FROM SOUZA ET AL, 2022

Example1 = {

    # ========================================== General Information ==========================================

    'Number_of_Equipment': 3,   

    'Equipment1': {

        'Model_Declarations': {

            'Type_Equipment': 'STRAY',
                                  
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

            'Selected_OF': ['Wshell_OF','dPtotal_OF'],

            'Sorting_by_Variable' : 'Dc'

        },

        'Model_Parameters': {

            'Lw' : [0.821, 0.802, 0.782, 0.757, 0.722, 0.661, 0.507],  # Lw (kg/s)
            'Vw' : [1.497, 1.479, 1.459, 1.434, 1.399, 1.338, 1.184],  # Vw (kg/s)
            'rol' : [753.759, 754.643, 755.643, 756.920, 758.837, 762.572, 776.265],  # rol (kg/m3)
            'rov' : [2.103, 2.085, 2.066, 2.041, 2.007, 1.945, 1.777],  # rov (kg/m3)
            'sig' : [0.02228, 0.02320, 0.02421, 0.02545, 0.02721, 0.03028, 0.03860],  # sigma (N/m) 
            'roshell' : 7900,  # roshell (kg/m3)
            'wczin' : 0.05,   # wczin (m)
            'wczout' : 0.05,    # wczout (m)
            'Nt' : 7, # Nt      
        }
    },

    'Equipment2': {

        'Model_Declarations': {

            'Type_Equipment': 'STRAY',
                                  
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

            'Selected_OF': ['Wshell_OF','dPtotal_OF'],

            'Sorting_by_Variable' : 'Dc'

        },

        'Model_Parameters': {

            'Lw' : [3.122, 2.784],  # Lw (kg/s)
            'Vw' : [1.019, 0.680],  # Vw (kg/s)
            'rol' : [873.008, 900.725],  # rol (kg/m3)
            'rov' : [1.610, 1.022],  # rov (kg/m3)
            'sig' : [0.05914, 0.06079],  # sigma (N/m) 
            'roshell' : 7900,  # roshell (kg/m3)
            'wczin' : 0.05,   # wczin (m)
            'wczout' : 0.05,    # wczout (m)
            'Nt' : 2, # Nt    
        }
    },

    'Equipment3': {

        'Model_Declarations': {

            'Type_Equipment': 'STRAY_2D',
                                  
            'Discrete_Values_of_Variables': [
                [0.6096, 0.762, 0.9144, 1.0668, 1.27, 1.4732, 1.6764, 1.9304, 2.1844, 2.4384, 2.7432, 3.048, 3.3528, 3.7084, 4.064, 4.4196, 4.826],  # D_rect (m)
                [0.6096, 0.762, 0.9144, 1.0668, 1.27, 1.4732, 1.6764, 1.9304, 2.1844, 2.4384, 2.7432, 3.048, 3.3528, 3.7084, 4.064, 4.4196, 4.826]   # D_strip (m)      
            ]

        },

        'Model_Parameters': {

            'Nt_strip': 7,
            'Nt_rect': 2,
            'roshell' : 7900

        }
    }

}


# endregion
###################################################################################################################
###################################################################################################################














