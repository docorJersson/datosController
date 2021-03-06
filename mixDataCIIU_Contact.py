# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 21:17:26 2022

@author: HP
""" 

import pandas as pd
from datetime import date
import os
from numpy import array
import random
#desabilita el aviso de la reasignacion
pd.options.mode.chained_assignment = None 

def main():
    dfFaltantes = readExcels()
    fileName = input("Ingrese el nombre del archivo:")+".csv"
    dfCIIU_Contacto=readCIIU_DATOS(fileName)
    dfFaltantes=selection(dfFaltantes, dfCIIU_Contacto)
    dfReasignado= reasignando(dfFaltantes, dfCIIU_Contacto)
    dfColaborador=colaboradores()
    dfReasignado=asignar(dfReasignado, dfColaborador)
    exportar(dfReasignado)


def readExcels():

    dfFaltantes = pd.read_excel(f"..\output\{date.today()}_faltantes.xlsx",
                                sheet_name="Sheet1",
                                header=0)
    return dfFaltantes

def readCIIU_DATOS(fileName):
    path = "..\input"
    fullPath = os.path.join(path, fileName)
    dfCIIU_Contacto = pd.read_csv(fullPath,
                                  delimiter=",",
                                  header=0
                                  )
    return dfCIIU_Contacto


def selection(dfFaltantes, dfCIIU_Contacto):
    # le digo que me muestre los valores cuales el ruc no este en el dataframe de dfCIIU_CONTACTO
    dfFaltantes = dfFaltantes[~dfFaltantes["ruc"].isin(dfCIIU_Contacto['ruc'])]
    return dfFaltantes

def reasignando(dfFaltantes, dfCIIU_Contacto):
    numberRow = len(dfFaltantes)
    if numberRow>0:
        print(f"\nSe encontrĂ³ {numberRow} nuevos contribuyentes")
        numerUltimo=int(dfCIIU_Contacto.Title.max())+1
        datos = [range(numerUltimo,numerUltimo+numberRow),
                 dfFaltantes.univ,
                 dfFaltantes.ruc,
                 dfFaltantes.nombre,
                 ["No"]*numberRow,
                 [""]*numberRow,
                 [""]*numberRow,
                 dfFaltantes.correo1,
                 dfFaltantes.NumTelef3,
                 ["No"]*numberRow,
                 ["Ninguno designado"]*numberRow,
                 [""]*numberRow,
                 [""]*numberRow,
                 dfFaltantes.ok_A1,
                 ["Pendiente"]*numberRow,
                 [""]*numberRow,  # reportar
                 [""]*numberRow,  # esquela
                 [""]*numberRow,  # motivo no contacto
                 [""]*numberRow,  # fecha
                 [""]*numberRow,  # observaciones
                 [""]*numberRow,
                 [""]*numberRow]
    
        colums_name = dfCIIU_Contacto.columns.to_numpy(copy=True)
        list_tuples = list(zip(colums_name, datos))
        data_dicctionary = dict(list_tuples)
        dfReasignado = pd.DataFrame(data_dicctionary)
        return dfReasignado

def exportar(dfReasignado):
    dfReasignado.to_excel(f"..\output\{date.today()}_reasignado.xlsx",
                          header=True,
                          index=False)
    print("La data ha sido reasignada")

def colaboradores():
    dfColaborador = pd.read_excel("..\input\colaboradores.xlsx",
                                sheet_name="Hoja1",
                                header=0)
    opcion=input("Â¿Desea que se procese segĂºn a los valores dados?[Y/N]:")
    
    #print(dfColaborador)
    if opcion.upper()=='Y':
        dfColaborador=dfColaborador[dfColaborador.participacion==1]
    else:
        dfColaborador=dfColaborador[dfColaborador.Modalidad!="Vacaciones"]
        o=int(input("Opciones de distribuciĂ³n:\n1:Todos\n2:Seleccionar\n3:Yo lo harĂ© por tĂ­:"))
        if o==1:
            print("Todos han sido seleccionados")
        elif o==2:
            lisColaboradores=dfColaborador.colaborador.tolist()
            print("Lista de trabajadores")
            print("\n".join(map(str,list(enumerate(lisColaboradores)))))
            seleccionCola=input("\Ingrese cĂ³digos(separelos por ,):")
            codeSelect=list(map(int,seleccionCola.split(",")))
            lisColaboradores=array(lisColaboradores)[codeSelect]
            dfColaborador=dfColaborador[dfColaborador.colaborador.isin(lisColaboradores)]
            
        else:
            numbers=random.randint(1,(len(dfColaborador)-1)/2)
            dfColaborador=dfColaborador.sample(numbers)
            print(dfColaborador)
    return dfColaborador



def asignar(dfReasignado,dfColaborador):
    n=input("Â¿Nos dejarĂ­as asignar aleatoriamente los colaboradores?[Y/N]:")
    if n.upper()=="Y":
      
        for i in dfReasignado.index:
            randowmCola=dfColaborador.sample()
            dfReasignado["Registro"][i]=randowmCola.Registro.values[0]
            dfReasignado['Nombre de colaborador'][i]=randowmCola.colaborador.values[0]
        
    else:
        numeroContri=len(dfReasignado)
        print(f"\nTotal de Contribuyentes:{numeroContri}")
        suma=0
        nroContris=0
        arrayNumero=[]
        for i,row in dfColaborador.iterrows():
            while True:
                nroContris=int(input(f"\nÂ¿CuĂ¡ntos a {row['colaborador']}:"))
                if((suma+nroContris)<=numeroContri):
                    print(nroContris)
                    suma=suma+nroContris
                    arrayNumero.append(nroContris)
                    break
                else:
                    print("\nValor superado al nĂºmero disponible. Intente otra vez")
        print("Asignando")
        itera=0
        for i in dfColaborador.index:
            print(itera)
            print(arrayNumero[itera])
            print(arrayNumero)
            lis=dfReasignado[dfReasignado.Registro==""].sample(arrayNumero[itera]).ruc.tolist()
            print(lis)
            print(dfColaborador['Registro'][i])
            dfReasignado.loc[dfReasignado.ruc.isin(lis),'Registro']= dfColaborador['Registro'][i]
            dfReasignado.loc[dfReasignado.ruc.isin(lis),'colaborador']= dfColaborador['colaborador'][i]
            print(dfReasignado.Registro)
            print(dfReasignado[dfReasignado.Registro==""])
            itera=itera+1
            print(itera)
    return dfReasignado

if __name__ == "__main__":
    main()
