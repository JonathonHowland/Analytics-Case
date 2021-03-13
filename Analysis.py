#File for data analysis

import pandas as pd
import numpy as np
from scipy.stats.distributions import chi2


#Import sheets from Excel as dataframes

UNPop = pd.read_excel("BACCFromPython.xlsx", sheet_name="UN Population")
IHMEPop = pd.read_excel("BACCFromPython.xlsx", sheet_name="IHME Population")
WHO = pd.read_excel("BACCFromPython.xlsx", sheet_name="WHO Vaccine Coverage")
IHMEVacc = pd.read_excel("BACCFromPython.xlsx", sheet_name="IHME Vaccine Coverage")
Vacc = pd.read_excel("BACCFromPython.xlsx", sheet_name="Vaccine_Impact_Data")

#Rename age_group_name from IHME to age_group
#IHMEPop = IHMEPop.rename(columns={"age_group_name": "age_group"})

print(IHMEPop.head(100))

PopTot = pd.merge(UNPop, IHMEPop, how="inner", left_on=["iso_code", "age_group", "year"], right_on=["iso_code", "age_group_name", "year"])

print(PopTot)

#Perform the chi^2 test

R = PopTot["population"].sum()
S = PopTot["reference"].sum()
N = len(PopTot)
chisq = 0

for i in range(N):
    chisq += (np.sqrt(S/R)*PopTot["population"][i] - np.sqrt(R/S)*PopTot["reference"][i])**2/(PopTot["population"][i] + PopTot["reference"][i])

chiScaled = chisq/N

print("Chi^2 = {}, scaled Chi^2 = {}".format(chisq, chiScaled))

pVal = chi2.sf(chisq, N-1)

print("P-value = {}".format(pVal))
