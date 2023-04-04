import requests
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import csv
import time
import sys
import re


from bd import *


urlImdb =       "https://www.imdb.com/"
urlStringList=      "list/"
UrlStringTittle=    "lists/"
urlToExport=    "/export?ref_=ttls_otexp"

# # [SCRAPPER] Numero de consultas(peticiones) que se ha hecho

def obtenerNumIteraciones( number ):
    
    nIteration = 1    
   
    if number >= 100:
        
        nIteration = int( number/100 )+1
      
        
    return nIteration

# # [SCRAPPER] Se obtiene informacion referente a una lista

def obtenerInfoDeLista( lists ):

    print("\n Obteniendo metadata de %s listas" %( len(lists) ) )
    
    resultList = []
    
    #RECORRO LAS LISTAS Y SACO LA INFORMACIÓN
    
    for list in lists:
        
        collectorList = []
        
        #OBTENGO EL NOMBRE DE LA LISTA
        
        infoList = list.find( "div" , {"class": "list_name"} )
        
        nameList = infoList.find( "a" )    
        
        collectorList.append( nameList.text )


        #OBTENGO EL LINK DE LA LISTA

        linkList = infoList.find( 'a', href = True) 
        
        collectorList.append( linkList[ 'href' ] )
        


        #OBTENGO LA METADATA DE LA LISTA
        
        metadataList = list.find( "div" , {"class": "list_meta"} )
        
        collectorList.append( metadataList.text )

        resultList.append( collectorList )
        
    return resultList

# # [SCRAPPER] Se modifica la URL para modificar a traves de las paginas

def modificarNumPagina( url, number ):
    
    
    url += "?page=%d"%number #url formatada para rec
    print("url number pagina", url)
    return  url
  
# # [SCRAPPER] Se descarga excel que contiene el listado de peliculas de una lista

def descargarExcelDeLista( idList ):
    #ok
    #Esta funcion descarga el excel y lo almacena temporalmente de manera local
    # input idList: string con url de una lista      
    #           ej: "ls092155333"
    #return fileName: El nombre del archivo que guardó
    
    print("\n descargarExcelDeLista:",urlImdb, urlStringList, idList, urlToExport)
        
    url = urlImdb + urlStringList + idList + urlToExport
    
    print("\n Se descargará: ", url )    
    
    time.sleep( 5 )
    
    http = urllib3.PoolManager()
    
    r = http.request('GET', url, preload_content=False)
    
    if r.status == 200:
        
        print("\n Descargando excel de lista [%s]..." %( idList ) )
        
        fileName= idList+".csv"
        
        with open( fileName, 'wb' ) as out:
            
            while True:
                
                data = r.read()
                
                if not data:
                    
                    break
                
                out.write( data )
    else:
        
        print("\n NO SE PUDO DESCARGAR LISTA [%s] STATUS CODE [%s]"%( idList, r.status ) )
        
        return False
    
    r.release_conn()
    
    print("\n Lista [%s] se guardó su excel con nombre [%s]"%( idList, fileName ) )
    
    return fileName

# # [SCRAPPER] Función que comienza el proceso de descargar listados de peliculas relacionadas al ID de una pelicula

def obtenerListasDesdeTitulo( idTittle ):
    
    #Input url = https://www.imdb.com/lists/tt0074486?ref_=tt_rls_sm
    
    #return lista= con metadatos [0]-> [Nombre, idList, metadatos]
    
    #Esta Función descarga todas las listas asociadas al ID de una película. Navega por el dominio de IMDB
    
    countPage = 1 #contador que irá aumentando para buscar más páginas con listas asociadas a la pelicula buscada. Minimo debe ser 1
    
    url= urlImdb + UrlStringTittle + idTittle

    url = modificarNumPagina( url, countPage ) #string de la URL que se le concatena el número de páginas

    r = requests.get( url ) #obtiene la petición a la URL
    
    html_content = r.text #se "parsea" la petición a string (texto)
    
    soup = BeautifulSoup( html_content, 'lxml' ) #se crea una instancia de BeatifulSoup, librería usada para navegar por el DOM HTML
          
    countIterations = 0 #contador que irá indicando las iteraciones (páginas) que se encuentra posicionado en la función
    
    resultList = None # colección que guardará la información extraidas de las páginas
    
    countNot200 = 0 #contador que indicará el límite de peticiones rechazadas por IMDB
    
    numPaginas= int(soup.findAll("span", {"class":"list-pagination-total-elements"})[0].string)
    

 
    #while countIterations < nIterations:
    
    while numPaginas > 0:
        
        time.sleep(10) # se da una pausa de 10 segundo, para no saturar de peticiones a IMDB
        print("\n Numero de paginas", numPaginas)
            
        if r.status_code == 200:
            print("\nScrapeando: ",url)
            
            countNot200 = 0
            
            html_content = r.text
            
            soup = BeautifulSoup( html_content, 'lxml' )
            
            #OBTENGO TODAS LAS LISTAS
            
            lists = soup.findAll( "div", { "class": "list-preview" } ) #se obtiene del DOM metadata asociada a la listas 
            
            resultList = obtenerInfoDeLista( lists )
            
            countPage += 1
            
            url = url.split( '?',1 )[0]
            
            url = modificarNumPagina( url, countPage )
            
            r = requests.get( url )
            
            numPaginas -= 100

        elif countNot200 >= 4:
            
            print ( "ERROR AL DESCARGAR LISTAS: Se guardaron solo: " ,countIterations )
            
            return resultList
        
        else:
            print("\n La petición arrojó un error. Intento: ", countNot200)
            countNot200 += 1
    
    print ( "Se guardaron bien todas las  listas\n" )    
    return resultList

# # [SCRAPPER] Proceso de rescatar los datos del excel descargado

def leerExcelYGuardarInfo( fileName ):
    #Esta funcion lee un excel y guarda la información leida en la BD
    # input fileName: referencia al nombre de la lista que se leerá en excel || ej: ls080428597
    
    print("\n Comienza proceso de leer excel[%s] y guardar su metadata..."%( fileName ) )
    
    if fileName == False:
        
        print("\n No se puede leer archivo[%s]"%( fileName ) )
        
        return fileName
    
    if (fileName.find('.csv') == -1):
        
        idList = fileName
        
        fileName += ".csv"
    
    else:
        
        idList = fileName.split( '.', 1 )[0]
    
    with open( fileName, 'r' ) as file:
        
        reader = csv.reader( file, delimiter = ',' )
        
        countRow = 0
        
        print("\nLeyendo archivo [%s] y guardando su información..."%( fileName ) )
        
        for row in reader:
            
            if countRow >0 :
                print("\nValidando:",idList, row[1])
                
                if not existeAsociacionListaTittle(idList, row[1]):

                    print("\nNo estaba almacenado asociación entre: ",idList, row[1] )

                    instertarListTittleList( idList, row[1] )
                else:
                    print("\nYa estaba almacenado asociación entre: ",idList, row[1] )
                
                if not ( existeMetadaDeTittle( row[1] ) ):                        
                    print("Guardando metadata de: ",row[1] )
                    instertarTittleList( row[1], row[2], row[3], row[4] ,row[5], row[6], row[7], row[8], row[9], row[10], row[13] )                  
                else:
                    print("\nYa estaba guardada la metadata de : ", row[1] )
                

            countRow += 1
            
        print( "\n[%s] Registros guardados"%( countRow-1 ) )
        file.close()
    return True

# # [SCRAPPER] Leer excel y guardar su contenido en BD

def descargarGuardarInfoList( idList ):
    #Esta funcion comienza el proceso de descarga de una lista
    
    flag = False
    
    fileNameList = descargarExcelDeLista( idList )
    
    if fileNameList != False:
        
        dataCsv = leerExcelYGuardarInfo( fileNameList )
        
        if dataCsv != False:
            
            flag = True
            
            print( "\n Lista[%s] se guardó con éxtio" % ( idList ) )
    
    return flag

# # [SCRAPPER] Proceso de selección del tipo de descarga

def startScrapper( idElement, idListToCompare = None ):
    #Esta funcion comienza el proceso de descarga de contenido dependiendo si 
    # idElement puede ser una el ID de una lista o de una pelicula
    #   ejemplo de ID lista    -> "ls021428038"
    #   ejemplo de ID pelicula -> "tt0074486"
    # tipoDescarga puede tomar 2 valores objetivos:
    #   1-> Descarga una lista por ID de una lista
    #   2-> Descarga una lista por ID de una pelicula
    # idListToCompare puede ser un string o list
    #   string-> es unicamente un ID de una lista 
    #   list  -> es una lista de ID de listas
    
    
    #TODO: CUANDO ES PELICULA GUARDAR EN LA PAGINA QUE QUEDO PARA COMENZAR LA SIGUIENTE DESCARGA DESDE ESA PAGINA
    
    
    if not isinstance(idElement,str):
        print("\n idElement ingresado tipo incorrecto: ", type(idElement))
        return False

    if  re.findall("^ls", idElement):
        tipoDescarga = 1
    else:
        if re.findall("^tt", idElement):
            tipoDescarga = 2
        else:
            print("\n idElement con formato incorrecto: ", idElement )
            return False

    print("\n Comenzando comprobación y descarga de información OriginList[%s] tipoDescarga[%s]" % ( idElement, tipoDescarga ) )
    if  tipoDescarga == 1:
        
        print("\n Procesando descarga de una lista directamente...")    
 
        descargarGuardarInfoList( idElement )       

        if isinstance( idListToCompare, list ):
            
            print("\nDescargando %s listas..." %( len(idListToCompare) )   )

            for idListToCompareAux in idListToCompare:    
               
                print("\n Guarando info de: " , idListToCompareAux  )
                
                descargarGuardarInfoList(idListToCompareAux)                
        else:
                       
            print("[listToCompare] Descargando lista:", idListToCompare)
            
            descargarGuardarInfoList( idListToCompare )
                
            
    
    if  tipoDescarga == 2:
        
        # Descarga de listas en base a una pelicula
        
        listas = obtenerListasDesdeTitulo( idElement )
        
        toolbar_width = 40
        
        totalIteration = len( listas )
        
        countAdvance = 1
        
        # setup toolbar
        
        sys.stdout.write( "[%s]" % (" " * toolbar_width ) )
        
        #sys.stdout.flush()
        
        sys.stdout.write( "\b" * ( toolbar_width +1 ) ) # return to start of line, after '['
        
        
        #TODO: DEJAR ESTE PRCESO EN UN METODO APARTE
        
        for lista in listas:
            
            # update the bar
            
            sys.stdout.write( "\r %d de %d" % ( countAdvance, totalIteration ) )

            countAdvance += 1
            
            sys.stdout.flush()
            
            time.sleep( 5 )
            
            idImdb = lista[ 1 ]
            
            idImdb = idImdb.split( '/', 2 )[-1]        

            if not ( existeMetadataDeLista( lista[1] ) ):    

                instertarLista( lista[0], lista[1], lista[2], idImdb )
                descargarGuardarInfoList(idImdb)
        
        sys.stdout.write( "]\n" ) # this ends the progress bar
    
       
    print( "\n ¡Proceso finalizado!" )

