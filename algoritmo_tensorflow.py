# Modelo de aprendizaje profundo  utilizando TensorFlow y Keras. 
# En este caso, dado que la relación entre 
# "imdb_id" y "link" parece ser de naturaleza no secuencial, se usa  una 
# red neuronal totalmente conectada (Feedforward).


import sqlite3
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Función para cargar datos de la base de datos
def load_data(database="imdb_links.db", table="imdb_movie_links"):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = f"SELECT imdb_id, link FROM {table}"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# Función para preprocesar los datos
def preprocess_data(data):
    imdb_ids = []
    links = []

    for row in data:
        imdb_id = row[0]
        link = row[1]
        imdb_id_numeric = int(imdb_id[2:])  # Extraer la parte numérica de la cadena 'imdb_id'
        imdb_ids.append(imdb_id_numeric)
        links.append(link)

    return np.array(imdb_ids), np.array(links)


# Cargar y preprocesar los datos
data = load_data("imdb_links.db", "imdb_movie_links")
imdb_ids, links = preprocess_data(data)

# Separar los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(imdb_ids, links, test_size=0.2, random_state=42)

from tensorflow.keras.utils import to_categorical


# En lugar de escalar, aplicar codificación One-Hot

num_classes_imdb_id = len(np.unique(imdb_ids))
num_classes_links = len(np.unique(links))

X_train_one_hot = to_categorical(X_train, num_classes=num_classes_imdb_id)
X_test_one_hot = to_categorical(X_test, num_classes=num_classes_imdb_id)
y_train_one_hot = to_categorical(y_train, num_classes=num_classes_links)
y_test_one_hot = to_categorical(y_test, num_classes=num_classes_links)


# Crear el modelo de red neuronal
model = Sequential()
model.add(Dense(64, activation="relu", input_shape=(1,)))
model.add(Dense(64, activation="relu"))
model.add(Dense(1, activation="linear"))

# Compilar el modelo
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# Entrenar el modelo
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

# Evaluar el modelo
loss, mae = model.evaluate(X_test, y_test)
print(f"Mean Absolute Error: {mae}")

# Realizar predicciones
predictions = model.predict(X_test)

# Comparar las predicciones con los valores reales
for i in range(10):
    print(f"Predicción: {predictions[i]}, Valor real: {y_test[i]}")
