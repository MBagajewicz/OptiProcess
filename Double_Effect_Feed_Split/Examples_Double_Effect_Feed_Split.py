##################################################################################################################
# region Titles and Header
# Nature: Repository
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
# region INPUT EXAMPLE 1 - METHANOL-WATER DISTILLATION COLUMN --> Type : Double_Effect + DC_Q_Condenser

Example1 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'Double_Effect',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [
    
                            list(range(10, 21)), # Nf (Feed considered from stage 3 to 40, considering there are always a stripping 
                                                # and a rectifying section)
                                                # Nf is interpreted regarding stages and not trays (same as in Aspen Plus)
                            list(range(24, 25))  # Ns (Stages and not trays, as in Aspen Plus)
                                                # Ns = 5 means: condenser + 3 stages within the column + reboiler
                                                # Ns = 42 means: condenser + 40 stages within the column + reboiler                  
                                    ],

             # Enumeration type (Options are 'Exhaustive', 'Smart' or 'Segmental_Smart' ---> Default is 'Smart')
            'Type_Enumeration': 'Exhaustive', 

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
            'z_f' : [0.6, 0.4], # Feed composition [Benzene, Toluene, m-Xylene]
            'Feed' : 650,               # Feed flow in the first column (kmol/h)
            'Split' : 0.85,              # Split fraction of the molar flow in the first column
            'F_f' :  550,               # Feed flow (kmol/h)
            'T_f' :  113.4 + 273.15,    # Feed temperature (K)
            # Separation Task Specification 
            'SPEC_1' : 0.99,                    # Top product purity
            'SPEC_2' : 0.005,                   # Bottom product purity       
            # Components - NAMES MUST BE THE SAME AS SET IN ASPEN PLUS (if Aspen is to be used)!! CASE SENSITIVE 
            'Comp_name' : ['METHANOL', 'WATER'],         

            # --------------------------- 
            # Thermal Utilities Data
            # ---------------------------
            # Global heat exchange coefficient (W/m²K) - Cheng - 2009 and Douglas book
            'Ur' : 250/0.17611,         # Reboiler
            'Uc' : 250/0.17611,         # Condenser
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
            'lt' : 0.6096,                              # Tray spacing
            
            # --------------------------- 
            # Reflux Drum Data
            # ---------------------------
            'L_D': 4,                                   # L/D ratio
            'TRL_min': 10,                              # Reflux Drum residence time (min)

            # --------------------------- 
            # Aspen Related Data
            # ---------------------------
            # File, block and streams - ATTENTION: THIS NAMES ARE CASE SENSITIVE, MUST BE THE SAME AS IN ASPEN FILE
            'file_name' : ['Methanol_H2O - Q_Fixo.bkp'],
            'block_name' : ['LPC'],
            'stream_names': ['FEED-LPC', 'L-TOP', 'L-BOTTOM'],
            # Bounds for manipulated variables within Aspen Active Specs
            'reflux_ratio_bounds': [0,100],             # Reflux ratio 
            'distillate_rate_bounds': [0.01,1],           # Distillate rate 

            # --------------------------- 
            # Lower Bound Generation Data
            # ---------------------------
            'Dcmin' : 0.6096,
            'ltmin' : 0.1524,
            'roshell' : 7900,  # roshell (kg/m3)

            #Save TAC results in Excel file
            'TAC_new_file': True       # If True, creates a new .xlsx file with the TAC results of each simulation

        }
    },
#######################################################################

    'Next_Level_Equipments': {

        'Number_of_Equipment': 1,

        'Equipment1': {

            'Model_Declarations': {

                # Type of Equipment - Models_List
                'Type_Equipment': 'DC_Q_Condenser',
                                   
                # Discrete_Values_of_Variables
                # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
                'Discrete_Values_of_Variables': [
                            
                            list(range(1, 20)), # Nf (Feed considered from stage 3 to 40, considering there are always a stripping 
                                                # and a rectifying section)
                                                # Nf is interpreted regarding stages and not trays (same as in Aspen Plus)
                            list(range(15, 21))  # Ns (Stages and not trays, as in Aspen Plus)
                                                # Ns = 5 means: condenser + 3 stages within the column + reboiler
                                                # Ns = 42 means: condenser + 40 stages within the column + reboiler           
                ],

                # Enumeration type (Options are 'Exhaustive', 'Smart' or 'Segmental_Smart' ---> Default is 'Smart')
                'Type_Enumeration': 'Exhaustive',  
            
                # Segmentation parameters - to be used when Segmental Smart Enumeration is true --> Leave it empty otherwise []
                'Segmentation_Parameters' : [], 
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

            # General Data
            'Nc' : 3,                           # Number of components
            'Nsmin' : 13,                       # Minimum number of stages (Condenser + 11 stages within the column + Reboiler)
            'Nfmin' : 3,                        # Minimum feed tray
            'Pcol' : 5e5,                       # Column Pressure (Pa) - constant throughout the column --> Pendência: consider some pressure drop
            # Feed Data 
            'z_f' : [0.6, 0.4],                 # Feed molar composition [Benzene, Toluene, m-Xylene]
            #'Feed' : 650,                       # Feed flow in the first column (kmol/h)
            'Split' : 0.15,                      # Split fraction of the molar flow in the first column
            'F_f' :  100,                       # Feed flow (kmol/h)
            'T_f' :  113.4 + 273.15,            # Feed temperature (K)
            # Separation Task Specification 
            'SPEC_1' : -5548807.1,			    # Condenser duty (kJ/h) (Negative value means condenser duty)
            'SPEC_2' : 0.005,                   # Bottom product purity  
            'Purity' : 0.99,                    # Top product purity 
            # Components - NAMES MUST BE THE SAME AS SET IN ASPEN PLUS (if Aspen is to be used)!! CASE SENSITIVE 
            'Comp_name' : ['METHANOL', 'WATER'],      

            # --------------------------- 
            # Thermal Utilities Data
            # ---------------------------
            # Global heat exchange coefficient (W/m²K) - Cheng - 2009 and Douglas book
            'Ur' : 250/0.17611,         # Reboiler
            'Uc' : 250/0.17611,         # Condenser
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
            'lt' : 0.6096,                              # Tray spacing
            'roshell' : 7900,                           # roshell (kg/m³)

            # --------------------------- 
            # Reflux Drum Data
            # ---------------------------
            'L_D': 4,                                   # L/D ratio
            'TRL_min': 5,                              # Reflux Drum residence time (min)

            # --------------------------- 
            # Aspen Related Data
            # ---------------------------
            # File, block and streams - ATTENTION: THIS NAMES ARE CASE SENSITIVE, MUST BE THE SAME AS IN ASPEN FILE
            'file_name' : ['Methanol_H2O - Q_Fixo.bkp'],
            # Main Column (Specification is the Condenser Duty)
            'block_name' : ['HPC'],
            'stream_names': ['FEED-HPC', 'H-TOP', 'H-BOTTOM'],
            # Secondary Column (Specification is the Top Product Concentration)
            'block_name_2' : ['LPC'],
            'feed_name' : ['FEED-LPC'],
            'stream_names_2': ['FEED-LPC', 'L-TOP', 'L-BOTTOM'],
            # Bounds for manipulated variables within Aspen Active Specs
            'reflux_ratio_bounds': [0,100],             # Reflux ratio 
            'distillate_rate_bounds': [0.01,1]           # Distillate rate 

            }
        },

    },

    'Global_Optimizer': {

        'Selected_Optimizer': 'Golden_Section', # Options are 'Parameter_Enumeration', 'Direct', 'Golden_Section'
        # Bounds must be given in the same order as model optimization variables ['Split']
        'Lower_Bounds': [0.70],
        'Upper_Bounds': [0.90],
        #'Step': 0.10

    },

}

# endregion
###################################################################################################################
###################################################################################################################












