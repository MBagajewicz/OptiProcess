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

##################################################################################################################
#region Calculations organizer to call Initial Set Up

def _empty_report():
    return {
        'passed': True,
        'equipments': [],
        'warnings': [],
        'mandatory_failures': [],
    }


def _append_equipment_report(global_report, equipment_name, model_name, report):
    if report is None:
        report = {'passed': True, 'results': [], 'warnings': [], 'mandatory_failures': []}
    equipment_report = {
        'equipment': equipment_name,
        'model': model_name,
        'passed': report.get('passed', True),
        'results': report.get('results', []),
        'warnings': report.get('warnings', []),
        'mandatory_failures': report.get('mandatory_failures', []),
    }
    global_report['equipments'].append(equipment_report)
    global_report['warnings'].extend(equipment_report['warnings'])
    global_report['mandatory_failures'].extend(equipment_report['mandatory_failures'])
    global_report['passed'] = global_report['passed'] and equipment_report['passed']


def _call_consistency_function(function_obj, model_declarations, model_parameters, save_result):
    result = function_obj(model_declarations, model_parameters, save_result)
    if isinstance(result, tuple) and len(result) >= 3 and isinstance(result[2], dict):
        return result[2]
    return {'passed': True, 'results': [], 'warnings': [], 'mandatory_failures': []}


def Consistency_Check(Active_Example, Active_Models, save_result):
    report = _empty_report()

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
            function_report = _call_consistency_function(
                getattr(Parameters_Update_Module, function), model_declarations, model_parameters, save_result
            )
            _append_equipment_report(report, f'Equipment{i}', Type_Equipment, function_report)
        
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
                function_report = _call_consistency_function(
                    getattr(Parameters_Update_Module, function), model_declarations, model_parameters, save_result
                )
                _append_equipment_report(report, f'Next_Level_Equipment{i}', Type_Equipment, function_report)

    return report
                 
#endregion
####################################################################################################################
