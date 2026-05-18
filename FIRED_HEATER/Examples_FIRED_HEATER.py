##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0         17-Feb-2025     Diego Oliva                STHE Examples Repository
#   0.1         23-Mar-2025     Sung Young Kim             Copy and made HEATER Examples Ropository 
#   0.2         14-Apr-2025     Sung Young Kim             Rename 'HEATER' to 'FIRED_HEATER'
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of FIRED_HEATER in this file
##################################################################################################################

# region Import Library
import numpy as np
import copy
# endregion


####################################################################################################################
####################################################################################################################

# region INPUT EXAMPLE 1 - FIRED_HEATER

Example1 = {

    'Number_of_Equipment': 1,

    'Equipment1': {

        'Model_Declarations': {

            # Type of Equipment - Models_List
            'Type_Equipment': 'FIRED_HEATER',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discretized_Values_of_Variables': [
                ["(0.2917,0.0183)", "(0.3333,0.0192)", "(0.3750,0.0200)", "(0.4636,0.0217)", "(0.5521,0.0233)"], #tuples for Do and td
                #["(0.3750,0.0200)"],
                #[0.2917, 0.3333, 0.3750, 0.4636, 0.5521], # Do : outer tube diameter 
                #[0.0183, 0.0192, 0.0200, 0.0217, 0.0233], # td : tube wall thickness
                #[0.0200], # td : tube wall thickness

                ["(5, 0.1667)", "(8, 0.250)", "(11, 0.333)"], # tuples for Ds and ts
                #["(5, 0.1667)"],
                #[5, 8, 11], # Ds : stack diameter
                #[0.1667, 0.250, 0.333], # ts : stack thickness
                #[0.1667], # ts : stack thickness

                
                [30, 35, 40, 45, 50],  # L : length of the radiation and convection section
                #[40],

                [8, 10, 12, 14, 16],  # Npasses : # of passes
                #[8],

                [10, 12, 14, 16, 18],  # Ntceil : # of tubes in the ceiling
                #[18],

                [8, 9, 10, 11, 12],  # Nrconv : # of rows of finnes tubes in the convection section
                #[8],
 
                [8, 9, 10, 11, 12],  # Nprad : # of tubes per pass in the ceiling and side walls of the radiation section
                #[12],

                [1, 2, 3, 4], #Npconv : # of tubes per pass per row in the convection section
                #[1],

                [50, 60, 70, 80], #Hs : stack height
                #[50],

                [1.80, 1.85, 1.90, 1.95],  # Rpr : tube pitch ratio of the radiation section
                #[1.90],

                [1.55, 1.60, 1.65], # Rph : Transverse tube pitch ratio (horizontal) of the convection section
                #[1.60],

                [1.45]  # Rpv : Longitudinal pitch ratio of the convection section

            ],

        },

        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # minimum and maximums
            'HW_Min': 1,        # H/W min
            'HW_Max': 1.5,      # H/W max
            'LW_Min': 1.8,      # L/W min
            'LW_Max': 3,        # L/W max
            'BOX_Min': 3.5,     # Boxsize min
            'BOX_Max': 4.5,     # Boxsize max
            'G_Min': 0.3,       # mass flux of gases min
            'G_Max': 0.4,       # mass flux of gases max
            'Tfb_Min': 932,     # Tfb min
            'Tfb_Max': 1652,    # Tfb max
            'Voil_tube_Max': 6, # maximum velocity of tube oil
            'Pd_tube_Max':5760, # maximum pressure drop for tube

            # Oil parameters
            'Moil': 357000/3600,    # oil mass flowrate (lb/s)
            'rho_oil': 44.3594,     # oil density (lb/ft3)
            'mu_oil': 0.00522,      # oil viscosity (lb/ft s)
            'Cp_oil': 0.43,         # oil heat capacity (Btu/lb F)
            'k_oil': 0.0000193,     # Thermal conductivity of oil (Btu/ft s F)
            'Pr_oil': 16.1,         # Prandtl number
            'To_oil': 675,          # outlet temperature of oil (F)
            'Ti_oil': 380,          # inlet temperature of oil (F)
            'Enthoil_c1': 0.0004208148, # parameters for enthalpy of oil
            'Enthoil_c2': 0.2679048,    
            'Enthoil_c3': 110.4305,     
                                    # inlet enthalpy of oil = Enthoil_c1*Ti_oil^2 + Enthoil_c2*Ti_oil + Enthoil_c3
                                    # outlet enthalpy of oil = Enthoil_c1*To_oil^2 + Enthoil_c2*To_oil + Enthoil_c3
            'ks': 9.25/3600,        # conductivity of pipe wall (Btu/s ft F)
            'rf_oil': 20.4417482,   # fouling factor of the oil stream (s ft2 F/ Btu)


            # Gas parameters
            'hgr': 7/3600,              # gas side heat transfer coefficientin the radiations section  (Btu/s ft2 F)
            'h_methane': 32179.73655,   # enthalpy of formarion of methane(btu/mol)
            'sigma': 1.714e-9/3600,     # (Btu/s ft2 R)
            'Pr_gas': 0.74,             # Prandtk number of gas
            'rf_gas': 18.0091802,       # fouling factor of the flue gas (s ft2 F/ Btu)
            'k_fin': 0.0073075,         # thermal conductivity of fin (Btu/s ft F)
            'excess_air': 15,           # excess air
                                        # PartPres_CO2_H2O =(2/3)* (0.29067-0.0029654*excess_air +2.72e-5*power(excess_air,2)-1.175e-7*power(excess_air,3))
            'Tflame': 3394.544,         # flame temeprature (F)
            'hflame': 1046.3261178,     # enthalpy of flame (Btu/lb)
            'rho_gas': 0.017167689,     # gas density (lb/ft3)
            'mu_gas': 0.0000325233,     # gas viscosity (lb/ft s)        

            # Parameters and coefficients
            'e_c1': -9.61e-05,  # for emissivity equation
            'e_c2': 0.116,
            'e_c3': -0.008,
            'e_c4': 0.339,
            'f_c1': 0.325,      # for exchange factor equation
            'f_c2': 0.215,
            'f_c3': -0.073,
            'f_c4': 0.07,
            'f_c5': -0.049,
            'f_c6': 0.594,

            # Problem
            'pk1': 0.4572,          # unexposed portion of the tubes
            'Flux_Max': 12000/3600,  # 12000/3600, maximum flux (Btu/s ft2)
            'Flux_Min': 10000/3600,  # 10000/3600, minimum flux (Btu/s ft2)
            'percent_loss_Rad' : 0.02,
            'percent_loss_Conv': 0.02,
            'T_outside': 77,        # outside temperature
            'tf': 0.00905,          # fin thinkness [ft]
            'lf': 0.0833,           # fin height [ft]
            'Nf': 48,               # number of fins per unit length

            # Cost parameters
            'R_uni' : 170,          # unitary cost of radiant section
            'C_uni' : 100,          # unitary cost of convection section
            'S_uni' : 111.002,      # unitary cost of stack (carbon steel)
            'O_uni' : 0.043,        # unitary cost of fuel
            'CRF'   : 0.18,         # capital recovery cost
            'OT'    : 8000*3600,    # plant operating time
            'FK1'   : 5000,         
            'FK2'   : 50, 
            'LHV'   : 21500         # lower heating value
        }
    },

########################################################################
}

# endregion

######################################################################################################################
######################################################################################################################

