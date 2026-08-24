# EcoSort

Sistema automatizado de clasificación de residuos mediante visión artificial, inteligencia artificial y control electrónico.

## Problema

La separación de residuos requiere identificar y clasificar cada objeto antes de su disposición. Cuando este proceso se realiza manualmente, puede ser lento y presentar errores.

EcoSort busca automatizar esta tarea mediante un sistema que identifica el residuo con una cámara y posteriormente lo dirige hacia el contenedor correspondiente.

## Funcionamiento

1. El residuo ingresa al sistema.
2. La cámara captura el objeto.
3. El modelo de TensorFlow identifica el tipo de residuo.
4. El resultado se comunica a la ESP32.
5. La ESP32 controla los servomotores.
6. Las compuertas dirigen el residuo al contenedor correspondiente.
7. Después de un breve intervalo, el sistema vuelve a detectar.

```text
Residuo
   ↓
Cámara
   ↓
OpenCV
   ↓
Modelo TensorFlow
   ↓
Clasificación
   ↓
Comunicación Serial
   ↓
ESP32
   ↓
Servomotores
   ↓
Contenedor
```

## Modelo de inteligencia artificial

El modelo de TensorFlow se encuentra en `modeloDEFF` y debe conservar esta estructura:

```text
EcoSort/
├── modeloDEFF/
│   └── model.savedmodel/
├── main.py
├── main_esp32.py
├── requirements.txt
└── README.md
```

El modelo se carga mediante:

```python
MODEL_PATH = r"modeloDEFF\model.savedmodel"

class_names = ["Plastico", "Metal", "Papel", "NULL"]
```

Las clases deben conservar el mismo orden utilizado durante el entrenamiento:

```text
0 → Plastico
1 → Metal
2 → Papel
3 → NULL
```

## Librerías

### Python

Las librerías utilizadas por el programa principal son:

| Librería   | Función                                                 |
| ---------- | ------------------------------------------------------- |
| TensorFlow | Carga y ejecución del modelo de inteligencia artificial |
| NumPy      | Procesamiento de datos y matrices                       |
| OpenCV     | Captura y procesamiento de imágenes                     |
| PySerial   | Comunicación entre el computador y la ESP32             |
| time       | Control de intervalos y tiempos de espera               |

`time` forma parte de Python y no necesita instalarse.

Las dependencias pueden instalarse mediante:

```bash
pip install tensorflow numpy opencv-python pyserial
```

O utilizando:

```bash
pip install -r requirements.txt
```

### ESP32

La ESP32 utiliza MicroPython. La principal librería utilizada es:

| Librería | Función                                              |
| -------- | ---------------------------------------------------- |
| machine  | Control de pines, PWM y comunicación con el hardware |

`machine` forma parte de MicroPython y no se instala mediante `pip`.

## Ejecución

Después de instalar las dependencias y conectar la cámara y la ESP32:

```bash
python main.py
```

El archivo `main_esp32.py` debe cargarse en la ESP32 mediante un entorno compatible con MicroPython, como Thonny.

## Hardware

* ESP32
* Cámara
* Servomotores SG90
* Mecanismo de clasificación
* Sistema de alimentación

## Tecnologías

* Python
* TensorFlow
* OpenCV
* NumPy
* PySerial
* MicroPython
* ESP32
* Visión artificial
* Aprendizaje automático

## Objetivo

EcoSort integra inteligencia artificial, visión artificial y electrónica para convertir la identificación automática de residuos en una acción física de clasificación.
