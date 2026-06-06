import cv2

class InteractiveElement:
    def __init__(self, x, y, w, h, color=(200, 200, 200), text=""):
        self.rect = (x, y, w, h)
        self.color = color
        self.base_color = color
        self.text = text
        self.is_pressed = False

    def draw(self, img):
        x, y, w, h = self.rect
        color = (0, 255, 0) if self.is_pressed else self.color
        cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
        
        # Texto centrado
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(self.text, font, 0.6, 2)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, self.text, (text_x, text_y), font, 0.6, (0, 0, 0), 2)

    def is_inside(self, px, py):
        x, y, w, h = self.rect
        return x < px < x + w and y < py < y + h

class PianoKey(InteractiveElement):
    def __init__(self, x, y, w, h, note, text=""):
        super().__init__(x, y, w, h, (255, 255, 255), text)
        self.note = note

class InstrumentButton(InteractiveElement):
    def __init__(self, x, y, w, h, instrument_name):
        super().__init__(x, y, w, h, (150, 150, 150), instrument_name)
        self.instrument_name = instrument_name

class UIManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.keys = []
        self.buttons = []
        self._setup_ui()

    def _setup_ui(self):
        # 8 Teclas (Octava C4 a C5)
        num_keys = 8
        key_w = self.width // num_keys
        key_h = 150
        start_y = self.height - key_h - 20
        notes = [60, 62, 64, 65, 67, 69, 71, 72] # C, D, E, F, G, A, B, C
        labels = ["C", "D", "E", "F", "G", "A", "B", "C"]
        
        for i in range(num_keys):
            self.keys.append(PianoKey(i * key_w + 5, start_y, key_w - 10, key_h, notes[i], labels[i]))

        # Botones de instrumentos
        instruments = ["Piano", "Organ", "Synth", "Guitar", "Drums"]
        btn_w = 100
        btn_h = 50
        for i, name in enumerate(instruments):
            self.buttons.append(InstrumentButton(10 + i * (btn_w + 10), 20, btn_w, btn_h, name))

    def draw_all(self, img):
        for key in self.keys:
            key.draw(img)
        for btn in self.buttons:
            btn.draw(img)

    def update_states(self, finger_points):
        # Reset states
        for key in self.keys:
            key.is_pressed = False
        
        # Check keys
        pressed_keys = []
        for fx, fy in finger_points:
            for key in self.keys:
                if key.is_inside(fx, fy):
                    key.is_pressed = True
                    pressed_keys.append(key.note)
        
        # Check buttons (click simple, no multitouch para cambio de instrumento)
        selected_instrument = None
        for fx, fy in finger_points:
            for btn in self.buttons:
                if btn.is_inside(fx, fy):
                    selected_instrument = btn.instrument_name
        
        return list(set(pressed_keys)), selected_instrument
