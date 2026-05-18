##################################################################################################################
# region Titles and Header
# Nature: Model Definition
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025       Diego Oliva                Distillation Examples Repository
#   0.1       17-Jun-2025       Miguel Bagajewicz          Rearrange from Ditillation File
##################################################################################################################
# INPUT: Model Definitions for DC model
##################################################################################################################
# INSTRUCTIONS
# Do not modify this file!
##################################################################################################################
############################################## ABSORPTION COLUMN ###############################################
##################################################################################################################

##################################################################################################################
# region INPUT MODEL_DC DEFINITIONS

Model_Absorber = {

    # =========================================== General Information ============================================

    'Global_Optimizer': False,  
    'Next_Level': False,
    'Set_Trimming_Mode': False,     
    'Sorting_Mode': False,          
    'Enumeration_Mode': True,       

    # ============================================= Model Information ============================================

    'Model_Info': {

        'Parameters_Calculations_List': ['par_start_Aspen'],

        'Objective_Function': {'Equation_Name': ['CAPEX_OF'], 'Optimization_Variables_Names': ['CAPEX'], 'Unit_OF': ['$']},

        'List_of_Variables': ['Ns'],

    },

    # ========================================= Set Trimming Information =========================================

    'Set_Trimming_Info': {

        'Primordial_Set_Trimming_Constraints_List': ['ST_Ns0'],

        'Set_Trimming_Constraints_List': [],

    },

    # ========================================= Enumeration Information =========================================

    'Enumeration_Info': {

        'Enumeration_Constraint_List': ['Absorber'],

        'Lower_Bound_Equation': ['LB_Gen'],

        'Fobj_within_LB' : False, 

    },
    
}



















