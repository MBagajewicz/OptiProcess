##################################################################################################################
# region Titles and Header
# Nature: Examples Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025       Diego Oliva                Distillation Examples Repository
#   0.1       11-Mar-2025       Alice Peccini              Separation of Model_Def and Examples files
#   0.2       12-May-2025       Mariana Mello              Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
#   0.3       17-Jun-2025       Miguel Bagajewicz          Rearrange from Ditillation File
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples for DC model in this file
##################################################################################################################

##################################################################################################################
############################################## DISTILLATION COLUMN ###############################################
##################################################################################################################

##################################################################################################################
#region Import Library
import copy
#endregion
##################################################################################################################

###################################################################################################################
# region INPUT EXAMPLE 1

Example1 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'Absorber',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [
    
                            list(range(5, 63))  # Ns (Stages and not trays, as in Aspen Plus)
                                                # Ns = 5 means: condenser + 3 stages within the column + reboiler
                                                # Ns = 42 means: condenser + 40 stages within the column + reboiler                
                                    ],

            # Enumeration type (Options are 'Exhaustive', 'Smart' or 'Segmental_Smart' ---> Default is 'Smart')
            'Type_Enumeration': 'Smart',  
            
        },

         # These Problem_Parameters are used for the computation of Constraint and Objective function values
         #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {


            # --------------------------- 
            # Problem Data
            # ---------------------------

            # General Data
            'Nc' : 3,                           # Number of components
            'Nsmin' : 4,                        # Minimum number of stages (Condenser + 11 stages within the column + Reboiler)
            'Pcol' : 1e5,                       # Column Pressure (Pa) - constant throughout the column --> Pendência: consider some pressure drop

            # Components - NAMES MUST BE THE SAME AS SET IN ASPEN PLUS (if Aspen is to be used)!! CASE SENSITIVE 
            'Comp_name' : ['Amine', 'H2O', 'CO2'], # This was just an example. You may need to consider other components due to dissociations      

            # Feed Data - Lean Solvent Stream 
            'Lean_flow' :  [70, 30, 0.1],       # Component lean solvent feed flow (kmol/h) (same order as Comp_name)
            'Lean_temp' :  113.4 + 273.15,      # Lean solvent temperature (K)

            # Feed Data - Flue Gas Stream
            'Flue_Gas_flow' :  [70, 30, 0.1],   # Component fluie gas feed flow (kmol/h) (same order as Comp_name)
            'Flue_Gas_temp' : 113.4 + 273.15,   # Flue gas temperature (K)

            # Separation Task Specification 
            'CO2_Minimum_Recovery' : 0.90,          # Minimum CO2 recovery


            # --------------------------- 
            # Costing Data
            # ---------------------------
            'lt' : 0.6096,                              # Tray spacing
            'roshell' : 7900,                           # roshell (kg/m³)

            # --------------------------- 
            # Aspen Related Data
            # ---------------------------
            # File, block and streams - ATTENTION: THIS NAMES ARE CASE SENSITIVE, MUST BE THE SAME AS IN ASPEN FILE
            'file_name' : ['Absorber.bkp'],
            'block_name' : ['COLUMN1'],
            'stream_names': ['FLUEGAS', 'LEANSOL', 'RICHSOL', 'PURIFIEDGAS'],

        }
    },
    
}

# endregion
###################################################################################################################
###################################################################################################################
###################################################################################################################













