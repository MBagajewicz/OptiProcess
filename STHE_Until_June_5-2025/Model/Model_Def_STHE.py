##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         17-Feb-2025     Diego Oliva                STHE Examples Repository
#   0.2         28-Feb-2025     Alice Peccini              Relocating folders
#   0.3         08-May-2025     Mariana Mello              Add consistency check
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add STHE Model info in this file
##################################################################################################################

# region Import Library
# endregion


####################################################################################################################
####################################################################################################################

# region

Model_STHE = {

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

        'Parameters_Calculations_List': ['allocation'],
        # This is a list of functions used to generated model calculated parameters and they must be defined 
        # in Model.Parameters_Update_(Model).py file 
        # These parameters are generated before Initial Set generation by Calculations_Initial_Set_Up.py
        # For bilevel optimization models (e.g. Kettle Model used in next_level of DC_ST_HE model), some of the 
        # functions of the list may be skipped and should be called by model programmer inside Next_Level_Set_Up
        # function

        'List_of_Variables': ['Ds', 'dte', 'Npt', 'rp', 'lay', 'L', 'Nb', 'Bc'],
        # List of discrete design variables. User will give discrete options in example file in the same order as 
        # defined here, and this is also the same order that must be used in Constraints_and_OF.py functions

        'Objective_Function': {
            'Equation_Name': ['TAC_OF', 'CAPEX_OF', 'AREA_OF'],
            'Optimization_Variables_Names': ['TAC', 'CAPEX', 'Area'],
            'Unit_OF': ['$/year', '$', 'm²']
        },
        # Objetive Function to be minimized and its corresponding variable and measurement unit
        # Equation_Name must be a function defined in "Constraints_and_FO.py" where Optimization_Variables_Names is 
        # its return variable. When more than one is given, user may select the desired objective function, but the
        # first one on the list will be the default if no selection is made

        'Consistency_Check_Functions': ['consistency'],
        'Standard_Variables_Values': {
            'Ds': [0.2032, 0.254, 0.3048, 0.33655, 0.38735, 0.43815, 0.48895, 0.53975, 0.59055, 0.635, 0.6858, 0.7366,
                   0.7874, 0.8382, 0.8890, 0.9398, 0.9906, 1.0668, 1.143, 1.2192, 1.3716, 1.524, 1.6764, 1.8288, 1.9812,
                   2.1336, 2.286, 2.4384, 2.7432, 3.048],
            'dte': [0.01905, 0.02540, 0.03175, 0.03810, 0.05080],
            'Npt': [1, 2, 4, 6],
            'rp': [1.25, 1.33, 1.50],
            'lay': [1, 2, 3],
            'L': [1.2195, 1.524, 1.8288, 2.1336, 2.4384, 2.7432, 3.048, 3.3528, 3.6576, 3.9624, 4.2672, 4.572, 4.8768,
                  5.1816, 5.4864, 5.7912, 6.0976],
            'Nb': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'Bc': [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45]
        }

        # Functions that checks if Example Data provided by user has any consistency problems (e.g. negative flows or compositions)
        # These functions must be provided on Parameters_Update_{Model}.py file
        
    },

    # ========================================= Set Trimming Information =========================================
    # Set Trimming Information section only needs to be filled if Set_Trimming_Mode is set to True. If not, 
    # model programmer may either leave an empty dictionary or completely skip the entry definition

    'Set_Trimming_Info': {

        'Primordial_Set_Trimming_Constraints_List': ['LD_lb', 'LD_ub', 'lbc_lb', 'lbc_ub'],
        # These are the Set_Trimming functions used for Initial Set Generation (they are applied to Primordial Set before
        # solver is called (e.g. Geometric Constraints, that do not depend on problem data)
        # Listed functions must be defined in Constraints_and_OF.py file
        # This entry is optional, if the list is empty, or if the entry is completely skipped, the Initial Set
        # will be the same as the Primordial Set

        'Set_Trimming_Constraints_List': ['lbmax', 'vs_lb', 'vs_ub', 'vt_lb', 'vt_ub', 'Ret_lb', 'Ret_ub', 'Res_lb',
                                          'Res_ub', 'DPs_ub', 'DPt_ub', 'F_min', 'Areq'],
        #'Set_Trimming_Constraints_List': ['vs_lb', 'vs_ub', 'vt_lb', 'vt_ub', 'Ret_lb', 'Ret_ub', 'Res_lb',
        #                                  'Res_ub', 'DPs_ub', 'DPt_ub', 'F_min', 'Areq'],
        # These are the Set Set Trimming Constraints to be applied to Initial Set when Solver is called
        # They also must be defined in Constraints_and_OF.py file

        'Recursive_Set_Trimming': {
            'Variable_Name': 'yfluid',
            'Variable_Options': ['cold_stream', 'hot_stream'],
            'ST_Exclusion_Functions': ['TAC_OF']
            },
        # Recursive Set Trimming Option. It is Optional. If user defines the parameter with the same name, 
        # only one option would be evaluated. If user does not enter a valid option, Varible_Options will be used.

    }

}
