import pygame.midi
import time

class InstrumentController:
    def __init__(self):
        pygame.midi.init()
        port = pygame.midi.get_default_output_id()
        if port == -1:
            print("Error: No se encontró un dispositivo MIDI de salida predeterminado.")
            self.midi_out = None
        else:
            self.midi_out = pygame.midi.Output(port, 0)
            print(f"Dispositivo MIDI configurado en el puerto: {port}")
        
        # Diccionario de instrumentos (General MIDI)
        self.instruments = {
            "Piano": 0,
            "Organ": 16,
            "Synth": 81,
            "Guitar": 30,
            "Drums": 118  # Synth Drum (Nota: Los sonidos de batería reales suelen estar en el canal 10)
        }
        self.current_instrument = "Piano"
        self.set_instrument("Piano")

    def set_instrument(self, name):
        if name in self.instruments and self.midi_out:
            self.current_instrument = name
            program = self.instruments[name]
            self.midi_out.set_instrument(program)
            print(f"Instrumento cambiado a: {name} (Program {program})")

    def note_on(self, note, velocity=100):
        if self.midi_out:
            self.midi_out.note_on(note, velocity)

    def note_off(self, note, velocity=0):
        if self.midi_out:
            self.midi_out.note_off(note, velocity)

    def close(self):
        if self.midi_out:
            del self.midi_out
        pygame.midi.quit()

if __name__ == "__main__":
    # Prueba rápida
    ic = InstrumentController()
    if ic.midi_out:
        print("Probando Piano...")
        ic.note_on(60) # C4
        time.sleep(0.5)
        ic.note_off(60)
        
        print("Probando Guitarra...")
        ic.set_instrument("Guitar")
        ic.note_on(64) # E4
        time.sleep(0.5)
        ic.note_off(64)
    ic.close()
