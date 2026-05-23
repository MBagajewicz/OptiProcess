##################################################################################################################
# region Titles and Header
# Nature: Model Definition
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025       Diego Oliva                Distillation Examples Repository
##################################################################################################################
# INPUT: Model Definitions for DC_ST model
##################################################################################################################
# INSTRUCTIONS
# Do not modify this file!
##################################################################################################################
######################################## DISTILLATION COLUMN + SIEVE TRAY ########################################
##################################################################################################################

###################################################################################################################
# region INPUT MODEL_DC_ST DEFINITIONS

Model_Double_Effect = {

    # =========================================== General Information ============================================

    'Global_Optimizer': False,  
    'Next_Level': True,
    'Set_Trimming_Mode': True,       
    'Sorting_Mode': True,           
    'Enumeration_Mode': True,       

    # ============================================= Model Information ============================================

    'Model_Info': {

        'Parameters_Calculations_List': ['par_start_Aspen'],

        'Objective_Function': {'Equation_Name': ['TAC_OF'], 'Optimization_Variables_Names': ['TAC'], 'Unit_OF': ['$/year']},

        'List_of_Variables': ['Nf' , 'Ns'],
                                   
    },

    # ========================================= Set Trimming Information =========================================

    'Set_Trimming_Info': {

        'Primordial_Set_Trimming_Constraints_List': ['ST_Triang','ST_Ns0'],

        'Set_Trimming_Constraints_List': [],

    },

    # ========================================= Enumeration Information =========================================

    'Enumeration_Info': {

        'Enumeration_Constraint_List': [],

        'Lower_Bound_Equation': ['LB_Gen','LB_Gen'],

        'Fobj_within_LB' : False, 

    },

    # ========================================= Next Level Equipment =========================================

    'Next_Level_Info': {

        'Set_Up_Next_Level': {
            'Equipment1': 'Set_Up_HPCOL'
        }

    },

}

# endregion
###################################################################################################################
###################################################################################################################







