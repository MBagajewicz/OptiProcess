##################################################################################################################
# region Titles and Header
# Nature: 'Parameters_Calculations_List' and 'Example_Within_Set_Up' functions
# Methodology: Set trimming and Enumeration
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0          28-Fev-2025     Alice Peccini             Original
##################################################################################################################
# INPUT: Define Functions for 'Parameters_Calculations_List' and 'Example_Within_Set_Up'
##################################################################################################################
# INSTRUCTIONS
# Add python functions (def)
# For 'Parameters_Calculations_List':
#   def fun(model_parameters)
#       return model_parameters
# For 'Example_Within_Set_Up':
#   def fun(results,model_parameters)
#       return model_parameters
# endregion
##################################################################################################################

##################################################################################################################
# region Import Library
from Commom_Equations_DC import Calculations_DC_Param_Set_Up
from Reflux_Drum.Model import Parameters_Update_Reflux_Drum

# endregion
##################################################################################################################


##################################################################################################################
# region Parameters Calculation functions


# Initialize Aspen
def par_start_Aspen(m_p):

    m_p = Calculations_DC_Param_Set_Up.call_initial_Aspen(m_p)

    return m_p

# HSTC set up
def Set_Up_HSTC(results, m_p):

    m_p = Calculations_DC_Param_Set_Up.SU_HSTC(results, m_p)

    return m_p

# Kettle Set up
def Set_Up_Kettle(results, m_p):

    m_p = Calculations_DC_Param_Set_Up.SU_Kettle(results, m_p)

    return m_p

# Reflux Drum Set Up
def Set_Up_Reflux_Drum(results, m_p):

    m_p = Calculations_DC_Param_Set_Up.SU_Reflux_Drum(results, m_p)

    return m_p

def Set_Up_Stripping(results, m_p):

    # Number of trays:
    Nt_strip = results['Nf'] - 2
    m_p['Nt'] = Nt_strip
    
    # Liquid and vapor flows (converted from kg/hr to kg/s)
    m_p['Lw'] = (results['liquid_mass_flows'][1:Nt_strip+1]/3600).tolist()
    m_p['Vw'] = (results['vapor_mass_flows'][1:Nt_strip+1]/3600).tolist()

    # Hydraulics:
    m_p['rol'] = results['hydraulics']['density_liquid'][0:Nt_strip].tolist()       # kg/m³
    m_p['rov'] = results['hydraulics']['density_vapor'][0:Nt_strip].tolist()        # kg/m³
    m_p['sig'] = results['hydraulics']['surface_tension'][0:Nt_strip].tolist()      # N/m

    return m_p

def Set_Up_Rectifying(results, m_p):

    # Number of trays:
    Nt_rect = results['Ns'] - results['Nf']
    m_p['Nt'] = Nt_rect
    Nf = results['Nf']
    
    # Liquid and vapor flows (converted from kg/hr to kg/s)
    m_p['Lw'] = (results['liquid_mass_flows'][Nf-1:-1]/3600).tolist()
    m_p['Vw'] = (results['vapor_mass_flows'][Nf-1:-1]/3600).tolist()

    # Hydraulics:
    m_p['rol'] = results['hydraulics']['density_liquid'][Nf-2:].tolist()       # kg/m³
    m_p['rov'] = results['hydraulics']['density_vapor'][Nf-2:].tolist()        # kg/m³
    m_p['sig'] = results['hydraulics']['surface_tension'][Nf-2:].tolist()      # N/m

    return m_p

def Set_Up_Column(results, m_p):

    Nt_strip = results['Nf'] - 2
    m_p['Nt_strip'] = Nt_strip

    Nt_rect = results['Ns'] - results['Nf']
    m_p['Nt_rect'] = Nt_rect

    return m_p

# endregion
##################################################################################################################

