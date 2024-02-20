# -- coding: utf-8 --
"""
Created on Tue May  9 14:21:50 2023

@author: lixan
"""

#%%Inicializacion y Funciones
from urllib.request import urlopen
import pandas as pd
import datetime
from datetime import datetime, timedelta, time
import tkinter as tk
from tkinter import filedialog
import simplekml
import utm
from time import sleep


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
    print(F)
    return datetime.strptime(F,'%Y-%m-%dT%H:%M:%SZ')-timedelta(hours=3)
def convertir_fecha_sinhora(F):
    print(F)
    return datetime.strptime(F,'%Y-%m-%dT%H:%M:%SZ')-timedelta(hours=3)

def Obtener_dia(t):
    try:
        return t.date()
    except: del (t)
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

Result = filedialog.askdirectory(title='Elija Carpeta de Resultados') #OJO AQUI ESTA LA CARPETA DONDE SE GUARDAN LOS RESULTADOS

#%%Tomar Datos Originales
from statistics import mean

#Po = pd.read_csv('Centroides_Paneles_GUANCHOI.csv')
Po=pd.read_csv(filedialog.askopenfilename(title='Elija Excel Con centroides GUANCHOI'))
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



#%%Leer Base de Datos
URL=['https://api.orcascan.com/views/lCkVsM7sSVs6VAsD.csv?history=True']

# Abrir URL y tratamiento de datos. Crear DF de datos

Total=pd.DataFrame()
for u in URL:
    r=urlopen(u)
    
    a=r.read()
    a=a.decode().split('\n')
    print('Descarga de base de datos realizada')



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
    print('Creado el formato de datos desde base de datos')        
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
    df=df.query('lat!="?"').copy()
    df['Date']=df['ChangedOn'].apply(convertir_fecha)   
    df['lon']=df['lon'].str.replace(' ','').apply(to_float)
    df['lat']=df['lat'].str.replace(' ','').apply(to_float)
    df['Day']=df['Date'].apply(Obtener_dia)
    df=df.sort_values(['ChangedBy','Date'],ignore_index=True)
    Total=pd.concat([Total,df],axis=0)
    ing=datetime(2024,1,1).date()
    Total=Total.query('Day > @ing').copy()

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

SINCRO=Total.copy()
SINCRO.to_csv(Result+r'/todo_Sincronizados.csv')

print('Descarga de base de datos realizada, Excel con datos de respaldo creado (todo_Sincronizados.csv)')

#%%Agregar excels nuevos
import os
sueltos = filedialog.askdirectory(title='Elija Carpeta de exceles de Listas ')

csvs=bus_direc('.csv', sueltos) # Revisa si es CSV
xlsx=bus_direc('.xls', sueltos) # Revisa si es EXCEL

# Creación de listas

Change2=list() #
SheetName2=list()       # Listado de excel
Barcode2=list()         # Listado de codigos de barra
lat2=list()             # Listado de latitud
lon2=list()             # Listado de longitud
ids2=list()             # Listado de ids
Date2=list()            # Listado de fecha
ChangedBy2=list()       # ??
ChangedOn2=list()       # ??
ChangedUsing2=list()    # ??
Malos2=list()           # ??

for ex in xlsx:
    Lec=pd.read_excel(ex)
    cuenta=ex.split('/')[-3]
    # iteración sobre los archivos excel/csv
    # Toma en cuenta solo los mediciones GPS correctas
    # BC = barcode
    # LATLON = GPS
    # DATE = Date
    for BC,LATLON,DATE  in zip(Lec['Barcode'],Lec['GPS'],Lec['Date']):
        if LATLON=='Unknown': 
            print(ex)
            pass
        
        else:
            # Guarda los datos de los excel en una lista que tiene los campos de add,archivo,barcode,lat,lon,id,fecha,correo,timestamp,"un ladrillo"???
            Change2.append('add')
            SheetName2.append(ex.split('/')[-1])
            Barcode2.append(BC) 
            lat2.append(float(LATLON.split(',')[0]))
            lon2.append(float(LATLON.split(',')[1]))
            ids2.append(1)
            Date2.append(DATE)
            ChangedBy2.append(f'sdlascan{int(ex.split("/")[-1].split("-")[1])}@gmail.com')
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

df2=df2.sort_values(['Date','ChangedBy','SheetName'],ignore_index=True)
Total=df2.copy()

Total['int']=Total['lat'].astype(str)+' '+Total['lon'].astype(str)
Total['X']=Total['int'].apply(lambda x: utm.from_latlon(float(x.split(' ')[0]), float(x.split(' ')[1]))[0])
Total['Y']=Total['int'].apply(lambda x: utm.from_latlon(float(x.split(' ')[0]), float(x.split(' ')[1]))[1])
del Total['int']
Total['D']='?'
filtro = Total.Date.dt.time < time(14, 0)
Total.loc[filtro,'D']='M'
filtro = Total.Date.dt.time >= time(14, 0)
Total.loc[filtro,'D']='T'
EXX=Total.copy()


EXX['idlista']=0
EXX['CT_LISTA']='?'
cont_id=0
for DD in EXX.Day.drop_duplicates().sort_values():
    Total_DD=EXX.query('Day==@DD') #Filtrado por dia
    
    for User in Total_DD.ChangedBy.drop_duplicates().sort_values():
        Total_User=Total_DD.query('ChangedBy==@User')
        
        for ShNa in Total_User.SheetName.drop_duplicates().sort_values():
            cont_id+=1
            Total_ShNa=Total_User.query('SheetName==@ShNa')
            EXX.loc[(EXX['Day']==DD)&(EXX['ChangedBy']==User)&(EXX['SheetName']==ShNa),'idlista']=cont_id
            print(ShNa,cont_id)
        
EXX=EXX.drop_duplicates('Barcode',keep='last')
EXX['Barcode']=EXX['Barcode'].astype('str')
print('Creado el formato de datos desde Exceles, respaldado en TODO_EXCELES.csv')
#%%Estadisticas

print('Para los Excels')
for DD in Total.Day.drop_duplicates().sort_values():
    Total_DD=Total.query('Day==@DD') #Filtrado por dia
    print(DD)
    print('El dia',DD,'se escanearon',len(Total_DD), 'en total')
    
    for User in Total_DD.ChangedBy.drop_duplicates().sort_values():
        Total_User=Total_DD.query('ChangedBy==@User')
        print('El usuario',User,'escaneo',len(Total_User),'codigos')
        


REPORT=pd.DataFrame()
Repair=pd.DataFrame()

sen=7 #sensibilidad 



DIA=list()
USER=list()
SHEET=list()
CCM=list()
CCT=list()
CCM_F=list()
CCT_F=list()
REPARACIONES=list()

campos_de_listas=pd.DataFrame()
d_=list()
lis_=list()
ct_=list()
idlis_=list()


id_sheet=0
stat=dict()
for h in range(37,66):
    stat[str(h)]=0
    
for DD in EXX.Day.drop_duplicates().sort_values():
    Total_DD=EXX.query('Day==@DD') #Filtrado por dia
    for User in Total_DD.ChangedBy.drop_duplicates().sort_values():
        Total_User=Total_DD.query('ChangedBy==@User')
        
        #REVISAR LAS LISTAS
        for ShNa in Total_User.SheetName.drop_duplicates().sort_values():
            Total_ShNa=Total_User.query('SheetName==@ShNa')
            idlis=Total_ShNa.idlista.iloc[0]
            #Selector de lineas
            xm=mean(Total_ShNa.X)
            ym=mean(Total_ShNa.Y)
            horario=Total_ShNa.D.drop_duplicates().iloc[0][0]
            line=Po_stats.query('abs(Xmed-@xm)<@sen and Ysup>@ym and Yinf<@ym and side==@horario')


            if len(line)==1:
                #print(line.CT.iloc[0], line.Cant_p.iloc[0],len(Total_ShNa.query('Barcode.str.len()==14')))
                escans=len(Total_ShNa.query('Barcode.str.len()==14 and Barcode.str.contains("I")').drop_duplicates())
                original=line.Cant_p.iloc[0]
                
                if escans%42==0:
                    
                    stat[str(line.CT.iloc[0])]=stat[line.CT.iloc[0]]+escans
                    EXX.loc[EXX['idlista']==idlis,'CT_LISTA']=line.CT.iloc[0]
                    d_.append(DD)
                    lis_.append(ShNa)
                    idlis_.append(idlis)
                    ct_.append(line.CT.iloc[0])
                
                elif (escans!=original):
                    REPARACIONES.append(' '.join(['Revisar',ShNa,'del dia',str(DD),'se escaneo',str(escans), 'de',str(original)]))
            
                
            else: 
                print(ShNa,DD,len(line))
                REPARACIONES.append(' '.join(['Revisar',ShNa,'del dia',str(DD),'se escaneo',str(escans), 'de',str(original)]))
        DIA.append(DD)
        USER.append(User)
        CCM.append(len(Total_User.query('D=="M"')))
        CCT.append(len(Total_User.query('D=="T"')))
        CCM_F.append(len(Total_User.query('D=="M" and Barcode.str.len()==14')))
        CCT_F.append(len(Total_User.query('D=="T" and Barcode.str.len()==14')))

REPORT['DIA']=DIA
REPORT['USER']=USER
REPORT['CCM']=CCM
REPORT['CCT']=CCT
REPORT['CCM_F']=CCM_F
REPORT['CCT_F']=CCT_F

campos_de_listas['Fecha']=d_
campos_de_listas['Lista']=lis_
campos_de_listas['idlista']=idlis_
campos_de_listas['CT']=ct_
campos_de_listas.to_csv(Result+r'/CAMPOS_DE_LISTAS.csv',index=False)


REPORT.to_csv(Result+rf'/REPORTE_{str(datetime.now()).replace(":","_")}_{str(datetime.now()).replace(":","_")}.csv')
Repair['R']=REPARACIONES
Repair.to_csv(Result+rf'/Reparaciones_{str(datetime.now()).replace(":","_")}.csv',index=False)

EXX.to_csv(Result+r'/TODO_EXELES.csv')
print(stat)
print('Proceso terminado')

#%%


