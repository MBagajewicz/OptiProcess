##################################################################################################################
# region Titles and Header
# Nature: Examples Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025       Diego Oliva                Distillation Examples Repository
#   0.1       11-Mar-2025       Alice Peccini              Separation of Model_Def and Examples files
#   0.2       12-May-2025       Mariana Mello              Changed name from 'Discretized_Values_of_Variables' to
#                                                          'Discrete_Values_of_Variables'
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples for DC model in this file
##################################################################################################################

##################################################################################################################
############################################## DISTILLATION COLUMN ###############################################
##################################################################################################################

##################################################################################################################
#region Import Library
import copy
#endregion
##################################################################################################################

###################################################################################################################
# region INPUT EXAMPLE 1 - Methanol-Water DISTILLATION COLUMN WITH SEGMENTAL SMART ENUMERATION

Example1 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'DC_Q_Condenser',

            # Discrete_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discrete_Values_of_Variables': [
    
                            list(range(10, 21)), # Nf (Feed considered from stage 3 to 40, considering there are always a stripping 
                                                # and a rectifying section)
                                                # Nf is interpreted regarding stages and not trays (same as in Aspen Plus)
                            list(range(15, 21))  # Ns (Stages and not trays, as in Aspen Plus)
                                                # Ns = 5 means: condenser + 3 stages within the column + reboiler
                                                # Ns = 42 means: condenser + 40 stages within the column + reboiler                
                                    ],

            # Enumeration type (Options are 'Exhaustive', 'Smart' or 'Segmental_Smart' ---> Default is 'Smart')
            'Type_Enumeration': 'Smart',  
            
            # Segmentation parameters - to be used when Segmental Smart Enumeration is true --> Leave it empty otherwise []
            'Segmentation_Parameters' : [], 
                                    # Segmentation_Parameters[0]: The name of the discrete variable needs to mach one of the variables 
                                    #                             given in 'List_of_Variables'
                                    # Segmentation_Parameters[1]: Increment (n° of values in each segment) 
                                    #                             -> If too small --> Excessive n° of intervals
                                    #                             -> If too large --> Candidates cutting may not be as effective
                                    # Segmentation_Parameters[2]: Correction factor to avoid small interval at the last segment


        },

         # These Problem_Parameters are used for the computation of Constraint and Objective function values
         #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {


            # --------------------------- 
            # Problem Data
            # ---------------------------
            # General Data
            'Nc' : 3,                           # Number of components
            'Nsmin' : 1,                       # Minimum number of stages (Condenser + 11 stages within the column + Reboiler)
            'Nfmin' : 1,                        # Minimum feed tray
            'Pcol' : 5e5,                       # Column Pressure (Pa) - constant throughout the column --> Pendência: consider some pressure drop
            # Feed Data 
            'z_f' : [0.6, 0.4],                 # Feed molar composition [Benzene, Toluene, m-Xylene]
            'F_f' :  100,                       # Feed flow (kmol/h)
            'T_f' :  113.4 + 273.15,            # Feed temperature (K)
            # Separation Task Specification 
            'SPEC_1' : -5098859.86,			    # Condenser duty (kJ/h) (Negative value means condenser duty)
            'SPEC_2' : 0.005,                   # Bottom product purity  
            'Purity' : 0.99,                    # Top product purity
            # Components - NAMES MUST BE THE SAME AS SET IN ASPEN PLUS (if Aspen is to be used)!! CASE SENSITIVE 
            'Comp_name' : ['METHANOL', 'WATER'],      

            # --------------------------- 
            # Thermal Utilities Data
            # ---------------------------
            # Global heat exchange coefficient (W/m²K) - Cheng - 2009 and Douglas book
            'Ur' : 1050,                # Reboiler
            'Uc' : 850,                 # Condenser
            # Utilities temperatures (K)
            'Tlpst' : 160 + 273.15,     # Low pressure steam 
            'Tcwin' : 370.0,           # Cooling water inlet  (Before: 303.15 K)
            'Tcwout' : 371.9,          # Cooling water outlet (Before: 323.15 K)

            # --------------------------- 
            # Costing Data
            # ---------------------------
            'Ccw' : 0.378e-6,                           # Utilities costs ($/kJ) from Turton -> page 245 5ed 
            'Clpst' : 2.78e-6,                          # Utilities costs ($/kJ) from Turton -> page 245 5ed 
            'hours' : 8150,                             # Number of operation hours in a year (considering 7% of idle capacity)
            'Pb' : 3,                                   # Payback period (years)
            'lt' : 0.6096,                              # Tray spacing
            'roshell' : 7900,                           # roshell (kg/m³)

            # --------------------------- 
            # Reflux Drum Data
            # ---------------------------
            'L_D': 4,                                   # L/D ratio
            'TRL_min': 5,                              # Reflux Drum residence time (min)

            # --------------------------- 
            # Aspen Related Data
            # ---------------------------
            # File, block and streams - ATTENTION: THIS NAMES ARE CASE SENSITIVE, MUST BE THE SAME AS IN ASPEN FILE
            'file_name' : ['Methanol_H2O - Q_Fixo.bkp'],
            # Main Column (Specification is the Condenser Duty)
            'block_name' : ['HPC'],
            'stream_names': ['FEED-HPC', 'H-TOP', 'H-BOTTOM'],
            # Secondary Column (Specification is the Top Product Concentration)
            'block_name_2' : ['LPC'],
            'stream_names_2' : ['FEED-LPC', 'L-TOP', 'L-BOTTOM'],
            # Bounds for manipulated variables within Aspen Active Specs
            'reflux_ratio_bounds': [0,100],             # Reflux ratio 
            'distillate_rate_bounds': [0,100],           # Distillate rate 

            #Save TAC results in Excel file
            'TAC_new_file': True       # If True, creates a new .xlsx file with the TAC results of each simulation
            #m_p['TAC_new_file'] = True

        }
    },
    
}

# endregion
###################################################################################################################
###################################################################################################################


