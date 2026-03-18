import sys
import cv2
import numpy as np
import mss
import pytesseract
import keyboard
from difflib import SequenceMatcher 
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QSizeGrip, QSizePolicy, QFrame, QGraphicsDropShadowEffect, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPoint, pyqtSignal 
from deep_translator import GoogleTranslator

# DİKKAT: Tesseract yolunu kontrol et
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ==========================================
# OYUN İÇİ ŞEFFAF ÇEVİRİ ARAYÜZÜ (OVERLAY)
# ==========================================
class TransparentOverlay(QMainWindow):
    pause_signal = pyqtSignal()
    lock_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 800, 250) 
        self.setMinimumSize(400, 150) 

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # ÜST KISIM (ÇEVİRİ PANELİ)
        self.text_label = QLabel("Çeviri Bekleniyor...\n[F9: Duraklat | F10: Kilitle]", self)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setWordWrap(True)
        self.text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setColor(Qt.black)
        shadow.setOffset(2, 2)
        self.text_label.setGraphicsEffect(shadow)
        
        self.layout.addWidget(self.text_label)
        self.update_label_style("#EAE6D6", is_translating=False) 

        # ALT KISIM (EKRAN YAKALAMA ÇERÇEVESİ)
        self.capture_frame = QFrame(self)
        self.capture_frame.setStyleSheet("""
            background-color: transparent;
            border: 1px dashed rgba(255, 255, 255, 60);
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """)
        self.capture_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.capture_frame)

        self.frame_layout = QVBoxLayout(self.capture_frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        
        # BOYUTLANDIRMA KÖŞESİ 
        self.size_grip = QSizeGrip(self.capture_frame)
        self.size_grip.setStyleSheet("""
            background-color: rgba(30, 30, 32, 220); 
            border: 2px solid rgba(234, 230, 214, 180); 
            width: 25px; 
            height: 25px; 
            border-top-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """)
        self.frame_layout.addWidget(self.size_grip, 0, Qt.AlignBottom | Qt.AlignRight)

        self.oldPos = self.pos()
        self.sct = mss.mss() 
        
        self.last_text = ""
        self.last_translated_text = "" 
        self.stable_count = 0
        
        self.is_paused = False 
        self.is_locked = False 
        self._is_dragging = False # YENİ: Sürükleme kontrol değişkeni

        self.pause_signal.connect(self.toggle_pause)
        self.lock_signal.connect(self.toggle_lock)

        keyboard.add_hotkey('F9', lambda: self.pause_signal.emit())
        keyboard.add_hotkey('F10', lambda: self.lock_signal.emit())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_and_read)
        self.timer.start(1000)

    def toggle_lock(self):
        self.is_locked = not self.is_locked
        if self.is_locked:
            self.size_grip.hide() 
            self.capture_frame.setStyleSheet("""
                background-color: transparent;
                border: 1px dashed rgba(255, 255, 255, 10);
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            """)
            self.update_label_style("#98FB98", is_translating=False)
            self.text_label.setText("Arayüz Kilitlendi.\n(Açmak için F10)")
        else:
            self.size_grip.show() 
            self.capture_frame.setStyleSheet("""
                background-color: transparent;
                border: 1px dashed rgba(255, 255, 255, 60);
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            """)
            self.update_label_style("#EAE6D6", is_translating=False)
            self.text_label.setText("Kilit Açıldı.\n[F9: Duraklat | F10: Kilitle]")

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.update_label_style("#FF9999", is_translating=False) 
            self.text_label.setText("Çeviri Duraklatıldı.\n(Devam etmek için F9)")
            self.last_translated_text = "" 
        else:
            self.update_label_style("#EAE6D6", is_translating=False)
            self.text_label.setText("Çeviri Bekleniyor...")

    def update_label_style(self, color, is_translating=False):
        font_style = "italic" if is_translating else "normal"
        opacity = "0.7" if is_translating else "1.0"
        
        self.text_label.setStyleSheet(f"""
            background-color: rgba(20, 20, 22, 230); 
            color: {color}; 
            font-size: 26px; 
            font-weight: 400; 
            font-style: {font_style};
            font-family: 'Georgia', 'Times New Roman', serif; 
            padding: 20px; 
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            line-height: 1.5;
        """)

    # --- ÇÖZÜMÜN OLDUĞU FARE KONTROL KISMI ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.is_locked:
            # Fare sağ alt köşedeki 30x30 piksellik alana (butonun üstüne) tıklandıysa taşımayı iptal et
            if event.pos().x() > self.width() - 30 and event.pos().y() > self.height() - 30:
                self._is_dragging = False
            else:
                self._is_dragging = True
                self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        # Sadece _is_dragging True ise pencereyi hareket ettir
        if event.buttons() == Qt.LeftButton and not self.is_locked and self._is_dragging:
            delta = event.globalPos() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = False # Tıklama bırakıldığında sürüklemeyi sıfırla

    def capture_and_read(self):
        if self.is_paused:
            return

        global_pos = self.capture_frame.mapToGlobal(QPoint(0, 0))
        cap_width = max(10, self.capture_frame.width() - 4)
        cap_height = max(10, self.capture_frame.height() - 4)

        rect = {
            'top': global_pos.y() + 2, 
            'left': global_pos.x() + 2, 
            'width': cap_width, 
            'height': cap_height
        }
        
        try:
            sct_img = self.sct.grab(rect)
            img = np.array(sct_img)
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            
            custom_config = r'--oem 3 --psm 6'
            current_text = pytesseract.image_to_string(thresh, lang='eng', config=custom_config).strip()
            current_text = " ".join(current_text.split('\n'))

            if current_text:
                if self.last_translated_text and SequenceMatcher(None, current_text, self.last_translated_text).ratio() > 0.85:
                    return 

                if current_text == self.last_text:
                    self.stable_count += 1
                    
                    if self.stable_count == 2:
                        self.update_label_style("#EAE6D6", is_translating=True) 
                        self.text_label.setText("Çevriliyor...")
                        QApplication.processEvents() 
                        
                        translated = GoogleTranslator(source='en', target='tr').translate(current_text)
                        
                        self.update_label_style("#EAE6D6", is_translating=False)
                        self.text_label.setText(translated)
                        
                        self.last_translated_text = current_text
                else:
                    self.last_text = current_text
                    self.stable_count = 0
                    self.update_label_style("#EAE6D6", is_translating=True)
                    self.text_label.setText("...") 
        except Exception as e:
            pass 

# ==========================================
# BAŞLATMA ARAYÜZÜ (LAUNCHER)
# ==========================================
class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Görsel Roman Çevirmen")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #1E1E22;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("ANLIK ÇEVİRİ ARACI", self)
        self.title_label.setStyleSheet("color: #EAE6D6; font-size: 24px; font-weight: bold; font-family: 'Segoe UI';")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.info_label = QLabel("F9: Duraklat | F10: Kilitle", self)
        self.info_label.setStyleSheet("color: #A0A0A0; font-size: 14px; margin-bottom: 20px;")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        self.start_btn = QPushButton("BAŞLAT", self)
        self.start_btn.setFixedSize(200, 50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.start_btn.clicked.connect(self.start_overlay)
        self.layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)

    def start_overlay(self):
        self.overlay = TransparentOverlay()
        self.overlay.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = LauncherWindow()
    launcher.show()
    sys.exit(app.exec_())