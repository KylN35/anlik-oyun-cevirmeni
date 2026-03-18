\# 🎮 Real-Time Game \& Visual Novel Translator (Anlık Oyun Çevirmeni)



Bu proje, ekrandaki belirli bir bölgedeki İngilizce metinleri anlık olarak algılayan, görüntü işleme algoritmalarıyla netleştiren ve Türkçe'ye çevirerek şeffaf bir arayüz üzerinde gösteren bir masaüstü uygulamasıdır. 



Özellikle metin yoğunluğu yüksek olan \*\*Görsel Romanlar (Visual Novels)\*\* ve hikaye tabanlı \*\*JRPG'ler (örneğin Persona 5 Royal vb.)\*\* oynarken akıcılığı bozmadan, göz yormayan bir çeviri deneyimi sunmak amacıyla Python ile geliştirilmiştir.



!\[Ekran Görüntüsü](\[Buraya programın çalışırken çekilmiş bir ekran görüntüsünü veya GIF'ini ekleyin])



\## ✨ Özellikler



\* \*\*Anlık ve Kesintisiz Çeviri:\*\* Ekrandaki hedef bölgeyi saniyede bir okur ve metni anında çevirir.

\* \*\*Daktilo Efekti (Typewriter) Koruması:\*\* Oyunlardaki harf harf ekrana gelen diyalogları algılar. OCR sapmalarını ve eksik çevirileri önlemek için metin tamamen sabitlenene kadar (debouncing) bekler.

\* \*\*Şeffaf ve Kitap Estetiğinde Arayüz:\*\* Oyunun arayüzünü kapatmayan, serif fontlarla desteklenmiş, uzun okumalarda göz yormayan "karanlık mod / kitap sayfası" estetiğine sahip dinamik UI.

\* \*\*Gelişmiş Görüntü İşleme:\*\* Saydam oyun metin kutularındaki parlamaları ve renk karmaşasını çözmek için OpenCV ile gri tonlama, büyütme ve eşikleme (thresholding) filtreleri uygular.

\* \*\*Akıllı Kısayollar:\*\* Oyun oynarken fareye ihtiyaç duymadan arayüzü kontrol edebilme.



\## ⌨️ Kısayollar ve Kullanım



Programı başlattıktan sonra yeşil/saydam çerçeveyi oyunun metin kutusuna hizalayın ve arayüzü yönetmek için kısayolları kullanın:



\* \*\*`F9` - Duraklat / Devam Et:\*\* Ara sahnelerde veya çeviri istemediğiniz anlarda programı uyku moduna alır.

\* \*\*`F10` - Pencereyi Kilitle:\*\* Arayüzün yanlışlıkla sürüklenmesini veya boyutunun değişmesini engeller. Okuma çerçevesini görünmez yaparak oyunun atmosferine uyum sağlar.



\## 🛠️ Kullanılan Teknolojiler



\* \*\*Python 3.x\*\*

\* \*\*PyQt5:\*\* Çerçevesiz (Frameless), şeffaf ve her zaman üstte duran (Always on Top) grafik arayüz (GUI) mimarisi.

\* \*\*Tesseract OCR (PyTesseract):\*\* Optik karakter tanıma motoru.

\* \*\*OpenCV \& Numpy:\*\* OCR doğruluk oranını artırmak için ön görüntü işleme.

\* \*\*Mss:\*\* Ultra hızlı ekran görüntüsü yakalama.

\* \*\*Deep-Translator:\*\* Limitsiz ve stabil çeviri API entegrasyonu.



\## 🚀 Kurulum



Bu projeyi kendi bilgisayarınızda çalıştırmak veya geliştirmek için aşağıdaki adımları izleyin:



\### 1. Tesseract OCR Kurulumu (Zorunlu)

Bu program metinleri okuyabilmek için Tesseract motoruna ihtiyaç duyar.

\* \[Tesseract OCR Windows sürümünü buradan indirin](https://github.com/UB-Mannheim/tesseract/wiki) ve kurun.

\* Kurulum yolunun `C:\\Program Files\\Tesseract-OCR\\tesseract.exe` olduğundan emin olun (Farklı bir yere kurarsanız `ceviri.py` içindeki yolu güncelleyin).



\### 2. Kütüphanelerin Kurulumu

Projeyi klonlayın ve gerekli Python kütüphanelerini yükleyin:



```bash

git clone https://github.com/KylN35/anlik-oyun-cevirmeni.git

cd \anlık-oyun-cevirmeni

pip install -r requirements.txt

