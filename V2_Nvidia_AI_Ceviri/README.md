Markdown
# 🤖 V2: Nvidia AI Powered Game Translator
> **"Don't just translate, localize the experience."**

![Nvidia NIM](https://img.shields.io/badge/NVIDIA-NIM_API-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![Model](https://img.shields.io/badge/Model-Llama_3.3_70B-blueviolet?style=for-the-badge&logo=meta&logoColor=white)
![UI](https://img.shields.io/badge/Framework-PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white)

V2 sürümü, klasik makine çevirisinin ötesine geçerek oyun atmosferini doğrudan ekranına taşır. **Nvidia NIM API** altyapısı ve **Llama 3.3 70B** devasa dil modeli sayesinde, çeviriler sadece kelime anlamıyla değil, oyunun ruhuna uygun bir "yerelleştirme" (localization) mantığıyla yapılır.

---

## 🔥 Öne Çıkan Özellikler

* **🧠 Derin Bağlam Analizi:** Llama 3.3 modeli, cümleleri tek tek değil, oyunun genel gidişatına ve karakterlerin konuşma tarzına göre analiz eder.
* **🎭 Dinamik Prompt Mühendisliği:** Seçilen oyun türüne göre yapay zekanın "kişiliği" değişir:
    * **JRPG / Hikaye:** *Persona 5 Royal* gibi oyunlarda karakterlerin duygularını ve günlük sokak jargonunu yakalar.
    * **FPS / Rekabetçi:** *The Finals* veya *Valorant* gibi hızlı oyunlarda kısa, vurucu ve taktiksel anonslar yapar.
    * **FRP / Derin RPG:** Masaüstü RPG veya fantastik evrenlerde edebi ve destansı bir dil kullanır.
* **⚡ Sıfır Takılma (QThread):** Çeviri işlemi arka planda bir iş parçacığı (thread) olarak çalışır. API'den cevap beklerken oyununuz veya çeviri pencereniz asla donmaz.
* **🔒 Akıllı Güvenlik:** API anahtarınız yerel bir `config.json` dosyasında saklanır ve `.gitignore` sayesinde asla GitHub'a sızmaz.

---

## 🛠️ Teknik Kurulum

### 1. Sistem Gereksinimleri
* Python 3.8 veya üzeri.
* [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (Bilgisayarınıza yüklü ve yolu koda tanımlı olmalıdır).

### 2. Kütüphanelerin Kurulumu
Klasörün içindeyken terminale şu komutu girin:
```bash
pip install -r requirements.txt
3. Nvidia NIM API Anahtarı
build.nvidia.com adresine gidin.

Llama 3.3 70B Instruct modelini seçin.

Ücretsiz API anahtarınızı kopyalayın ve uygulama açıldığında ilgili kutucuğa yapıştırın.

🎮 Kullanım Klavuzu
Alan Seçimi: Şeffaf çerçeveyi oyunun altyazı alanının üzerine getirin.

Tür Belirleme: Başlatıcı ekranından oyun türünü (JRPG, FPS vb.) seçin.

Kısayollar:

F9: Çeviriyi anlık duraklatır (Sahneler arası geçişlerde işe yarar).

F10: Arayüzü kilitler. Kilitliyken çerçeve "hayalet" moduna geçer; üzerinden mouse ile oyuna tıklayabilirsiniz.
