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
#with the true value

for i in range(len(IHMEPop)):
    if(np.isnan(IHMEPop["upper"][i])):
        IHMEPop["upper"][i] = IHMEPop["reference"][i]
    elif(np.isnan(IHMEPop["lower"][i])):
        IHMEPop["lower"][i] = IHMEPop["reference"][i]

#Remove "All Ages" from IHMEPop
IHMEPop = IHMEPop[~IHMEPop["age_group_name"].str.contains("All Ages")]

#Combine neonatals into one group
Young = IHMEPop[IHMEPop["age_group_name"].str.contains("Neo")]
YoungSum = Young.groupby(["iso_code", "year"]).sum()
YoungSum.insert(1, "age_group_name", "<1 year")

#Put that information back into the original dataframe
#and remove the neonatal categories
IHMEPop = IHMEPop[~IHMEPop["age_group_name"].str.contains("Neo")]
IHMEPop.append(YoungSum, sort=True)
IHMEPop.sort_values(by=["iso_code", "age_group_name", "year"])
IHMEPop.reindex()

#Use DTP3 for other vaccines
#First, replace the nulls in WHO with 0 to match IHMEVacc
WHO = WHO.fillna(0)

WHO[(WHO["coverage"]==0).any() and (WHO["vaccine"].str.contains("DTP3"))]["coverage"] = WHO[WHO["vaccine"].str.contains("DTP3")]["coverage"]

print(WHO[WHO["iso_code"].str.contains("AFG")])

#Write the dataframes to a new Excel workbook

with pd.ExcelWriter("BACCFromPython.xlsx") as writer:
    UNPop.to_excel(writer, sheet_name="UN Population", index=False)
    IHMEPop.to_excel(writer, sheet_name="IHME Population", index=False)
    WHO.to_excel(writer, sheet_name="WHO Vaccine Coverage", index=False)
    IHMEVacc.to_excel(writer, sheet_name="IHME Vaccine Coverage", index=False)
    Vacc.to_excel(writer, sheet_name="Vaccine_Impact_Data", index=False)
