###################################################################################################################
#region Titles and Header
# Nature: Here we put the constraints and Objective Function used in Set Trimming 
# methodology 
# Methodology: Set trimming
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.1          22-Jul-2025     Alice Peccini             Proposed 
##################################################################################################################
# INPUT: Define Constraints as def and return + or - values depending the > or < inequality
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def) that need to be declared on Example_Repository in 
# ExampleX['EquipmentY']['Model_Declarations']
#endregion
############################################################################################

##################################################################################################################
#region Import Library
import numpy as np
from Commom_Equations_DC import (
    Calculations_DC_Aspen,
    Calculations_DC_Column_Sizing, 
    Calculations_DC_Costs
)

#endregion
##################################################################################################################

##################################################################################################################
#region Functions

# ---------------------------------------------------------------------------------------------------------------- 
# Trimming Functions
# ----------------------------------------------------------------------------------------------------------------

def ST_Ns0(Ns_c,m_p): # Allows only candidates with Ns >= Nsmin (where Nsmin is the minimum of the search, not necessarily the minimum required for the separation task)
    fun_val = m_p['Nsmin'] - Ns_c
    return fun_val

# ---------------------------------------------------------------------------------------------------------------- 
# Objective Function
# ----------------------------------------------------------------------------------------------------------------
def CAPEX_OF(Ns_c,m_p):    

    # Column CAPEX:
    Nt = Ns_c[0]
    Wshell = Calculations_DC_Column_Sizing.f_Wshell(m_p['lt'], Nt, m_p['Dc'], m_p['roshell'])
    CAPEX = Calculations_DC_Costs.fun_CAPEX_Col(Wshell,m_p['Dc'],Nt)

    return CAPEX

# ---------------------------------------------------------------------------------------------------------------- 
# Enumeration Constraints
# ----------------------------------------------------------------------------------------------------------------
def Absorber(Ns_c,m_p):    

    # Running Aspen simulation:
    print(f'Running Aspen simulation for candidate with Ns = {Ns_c[0]}')

    ####### CHANGE NEEDED #######
    # This is the function called to run Aspen for DC model (note that the entries include feed tray)
    # A similar one made for an absorber column must be included in Calculations_DC_Aspen file, and then called here
    results = Calculations_DC_Aspen.fun_run_Aspen(Ns_c[0], Nf_c[0], m_p['Aspen_engine'], m_p['block_name'][0], m_p['stream_names'], m_p['Comp_name'], m_p['Nc'])

    # Viability check:
    ####### CHANGE NEEDED #######
    # Here the absorption task must be checked
    # Assuming a target for minimum recovery
    CO2_rich = results['CO2_flow_rich_solvent'] # You can rename it within the new aspen function defined in Calculations_DC_Aspen, you will new to retrieve this result from Aspen
    CO2_lean = m_p['Lean_flow'][2]              # Retrieve CO2 flow in lean solvent from problem data
    CO2_flue_gas = m_p['Flue_Gas_flow'][2]      # Retrieve CO2 flow in flue gas from problem data
    CO2_absorbed = CO2_rich - CO2_lean
    CO2_recovery = CO2_absorbed/CO2_flue_gas
    fun_val = m_p['CO2_Minimum_Recovery'] - CO2_recovery

    return fun_val

# ---------------------------------------------------------------------------------------------------------------- 
# Lower Bound Function
# ----------------------------------------------------------------------------------------------------------------
def LB_Gen(Ns_c,m_p):

    # Column CAPEX:
    Nt = Ns_c
    Wshell = Calculations_DC_Column_Sizing.f_Wshell(m_p['lt'], Nt, m_p['Dc'], m_p['roshell'])
    LB_sol = Calculations_DC_Costs.fun_CAPEX_Col(Wshell,m_p['Dc'],Nt)

    return LB_sol

#endregion
##################################################################################################################
