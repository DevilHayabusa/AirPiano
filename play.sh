#!/bin/bash

# 1. Matar procesos previos si existen
pkill fluidsynth

# 2. Iniciar FluidSynth en segundo plano
echo "Iniciando sintetizador..."
# Intentamos primero con pipewire, luego pulseaudio, luego alsa
if fluidsynth -s -i -a pipewire -m alsa_seq /usr/share/soundfonts/FluidR3_GM.sf2 > /dev/null 2>&1 & then
    echo "Usando driver: pipewire"
elif fluidsynth -s -i -a pulseaudio -m alsa_seq /usr/share/soundfonts/FluidR3_GM.sf2 > /dev/null 2>&1 & then
    echo "Usando driver: pulseaudio"
else
    fluidsynth -s -i -a alsa -m alsa_seq /usr/share/soundfonts/FluidR3_GM.sf2 > /dev/null 2>&1 &
    echo "Usando driver: alsa"
fi
sleep 2

# 3. Conectar automáticamente la salida MIDI al sintetizador
# Buscamos el ID de FluidSynth
FS_ID=$(aconnect -o | grep "FLUID Synth" | head -n 1 | awk '{print $2}' | cut -d: -f1)
# Buscamos el ID de nuestro puerto MIDI Through
TH_ID=$(aconnect -o | grep "Midi Through" | head -n 1 | awk '{print $2}' | cut -d: -f1)

if [ ! -z "$FS_ID" ] && [ ! -z "$TH_ID" ]; then
    echo "Conectando Puerto $TH_ID a FluidSynth ($FS_ID)..."
    aconnect $TH_ID:0 $FS_ID:0
else
    echo "Aviso: No se pudo auto-conectar. Puede que necesites usar 'qjackctl' para conectar los puertos."
fi

# 4. Lanzar la aplicación
echo "Lanzando AirPiano..."
./venv/bin/python main.py

# 5. Al cerrar, limpiar
pkill fluidsynth
