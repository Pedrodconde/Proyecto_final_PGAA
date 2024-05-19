import numpy as np
from flask import Flask, request, render_template, jsonify
import matplotlib
matplotlib.use('Agg')  # Usar modo no interactivo
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Crear la aplicación Flask
app = Flask(__name__)

# Definir los datos de los aviones
aviones = {
    'A350': {'MTOW': 187000, 'OEW': 125000, 'MPL': 24000, 'MFW': 47000, 'R_MAX': 16100},
    'A330': {'MTOW': 175000, 'OEW': 120500, 'MPL': 20400, 'MFW': 45000, 'R_MAX': 13400},
    'A319': {'MTOW': 64300, 'OEW': 41500, 'MPL': 13400, 'MFW': 17000, 'R_MAX': 4200},
    'A321': {'MTOW': 77000, 'OEW': 50500, 'MPL': 14800, 'MFW': 20000, 'R_MAX': 3700},
    'A320': {'MTOW': 64000, 'OEW': 41600, 'MPL': 12000, 'MFW': 17300, 'R_MAX': 2400},   
}

# Función para calcular el avión idóneo según la distancia a recorrer
def avion_idoneo(distancia):
    avion_idoneo = None
    menor_diferencia = float('inf')
    for avion, datos in aviones.items():
        diferencia = abs(datos['R_MAX'] - distancia)
        if diferencia < menor_diferencia and distancia <= datos['R_MAX']:
            avion_idoneo = avion
            menor_diferencia = diferencia
    return avion_idoneo

# Función para calcular el parámetro K en función del alcance máximo del avión idóneo
def calcular_K(avion):
    R_MAX = aviones[avion]['R_MAX']
    MTOW = aviones[avion]['MTOW']
    MFW = aviones[avion]['MFW']
    OEW = aviones[avion]['OEW']
    return R_MAX / np.log(MTOW / (MTOW - MFW))

# Definir los puntos característicos del Diagrama PL-R
class PuntoCaracteristico(object):
    def __init__(self, nombre, PL, TOW, FW, OEW, K):
        self.nombre = nombre
        self.PL = PL
        self.TOW = TOW
        self.FW = FW
        self.OEW = OEW
        self.K = K
        self.x = self.K * np.log((self.TOW) / (self.TOW - self.FW))
        self.y = self.PL 

# Función para calcular los puntos característicos con los valores dados
def calcular_puntos(MTOW, OEW, MPL, MFW, K):
    valores_puntos = [
        {'nombre': ' O', 'PL': MPL, 'TOW': OEW + MPL, 'FW': 0},
        {'nombre': ' A', 'PL': MPL, 'TOW': MTOW, 'FW': MTOW - OEW - MPL},
        {'nombre': ' B', 'PL': MTOW - OEW - MFW, 'TOW': MTOW, 'FW': MFW},
        {'nombre': ' C', 'PL': 0, 'TOW': MFW + OEW, 'FW': MFW}
    ]
    colores = ['b', 'g', 'r', 'c']  
    puntos = []
    for i, valores in enumerate(valores_puntos):
        puntos.append(PuntoCaracteristico(valores['nombre'], valores['PL'], valores['TOW'], valores['FW'], OEW, K))
        puntos[-1].color = colores[i] 
    return puntos

# Función para calcular la función a trozos
def funcion_a_trozos(x, puntos):
    if x <= puntos[0].x:  
        return puntos[0].y
    elif x >= puntos[-1].x: 
        return puntos[-1].y
    else:
        for i in range(len(puntos) - 1):
            if puntos[i].x <= x <= puntos[i + 1].x:  
                m = (puntos[i + 1].y - puntos[i].y) / (puntos[i + 1].x - puntos[i].x)
                b = puntos[i].y - m * puntos[i].x
                return m * x + b

# Función para generar el gráfico
def generar_grafico(avion, distancia):
    MTOW = aviones[avion]['MTOW']
    OEW = aviones[avion]['OEW']
    MPL = aviones[avion]['MPL']
    MFW = aviones[avion]['MFW']
    R_MAX = aviones[avion]['R_MAX']
    K = calcular_K(avion)

    puntos = calcular_puntos(MTOW, OEW, MPL, MFW, K)
    x_values = np.linspace(puntos[0].x, puntos[-1].x, 100)
    y_values = [funcion_a_trozos(x, puntos) for x in x_values]

    plt.plot(x_values, y_values, 'r-')
    for punto in puntos:
        plt.plot(punto.x, punto.y, marker='o', color=punto.color, label=punto.nombre)
        plt.text(punto.x, punto.y, punto.nombre, fontsize=8, ha='right', va='bottom')

    # Añadir el punto correspondiente a la distancia R
    x_distancia = K * np.log(MTOW / (MTOW - MFW * (distancia / R_MAX)))
    y_distancia = funcion_a_trozos(x_distancia, puntos)
    plt.plot(x_distancia, y_distancia, 'mo', label=f'R = {distancia} km')
    plt.text(x_distancia, y_distancia, f' R = {distancia} km', fontsize=8, ha='left', va='bottom', color='m')

    # Determinar si el punto está entre A y B
    if puntos[1].x <= x_distancia <= puntos[2].x:
        mensaje = "El avión opera en la zona de interés comercial."
    else:
        mensaje = "El avión no opera dentro de la zona de interés comercial, se debería eliminar la ruta correspondiente."
        
    plt.xlabel('Alcance (km)')
    plt.ylabel('Carga de Pago (kg)')
    plt.title('DIAGRAMA PL-R')
    plt.legend()
    plt.grid(True)

    # Calcular K y mostrar en un recuadro
    K_calculada = R_MAX / np.log(MTOW / (MTOW - MFW))
    plt.text(0.1, 0.9, f'K = {K_calculada:.2f}', transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()

    plt.close()  # Cerrar la figura para liberar recursos

    return img_base64, mensaje

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        distancia = float(request.form['distancia'])
        avion = avion_idoneo(distancia)
        if avion:
            img_base64, mensaje = generar_grafico(avion, distancia)
            K = calcular_K(avion)
            return render_template('index.html', avion=avion, img_base64=img_base64, K=K, distancia=distancia, mensaje=mensaje)
        else:
            return render_template('index.html', error=True)
    else:
        return render_template('index.html', aviones=aviones.keys())

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

