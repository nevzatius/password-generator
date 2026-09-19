# Password Generator

Yerel olarak çalışan, basit bir şifre üretici ve şifre kasası uygulaması. Python ve Tkinter ile yazılmıştır, herhangi bir sunucuya veya internet bağlantısına ihtiyaç duymaz — tüm veriler kendi bilgisayarınızda kalır.

## Özellikler

- **Güvenli şifre üretimi**: Uzunluk seçimi, büyük/küçük harf, rakam ve sembol dahil etme seçenekleriyle `secrets` modülü kullanılarak kriptografik olarak güvenli şifreler üretir.
- **Şifre kasası**: Üretilen şifreleri "hangi alan/site için" olduklarıyla birlikte kaydeder ve daha sonra görüntülemenizi sağlar.
- **Giriş sistemi**: Uygulamayı yalnızca sizin kullanabilmeniz için kullanıcı adı + ana şifre ile korunur. İlk açılışta hesap oluşturulur, sonraki açılışlarda giriş yapılır.
- **Uçtan uca şifreleme**: Kasadaki kayıtlar diskte düz metin olarak değil, ana şifrenizden türetilen bir anahtarla şifrelenmiş olarak saklanır. Ana şifreyi bilmeyen biri `vault.dat` dosyasını açsa bile içeriği okuyamaz.

## Nasıl çalışır

- Giriş şifreniz `PBKDF2-HMAC-SHA256` ile salt'lanarak hash'lenir ve `auth.json` içinde saklanır — şifrenizin kendisi hiçbir zaman diske yazılmaz.
- Kasa (`vault.dat`), ana şifrenizden `PBKDF2` ile türetilen bir anahtar kullanılarak `Fernet` (AES tabanlı, kimlik doğrulamalı şifreleme) ile şifrelenir.
- Kasa yalnızca doğru ana şifreyle giriş yapıldığında bellekte çözülür; diskte her zaman şifreli kalır.

## Kurulum

```bash
pip install -r requirements.txt
```

## Çalıştırma

```bash
python main.py
```

İlk çalıştırmada bir kullanıcı adı ve ana şifre belirlemeniz istenecek. Bu bilgiler `auth.json` dosyasında (hash'lenmiş olarak) saklanır ve sonraki açılışlarda giriş yapmak için kullanılır.

## Kullanım

1. **Şifre Üret** sekmesinde uzunluk ve karakter türlerini seçip "Üret" butonuna basın.
2. Üretilen şifreyi "Alan/Site adı" kutusuna kaydetmek istediğiniz alanın adını (örn. `Gmail`) yazıp "Kasaya Kaydet" butonuna basın.
3. **Kayıtlı Şifreler** sekmesinden daha önce kaydettiğiniz tüm şifreleri görüntüleyebilir, panoya kopyalayabilir veya silebilirsiniz.

## Proje Yapısı

```
main.py              # Giriş noktası
auth.py              # Hesap oluşturma / giriş doğrulama
crypto_utils.py      # Anahtar türetme ve şifreleme yardımcıları
vault.py             # Şifreli kasa modeli ve dosya işlemleri
password_gen.py      # Şifre üretim mantığı
ui/
  app.py             # Ekran geçiş kontrolcüsü
  screens_auth.py    # Hesap oluşturma / giriş ekranları
  screens_main.py    # Şifre üretici ve kasa ekranları
```

## Güvenlik Notu

Bu proje kişisel/yerel kullanım için tasarlanmıştır. `auth.json` ve `vault.dat` dosyaları çalışma zamanında oluşturulur ve `.gitignore` ile depo dışında tutulur — bu dosyaları kimseyle paylaşmayın veya versiyon kontrolüne eklemeyin.

## Gereksinimler

- Python 3.10+
- [cryptography](https://pypi.org/project/cryptography/)
