class HEX_Allocation:

    def allocation(self, m_p):

        if m_p['yfluid'] == 'cold_stream':

            m_p['mt'] = m_p['mc']
            m_p['rot'] = m_p['roc']
            m_p['Cpt'] = m_p['Cpc']
            m_p['mit'] = m_p['mic']
            m_p['kt'] = m_p['kc']
            m_p['Rft'] = m_p['Rfc']
            m_p['DPtdisp'] = m_p['DPcdisp']

            m_p['ms'] = m_p['mh']
            m_p['ros'] = m_p['roh']
            m_p['Cps'] = m_p['Cph']
            m_p['mis'] = m_p['mih']
            m_p['ks'] = m_p['kh']
            m_p['Rfs'] = m_p['Rfh']
            m_p['DPsdisp'] = m_p['DPhdisp']

        elif m_p['yfluid'] == 'hot_stream':

            m_p['mt'] = m_p['mh']
            m_p['rot'] = m_p['roh']
            m_p['Cpt'] = m_p['Cph']
            m_p['mit'] = m_p['mih']
            m_p['kt'] = m_p['kh']
            m_p['Rft'] = m_p['Rfh']
            m_p['DPtdisp'] = m_p['DPhdisp']

            m_p['ms'] = m_p['mc']
            m_p['ros'] = m_p['roc']
            m_p['Cps'] = m_p['Cpc']
            m_p['mis'] = m_p['mic']
            m_p['ks'] = m_p['kc']
            m_p['Rfs'] = m_p['Rfc']
            m_p['DPsdisp'] = m_p['DPcdisp']

        return m_p