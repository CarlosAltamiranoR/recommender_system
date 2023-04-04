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

# Crear la base de datos SQLite y la tabla para almacenar los datos
conn = sqlite3.connect('imdb_links.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS imdb_links
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
        print(f"Se ha insertado el enlace '{link}' con el ID '{imdb_id}' en la base de datos.")
    conn.commit()
else:
    print("Error al obtener la página:", response.status_code)

# Cerrar la conexión a la base de datos
conn.close()
