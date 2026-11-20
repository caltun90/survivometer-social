# The Survivometer: üretim kiti

Bu depo kanalın tek kaynağıdır: `caltun90/survivometer-social` (herkese açık). Depoya anahtar, belirteç ya da kişisel bilgi yazılmaz. Anahtarlar yalnızca komutlarda ortam değişkeni olarak kullanılır.

## 1. Sabitler

- Kanal: The Survivometer, YouTube @TheSurvivometer. X hesabı Buffer üzerinden bağlı. TikTok sonra eklenecek.
- Dil: videolar İngilizce (seslendirme ve altyazı), hedef kitle Avrupa ve ABD. Cem'e yazılan her şey Türkçe, kısa, sade. Uzun tire hiçbir yerde kullanılmaz.
- Biçim: 9-10 dakikalık "absürt varsayım" videosu. Her bölüm bir felaket ya da tuhaf durumu saat saat, gün gün anlatır ve ekranda hayatta kalma ihtimali (survival odds) göstergesi durur.
- Ritim (Cem onaylayınca başlar): 2 günde bir uzun video (TR 21:00), her gün bir Short ve bir X gönderisi.

## 2. İçerik kuralları (Cem)

- Başlık her zaman "What If ...?" sorusudur. Örnek: "What If You Could Stop Time?", "What If Zombies Took Over Tomorrow?"
- İlk 2 saniye kanca: en fazla 8 kelimelik cümle, 2.0 saniyeden önce biter. İlk kare dolu olur (boş ya da kararan açılış yok), ekranda en fazla 5 kelimelik kanca yazısı ve hareket vardır.
- Görseller ChatGPT'de üretilir (19 Kasım 2026 Cem kararı: "bu görseller daha güzel"). Her bölüm için yaklaşık 50 sahne, hepsi aynı karakter ve stil. Kodla çizilen eski mod (toon.py) yalnızca yedek.
- Mekan ve insanlar (Cem, 19 Kasım 2026): olaylar ABD ve Avrupa'da geçer. Her istemde: Amerikan şehri (tuğla apartman, yangın merdiveni, banliyö evleri, pikap, sarı okul otobüsü) ya da Amerikan kırsalı; cami, minare, kubbe yok; insanlar günlük Batı kıyafetlerinde, erkekler sakalsız, başörtüsü ya da türban yok.
- Hikaye net olmalı: zombi bölümünde zombiler görünür ve olay örgüsü var (kapıyı yumruklayan komşu, market baskını, köprüdeki sürü, kamp gecesi). Zombiler çizgi film tarzı, yeşilimsi gri, kansız.
- Ana karakter (sabit): büyük, tam yuvarlak açık renk kafa, küçük siyah oval gözler, küçük kaşlar, burun ve saç yok, teal (camgöbeği) kapüşonlu, lacivert kot, beyaz spor ayakkabı. Stil: cilalı 2D çizgi film anlatım stili, yumuşak cel gölge, sinematik ışık, katmanlı derinlik, 16:9, görselde hiç yazı yok.
- Ses: yerel Kokoro modeli, ses karışımı `am_puck:0.3,am_fenrir:0.7` (script.py'de KOKORO_VOICE; Cem seçti, 20 Kasım 2026). Kanal adı "survive-o-meter" diye okunur; voice.py bunu fonem düzeltmesiyle otomatik yapar. Metinde "a.m./p.m." yazma, "seven in the morning" gibi yaz (Kokoro "a" deyip durup "em" diyor). Kota yok, her bölümde birebir aynı ses. Model dosyaları GitHub'dan: thewh1teagle/kokoro-onnx releases model-files-v1.0 (kokoro-v1.0.onnx, voices-v1.0.bin), `pip install kokoro-onnx`. Komut: `KOKORO_SPEED=0.88 python3 engine/voice.py <bölüm> kokoro`, sonra `psalign` (satır satır hizalar) ve `GAP_MIN=0.3 GAP_MAX=0.5 BEAT=2.8 ... build` (BEAT 2.5'in altına inmesin: tahtadaki bölüm yazısı 1.75 saniyede yazılıyor, 1.3'te yazı bitmeden sahne geçti ve Cem fark etti). (yaklaşık 1500 kelime 10 dakika eder). Gemini TTS kullanma: aynı ses adı farklı isteklerde farklı çıkıyor (Cem fark etti).
- Kanca (Cem, 20 Kasım 2026): her videonun ilk 4-5 saniyesi Veo ile hareketli video olacak. caltun90 hesabı Google'da Rusya bölgesine bağlı olduğu için Flow ve Gemini'de video şimdilik kapalı; bölge değişikliği bekleniyor.
- Anlatım tarzı (Cem, 20 Kasım 2026, izleyicinin beğendiği "Hâlâ Hayattasın" tarzı): kancadan sonra küçük, sıradan, somut bir anla başla (mutfakta kahve yaparken titreyen telefon, kasada onaylanmayan kart gibi), oradan büyüt. İkinci tekil şahıs ve geniş zaman ("You go to the window."), saat saat akan tek bir hikaye. Seçimler soru listesi değil hikayenin içinde olur ("You could join them. Most people do. You decide to stay put."). Her bölümde gerçekçi, öğretici ayrıntılar (su ısıtıcısındaki su, baz istasyonu bataryası, GPS'in uyduyla çalışması, amatör telsiz). Bölüm başlıkları sonuç cümlesidir ("THE TAPS RUN DRY", "A KNOCK AT THE DOOR"). İhtimal ibresi kalır ama bölüm sonlarında doğal bir cümleyle geçer. Uzunluk 1400-1550 kelime.
- Ses ve görüntü uyumu (Cem, 20 Kasım 2026: bölüm 1'de "görüntü ile ses arasında kaymalar var"). Sebep: v9'da hikaye tarzına geçerken 3-4 cümleyi tek satırda birleştirdik (71 satır, 10-13 saniyelik satırlar); kart, liste, ibre ve seçim ekranı kendi cümlesinden 5-8 saniye önce geldi, tek görsel üç farklı şeyi anlatan cümlelerin üstünde kaldı. Bölüm 2'den itibaren kural: her satır tek cümle ya da tek nefeslik düşünce (en fazla 18 kelime, 3-7 saniye). card, list, odds, choice ve final satırı yalnızca o bilgiyi söyleyen cümledir; önüne arkasına başka cümle eklenmez. Bir görsel en fazla 2 ardışık satırda kalır ve o satırda söyleneni gösterir. Hedef 100-130 satır, 65-80 görsel. INSERTS (telefon, TV) da o an anlatılan cümlenin satırına bağlanır, oran 0.0-0.1. Render'dan sonra her bölümden 2 satır seç, satırın ortasındaki kareyi aç: ekrandaki şey o anda söylenen şey mi, bak.
- Sayılar ve iddialar gerçek kaynağa dayanır, kaynak adı ekranda küçük yazıyla geçer. İhtimal yüzdeleri eğlence amaçlı tahmindir ve son ekranda bu yazılır.
- Şiddet gösterilmez: zombiler yalnızca uzak siluet olarak çizilir; yara, kan ve silah çizilmez. Ton meraklı ve hafif.

## 3. Depo düzeni

- `engine/voice.py`: ses üretimi, hizalama, kurgu zaman çizelgesi.
- `engine/toon.py`: karakter ve sahneler. `engine/render.py`: kare çizimi ve video.
- `episodes/NNN-slug/script.py`: bölüm metni. TITLE, SLUG, VOICE, STYLE, START_ODDS, CHAPTERS (label, tag, accent, lines), GROUPS (bir TTS isteğinde okunacak bölüm grupları). Her satır `(okunacak metin, görsel, [altyazı])`. Görsel türleri: hook, big, card, icon, list, choice, odds, final.
- `episodes/NNN-slug/voice/cuts.json`, `words.json`, `timeline.json` depoda durur. WAV dosyaları ve videolar depoya girmez.
- `log.json`: bölüm kayıtları. Durumlar: taslak, onay-bekliyor, yuklendi.

## 4. Bölüm üretimi

Sahne cihazları (Cem'in örnek videosundan, 20 Kasım 2026; videoyu düz slayt olmaktan çıkarır):
- Sol üstte kırmızı gün rozeti (HOUR 6, DAY 1) ve yanında işleyen hikaye saati. Saat script.py'de her bölümün `clock` alanı.
- Kart ve liste satırları masadaki not defterine elle yazılır, kalem yazıyı takip eder (engine/fx.py, notepad).
- Bölüm başlıkları kara tahtaya tebeşirle yazılır (chalk_card).
- Telefon ve TV araya girişleri: shots.py'de INSERTS = {satır: ("phone_alerts" | "phone_message" | "phone_silent" | "tv", başlangıç oranı)}. Yeni bölümde konuya uyan 3-5 araya giriş seç; yeni ekran türü gerekirse fx.py'ye ekle.
- Ortak görseller engine/assets/ (masa ve defter, kara tahta, eldeki telefon, TV). Her bölümde yeniden üretme.
- Veo klipleri (20 Kasım 2026): caltun90 hesabında gemini.google.com/u/0/videos sayfasında "Videolar" modu açık (Google AI Plus, günde yaklaşık 2 video, 10 sn, 1280x720). Flow bu hesapta kapalı (bölge Rusya). Yöntem: "+" menüsünü aç, `input[type=file]` öğelerine aria-label ver, find ile ref al, file_upload ile görseli yükle (dosya yolu konteynerdeki /mnt/user-data/uploads/... olmalı), istemi yaz, gönder; video hazır olunca sayfadaki `video` öğesinin src'sini fetch edip indir. İstem: "Animate this exact image, keep the same 2D cartoon style..." + tek net hareket + "No text, no captions, no dialogue".
- Her bölümde: klip 1 = kanca (ilk 4-6 sn, hook satırı ve sonraki satırın başı aynı sahne), klip 2 = bölümün en gerilimli anı. shots.py: `CLIPS = {"s01": "clips/s01.mp4"}`; render klibi o sahnenin yerine oynatır, klip bitince son karede durur.

Görsel adımı (ses ve hizalamadan sonra, render'dan önce):
- `episodes/NNN-slug/shots.py`: SHOTS = (kimlik, ad, satır numaraları, side, açıklama). Her satır tam bir sahneye ya da REUSE ile başka sahnenin görseline bağlanır. Liste ve kart satırlarının sahnesinde `side=True`: karakter solda, sağ %40 sakin, çünkü bilgi paneli sağa gelir.
- ChatGPT'de yeni bir sohbet aç. İlk mesajda stil ve karakter tarifini ver, sonra her mesajda tek görsel iste. Her istemin başına kısa stil ve karakter hatırlatması ekle (yoksa 12-13 görselden sonra stil kayıyor). İstemde etiket `SHOT (sNN_ad)` biçiminde olsun; indirme etiketle eşleşir.
- Görseller Cem'in Downloads klasörüne `survNNN_sNN_ad.png` adıyla iner. Adla stage et (Downloads'u listeleme, çok büyük), `episodes/NNN-slug/img/sNN_ad.png` olarak kopyala. img/ depoya girmez.
- Her 10-12 görselde bir toplu kontrol: karakter aynı mı, yazı var mı, stil kaydı mı. Bozuk olanı aynı etiketle tekrar iste.
- Render `shots.py` varsa otomatik görsel modunda çalışır (`RENDER_MODE=toon` eski mod).


Kurulum: `pip install --break-system-packages skia-python numpy soundfile pillow pocketsphinx`, ayrıca ffmpeg.

1. `script.py` yaz. Yaklaşık 1.300 kelime 9,3 dakika eder. Sekiz bölüm, her bölümün sonunda bir "odds" satırı.
2. Ses: `GEMINI_API_KEY=... python3 engine/voice.py episodes/NNN-slug tts`. Varsayılan model `gemini-3.1-flash-tts-preview` (günde yaklaşık 10 istek). Kota biterse ya da SAFETY ile boş dönerse `TTS_MODEL=gemini-2.5-flash-preview-tts` ile kalan grupları üret (ayrı kota, aynı ses). `gemini-3.8-flash-tts` kullanma: stil cümlesini sesli okuyor ve çok hızlı.
3. Hizalama: `python3 engine/voice.py episodes/NNN-slug psalign`. Yerel çalışır, API kotası harcamaz. Satır kesimlerini ve kelime zamanlarını yazar. "BAD lines" derse o satırı `fixline <grup> <satır>` ile yeniden seslendir, sonra o grup için `psalign` tekrar.
4. `python3 engine/voice.py episodes/NNN-slug build`: `voice/final.wav` ve `timeline.json`. Çıktıda toplam süre 9-10 dakika ve "hook ends at" 2.0 saniyenin altında olmalı.
5. Kare kontrolü: `python3 engine/render.py episodes/NNN-slug frames 0 1 1.9 <her bölümden bir saniye>`, `chk/` altındaki kareleri Read ile aç. Bakılacaklar: ilk kare dolu mu, altyazı taşıyor mu, kenarda siyah şerit var mı, ihtimal göstergesi ile altyazı üst üste biniyor mu.
6. Video: süreyi 40 saniyelik parçalara böl, `render.py <bölüm> seg <t0> <t1> <çıktı.mp4>` komutlarını ikişer paralel çalıştır (iki çekirdekte yaklaşık 18 dakika), sonra `render.py <bölüm> join <çıktı.mp4> <parçalar>`.
7. Bitmiş dosyadan 6-8 kare çekip son kez bak.

## 5. Yayın

- Kanal kimliği: UCWCkPXqeOpQKwmO13xnCtqg (The Survivometer, caltun90 hesabının marka kanalı). Bölüm 1: https://youtu.be/eJeKgg5ryMg (20 Kasım 2026 21:00).
- Bu kanal için YouTube API belirteci yok. 20 Kasım 2026'da izin ekranı onaylandı ama dönen kod araç çıktısında gizlendiği için belirteç alınamadı. Yükleme Cem'in Chrome'unda YouTube Studio üzerinden yapılır (Claude in Chrome):
  1. studio.youtube.com aç. Sağ üst hesap > Hesap değiştir > The Survivometer. Adres `/channel/UCWCkPXqeOpQKwmO13xnCtqg` değilse yükleme.
  2. "Video yükle" ile yükleme penceresini aç.
  3. file_upload çağrı başına en fazla 3,8 MB alıyor. Videoyu böl: `split -b 3750000 -d -a 3 --additional-suffix=.bin video.mp4 /mnt/user-data/uploads/surv/parts/part_`. Yeniden kodlama boyutu düşürmedi, deneme.
  4. Sayfaya JS ile kendi dosya girişini ekle (`<input type=file id=claude_chunk aria-label="claude chunk file input">`, sabit konum, görünür). `change` dinleyicisi gelen her `part_NNN.bin` dosyasını `arrayBuffer()` ile okuyup `window.__chunks[ad] = new Blob([b])` yapsın.
  5. `find` ile bu girişin ref'ini al, parçaları sırayla file_upload ile gönder (bir blokta 15-18 çağrı sorunsuz). Arada JS ile sayıyı ve boyutları kontrol et.
  6. JS: parçaları ada göre sırala, tek Blob yap, boyutu ve SHA-256'yı yereldeki dosyayla karşılaştır. Aynıysa `new File([blob], "<Başlık>.mp4", {type:"video/mp4"})`, `input[name=Filedata]` öğesine DataTransfer ile ata, `change` olayı gönder. 226 MB yaklaşık 4 dakikada yüklendi.
  7. Ayrıntılar: başlık ("What If ...?"), açıklama (2-3 cümle kanca, Chapters dakikaları timeline.json'dan, soru, Sources, "The survival odds are estimates for entertainment", yapay zeka görsel ve ses notu, en fazla 5 hashtag), "Hayır, çocuklara özel değil". "Gelişmiş ayarları göster": ücretli tanıtım Hayır, yapay zeka kullanımı Evet (kesin kural), etiketler, video dili İngilizce (Amerika Birleşik Devletleri).
  8. İleri, İleri, İleri. Görünürlük > Planlayın: tarih, saat 21:00, saat dilimi "(GMT+0300) Yerel Saat". Planla. "Video planlandı" penceresinde tarih ve saati gör.
  9. JS çıktısında adres ya da çerez benzeri metin döndürme ("BLOCKED" verir); yalnızca sayı ve kısa metin döndür.
- Özel kapak: `episodes/NNN-slug/thumb.jpg` (1280x720) üret. 20 Kasım'da dosya gönderildi ama Studio kapağı değiştirmedi, hata da göstermedi (büyük olasılıkla kanal telefonla doğrulanmamış). Her yüklemede bir kez dene; olmazsa "Videodan seç" ile en iyi kareyi seç ve raporda yaz.
- X ve Short: Survivometer'ın Buffer anahtarı bu depoda ve görevde yok. Claude'a bağlı Buffer bağlayıcısı engrowapp hesabıdır, bu kanal için KULLANMA. Anahtar gelene kadar X ve Short yok.
- Yükleme Cem'in onayıyla yapılır (bkz. görev talimatı). Aynı videoyu iki kez yükleme.

## 6. Öğrenilenler

- (19 Kasım 2026) Gemini ile zaman damgası ve parça yazıya dökme güvenilmez çıktı ve günlük kotayı bitirdi. Hizalama artık pocketsphinx ile yerel yapılıyor; 1.300 kelimenin tamamını eşleştirdi.
- (19 Kasım 2026) `gemini-2.5-flash-preview-tts` satır aralarına 5 saniyelik boşluk koyabiliyor ve metnin sonuna fazladan konuşma ekleyebiliyor. `psalign` bunu "BAD lines" ve "extra speech" diye bildirir; `build` uzun boşlukları kendisi kısaltır.
- (19 Kasım 2026) Kamera yakınlaşmasında sahne kenarı görünmesin diye odak noktası sahne sınırına kıstırılıyor. Geniş planda kıstırma payı sıfır olmalı, yoksa solda ve üstte siyah şerit çıkar.
- (19 Kasım 2026) ChatGPT Plus görsel sınırı: yaklaşık 24 saatte 130-140 görselden sonra "You're out of images" diyor ve yaklaşık 10 saat bekletiyor. Lala bölümü (36 görsel) ve Survivometer bölümü (yaklaşık 50 görsel) aynı güne denk gelmesin. Sınır gelirse eksik sahneleri shots.py'de REUSE ile mevcut görsellere bağla, videoyu bitir, eksikleri sonra üret.
- (19 Kasım 2026) Uzun ChatGPT sohbetinde görsel başına süre 2,5 dakikaya çıkıyor. Her bölümü iki yeni sohbete böl (iki sekme), sayfa içi beklemeler için Web Worker zamanlayıcısı kullan (arka plan sekmesi yavaşlamasın). Görsel başına yaklaşık 1 dakika.
- (19 Kasım 2026) Bölüm kısa kalırsa: `STRETCH=0.93 GAP_MIN=0.42 GAP_MAX=0.75 BEAT=2.2 python3 engine/voice.py <bölüm> build`. Okumayı yüzde 7 yavaşlatır (kanca hariç), aralıkları açar. 1.213 kelime bu ayarla 9,3 dakika etti.
- (19 Kasım 2026) Ücretsiz ChatGPT hesabı günde yaklaşık 4 görsel veriyor. Plus sınırına takılınca Cem başka hesaba geçebiliyor; yeni hesapta ilk açılışta çıkan şartlar ekranını Cem onaylar. Ücretsiz hesabın çizimi biraz daha düz ve parlak.
- (20 Kasım 2026) Yazı yarım kalmasın: render'dan önce her yazılı sahnenin (tahta kartı, not defteri, telefon, TV) kaybolmadan hemen önceki karesini `render.py <bölüm> frames ...` ile çıkar ve yazının bittiğini gör. Tahta kartı `beat` bitişinden 0.07 sn önce, not defteri `t_in + fx.notepad_len(l, t_in)` bitişinden 0.07 sn önce. Not defteri ve tahta kısa satırda yazıyı kendiliğinden hızlandırır ama kontrol yine yapılır. 4 maddelik listede son satır altyazının üstünde kalmalı.
