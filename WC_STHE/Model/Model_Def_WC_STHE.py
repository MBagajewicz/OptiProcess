##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         17-Feb-2025     Diego Oliva                STHE Examples Repository
#   0.2         28-Feb-2025     Alice Peccini              Relocating folders
#   0.3         31-Mar-2025     Mariana Mello              Updates Water Cooler STHE Model
#   0.4         12-May-2025     Mariana Mello              Add data consistency
##################################################################################################################
# INPUT: Model of Water Cooler STHE
##################################################################################################################
# INSTRUCTIONS
# Model of Water Cooler STHE in this file
##################################################################################################################
###################################################################################################################

# region

Model_WC_STHE = {

    # =========================================== General Information ============================================
    # The first entries are General (True or False) Information regarding the Model Operation Mode.
    # These entries are required for all models

    'Global_Optimizer': False,      # Set to True if model requires an external global solver. False otherwise

    'Next_Level': False,            # Set to True if model involves a bilevel optimization. False otherwise

    'Set_Trimming_Mode': True,      # Set to True Set Trimming Mode is selected. False otherwise

    'Sorting_Mode': False,           # Set to True if Sorting is required after Trimming. False otherwise

    'Enumeration_Mode': True,      # Set to True if an Enumeration Mode is to be activated (Enumeration type will
                                    # be selected by user within Example Data if this is set to True)

    # ============================================= Model Information ============================================
    # This entry is required for all models

    'Model_Info': {

        'Parameters_Calculations_List': ['allocation', 'Fw_Thi_min', 'Fw_Tco_min'],
        # This is a list of functions used to generated model calculated parameters and they must be defined
        # in Model.Parameters_Update_(Model).py file 
        # These parameters are generated before Initial Set generation by Calculations_Initial_Set_Up.py
        # For bilevel optimization models (e.g. Kettle Model used in next_level of DC_ST_HE model), some of the 
        # functions of the list may be skipped and should be called by model programmer inside Next_Level_Set_Up function

        'List_of_Variables': ['Ds', 'dte', 'Npt', 'rp', 'lay', 'L', 'Nb', 'Bc'],
        # List of discrete design variables. User will give discrete options in example file in the same order as 
        # defined here, and this is also the same order that must be used in Constraints_and_OF.py functions

        'Objective_Function': {
            'Equation_Name': ['TAC_OF'],
            'Optimization_Variables_Names': ['TAC'],
            'Unit_OF': ['$/year']
        },
        # Objetive Function to be minimized and its corresponding variable and measurement unit
        # Equation_Name must be a function defined in "Constraints_and_FO.py" where Optimization_Variables_Names is
        # its return variable. When more than one is given, user may select the desired objective function, but the first
        # one on the list will be the default is no selection is made

        'Alternative_Objective_Functions': {
            'Equation_Name': [],
            'Optimization_Variables_Names': [],
            'Unit_OF': []
        },
        # This entry is OPTIONAL. If only one objective function is possible for a given model, programmer may either
        # leave it empty, or completely skip it. This is for models where alternative objective functions are possible
        # User will select the desired function in Examples file 
        # Objective_Function entry is used as DEFAULT

        'Consistency_Check_Functions': ['consistency']

        # Functions that checks if Example Data provided by user has any consistency problems (e.g. negative flows or
        # compositions). These functions must be provided on Parameters_Update_{Model}.py file

    },

    # ========================================= Set Trimming Information =========================================
    # Set Trimming Information section only needs to be filled if Set_Trimming_Mode is set to True. If not, 
    # model programmer may either leave an empty dictionary or completely skip the entry definition

    'Set_Trimming_Info': {

        'Incremental_Set_Trimming': True,
        # If it is True you will run Set Trimming in incremental mode

        # If it is False you will run Set Trimming in tradicional mode (i.e. all variables will be always used)

        #'Primordial_Set_Trimming_Constraints_List': ['LD_lb', 'LD_ub', 'lbc_lb', 'lbc_ub','vs_lb','vs_ub','Res_ub','Res_lb','DPs_ub'],
        'Primordial_Set_Trimming_Constraints_List': ['LD_lb', 'LD_ub', 'lbc_lb', 'lbc_ub'],


        # These are the Set_Trimming functions used for Initial Set Generation (they are applied to Primordial Set before
        # solver is called (e.g. Geometric Constraints, that do not depend on problem data)
        # Listed functions must be defined in Constraints_and_OF.py file
        # This entry is optional, if the list is empty, or if the entry is completely skipped, the Initial Set
        # will be the same as the Primordial Set

        'All_Variables_In_The_Problem': ['Ds', 'dte', 'Npt', 'rp', 'lay', 'L', 'Nb', 'Bc'],
        # These are all variables used in the problem constraints ordered as they are declared in constraints; is
        # used when 'Incremental_Set_Trimming" is set to True.


        # This is valid if 'Incremental_Set_Trimming' option is set in True
        # Here you need to add the active variables used in each Primordial_Constraint
        # The order used in 'Primordial_Set_Trimming_Constraints_List' is the order
        # of declaration of each group of the correspondent variables declared in 
        # 'Variables_Used_In_Incremental_For_Each_Primordial_Constraint'
        # (i.e. - 'Primordial_Set_Trimming_Constraints_List': ['LD_lb', 'LD_ub']
        #  - 'Variables_Used_In_Incremental_For_Each_Primordial_Constraint': [['x','y'],['z','x']]
        # where LD_lb depends on x and y while LD_ub depends on z and x


        #'Set_Trimming_Constraints_List': ['vs_lb', 'vs_ub', 'Res_ub', 'Res_lb', 'DPs_ub', 'vt_ub', 'vt_lb', 'Ret_ub',
        #                                  'Ret_lb', 'Tco_ub', 'DPt_ub', 'Areq'],


        'Set_Trimming_Constraints_List': ['vt_lb', 'vt_ub', 'Ret_ub', 'Ret_lb', 'Tco_ub', 'vs_lb', 'vs_ub', 'Res_ub',
                                          'Res_lb', 'DPs_ub', 'DPt_ub', 'Areq'],

        # 'Set_Trimming_Constraints_List': ['vt_lb', 'vt_ub', 'vs_lb', 'vs_ub', 'Ret_ub', 'Ret_lb', 'Res_ub', 'Res_lb',
        #                                   'Tco_ub', 'Areq', 'DPs_ub', 'DPt_ub'],
        # These are the Set Trimming Constraints to be applied to Initial Set when Solver is called

        # They also must be defined in Constraints_and_OF.py file

        'Variables_Used_In_Incremental_For_Each_Set_Trimming_Constraint': [['Ds', 'dte', 'Npt', 'rp', 'lay'],
                                                                           ['Ds', 'dte', 'Npt', 'rp', 'lay'],
                                                                           ['Ds', 'dte', 'Npt', 'rp', 'lay'],
                                                                           ['Ds', 'dte', 'Npt', 'rp', 'lay'],
                                                                           ['Ds', 'dte', 'Npt', 'rp', 'lay'],
                                                                           ['Ds', 'dte', 'Npt', 'rp', 'lay', 'L'],
                                                                           ['Ds', 'dte', 'rp', 'lay', 'L', 'Nb'],
                                                                           ['Ds', 'dte', 'rp', 'lay', 'L', 'Nb'],
                                                                           ['Ds', 'dte', 'rp', 'lay', 'L', 'Nb'],
                                                                           ['Ds', 'dte', 'rp', 'lay', 'L', 'Nb', 'Bc'],
                                                                           ['Ds', 'dte', 'Npt', 'rp', 'lay', 'L', 'Nb',
                                                                            'Bc'],
                                                                           ['Ds', 'dte', 'Npt', 'rp', 'lay', 'L', 'Nb',
                                                                            'Bc']],


        # This is valid if 'Incremental_Set_Trimming' option is set in True
        # Here you need to add the active variables used in each Set_Trimming_Constraint
        # The order used in 'Set_Trimming_Constraints_List' is the order
        # of declaration of each group of the correspondent variables declared in
        # 'Variables_Used_In_Incremental_For_Each_Set_Trimming_Constraint'
        # (i.e. - 'Primordial_Set_Trimming_Constraints_List': ['vs_lb', 'vs_ub']
        #  - 'Variables_Used_In_Incremental_For_Each_Primordial_Constraint': [['x','y'],['z','x']]
        # where vs_lb depends on x and y while vs_ub depends on z and x)

    },

    # ========================================= Enumeration Information =========================================
    # Enumeration Information section only needs to be filled if Enumeration_Mode is set to True. If not,
    # model programmer may either leave an empty dictionary or completely skip the entry definition
    # To see an example go to DC model

    'Enumeration_Info': {

        'Enumeration_Constraint_List': ['Fw_ub_SE', 'vt_ub_SE', 'Ret_ub_SE', 'DPt_ub_SE'],
        # These are feasibility constraints that may be required to check candidate feasibility during enumeration
        # Listed functions must be defined in Constraints_and_OF.py file
        # This entry is optional, if the list is empty, or if the entry is completely skipped, feasibility
        # will not be checked by Enumeration routine, it will be assumed as true

        'Lower_Bound_Equation': ['LB_WC_STHE'],
        # These are the lower bound generation functions required for smart and segmental enumerations
        # If two different functions are to be used for each type of enumeration, the list must have two positions
        # ['fun_LB_Smart','fun_LB_Segmental']. If the same function is to be used programmer may either leave it
        # with a single position, or repeat the function name

        'Fobj_within_LB': False,
        # This must be set to True if candidate's Objective Function are evaluated within LB generation function
    },

}
