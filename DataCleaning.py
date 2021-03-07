#File for data cleaning

import pandas as pd
import numpy as np


#Import sheets from Excel as dataframes

UNPop = pd.read_excel("BACCForPython.xlsx", sheet_name="UN Population")
IHMEPop = pd.read_excel("BACCForPython.xlsx", sheet_name="IHME Population")
WHO = pd.read_excel("BACCForPython.xlsx", sheet_name="WHO Vaccine Coverage")
IHMEVacc = pd.read_excel("BACCForPython.xlsx", sheet_name="IHME Vaccine Coverage")
Vacc = pd.read_excel("BACCForPython.xlsx", sheet_name="Vaccine_Impact_Data")

#Replace the null values in IHME Population's confidence intervals
#with the true value (only if both are null)

for i in range(len(IHMEPop)):
    if(np.isnan(IHMEPop["upper"][i]) and np.isnan(IHMEPop["lower"][i])):
        IHMEPop["upper"][i] = IHMEPop["reference"][i]
        IHMEPop["lower"][i] = IHMEPop["reference"][i]
        
#Write the dataframes to a new Excel workbook

with pd.ExcelWriter("BACCFromPython.xlsx") as writer:
    UNPop.to_excel(writer, sheet_name="UN Population", index=False)
    IHMEPop.to_excel(writer, sheet_name="IHME Population", index=False)
    WHO.to_excel(writer, sheet_name="WHO Vaccine Coverage", index=False)
    IHMEVacc.to_excel(writer, sheet_name="IHME Vaccine Coverage", index=False)
    Vacc.to_excel(writer, sheet_name="Vaccine_Impact_Data", index=False)
