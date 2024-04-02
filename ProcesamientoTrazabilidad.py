# -*- coding: utf-8 -*-

import pandas as pd
import datetime
from datetime import datetime, timedelta, time
from tkinter import *
from tkinter import filedialog
import utm
from time import sleep
import os
import shutil
from statistics import mean
import openpyxl
from tqdm import tqdm, trange

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


def opcion_1(dirPrincipal,dirResultados):

    print("Paso 2: DataFrame con centroides")
    dir_centroide = filedialog.askopenfilename(title='Elija Excel Con centroides',initialdir=dirPrincipal)
    Po=pd.read_csv(dir_centroide)
    Po.columns=['X','Y','TRK','STRg']

    Po['CT']=Po.TRK.apply(lambda x: x.split('.')[1])
    Po['X']=Po.X.apply(lambda x: round(x,1))

    # Se crean 3 columnas más con datos ?

    Po['COD']='?'  # Columna para codigos inicializada con ?
    Po['D']='?'    # Columna D para la tanda inicializada con ?
    Po['time']=datetime(2,2,2) # Columna Time con la fecha

    # Creación de listas para crar dataframe poStats
    campo=list()
    Xme=list() # Xme -> media de coordenadas X
    Ysup=list() #Ysup -> coordenada Y superior
    Yinf=list() #Yinf -> coordenada Y inferior
    Cantp=list() #Cantp -> Cantidad de paneles
    side=list() #side -> Tanda


    for ct in tqdm(Po.CT.drop_duplicates().sort_values(), desc= "Cargando Centroides"):
        # Se crea Po_ex
        # Se filtra por CT y se eliminan los duplicados y ordenando los valores
        Po_ex=Po.query('CT==@ct') # Se filtra por CT
        i=0
        for Xs in Po_ex.X.drop_duplicates().sort_values():
            # Se filtra por "x" eliminado los duplicados y ordenando los valores
            Po_Xs=Po_ex.query('X==@Xs').sort_values('Y') # ordena las columnas(x) y dentro ordena los paneles(y)
            compa=min(Po_Xs.Y) # Toma el menor valor de x (Panel)

            separar=False
            for Ys in Po_Xs.Y: # Revisa si la diferencia en distancia entre un panel y otro es mayor a 10
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


    Po_stats=pd.DataFrame() # Se crea data frame con información procesada de los centroides

    Po_stats['CT']=campo
    Po_stats['Xmed']=Xme
    Po_stats['Ysup']=Ysup
    Po_stats['Yinf']=Yinf
    Po_stats['Cant_p']=Cantp
    Po_stats['side']=side

    # se crea objetos con atributos con iterrows
    for ind,row in Po_stats.iterrows():
        dat=Po[(Po['X']==row['Xmed'] )&( Po['Y']>=row['Yinf'])&(Po['Y']<=row['Ysup'])].index
        Po.loc[dat,'D']=row['side']


    for CR in tqdm(Po.CT.drop_duplicates().sort_values(),desc="Ordenando Datos"):
        count=0.5
        nyn=Po.query('CT==@CR')
        for Xx in nyn.X.drop_duplicates().sort_values():
            count=count+0.5
            fil=nyn.query('X==@Xx')
            Po.loc[fil.index,'line']=str(int(count))

    Po.to_csv(dirResultados+r'/TabladeEmision.csv',index=False) # Deja un archivo csv con los datos procesados en la etapa 1
    Po_stats.to_csv(dirResultados+r'/TabladeEstadisticas.csv',index=False) # Archivo de control para etapas posteriores

    print(f"OUTPUT 1: {dirResultados}/TabladeEmision.csv")
    print(f"OUTPUT 2: {dirResultados}/TabladeEstadisticas.csv")
    print("-------------------------------------------------------------")
    #return Po_stats,Po # output Po_stat = estadisticas, Po = tabla de emisión # Ca

def opcion_2(dirPrincipal, dirReportes, dirListas):
    print("Paso 3: Conversión de archivos crudos")
    dir_excelOriginales = filedialog.askdirectory(title='Carpeta de Descargas',initialdir=dirPrincipal)
    xlsx=bus_direc('.xls', dir_excelOriginales) #Busca directorios al interior de esa carpeta

    # Creación de listas
    erroneos=list()
    analisis=list()

    FF=list() # Fecha de listas
    N_Or=list() # Nombre original de las listas
    Nombre_new=list() # Nombre nuevo de listas
    id_user=list() # Id de usuario que escanea
    CT_ZO=list()    # Nombre de CT extraido del interior de la lista (Dato ingresado desde usuario)
    line_or=list()  # Linea extraida del interior del archivo (Dato ingresado desde usuario)
    Tanda=list()    # Medición de tarde o mañana (Dato ingresado desde usuario)
    cant_codd=list() # Cantidad de codigos que contiene la lista
    infos_cel=list()    # información introducida por el usuario en los excel

    for Excel in tqdm(xlsx):
        try:
            archivoLista = pd.read_excel(Excel) #Dataframe
            InfoLista = archivoLista.Barcode.head(1).iloc[0].replace(' ','').upper()#primer dato info
            if 'CT' not in InfoLista:
                erroneos.append(' '.join(['error de dato',Excel.split('/')[-1],InfoLista]))
                print('error de dato',Excel.split('/')[-1],InfoLista)
                break
            InfoCT='CT'+InfoLista.split('CT')[1][0:2] #info ct
            FechaLista=Excel.split('/')[-2] #info Fecha
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

            #print(InfoLista)
            #print('_'.join([FechaLista,'U'+userLista,InfoCT,'L'+archivoLinea.zfill(2),InfoHorario]))
            n_cod=len(archivoLista.drop_duplicates('Barcode').query('Barcode.str.len()==14 and Barcode.str.contains("I") and Barcode.str.contains("4")'))
            N_Or.append(Excel.split('/')[-1])
            infos_cel.append(InfoLista)
            Nombre_new.append('_'.join([FechaLista,'U'+userLista,InfoCT,'L'+archivoLinea.zfill(2),InfoHorario,'C'+str(n_cod).zfill(3)]))
            CT_ZO.append(InfoCT)
            FF.append(FechaLista)
            id_user.append(userLista)
            line_or.append(archivoLinea)
            Tanda.append(InfoHorario)
            cant_codd.append(n_cod)
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
        #os.makedirs(dirPrincipal+rf'/Listas/{InfoCT}', exist_ok=True)

        os.makedirs(dirListas + rf'/{InfoCT}', exist_ok=True)

        #name_new='_'.join([FechaLista,'U'+userLista,InfoCT,'L'+archivoLinea.zfill(2),InfoHorario])+'.xlsx'
        name_new = '_'.join([FechaLista, 'U' + userLista, InfoCT, 'L' + archivoLinea.zfill(2),InfoHorario,'C' + str(n_cod).zfill(3)]) + '.xlsx'

        # Directorio de Zonas
        shutil.copy(Excel,dirPrincipal+rf'/Listas/{InfoCT}/{name_new}')

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

    # **** Directorio de Reporte ****
    df2.to_csv(dirReportes + rf'/Reporte_Diario_{str(datetime.now().date())}.csv')
    pd.DataFrame(erroneos).to_csv(dirReportes + rf'/Listas_Erroneas_{str(datetime.now().date())}.csv')

    print(f"OUTPUT 1: {dirReportes}/Reporte_Diario_{str(datetime.now().date())}.csv")
    print(f"OUTPUT 2: {dirReportes}/Listas_Erroneas_{str(datetime.now().date())}.csv")
    print(f"OUTPUT 3: Listas por zonas: {os.listdir(dirListas)}")
    print("-------------------------------------------------------------")

def opcion_3(dirPrincipal,dirMapa):
    print("Paso 4: Procesamiento de listas")

    dir_listasCts = filedialog.askdirectory(title='Elija Carpeta de exceles Separados por CT',initialdir=dirPrincipal)
    xlsx=bus_direc('.xls', dir_listasCts) # Revisa si es EXCEL

    # Creación de listas auxiliares
    Change2=list()          #
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
    zonaCT=list()
    totald=list()
    ll=list()

    for ex in tqdm(xlsx, desc= "Cargando Listas"):
        Lec=pd.read_excel(ex)
        #xl = pd.ExcelFile(ex)
        #print(ex)
        for BC,LATLON,DATE,II in zip(Lec['Barcode'],Lec['GPS'].astype('str'),Lec['Date'],Lec['id']):
            if LATLON == 'Unknown':
                pass
            else:
                Change2.append('add')
                SheetName2.append(ex.split('/')[-1])
                Barcode2.append(BC)
                lat2.append(float(LATLON.split(',')[0]))
                lon2.append(float(LATLON.split(',')[1]))
                ids2.append(II)
                Date2.append(DATE)
                ChangedOn2.append(DATE)
                ChangedUsing2.append('Un Ladrillo')
                zonaCT.append(ex.split('/')[-2].replace('CT', ''))
                
                if len(ex.split('/')[-1].split('_')) == 6:
                    totald.append(ex.split('/')[-1].split('_')[-2])
                    ll.append(ex.split('/')[-1].split('_')[-3].replace('L', ''))
                    ChangedBy2.append(f'sdlascan{ex.split("/")[-1].split("_")[1][-1:]}@gmail.com')


                elif len(ex.split('/')[-1].split('_')) == 7:
                    totald.append(ex.split('/')[-1].split('_')[-3])
                    ll.append(ex.split('/')[-1].split('_')[-4].replace('L', ''))
                    ChangedBy2.append(f'sdlascan{ex.split("/")[-1].split("_")[1][-1:]}@gmail.com')
                    
                else:
                    print(ex,len(ex.split('/')[-1].split('_')))

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
    df2['CT_LISTA']=zonaCT
    df2['D']=totald
    df2['linea']=ll

    df2['Day']=df2['Date'].apply(Obtener_dia)

    print("Preparando Listas")
    df2=df2.sort_values(['Date','ChangedBy','SheetName'],ignore_index=True)
    Total=df2.copy()

    Total['int']=Total['lat'].astype(str)+' '+Total['lon'].astype(str)
    Total['X']=Total['int'].apply(lambda x: utm.from_latlon(float(x.split(' ')[0]), float(x.split(' ')[1]))[0])
    Total['Y']=Total['int'].apply(lambda x: utm.from_latlon(float(x.split(' ')[0]), float(x.split(' ')[1]))[1])
    del Total['int']

    print("*")
    EXX2=Total.copy()

    EXX2['idlista']=0
    EXX2['Xm']=0
    cont_id=0
    Comp=EXX2.copy()
    print("*")
    EXX2=EXX2.drop_duplicates('Barcode',keep='last').copy()
    EXX2['Barcode']=EXX2['Barcode'].astype('str')
    EXX2['CT_LISTA']=EXX2['CT_LISTA'].astype('str')


    # Avance Filtrado -> Mapa
    EXX2.to_csv(dirMapa+rf'/TodoEscaneos.csv',index=False)


    for DD in tqdm(EXX2.Day.drop_duplicates().sort_values(),desc="Revision de Listas "):
        Total_DD=EXX2.query('Day==@DD') #Filtrado por dia

        for User in Total_DD.ChangedBy.drop_duplicates().sort_values():
            Total_User=Total_DD.query('ChangedBy==@User')

            for ShNa in Total_User.SheetName.drop_duplicates().sort_values():
                cont_id+=1
                Total_ShNa=Total_User.query('SheetName==@ShNa')
                EXX2.loc[(EXX2['Day']==DD)&(EXX2['ChangedBy']==User)&(EXX2['SheetName']==ShNa),'idlista']=cont_id
                EXX2.loc[(EXX2['idlista']==cont_id), 'Xm']=mean(Total_ShNa.X)
                #print(len(Total_ShNa),ShNa,cont_id)

    EXX2=EXX2.query('Barcode.str.len()==14 and (Barcode.str.contains("I") | Barcode.str.contains("l")) and Barcode.str.contains("4") or Barcode=="ERROR-REPASAR"').copy().drop_duplicates('Barcode')

    # Avance Filtrado
    EXX2.to_csv(dirMapa+rf'/TodoEscaneos_filtrado.csv',index=False)
    
    print(f"OUTPUT 1: {dirMapa}/TodoEscaneos.csv -> Revisión avance desde QGIS")
    print(f"OUTPUT 2: {dirMapa}/TodoEscaneos_filtrado.csv -> Revisión avance filtrado desde QGIS")
    print("-------------------------------------------------------------")

def opcion_4(dirPrincipal,dirMapa):

    print("Paso 5: Correccion de centroides")
"""
    
    EXX2 = filedialog.askopenfilename(title='TodoEscaneos_filtrado', initialdir=dirMapa)
    
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
    for CCTT in ['48']:
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
"""
def opcion_5(dirEmision,dirMapa,dirResultados):
    print("Paso 6: Emision Tratamientos")

    EXX2 = pd.read_csv(filedialog.askopenfilename(title='TodoEscaneos_filtrado.csv', initialdir=dirMapa))
    Po = pd.read_csv(filedialog.askopenfilename(title='TabladeEmision.csv', initialdir=dirResultados))
    Po['line']=Po['line'].apply(lambda x: str(x).zfill(2))
    for CCTT in tqdm(Po.CT.drop_duplicates().sort_values(),desc="Volcado de lineas - codigos - Horarios"):
        for tanda in ['M', 'T']:
            SCANS_use = EXX2.query('CT_LISTA==@CCTT and D==@tanda')
            Volche = Po.query('CT==@CCTT and D==@tanda').sort_values(['X', 'Y'])
            for lin in Volche.line.drop_duplicates():
                V_ = Volche.query('line==@lin').sort_values(['X', 'Y'])
                Cues = SCANS_use.query('linea==@lin.zfill(2)')
                if len(V_)==len(Cues):
                    if Cues.head(1).Y.iloc[0] > Cues.tail(1).Y.iloc[0]:  # Norte a sur, invertir
                        CODES = list(reversed(list(Cues.Barcode)))
                        TIMES = list(reversed(list(Cues.Date)))
                        Cues.loc[Cues.index, 'Barcode'] = CODES
                        Cues.loc[Cues.index, 'Date'] = TIMES
                    Po.loc[V_.index, 'COD'] = list(Cues.Barcode)
                    Po.loc[V_.index, 'time'] = list(Cues.Date)

    for CCTT in Po.CT.drop_duplicates().sort_values():
        CT40 = Po.query('CT==@CCTT').copy().sort_values(['CT', 'TRK', 'STRg', 'X', 'Y']).reset_index()
        CT40['SI'] = CT40.TRK.apply(lambda x: "SI " + '.'.join(x.split('.')[1:4]))
        CT40['iNV'] = CT40.TRK.apply(lambda x: x.split('.')[2])
        del CT40['index']
        CT40_ = CT40.reindex(['time', 'COD', 'CT', 'iNV', 'SI', 'STRg', 'TRK', 'X', 'Y'], axis=1)

        CT40_.to_csv(dirEmision + rf'/EIFG-005-CSV-{str((int(CCTT) - 36)).zfill(3)}-0 Listado módulos CT{CCTT}.csv', index=False)


def salir():
    print("Saliendo del programa...")

# Definición de rutas
ruta_script = os.path.dirname(os.path.realpath(__file__))
dir_principal = ruta_script
os.makedirs(dir_principal+rf'/Resultados', exist_ok=True) # Crea carpeta resultados
dir_resultados = dir_principal+"/Resultados"

os.makedirs(dir_principal+rf'/Emision', exist_ok=True) # Crea carpeta resultados
dir_emision = dir_principal+"/Emision"

os.makedirs(dir_principal+rf'/Mapa', exist_ok=True) # Crea carpeta resultados
dir_mapa = dir_principal+"/Mapa"

os.makedirs(dir_principal+rf'/Reportes', exist_ok=True) # Crea carpeta resultados
dir_reportes = dir_principal+"/Reportes"

os.makedirs(dir_principal+rf'/Listas', exist_ok=True) # Crea carpeta resultados
dir_listas = dir_principal+"/Listas"

os.makedirs(dir_principal+rf'/Descargas', exist_ok=True) # Crea carpeta resultados
dir_descargas = dir_principal+"/Descargas"

while True:
    print("** Procesamiento Trazabilidad **")
    print(" - Menu - ")
    print("Paso 1: Cargar archivo de Centroides Original")
    print("Paso 2: Preproceso de listas (Renombrar listas y ubicarlas en zonas)")
    print("Paso 3: Creación y actualización de Avance")
    print("Paso 4: Correccion de centroides") #Se utiliza cuando no hay separacion previa de lineas
    print("Paso 5: Emisión")
    print("Salir - 6")

    seleccion = input("Por favor, selecciona una opción: ")

    if seleccion == '1':
        opcion_1(dir_principal, dir_resultados)
    elif seleccion == '2':
        opcion_2(dir_principal,dir_reportes,dir_listas)
    elif seleccion == '3':
        opcion_3(dir_principal, dir_mapa)
    elif seleccion == '4':
        opcion_4(dir_principal, dir_mapa)
    elif seleccion == '5':
        opcion_5(dir_emision,dir_mapa,dir_resultados)
    elif seleccion == '6':
        break
    else:
        print("Selección no válida. Por favor, selecciona una opción válida.")


