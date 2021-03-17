#File for data analysis

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats.distributions import chi2
from scipy.optimize import linprog
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

PopTot["AvgPop"] = 0.5*(PopTot["population"] + PopTot["reference"])
PopTot = PopTot.drop(columns=["population", "reference"])
VeryYoung = PopTot[PopTot["age_group"]=="<1 year"]
Young = PopTot[(PopTot["age_group"]=="<1 year") | (PopTot["age_group"]=="1 to 4")]
Young = Young.groupby(by=["iso_code", "year"], as_index=False).sum()
Young["YoungPop"] = Young["AvgPop"]
Young = Young.drop(["AvgPop", "upper", "lower"], axis=1)
#print(Young)
PopTot = PopTot.groupby(by=["iso_code","year"], as_index=False).sum()
PopTot = PopTot.drop(["upper", "lower"], axis=1)
#print(PopTot)

#Merge populations
PopTot = pd.merge(PopTot, Young, how="inner", on=["iso_code", "year"])
print(PopTot)

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
Final = pd.merge(Final, PopTot, how="inner", on=["iso_code", "year"])
VeryYoung = pd.merge(VeryYoung, Final, how="inner", on=["iso_code", "year"])
Mcv2Young = VeryYoung[VeryYoung["vaccine"]==XList[0]]
Hib3Young = VeryYoung[VeryYoung["vaccine"]==XList[1]]
Pcv3Young = VeryYoung[VeryYoung["vaccine"]==XList[2]]
RotaYoung = VeryYoung[VeryYoung["vaccine"]==XList[3]]
VaccList=[Mcv2Young, Hib3Young, Pcv3Young, RotaYoung]

print(Final)

print(Final.columns)

#Make a list of datasets (one for each vaccine)
Mcv2 = Final[Final["vaccine"]=="MCV2"]
Mcv2 = Mcv2.rename(columns={"mcv2_coverage": "coverage"})
Hib3 = Final[Final["vaccine"]=="Hib3"]
Hib3 = Hib3.rename(columns={"Hib3_coverage": "coverage"})
Pcv3 = Final[Final["vaccine"]=="PCV3"]
Pcv3 = Pcv3.rename(columns={"pcv3_coverage": "coverage"})
Rota = Final[Final["vaccine"]=="Rota"]
Rota = Rota.rename(columns={"rota_coverage": "coverage"})

#Set the herd immunity threshold and number of vaccines
H = 0.5
n= 1.0e7

#Do it for MCV2 first
df = Mcv2

#df.to_excel("Test.xlsx", index=False)

#Here's the code to do it for all the vaccines

dfList = [Mcv2, Hib3, Pcv3, Rota]
Result=[]
i=0

for df in dfList:
    df["FVP"] = df["coverage"]*df["AvgPop"]
    for year in range(2022, 2031):
        #Constant to multiply our number of vaccines by
        c = -df["dalys_averted_rate"].to_numpy()
        #Upper boundary condition (maximum number of vaccines to give)
        A = np.ones(shape=[1,len(c)])
        b_ub = H*df["AvgPop"].to_numpy()
        #Boundary conditions. Don't add more vaccines unless under herd immunity threshold,
        #younger than 5, and in the correct year
        lb = df["FVP"].to_numpy()
        ub = np.where((df["FVP"]/df["AvgPop"]<H) & (df["year"]==year), df["FVP"]+df["YoungPop"], df["FVP"])
        bounds = list(zip(lb, ub))
        #We start where we were
        x0 = df["FVP"].to_numpy()
        #Our maximum number of FVPs is equal to our current number plus our vaccine number
        N = n + np.sum(x0)

        #Run the optimization
        res = linprog(c=c, A_ub=A, b_ub=N, method="revised simplex",bounds=bounds, x0=x0)

        print(res)

        print(np.sum(res.x), np.shape(res.x))

        df[str(year)] = res.x - df["FVP"]

        df[str(year)] = df[str(year)].round()

        df["YoungPop"] = df["YoungPop"].reindex() - (res.x - df["FVP"].reindex()) - np.where(VaccList[i]["year"] == (year-4), VaccList[i]["AvgPop_x"], 0) + np.where(VaccList[i]["year"] == (year+1), VaccList[i]["AvgPop_x"], 0)

        df["FVP"] = res.x
    Result.append(df)
        
with pd.ExcelWriter("Recommendation.xlsx") as writer:
    for i in range(len( Result)):
        Result[i].to_excel(writer, sheet_name=str(i), index=False)
