#File for data cleaning

import pandas as pd
import numpy as np


#Import sheets from Excel as dataframes

dfUNPop = pd.read_excel("BACCForPython.xlsx", sheet_name="UN Population")
dfIHMEPop = pd.read_excel("BACCForPython.xlsx", sheet_name="IHME Population")
dfWHO = pd.read_excel("BACCForPython.xlsx", sheet_name="WHO Vaccine Coverage")
dfIHMEVacc = pd.read_excel("BACCForPython.xlsx", sheet_name="IHME Vaccine Coverage")
dfVacc = pd.read_excel("BACCForPython.xlsx", sheet_name="Vaccine_Impact_Data")
