##################################################################################################################
# region Titles and Header
# Nature: Repository
# Methodology: Dictionary
##################################################################################################################
# VERSION        DATE            AUTHOR                    DESCRIPTION OF CHANGES MADE
#   0.0       17-Feb-2025        Diego Oliva               Kettle Examples Repository
#   0.1       08-May-2025        Gustavo Rabello           Kettle file revise to match article
#   0.2       18-May-2025        Gustavo Rabello           Addition of the remaining examples
##################################################################################################################
# INPUT: Setting of examples
##################################################################################################################
# INSTRUCTIONS
# Add Examples of Kettle in this file
##################################################################################################################

###################################################################################################################
# region Import Library
import copy
# endregion
###################################################################################################################

######################################## Kettle Reboiler - Sales et al 2021 #######################################

###################################################################################################################
# region Examples Description
'''
Example1:  Horizontal Shell and Tube from Sales et al, 2021
Example2:  Horizontal Shell and Tube from Sales et al, 2021
Example3:  Horizontal Shell and Tube from Sales et al, 2021
Example4:  Horizontal Shell and Tube from Sales et al, 2021
Example5:  Horizontal Shell and Tube from Sales et al, 2021
Example6:  Horizontal Shell and Tube from Sales et al, 2021
Example7:  Horizontal Shell and Tube from Sales et al, 2021
Example8:  Horizontal Shell and Tube from Sales et al, 2021
Example9:  Horizontal Shell and Tube from Sales et al, 2021
Example10:  Horizontal Shell and Tube from Sales et al, 2021


'''
# endregion
###################################################################################################################

###################################################################################################################
# region INPUT EXAMPLE 1 - KETTLE REBOILER

Example1 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'RTH',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discretized_Values_of_Variables': [
                


                
                [0.203, 0.254, 0.305, 0.337, 0.387, 0.438, 0.489, 0.540, 0.591, 0.635, 0.686, 0.737, 0.787, 0.838, 
                 0.889, 0.940, 0.991, 1.067, 1.143, 1.219, 1.295, 1.372, 1.448, 1.524],  # Ds (m)

                [0.01905, 0.0254, 0.03175, 0.03810, 0.05080],    # dte (m)

                [2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0960]  # L (m)
            ],

            'Selected_OF': ['Cost_OF','Area_OF'],
            
        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Example 1 from Sales et al 2021
            # Hot stream - Tube side
             'Tin_t': 190,       # Inlet temperature (°C)
            'Tout_t': 130,      # Outlet temperature (°C)
            'Rf_t': 0.0006,   # Fouling factor (m².°C/W)
            'rol_t': 913.4,     # Condensate density (kg/m³)
            'rov_t': 2.1,       # Steam density (kg/m³)
            'mil_t': 1.33e-3,   # Viscosity (Pa.s)
            'miv_t': 1.36e-5,   # Viscosity (Pa.s)
            'kl_t': 0.109,      # Thermal conductivity (W/(m.K))
            'Hvap_t': 2.148e6,    # Vaporization enthalpy (J/kg)
            'fluid_type': 1,     # 1 Oil ; 2 Steam
            'Cp_t':2.0505e3,

            # Cold stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 112,      # Inlet temperature (°C)
            'Tout_s':112,      # Outlet temperature (°C)
            'Rf_s': 0.0004,   # Fouling factor (m².°C/W)
            'Pc': 3800000,      # Critical pressure (Pa)
            'P_s': 1925000,     # Pressure (Pa)
            'Hvap_s': 233000,   # Vaporization enthalpy (J/kg)
            'Q2':1.59e6,        # Heat load if task = 2
            'Fv':0.2,
            'rol_s': 850,
            'rov_s': 5,
            'mil_s':2e-3,
            'miv_s': 3e-5,
            'kl_s': 0.15,
            'Cpl_s': 2000,



            # General data
            'thk': 0.00165,     # Tube thickness (m)
            'ktube': 45,        # Thermal conductivity of material (W/(m.°C))
            'Aexc': 0.1,        # Area excess (%)
            'g': 9.81,          # Gravity accelertion (m/s²)
            'BR': 0,          # Boiling range; difference between the dew and bubble points
            'hnc': 250,         # Contribution of the natural convection (W/(m²°C)) ,250 for hydrocarbons and 1000 for water
            'multiplier':1,     # multiplication of the original heat load value by three factors: 1, 2 and 4.
            'task':1,           # Shell-side fluid type

            # Bounds
            'dPt_disp': 70000, # Available pressure drop (Pa) ; 70kPa (Thermal oil) and 10kPa (Saturated steam)
            'Retmin': 10000,    # Minimum reynolds number for condensing stream(3380); 10000 if there is no fase change inside the tube
            'vtmax': 3,         # Maximum velocity (m/s); 3m/s (Thermal oil) and 25m/s (Saturated steam)
            'vtmin': 1,         # Minimum velocity (m/s) ; 1m/s (Thermal oil) and 0m/s (Saturated steam)
            'LBLD': 3,          # Tube length/shell diameter ratio LB
            'UBLD': 15          # Tube length/shell diameter ratio UB
        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

Example2 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'RTH',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discretized_Values_of_Variables': [
                


                [0.203, 0.254, 0.305, 0.337, 0.387, 0.438, 0.489, 0.540, 0.591, 0.635, 0.686, 0.737, 0.787, 0.838, 
                 0.889, 0.940, 0.991, 1.067, 1.143, 1.219, 1.295, 1.372, 1.448, 1.524],  # Ds (m)

                [0.01905, 0.0254, 0.03175, 0.03810, 0.05080],    # dte (m)

                [2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0960]  # L (m)

            ],

            'Selected_OF': ['Cost_OF','Area_OF'],
            
        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Example 2 from Sales et al 2021
            # Hot stream - Tube side
            'Tin_t': 190,       # Inlet temperature (°C)
            'Tout_t': 130,      # Outlet temperature (°C)
            'Rf_t': 0.0006,   # Fouling factor (m².°C/W)
            'rol_t': 913.4,     # Condensate density (kg/m³)
            'rov_t': 2.1,       # Steam density (kg/m³)
            'mil_t': 1.33e-3,   # Viscosity (Pa.s)
            'miv_t': 1.36e-5,   # Viscosity (Pa.s)
            'kl_t': 0.109,      # Thermal conductivity (W/(m.K))
            'Hvap_t': 2.148e6,    # Vaporization enthalpy (J/kg)
            'fluid_type': 1,     # 1 Oil ; 2 Steam
            'Cp_t':2.0505e3,

            # Cold stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 112,      # Inlet temperature (°C)
            'Tout_s':112,      # Outlet temperature (°C)
            'Rf_s': 0.0004,   # Fouling factor (m².°C/W)
            'Pc': 3800000,      # Critical pressure (Pa)
            'P_s': 1925000,     # Pressure (Pa)
            'Hvap_s': 233000,   # Vaporization enthalpy (J/kg)
            'Q2':1.59e6,        # Heat load if task = 2
            'Fv':0.2,
            'rol_s': 850,
            'rov_s': 5,
            'mil_s':2e-3,
            'miv_s': 3e-5,
            'kl_s': 0.15,
            'Cpl_s': 2000,

            # General data
            'thk': 0.00165,     # Tube thickness (m)
            'ktube': 45,        # Thermal conductivity of material (W/(m.°C))
            'Aexc': 0.1,        # Area excess (%)
            'g': 9.81,          # Gravity accelertion (m/s²)
            'BR': 0,          # Boiling range; difference between the dew and bubble points
            'hnc': 250,         # Contribution of the natural convection (W/(m²°C)) ,250 for hydrocarbons and 1000 for water
            'multiplier':2,     # multiplication of the original heat load value by three factors: 1, 2 and 4.
            'task':1,           # Shell-side fluid type

            # Bounds
            'dPt_disp': 70000, # Available pressure drop (Pa) ; 70kPa (Thermal oil) and 10kPa (Saturated steam)
            'Retmin': 10000,    # Minimum reynolds number for condensing stream(3380); 10000 if there is no fase change inside the tube
            'vtmax': 3,         # Maximum velocity (m/s); 3m/s (Thermal oil) and 25m/s (Saturated steam)
            'vtmin': 1,         # Minimum velocity (m/s) ; 1m/s (Thermal oil) and 0m/s (Saturated steam)
            'LBLD': 3,          # Tube length/shell diameter ratio LB
            'UBLD': 15          # Tube length/shell diameter ratio UB
        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

Example3 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'RTH',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discretized_Values_of_Variables': [
                


                [0.203, 0.254, 0.305, 0.337, 0.387, 0.438, 0.489, 0.540, 0.591, 0.635, 0.686, 0.737, 0.787, 0.838, 
                 0.889, 0.940, 0.991, 1.067, 1.143, 1.219, 1.295, 1.372, 1.448, 1.524],  # Ds (m)

                [0.01905, 0.0254, 0.03175, 0.03810, 0.05080],    # dte (m)

                [2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0960]  # L (m)

            ],

            'Selected_OF': ['Cost_OF','Area_OF'],
            
        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Example 3 from Sales et al 2021
            # Hot stream - Tube side
            'Tin_t': 190,       # Inlet temperature (°C)
            'Tout_t': 130,      # Outlet temperature (°C)
            'Rf_t': 0.0006,   # Fouling factor (m².°C/W)
            'rol_t': 913.4,     # Condensate density (kg/m³)
            'rov_t': 2.1,       # Steam density (kg/m³)
            'mil_t': 1.33e-3,   # Viscosity (Pa.s)
            'miv_t': 1.36e-5,   # Viscosity (Pa.s)
            'kl_t': 0.109,      # Thermal conductivity (W/(m.K))
            'Hvap_t': 2.148e6,    # Vaporization enthalpy (J/kg)
            'fluid_type': 1,     # 1 Oil ; 2 Steam
            'Cp_t':2.0505e3,
            


            # Cold stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 94.7,      # Inlet temperature (°C)
            'Tout_s':94.7,      # Outlet temperature (°C)
            'Rf_s': 0.000088,   # Fouling factor (m².°C/W)
            'Pc': 3829000,      # Critical pressure (Pa)
            'P_s': 1724000,     # Pressure (Pa)
            'Hvap_s': 233000,   # Vaporization enthalpy (J/kg)
            'Q2':1.59e6,        # Heat load if task = 2
            'Fv':0.3,
            'rol_s': 850,
            'rov_s': 5,
            'mil_s':2e-3,
            'miv_s': 3e-5,
            'kl_s': 0.15,
            'Cpl_s': 2000,

            # General data
            'thk': 0.00211,     # Tube thickness (m)
            'ktube': 45,        # Thermal conductivity of material (W/(m.°C))
            'Aexc': 0.1,        # Area excess (%)
            'g': 9.81,          # Gravity accelertion (m/s²)
            'BR': 4.4,          # Boiling range; difference between the dew and bubble points
            'hnc': 250,         # Contribution of the natural convection (W/(m²°C)) ,250 for hydrocarbons and 1000 for water
            'multiplier':1,     # multiplication of the original heat load value by three factors: 1, 2 and 4.
            'task':2,           # Shell-side fluid type

            # Bounds
            'dPt_disp': 70000, # Available pressure drop (Pa) ; 70kPa (Thermal oil) and 10kPa (Saturated steam)
            'Retmin': 10000,    # Minimum reynolds number for condensing stream(3380); 10000 if there is no fase change inside the tube
            'vtmax': 3,         # Maximum velocity (m/s); 3m/s (Thermal oil) and 25m/s (Saturated steam)
            'vtmin': 1,         # Minimum velocity (m/s) ; 1m/s (Thermal oil) and 0m/s (Saturated steam)
            'LBLD': 3,          # Tube length/shell diameter ratio LB
            'UBLD': 15          # Tube length/shell diameter ratio UB
        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

Example4 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'RTH',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discretized_Values_of_Variables': [
                


                [0.203, 0.254, 0.305, 0.337, 0.387, 0.438, 0.489, 0.540, 0.591, 0.635, 0.686, 0.737, 0.787, 0.838, 
                 0.889, 0.940, 0.991, 1.067, 1.143, 1.219, 1.295, 1.372, 1.448, 1.524],  # Ds (m)

                [0.01905, 0.0254, 0.03175, 0.03810, 0.05080],    # dte (m)

                [2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0960]  # L (m)

            ],

            'Selected_OF': ['Cost_OF','Area_OF'],
            
        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Example 4 from Sales et al 2021
            # Hot stream - Tube side
             'Tin_t': 190,       # Inlet temperature (°C)
            'Tout_t': 130,      # Outlet temperature (°C)
            'Rf_t': 0.0006,   # Fouling factor (m².°C/W)
            'rol_t': 913.4,     # Condensate density (kg/m³)
            'rov_t': 2.1,       # Steam density (kg/m³)
            'mil_t': 1.33e-3,   # Viscosity (Pa.s)
            'miv_t': 1.36e-5,   # Viscosity (Pa.s)
            'kl_t': 0.109,      # Thermal conductivity (W/(m.K))
            'Hvap_t': 2.148e6,    # Vaporization enthalpy (J/kg)
            'fluid_type': 1,     # 1 Oil ; 2 Steam
            'Cp_t':2.0505e3,


            # Cold stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 94.7,      # Inlet temperature (°C)
            'Tout_s':94.7,      # Outlet temperature (°C)
            'Rf_s': 0.000088,   # Fouling factor (m².°C/W)
            'Pc': 3829000,      # Critical pressure (Pa)
            'P_s': 1724000,     # Pressure (Pa)
            'Hvap_s': 233000,   # Vaporization enthalpy (J/kg)
            'Q2':1.59e6,        # Heat load if task = 2
            'Fv':0.2,
            'rol_s': 850,
            'rov_s': 5,
            'mil_s':2e-3,
            'miv_s': 3e-5,
            'kl_s': 0.15,
            'Cpl_s': 2000,

            # General data
            'thk': 0.00211,     # Tube thickness (m)
            'ktube': 45,        # Thermal conductivity of material (W/(m.°C))
            'Aexc': 0.1,        # Area excess (%)
            'g': 9.81,          # Gravity accelertion (m/s²)
            'BR': 4.4,          # Boiling range; difference between the dew and bubble points
            'hnc': 250,         # Contribution of the natural convection (W/(m²°C)) ,250 for hydrocarbons and 1000 for water
            'multiplier':2,     # multiplication of the original heat load value by three factors: 1, 2 and 4.
            'task':2,           # Shell-side fluid type

            # Bounds
            'dPt_disp': 70000, # Available pressure drop (Pa) ; 70kPa (Thermal oil) and 10kPa (Saturated steam)
            'Retmin': 10000,    # Minimum reynolds number for condensing stream(3380); 10000 if there is no fase change inside the tube
            'vtmax': 3,         # Maximum velocity (m/s); 3m/s (Thermal oil) and 25m/s (Saturated steam)
            'vtmin': 1,         # Minimum velocity (m/s) ; 1m/s (Thermal oil) and 0m/s (Saturated steam)
            'LBLD': 3,          # Tube length/shell diameter ratio LB
            'UBLD': 15          # Tube length/shell diameter ratio UB
        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

Example5 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'RTH',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discretized_Values_of_Variables': [
                


                [0.203, 0.254, 0.305, 0.337, 0.387, 0.438, 0.489, 0.540, 0.591, 0.635, 0.686, 0.737, 0.787, 0.838, 
                 0.889, 0.940, 0.991, 1.067, 1.143, 1.219, 1.295, 1.372, 1.448, 1.524],  # Ds (m)

                [0.01905, 0.0254, 0.03175, 0.03810, 0.05080],    # dte (m)

                [2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0960]  # L (m)

            ],

            'Selected_OF': ['Cost_OF','Area_OF'],
            
        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Example 5 from Sales et al 2021
            # Hot stream - Tube side
            'Tin_t': 190,       # Inlet temperature (°C)
            'Tout_t': 130,      # Outlet temperature (°C)
            'Rf_t': 0.0006,   # Fouling factor (m².°C/W)
            'rol_t': 913.4,     # Condensate density (kg/m³)
            'rov_t': 2.1,       # Steam density (kg/m³)
            'mil_t': 1.33e-3,   # Viscosity (Pa.s)
            'miv_t': 1.36e-5,   # Viscosity (Pa.s)
            'kl_t': 0.109,      # Thermal conductivity (W/(m.K))
            'Hvap_t': 2.148e6,    # Vaporization enthalpy (J/kg)
            'fluid_type': 1,     # 1 Oil ; 2 Steam
            'Cp_t':2.0505e3,


            # Cold stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 94.7,      # Inlet temperature (°C)
            'Tout_s':94.7,      # Outlet temperature (°C)
            'Rf_s': 0.000088,   # Fouling factor (m².°C/W)
            'Pc': 3829000,      # Critical pressure (Pa)
            'P_s': 1724000,     # Pressure (Pa)
            'Hvap_s': 233000,   # Vaporization enthalpy (J/kg)
            'Q2':1.59e6,        # Heat load if task = 2
            'Fv':0.2,
            'rol_s': 850,
            'rov_s': 5,
            'mil_s':2e-3,
            'miv_s': 3e-5,
            'kl_s': 0.15,
            'Cpl_s': 2000,

            # General data
            'thk': 0.00211,     # Tube thickness (m)
            'ktube': 45,        # Thermal conductivity of material (W/(m.°C))
            'Aexc': 0.1,        # Area excess (%)
            'g': 9.81,          # Gravity accelertion (m/s²)
            'BR': 4.4,          # Boiling range; difference between the dew and bubble points
            'hnc': 250,         # Contribution of the natural convection (W/(m²°C)) ,250 for hydrocarbons and 1000 for water
            'multiplier':4,     # multiplication of the original heat load value by three factors: 1, 2 and 4.
            'task':2,           # Shell-side fluid type

            # Bounds
            'dPt_disp': 70000, # Available pressure drop (Pa) ; 70kPa (Thermal oil) and 10kPa (Saturated steam)
            'Retmin': 10000,    # Minimum reynolds number for condensing stream(3380); 10000 if there is no fase change inside the tube
            'vtmax': 3,         # Maximum velocity (m/s); 3m/s (Thermal oil) and 25m/s (Saturated steam)
            'vtmin': 1,         # Minimum velocity (m/s) ; 1m/s (Thermal oil) and 0m/s (Saturated steam)
            'LBLD': 3,          # Tube length/shell diameter ratio LB
            'UBLD': 15          # Tube length/shell diameter ratio UB
        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

Example6 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'RTH',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discretized_Values_of_Variables': [
                


                [0.203, 0.254, 0.305, 0.337, 0.387, 0.438, 0.489, 0.540, 0.591, 0.635, 0.686, 0.737, 0.787, 0.838, 
                 0.889, 0.940, 0.991, 1.067, 1.143, 1.219, 1.295, 1.372, 1.448, 1.524],  # Ds (m)

                [0.01905, 0.0254, 0.03175, 0.03810, 0.05080],    # dte (m)

                [2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0960]  # L (m)

            ],

            'Selected_OF': ['Cost_OF','Area_OF'],
            
        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Example 6 from Sales et al 2021
            # Hot stream - Tube side
             'Tin_t': 143,       # Inlet temperature (°C)
            'Tout_t': 143,      # Outlet temperature (°C)
            'Rf_t': 0.000088,   # Fouling factor (m².°C/W)
            'rol_t': 922.8,     # Condensate density (kg/m³)
            'rov_t': 2.1,       # Steam density (kg/m³)
            'mil_t': 1.91e-4,   # Viscosity (Pa.s)
            'miv_t': 1.36e-5,   # Viscosity (Pa.s)
            'kl_t': 0.688,      # Thermal conductivity (W/(m.K))
            'Hvap_t': 2.148e6,    # Vaporization enthalpy (J/kg)
            'fluid_type': 2,     # 1 Oil ; 2 Steam
            'Cp_t':2.0505e3,

            # Cold stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 112,      # Inlet temperature (°C)
            'Tout_s':112,      # Outlet temperature (°C)
            'Rf_s': 0.0004,   # Fouling factor (m².°C/W)
            'Pc': 3800000,      # Critical pressure (Pa)
            'P_s': 1925000,     # Pressure (Pa)
            'Hvap_s': 233000,   # Vaporization enthalpy (J/kg)
            'Q2':1.59e6,        # Heat load if task = 2
            'Fv':0.2,
            'rol_s': 850,
            'rov_s': 5,
            'mil_s':2e-3,
            'miv_s': 3e-5,
            'kl_s': 0.15,
            'Cpl_s': 2000,

            # General data
            'thk': 0.00165,     # Tube thickness (m)
            'ktube': 45,        # Thermal conductivity of material (W/(m.°C))
            'Aexc': 0.1,        # Area excess (%)
            'g': 9.81,          # Gravity accelertion (m/s²)
            'BR': 0,          # Boiling range; difference between the dew and bubble points
            'hnc': 250,         # Contribution of the natural convection (W/(m²°C)) ,250 for hydrocarbons and 1000 for water
            'multiplier':1,     # multiplication of the original heat load value by three factors: 1, 2 and 4.
            'task':1,           # Shell-side fluid type

            # Bounds
            'dPt_disp': 10000, # Available pressure drop (Pa) ; 70kPa (Thermal oil) and 10kPa (Saturated steam)
            'Retmin': 3380,    # Minimum reynolds number for condensing stream(3380); 10000 if there is no fase change inside the tube
            'vtmax': 25,         # Maximum velocity (m/s); 3m/s (Thermal oil) and 25m/s (Saturated steam)
            'vtmin': 0,         # Minimum velocity (m/s) ; 1m/s (Thermal oil) and 0m/s (Saturated steam)
            'LBLD': 3,          # Tube length/shell diameter ratio LB
            'UBLD': 15          # Tube length/shell diameter ratio UB
        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

Example7 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'RTH',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discretized_Values_of_Variables': [
                


                [0.203, 0.254, 0.305, 0.337, 0.387, 0.438, 0.489, 0.540, 0.591, 0.635, 0.686, 0.737, 0.787, 0.838, 
                 0.889, 0.940, 0.991, 1.067, 1.143, 1.219, 1.295, 1.372, 1.448, 1.524],  # Ds (m)

                [0.01905, 0.0254, 0.03175, 0.03810, 0.05080],    # dte (m)

                [2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0960]  # L (m)

            ],

            'Selected_OF': ['Cost_OF','Area_OF'],
            
        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Example 7 from Sales et al 2021
            # Hot stream - Tube side
             'Tin_t': 143,       # Inlet temperature (°C)
            'Tout_t': 143,      # Outlet temperature (°C)
            'Rf_t': 0.000088,   # Fouling factor (m².°C/W)
            'rol_t': 922.8,     # Condensate density (kg/m³)
            'rov_t': 2.1,       # Steam density (kg/m³)
            'mil_t': 1.91e-4,   # Viscosity (Pa.s)
            'miv_t': 1.36e-5,   # Viscosity (Pa.s)
            'kl_t': 0.688,      # Thermal conductivity (W/(m.K))
            'Hvap_t': 2.148e6,    # Vaporization enthalpy (J/kg)
            'fluid_type': 2,     # 1 Oil ; 2 Steam
            'Cp_t':2.0505e3,

            # Cold stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 112,      # Inlet temperature (°C)
            'Tout_s':112,      # Outlet temperature (°C)
            'Rf_s': 0.0004,   # Fouling factor (m².°C/W)
            'Pc': 3800000,      # Critical pressure (Pa)
            'P_s': 1925000,     # Pressure (Pa)
            'Hvap_s': 233000,   # Vaporization enthalpy (J/kg)
            'Q2':1.59e6,        # Heat load if task = 2
            'Fv':0.2,
            'rol_s': 850,
            'rov_s': 5,
            'mil_s':2e-3,
            'miv_s': 3e-5,
            'kl_s': 0.15,
            'Cpl_s': 2000,

            # General data
            'thk': 0.00165,     # Tube thickness (m)
            'ktube': 45,        # Thermal conductivity of material (W/(m.°C))
            'Aexc': 0.1,        # Area excess (%)
            'g': 9.81,          # Gravity accelertion (m/s²)
            'BR': 0,          # Boiling range; difference between the dew and bubble points
            'hnc': 250,         # Contribution of the natural convection (W/(m²°C)) ,250 for hydrocarbons and 1000 for water
            'multiplier':2,     # multiplication of the original heat load value by three factors: 1, 2 and 4.
            'task':1,           # Shell-side fluid type

            # Bounds
            'dPt_disp': 10000, # Available pressure drop (Pa) ; 70kPa (Thermal oil) and 10kPa (Saturated steam)
            'Retmin': 3380,    # Minimum reynolds number for condensing stream(3380); 10000 if there is no fase change inside the tube
            'vtmax': 25,         # Maximum velocity (m/s); 3m/s (Thermal oil) and 25m/s (Saturated steam)
            'vtmin': 0,         # Minimum velocity (m/s) ; 1m/s (Thermal oil) and 0m/s (Saturated steam)
            'LBLD': 3,          # Tube length/shell diameter ratio LB
            'UBLD': 15          # Tube length/shell diameter ratio UB
        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

Example8 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'RTH',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discretized_Values_of_Variables': [
                


                [0.203, 0.254, 0.305, 0.337, 0.387, 0.438, 0.489, 0.540, 0.591, 0.635, 0.686, 0.737, 0.787, 0.838, 
                 0.889, 0.940, 0.991, 1.067, 1.143, 1.219, 1.295, 1.372, 1.448, 1.524],  # Ds (m)

                [0.01905, 0.0254, 0.03175, 0.03810, 0.05080],    # dte (m)

                [2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0960]  # L (m)

            ],

            'Selected_OF': ['Cost_OF','Area_OF'],
            
        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Example 8 from Sales et al 2021
            # Hot stream - Tube side
             'Tin_t': 143,       # Inlet temperature (°C)
            'Tout_t': 143,      # Outlet temperature (°C)
            'Rf_t': 0.000088,   # Fouling factor (m².°C/W)
            'rol_t': 922.8,     # Condensate density (kg/m³)
            'rov_t': 2.1,       # Steam density (kg/m³)
            'mil_t': 1.91e-4,   # Viscosity (Pa.s)
            'miv_t': 1.36e-5,   # Viscosity (Pa.s)
            'kl_t': 0.688,      # Thermal conductivity (W/(m.K))
            'Hvap_t': 2.148e6,    # Vaporization enthalpy (J/kg)
            'fluid_type': 2,     # 1 Oil ; 2 Steam
            'Cp_t':2.0505e3,

            # Cold stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 94.7,      # Inlet temperature (°C)
            'Tout_s':94.7,      # Outlet temperature (°C)
            'Rf_s': 0.000088,   # Fouling factor (m².°C/W)
            'Pc': 3829000,      # Critical pressure (Pa)
            'P_s': 1724000,     # Pressure (Pa)
            'Hvap_s': 233000,   # Vaporization enthalpy (J/kg)
            'Q2':1.59e6,        # Heat load if task = 2
            'Fv':0.2,
            'rol_s': 850,
            'rov_s': 5,
            'mil_s':2e-3,
            'miv_s': 3e-5,
            'kl_s': 0.15,
            'Cpl_s': 2000,

            # General data
            'thk': 0.00211,     # Tube thickness (m)
            'ktube': 45,        # Thermal conductivity of material (W/(m.°C))
            'Aexc': 0.1,        # Area excess (%)
            'g': 9.81,          # Gravity accelertion (m/s²)
            'BR': 4.4,          # Boiling range; difference between the dew and bubble points
            'hnc': 250,         # Contribution of the natural convection (W/(m²°C)) ,250 for hydrocarbons and 1000 for water
            'multiplier':1,     # multiplication of the original heat load value by three factors: 1, 2 and 4.
            'task':2,           # Shell-side fluid type

            # Bounds
            'dPt_disp': 10000, # Available pressure drop (Pa) ; 70kPa (Thermal oil) and 10kPa (Saturated steam)
            'Retmin': 3380,    # Minimum reynolds number for condensing stream(3380); 10000 if there is no fase change inside the tube
            'vtmax': 25,         # Maximum velocity (m/s); 3m/s (Thermal oil) and 25m/s (Saturated steam)
            'vtmin': 0,         # Minimum velocity (m/s) ; 1m/s (Thermal oil) and 0m/s (Saturated steam)
            'LBLD': 3,          # Tube length/shell diameter ratio LB
            'UBLD': 15          # Tube length/shell diameter ratio UB
        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

Example9 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'RTH',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discretized_Values_of_Variables': [
                


                [0.203, 0.254, 0.305, 0.337, 0.387, 0.438, 0.489, 0.540, 0.591, 0.635, 0.686, 0.737, 0.787, 0.838, 
                 0.889, 0.940, 0.991, 1.067, 1.143, 1.219, 1.295, 1.372, 1.448, 1.524],  # Ds (m)

                [0.01905, 0.0254, 0.03175, 0.03810, 0.05080],    # dte (m)

                [2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0960]  # L (m)

            ],

            'Selected_OF': ['Cost_OF','Area_OF'],
            
        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Example 9 from Sales et al 2021
            # Hot stream - Tube side
             'Tin_t': 143,       # Inlet temperature (°C)
            'Tout_t': 143,      # Outlet temperature (°C)
            'Rf_t': 0.000088,   # Fouling factor (m².°C/W)
            'rol_t': 922.8,     # Condensate density (kg/m³)
            'rov_t': 2.1,       # Steam density (kg/m³)
            'mil_t': 1.91e-4,   # Viscosity (Pa.s)
            'miv_t': 1.36e-5,   # Viscosity (Pa.s)
            'kl_t': 0.688,      # Thermal conductivity (W/(m.K))
            'Hvap_t': 2.148e6,    # Vaporization enthalpy (J/kg)
            'fluid_type': 2,     # 1 Oil ; 2 Steam
            'Cp_t':2.0505e3,

            # Cold stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 94.7,      # Inlet temperature (°C)
            'Tout_s':94.7,      # Outlet temperature (°C)
            'Rf_s': 0.000088,   # Fouling factor (m².°C/W)
            'Pc': 3829000,      # Critical pressure (Pa)
            'P_s': 1724000,     # Pressure (Pa)
            'Hvap_s': 233000,   # Vaporization enthalpy (J/kg)
            'Q2':1.59e6,        # Heat load if task = 2
            'Fv':0.2,
            'rol_s': 850,
            'rov_s': 5,
            'mil_s':2e-3,
            'miv_s': 3e-5,
            'kl_s': 0.15,
            'Cpl_s': 2000,

            # General data
            'thk': 0.00211,     # Tube thickness (m)
            'ktube': 45,        # Thermal conductivity of material (W/(m.°C))
            'Aexc': 0.1,        # Area excess (%)
            'g': 9.81,          # Gravity accelertion (m/s²)
            'BR': 4.4,          # Boiling range; difference between the dew and bubble points
            'hnc': 250,         # Contribution of the natural convection (W/(m²°C)) ,250 for hydrocarbons and 1000 for water
            'multiplier':2,     # multiplication of the original heat load value by three factors: 1, 2 and 4.
            'task':2,           # Shell-side fluid type

            # Bounds
            'dPt_disp': 10000, # Available pressure drop (Pa) ; 70kPa (Thermal oil) and 10kPa (Saturated steam)
            'Retmin': 3380,    # Minimum reynolds number for condensing stream(3380); 10000 if there is no fase change inside the tube
            'vtmax': 25,         # Maximum velocity (m/s); 3m/s (Thermal oil) and 25m/s (Saturated steam)
            'vtmin': 0,         # Minimum velocity (m/s) ; 1m/s (Thermal oil) and 0m/s (Saturated steam)
            'LBLD': 3,          # Tube length/shell diameter ratio LB
            'UBLD': 15          # Tube length/shell diameter ratio UB
        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

Example10 = {

    'Number_of_Equipment': 1,
    # If there is only 1 piece of equipment, add the information as 'Equipment1'.

    'Equipment1': {

        'Model_Declarations': {
            
            # Type of Equipment - Models_List
            'Type_Equipment': 'RTH',

            # Discretized_Values_of_Variables
            # Values of the discrete variables (All variables declared in 'List_of_Variables' must be given values)
            'Discretized_Values_of_Variables': [
                


                [0.203, 0.254, 0.305, 0.337, 0.387, 0.438, 0.489, 0.540, 0.591, 0.635, 0.686, 0.737, 0.787, 0.838, 
                 0.889, 0.940, 0.991, 1.067, 1.143, 1.219, 1.295, 1.372, 1.448, 1.524],  # Ds (m)

                [0.01905, 0.0254, 0.03175, 0.03810, 0.05080],    # dte (m)

                [2, 4, 6],  # Npt

                [1.25, 1.33, 1.50],  # rp

                [1, 2],  # lay 1 = Square e 2 = Triangle

                [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0960]  # L (m)

            ],

            'Selected_OF': ['Cost_OF','Area_OF'],
            
        },
        # These Problem_Parameters are used for the computation of Constraint and Objective function values
        #                                                                      in "Constraints_and_OF.py"
        'Model_Parameters': {

            # Example 10 from Sales et al 2021
            # Hot stream - Tube side
             'Tin_t': 143,       # Inlet temperature (°C)
            'Tout_t': 143,      # Outlet temperature (°C)
            'Rf_t': 0.000088,   # Fouling factor (m².°C/W)
            'rol_t': 922.8,     # Condensate density (kg/m³)
            'rov_t': 2.1,       # Steam density (kg/m³)
            'mil_t': 1.91e-4,   # Viscosity (Pa.s)
            'miv_t': 1.36e-5,   # Viscosity (Pa.s)
            'kl_t': 0.688,      # Thermal conductivity (W/(m.K))
            'Hvap_t': 2.148e6,    # Vaporization enthalpy (J/kg)
            'fluid_type': 2,     # 1 Oil ; 2 Steam
            'Cp_t':2.0505e3,

            # Cold stream - Shell side
            'm_s': 5.8,         # Flow rate (kg/s)
            'Tin_s': 94.7,      # Inlet temperature (°C)
            'Tout_s':94.7,      # Outlet temperature (°C)
            'Rf_s': 0.000088,   # Fouling factor (m².°C/W)
            'Pc': 3829000,      # Critical pressure (Pa)
            'P_s': 1724000,     # Pressure (Pa)
            'Hvap_s': 233000,   # Vaporization enthalpy (J/kg)
            'Q2':1.59e6,        # Heat load if task = 2
            'Fv':0.2,
            'rol_s': 850,
            'rov_s': 5,
            'mil_s':2e-3,
            'miv_s': 3e-5,
            'kl_s': 0.15,
            'Cpl_s': 2000,

            # General data
            'thk': 0.00211,     # Tube thickness (m)
            'ktube': 45,        # Thermal conductivity of material (W/(m.°C))
            'Aexc': 0.1,        # Area excess (%)
            'g': 9.81,          # Gravity accelertion (m/s²)
            'BR': 4.4,          # Boiling range; difference between the dew and bubble points
            'hnc': 250,         # Contribution of the natural convection (W/(m²°C)) ,250 for hydrocarbons and 1000 for water
            'multiplier':4,     # multiplication of the original heat load value by three factors: 1, 2 and 4.
            'task':2,           # Shell-side fluid type

            # Bounds
            'dPt_disp': 10000, # Available pressure drop (Pa) ; 70kPa (Thermal oil) and 10kPa (Saturated steam)
            'Retmin': 3380,    # Minimum reynolds number for condensing stream(3380); 10000 if there is no fase change inside the tube
            'vtmax': 25,         # Maximum velocity (m/s); 3m/s (Thermal oil) and 25m/s (Saturated steam)
            'vtmin': 0,         # Minimum velocity (m/s) ; 1m/s (Thermal oil) and 0m/s (Saturated steam)
            'LBLD': 3,          # Tube length/shell diameter ratio LB
            'UBLD': 15          # Tube length/shell diameter ratio UB
        }
    },

}

# endregion
###################################################################################################################
###################################################################################################################

##################################################################################################################

