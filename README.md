# 🃏 Balatro Vision: IA de Detección de Cartas en Tiempo Real

Este proyecto implementa un sistema de visión artificial para el juego **Balatro**. Utiliza un modelo **YOLO** v8 entrenado para identificar cartas y palos en tiempo real a través de un flujo de video enviado desde **OBS Studio** hacia contenedores **Docker**.
link con el dataset subido en drive:
https://drive.google.com/drive/folders/1kMSBHG3xBHJos9hLqAqVrsynY_G8ikNS?usp=sharing

## 🏗️ Arquitectura del Proyecto

El sistema funciona mediante una tubería (pipeline) de video:
1.  **Captura:** OBS Studio captura la ventana de Balatro.
2.  **Streaming:** OBS envía el video via RTMP al servidor de medios en el puerto 1935.
3.  **Servidor:** `rtmp-server` (MediaMTX) recibe y distribuye la señal.
4.  **Inferencia:** El contenedor `balatro-ai` procesa el video con YOLO y dibuja los cuadros de detección.
5.  **Visualización:** Los resultados se sirven en una interfaz web local en el puerto 5000.

## 📋 Requisitos Previos

* **Docker Desktop** (con soporte para WSL 2 en Windows).
* **OBS Studio** para la transmisión de video.
* Archivo del modelo entrenado **`best.pt`** en la raíz del proyecto.
* Dataset en formato YOLO (archivos `.txt`) para re-entrenamiento.

## 🚀 Instalación y Ejecución

1.  Abre una terminal (PowerShell en Windows) en la carpeta del proyecto.
2.  Construye e inicia los contenedores:

```powershell
docker compose up --build
```
El sistema estará listo cuando veas el mensaje:```Serving Flask app 'detect' Running on http://0.0.0.0:5000.```
🎥 Configuración de OBS Studio (Obligatorio)
Para que la IA funcione correctamente y sin retraso, aplica estos ajustes en OBS:

1. Emisión
Servidor: rtmp://127.0.0.1:1935/live

Clave de retransmisión: balatro

2. Salida (Output)
Codificador: H.264 (Importante: NO usar H.265/HEVC).

Bitrate: 1500 - 2500 Kbps.

Sintonía: Zerolatency.

3. Video
Resolución de salida: 1280x720 o 640x640 (Resoluciones bajas mejoran el rendimiento en CPU).

FPS: 10 o 15 (Suficiente para Balatro y evita saturar el procesador).

🖥️ Visualización
Una vez iniciada la transmisión en OBS, accede a la interfaz de detección en vivo:

👉 http://localhost:5000

🛠️ Solución de Problemas
"Reader is too slow / Discarding frames": Tu CPU no procesa a tiempo. Reduce los FPS en OBS a 10 y la resolución a 480p.

"Skipping track 1 (H265)": OpenCV no soporta H265 vía RTMP. Cambia el codificador de OBS a H.264.

"ModuleNotFoundError: flask": Asegúrate de que tu Dockerfile incluya la línea RUN pip install flask.

Docker no reconocido: Asegúrate de que Docker Desktop esté abierto y configurado en el PATH del sistema.

🧠 Entrenamiento (Google Colab)
El archivo Untitled0.ipynb incluye el código para entrenar modelos YOLOv8 o YOLO11. Asegúrate de exportar tu dataset desde Roboflow en formato YOLOv8 para obtener las etiquetas en archivos .txt compatibles.
