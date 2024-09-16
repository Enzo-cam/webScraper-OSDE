# OSDE Web Scraper

## Tabla de Contenidos
- [OSDE Web Scraper](#osde-web-scraper)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Introducción](#introducción)
  - [Características](#características)
  - [Requisitos](#requisitos)
  - [Instalación](#instalación)
  - [Uso](#uso)
  - [Configuración](#configuración)
  - [Salida](#salida)
  - [Estructura del Código](#estructura-del-código)
  - [Manejo de Errores y Registro](#manejo-de-errores-y-registro)
  - [Consideraciones de Rendimiento](#consideraciones-de-rendimiento)
  - [Áreas de Mejora](#áreas-de-mejora)
  - [Comparación con la Solución API de NodeJS](#comparación-con-la-solución-api-de-nodejs)
    - [Ventajas del Web Scraper (Python):](#ventajas-del-web-scraper-python)
    - [Ventajas de la Solución basada en API (NodeJS):](#ventajas-de-la-solución-basada-en-api-nodejs)

## Introducción

Este proyecto es un web scraper diseñado para extraer información de profesionales de salud mental del directorio de proveedores de OSDE. Utiliza Selenium WebDriver para navegar por el sitio web de OSDE, seleccionar varias opciones y extraer datos sobre los proveedores de atención médica.

## Características

- Parámetros de scraping configurables a través de archivo YAML
- Automatización de navegador sin interfaz gráfica usando Selenium
- Manejo robusto de errores y lógica de reintento
- Limitación de tasa para respetar los recursos del sitio web
- Salida de datos estructurada en formato CSV
- Registro para depuración y monitoreo
- Soporte para múltiples configuraciones en una sola ejecución

## Requisitos

- Python 3.7+

## Instalación

1. Clona el repositorio:
   ```
   
   git clone https://github.com/Enzo-cam/webScraper-OSDE.git
   cd scraper-python
   ```

2. Crea un entorno virtual:
   ```
   python -m venv venv
   ```

3. Activa el entorno virtual:
   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS y Linux:
     ```
     source venv/bin/activate
     ```

4. Instala los paquetes requeridos:
   ```
   pip install -r requirements.txt
   ```

5. Asegúrate de tener ChromeDriver instalado y añadido a tu PATH del sistema.
   - Puedes descargar ChromeDriver desde: https://sites.google.com/a/chromium.org/chromedriver/downloads
   - Asegúrate de elegir la versión que coincida con tu versión del navegador Chrome.

## Uso

Para ejecutar el scraper:

1. Activa el entorno virtual si aún no está activado:
   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS y Linux:
     ```
     source venv/bin/activate
     ```

2. Ejecuta el scraper:
   ```
   python main.py
   ```

Esto ejecutará el scraper utilizando las configuraciones definidas en `scraper_config.yaml`.

## Configuración

El scraper se configura utilizando el archivo `scraper_config.yaml`. Puedes especificar múltiples configuraciones para extraer diferentes combinaciones de plan, provincia, localidad y especialidad.

Ejemplo de configuración:

```yaml
url: 'https://www.osde.com.ar/index1.html#!cartilla.html'

configurations:
  - plan: "510"
    provincia: "Ciudad de Buenos Aires"
    localidad: "Todas las Localidades"
    especialidad: "PSICOLOGÍA ADULTOS"
  - plan: "210"
    provincia: "GBA Zona Oeste"
    localidad: "Todas las Localidades"
    especialidad: "PSICOLOGÍA ADULTOS"
```

## Salida

El scraper genera un archivo CSV en el directorio `csv/` con las siguientes columnas:

- `config_index`: Índice de la configuración utilizada para esta entrada
- `indice`: Identificador único para cada proveedor (incluye sub-índice para duplicados)
- `plan`: Plan de salud
- `provincia`: Provincia
- `localidad`: Localidad
- `especialidad`: Especialidad
- `nombre`: Nombre del proveedor
- `direccion`: Dirección
- `localidad_prestador`: Localidad del proveedor
- `telefono`: Número de teléfono
- `consultorio_digital`: Si las consultas digitales están disponibles
- `scraping_date`: Fecha y hora del scraping

Las columnas `config_index` e `indice` se añadieron para:
1. Rastrear qué configuración produjo cada entrada, permitiendo un fácil filtrado y análisis.
2. Proporcionar un identificador único para cada proveedor, incluso cuando aparecen varias veces (por ejemplo, con diferentes ubicaciones de consultorio). Esto permite un procesamiento de datos preciso y deduplicación si es necesario.

## Estructura del Código

- `main.py`: Punto de entrada de la aplicación
- `scraper.py`: Contiene la clase `OSDEScraper`, que maneja la lógica del web scraping
- `data_processor.py`: Procesa el HTML extraído y extrae datos estructurados
- `csv_utils.py`: Maneja operaciones de archivo CSV
- `webdriver_utils.py`: Configura el Selenium WebDriver
- `config.py`: Carga la configuración desde el archivo YAML
- `text_utils.py`: Proporciona utilidades de normalización y limpieza de texto

## Manejo de Errores y Registro

El scraper utiliza la biblioteca `structlog` para el registro. Implementa un manejo de errores y registro integral a lo largo del proceso de scraping. Los registros se envían a la consola y pueden redirigirse fácilmente a un archivo si es necesario.

## Consideraciones de Rendimiento

- El scraper implementa retrasos aleatorios entre solicitudes para evitar sobrecargar el sitio web objetivo.
- Utiliza un navegador sin interfaz gráfica para reducir el uso de recursos.
- El scraper carga todos los resultados haciendo clic en el botón "Cargar más", asegurando una recopilación completa de datos.

## Áreas de Mejora

1. **Agregar pruebas**: Implementar pruebas unitarias y de integración para garantizar la fiabilidad del scraper.
2. **Procesamiento paralelo**: Implementar multi-threading o multiprocesamiento para extraer múltiples configuraciones simultáneamente.
3. **Rotación de proxy**: Implementar un mecanismo de rotación de proxy para distribuir solicitudes a través de múltiples direcciones IP.
4. **Integración de base de datos**: Considerar escribir directamente en una base de datos para una gestión y consulta de datos más fácil.
5. **Scraping incremental**: Implementar un mecanismo para rastrear datos ya extraídos y solo extraer información nueva o actualizada en ejecuciones subsiguientes.
6. **Rotación de user agent**: Rotar user agents para que las solicitudes del scraper parezcan provenir de diferentes navegadores.
7. **Manejo de captcha**: Implementar una solución para manejar CAPTCHAs si el sitio web los implementa en el futuro.

