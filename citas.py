# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 11:33:45 2022

@author: HP
"""
import tratamientoDatos as td
#from tratamientoDatos import readFile
import pandas as pd
import os
from tqdm import tqdm
from datetime import date

def main():
    fileName=input("Ingrese el nombre del archivo:")+".xlsx"
    df=td.readFile(fileName)
    
    
    #dfUpdated=dfDatos[~dfDatos.ruc.isin(dFilter.ruc)]
    df=df[(df["ok_A1"]=='NO') & (df ["excluir_A1"]=='NO') | (df["ok_A2"]=='NO') & (df ["excluir_A2"]=='NO')]
    #df=df[df["ok_A2"]=="NO"]
    #df=df[df["excluir_A2"]=="NO"]
    print(df)
    td.exportData(df, "ambosCualquiera")
    

if __name__ == "__main__":
    main()


