from Common.Stream import Stream
from Common.Stream import ThermoBackend

class HEX_Tho_Tco:
    

    def HEX_Tho_Tco(self,m_p):

        # ==================================================================
        # TEMPERATURE SPECIFICATION
        # ==================================================================

        if m_p['Outlet_Temperature_Spec'] == 'cold':

            # Tco is specified by the user.
            # Tho must be calculated.

            if m_p['Property_Source'] == 'CoolProp':

                # ----------------------------------------------------------
                # Calculate inlet stream enthalpies using CoolProp
                # ----------------------------------------------------------

                hot_stream_in = Stream(
                    composition=m_p['hot_composition'],
                    P=m_p['hot_pressure'],
                    T=m_p['Thi'] + 273.15,
                    mass_flow=m_p['mh'],
                    backend=ThermoBackend.HEOS,
                )

                cold_stream_in = Stream(
                    composition=m_p['cold_composition'],
                    P=m_p['cold_pressure'],
                    T=m_p['Tci'] + 273.15,
                    mass_flow=m_p['mc'],
                    backend=ThermoBackend.HEOS,
                )

                cold_stream_out = Stream(
                    composition=m_p['cold_composition'],
                    P=m_p['cold_pressure'],
                    T=m_p['Tco'] + 273.15,
                    mass_flow=m_p['mc'],
                    backend=ThermoBackend.HEOS,
                )

                # ----------------------------------------------------------
                # Energy balance using enthalpy
                # ----------------------------------------------------------

                Qc = m_p['mc'] * (
                    cold_stream_out.enthalpy_mass
                    - cold_stream_in.enthalpy_mass
                )

                h_hot_out = (
                    hot_stream_in.enthalpy_mass
                    - Qc / m_p['mh']
                )

                # ----------------------------------------------------------
                # Calculate Tho from hot outlet enthalpy
                # ----------------------------------------------------------

                hot_stream_out = Stream.from_PH(
                    composition=m_p['hot_composition'],
                    P=m_p['hot_pressure'],
                    H=h_hot_out,
                    mass_flow=m_p['mh'],
                    backend=ThermoBackend.HEOS,
                )

                m_p['Tho'] = hot_stream_out.T - 273.15
                print(f'>>>>>> Hot out temperature calculated with Property_Source set as CoolProp: {m_p['Tho']}')

            elif m_p['Property_Source'] == 'User':

                # ----------------------------------------------------------
                # Calculate Tho using inlet hot-stream Cp
                # ----------------------------------------------------------

                Qc = (
                    m_p['mc']
                    * m_p['Cpc']
                    * (m_p['Tco'] - m_p['Tci'])
                )

                m_p['Tho'] = (
                    m_p['Thi']
                    - Qc / (m_p['mh'] * m_p['Cph'])
                )
                print(f'>>>>>> Hot out temperature calculated with Property_Source set as User: {m_p['Tho']}')


        elif m_p['Outlet_Temperature_Spec'] == 'hot':

            # Tho is specified by the user.
            # Tco must be calculated.

            if m_p['Property_Source'] == 'CoolProp':

                # ----------------------------------------------------------
                # Calculate inlet stream enthalpies using CoolProp
                # ----------------------------------------------------------

                hot_stream_in = Stream(
                    composition=m_p['hot_composition'],
                    P=m_p['hot_pressure'],
                    T=m_p['Thi'] + 273.15,
                    mass_flow=m_p['mh'],
                    backend=ThermoBackend.HEOS,
                )

                hot_stream_out = Stream(
                    composition=m_p['hot_composition'],
                    P=m_p['hot_pressure'],
                    T=m_p['Tho'] + 273.15,
                    mass_flow=m_p['mh'],
                    backend=ThermoBackend.HEOS,
                )

                cold_stream_in = Stream(
                    composition=m_p['cold_composition'],
                    P=m_p['cold_pressure'],
                    T=m_p['Tci'] + 273.15,
                    mass_flow=m_p['mc'],
                    backend=ThermoBackend.HEOS,
                )

                # ----------------------------------------------------------
                # Energy balance using enthalpy
                # ----------------------------------------------------------

                Qh = m_p['mh'] * (
                    hot_stream_in.enthalpy_mass
                    - hot_stream_out.enthalpy_mass
                )

                h_cold_out = (
                    cold_stream_in.enthalpy_mass
                    + Qh / m_p['mc']
                )

                # ----------------------------------------------------------
                # Calculate Tco from cold outlet enthalpy
                # ----------------------------------------------------------


                cold_stream_out = Stream.from_PH(
                    composition=m_p['cold_composition'],
                    P=m_p['cold_pressure'],
                    H=h_cold_out,
                    mass_flow=m_p['mc'],
                    backend=ThermoBackend.HEOS,
                )

                m_p['Tco'] = cold_stream_out.T - 273.15
                print(f'>>>>>> Cold out temperature calculated with Property_Source set as CoolProp: {m_p['Tco']}')



            elif m_p['Property_Source'] == 'User':

                # ----------------------------------------------------------
                # Calculate Tco using inlet cold-stream Cp
                # ----------------------------------------------------------

                Qh = (
                    m_p['mh']
                    * m_p['Cph']
                    * (m_p['Thi'] - m_p['Tho'])
                )

                m_p['Tco'] = (
                    m_p['Tci']
                    + Qh / (m_p['mc'] * m_p['Cpc'])
                )

                print(f'>>>>>> Cold out temperature calculated with Property_Source set as User: {m_p['Tco']}')


        else:

            raise ValueError(
                f"Invalid Outlet_Temperature_Spec "
                f"'{m_p['Outlet_Temperature_Spec']}'. "
                f"Expected 'cold' or 'hot'."
            )


        # ==================================================================
        # PROPERTY SOURCE
        # ==================================================================

        if m_p['Property_Source'] == 'CoolProp':

            # ==================================================================
            # HOT STREAM - INLET
            # ==================================================================

            hot_stream_in = Stream(
                composition=m_p['hot_composition'],
                P=m_p['hot_pressure'],
                T=m_p['Thi'] + 273.15,
                mass_flow=m_p['mh'],
                backend=ThermoBackend.HEOS,
            )

            # ==================================================================
            # HOT STREAM - OUTLET
            # ==================================================================

            hot_stream_out = Stream(
                composition=m_p['hot_composition'],
                P=m_p['hot_pressure'],
                T=m_p['Tho'] + 273.15,
                mass_flow=m_p['mh'],
                backend=ThermoBackend.HEOS,
            )

            # ==================================================================
            # COLD STREAM - INLET
            # ==================================================================

            cold_stream_in = Stream(
                composition=m_p['cold_composition'],
                P=m_p['cold_pressure'],
                T=m_p['Tci'] + 273.15,
                mass_flow=m_p['mc'],
                backend=ThermoBackend.HEOS,
            )

            # ==================================================================
            # COLD STREAM - OUTLET
            # ==================================================================

            cold_stream_out = Stream(
                composition=m_p['cold_composition'],
                P=m_p['cold_pressure'],
                T=m_p['Tco'] + 273.15,
                mass_flow=m_p['mc'],
                backend=ThermoBackend.HEOS,
            )

            # ==================================================================
            # Store Streams
            # ==================================================================

            m_p['hot_stream_in'] = hot_stream_in
            m_p['hot_stream_out'] = hot_stream_out

            m_p['cold_stream_in'] = cold_stream_in
            m_p['cold_stream_out'] = cold_stream_out

            # ==================================================================
            # Legacy parameters - INLET STREAMS
            # ==================================================================

            m_p['mh'] = hot_stream_in.mass_flow
            m_p['roh'] = hot_stream_in.density_mass
            m_p['Cph'] = hot_stream_in.cp_mass
            m_p['mih'] = hot_stream_in.viscosity
            m_p['kh'] = hot_stream_in.conductivity

            m_p['mc'] = cold_stream_in.mass_flow
            m_p['roc'] = cold_stream_in.density_mass
            m_p['Cpc'] = cold_stream_in.cp_mass
            m_p['mic'] = cold_stream_in.viscosity
            m_p['kc'] = cold_stream_in.conductivity

            # ==================================================================
            # Outlet stream properties
            # ==================================================================

            m_p['roh_out'] = hot_stream_out.density_mass
            m_p['Cph_out'] = hot_stream_out.cp_mass
            m_p['mih_out'] = hot_stream_out.viscosity
            m_p['kh_out'] = hot_stream_out.conductivity

            m_p['roc_out'] = cold_stream_out.density_mass
            m_p['Cpc_out'] = cold_stream_out.cp_mass
            m_p['mic_out'] = cold_stream_out.viscosity
            m_p['kc_out'] = cold_stream_out.conductivity

            # ==================================================================
            # Enthalpies
            # ==================================================================

            m_p['hh_in'] = hot_stream_in.enthalpy_mass
            m_p['hh_out'] = hot_stream_out.enthalpy_mass

            m_p['hc_in'] = cold_stream_in.enthalpy_mass
            m_p['hc_out'] = cold_stream_out.enthalpy_mass


        elif m_p['Property_Source'] == 'User':

            # ==================================================================
            # User-defined properties
            # ==================================================================

            # Properties are already provided in m_p.
            # No CoolProp calculation is required.

            pass

        return m_p

