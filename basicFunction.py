# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 10:17:47 2022

@author: HP
"""
import os
import pandas as pd
def readCSV(nameFile):
    path = "..\input"
    fullPath = os.path.join(path, nameFile)
    dfCSV = pd.read_csv(fullPath,
                                  delimiter=",",
                                  header=0
                                  )
    return dfCSV