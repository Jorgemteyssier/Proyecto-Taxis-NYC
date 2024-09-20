import requests
from bs4 import BeautifulSoup
import os

# URL de la página
url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"

# Hacer la solicitud a la página
response = requests.get(url)

# Analizar el contenido de la página
soup = BeautifulSoup(response.text, "html.parser")

# Lista de los meses en orden
months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Años de interés (2009 en adelante)
years = list(range(2014, 2025))

# Directorio base donde se guardarán los archivos
base_dir = 'data'
os.makedirs(base_dir, exist_ok=True)

# Iterar sobre los años de interés
for year in years:
    # Crear carpeta por cada año
    year_folder = os.path.join(base_dir, str(year))
    os.makedirs(year_folder, exist_ok=True)

    # Buscar el contenedor del año correspondiente por id
    year_section = soup.find("div", id=f"faq{year}")

    if year_section:
        # Dentro del contenedor del año, buscar las listas <ul> con los meses
        for month in months:
            # Buscar la etiqueta <strong> que contenga el nombre del mes (con posibles espacios adicionales)
            month_section = year_section.find("strong", string=lambda s: s and month in s)

            if month_section:
                # Ir al siguiente elemento que es la lista <ul>
                ul_list = month_section.find_next("ul")
                if ul_list:
                    # Recorrer todos los <li> dentro del <ul>
                    for li in ul_list.find_all("li"):
                        # Buscar el enlace <a> dentro de cada <li>
                        link_tag = li.find("a", href=True)

                        # Verificar si el título del enlace empieza con "Yellow" o "Green"
                        if link_tag and link_tag['title'].startswith(("Yellow", 'Green')):
                            parquet_link = link_tag['href']

                            # Crear el nombre del archivo con el mes y si es Yellow o Green
                            taxi_type = "Yellow" if "Yellow" in link_tag['title'] else "Green"
                            file_name = f"{year}_{month}_{taxi_type}.parquet"
                            file_path = os.path.join(year_folder, file_name)

                            # Formar la URL completa del archivo
                            file_url = parquet_link if parquet_link.startswith('https') else f"https://{parquet_link}"

                            # Descargar el archivo
                            response = requests.get(file_url)
                            with open(file_path, 'wb') as file:
                                file.write(response.content)

                            print(f"Archivo {file_path} descargado.")
    else:
        print(f"No se encontró el contenedor para el año {year}")

print("Todos los archivos Parquet han sido descargados.")