
##################################################################################################################
#region Titles and Header
# Nature: Optimization
# Methodology: Set Trimming and/or Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          12-Dec-2024     Mariana Mello             Original - Apply direct loop
#   0.2          17-Jan-2025     Mariana Mello             Change the name
#   0.3          24-Jan-2025     Mariana Mello             Changes for solve flowsheet with recycle or not
#   0.4          03-Fev-2025     Alice Peccini             Changes for different enumeration type selection
#   0.5          25-Fev-2025     Diego Oliva               Ubication of examples changed. Examples are in
#   0.5          25-Fev-2025     Diego Oliva               subfolders related with the unit type.
#   0.5          25-Fev-2025     Diego Oliva               Calling structure: Projects/ProjectName.py
#   0.6          26-Fev-2025     Alice Peccini             Repository dynamic importation
#   0.7          27-Fev-2025     Alice Peccini             OptiProcess Code Structure Update
#   0.8          26-Apr-2025     Mariana Mello             Add .txt file with Results of Examples
#   0.9          13-May-2025     Mariana Mello             Update .txt file with Examples Results
#   0.10         29-Ago-2025     Diego Oliva               New Set Trimming Incremental full developed
##################################################################################################################
#endregion

##################################################################################################################
##################################################################################################################
#region INPUT: !! Only Model and Example Selection and if you want to create a .txt file with the results!!
# !! Do not modify any other aspect of the file !!
##################################################################################################################

Selected_Model = 'STHE'             # The same as defined in Models_List (CASE SENSITIVE)
Selected_Project = 'Example1'      # The same as defined in {Model}/Projects/{Project}.py (CASE SENSITIVE)
Create_Results_txt = True          # True or False

##################################################################################################################
#endregion
##################################################################################################################
##################################################################################################################
#region Import Library
##################################################################################################################
from OptiCode import (
    Calculations_Prep_Organizer,
    Calculations_Solver_Selection,
    Calculations_Consistency_Check,
    Import_Functions,
    Import_Models)
import sys
import os
import time
from project_store import ProjectError, load_project
##################################################################################################################
#endregion
##################################################################################################################
##################################################################################################################
#region Import Active Example Data and Models Declarations
##################################################################################################################

# Ensure the root directory is in sys.path so Python can locate modules
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

# ========================================= IMPORT SELECTED PROJECT DATA =========================================

# Dynamically select the active project based on user input
try:
    Active_Example = load_project(Selected_Model, Selected_Project, scope="examples")
except ProjectError as exc:
    print(f'**Could not load project {Selected_Project} for model {Selected_Model}: {exc}**')
    sys.exit()

# ================================================================================================================

f_path = f"{Selected_Model}"
file_name = f"Results_{Selected_Model}_{Selected_Project}.txt"
file_path = os.path.join(f_path, file_name)

try:
    if Create_Results_txt:
        with open(file_path, "w", encoding="utf-8") as f:
            pass
except (NameError, KeyError):
    print('\n@@@@@@@@ A .txt file with the results was automatically created @@@@@@@@')
    with open(file_path, "w", encoding="utf-8") as f:
        pass

def save_result(*texts):
    text_c = " ".join(str(t) for t in texts)
    try:
        if Create_Results_txt:
            print(text_c)
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(text_c + "\n")
        else:
            print(text_c)
    except (NameError, KeyError):
        print(text_c)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(text_c + "\n")

# ===================================== IMPORT REQUIRED MODELS DECLARATIONS =====================================

Active_Models_List = [Selected_Model]

# Identify which models are required for first optimization level
for i in range(1, Active_Example['Number_of_Equipment'] + 1):
    
    equipment_key = f'Equipment{i}'             
    Active_Models_List.append(Active_Example[equipment_key]['Model_Declarations']['Type_Equipment'])

# Identify which models are required for next level optimization (if it exists)
if Active_Example.get('Next_Level_Equipments'):

    for i in range(1, Active_Example['Next_Level_Equipments']['Number_of_Equipment'] + 1):
        equipment_key = f'Equipment{i}'
        Active_Models_List.append(Active_Example['Next_Level_Equipments'][equipment_key]['Model_Declarations']
                                  ['Type_Equipment'])

# Removes duplicates from the list
Active_Models_List = list(set(Active_Models_List))

Active_Models = {}
# Import Active_Models Definitions
Active_Models['Models_Def'] = Import_Models.Import_Models(Active_Models_List,'Model_Def_')
# Import Active_Models Constraints_and_OF
Active_Models['Constraints_and_OF'] = Import_Functions.Import_Functions(Active_Models_List,'Constraints_and_OF_')
# Import Active_Models Parameters_Update
Active_Models['Parameters_Update'] = Import_Functions.Import_Functions(Active_Models_List,'Parameters_Update_')

##################################################################################################################
#endregion
##################################################################################################################

##################################################################################################################
#region Run Optimization Code
##################################################################################################################

# Recording start time
start_time = time.time()

# Calls for Example Data Consistency Check 
consistency_report = Calculations_Consistency_Check.Consistency_Check(Active_Example, Active_Models, save_result)
if not consistency_report.get('passed', True):
    save_result('\nMandatory consistency checks failed. Solver was not executed.\n')
    for failure in consistency_report.get('mandatory_failures', []):
        save_result(f" - {failure.get('label', failure.get('id', 'unknown'))}: {failure.get('message', '')}\n")
    sys.exit()

# Active Example Initial Set Up (Parameters, Primordial and Initial Set Generation)
Calculations_Prep_Organizer.Prep_Organizer(Active_Example, Active_Models, Selected_Model, Selected_Example, save_result)

save_result(f'\n******************** Starting Execution for {Selected_Model}_{Selected_Example} ********************\n')

# Call calculations
Solution = Calculations_Solver_Selection.Solver_Selection(Active_Example, Active_Models, Selected_Model, Selected_Example, save_result)
# # Tomazim
# # Display total number of LPC simulations executed 
# from Double_Effect.Model.Constraints_and_OF_Double_Effect import TAC_OF
# print(f"\n\033[92m>>> Total number of LPC simulations executed: {TAC_OF.count_LPC}\033[0m")
# from DC_Q_Condenser.Model.Constraints_and_OF_DC_Q_Condenser import TAC_OF
# print(f"\n\033[92m>>> Total number of HPC simulations executed: {TAC_OF.count_HPC}\033[0m")
# from Commom_Equations_DC.Calculations_DC_Aspen import fun_run_Aspen
# print(f"\n\033[92m>>> Total simulations executed: {fun_run_Aspen.count}\033[0m")
# # Show total simulations executed in Lower Bound Generation
# from Double_Effect.Model.Constraints_and_OF_Double_Effect import LB_Gen
# print(f"\033[92m[Total LB_LPC Run #{LB_Gen.count_LB_LPC}]\033[0m")
# from Double_Effect.Model.Parameters_Update_Double_Effect import TAC_LB_Gen_HPCol
# print(f"\033[92m[Total LB_LPC(HPCol) Run #{TAC_LB_Gen_HPCol.count_LB_LPC_HPCol}]\033[0m")
# from DC_Q_Condenser.Model.Constraints_and_OF_DC_Q_Condenser import TAC_LB_Gen
# print(f"\033[92m[Total LB_HPC Run #{TAC_LB_Gen.count_LB_HPC}]\033[0m")
#from DC_Q_Condenser.Model.Parameters_Update_DC_Q_Condenser import Set_Up_HPCOL
#print(f"\033[92m[Total LB_HPC_x_top Run #{Set_Up_HPCOL.count_LB_HPC_x_top}]\033[0m")

# Record end time
end_time = time.time()


elapsed_total_time = end_time - start_time

save_result(f'Total time elapsed: {elapsed_total_time:.5f} seconds\n')


##################################################################################################################
#endregion
##################################################################################################################
