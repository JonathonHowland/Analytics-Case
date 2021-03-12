#File for data cleaning

import pandas as pd
import numpy as np


#Import sheets from Excel as dataframes

UNPop = pd.read_excel("Reshaped.xlsx", sheet_name="UN Population")
IHMEPop = pd.read_excel("Reshaped.xlsx", sheet_name="IHME Population")
WHO = pd.read_excel("Reshaped.xlsx", sheet_name="WHO Vaccine Coverage")
IHMEVacc = pd.read_excel("Reshaped.xlsx", sheet_name="IHME Vaccine Coverage")
Vacc = pd.read_excel("Reshaped.xlsx", sheet_name="Vaccine_Impact_Data")

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

#Now, for years less than or equal to 

print(IHMEVacc.head(100))

#Write the dataframes to a new Excel workbook

with pd.ExcelWriter("BACCFromPython.xlsx") as writer:
    UNPop.to_excel(writer, sheet_name="UN Population", index=False)
    IHMEPop.to_excel(writer, sheet_name="IHME Population", index=False)
    WHO.to_excel(writer, sheet_name="WHO Vaccine Coverage", index=False)
    IHMEVacc.to_excel(writer, sheet_name="IHME Vaccine Coverage", index=False)
    Vacc.to_excel(writer, sheet_name="Vaccine_Impact_Data", index=False)
