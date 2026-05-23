##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025        Diego Oliva               Kettle Examples Repository
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
# endregion
###################################################################################################################

###################################################################################################################
# region INPUT EXAMPLE 1 - KETTLE REBOILER

Model_RTH = {

    # =========================================== General Information ============================================
    # The first entries are General (True or False) Information regarding the Model Operation Mode.
    # These entries are required for all models

    'Global_Optimizer': False,  

    'Next_Level': False,

    'Set_Trimming_Mode': True,      # Set to True Set Trimming Mode is selected. False otherwise

    'Sorting_Mode': True,           # Set to True if Sorting is required after Trimming. False otherwise

    'Enumeration_Mode': False,      # Set to True if an Enumeration Mode is to be activated (Enumeration type will 
                                    # be selected by user within Example Data if this is set to True)

    # ============================================= Model Information ============================================
    # This entry is required for all models

    'Model_Info': {

        'Parameters_Calculations_List': ['fun_Q', 'fun_LMTD', 'fun_m_t', 'fun_Pr', 'fun_Fp', 'fun_q1_max'],

        'List_of_Variables': ['Ds', 'dte', 'Npt', 'rp', 'lay', 'L'],
        
        'Objective_Function': {'Equation_Name': ['Cost_OF', 'Area_OF'], 'Optimization_Variables_Names': ['HE_CAPEX','HE_Area'], 'Unit_OF': ['$','m2']},

    },

    # ========================================= Set Trimming Information =========================================
    # Set Trimming Information section only needs to be filled if Set_Trimming_Mode is set to True. If not, 
    # model programmer may either leave an empty dictionary or completly skip the entry definition

    'Set_Trimming_Info': {

        'Primordial_Set_Trimming_Constraints_List': ['LD_lb', 'LD_ub'],
        # These are the Set_Trimming functions used for Initial Set Generation (they are applied to Primordial Set before
        # solver is called (e.g. Geometric Constraints, that do not depend on problem data)
        # Listed functions must be defined in Constraints_and_OF.py file
        # This entry is optional, if the list is empty, or if the entry is completly skipped, the Initial Set 
        # will be the same as the Primordial Set

        'Set_Trimming_Constraints_List': ['vt_lb', 'vt_ub', 'Ret_lb', 'q_ub', 'dPt_up', 'A_exc'],
        # These are the Set Set Trimming Constraints to be applied to Initial Set when Solver is called
        # They also must be defined in Constraints_and_OF.py file

    }

}

# endregion
###################################################################################################################
###################################################################################################################
