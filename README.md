# 🎮 Anlık Oyun Çevirmeni (Live Game Translator)

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Nvidia AI](https://img.shields.io/badge/Nvidia-Llama_3.3_AI-76B900?style=for-the-badge&logo=nvidia&logoColor=white)

Bu proje, oyunlardaki İngilizce metinleri anlık olarak ekran üzerinden okuyup (OCR) Türkçe'ye çeviren ve oyunun üzerine şeffaf bir katman olarak yansıtan gelişmiş bir yerelleştirme aracıdır. Özellikle resmi Türkçe dil desteği olmayan **JRPG, Visual Novel ve FPS** oyunları için tasarlanmıştır.

---

## 📂 Proje Yapısı

Proje, ihtiyaçlara göre iki farklı motor seçeneği sunar:

| Klasör | Motor | Özellikler |
| :--- | :--- | :--- |
| [**V1_Google_Ceviri**](./V1_Google_Ceviri) | Google Translate | Hızlı, stabil ve kurulum gerektirmeyen temel sürüm. |
| [**V2_Nvidia_AI_Ceviri**](./V2_Nvidia_AI_Ceviri) | **Nvidia Llama 3.3 AI** | Bağlamı anlayan, oyun jargonu kullanan profesyonel sürüm. |

---

## ✨ Neden V2 (Nvidia AI) Sürümü?

V2 sürümü, klasik makine çevirisi hatalarını minimuma indirmek için **Nvidia NIM API** altyapısını kullanır.

* **Bağlam Duyarlı Çeviri:** Karakterlerin konuşma tarzını ve oyunun atmosferini (Ortaçağ, Siberpunk, Sokak Jargonu) korur.
* **Oyun Türü Seçimi:** JRPG, FPS veya FRP türlerinden birini seçerek yapay zekanın o türe özel çeviri yapmasını sağlayabilirsiniz.
* **Gecikmesiz Deneyim:** `QThread` yapısı sayesinde çeviri işlemi arka planda yapılır, oyun sırasında takılma yapmaz.
* **Kullanıcı Dostu Arayüz:** Modern, karanlık tema destekli ve kilitlenebilir overlay sistemi.

---

## 🛠️ Hızlı Kurulum

1.  **Tesseract OCR Yükleyin:** Bilgisayarınızda [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) yüklü olmalıdır.
2.  **Kütüphaneleri Kurun:**
    ```bash
    pip install opencv-python numpy mss pytesseract keyboard PyQt5 requests
    ```
3.  **API Anahtarı:** V2 sürümü için [Nvidia Build](https://build.nvidia.com/) üzerinden ücretsiz API anahtarınızı alın.

---

## ⌨️ Kontroller

* **`F9`**: Çeviriyi Duraklat / Başlat.
* **`F10`**: Arayüzü Kilitle / Aç (Kilitliyken pencereye tıklanamaz, doğrudan oyun kontrol edilebilir).
* **Sürükle-Bırak**: Çeviri çerçevesini ekranın istediğiniz yerine taşıyın ve boyutlandırın.

---

## 🛡️ Güvenlik Notu
`V2_Nvidia_AI_Ceviri` klasörü içinde bulunan `.gitignore` dosyası sayesinde `config.json` (API anahtarınız) asla GitHub'a yüklenmez. Kendi güvenliğiniz için bu dosyayı manuel olarak yüklemeyiniz.

---

## 👨‍💻 Geliştirici
**Arda Aktaş** 

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=flat-square&logo=github)](https://github.com/KylN35)
