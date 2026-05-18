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

import copy

################################################### SIEVE TRAY ###################################################

##################################################################################################################
##################################################################################################################
# region INPUT EXAMPLE 1 - SIEVE TRAYS - EXAMPLE FROM SOUZA ET AL, 2022

Model_STRAY = {

    # =========================================== General Information ============================================
    # The first entries are General (True or False) Information regarding the Model Operation Mode.
    # These entries are required for all models

    'Global_Optimizer': False,     # Set to True if model requires an external solver (direct). False otherwise

    'Next_Level': False,        # Set to True if model involves a bilevel optimization. False otherwise

    'Set_Trimming_Mode': True,       # Set to True Set Trimming Mode is selected. False otherwise

    'Sorting_Mode': True,            # Set to True if Sorting is required after Trimming. False otherwise

    'Enumeration_Mode': False,       # Set to True if an Enumeration Mode is to be activated (Enumeration type will 
                                # be selected by user within Example Data if this is set to True)

    # ============================================= Model Information ============================================

    # Model Information (Parameters Calculation List, Objective Function and List of Variables)
    'Model_Info': {

        'Parameters_Calculations_List': [],
        # This is a list of functions used to generated model calculated parameters and they must be defined 
        # in Model.Parameters_Update_(Model).py file 
        # These parameters are generated before Intial Set generation by Calculations_Initial_Set_Up.py
        # For bilevel optimization models (e.g. Kettle Model used in next_level of DC_ST_HE model), some of the 
        # functions of the list may be skipped and should be called by model programmer inside Next_Level_Set_Up function

        'List_of_Variables': ['Dc' , 'dh' , 'hdwap' , 'hw' , 'lt' , 'lw' , 'lp' , 'tt' , 'lay'],
        # List of discrete design variables. User will give discrete options in example file in the same order as 
        # defined here, and this is also the same order that must be used in Constraints_and_OF.py functions

        'Objective_Function': {
            'Equation_Name': ['Cost_OF','Wtotal_OF','Wshell_OF', 'dPtotal_OF'], 
            'Optimization_Variables_Names': ['COL_CAPEX','Wtotal', 'Wshell', 'ht_total'],
            'Unit_OF': ['$','kg', 'kg', 'm']
            },
        # Objetive Function to be minimized and its corresponding variable and measurement unit
        # Equation_Name must be a function defined in "Constraints_and_FO.py" where Optimization_Variables_Names is 
        # its return variable. When more than one is given, user may select the desired objective function, but the first
        # one on the list will be the default if no selection is made

    },

    # ========================================= Set Trimming Information =========================================

    # Set Trimming Information section only needs to be filled if Model['Set_Trimming'] is set to True
    'Set_Trimming_Info': {

        # Set Trimming Constraints to be applied to Primordial Set for an Initial Set Generation (eg. Geometric coinstraints)
        'Primordial_Set_Trimming_Constraints_List': ['f_lw_Dc', 'f_lp_dh' , 'f_dh_tt', 'f_hw_lt', 'f_Ah_Aa_LB', 'f_Ah_Aa_UB'],

        # Equations Trimming List - to be used when Set_Trimming_Mode = True --> Leave as empty [] otherwise
        'Set_Trimming_Constraints_List': ['f_uh_uhmin', 'f_hb_lt_hw', 'f_rtime', 'f_un_uflood', 'f_psi_snt'],

    },

}












