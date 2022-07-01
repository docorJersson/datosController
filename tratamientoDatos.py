# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 14:45:32 2022

@author: HP
"""
import pandas as pd
import os
from tqdm import tqdm
from datetime import date
import time
import mixDataCIIU_Contact as mD
    
def loading():
    for i in tqdm(range(200)):
        time.sleep(0.001)
        
    
def readFile(fileName):
    index_columns=[0,3,4,7,10,24,25,29,30]
    path="..\input"   
    fullPath= os.path.join(path,fileName)
    print("Archivo reconocido, leyendo---")
    df=pd.read_excel(fullPath,
                     sheet_name="Hoja1",
                     header=0,
                     usecols=index_columns
                     )
    return df

def filters(df,mainFilter):
    if mainFilter.upper()=="OKA1":
        df=df[(df["ok_A1"]=='NO') & (df ["excluir_A1"]=='NO')]
    elif mainFilter.upper()=="AMBOS":
        df=df[df["ok_A1"]=="NO"]
        df=df[df["excluir_A1"]=="NO"]
        df=df[df["ok_A2"]=="NO"]
        df=df[df["excluir_A2"]=="NO"]
    elif mainFilter.upper()=="ALTERNADO":
        df=df[(df["ok_A1"]=='NO') & (df ["excluir_A1"]=='NO') | (df["ok_A2"]=='NO') & (df ["excluir_A2"]=='NO')]
    else:
        df=df[(df["ok_A2"]=='NO') & (df ["excluir_A2"]=='NO')]
        
    df=df[~df["NumTelef3"].isin(["-"]) & df["NumTelef3"].notnull()]
    print("Aplicando filtros ....")
    return df


def getContrisUpdateds(df,dFilter):
    
    dfUpdated=df[~df.ruc.isin(dFilter.ruc)]
    return dfUpdated


def contriSolo(dfUpdated):
    print(dfFileGeneral)
    fileName = input("Ingrese el nombre del archivo DE DATOS:")+".csv"
    dfCIIU_Contacto=mD.readCIIU_DATOS(fileName)
    dfCIIU_Contacto=dfCIIU_Contacto[dfCIIU_Contacto["¿Actualizó datos de contacto?"]!="SI"]
    
    #los que ya lo hicieron
    dfShare=dfUpdated[dfUpdated.ruc.isin(dfCIIU_Contacto.ruc)]
    
    #los pendientes
    dfFaltan=dfCIIU_Contacto[~dfCIIU_Contacto.ruc.isin(dfUpdated.ruc)]
    

    #los que ya lo hicieron con colaboradores    
    dfWithCola=pd.merge(dfShare,dfCIIU_Contacto[["ruc","Nombre de colaborador","Title"]],on="ruc",how="left")
    
    #que no están en la intendencia 
    dfNotIntedencia=dfCIIU_Contacto[~dfCIIU_Contacto.ruc.isin(dfFileGeneral.ruc)]
    print(dfNotIntedencia)
    exportData(dfNotIntedencia,"noIntendencia")
    exportData(dfWithCola, "contrisSolo")
    exportData(dfFaltan, "nuevoCIIU_DATOS")


def view(df):
    df_cols=df.columns
    for col in df_cols:
        print(df[col].head())
    
def exportData(df,tipoExporta):
    df.to_excel(f"..\output\{date.today()}_{tipoExporta}.xlsx",
              header=True,
              index=False)
    print("\n Archivo procesado listo ")


def citas(dfUpdated,mainFilter):
    citasFile=input("Ingrese el nombre del archivo de citas:")+".csv"
    path = "..\input"
    fullPath = os.path.join(path, citasFile)
    dfCitas= pd.read_csv(fullPath,
                                  delimiter=",",
                                  header=0
                                  )
     
    if mainFilter.upper()=="OKA1":
        dfCitas=dfCitas[dfCitas["Motivo de cita"]!="Datos de contacto"]

    if mainFilter.upper()=="OKA2":
        dfCitas=dfCitas[dfCitas["Motivo de cita"]!="Actualización de CIIU"]
   #verificar cuando sea alternando porque tenemos que evalualr variables
    dfContriUpda=dfCitas[dfCitas.RUC.isin(dfUpdated.ruc)]
    exportData(dfContriUpda,"citadosActualizados")



def main():
    fileName=input("Ingrese el nombre del archivo:")+".xlsx"
    global dfFileGeneral
    dfFileGeneral=readFile(fileName)
    mainFilter=input('¿Cuál será el indicador princial,OKA1, OKA2, AMBOS O ALTERNAOD:')
    dFilter=filters(dfFileGeneral,mainFilter)
    dfUpdated=getContrisUpdateds(dfFileGeneral,dFilter)
    print(dfFileGeneral)
    contriSolo(dfUpdated)
    citas(dfUpdated,mainFilter)
    

    #view(df)
    #loading()
    exportData(dFilter,"faltantes")
    
dfFileGeneral=None
    
if __name__=="__main__":
   main()
