#librerÃ­a para el tratamiento de datos
import pandas as pd
import os
from tqdm import tqdm
from datetime import date
import time
def main():
    df=readFile()
    df=filters(df)
    #view(df)
    #loading()
    exportData(df)
    
def loading():
    for i in tqdm(range(200)):
        time.sleep(0.001)
        
    
def readFile():
    index_columns=[0,3,4,7,10,24,25,29,30]
    path="..\input"
    fileName=input("Ingrese el nombre del archivo:")+".xlsx"
    fullPath= os.path.join(path,fileName)
    print("Archivo reconocido, leyendo---")
    df=pd.read_excel(fullPath,
                     sheet_name="Hoja1",
                     header=0,
                     usecols=index_columns)

    return df

def filters(df):
    mainFilter=input("¿Cuál será el indicador princial,OKA1 o OKA2:")
    if mainFilter.upper()=="OKA1":
        df=df[df["ok_A1"]=="NO"]
        df=df[df["excluir_A1"]=="NO"]
    else:
        df=df[df["ok_A2"]=="NO"]
        df=df[df["excluir_A2"]=="NO"]
    df=df[~df["NumTelef3"].isin(["-"]) & df["NumTelef3"].notnull()]
    print("Aplicando filtros ....")
    return df

def view(df):
    df_cols=df.columns
    for col in df_cols:
        print(df[col].head())
    
def exportData(df):
    df.to_excel(f"..\output\{date.today()}_faltantes.xlsx",
              header=True,
              index=False)
    print("\n Archivo procesado listo ")

if __name__=="__main__":
    main()