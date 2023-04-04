
# Este código completo realiza las siguientes acciones:

# 1. Obtiene los enlaces `/list/ls...` de la página original.
# 2. Inserta estos enlaces en la tabla `imdb_links` en la base de datos SQLite `imdb_links.db`.
# 3. Por cada enlace `/list/ls...`, realiza una solicitud a la página correspondiente de la lista de películas en IMDb.
# 4. Filtra los enlaces de las películas `/title/tt...` de cada página de la lista.
# 5. Inserta estos enlaces de películas en la tabla `imdb_movie_links` en la base de datos SQLite `imdb_links.db`.

# Cuando ejecutes este script, se crearán dos tablas en la base de datos `imdb_links.db`: una para los enlaces de las listas y otra para los enlaces de las películas. Además, se mostrarán en la terminal los enlaces y los ID almacenados en la base de datos.




import requests
from bs4 import BeautifulSoup
import sqlite3
import re

# Definir la URL de la página web que deseas hacer scraping
url = 'https://www.imdb.com/lists/tt0111161/?ref_=tt_rls_sm'

# Realizar una solicitud HTTP GET a la URL
response = requests.get(url)

# Extraer el ID "tt01..." de la URL
imdb_id = re.search(r'tt\d+', url).group()

# Crear la base de datos SQLite y las tablas para almacenar los datos
conn = sqlite3.connect('imdb_links.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS imdb_links
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, imdb_id TEXT, link TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS imdb_movie_links
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, imdb_id TEXT, link TEXT)''')

# Comprobar si la solicitud fue exitosa (código de estado HTTP 200)
if response.status_code == 200:
    # Crear una instancia de BeautifulSoup y especificar el analizador
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar todos los elementos 'a' con el atributo 'href' que comienza con '/list/ls...'
    a_elements = soup.find_all('a', href=True)

    # Filtrar los elementos 'a' cuyo atributo 'href' comienza con '/list/ls...'
    filtered_a_elements = [a for a in a_elements if a['href'].startswith('/list/ls')]

    # Insertar los enlaces 'href' filtrados en la base de datos junto con el ID "tt01..."
    for a in filtered_a_elements:
        link = a['href']
        cursor.execute('INSERT INTO imdb_links (imdb_id, link) VALUES (?, ?)', (imdb_id, link))
        print(f"Se ha insertado el enlace '{link}' con el ID '{imdb_id}' en la tabla imdb_links.")
        
        # Concatenar el enlace al final de "https://www.imdb.com/" y realizar una nueva solicitud
        full_url = f'https://www.imdb.com{link}'
        list_response = requests.get(full_url)
        
        if list_response.status_code == 200:
            list_soup = BeautifulSoup(list_response.content, 'html.parser')
            movie_a_elements = list_soup.find_all('a', href=True)
            
            # Filtrar los elementos 'a' cuyo atributo 'href' comienza con '/title/tt'
            filtered_movie_a_elements = [a for a in movie_a_elements if a['href'].startswith('/title/tt')]
            
            # Insertar los enlaces de películas filtrados en la base de datos junto con el ID "tt01..."
            for movie_a in filtered_movie_a_elements:
                movie_link = movie_a['href']
                cursor.execute('INSERT INTO imdb_movie_links (imdb_id, link) VALUES (?, ?)', (imdb_id, movie_link))
                print(f"Se ha insertado el enlace de película '{movie_link}' con el ID '{imdb_id}' en la tabla imdb_movie_links.")
            conn.commit()
        else:
                print(f"Error al obtener la página de la lista {full_url}: {list_response.status_code}")
else:
    print("Error al obtener la página:", response.status_code)

# Cerrar la conexión a la base de datos
conn.close()
