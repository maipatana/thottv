import pandas as pd
import numpy as np
def materials_list(*args):
    MATLIST = [["Concrete",1.7, 2400, 0.92],
               ["Plaster",0.72, 1860, 0.84],
               ["Brick",0.473, 1600, 0.79]
              ]
    MATLIST = pd.DataFrame(MATLIST)
    MATLIST.columns = ["Material","Conductivity","Density","Specific Heat Capacity"]
    if args:
        if isinstance(args[0],(list,tuple)):
            return MATLIST[MATLIST["Material"].isin(*args)]
        else:
            return MATLIST[MATLIST["Material"].isin(args)]
    else:
        return MATLIST

if __name__ == "__main__":
    materials_list(*args)
