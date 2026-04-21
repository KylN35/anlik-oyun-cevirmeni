import re
import sys
import cv2
import numpy as np
import mss
import pytesseract
import keyboard
import requests
import json
import os
from difflib import SequenceMatcher 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QSizeGrip, QSizePolicy, QFrame, 
                             QGraphicsDropShadowEffect, QPushButton, QLineEdit, 
                             QMessageBox, QComboBox)
from PyQt5.QtCore import Qt, QTimer, QPoint, pyqtSignal, QThread

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
CONFIG_FILE = "config.json"

PROMPTS = {
    "JRPG / Hikaye Odaklı": "Sen profesyonel bir oyun yerelleştirme uzmanısın. Görevin, ekrandaki İngilizce metinleri kelimesi kelimesine çevirmek değil, Türk oyunculara en doğal gelecek şekilde uyarlamaktır. Karakterlerin duygularını, aralarındaki ilişki dinamiklerini ve sokak jargonunu koru. İngilizce deyimleri doğrudan çevirmek yerine Türkçe karşılıklarını bul. Metin bir menü veya eşya açıklamasıysa kısa ve anlaşılır tut. Asla tırnak işareti kullanma, not düşme veya ekstra açıklama yapma; sadece nihai çeviriyi ver.",
    "FPS / Rekabetçi": "Sen rekabetçi nişancı (FPS) ve aksiyon oyunları için çalışan bir yerelleştirme uzmanısın. Ekranda okuduğun metinler genellikle hızlı reaksiyon gerektiren yetenek açıklamaları, maç sunucusu anonsları veya takım içi taktiksel çağrılardır. Çevirilerini kısa, vurucu ve aksiyon hissiyatını koruyacak şekilde, Türk oyuncu jargonuna uygun yap. Asla açıklama ekleme, sadece çeviriyi ver.",
    "FRP / Derin RPG": "Sen derin hikayeli fantastik rol yapma oyunları (RPG) için usta bir yerelleştirme çevirmenisin. Zindanlar, büyüler, fantastik yaratıklar ve evren terminolojisine tam anlamıyla hakimsin. Karakter diyaloglarını ve eşya açıklamalarını çevirirken edebi, destansı ve atmosfere uygun bir dil kullan; ancak oyuncunun oyun mekaniklerini anlamasını zorlaştırma. Sadece doğrudan çeviriyi ver, asla kendi yorumunu katma.",
    "Genel Çeviri": "Sen usta bir çevirmensin. Verilen metni oyun bağlamına en uygun, doğal ve akıcı Türkçe ile çevir. Sadece çeviriyi ver, ekstra açıklama yapma."
}

class TranslationWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, text, api_key, system_prompt):
        super().__init__()
        self.text = text
        self.api_key = api_key
        self.system_prompt = system_prompt

    def run(self):
        invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        
        payload = {
            "model": "meta/llama-3.3-70b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": self.text
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.3
        }

        try:
            response = requests.post(invoke_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            translated_text = data["choices"][0]["message"]["content"].strip()
            self.finished.emit(translated_text)
        except Exception as e:
            print(f"GERÇEK HATA BURADA: {e}") 
            # Eğer response hatasıysa içeriğini de yazdıralım
            if hasattr(e, 'response') and e.response is not None:
                print(f"SUNUCU CEVABI: {e.response.text}")
            self.error.emit("Çeviri Hatası! API Anahtarını kontrol et.")

class TransparentOverlay(QMainWindow):
    pause_signal = pyqtSignal()
    lock_signal = pyqtSignal()

    def __init__(self, api_key, system_prompt):
        super().__init__()
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 800, 250) 
        self.setMinimumSize(400, 150) 

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

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
        self._is_dragging = False 
        self.worker = None

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
        opacity = "0.85" if is_translating else "1.0"
        
        self.text_label.setStyleSheet(f"""
            background-color: rgba(20, 20, 22, 130); 
            color: rgba(234, 230, 214, {opacity});
            font-size: 26px; 
            font-weight: 500; 
            font-style: {font_style};
            font-family: 'Georgia', 'Times New Roman', serif; 
            padding: 15px; 
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            line-height: 1.5;
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.is_locked:
            if event.pos().x() > self.width() - 30 and event.pos().y() > self.height() - 30:
                self._is_dragging = False
            else:
                self._is_dragging = True
                self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and not self.is_locked and self._is_dragging:
            delta = event.globalPos() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = False 

    def on_translation_finished(self, translated_text):
        self.update_label_style("#EAE6D6", is_translating=False)
        self.text_label.setText(translated_text)
        self.worker = None

    def on_translation_error(self, error_msg):
        self.update_label_style("#FF9999", is_translating=False)
        self.text_label.setText(error_msg)
        self.worker = None

    def capture_and_read(self):
        if self.is_paused or self.worker is not None:
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

            current_text = current_text.replace('|', 'I') 
            current_text = re.sub(r'\bl\b', 'I', current_text) 

            if current_text:
                if self.last_translated_text and SequenceMatcher(None, current_text, self.last_text).ratio() > 0.85:
                    return 

                if current_text == self.last_text:
                    self.stable_count += 1
                    
                    if self.stable_count == 2:
                        self.update_label_style("#EAE6D6", is_translating=True) 
                        self.text_label.setText("Nvidia AI Çeviriyor...")
                        
                        self.worker = TranslationWorker(current_text, self.api_key, self.system_prompt)
                        self.worker.finished.connect(self.on_translation_finished)
                        self.worker.error.connect(self.on_translation_error)
                        self.worker.start()
                        
                        self.last_translated_text = current_text
                else:
                    self.last_text = current_text
                    self.stable_count = 0
                    self.update_label_style("#EAE6D6", is_translating=True)
                    self.text_label.setText("...") 
        except Exception as e:
            pass 

class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yapay Zeka Oyun Çevirmen")
        self.setFixedSize(400, 420)
        self.setStyleSheet("background-color: #1E1E22;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("NVIDIA AI ÇEVİRİ ARACI", self)
        self.title_label.setStyleSheet("color: #EAE6D6; font-size: 22px; font-weight: bold; font-family: 'Segoe UI';")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.info_label = QLabel("F9: Duraklat | F10: Kilitle", self)
        self.info_label.setStyleSheet("color: #A0A0A0; font-size: 14px; margin-bottom: 10px;")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        self.api_input = QLineEdit(self)
        self.api_input.setPlaceholderText("Nvidia NIM API Anahtarını Girin...")
        self.api_input.setEchoMode(QLineEdit.Password)
        self.api_input.setStyleSheet("""
            QLineEdit {
                background-color: #2A2A30;
                color: #EAE6D6;
                padding: 10px;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                font-size: 12px;
                margin-bottom: 5px;
            }
        """)
        self.layout.addWidget(self.api_input)

        self.genre_combo = QComboBox(self)
        self.genre_combo.addItems(PROMPTS.keys())
        self.genre_combo.setStyleSheet("""
            QComboBox {
                background-color: #2A2A30;
                color: #EAE6D6;
                padding: 10px;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                font-size: 14px;
                margin-bottom: 15px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #2A2A30;
                color: #EAE6D6;
                selection-background-color: #4CAF50;
            }
        """)
        self.layout.addWidget(self.genre_combo)

        self.load_api_key()

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

    def load_api_key(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as file:
                    data = json.load(file)
                    if "api_key" in data:
                        self.api_input.setText(data["api_key"])
            except Exception:
                pass

    def save_api_key(self, api_key):
        with open(CONFIG_FILE, "w") as file:
            json.dump({"api_key": api_key}, file)

    def start_overlay(self):
        api_key = self.api_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir Nvidia API Anahtarı girin!")
            return
        
        self.save_api_key(api_key)
        
        selected_genre = self.genre_combo.currentText()
        system_prompt = PROMPTS[selected_genre]
        
        self.overlay = TransparentOverlay(api_key, system_prompt)
        self.overlay.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = LauncherWindow()
    launcher.show()
    sys.exit(app.exec_())