#File for data cleaning

import pandas as pd
import numpy as np


#Import sheets from Excel as dataframes

UNPop = pd.read_excel("Reshaped.xlsx", sheet_name="UN Population")
IHMEPopDirty = pd.read_excel("Reshaped.xlsx", sheet_name="IHME Population")
WHO = pd.read_excel("Reshaped.xlsx", sheet_name="WHO Vaccine Coverage")
IHMEVacc = pd.read_excel("Reshaped.xlsx", sheet_name="IHME Vaccine Coverage")
Vacc = pd.read_excel("Reshaped.xlsx", sheet_name="Vaccine_Impact_Data")

#Replace the null values in IHME Population's confidence intervals
#with the true value
for i in range(len(IHMEPopDirty)):
    if(np.isnan(IHMEPopDirty["upper"][i])):
        IHMEPopDirty["upper"][i] = IHMEPopDirty["reference"][i]
    if(np.isnan(IHMEPopDirty["lower"][i])):
        IHMEPopDirty["lower"][i] = IHMEPopDirty["reference"][i]

#Remove "All Ages" from IHMEPop
IHMEPopDirty = IHMEPopDirty[~IHMEPopDirty["age_group_name"].str.contains("All Ages")]

#Combine neonatals into one group
Young = IHMEPopDirty[IHMEPopDirty["age_group_name"].str.contains("Neo")]
YoungSum = Young.groupby(["iso_code", "year"]).sum()
YoungSum.insert(0, "age_group_name", "<1 year")
YoungSum = YoungSum.reset_index()

#Put that information back into the original dataframe
#and remove the neonatal categories
IHMEPopNoBabies = IHMEPopDirty[~IHMEPopDirty["age_group_name"].str.contains("Neo")]
IHMEPopClean = IHMEPopNoBabies.append(YoungSum, sort = True, ignore_index = True)
IHMEPopClean = IHMEPopClean.sort_values(by=["iso_code", "year","age_group_name"])
IHMEPop = IHMEPopClean.reindex()

#Use DTP3 for other vaccines
#We can directly use fillna() for the WHO dataset

WHO["mcv2_coverage"] = WHO["mcv2_coverage"].fillna(WHO["dtp3_coverage"])
WHO["Hib3_coverage"] = WHO["Hib3_coverage"].fillna(WHO["dtp3_coverage"])
WHO["pcv3_coverage"] = WHO["pcv3_coverage"].fillna(WHO["dtp3_coverage"])
WHO["rota_coverage"] = WHO["rota_coverage"].fillna(WHO["dtp3_coverage"])

print(WHO.head(100))

#First, let's remove the values where coverage/reference is 0 and the interval is not

IHMEVacc["mcv2_better"].mask(IHMEVacc["mcv2_coverage"].eq(0), 0, inplace=True)
IHMEVacc["mcv2_worse"].mask(IHMEVacc["mcv2_coverage"].eq(0), 0, inplace=True)
IHMEVacc["Hib3_better"].mask(IHMEVacc["Hib3_coverage"].eq(0), 0, inplace=True)
IHMEVacc["Hib3_worse"].mask(IHMEVacc["Hib3_coverage"].eq(0), 0, inplace=True)
IHMEVacc["pcv3_better"].mask(IHMEVacc["pcv3_coverage"].eq(0), 0, inplace=True)
IHMEVacc["pcv3_better"].mask(IHMEVacc["pcv3_coverage"].eq(0), 0, inplace=True)
IHMEVacc["rota_better"].mask(IHMEVacc["rota_coverage"].eq(0), 0, inplace=True)
IHMEVacc["rota_worse"].mask(IHMEVacc["rota_coverage"].eq(0), 0, inplace=True)

#We'll use replace() to replace 0s in IHMEVacc

IHMEVacc["mcv2_coverage"] = IHMEVacc["mcv2_coverage"].replace(0, IHMEVacc["dtp3_coverage"])
IHMEVacc["Hib3_coverage"] = IHMEVacc["Hib3_coverage"].replace(0, IHMEVacc["dtp3_coverage"])
IHMEVacc["pcv3_coverage"] = IHMEVacc["pcv3_coverage"].replace(0, IHMEVacc["dtp3_coverage"])
IHMEVacc["rota_coverage"] = IHMEVacc["rota_coverage"].replace(0, IHMEVacc["dtp3_coverage"])

#Now, for years less than or equal to 2018, set intervals to 0 width

IHMEVacc["mcv2_better"] = np.where(IHMEVacc["year"] < 2019, IHMEVacc["mcv2_coverage"], IHMEVacc["mcv2_better"]) 
IHMEVacc["mcv2_worse"] = np.where(IHMEVacc["year"] < 2019, IHMEVacc["mcv2_coverage"], IHMEVacc["mcv2_worse"])
IHMEVacc["Hib3_better"] = np.where(IHMEVacc["year"] < 2019, IHMEVacc["Hib3_coverage"], IHMEVacc["Hib3_better"]) 
IHMEVacc["Hib3_worse"] = np.where(IHMEVacc["year"] < 2019, IHMEVacc["Hib3_coverage"], IHMEVacc["Hib3_worse"])
IHMEVacc["pcv3_better"] = np.where(IHMEVacc["year"] < 2019, IHMEVacc["pcv3_coverage"], IHMEVacc["pcv3_better"]) 
IHMEVacc["pcv3_worse"] = np.where(IHMEVacc["year"] < 2019, IHMEVacc["pcv3_coverage"], IHMEVacc["pcv3_worse"])
IHMEVacc["rota_better"] = np.where(IHMEVacc["year"] < 2019, IHMEVacc["rota_coverage"], IHMEVacc["rota_better"]) 
IHMEVacc["rota_worse"] = np.where(IHMEVacc["year"] < 2019, IHMEVacc["rota_coverage"], IHMEVacc["rota_worse"])

print(IHMEVacc.head(100))

#Finally, let's drop the rows where there are null values
UNPop = UNPop.dropna()
IHMEPop = IHMEPop.dropna()
WHO = WHO.dropna()
IHMEVacc = IHMEVacc.dropna()

#Write the dataframes to a new Excel workbook

with pd.ExcelWriter("BACCFromPython.xlsx") as writer:
    UNPop.to_excel(writer, sheet_name="UN Population", index=False)
    IHMEPop.to_excel(writer, sheet_name="IHME Population", index=False)
    WHO.to_excel(writer, sheet_name="WHO Vaccine Coverage", index=False)
    IHMEVacc.to_excel(writer, sheet_name="IHME Vaccine Coverage", index=False)
    Vacc.to_excel(writer, sheet_name="Vaccine_Impact_Data", index=False)