# Clasificador de Precios Anómalos en Supermercados 🛒📈

## Descripción

Este proyecto desarrolla un sistema de detección y clasificación de precios fuera de lo normal en productos de supermercados de Ecuador (Coral, (SuperMaxi, Megamaxi y Gran AKI) TipTi).  
Utilizamos Web Scraping para recolectar precios, aplicamos Z-Score para detectar anomalías y clasificamos los precios anómalos como **"Precio Alto"** o **"Promoción"**.

## Objetivo

- Detectar precios anómalos en productos básicos.
- Clasificar anomalías para identificar promociones o precios inusualmente altos.
- Analizar tendencias y posibles estrategias de precios.

## Tecnologías

- Python
- PySpark
- Pandas
- BeautifulSoup / Scrapy (para Web Scraping)
- Matplotlib / Seaborn (para visualización de resultados)

## Metodología

1. **Scraping**: Recolección de precios de productos en 4 supermercados.
2. **Procesamiento**: Cálculo del **Precio Promedio** y **Desviación Estándar** por producto.
3. **Cálculo de Z-Score**:

   ```python
   data = data.withColumn(
       "Z_Score", 
       (col("Precio") - col("Precio_Promedio")) / col("Desviacion_Estandar")
   )
   ```
4. Clasificación de anomalías:
  Si Z_Score > 3: Precio Alto
  Si Z_Score < -3: Promoción
