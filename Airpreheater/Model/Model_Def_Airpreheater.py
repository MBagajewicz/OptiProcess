##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         22-Aug-2025     Sung Young Kim             Copy from GPHE folder

#################################################################################################################
# INPUT: Model of GPHE
##################################################################################################################
##################################################################################################################

# region Model of GPHE

Model_Airpreheater = {

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
        # These parameters are generated before Initial Set generation by Calculations_Initial_Set_Up.py
        # For bilevel optimization models (e.g. Kettle Model used in next_level of DC_ST_HE model), some of the 
        # functions of the list may be skipped and should be called by model programmer inside Next_Level_Set_Up function

        'List_of_Variables': ['Ntp', 'Pl', 'Sa', 'Nph', 'Npc'],
        # List of discrete design variables. User will give discrete options in example file in the same order as 
        # defined here, and this is also the same order that must be used in Constraints_and_OF.py functions

        'Objective_Function': {
            'Equation_Name': ['TAC_OF', 'CAPEX_OF', 'AREA_OF'],
            'Optimization_Variables_Names': ['TAC', 'CAPEX', 'Area'],
            'Unit_OF': ['$/year', '$', 'm²']
        },
        # Objetive Function to be minimized and its corresponding variable and measurement unit
        # Equation_Name must be a function defined in "Constraints_and_FO.py" where Optimization_Variables_Names is 
        # its return variable. 

        'Alternative_Objective_Functions': {
            'Equation_Name': [],
            'Optimization_Variables_Names': [],
            'Unit_OF': []
        },
        # This entry is OPTIONAL. If only one objective function is possible for a given model, programmer may either
        # leave it empty, or completely skip it. This is for models where alternative objective functions are possible
        # User will select the desired function in Examples file 
        # Objective_Function entry is used as DEFAULT

        'Consistency_Check_Functions': ['consistency'],
        'Standard_Variables_Values': {
            'Ntp': list(range(10, 800 + 1)),
            'Pl': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # Pl - Plate size (options of Lp, Lw, Dp)
            'Sa': [30, 45, 50, 60, 65],            # Sa - Chevron angle
            'Nph': [1, 2],                         # Nph - Number of passes of hot stream
            'Npc': [1, 2]                           # Npc - number of passes of cold stream
        }

        # Functions that checks if Example Data provided by user has any consistency problems (e.g. negative flows or compositions)
        # These functions must be provided on Parameters_Update_{Model}.py file

    },

    # ========================================= Set Trimming Information =========================================
    # Set Trimming Information section only needs to be filled if Set_Trimming_Mode is set to True. If not, 
    # model programmer may either leave an empty dictionary or completely skip the entry definition

    'Set_Trimming_Info': {

        'Primordial_Set_Trimming_Constraints_List': [],
        # These are the Set_Trimming functions used for Initial Set Generation (they are applied to Primordial Set before
        # solver is called (e.g. Geometric Constraints, that do not depend on problem data)
        # Listed functions must be defined in Constraints_and_OF.py file
        # This entry is optional, if the list is empty, or if the entry is completely skipped, the Initial Set
        # will be the same as the Primordial Set

        'Set_Trimming_Constraints_List': ['vh_lb', 'vh_ub', 'vc_lb', 'vc_ub', 'DPh_ub', 'DPc_ub', 'Areq'],
        # These are the Set Set Trimming Constraints to be applied to Initial Set when Solver is called
        # They also must be defined in Constraints_and_OF.py file

    }

}

