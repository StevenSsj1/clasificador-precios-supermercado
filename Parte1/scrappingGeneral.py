from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd


# Ruta al WebDriver de Chrome (cambia la ruta si es necesario)
# Asegúrate de que el archivo chromedriver esté en el mismo directorio o en tu PATH
chromedriver_path = 'chromedriver.exe'  # Cambia esto por tu ruta

# Configura las opciones para el navegador (por ejemplo, no abrir la ventana del navegador)
options = Options()
options.headless = True#False  # Cambia a True si no quieres ver el navegador en acción

# Inicializa el WebDriver
driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

def obtTipti(url:str,nombre:str):
    driver.get(url)
    time.sleep(15)
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Realizar el scroll hasta que se llegue al final
    i=0
    while True:
        i+=1
        # Realiza el scroll hacia abajo
        driver.execute_script("window.scrollBy(0, 1200);")
        print(f"Scroll {i+1} ejecutado.")

        # Espera un poco para que la página cargue el contenido nuevo
        time.sleep(3)

        # Verifica si la altura de la página ha cambiado
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Si la altura de la página no cambia, hemos llegado al final
        if new_height == last_height:
            print("¡Has llegado al final de la página!")
            break

        # Actualiza la altura de la página
        last_height = new_height

    # Obtén el HTML completo de la página
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.find_all(itemtype="http://schema.org/Product")
    product_list = []
    for product in products:
        product_info = {}

        name_tag = product.find(class_="fs-16 fw-200 text-lines-2 margin-y-1")
        if name_tag:
            product_info['nombre'] = name_tag.get_text(strip=True)

        # Buscar el precio del producto
        price_tag = product.find(class_="fs-18 fw-600 product-card__regular-price")
        if price_tag:
            product_info['precio'] = price_tag.get_text(strip=True)
            product_info['descuento'] = "False"

        else:
            price_tag = product.find(class_="fs-18 fw-500 on-primary radius-1 bg-error align-self-start discounted-price")
            product_info['precio'] = price_tag.get_text(strip=True)
            product_info['descuento'] = "True"
        if product_info:
            product_info['tienda'] = nombre
            product_list.append(product_info)
    return pd.DataFrame(product_list)

    # Verificar que los datos se hayan almacenado correctamente
    print(df.head(10))


    # Exportar el DataFrame a un archivo CSV
lista = [('https://www.tipti.market/tienda/megamaxi','MEGAMAXI'),
         ('https://www.tipti.market/tienda/supermaxi','SUPERMAXI'),
         ('https://www.tipti.market/tienda/gran-aki','GRAN AKI')]
dfInicial = pd.DataFrame(columns=['nombre', 'precio','descuento','tienda'])
for l in lista:
    df= obtTipti(l[0],l[1])
    dfInicial=pd.concat([dfInicial,df],ignore_index=True)

dfInicial.to_csv('../data/productos_extraidos.csv', index=False, encoding='utf-8')
# Cierra el navegador
driver.quit()
