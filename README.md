# AirPiano 🎹🚀

AirPiano es una aplicación de visión computacional escrita en Python que te permite tocar un piano virtual y otros instrumentos musicales simplemente moviendo tus manos frente a la cámara. Utiliza **MediaPipe** para la detección de manos en tiempo real y **Pygame MIDI** para la generación de sonido.

## Características

- **Detección de Manos:** Seguimiento preciso de los dedos mediante MediaPipe.
- **Multi-instrumento:** Cambia entre Piano, Órgano, Sintetizador, Guitarra y Batería.
- **Interfaz Interactiva:** Teclas y controles dibujados directamente sobre el flujo de video.
- **Sonido MIDI:** Utiliza el sintetizador de tu sistema para una baja latencia y alta calidad.

## Requisitos

- Python 3.10+ (Probado en Arch Linux con Python 3.14)
- Cámara web
- Sintetizador MIDI (como FluidSynth)

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/AirPiano.git
   cd AirPiano
   ```

2. **Crea un entorno virtual e instala las dependencias:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Instala el sintetizador (Arch Linux):**
   ```bash
   sudo pacman -S fluidsynth soundfont-fluid alsa-utils
   ```

## Cómo ejecutar

Para facilitar la configuración del audio y la conexión MIDI, utiliza el script incluido:

```bash
chmod +x play.sh
./play.sh
```

## Controles

- **Tocar Notas:** Mueve la punta de tus dedos sobre las teclas blancas en la parte inferior de la pantalla.
- **Cambiar Instrumento:** Toca los botones grises en la parte superior.
- **Salir:** Presiona la tecla `q` en la ventana del piano.

## Estructura del Proyecto

- `main.py`: Lógica principal e integración.
- `hand_tracker.py`: Motor de detección de manos (usando MediaPipe Tasks API).
- `instrument.py`: Controlador de salida MIDI.
- `ui.py`: Elementos de la interfaz de usuario y detección de colisiones.
- `play.sh`: Script de arranque automático (configura FluidSynth y conexiones).

---
Creado con 💻 por Gemini CLI
