##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0        17-Feb-2025      Diego Oliva                Sieve Tray Examples Repository
#   0.1        28-Feb-2025      Alice Peccini              Relocating folders 
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of Sieve Tray Distillation Column Design in this file
##################################################################################################################

################################################### SIEVE TRAY ###################################################

##################################################################################################################
##################################################################################################################
# region INPUT EXAMPLE 1 - SIEVE TRAYS - EXAMPLE FROM SOUZA ET AL, 2022

Model_STRAY_2D = {

    # =========================================== General Information ============================================

    'Global_Optimizer': False,     

    'Next_Level': False,        

    'Set_Trimming_Mode': True,      

    'Sorting_Mode': True,            

    'Enumeration_Mode': False,               

    # ============================================= Model Information ============================================

    'Model_Info': {

        'Parameters_Calculations_List': [],

        'List_of_Variables': ['DRECT' , 'DSTRIP'],

        'Objective_Function': {'Equation_Name': ['Cost_OF'], 'Optimization_Variables_Names': ['COL_CAPEX'], 'Unit_OF': ['$']},

        'Set_Up_Sequential': {'Equipment3': ['fun_sequential']},

    },

    # ========================================= Set Trimming Information =========================================

    'Set_Trimming_Info': {

        'Primordial_Set_Trimming_Constraints_List': [],

        'Set_Trimming_Constraints_List': ['f_viable_DRECT', 'f_viable_DSTRIP']

    },

}












