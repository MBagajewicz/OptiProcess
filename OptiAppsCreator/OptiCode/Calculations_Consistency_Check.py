#
#region Titles and Header
# Nature: Optimization
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE             AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          May-2025         Alice Peccini             Proposed
#   0.2          13-May-2025      Mariana Mello             Update .txt file with Examples Results
##################################################################################################################
##################################################################################################################
#endregion

import inspect

##################################################################################################################
#region Calculations organizer to call Initial Set Up

def _call_consistency_function(function_obj, model_declarations, model_parameters, save_result, consistency_config, consistency_report):
    signature = inspect.signature(function_obj)
    if len(signature.parameters) >= 5:
        return function_obj(model_declarations, model_parameters, save_result, consistency_config, consistency_report)
    return function_obj(model_declarations, model_parameters, save_result)

def Consistency_Check(Active_Example, Active_Models, save_result, consistency_config=None, consistency_report=None):

    # First Level Optimization Equipment Data Consistency Check:
    for i in range(1, Active_Example['Number_of_Equipment'] + 1):

        # Detect Equipment Data and corresponding Model Definitions, Model Declarations and Model Parameters
        equipment_dt = Active_Example[f'Equipment{i}']
        model_declarations = equipment_dt['Model_Declarations']
        model_parameters = equipment_dt['Model_Parameters']
        Type_Equipment = model_declarations['Type_Equipment']
        equipment_def = Active_Models['Models_Def'][Type_Equipment]

        # Identify and run consistency check functions
        Parameters_Update_Module = Active_Models['Parameters_Update'][Type_Equipment]
        Consistency_Funcions = equipment_def['Model_Info'].setdefault('Consistency_Check_Functions', [])
        for function in Consistency_Funcions:
            _call_consistency_function(getattr(Parameters_Update_Module, function), model_declarations, model_parameters, save_result, consistency_config, consistency_report)
        
    # Next Level Equipment Data Consistency Check:
    if Active_Example.get('Next_Level_Equipments'):
        
        for i in range(1, Active_Example['Next_Level_Equipments']['Number_of_Equipment'] + 1):
   
            # Detect Equipment Data and corresponding Model Definitions, Model Declarations and Model Parameters
            equipment_dt = Active_Example['Next_Level_Equipments'][f'Equipment{i}']
            model_declarations = equipment_dt['Model_Declarations']
            model_parameters = equipment_dt['Model_Parameters'] 
            Type_Equipment = model_declarations['Type_Equipment']
            equipment_def = Active_Models['Models_Def'][Type_Equipment]

            # Identify and run consistency check functions
            Parameters_Update_Module = Active_Models['Parameters_Update'][Type_Equipment]
            Consistency_Funcions = equipment_def['Model_Info'].setdefault('Consistency_Check_Functions', [])
            for function in Consistency_Funcions:
                _call_consistency_function(getattr(Parameters_Update_Module, function), model_declarations, model_parameters, save_result, consistency_config, consistency_report)
                
#endregion
####################################################################################################################
