# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:21:50 2023

@author: lixan
"""

#%%Inicializacion y Funciones
from urllib.request import urlopen
import pandas as pd
from datetime import datetime, timedelta, time
import tkinter as tk
from tkinter import filedialog
import simplekml
import utm

def bus_direc(name,direc):
    d=list()
    for n in os.listdir(direc):
        try:
            for m in os.listdir(direc+r'/'+n):
                try:
                    for l in os.listdir(direc+r'/'+n+r'/'+m):
                        try:
                            for on in os.listdir(direc+r'/'+n+r'/'+m+r'/'+l):
                                try:
                                    for off in os.listdir(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on):
                                        try:
                                            for add in os.listdir(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on+r'/'+off):
                                                try:
                                                    for add2 in os.listdir(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on+r'/'+off+r'/'+add):
                                                        try:
                                                            for add3 in os.listdir(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on+r'/'+off+r'/'+add+r'/'+add2):
                                                                if name in add3:
                                                                    d.append(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on+r'/'+off+r'/'+add+r'/'+add2+r'/'+add3)
                                                        except:
                                                            if name in add2:
                                                                d.append(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on+r'/'+off+r'/'+add+r'/'+add2)
                                                except:
                                                   if name in add:
                                                       d.append(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on+r'/'+off+r'/'+add) 
                                        except:       
                                            if name in off:
                                                d.append(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on+r'/'+off)
                                except:
                                    if name in on:
                                        d.append(direc+r'/'+n+r'/'+m+r'/'+l+r'/'+on)
                        except:
                            if name in l:
                                d.append(direc+r'/'+n+r'/'+m+r'/'+l)
                except:
                    if name in m:
                        d.append(direc+r'/'+n+r'/'+m)
        except:
            if name in n:
                d.append(direc+r'/'+n)
    
    return (d)


def inv(stri):
    out= 'I'+stri[1:4]+'.'+stri[5:7]
    return out

def CB(s):
    out2='SB'+s[1:4]+'.'+s[5:7]+'.'+s[8:10]
    return out2

def Quitar_(l):
    out3=l[0:13]
    return out3

def convertir_fecha(F):
    try:
        return datetime.strptime(F,'%Y-%m-%dT%H:%M:%SZ')
    except: del F

def Obtener_dia(t):
    return t.date()
def Obtener_hora(t):
    try:
        return t.time()
    except: del (t)
def to_float(text):
    try:
        return float(text)
    except: return text

def marcar_linea(marca,data):
    print(f'La linea {marca} tiene {len(data)} datos posibles')
    pass

def sumarHora(t):
    return t-timedelta(hours=3)

def to_time(t):
    return datetime.strptime(t, '%H:%M:%S').time()

def replacemarzo(t):
    if 'marzo' in t:
        return t.replace('marzo','March')
    if 'abril' in t:
        return t.replace('abril','April')

def to_date(t):
    return datetime.strptime(t," %d de %B de %Y").date()

#%%Tomar Datos Originales
from statistics import mean

#Po = pd.read_csv('Centroides_Paneles_GUANCHOI.csv')
Po=pd.read_csv(filedialog.askopenfilename(title='Elija Carpeta de Excel Sueltos'))
Po.columns=['X','Y','TRK']

Po['CT']=Po.TRK.apply(lambda x: x.split('.')[1])
Po['X']=Po.X.apply(lambda x: round(x,1))

campo=list()
Xme=list()
Ysup=list()
Yinf=list()
Cantp=list()
side=list()
for ct in Po.CT.drop_duplicates().sort_values():
    Po_ex=Po.query('CT==@ct')
    i=0
    for Xs in Po_ex.X.drop_duplicates().sort_values():
        campo.append(ct)
        Xme.append(Xs)
        Ysup.append(max(Po_ex.query('X==@Xs').Y))
        Yinf.append(min(Po_ex.query('X==@Xs').Y))
        Cantp.append(len(Po_ex.query('X==@Xs')))
        if i%2==0:
            side.append('T')
        else:
            side.append('M')
        i+=1
Po_stats=pd.DataFrame()
Po_stats['CT']=campo
Po_stats['Xmed']=Xme
Po_stats['Ysup']=Ysup
Po_stats['Yinf']=Yinf
Po_stats['Cant_p']=Cantp
Po_stats['side']=side



#%%Crear Listas de Trackers
URL=['https://api.orcascan.com/views/lCkVsM7sSVs6VAsD.csv?history=True']

#%% Abrir URL y tratamiento de datos. Crear DF de datos

Total=pd.DataFrame()
for u in URL:
    r=urlopen(u)
    a=r.read()
    a=a.decode().split('\n')
    del a[0]
    Change=list()
    SheetName=list()
    Barcode=list()
    lat=list()
    lon=list()
    ids=list()
    Date=list()
    ChangedBy=list()
    ChangedOn=list()
    ChangedUsing=list()
    Malos=list()
    for dat in a:   
        dat=dat.replace('"','').split(',')
        if len(dat) in [10]:
            Change.append(dat[0])
            SheetName.append(dat[1])
            Barcode.append(dat[2])
            if not dat[3] in ['Unknown','']:
                lat.append(dat[3])
                lon.append(dat[4])
            else:
                lat.append('?')
                lon.append('?')
                dat.insert(3,'?')
            ids.append(dat[5])
            Date.append(dat[6])
            ChangedBy.append(dat[7])
            ChangedOn.append(dat[8])
            ChangedUsing.append(dat[9])
        else: Malos.append(dat)
            
    df=pd.DataFrame()
    df['Change']=Change
    df['SheetName']=SheetName
    df['Barcode']=Barcode
    df['lat']=lat   
    df['lon']=lon
    df['ids']=ids
    df['Date']=Date
    df['ChangedBy']=ChangedBy
    df['ChangedOn']=ChangedOn
    df['ChangedUsing']=ChangedUsing
    
    df=df[df['Barcode'].str.len()>1]
    df['Date']=df['Date'].apply(convertir_fecha)   
    df['lon']=df['lon'].str.replace(' ','').apply(to_float)
    df['lat']=df['lat'].str.replace(' ','').apply(to_float)
    df['Day']=df['Date'].apply(Obtener_dia)
    df=df.sort_values(['ChangedBy','Date'],ignore_index=True)
    Total=pd.concat([Total,df],axis=0)
    Total=Total.query('Day>datetime(2024,1,1).date()')

#Crear utm
Total['int']=Total['lat'].astype(str)+' '+Total['lon'].astype(str)
Total['X']=Total['int'].apply(lambda x: utm.from_latlon(float(x.split(' ')[0]), float(x.split(' ')[1]))[0])
Total['Y']=Total['int'].apply(lambda x: utm.from_latlon(float(x.split(' ')[0]), float(x.split(' ')[1]))[1])
del Total['int']
Total['D']='?'
filtro = Total.Date.dt.time < time(14, 0)
Total.loc[filtro,'D']='M'
filtro = Total.Date.dt.time >= time(14, 0)
Total.loc[filtro,'D']='T'

#%%Agregar excels nuevos
import os
sueltos = filedialog.askdirectory(title='Elija Carpeta de Excel Sueltos')

csvs=bus_direc('.csv', sueltos)
xlsx=bus_direc('.xls', sueltos)

Change2=list()
SheetName2=list()
Barcode2=list()
lat2=list()
lon2=list()
ids2=list()
Date2=list()
ChangedBy2=list()
ChangedOn2=list()
ChangedUsing2=list()
Malos2=list()

for ex in xlsx:
    Lec=pd.read_csv(ex)
    cuenta=ex.split('/')[-3]
    #Lec.columns=['BARCODE','idd','GPS','DATE']
    for BC,LATLON,DATE  in zip(Lec['Barcode'],Lec['GPS'],Lec['Date']):
        if LATLON=='Unknown': 
            print(ex)
            pass
        else:
            Change2.append('add')
            SheetName2.append(ex)
            Barcode2.append(BC)
            lat2.append(float(LATLON.split(',')[0]))
            lon2.append(float(LATLON.split(',')[1]))
            ids2.append(1)
            Date2.append(DATE)
            ChangedBy2.append(cuenta)
            ChangedOn2.append(DATE)
            ChangedUsing2.append('Un Ladrillo')

df2=pd.DataFrame()
df2['Change']=Change2
df2['SheetName']=SheetName2
df2['Barcode']=Barcode2
df2['lat']=lat2
df2['lon']=lon2
df2['ids']=ids2
df2['Date']=Date2
df2['ChangedBy']=ChangedBy2
df2['ChangedOn']=ChangedOn2
df2['ChangedUsing']=ChangedUsing2

df2['Day']=df2['Date'].apply(Obtener_dia)

df2=df2.sort_values(['ChangedBy','Date'],ignore_index=True)

Result = filedialog.askdirectory(title='Elija Carpeta de Resultados')
df2.to_csv(Result+r'/TODO_EXELES.csv')
Total.to_csv(Result+r'/TODO_Sincronizado.csv')
Po_ex.to_csv(Result+r'/Centroides_UTM.csv')
Po_stats.to_csv(Result+r'/Estadisticas_Planta_por_linea.csv')
Total=df2.copy()

#%% Estadisticas
from time import sleep
for di in Total.Day.drop_duplicates().sort_values():
    T_dia=Total.query('Day==@di').copy()
    #if di==datetime(2024,1,31).date():continue
    #print(di,len(T_dia))
    for user in T_dia.ChangedBy.drop_duplicates().sort_values():
        T_user=T_dia.query('ChangedBy==@user')
        print(di,user,len(T_user.query('Barcode.str.len()==14 and D=="M"')),len(T_user.query('Barcode.str.len()==14 and D=="T"')),len(T_user.query('D=="M"')),len(T_user.query('D=="T"')))#,len(T_user.query('Barcode.str.len()==14'))/42)
        for Sheet_ in T_user.SheetName.drop_duplicates().sort_values():
            T_sheet=T_user.query('SheetName==@Sheet_')
            Xmm=mean(T_sheet.X)
            Ymm=mean(T_sheet.Y)
            try:
                CT=list(Po_stats.query('abs(Xmed-@Xmm)<2 and Ysup>@Ymm and Yinf<@Ymm').CT)[0]
            except: CT='?'
            #print(len(T_sheet.query('Barcode.str.len()==14').drop_duplicates(keep='last'))/42)
            #print(di,user,Sheet_,CT,len(T_sheet.drop_duplicates('Barcode')))
            #T_sheet.to_csv('Primer_avance.csv')
            #sleep(5)




#%%Datos anteriores TRATAMIENTO DE DATOS
totalPaneles=len(Z1)+len(Z2)+len(Z3)+len(Z4)+len(Z5)

TCSV=df.copy() #Copia de Datos

#Rectiicar lineas Segunda Visita
tf=TCSV[TCSV['Barcode'].str.len()==21].drop_duplicates('Barcode',keep='last')
tf=tf[tf['lat']!='?']

import utm
Xn=list()
Yn=list()

for lat,lon in zip(tf['lat'],tf['lon']):
    print((lat, lon))
    Xn.append(utm.from_latlon(lat, lon)[0])
    Yn.append(utm.from_latlon(lat, lon)[1])

tf['X']=Xn
tf['Y']=Yn
tf['Hour']=tf['Date'].apply(Obtener_hora)
tf.to_csv(Result+r'/tf_sinrec.csv')

#%% Rectificar segunda visita
Rect=tf.sort_values(['Day','SheetName','Hour']).drop_duplicates('Barcode',keep='last')
'''
ho=list()
for dati,hori in zip(Rect['Date'],Rect['Hour']):
    if dati == datetime(2023, 3, 30).date():
        ho.append(hori)
    if dati >= datetime(2023, 3, 31).date():
        ho.append(hori.replace(hour=(hori.hour-1)))

PrVis['Hora']=ho
'''
Corr=pd.DataFrame()
Erro=pd.DataFrame()
horaMañana=datetime(1990,3,3, 13, 20, 1).time()
import statistics
from statistics import mean
from time import sleep

for Dia in Rect.Day.drop_duplicates():
    print(Dia)
    for Sheet in Rect.query('Day==@Dia').SheetName.drop_duplicates():
        Scans=Rect.query('(Day==@Dia) & (SheetName==@Sheet)')
        if statistics.pstdev(Scans.X)<4 and statistics.pstdev(Scans.X)>0:
            Dat=Rect.query('(Day==@Dia) & (SheetName==@Sheet)')#.to_csv('test.csv')
            if len(Dat):
                print (len(Scans),statistics.pstdev(Scans.X),Sheet,mean(Dat['X']))
                Dat['Xmean']=mean(Dat['X'])
                Corr=pd.concat([Corr,Dat],axis=0)
            #sleep(1)
        if statistics.pstdev(Scans.X)>=4:
            Dat=Rect.query('(Day==@Dia) & (SheetName==@Sheet)')#.to_csv('test.csv')
            if len(Dat)>10:
                print (len(Scans),statistics.pstdev(Scans.X),Sheet,mean(Dat['X']))
                #Mañana
                Dat=Rect.query('(Day==@Dia) & (SheetName==@Sheet) & (Hour<@horaMañana)')
                if len(Dat)>10:
                    if statistics.pstdev(Dat.X)>4:
                        Dat1=Dat.query(f'X<{mean(Dat["X"])}')
                        Dat2=Dat.query(f'X>{mean(Dat["X"])}')
                        
                        if statistics.pstdev(Dat1.X)>4:
                            Dat3=Dat1.query(f'X<{mean(Dat1["X"])}')
                            Dat4=Dat1.query(f'X>{mean(Dat1["X"])}')
                            Dat3['Xmean']=mean(Dat3["X"])
                            Dat4['Xmean']=mean(Dat4["X"])
                            Corr=pd.concat([Corr,Dat3,Dat4],axis=0)
                            
                        if statistics.pstdev(Dat1.X)<=4 and statistics.pstdev(Dat1.X)>0:
                            Dat1['Xmean']=mean(Dat1["X"])
                            Corr=pd.concat([Corr,Dat1],axis=0) 
                            
                        if statistics.pstdev(Dat2.X)>4:
                            Dat3=Dat2.query(f'X<{mean(Dat2["X"])}')
                            Dat4=Dat2.query(f'X>{mean(Dat2["X"])}')
                            Dat3['Xmean']=mean(Dat3["X"])
                            Dat4['Xmean']=mean(Dat4["X"])
                            Corr=pd.concat([Corr,Dat3,Dat4],axis=0)
                            
                        if statistics.pstdev(Dat2.X)<=4 and statistics.pstdev(Dat2.X)>0:
                            Dat2['Xmean']=mean(Dat2["X"])
                            Corr=pd.concat([Corr,Dat2],axis=0) 
                            
                    if statistics.pstdev(Dat.X)<=4 and statistics.pstdev(Dat.X)>0:
                        Dat['Xmean']=mean(Dat['X'])
                        Corr=pd.concat([Corr,Dat],axis=0) 
                #Tarde
                Dat=Rect.query('(Day==@Dia) & (SheetName==@Sheet) & (Hour>@horaMañana)')
                if len(Dat)>10:
                    if statistics.pstdev(Dat.X)>4:
                        Dat1=Dat.query(f'X<{mean(Dat["X"])}')
                        Dat2=Dat.query(f'X>{mean(Dat["X"])}')
                        
                        if statistics.pstdev(Dat1.X)>4:
                            Dat3=Dat1.query(f'X<{mean(Dat1["X"])}')
                            Dat4=Dat1.query(f'X>{mean(Dat1["X"])}')
                            Dat3['Xmean']=mean(Dat3["X"])
                            Dat4['Xmean']=mean(Dat4["X"])
                            Corr=pd.concat([Corr,Dat3,Dat4],axis=0)
                            
                        if statistics.pstdev(Dat1.X)<=4 and statistics.pstdev(Dat1.X)>0:
                            Dat1['Xmean']=mean(Dat1["X"])
                            Corr=pd.concat([Corr,Dat1],axis=0) 
                            
                        if statistics.pstdev(Dat2.X)>4:
                            Dat3=Dat2.query(f'X<{mean(Dat2["X"])}')
                            Dat4=Dat2.query(f'X>{mean(Dat2["X"])}')
                            Dat3['Xmean']=mean(Dat3["X"])
                            Dat4['Xmean']=mean(Dat4["X"])
                            Corr=pd.concat([Corr,Dat3,Dat4],axis=0)
                            
                        if statistics.pstdev(Dat2.X)<=4 and statistics.pstdev(Dat2.X)>0:
                            Dat2['Xmean']=mean(Dat2["X"])
                            Corr=pd.concat([Corr,Dat2],axis=0) 
                            
                    if statistics.pstdev(Dat.X)<=4 and statistics.pstdev(Dat.X)>0:
                        Dat['Xmean']=mean(Dat['X']) 
                        Corr=pd.concat([Corr,Dat],axis=0) 
            
Corr.to_csv(Result+r'/Corr.csv')

E=pd.DataFrame()
E['Xmean']=Corr['Xmean']
E['Y']=Corr['Y']
E['C']=Corr['Barcode']
E['Hour']=Corr['Hour']
E['Day']=Corr['Day']

#%%
#Rectificar Primera Visita
PrVis = pd.read_csv('Antecedentes/Primera Visita Codigos y posiciones en UTM, LAT LON, LISTA, HORA.csv').sort_values(['Lista','Fecha','Hora'])
PrVis['Fecha']=PrVis['Fecha'].apply(replacemarzo)
PrVis['Fecha']=PrVis['Fecha'].apply(to_date)
PrVis['Hora']=PrVis['Hora'].apply(to_time)
'''
ho=list()
for dati,hori in zip(PrVis['Fecha'],PrVis['Hora']):
    if dati < datetime(2022, 4, 2).date():
        ho.append(hori)
    if dati >= datetime(2022, 4, 2).date():
        ho.append(hori.replace(hour=(hori.hour-1)))

PrVis['Hora']=ho
'''
Rect2=PrVis.sort_values(['Fecha','Lista','Hora'])


import statistics
from statistics import mean
from time import sleep

Corr2=pd.DataFrame()
Erro2=pd.DataFrame()


for Dia in Rect2.Fecha.drop_duplicates():
    print(Dia)
    horaMañana=datetime(1990,3,3, 13, 20, 1).time()
    for Sheet in Rect2.query('Fecha==@Dia').Lista.drop_duplicates():
        Scans=Rect2.query('(Fecha==@Dia) & (Lista==@Sheet)')
        if len(Scans)>0:
            if statistics.pstdev(Scans.X)<4 and statistics.pstdev(Scans.X)>0:
                Dat=Rect2.query('(Fecha==@Dia) & (Lista==@Sheet)')#.to_csv('test.csv')
                if len(Dat)>10:
                    print (len(Scans),statistics.pstdev(Scans.X),Sheet,mean(Dat['X']))
                    Dat['Xmean']=mean(Dat['X'])
                Corr2=pd.concat([Corr2,Dat],axis=0)
                Dat.to_csv('muestra1.csv')
                #sleep(1)
            if statistics.pstdev(Scans.X)>4:
                Dat=Rect2.query('(Fecha==@Dia) & (Lista==@Sheet)')#.to_csv('test.csv')
                if len(Dat)>10:
                    print (len(Scans),statistics.pstdev(Scans.X),Sheet,mean(Dat['X']))
                    #Mañana
                    Dat=Rect2.query('(Fecha==@Dia) & (Lista==@Sheet) & (Hora<@horaMañana)')
                    if len(Dat)>10:
                        if statistics.pstdev(Dat.X)>4:
                            Dat1=Dat.query(f'X<{mean(Dat["X"])}')
                            Dat2=Dat.query(f'X>{mean(Dat["X"])}')
                            
                            if statistics.pstdev(Dat1.X)>4:
                                Dat3=Dat1.query(f'X<{mean(Dat1["X"])}')
                                Dat4=Dat1.query(f'X>{mean(Dat1["X"])}')
                                Dat3['Xmean']=mean(Dat3["X"])
                                Dat4['Xmean']=mean(Dat4["X"])
                                Corr2=pd.concat([Corr2,Dat3,Dat4],axis=0)
                                #Dat3.to_csv('muestra1.csv')
                                #sleep(0.5)
                                #Dat4.to_csv('muestra1.csv')
                                #sleep(0.5)
                                
                            if statistics.pstdev(Dat1.X)<4 and statistics.pstdev(Dat1.X)>0:
                                Dat1['Xmean']=mean(Dat1["X"])
                                Corr2=pd.concat([Corr2,Dat1],axis=0) 
                                Dat1.to_csv('muestra1.csv')
                                
                            if statistics.pstdev(Dat2.X)>4:
                                Dat3=Dat2.query(f'X<{mean(Dat2["X"])}')
                                Dat4=Dat2.query(f'X>{mean(Dat2["X"])}')
                                Dat3['Xmean']=mean(Dat3["X"])
                                Dat4['Xmean']=mean(Dat4["X"])
                                Corr2=pd.concat([Corr2,Dat3,Dat4],axis=0)
                                #Dat3.to_csv('muestra1.csv')
                                #sleep(0.5)
                                #Dat4.to_csv('muestra1.csv')
                                #sleep(0.5)
                                
                                
                            if statistics.pstdev(Dat2.X)<4 and statistics.pstdev(Dat2.X)>0:
                                Dat2['Xmean']=mean(Dat2["X"])
                                Corr2=pd.concat([Corr2,Dat2],axis=0) 
                                #Dat2.to_csv('muestra1.csv')
                                
                        if statistics.pstdev(Dat.X)<4 and statistics.pstdev(Dat.X)>0:
                           Corr2=pd.concat([Corr2,Dat],axis=0) 
                           #Dat2.to_csv('muestra1.csv')
                    #Tarde
                    Dat=Rect2.query('(Fecha==@Dia) & (Lista==@Sheet) & (Hora>@horaMañana)')
                    if len(Dat)>10:
                        if statistics.pstdev(Dat.X)>4:
                            Dat1=Dat.query(f'X<{mean(Dat["X"])}')
                            Dat2=Dat.query(f'X>{mean(Dat["X"])}')
                            
                            if statistics.pstdev(Dat1.X)>4:
                                Dat3=Dat1.query(f'X<{mean(Dat1["X"])}')
                                Dat4=Dat1.query(f'X>{mean(Dat1["X"])}')
                                Dat3['Xmean']=mean(Dat3["X"])
                                Dat4['Xmean']=mean(Dat4["X"])
                                Corr2=pd.concat([Corr2,Dat3,Dat4],axis=0)
                                #Dat3.to_csv('muestra1.csv')
                                #sleep(0.5)
                                #Dat4.to_csv('muestra1.csv')
                                #sleep(0.5)
                                
                            if statistics.pstdev(Dat1.X)<4 and statistics.pstdev(Dat1.X)>0:
                                Dat1['Xmean']=mean(Dat1["X"])
                                Corr2=pd.concat([Corr2,Dat1],axis=0) 
                                Dat1.to_csv('muestra1.csv')
                                
                            if statistics.pstdev(Dat2.X)>4:
                                Dat3=Dat2.query(f'X<{mean(Dat2["X"])}')
                                Dat4=Dat2.query(f'X>{mean(Dat2["X"])}')
                                Dat3['Xmean']=mean(Dat3["X"])
                                Dat4['Xmean']=mean(Dat4["X"])
                                Corr2=pd.concat([Corr2,Dat3,Dat4],axis=0)
                                #Dat3.to_csv('muestra1.csv')
                                #sleep(0.5)
                                #Dat4.to_csv('muestra1.csv')
                                #sleep(0.5)
                                
                                
                            if statistics.pstdev(Dat2.X)<4 and statistics.pstdev(Dat2.X)>0:
                                Dat2['Xmean']=mean(Dat2["X"])
                                Corr2=pd.concat([Corr2,Dat2],axis=0) 
                                #Dat2.to_csv('muestra1.csv')
                                
                        if statistics.pstdev(Dat.X)<4 and statistics.pstdev(Dat.X)>0:
                           Corr2=pd.concat([Corr2,Dat],axis=0) 
                           #Dat2.to_csv('muestra1.csv')
            
Corr2.to_csv(Result+r'/Corr2.csv')
Rect2.to_csv(Result+r'/Rect2.csv')

C=pd.DataFrame()
C['Xmean']=Corr2['Xmean']
C['Y']=Corr2['Y']
C['C']=Corr2['Codigo']
C['Hour']=Corr2['Hora']
C['Day']=Corr2['Fecha']
#%%
import simplekml
import utm

def latlon(mXM2,tXm2,miny2,maxy2):
    LL1=tuple(reversed(utm.to_latlon(mXM2, miny2, zone_number=19, northern=False)))
    LL2=tuple(reversed(utm.to_latlon(tXm2, miny2, zone_number=19, northern=False)))
    LL3=tuple(reversed(utm.to_latlon(tXm2, maxy2, zone_number=19, northern=False)))
    LL4=tuple(reversed(utm.to_latlon(mXM2, maxy2, zone_number=19, northern=False)))
    LL5=tuple(reversed(utm.to_latlon(mXM2, miny2, zone_number=19, northern=False)))
    return [LL1,LL2,LL3,LL4,LL5]
    


D=pd.concat([C,E],axis=0).drop_duplicates('C',keep='last')

tipo=list()
for fecha,hora in zip(D['Day'],D['Hour']):

    if fecha < datetime(2022, 8, 1).date(): #Primera Visita
        if (fecha < datetime(2022, 4, 2).date()):#Cambio de Horario
            if (hora<datetime(1990,3,3, 13, 30, 1).time()):
                tipo.append('Mañana')
            else:
                tipo.append('Tarde')
        else: #Horario Invierno Una hora menos
            if (hora<datetime(1990,3,3, 12, 30, 1).time()):
                tipo.append('Mañana')
            else:
                tipo.append('Tarde')
    else: #Segunda Visita
        if (fecha == datetime(2023, 3, 29).date()) or (fecha == datetime(2023, 4, 28).date()): #Solo se Paso por el Oeste
            tipo.append('Tarde')
            print(fecha)
        else:
            if (fecha < datetime(2023, 4, 1).date()):#Cambio de Horario
                if (hora<datetime(1990,3,3, 13, 10, 1).time()):
                    tipo.append('Mañana')
                else:
                    tipo.append('Tarde')
            else: #Horario Invierno Una hora menos
                if (hora<datetime(1990,3,3, 14, 10, 1).time()):
                    tipo.append('Mañana')
                else:
                    tipo.append('Tarde')

D['Tipo']=tipo

D.query('Tipo=="Tarde"').to_csv(Result+r'/Tarde total.csv') 
D.query('Tipo=="Mañana"').to_csv(Result+r'/Mañana total.csv') 
#%%
listatrk=list()

spdx=0
spdy=0

trkcn=list()
kml = simplekml.Kml()
kmlpt = simplekml.Kml()
kmlp = simplekml.Kml()
kmlp2 = simplekml.Kml()

for zone in ZT:
    alpha=10 #parametro de sensibilidad
    Mañana=D.query('Tipo=="Mañana"')
    Tarde=D.query('Tipo=="Tarde"')
    print(len(zone))
    zone['TRK']=zone['TRK'].str.replace('-','.')
    zone=zone.drop_duplicates('TRK')
    print(len(zone))
    for trk,CANTP,tXm,tXM,mXm,mXM,miny,maxy in zip(zone.TRK, zone.Paneles, zone.tardeXmin, zone.tardeXmax,zone.mañanaXmin,zone.mañanaXmax,zone.minY,zone.maxY):
        #mXm=mXm-10
        #mXM=mXM+10
        candidatos=Tarde.query(f'Xmean>{tXm-alpha} and Xmean<{tXM+alpha} and Y>@miny and Y<@maxy')
        
        if len(candidatos)<10:
            print(trk,'TARDE')
            pol = kml.newpolygon(name=f'{trk} Tarde')
            pol.outerboundaryis = latlon(tXM+spdx,tXm+spdx,miny+spdy,maxy+spdy)
            pol.innerboundaryis = latlon(tXM+spdx,tXm+spdx,miny+spdy,maxy+spdy)
            c=[tuple(reversed(utm.to_latlon(float((mXM+tXm)/2), float((miny+maxy)/2), zone_number=19, northern=False)))]
            kmlp.newpoint(name=f"{trk} Tarde", coords=c)   
            listatrk.append(f'{trk} Tarde')
        
      
        candidatos=Mañana.query(f'Xmean>{mXm-alpha} and Xmean<{mXM+alpha} and Y>@miny and Y<@maxy')
        if len(candidatos)<10:
            print(trk,'MAÑANA')
            pol2 = kmlpt.newpolygon(name=f'{trk} Mañana')
            pol2.outerboundaryis = latlon(mXM+spdx,mXm+spdx,miny+spdy,maxy+spdy)
            pol2.innerboundaryis = latlon(mXM+spdx,mXm+spdx,miny+spdy,maxy+spdy)
            c=[tuple(reversed(utm.to_latlon(float((mXM+tXm)/2), float((miny+maxy)/2), zone_number=19, northern=False)))]
            kmlp2.newpoint(name=f"{trk} Mañana", coords=c)
            listatrk.append(f'{trk} Mañana')
          

now=str(datetime.now()).replace(':','_').replace('.','-')
#pol.innerboundaryis
kml.save(Result+rf"/Tarde_{now}.kml")
kmlpt.save(Result+rf"/Mañana_{now}.kml")
kmlp.save(Result+rf"/Puntos Tarde_{now}.kml")
kmlp2.save(Result+rf"/Puntos Mañana__{now}.kml")
D.to_csv(Result+rf"/todo_{now}.csv")
test=pd.DataFrame(listatrk)
test.to_csv(Result+rf"/listaTRKfaltante_{now}.csv")  

'''
kml.save(rf"D:\Domeyko\result/Tarde_{now}.kml")
kmlpt.save(rf"D:\Domeyko\result/Mañana_{now}.kml")
kmlp.save(rf"D:\Domeyko\result/Puntos Tarde_{now}.kml")
kmlp2.save(rf"D:\Domeyko\result/Puntos Mañana__{now}.kml")
D.to_csv(rf'D:\Domeyko\result/todo_{now}.csv')
test=pd.DataFrame(listatrk)
test.to_csv(rf'D:\Domeyko\result/listaTRKfaltante_{now}.csv')  
'''

