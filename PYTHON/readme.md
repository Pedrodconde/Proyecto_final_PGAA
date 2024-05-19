# Diagrama PL-R

Este proyecto es una aplicación web desarrollada con Flask que permite calcular y visualizar el diagrama PL-R para determinar el avión idóneo para una ruta específica según la distancia a recorrer.

## Requisitos

- Python 3.x
- Flask
- NumPy
- Matplotlib

## Instalación

1. Clona este repositorio o descarga los archivos.

2. Instala las dependencias necesarias:
    ```bash
    pip install Flask numpy matplotlib
    ```

## Ejecución

1. Ejecuta la aplicación Flask:
    ```bash
    python app.py
    ```

2. Abre tu navegador web y navega a `http://127.0.0.1:5000/`.

## Uso

1. Ingresa la distancia (en kilómetros) que deseas recorrer en el formulario en la página principal.

2. Haz clic en "Calcular".

3. La aplicación mostrará:
    - El avión idóneo para la distancia ingresada.
    - El valor de K calculado para ese avión.
    - Un diagrama PL-R que visualiza la relación entre la carga de pago y el alcance del avión.
    - Un mensaje que indica si el avión opera dentro de la zona de interés comercial o no.

## Archivos

### `app.py`

Este archivo contiene la lógica principal de la aplicación:

- Definición de los datos de los aviones.
- Cálculo del avión idóneo basado en la distancia ingresada.
- Generación del gráfico PL-R usando Matplotlib.
- Rutas de Flask para manejar las solicitudes GET y POST.

### `templates/index.html`

Este archivo es la plantilla HTML que se usa para renderizar la página web:

- Un formulario para ingresar la distancia.
- Un bloque condicional para mostrar el resultado si se ha ingresado una distancia válida.
- Un bloque condicional para mostrar un mensaje de error si la distancia ingresada excede el alcance de todos los aviones disponibles.

## Funciones Principales

### `avion_idoneo(distancia)`

Calcula y devuelve el avión idóneo basado en la distancia proporcionada.

### `calcular_K(avion)`

Calcula el valor de K para el avión idóneo.

### `calcular_puntos(MTOW, OEW, MPL, MFW, K)`

Calcula los puntos característicos del diagrama PL-R.

### `funcion_a_trozos(x, puntos)`

Calcula la función a trozos para el diagrama PL-R.

### `generar_grafico(avion, distancia)`

Genera el gráfico PL-R y lo codifica en base64 para ser renderizado en la página web.

## Créditos

Este proyecto fue desarrollado utilizando Flask, NumPy y Matplotlib.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
