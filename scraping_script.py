import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from unidecode import unidecode
import os
import time
import random
import logging
import pickle
import urllib.robotparser

# Configuración del registro de logs
logging.basicConfig(filename='scraping.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Crear una sesión global para reutilizar conexiones
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (compatible; YourBotName/1.0; +http://yourwebsite.com/bot)'
})

def is_allowed(url):
    # Función para verificar si se permite acceder a una URL según robots.txt
    #rp = urllib.robotparser.RobotFileParser()
    #rp.set_url("https://letterboxd.com/robots.txt")
    #rp.read()
    #return rp.can_fetch(session.headers['User-Agent'], url)
    return True

def scrape(original_title, id_pelicula, processed_movies, all_pairs):
    # Si la película ya fue procesada, saltarla
    if id_pelicula in processed_movies:
        logging.info(f"'{original_title}' (ID: {id_pelicula}) ya fue procesada. Saltando.")
        return all_pairs

    # Formatear el nombre de la película para la URL
    nombre_pelicula = unidecode(original_title.lower()).replace(' ', '-').replace("'", '')
    nombre_pelicula = ''.join(c for c in nombre_pelicula if c.isalnum() or c == '-')

    # Set para almacenar los pares únicos (id_pelicula, id_lista)
    lista_ids = set()

    # Iterar sobre las páginas 1 a 10
    for pagina in range(1, 11):
        if pagina == 1:
            url = f"https://letterboxd.com/film/{nombre_pelicula}/lists/by/popular/"
        else:
            url = f"https://letterboxd.com/film/{nombre_pelicula}/lists/by/popular/page/{pagina}/"

        # Verificar si se permite acceder a la URL según robots.txt
        if not is_allowed(url):
            logging.warning(f"Acceso no permitido a {url} según robots.txt. Saltando.")
            continue

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = session.get(url, timeout=10)
                response.raise_for_status()
                break  # Salir del bucle si la solicitud es exitosa
            except requests.exceptions.RequestException as e:
                logging.warning(f"Intento {attempt + 1} de {max_retries} fallido para {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # Esperar antes del siguiente intento
                else:
                    logging.error(f"Fallo al acceder a {url} después de {max_retries} intentos.")
                    return all_pairs  # Continuar con la siguiente película

        # Pausa aleatoria entre solicitudes
        time.sleep(random.uniform(1, 3))

        html = response.content

        # Parsear el HTML con BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Encontrar todos los elementos <section> con las clases especificadas
        secciones = soup.select('section.list.-overlapped.-summary')

        for seccion in secciones:
            # Extraer el atributo 'data-film-list-id'
            list_id = seccion.get('data-film-list-id')
            if list_id:
                # Agregar el par al set para evitar duplicados
                lista_ids.add((id_pelicula, list_id))

        # Liberar memoria
        del html, soup, secciones

    # Actualizar el conjunto total de pares
    all_pairs.update(lista_ids)

    # Agregar el ID de la película al conjunto de películas procesadas
    processed_movies.add(id_pelicula)

    # Guardar los resultados actuales en el archivo CSV
    save_results(lista_ids)

    # Guardar el estado actual
    save_state(processed_movies, all_pairs)

    logging.info(f"Proceso completado para '{original_title}'. {len(lista_ids)} pares agregados.")

    return all_pairs

def save_results(pairs):
    # Verificar si el archivo ya existe
    file_exists = os.path.isfile('resultados.csv')

    # Abrir el archivo en modo adjuntar
    with open('resultados.csv', mode='a', newline='', encoding='utf-8') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        # Escribir el encabezado solo si el archivo no existe
        if not file_exists:
            escritor_csv.writerow(['ID_Pelicula', 'ID_Lista'])
        # Escribir los datos
        for id_pelicula, id_lista in pairs:
            escritor_csv.writerow([id_pelicula, id_lista])

def load_state():
    processed_movies = set()
    all_pairs = set()
    # Cargar estado desde el archivo estado.pkl si existe
    if os.path.isfile('estado.pkl'):
        with open('estado.pkl', 'rb') as f:
            estado = pickle.load(f)
            processed_movies = estado.get('processed_movies', set())
            all_pairs = estado.get('all_pairs', set())
    else:
        # Si no existe estado.pkl, cargar desde resultados.csv si existe
        if os.path.isfile('resultados.csv'):
            with open('resultados.csv', mode='r', newline='', encoding='utf-8') as archivo_csv:
                lector_csv = csv.reader(archivo_csv)
                next(lector_csv, None)  # Saltar el encabezado
                for row in lector_csv:
                    id_pelicula, id_lista = row
                    all_pairs.add((id_pelicula, id_lista))
                    processed_movies.add(id_pelicula)
    return processed_movies, all_pairs

def save_state(processed_movies, all_pairs):
    # Guardar el estado actual en estado.pkl
    with open('estado.pkl', 'wb') as f:
        pickle.dump({'processed_movies': processed_movies, 'all_pairs': all_pairs}, f)

def send_notification(message):
    # Función para enviar una notificación (puedes implementar correo electrónico u otra forma)
    logging.info(f"Notificación: {message}")
    # Implementar según tus necesidades

def main():
    try:
        # Cargar el archivo CSV 'movies.csv'
        movies_df = pd.read_csv('movies.csv')

        # Cargar las películas ya procesadas y los pares existentes
        processed_movies, all_pairs = load_state()

        countMovies=1
        # Iterar sobre cada fila y llamar a la función 'scrape'
        for index, row in movies_df.iterrows():
            id_pelicula = str(row['id'])
            original_title = str(row['original_title'])
            logging.info(f"{countMovies} | Procesando '{original_title}' (ID: {id_pelicula})")
            all_pairs = scrape(original_title, id_pelicula, processed_movies, all_pairs)
            countMovies+=1
        logging.info("Proceso completado. Los resultados se han guardado en 'resultados.csv'.")
        send_notification("El script de scraping ha finalizado correctamente.")
    except Exception as e:
        logging.exception("Se produjo un error durante la ejecución del script.")
        send_notification(f"El script ha encontrado un error: {e}")

if __name__ == "__main__":
    main()
