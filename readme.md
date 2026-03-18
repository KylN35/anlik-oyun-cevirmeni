# 🎮 Anlık Oyun Çevirmeni (Real-Time Game & Visual Novel Translator)

Selamlar! Bu projeyi, özellikle Persona 5 Royal gibi hikaye tabanlı JRPG'leri veya bol metinli Visual Novel'ları oynarken sürekli çeviri programlarına alt-tab yapmaktan sıkıldığım için geliştirdim. 

Ekranda belirlediğiniz bir alanı saniyede bir okuyor ve arka planda oyunu bölmeden, şeffaf bir arayüzle Türkçe'ye çeviriyor. Temel amacım, ekranda sürekli flaş gibi patlayan ve göz yoran tasarımlar yerine, sanki bir "kitap okuyormuş" hissiyatı veren, oyunun atmosferine yedirilmiş bir çeviri deneyimi sunmaktı.

<img width="1919" height="1079" alt="1773863484353" src="https://github.com/user-attachments/assets/93a11122-9ec5-4af1-b648-5ae057bf5b61" />


## 💡 Neler Yapabiliyor?

* **Anlık ve Kesintisiz Çeviri:** Hedef bölgedeki metni oyunu dondurmaya gerek kalmadan anında yakalayıp çevirir.
* **Daktilo (Typewriter) Efektiyle Başa Çıkma:** Oyunlarda metinlerin harf harf ekrana gelmesi OCR araçlarını genelde çıldırtır. Bu program, OCR sapmalarını önlemek için metnin tamamen sabitlenmesini bekliyor (debouncing) ve yarım yamalak, eksik çevirilerin önüne geçiyor.
* **Göz Yormayan "Kitap Sayfası" Arayüzü:** Uzun okumalarda gözü mahvetmemesi için arayüzü karanlık modda, serif fontlarla ve olabildiğince sade tasarladım. Okurken program varlığını hissettirmiyor bile.
* **Görüntü Temizleme (OpenCV):** Saydam metin kutularında veya renkli arka planlarda yazılar birbirine girmesin diye ufak bir ön işleme yapıyoruz. Anlık ekran görüntüsüne gri tonlama, büyütme ve threshold (eşikleme) filtreleri uygulayarak yazıları OCR için belirginleştiriyoruz.

## ⌨️ Kullanım ve Kısayollar

Programı açtıktan sonra ekrandaki yeşil/saydam çerçeveyi oyunun metin kutusuna denk getirin. Oyuna daldıktan sonra fareyle uğraşmamak için şu kısayolları kullanabilirsiniz:

* **`F9` - Duraklat / Devam Et:** Ara sahneler girdiğinde veya çeviriye o an ihtiyaç duymadığınızda programı hızlıca uyku moduna alabilirsiniz.
* **`F10` - Çerçeveyi Kilitle:** "Arayüzü yanlışlıkla kaydırdım" derdini bitirir. Okuma çerçevesini görünmez yapar ve programı oyunun kendi arayüzüymüş gibi ekrana kilitler.

## 🛠️ Arka Planda Neler Çalışıyor?

* **Python 3.x**
* **PyQt5:** O şeffaf, çerçevesiz ve her zaman üstte duran arayüzü yapmamızı sağlayan kütüphane.
* **Tesseract OCR (PyTesseract):** İşin kalbi, metin okuma motorumuz.
* **OpenCV & Numpy:** Tesseract'a göndermeden önce ekran görüntüsünü temizleyip okunabilir hale getiren filtreler.
* **Mss:** Çok daha hızlı ve performanslı ekran görüntüsü almak için (standart kütüphaneler oyunlarda yavaş kalabiliyor).
* **Deep-Translator:** Limitsiz, patlamayan stabil çeviri API'miz.

## 🚀 Nasıl Kurulur?

Kendi bilgisayarınızda denemek veya kodu kurcalamak isterseniz adımlar çok basit:

### 1. Tesseract OCR Kurulumu (Zorunlu)
Programın metinleri okuyabilmesi için sisteminizde Tesseract kurulu olmalı.
* [Tesseract OCR Windows sürümünü buradan indirin](https://github.com/UB-Mannheim/tesseract/wiki) ve kurun.
* Kurulumu yaparken varsayılan yolu (`C:\Program Files\Tesseract-OCR\tesseract.exe`) değiştirmemeye çalışın. Farklı bir yere kurarsanız `ceviri.py` içindeki Tesseract yolunu kendi bilgisayarınıza göre güncellemeniz gerekecek.

### 2. Kütüphaneleri Yükleme
Projeyi bilgisayarınıza klonlayın ve gerekli Python paketlerini kurun:

```bash
git clone [https://github.com/KylN35/anlik-oyun-cevirmeni.git](https://github.com/KylN35/anlik-oyun-cevirmeni.git)
cd anlik-oyun-cevirmeni
pip install -r requirements.txt
