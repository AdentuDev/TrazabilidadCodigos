# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 13:08:13 2024

@author: lixan
"""
#%%Inicializacion y Funciones PASO1
from urllib.request import urlopen
import pandas as pd
import datetime
from datetime import datetime, timedelta, time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import simplekml
import utm
from time import sleep
import os
import shutil

def ventanaCapturaDatos(hh,ll,shh,CCOODD):

    def devolverDatos():
        textoCaja=entryTexto.get()
        texto.set(textoCaja)
        root.destroy()


    root=Tk()
    root.title("Entrada de datos")

    #FRAME DE ENTRADA DE DATOS

    miFrame=Frame(root)
    miFrame.pack()

    texto=StringVar()


    #ENTRY 

    entryTexto=Entry(miFrame, justify=CENTER ,textvariable=texto)
    entryTexto.insert(0, "0")
    entryTexto.grid(row=0, column=0, padx=5, pady=5)

    #TEXTOS
    label = Label(miFrame,text=hh)
    label.grid(row=2, column=0, padx=5, pady=5)
    
    label1 = Label(miFrame,text=ll)
    label1.grid(row=3, column=0, padx=5, pady=5)
    
    label2 = Label(miFrame,text=shh)
    label2.grid(row=4, column=0, padx=5, pady=5)
    
    label3 = Label(miFrame,text=CCOODD)
    label3.grid(row=5, column=0, padx=5, pady=5)

    #BOTÓN ACEPTAR

    botonAceptar=Button(miFrame, text="Aceptar", command=lambda:devolverDatos())
    botonAceptar.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    
    wtotal = root.winfo_screenwidth()
    htotal = root.winfo_screenheight()
    #  Guardamos el largo y alto de la ventana
    wventana = 300
    hventana = 200
    
    #  Aplicamos la siguiente formula para calcular donde debería posicionarse
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)
    
    #  Se lo aplicamos a la geometría de la ventana
    root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))
        
    
    root.mainloop()

    return texto.get()





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

root=Tk()
Result = filedialog.askdirectory(title='Elija Directorio de procesamiento') #OJO AQUI ESTA LA CARPETA DONDE SE GUARDAN LOS RESULTADOS
root.destroy()

#%%Tomar Datos Originales PASO2
from statistics import mean

#Po = pd.read_csv('Centroides_Paneles_GUANCHOI.csv')
root=Tk()
Po=pd.read_csv(filedialog.askopenfilename(title='Elija Excel Con centroides'))
root.destroy()
Po.columns=['X','Y','TRK','STRg']

Po['CT']=Po.TRK.apply(lambda x: x.split('.')[1])
Po['X']=Po.X.apply(lambda x: round(x,1))

Po['COD']='?'
Po['D']='?'
Po['time']=datetime(2,2,2)

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
        Po_Xs=Po_ex.query('X==@Xs').sort_values('Y')
        compa=min(Po_Xs.Y)
        separar=False
        for Ys in Po_Xs.Y:
            if Ys-compa>10:
                separar=True
                break
            compa=Ys
        
        if separar:
            #primera fila
            ymm=min(Po_Xs.Y)
            campo.append(ct)
            Xme.append(Xs)
            Ysup.append(compa)
            Yinf.append(ymm)
            Cantp.append(len(Po_ex.query('X==@Xs and Y>=@ymm and Y<=@compa')))
            if i%2==0:    
                side.append('T')
            else:
                side.append('M')

            
            #Segunda Fila

            ymm=Ys
            YMM=max(Po_Xs.Y)
            campo.append(ct)
            Xme.append(Xs)
            Ysup.append(YMM)
            Yinf.append(ymm)
            Cantp.append(len(Po_ex.query('X==@Xs and Y>=@ymm and Y<=@YMM')))
            if i%2==0:    
                side.append('T')
            else:
                side.append('M')
            i+=1
        else:
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

for ind,row in Po_stats.iterrows():
    dat=Po[(Po['X']==row['Xmed'] )&( Po['Y']>=row['Yinf'])&(Po['Y']<=row['Ysup'])].index
    Po.loc[dat,'D']=row['side']
    

for CR in Po.CT.drop_duplicates().sort_values():
    count=0.5
    nyn=Po.query('CT==@CR')
    for Xx in nyn.X.drop_duplicates().sort_values():
        count=count+0.5
        fil=nyn.query('X==@Xx')
        Po.loc[fil.index,'line']=str(int(count))

Po.to_csv('entregable.csv',index=False)
        
#%%Conversion de Archivos de Escaneo y analisis simple PASO3
root=Tk()
EXC_OR = filedialog.askdirectory(title='Elija Carpeta de exceles para analizar')
root.destroy()
xlsx=bus_direc('.xls', EXC_OR)

erroneos=list()
analisis=list()

FF=list()
N_Or=list()
Nombre_new=list()
id_user=list()
CT_ZO=list()
line_or=list()
Tanda=list()
cant_codd=list()
infos_cel=list()



for Excel in xlsx:
    try:
        archivoLista=pd.read_excel(Excel) #Dataframe
        InfoLista=archivoLista.Barcode.head(1).iloc[0].replace(' ','').upper()#primer dato info
        if 'CT' not in InfoLista:
            erroneos.append(' '.join(['error de dato',Excel.split('/')[-1],InfoLista]))
            print('error de dato',Excel.split('/')[-1],InfoLista)
            pass
        InfoCT='CT'+InfoLista.split('CT')[1][0:2] #info ct
        FechaLista=Excel.split('/')[-2] #ifo Fecha
        userLista=Excel.split('/')[-1].split('-')[1] #Numero de Usuario
        archivoLinea=''
        for letra in InfoLista.split('CT')[0]:
            try: 
                int(letra)
                archivoLinea=archivoLinea+str(letra)
            except:pass
        if len(archivoLinea)==0:
            archivoLinea='XX'
        if 'M' in InfoLista.split('CT')[1]:
            InfoHorario='M'
        elif 'T' in InfoLista.split('CT')[1]:
            InfoHorario='T'
        else:
            erroneos.append(' '.join(['error horario tarde o mañana',Excel.split('/')[-1],InfoLista]))
            InfoHorario='X'
        
        print(InfoLista)
        print('_'.join([FechaLista,'U'+userLista,InfoCT,'L'+archivoLinea.zfill(2),InfoHorario]))
        
        N_Or.append(Excel.split('/')[-1])
        infos_cel.append(InfoLista)
        Nombre_new.append('_'.join([FechaLista,'U'+userLista,InfoCT,'L'+archivoLinea.zfill(2),InfoHorario]))
        CT_ZO.append(InfoCT)
        FF.append(FechaLista)
        id_user.append(userLista)
        line_or.append(archivoLinea)
        Tanda.append(InfoHorario)
        cant_codd.append(len(archivoLista.drop_duplicates('Barcode').query('Barcode.str.len()==14 and Barcode.str.contains("I") and Barcode.str.contains("4")')))
    except:
        erroneos.append(Excel.split('/')[-1])
        pass
        
    
    Cod_Lista=archivoLista.drop_duplicates('Barcode').query('Barcode.str.len()==14 and Barcode.str.contains("I") and Barcode.str.contains("4")')
    GPS_Lista=list(archivoLista.GPS)
    if len(Cod_Lista)%42!=0:
        analisis.append(f'Error de cantidad de codigos ({len(Cod_Lista)}) en {Excel}')
        pass
    if 'Unknown' in GPS_Lista:
        analisis.append(f'Error GPS en {Excel}')
        pass
    os.makedirs(Result+rf'/Listas/{InfoCT}', exist_ok=True)
    name_new='_'.join([FechaLista,'U'+userLista,InfoCT,'L'+archivoLinea.zfill(2),InfoHorario])+'.xlsx'
    shutil.copy(Excel,Result+rf'/Listas/{InfoCT}/{name_new}')
    
df2=pd.DataFrame()
df2['Fecha']=FF
df2['Nombre_Or']=N_Or
df2['Nombre_new']=Nombre_new
df2['id_user']=id_user
df2['CT_ZO']=CT_ZO
df2['line_or']=line_or
df2['Tanda']=Tanda
df2['cant_codd']=cant_codd
df2['infos_cel']=infos_cel


os.makedirs(Result+rf'/Reportes', exist_ok=True)
df2.to_excel(Result+rf'/Reportes/Reporte_Diario_{str(datetime.now().date())}.xls')

#%%#%% Procesar carpetas de exceles separadas por CT (usar nombre de carpeta como "CT02") PASO4
root=Tk()
sueltos = filedialog.askdirectory(title='Elija Carpeta de exceles Separados por CT')
root.destroy()

xlsx=bus_direc('.xls', sueltos) # Revisa si es EXCEL

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
CTT=list()
totald=list()
ll=list()
for ex in xlsx:
    Lec=pd.read_excel(ex)
    xl = pd.ExcelFile(ex)
    for BC,LATLON,DATE,II  in zip(Lec['Barcode'],Lec['GPS'],Lec['Date'],Lec['id']):
        if LATLON=='Unknown': 
            pass
        else:
            Change2.append('add')
            SheetName2.append(ex.split('/')[-1])
            Barcode2.append(BC) 
            lat2.append(float(LATLON.split(',')[0]))
            lon2.append(float(LATLON.split(',')[1]))
            ids2.append(II)
            Date2.append(DATE)
            ChangedBy2.append(f'sdlascan{ex.split("/")[-1].split("_")[1][-1:]}@gmail.com')
            ChangedOn2.append(DATE) 
            ChangedUsing2.append('Un Ladrillo')
            CTT.append(ex.split('/')[-2].replace('CT',''))
            totald.append(ex.split('/')[-1].split('_')[-2])
            ll.append(ex.split('/')[-1].split('_')[-3].replace('L',''))

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
df2['CT_LISTA']=CTT
df2['D']=totald
df2['linea']=ll

df2['Day']=df2['Date'].apply(Obtener_dia)

df2=df2.sort_values(['Date','ChangedBy','SheetName'],ignore_index=True)
Total=df2.copy()

Total['int']=Total['lat'].astype(str)+' '+Total['lon'].astype(str)
Total['X']=Total['int'].apply(lambda x: utm.from_latlon(float(x.split(' ')[0]), float(x.split(' ')[1]))[0])
Total['Y']=Total['int'].apply(lambda x: utm.from_latlon(float(x.split(' ')[0]), float(x.split(' ')[1]))[1])
del Total['int']
#Total['D']='?'
#filtro = Total.Date.dt.time < time(14, 0)
#Total.loc[filtro,'D']='M'
#filtro = Total.Date.dt.time >= time(14, 0)
#Total.loc[filtro,'D']='T'
EXX2=Total.copy()


EXX2['idlista']=0
#EXX2['CT_LISTA']='?'
EXX2['Xm']=0
cont_id=0
Comp=EXX2.copy()
EXX2=EXX2.drop_duplicates('Barcode',keep='last').copy()
EXX2['Barcode']=EXX2['Barcode'].astype('str')
EXX2['CT_LISTA']=EXX2['CT_LISTA'].astype('str')

os.makedirs(Result+rf'/Mapa', exist_ok=True)
EXX2.to_csv(Result+rf'/Mapa/TODO_EXCELES.csv',index=False)


Po=Po.sort_values(['X','Y'])

for DD in EXX2.Day.drop_duplicates().sort_values():
    Total_DD=EXX2.query('Day==@DD') #Filtrado por dia
    
    for User in Total_DD.ChangedBy.drop_duplicates().sort_values():
        Total_User=Total_DD.query('ChangedBy==@User')
        
        for ShNa in Total_User.SheetName.drop_duplicates().sort_values():
            cont_id+=1
            Total_ShNa=Total_User.query('SheetName==@ShNa')
            EXX2.loc[(EXX2['Day']==DD)&(EXX2['ChangedBy']==User)&(EXX2['SheetName']==ShNa),'idlista']=cont_id
            EXX2.loc[(EXX2['idlista']==cont_id), 'Xm']=mean(Total_ShNa.X)
            print(len(Total_ShNa),ShNa,cont_id)

EXX2=EXX2.query('Barcode.str.len()==14 and (Barcode.str.contains("I") | Barcode.str.contains("l")) and Barcode.str.contains("4") or Barcode=="ERROR-REPASAR"').copy().drop_duplicates('Barcode')

EXX2.to_csv(Result+rf'/Mapa/TODO_EXCELES.csv',index=False)

RESPALDO=EXX2.copy()
#EXX2=RESPALDO.copy()
for CCTT in Po.CT.drop_duplicates().sort_values():
    SCANS_use=EXX2.query('CT_LISTA==@CCTT')
    print(CCTT,len(SCANS_use))
    for idlis in SCANS_use.idlista.drop_duplicates():
        SCANS_list=SCANS_use.query('idlista==@idlis')
        if len(SCANS_list)%42!=0:
            shh=SCANS_list.SheetName.iloc[0]
            print(shh,len(SCANS_list))
#%%Testeos

a=Comp.query('SheetName=="12-03-2024_U04_CT64_L08_T_C252.xlsx"')
b=EXX2.query('SheetName=="12-03-2024_U04_CT64_L08_T_C252.xlsx"')
for nn in a.Barcode:
    if nn not in list(b.Barcode):
        print(nn)

print(Comp.query('Barcode=="461907l3201250"'))


for CCTT in Po.CT.drop_duplicates().sort_values():
    for Shh in EXX2.query('CT_LISTA==@CCTT').idlista.drop_duplicates():
        SCANS_use=EXX2.query('idlista==@Shh')
        print(CCTT,len(SCANS_use))
    sleep(4)
        




#%%Estudiar PASO5

#CT_LISTOS=['37','38?','39---','40','41','42','46','50','51','52','55','56','57','58','59','60','61','62','65']
#falta
CCTT="64"
SCANS_use=EXX2.query('CT_LISTA==@CCTT')
print(len(SCANS_use))
xxxxxx=SCANS_use.head(1).Barcode.iloc[0]
add=SCANS_use.head(1)
add['Barcode']=['461928I4240865']
SCANS_use=pd.concat([SCANS_use,add],axis=0).copy()
SCANS_use=SCANS_use.sort_values(['D','Xm','Date'])
print(len(SCANS_use))
#%%
#for CCTT in Po.CT.drop_duplicates().sort_values():
for CCTT in ['44']:
    anterior_flags=''
    SCANS_use=EXX2.query('CT_LISTA==@CCTT')
    #print(CCTT,len(SCANS_use))
    datos=''
    for lista in SCANS_use.sort_values('Xm').SheetName.drop_duplicates():
        SCANS_list=SCANS_use.query('SheetName==@lista')
        #print(lista,len(SCANS_list))
        largo=len(SCANS_list)
        Xmm=mean(SCANS_list.Xm)
        HORARIO=list(EXX2.loc[SCANS_list.index,'D'].drop_duplicates())[0]
        EXX2.loc[SCANS_list.index,'D']="Selec"
        EXX2.query('CT_LISTA==@CCTT').to_csv('test.csv',index=False)
        if SCANS_list.sort_values('Date').head(1).Y.iloc[0]>SCANS_list.sort_values('Date').tail(1).Y.iloc[0]:
            CODSUP=SCANS_list.sort_values('Date').tail(1).Barcode.iloc[0]
        else:CODSUP=SCANS_list.sort_values('Date').head(1).Barcode.iloc[0]
        
        datos=ventanaCapturaDatos(HORARIO,largo,lista,CODSUP)
        
        if datos=='Parar':
            EXX2.loc[SCANS_list.index,'D']=HORARIO
            break
        
        try:
            EXX2.loc[SCANS_list.index,'Xm']=Xmm+float((datos))
            EXX2.loc[SCANS_list.index,'D']=HORARIO
            EXX2.query('CT_LISTA==@CCTT').to_csv('test.csv',index=False)
            lista_or=lista
        except: 
            EXX2.loc[SCANS_list.index,'D']=HORARIO
            if datos=='A':
                lista=anterior_flags
                SCANS_list=SCANS_use.query('SheetName==@lista')
                #print(lista,len(SCANS_list))
                largo=len(SCANS_list)
                Xmm=mean(SCANS_list.X)
                HORARIO=list(EXX2.loc[SCANS_list.index,'D'].drop_duplicates())[0]
                EXX2.loc[SCANS_list.index,'D']="Selec"
                EXX2.query('CT_LISTA==@CCTT').to_csv('test.csv',index=False)
                datos=ventanaCapturaDatos(HORARIO,largo,lista)
                try:
                    EXX2.loc[SCANS_list.index,'Xm']=Xmm+float((datos))
                    EXX2.loc[SCANS_list.index,'D']=HORARIO
                    EXX2.query('CT_LISTA==@CCTT').to_csv('test.csv',index=False)
                except:
                    EXX2.loc[SCANS_list.index,'D']=HORARIO
                
        
                
                
        anterior_flags=lista_or
        if datos=='Parar':
            break
        
    
    if datos=='Parar':
        break            
    SCANS_use=EXX2.query('CT_LISTA==@CCTT').sort_values(['D','Xm','Date'])
    Volche=Po.query('CT==@CCTT').sort_values(['D','X','Y'])
    
    
    if len(SCANS_use)==len(Volche):
        print('ok')
        for XM in SCANS_use.Xm.drop_duplicates():
            Cues=SCANS_use.query('Xm==@XM').sort_values('Date')
            if Cues.head(1).Y.iloc[0]>Cues.tail(1).Y.iloc[0]:#Norte a sur, invertir
                CODES=list(reversed(list(Cues.Barcode)))
                TIMES=list(reversed(list(Cues.Date)))
                SCANS_use.loc[Cues.index,'Barcode']=CODES
                SCANS_use.loc[Cues.index,'Date']=TIMES
        #
        Po.loc[Volche.index,'COD']=list(SCANS_use.Barcode)
        Po.loc[Volche.index,'time']=list(SCANS_use.Date)
    

#%% EMISION PASO6




#CCTT='40'
for CCTT in Po.CT.drop_duplicates().sort_values():
    CT40=Po.query('CT==@CCTT').copy().sort_values(['CT','TRK','STRg','X','Y']).reset_index()      
    CT40['SI']=CT40.TRK.apply(lambda x: "SI "+ '.'.join(x.split('.')[1:4]))
    CT40['iNV']=CT40.TRK.apply(lambda x: x.split('.')[2])
    del CT40['index']
    CT40_=CT40.reindex(['time','COD','CT','iNV','SI','STRg','TRK','X','Y'],axis=1)
    CT40_.to_csv(f'EIFG-005-CSV-{str((int(CCTT)-36)).zfill(3)}-0 Listado módulos CT{CCTT}.csv',index=False)       

#%%ENCONTRAR ERRONEOS
#EXX2.to_csv(Result+rF'/BRUTO_EMISION.csv',index=False)

Prueba=list()
count=0
total=len(EXX2.query('ids==2').idlista.drop_duplicates())
CONCHALE=pd.DataFrame()
for N_Lista in EXX2.query('ids==2').idlista.drop_duplicates():
    count+=1
    if len(EXX2.query('idlista==@N_Lista and ids==2'))>2:
        CONCHALE=pd.concat([CONCHALE, EXX2.query('idlista==@N_Lista')], axis=0)
    print(f'ADV: {(total-count)/total}')
CONCHALE.to_csv('LOC.CSV', index=False)
    
#TE=CONCHALE.query('idlista==887')
for nn in CONCHALE.sort_values('CT_LISTA').idlista.drop_duplicates():
    TE=CONCHALE.query('idlista==@nn').sort_values('Date')
    #for n in range(int(len(TE)/(42/6))+1):
    for n in range(168,int(len(TE))-42):   
        #TE.head(int(n*(42/6))).to_csv('LOC.CSV', index=False)
        TE.head(int(n)).to_csv('LOC.CSV', index=False)
        sleep(0.3)

gap=5
compa=1
count=0
total=len(EXX2.idlista.drop_duplicates())
CONCHALE2=pd.DataFrame()
for N_Lista in EXX2.idlista.drop_duplicates():
    encontrado=False
    TE=EXX2.query('idlista==@N_Lista').reset_index().sort_values('Date').copy()
    del TE['index']
    ori=timedelta(hours=TE.Date.iloc[0].time().hour,minutes=TE.Date.iloc[0].time().minute,seconds=TE.Date.iloc[0].time().second)
    CORTES=list()
    if len(TE)%42==0:
        for di in range(int(len(TE)/42)+1):
            CORTES.append(42*di-1)
        CORTES[0]=0
        for nT in CORTES:
            ori=timedelta(hours=TE.Date.iloc[nT-compa].time().hour,minutes=TE.Date.iloc[nT-compa].time().minute,seconds=TE.Date.iloc[nT-compa].time().second)
            anti=timedelta(hours=TE.Date.iloc[nT].time().hour,minutes=TE.Date.iloc[nT].time().minute,seconds=TE.Date.iloc[nT].time().second)
            if anti-ori>timedelta(seconds=gap):
                encontrado=True
                TE.loc[TE['Date']==TE.Date.iloc[nT],'ids']=2
                print(anti-ori)
                
                
    if encontrado:
        CONCHALE2=pd.concat([CONCHALE2, TE], axis=0)
        #ori=timedelta(hours=TE.Date.iloc[nT].time().hour,minutes=TE.Date.iloc[nT].time().minute,seconds=TE.Date.iloc[nT].time().second)
    count=count+1
    print(f'ADV: {1-(total-count)/total}')

for elim in CONCHALE.idlista.drop_duplicates():
    CONCHALE2=CONCHALE2.query('idlista!=@elim')
    
CONCHALE2.to_csv('LOC.CSV', index=False)

Po['line']='?'
for ctt in Po.CT.drop_duplicates():
    ttr=Po.query('CT==@ctt')
    line=0
    for Xx in ttr.X.drop_duplicates().sort_values():
        line+=1
        Po.loc[ttr.query('X==@Xx').index,'line']=line

Po['YTM']='?'
Po['YTm']='?'
for tt in Po.TRK.drop_duplicates():
    CCC=Po.query('TRK==@tt')
    Po.loc[CCC.index,'YTM']=max(CCC.Y)
    Po.loc[CCC.index,'YTm']=min(CCC.Y)

#%%
TRKRS=list()
hora=list()
lineaA=list()
ctt=list()

for nn in list(CONCHALE2.sort_values('CT_LISTA').query('idlista>653').idlista.drop_duplicates()):
    TE=CONCHALE2.query('idlista==@nn')
    #for n in range(int(len(TE)/(42))+1):
    #    TE.head(int(n*(42))).to_csv('LOC.CSV', index=False)
    #    sleep(1)
    HORARIO=TE.D.iloc[0]
    largo=len(TE)
    lista=TE.SheetName.iloc[0]
    linea=int(TE.SheetName.iloc[0].split('L')[1][0:2])
    CTCT=TE.CT_LISTA.iloc[0]
    TE.to_csv('test.csv',index=False)
    TE=TE.sort_values('Date')
    if TE.head(1).Y.iloc[0]>TE.tail(1).Y.iloc[0]:
        CTCT2='N-S'
    else:
        CTCT2='S-N'
    datos=ventanaCapturaDatos(HORARIO,largo,lista,CTCT2)
    if datos=='Parar':
        break
    datos=int(datos)
    if int(datos)==0:
        pass
    if int(datos)>0:
        
        TE2=TE.iloc[42*(datos-1):42*(datos-1)+42]
        YMM=mean(TE2.Y)
        ORR=Po.query('Y>-3+@YMM and Y<3+@YMM and CT==@CTCT and line==@linea')
        TRKRS.append(ORR.TRK.drop_duplicates().iloc[0])
        hora.append(HORARIO)
        lineaA.append(linea)
        ctt.append(CTCT)

ENTR=pd.DataFrame()
ENTR['TRKRS']=TRKRS
ENTR['hora']=hora
ENTR['lineaA']=lineaA
ENTR['ctt']=ctt

ENTR.to_csv('TRK_REPA.csv',index=False)
    
    
    
