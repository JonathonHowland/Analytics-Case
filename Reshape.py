# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 13:38:27 2021

@author: brysonadcock22
"""
import pandas as pd
import numpy as np


#Import sheets from Excel as dataframes
UNPop = pd.read_excel("BACCForPython.xlsx", sheet_name="UN Population")
IHMEPop = pd.read_excel("BACCForPython.xlsx", sheet_name="IHME Population")
WHO = pd.read_excel("BACCForPython.xlsx", sheet_name="WHO Vaccine Coverage")
IHMEVacc = pd.read_excel("BACCForPython.xlsx", sheet_name="IHME Vaccine Coverage")
Vacc = pd.read_excel("BACCForPython.xlsx", sheet_name="Vaccine_Impact_Data")

#Create a new dataframe with just the iso_code and year to merge the vaccine coverages to
NewWHO = WHO.groupby(['iso_code','year']).size().reset_index().rename(columns={0:'count'})
NewWHO = NewWHO[['iso_code','year']]

#Create individual dataframes for each vaccine to make joining the data easier
dtp3_vac = WHO[WHO.vaccine == 'DTP3'].rename(columns={'coverage':'dtp3_coverage'}).drop('vaccine', axis=1)
mcv2_vac = WHO[WHO.vaccine == 'MCV2'].rename(columns={'coverage':'mcv2_coverage'}).drop('vaccine', axis=1)
hib3_vac = WHO[WHO.vaccine == 'Hib3'].rename(columns={'coverage':'Hib3_coverage'}).drop('vaccine', axis=1)
pcv3_vac = WHO[WHO.vaccine == 'PCV3'].rename(columns={'coverage':'pcv3_coverage'}).drop('vaccine', axis=1)
rota_vac = WHO[WHO.vaccine == 'RotaC'].rename(columns={'coverage':'rota_coverage'}).drop('vaccine', axis=1)

# Join the individual vaccine coverages to the matching iso_code and year
NewWHO = pd.merge(NewWHO, dtp3_vac,  how='inner', on=['iso_code','year'])
NewWHO = pd.merge(NewWHO, mcv2_vac,  how='inner', on=['iso_code','year'])
NewWHO = pd.merge(NewWHO, hib3_vac,  how='inner', on=['iso_code','year'])
NewWHO = pd.merge(NewWHO, pcv3_vac,  how='inner', on=['iso_code','year'])
NewWHO = pd.merge(NewWHO, rota_vac,  how='inner', on=['iso_code','year'])

NewWHO