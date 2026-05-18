##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         17-Feb-2025     Diego Oliva                STHE Examples Repository
#   0.1         23-Mar-2025     Sung Young Kim             HEATER Examples 
#   0.2         24-Mar-2025     Sung Young Kim             ('Do','td')('Ds','ts') used as set. 'tf', 'lf', 'Nf' move to parameter 
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of HEATER in this file
##################################################################################################################

# region Import Library
# endregion


####################################################################################################################
####################################################################################################################

# region INPUT EXAMPLE 1 - FIRED_HEATER

Model_FIRED_HEATER = {

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

        'Parameters_Calculations_List': [],
        # This is a list of functions used to generated model calculated parameters and they must be defined 
        # in Model.Parameters_Update_(Model).py file 
        # These parameters are generated before Intial Set generation by Calculations_Initial_Set_Up.py
        # For bilevel optimization models (e.g. Kettle Model used in next_level of DC_ST_HE model), some of the 
        # functions of the list may be skipped and should be called by model programmer inside Next_Level_Set_Up function

        #'List_of_Variables': ['Do' , 'td',  'Ds', 'ts', 'L',  'Npasses', 'Ntceil', 'Nrconv', 'Nprad', 'Npconv', 'Hs', 'Rpr', 'Rph', 'Rpv'],
        'List_of_Variables': ['Do_td' , 'Ds_ts', 'L',  'Npasses', 'Ntceil', 'Nrconv', 'Nprad', 'Npconv', 'Hs', 'Rpr', 'Rph', 'Rpv'],

        # List of discrete design variables. User will give discrete options in example file in the same order as 
        # defined here, and this is also the same order that must be used in Constraints_and_OF.py functions


        'Objective_Function': {'Equation_Name': 'FIRED_HEATER_OF', 'Optimization_Variables_Names': 'OF_Solution', 'Unit_OF': '$/year'},

        # Objetive Function to be minimized and its corresponding variable and measurement unit
        # Equation_Name must be a function defined in "Constraints_and_FO.py" where Optimization_Variables_Names is 
        # its return variable. 

        'Alternative_Objective_Functions': {
            'Equation_Name': [],
            'Optimization_Variables_Names': [],
            'Unit_OF': []
        },
        # This entry is OPTIONAL. If only one objective function is possible for a given model, programmer may either
        # leave it empty, or completly skip it. This is for models where alternative objective functions are possible
        # User will select the desired function in Examples file 
        # Objective_Function entry is used as DEFAULT

    },

    # ========================================= Set Trimming Information =========================================
    # Set Trimming Information section only needs to be filled if Set_Trimming_Mode is set to True. If not, 
    # model programmer may either leave an empty dictionary or completly skip the entry definition

    'Set_Trimming_Info': {

        'Primordial_Set_Trimming_Constraints_List': ['HW_lb', 'HW_ub', 'LW_lb', 'LW_ub','BOX_lb', 'BOX_ub' , 'dcr_lb', 'dch_lb', 'Tube_lb', 'Ds_ub'],
        # These are the Set_Trimming functions used for Initial Set Generation (they are applied to Primordial Set before
        # solver is called (e.g. Geometric Constraints, that do not depend on problem data)
        # Listed functions must be defined in Constraints_and_OF.py file
        # This entry is optional, if the list is empty, or if the entry is completly skipped, the Initial Set 
        # will be the same as the Primordial Set

        'Set_Trimming_Constraints_List': [
                                          'Vo_ub', 'Po_ub' ,    # Set-Trimming for oil velocity and pressure drop
                                          'glb_ub', 'gub_lb',  # Proxy Set Trimming for gas mass flux
                                          'tc_ub', 'tc_lb', 'tfb_ub', 'tfb_lb1', 'tfb_lb2',  # Proxy Set Trimming for radiant section                               
                                          'ts_lb' ,'ts_ub' , 'Qconv_ub',    # Proxy Set Trimming for convection section
                                          'DE_ub'      # draft
                                          ],
        # These are the Set Set Trimming Constraints to be applied to Initial Set when Solver is called
        # They also must be defined in Constraints_and_OF.py file

    },

    # ========================================= Enumeration Information =========================================
    # Enumeration Information section only needs to be filled if Enumeration_Mode is set to True. If not, 
    # model programmer may either leave an empty dictionary or completly skip the entry definition

    'Enumeration_Info': {

        'Enumeration_Constraint_List': [
                                        #'FLUX_lb', 'FLUX_ub'
                                       ], # eq 59, 92, 94
        # These are feasibility constraints that may be required to check candidate feasibility during enumeration 
        # Listed functions must be defined in Constraints_and_OF.py file
        # This entry is optional, if the list is empty, or if the entry is completly skipped, feasibility 
        # wont be checked by Enumeration routine, it will be assumed as true

        'Lower_Bound_Equation': ['FIRED_HEATER_LB', ],
        # This are the lower bound generation functions required for smart and segmental enumerations
        # If two different functions are to be used for each type of enumeration, the list must have two positions
        # ['fun_LB_Smart','fun_LB_Segmental']. If the same funtion is to be used programmer may either leave it 
        # with a single position, or repeat the function name 

        'Fobj_within_LB' : False, 
        # This must be set to True if candidate's Objective Function are evaluated within LB generation function
    }


}
