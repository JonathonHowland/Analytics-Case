#File for data analysis

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats.distributions import chi2
import matplotlib.pyplot as plt


#Import sheets from Excel as dataframes

UNPop = pd.read_excel("BACCFromPython.xlsx", sheet_name="UN Population")
IHMEPop = pd.read_excel("BACCFromPython.xlsx", sheet_name="IHME Population")
WHO = pd.read_excel("BACCFromPython.xlsx", sheet_name="WHO Vaccine Coverage")
IHMEVacc = pd.read_excel("BACCFromPython.xlsx", sheet_name="IHME Vaccine Coverage")
Vacc = pd.read_excel("BACCFromPython.xlsx", sheet_name="Vaccine_Impact_Data")

#Rename age_group_name from IHME to age_group
#IHMEPop = IHMEPop.rename(columns={"age_group_name": "age_group"})

PopTot = pd.merge(UNPop, IHMEPop, how="inner", left_on=["iso_code", "age_group", "year"], right_on=["iso_code", "age_group_name", "year"])

#Merge datasets
VaccTot = pd.merge(WHO, IHMEVacc, how="inner", left_on=["iso_code", "year"], right_on=["iso_code", "year"])

xList = ["mcv2_coverage", "Hib3_coverage", "pcv3_coverage", "rota_coverage"]

XList = ["MCV2", "Hib3", "PCV3", "Rota"]

#Look at the averages between the two datasets
for i in range(len(xList)):
    xString = xList[i] + "_x"
    yString = xList[i] + "_y"
    VaccTot[xList[i]] = 0.5*(VaccTot[xString] + VaccTot[yString])
    #Drop the old columns
    VaccTot = VaccTot.drop(columns=[xString, yString])
                             
print(VaccTot)

print(VaccTot.columns)

#Find the average by iso_code
#VaccAvg = VaccTot.groupby(["iso_code"]).mean()
#print(VaccAvg)


#Merge the datasets
Final = pd.merge(VaccTot, Vacc, how="inner", left_on=["iso_code"], right_on=["country"])

print(Final)

print(Final.columns)

#Make a list of datasets (one for each vaccine)
Mcv2 = Final[Final["vaccine"]=="MCV2"]
Mcv2 = Mcv2.rename(columns={"mcv2_coverage": "coverage"})
Hib3 = Final[Final["vaccine"]=="Hib3"]
Hib2 = Hib3.rename(columns={"Hib3_coverage": "coverage"})
Pcv3 = Final[Final["vaccine"]=="PCV3"]
Pcv3 = Pcv3.rename(columns={"pcv3_coverage": "coverage"})
Rota = Final[Final["vaccine"]=="Rota"]
Rota = Rota.rename(columns={"rota_coverage": "coverage"})

dfList = [Mcv2, Hib3, Pcv3, Rota]

for df in dfList:
    print(df)
    print(df.columns)


    
