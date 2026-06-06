import cv2
from hand_tracker import HandTracker
from instrument import InstrumentController
from ui import UIManager

def main():
    # Inicialización
    cap = cv2.VideoCapture(0)
    # Obtener dimensiones reales de la cámara
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    tracker = HandTracker()
    instrument = InstrumentController()
    ui = UIManager(width, height)
    
    playing_notes = set()
    last_instrument_change = 0 # Debounce simple para cambio de instrumento
    
    print("Iniciando AirPiano... Presiona 'q' para salir.")

    while True:
        success, frame = cap.read()
        if not success:
            break
        
        frame = cv2.flip(frame, 1) # Espejo
        frame = tracker.find_hands(frame)
        landmarks = tracker.get_landmarks(frame)
        
        # Extraer puntas de los dedos (índices 8, 12, 16, 20)
        finger_points = []
        if landmarks:
            for hand in landmarks:
                for tid in [8, 12, 16, 20]:
                    finger_points.append((hand[tid][1], hand[tid][2]))
        
        # Actualizar UI y obtener notas presionadas
        pressed_notes, selected_instrument = ui.update_states(finger_points)
        
        # Lógica de Cambio de Instrumento
        if selected_instrument and selected_instrument != instrument.current_instrument:
            instrument.set_instrument(selected_instrument)
            
        # Lógica de Notas MIDI
        # Notas que deben empezar a sonar
        for note in pressed_notes:
            if note not in playing_notes:
                instrument.note_on(note)
                playing_notes.add(note)
        
        # Notas que deben dejar de sonar
        to_remove = set()
        for note in playing_notes:
            if note not in pressed_notes:
                instrument.note_off(note)
                to_remove.add(note)
        playing_notes -= to_remove
        
        # Dibujar Interfaz
        ui.draw_all(frame)
        
        # Dibujar círculos en las puntas de los dedos para feedback visual
        for fx, fy in finger_points:
            cv2.circle(frame, (fx, fy), 10, (0, 0, 255), cv2.FILLED)

        cv2.imshow("AirPiano", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Limpieza
    for note in playing_notes:
        instrument.note_off(note)
    instrument.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
