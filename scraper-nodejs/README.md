# OSDE Directory Scraper

## Introducción

Este proyecto es un script para scrapear datos de profesionales de salud mental del directorio de proveedores de OSDE. Inicialmente concebido como un web scraper tradicional, el proyecto evolucionó hacia un enfoque más eficiente basado en API.
Durante la exploración de la página web de OSDE a través de las herramientas de desarrollo del navegador, específicamente en la pestaña de Network, se descubrió que era posible acceder directamente a la API que alimenta el directorio. Tras realizar pruebas con Postman, se confirmó que este método proporcionaba acceso más rápido y directo a la información deseada.
Basándose en este hallazgo, se tomó la decisión de desarrollar una solución que interactuara directamente con la API de OSDE en lugar de realizar web scraping tradicional. Esta aproximación resulta en un proceso más eficiente y menos propenso a errores, ya que evita la necesidad de navegar y extraer datos de la interfaz web.
El script utiliza axios para realizar solicitudes HTTP a la API de OSDE y procesa los datos recibidos para generar un archivo CSV con información detallada de los proveedores de salud mental.

## Características

- Extracción de datos de múltiples configuraciones (plan, provincia, especialidad)
- Manejo de paginación para obtener todos los resultados disponibles
- Generación de índices únicos para cada proveedor y sus consultorios
- Salida de datos estructurada en formato CSV
- Manejo robusto de errores y limitación de tasa de solicitudes

## Requisitos

- Node.js 12.0+
- npm (normalmente viene con Node.js)

## Instalación

1. Clona el repositorio:

   ```
   git clone https://github.com/Enzo-cam/web-scraping-osde.git
   cd scraper-nodejs
   ```

2. Instala las dependencias:
   ```
   npm install
   ```

## Uso

Para ejecutar el scraper:

```
node scraper.js
```

Esto ejecutará el scraper utilizando las configuraciones definidas en el archivo `scraper.js`.

## Configuración

Las configuraciones se definen directamente en el archivo `scraper.js`. Puedes modificar el array `configurations` para añadir o quitar configuraciones según sea necesario.

Ejemplo de una configuración:

```javascript
{
    baseUrl: "https://www.osde.com.ar/Cartilla/consultaPorEspecialidadRemote.ashx?metodo=ObtenerParaCartillaMedica&rubros=2&rubroId=2&provinciaId=1&provinciaTipo=METRO&provinciaNombre=Ciudad%20de%20Buenos%20Aires&localidadId=0&localidadNombre=Todas%20las%20localidades&planId=51&planNombre=510&especialidadId=810&especialidadNombre=Psicolog%C3%ADa%20adultos&filialId=&hiddenLat=&hiddenLng=&textDireccion=&textNombre=&txtFecha=&ordenador=&hidDetalleNombre=&hidDetalleDireccion=&hidDetalleTelefono=&hidDetalleObservacion=&hidDetalleEspecialidad=&hidDetalleLatitud=&hidDetalleLongitud=&prestadoresEnLista=0&modalidadAtencion=2",
    plan: "510",
    provincia: "Ciudad de Buenos Aires",
    especialidad: "PSICOLOGÍA ADULTOS"
}
```

## Salida

El scraper genera un archivo CSV llamado `osde_professionals.csv` con las siguientes columnas:

- `ConfigIndex`: Índice de la configuración utilizada
- `IndiceItem`: Identificador único para cada proveedor y consultorio
- `Nombre`: Nombre del proveedor
- `Especialidad`: Especialidad del proveedor
- `Dirección`: Dirección del consultorio
- `Teléfono`: Número de teléfono
- `Email`: Correo electrónico del proveedor
- `Localidad`: Localidad del consultorio
- `Provincia`: Provincia del consultorio
- `Plan`: Plan de salud
- `Número de Prestador`: Número único del prestador

## Estructura del Código

El script está contenido en un solo archivo `scraper.js`, que incluye:

- Configuraciones para diferentes búsquedas
- Función para obtener datos de una página específica
- Función para obtener todos los datos de una configuración
- Función principal que orquesta todo el proceso de scraping
