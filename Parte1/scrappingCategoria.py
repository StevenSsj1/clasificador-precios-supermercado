from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd


# Configuración del WebDriver
chromedriver_path = 'chromedriver.exe'
options = Options()
options.headless = False  # Cambiar a True si no quieres ver el navegador en acción
driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

# Función para manejar categorías
def categorias(click=False, n=0):
    elementos_categorias = driver.find_elements(By.CSS_SELECTOR, ".fs-14.text-lines-1.padding-1.nav-categories__categories.cursor-pointer")
    listaCat = [(cat.text.strip(), cat) for cat in elementos_categorias]
    if click:
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elementos_categorias[n])
            time.sleep(1)
            action = ActionChains(driver)
            action.move_to_element(elementos_categorias[n]).click().perform()
        except Exception as e:
            print(f"Error al hacer clic en la categoría {n}: {e}")
    return elementos_categorias, listaCat, len(elementos_categorias)

# Función para realizar desplazamiento gradual
def scrolldown():
    scroll_pause_time = 2
    scroll_increment = 700
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    while True:
        current_position += scroll_increment
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            print("¡Has llegado al final de la página!")
            break
        last_height = new_height

# Función para extraer productos
def getProductos(categoria, nombreTienda):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.find_all(itemtype="http://schema.org/Product")
    product_list = []
    for product in products:
        product_info = {}
        name_tag = product.find(class_="fs-16 fw-200 text-lines-2 margin-y-1")
        if name_tag:
            product_info['nombre'] = name_tag.get_text(strip=True)
        price_tag = product.find(class_="fs-18 fw-600 product-card__regular-price")
        if price_tag:
            product_info['precio'] = price_tag.get_text(strip=True)
            product_info['descuento'] = "False"
        else:
            price_tag = product.find(class_="fs-18 fw-500 on-primary radius-1 bg-error align-self-start discounted-price")
            if price_tag:
                product_info['precio'] = price_tag.get_text(strip=True)
                product_info['descuento'] = "True"
        if product_info:
            product_info['categoria'] = categoria
            product_info['tienda'] = nombreTienda
            product_list.append(product_info)
    return pd.DataFrame(product_list)

# Función principal
def obtTipti(url, nombreTienda):
    driver.get(url)
    time.sleep(3)
    _, _, largo = categorias(False)
    dfTienda = pd.DataFrame(columns=['nombre', 'precio', 'descuento', 'categoria', 'tienda'])
    for i in range(largo):
        _, listaCat, _ = categorias(True, i)
        scrolldown()
        df = getProductos(listaCat[i][0], nombreTienda)
        dfTienda = pd.concat([dfTienda, df], ignore_index=True)
        print(df.head(5))
    return dfTienda

# Lista de tiendas
lista = [
    ('https://www.tipti.market/tienda/megamaxi', 'MEGAMAXI'),
    ('https://www.tipti.market/tienda/supermaxi', 'SUPERMAXI'),
    ('https://www.tipti.market/tienda/gran-aki', 'GRAN AKI')
]

# Extraer datos
dfInicial = pd.DataFrame(columns=['nombre', 'precio', 'descuento', 'categoria', 'tienda'])
for l in lista:
    df = obtTipti(l[0], l[1])
    dfInicial = pd.concat([dfInicial, df], ignore_index=True)

# Guardar en CSV
dfInicial.to_csv('productos_extraidos.csv', index=False, encoding='utf-8')

# Cerrar navegador
driver.quit()
