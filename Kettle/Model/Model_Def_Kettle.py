##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025       Diego Oliva                Kettle Examples Repository
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of Kettle in this file
##################################################################################################################

# region Import Library
import numpy as np
# endregion


############################# Kettle Reboiler- Gustavo #####################################

###################################################################################################################
###################################################################################################################
# region INPUT EXAMPLE 1 - KETTLE REBOILER

Model_Kettle = {

    # =========================================== General Information ============================================
    # The first entries are General (True or False) Information regarding the Model Operation Mode.
    # These entries are required for all models

    'Global_Optimizer': False,      # Set to True if model requires an external global solver. False otherwise

    'Next_Level': False,            # Set to True if model involves a bilevel optimization. False otherwise

    'Set_Trimming_Mode': True,      # Set to True Set Trimming Mode is selected. False otherwise

    'Sorting_Mode': True,           # Set to True if Sorting is required after Trimming. False otherwise

    'Enumeration_Mode': False,      # Set to True if an Enumeration Mode is to be activated (Enumeration type will 
                                    # be selected by user within Example Data if this is set to True)
                                    
    # ============================================= Model Information ============================================
    # This entry is required for all models

     'Model_Info': {

        'Parameters_Calculations_List': [],
        # This is a list of functions used to generated model calculated parameters and they must be defined 
        # in Model.Parameters_Update_(Model).py file 
        # These parameters are generated before Intial Set generation by Calculations_Initial_Set_Up.py
        # For bilevel optimization models (e.g. Kettle Model used in next_level of DC_ST_HE model), some of the 
        # functions of the list may be skipped and should be called by model programmer inside Next_Level_Set_Up function

        'List_of_Variables': ['finnedsurface', 'L', 'rp', 'Nbay', 'Nbbay', 'Ntr', 'aircoolerconfig', 'Nfanbay',
                                'Dfan'],
        # List of discrete design variables. User will give discrete options in example file in the same order as 
        # defined here, and this is also the same order that must be used in Constraints_and_OF.py functions

        'Objective_Function': {'Equation_Name': ['Kettle_OF'], 'Optimization_Variables_Names': ['OF_Solution'], 'Unit_OF': ['$/year']},
        # Objetive Function to be minimized and its corresponding variable and measurement unit
        # Equation_Name must be a function defined in "Constraints_and_FO.py" where Optimization_Variables_Names is 
        # its return variable. 

    },

    # ========================================= Set Trimming Information =========================================
    # Set Trimming Information section only needs to be filled if Set_Trimming_Mode is set to True. If not, 
    # model programmer may either leave an empty dictionary or completly skip the entry definition

    'Set_Trimming_Info': {

        'Primordial_Set_Trimming_Constraints_List': [],
        # These are the Set_Trimming functions used for Initial Set Generation (they are applied to Primordial Set before
        # solver is called (e.g. Geometric Constraints, that do not depend on problem data)
        # Listed functions must be defined in Constraints_and_OF.py file
        # This entry is optional, if the list is empty, or if the entry is completly skipped, the Initial Set 
        # will be the same as the Primordial Set

       'Set_Trimming_Constraints_List': ['Reh_lb', 'Rec_lb', 'Rec_ub', 'Ltp_lb', 'Ltp_ub', 'L_Dti_ratio_lb',
                                            'Aot_Ar_ratio_lb', 'Aot_Ar_ratio_ub', 'Lf_tf_ratio_lb', 'Df_Dte_ratio_ub',
                                            'Areq', 'min_gap', 'DPh_ub', 'vt_lb', 'vt_ub', 'const_1', 'const_2',
                                            'const_3'],
                                                    # These are the Set Set Trimming Constraints to be applied to Initial Set when Solver is called
        # They also must be defined in Constraints_and_OF.py file

    }

}

# endregion
###################################################################################################################
###################################################################################################################

