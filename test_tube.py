from Common.Standards.Tubes.Tube import Common_Tube


tube = 'D7M_OD19.05_BWG18_t1.245'

try:

    dte, bwg, thk = Common_Tube.get_tube_values(tube)

    print("Tube:", tube)
    print("dte:", dte)
    print("bwg:", bwg)
    print("thk:", thk)

except Exception as e:

    print("ERROR:", e)

