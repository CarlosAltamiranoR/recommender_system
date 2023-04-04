import sys
import os
import pymysql
import pandas as pd
from numpy import *
host = os.getenv('localhost')
port = os.getenv('MYSQL_PORT')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DATABASE')


conn = pymysql.connect(
    host = host,
    port = int(3306),
    user = "root",
    passwd ="",
    db = "recommender_system",
    charset = 'utf8mb4')


#================================================EXISTE=======================================================
    
#existeListaPorId
def existeMetadataDeLista( idImdb ):

    exist = True

    sql  = " SELECT * FROM lists WHERE idImdb = %s "

    with conn.cursor() as cursor:

        row_count = cursor.execute( sql, (idImdb) )

        if row_count == 0:

            exist = False

    return exist

# # [BD] Comprueba si una lista está registrada en List_tittlelist
#existeEnListTittleList
def existeListaEnAsociacion( idImdb ):

    exist = True

    sql  = " SELECT * FROM list_tittlelist WHERE id_list = %s "

    with conn.cursor() as cursor:

        row_count = cursor.execute( sql, ( idImdb ) )

        if row_count == 0:

            exist = False

    return exist

def existeTittleEnAsociacion( idTittle ):

    exist = True

    sql  = " SELECT * FROM list_tittlelist WHERE id_tittlelist = %s "

    with conn.cursor() as cursor:

        row_count = cursor.execute( sql, ( idTittle ) )

        if row_count == 0:

            exist = False

    return exist
# # [BD] Consulta si un tittle (pelicula) existe
# existeTittlePorId
def existeMetadaDeTittle( tconst ):

    exist = True

    sql  = " SELECT * FROM tittle_list WHERE tconst = %s "

    with conn.cursor() as cursor:

        row_count = cursor.execute( sql, ( tconst ) )

        if row_count == 0:

            exist = False

    return exist


#existeListTittleList
def existeAsociacionListaTittle(id_list, id_tittlelist):

    exist = True

    sql  = "SELECT * FROM list_tittlelist where id_list =%s AND id_tittlelist =%s"

    with conn.cursor() as cursor:

        row_count = cursor.execute( sql, ( id_list, id_tittlelist ) )

        if row_count == 0:

            exist = False

    return exist
    
#================================================INSERTAR=======================================================
# # [BD] Insertar información descriptiva de una lista

def instertarLista( name, link, metadata, idImdb ):

    with conn.cursor() as cursor:

        # CREA UNA NUEVA FILA

        sql = "INSERT INTO lists ( name, link, metadata, idImdb ) VALUES ( %s, %s, %s,%s )"

        cursor.execute( sql,( name, link, metadata, idImdb ) )

        #GUARDAMOS LOS CAMBIOS

        conn.commit()


# # [BD] Inserta asosiciaion pelicula-lista (tabla n:n)

def instertarListTittleList( id_list, id_tittlelist):
    
    with conn.cursor() as cursor:

        # CREA UNA NUEVA FILA

        sql = "INSERT INTO list_tittlelist ( id_list, id_tittlelist ) VALUES ( %s, %s )"

        cursor.execute( sql,( id_list, id_tittlelist ) )

        #GUARDAMOS LOS CAMBIOS

        conn.commit()
        print("\n[BD]Guardando asociación id_list[%s] id_tittlelist[%s]" %(id_list, id_tittlelist ))

# # [BD] Inserta información de peliculas

def instertarTittleList( tconst, f_created, f_modified, description, name_tittle, url, tittle_type, imdb_rating, runtime_mins, year, release_date):

    with conn.cursor() as cursor:

        # CREA UNA NUEVA FILA

        sql = "INSERT INTO tittle_list ( tconst, f_created, f_modified, description, name_tittle, url, tittle_type, imdb_rating, runtime_mins, year, release_date ) VALUES ( %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s)"

        cursor.execute( sql,( tconst, f_created, f_modified, description, name_tittle, url, tittle_type, imdb_rating, runtime_mins, year, release_date ) )


        #GUARDAMOS LOS CAMBIOS

        conn.commit()

#================================================OBTENER=======================================================
# # [BD] OBTENGO TODAS LAS PELICULAS DE UNA LISTA

def obtenerTituloDesdeLista(idList):

    sql  = " SELECT id_tittlelist FROM list_tittlelist  where id_list = %s "
    result=[]
    with conn.cursor() as cursor:

        resultAux = cursor.execute( sql, ( idList ) )

        if result == 0:

            return -1

        resultAux= cursor.fetchall()

        for i in resultAux:
            for j in i:
                result.append(j)

    return result


# # [BD] OBTENGO TODAS LAS LISTAS DE UNA PELICULA

def obtenerListasDesdePelicula(idTittle):

    sql  = " SELECT id_list FROM list_tittlelist  where id_tittlelist= %s "
    result=[]
    with conn.cursor() as cursor:

        resultAux = cursor.execute( sql, ( idTittle ) )

        if result == 0:

            return -1

        resultAux= cursor.fetchall()

        for i in resultAux:
            for j in i:
                result.append(j)

    return result

def obtenerNombresPeliculas(idTittle):
    
    result= []

    if isinstance(idTittle,list ):
        for tittle in idTittle:
                result.append(obtenerNombresPeliculas(tittle))
    else:

        sql  = " select name_tittle from tittle_list where tconst= %s"

        with conn.cursor() as cursor:

            result = cursor.execute( sql, ( idTittle ) )

            if result == 0:

                return -1

            result= cursor.fetchall()


    return result

#================================================MISCELANEOS=======================================================
# # [BD] Buscar si una pelicula dentro de una lista existe

def validarPeliculaEnLista( idList, idTitleList ):

    exist = True

    sql  = "SELECT * FROM list_tittlelist where id_list=%s AND id_tittlelist=%s"

    with conn.cursor() as cursor:

        row_count = cursor.execute( sql, ( idList, idTitleList ) )

        if row_count == 0:

            exist = False

    return exist

# # [BD] Total de peliculas guardadas (S)


def totalDeTitulosGuardados(  ):

    sql  = "SELECT COUNT(DISTINCT(tconst)) FROM tittle_list "

    with conn.cursor() as cursor:

        cursor.execute( sql )

        value = cursor.fetchall()

        if len(value) <= 0:

            return None

    return value


def totalTittlesEnLista(idList):      


    sql  = "SELECT COUNT(id_list) FROM list_tittlelist where id_list=%s "

    with conn.cursor() as cursor:

        cursor.execute( sql, (idList) )

        value = cursor.fetchall()

        if len(value) <= 0:

            return None

    return value

