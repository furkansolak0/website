#!/usr/bin/env python3
"""İngilizce sayfalardan (index/prolig/baykul) Türkçe sürümleri tr/ klasörüne üretir.

Kullanım:  python3 tools/build_tr.py
Yeni bir İngilizce metin eklenirse TR sözlüğüne karşılığı eklenmeli; betik
çevrilmemiş metinleri listeler.
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "prolig.html", "baykul.html"]

# Çevrilmeden kalması gereken metinler (özel adlar, sayılar vb.)
KEEP = {
    "OFS", "Prolig", "Baykul Broadcaster", "OFS Dış Ticaret Ltd. Şti.", "Furkan Solak",
    "furkan@ofsenterprise.com", "YouTube", "Instagram", "Android", "Bonzalex vs Red Bull FC",
    "EN", "TR", "|", "/", "2022", "500+", "2026", "150+", "300+", "1", "2", "3",
}

TR = {
    # --- ortak ---
    "Get in touch": "İletişime geçin",
    "Open main menu": "Menüyü aç",
    "Approach": "Yaklaşım",
    "Products": "Ürünler",
    "Company": "Şirket",
    "Contact": "İletişim",
    "About": "Hakkımızda",
    "Features": "Özellikler",
    "Screens": "Ekranlar",
    "Roadmap": "Yol haritası",
    "Live": "Canlı",
    "All products": "Tüm ürünler",
    "Follow": "Takip edin",
    "OFS company site": "OFS şirket sitesi",
    "OFS logo": "OFS logosu",
    "©  OFS Dış Ticaret Ltd. Şti. · Istanbul, Türkiye": "©  OFS Dış Ticaret Ltd. Şti. · İstanbul, Türkiye",
    "OFS Dış Ticaret Ltd. Şti. · Istanbul, Türkiye": "OFS Dış Ticaret Ltd. Şti. · İstanbul, Türkiye",
    "©": "©",
    "Istanbul, Türkiye": "İstanbul, Türkiye",
    "Istanbul": "İstanbul",
    "Closed beta": "Kapalı beta",
    "Live in Kocaeli": "Kocaeli'de yayında",
    "View product": "Ürünü incele",
    "Works with": "Birlikte çalışır",
    "Log it once": "Bir kez girin",
    "It reaches the stream": "Yayına yansır",
    "The league updates itself": "Lig kendini günceller",
    "A goal, card or substitution is entered on the camera screen in Baykul Broadcaster, or on the operator screen in Prolig.":
        "Gol, kart ya da oyuncu değişikliği Baykul Broadcaster'ın kamera ekranından veya Prolig'in operatör ekranından girilir.",
    "The scorebug and lineup overlays on YouTube Live update in real time.":
        "YouTube Live'daki skor ve kadro grafikleri gerçek zamanlı güncellenir.",
    "Standings, top scorers, reports and social graphics in Prolig follow automatically.":
        "Prolig'deki puan tablosu, gol krallığı, raporlar ve sosyal medya görselleri kendiliğinden güncellenir.",
    "Done": "Tamamlandı",
    "Now": "Şimdi",
    "Next": "Sırada",

    # --- ana sayfa ---
    "OFS — Software products, built in Istanbul": "OFS — İstanbul'da geliştirilen yazılım ürünleri",
    "OFS Dış Ticaret Ltd. Şti. is an Istanbul-based company that designs, builds and operates its own software products.":
        "OFS Dış Ticaret Ltd. Şti., kendi yazılım ürünlerini tasarlayan, geliştiren ve işleten İstanbul merkezli bir şirkettir.",
    "An Istanbul-based company that designs, builds and operates its own software products.":
        "Kendi yazılım ürünlerini tasarlayan, geliştiren ve işleten İstanbul merkezli bir şirket.",
    "Istanbul · Founded 2022": "İstanbul · Kuruluş 2022",
    "Software products, built in Istanbul.": "İstanbul'da geliştirilen yazılım ürünleri.",
    "OFS designs, builds and operates its own software products — from the first idea to real users in the field.":
        "OFS, kendi yazılım ürünlerini ilk fikirden sahadaki gerçek kullanıcılara kadar kendisi tasarlar, geliştirir ve işletir.",
    "Explore our products": "Ürünlerimizi inceleyin",
    "About the company": "Şirket hakkında",
    "— streaming a league match in Kocaeli": "— Kocaeli'de bir lig maçını yayınlıyor",
    "Company founded": "Şirketin kuruluşu",
    "Headquarters": "Merkez",
    "Videos streamed with our software": "Yazılımımızla yayınlanan video",
    "Products live with real users": "Ürünler gerçek kullanıcılarla yayında",
    "How we build": "Nasıl geliştiriyoruz",
    "We take an everyday problem, build a working product for it, and keep improving it with the people who use it.":
        "Gündelik bir sorunu ele alır, ona çalışan bir ürün geliştirir ve ürünü kullananlarla birlikte iyileştirmeye devam ederiz.",
    "Built in-house": "Kendi bünyemizde",
    "Design, development and operations stay under one roof, so every product is something we fully understand and can support.":
        "Tasarım, geliştirme ve işletme tek çatı altında kalır; böylece her ürünü bütünüyle tanır ve destekleyebiliriz.",
    "Shaped with real users": "Gerçek kullanıcılarla şekillenir",
    "Products go into the field early. Feedback from the first users decides what we build next.":
        "Ürünler sahaya erken çıkar. Bir sonraki adımı ilk kullanıcılardan gelen geri bildirim belirler.",
    "AI-assisted development": "Yapay zekâ destekli geliştirme",
    "We build with modern AI tools, which lets a small company move from idea to working product quickly.":
        "Modern yapay zekâ araçlarıyla geliştiriyoruz; bu, küçük bir şirketin fikirden çalışan ürüne hızla ilerlemesini sağlıyor.",
    "What we build": "Neler geliştiriyoruz",
    "Two connected products for amateur football. Each works on its own, and together they keep the stream and the league in sync.":
        "Amatör futbol için birbirine bağlı iki ürün. Her biri tek başına çalışır; birlikte kullanıldığında yayın ve lig hep eşzamanlı kalır.",
    "League management": "Lig yönetimi",
    "A league management app for amateur football: from lineups and live scoring to standings, statistics and season reports.":
        "Amatör futbol için lig yönetim uygulaması: kadrolardan canlı skora, puan tablosundan istatistiklere ve sezon raporlarına.",
    "Live scoring, standings and player stats": "Canlı skor, puan tablosu ve oyuncu istatistikleri",
    "PDF match and season reports": "PDF maç ve sezon raporları",
    "Ready-to-post social graphics": "Paylaşıma hazır sosyal medya görselleri",
    "Live streaming": "Canlı yayın",
    "Turns a phone into a broadcast camera. Streams matches to YouTube Live with real-time score overlays.":
        "Telefonu yayın kamerasına dönüştürür. Maçları gerçek zamanlı skor grafikleriyle YouTube Live'a yayınlar.",
    "500+ videos streamed by a local league": "Yerel bir lig 500'den fazla video yayınladı",
    "Goals, cards and substitutions logged mid-stream": "Gol, kart ve değişiklikler yayın sırasında girilir",
    "Syncs instantly with Prolig": "Prolig ile anında eşitlenir",
    "About OFS": "OFS hakkında",
    "OFS Dış Ticaret Ltd. Şti. is an Istanbul-based company founded in 2022. Today our focus is building software products.":
        "OFS Dış Ticaret Ltd. Şti., 2022'de kurulmuş İstanbul merkezli bir şirkettir. Bugün odağımız yazılım ürünleri geliştirmektir.",
    "We are a small, founder-led company. That keeps us close to our users and lets us ship improvements quickly.":
        "Kurucusu tarafından yönetilen küçük bir şirketiz. Bu sayede kullanıcılarımıza yakın duruyor ve iyileştirmeleri hızla yayına alabiliyoruz.",
    "Legal name": "Ticaret unvanı",
    "Founded": "Kuruluş",
    "October 2022": "Ekim 2022",
    "Founder": "Kurucu",
    "Email": "E-posta",
    "Questions about OFS or one of our products? We would be glad to hear from you.":
        "OFS ya da ürünlerimizle ilgili bir sorunuz mu var? Sizden haber almaktan memnuniyet duyarız.",
    "A phone on a tripod streaming an amateur football match with Baykul Broadcaster":
        "Tripod üzerindeki bir telefon, Baykul Broadcaster ile amatör bir futbol maçını yayınlıyor",
    "Prolig live scoring screen": "Prolig canlı skor ekranı",
    "Prolig standings screen": "Prolig puan tablosu ekranı",
    "Baykul Broadcaster streaming a match from a phone on a tripod":
        "Baykul Broadcaster, tripod üzerindeki bir telefondan maç yayınlıyor",

    # --- Prolig ---
    "Prolig — League management for amateur football | OFS": "Prolig — Amatör futbol için lig yönetimi | OFS",
    "Prolig is a league management app for amateur 7-a-side football: live scoring, standings, player statistics, reports and social graphics. A product by OFS.":
        "Prolig, 7 kişilik amatör futbol ligleri için lig yönetim uygulamasıdır: canlı skor, puan tablosu, oyuncu istatistikleri, raporlar ve sosyal medya görselleri. Bir OFS ürünüdür.",
    "In use by a league in Kocaeli · Closed beta": "Kocaeli'de bir ligde kullanılıyor · Kapalı beta",
    "League management for amateur football.": "Amatör futbol için lig yönetimi.",
    "Prolig runs a league from the first fixture to the season report: lineups, live scoring, standings, player stats, PDF reports and ready-to-post social graphics.":
        "Prolig bir ligi ilk fikstürden sezon raporuna kadar yönetir: kadrolar, canlı skor, puan tablosu, oyuncu istatistikleri, PDF raporlar ve paylaşıma hazır sosyal medya görselleri.",
    "See the features": "Özellikleri görün",
    "View screens": "Ekranları görün",
    "4 months": "4 ay",
    "In use by a local league": "Yerel bir ligde kullanımda",
    "Instagram posts from app data": "Uygulama verisiyle Instagram gönderisi",
    "7-a-side": "7'ye 7",
    "Built for amateur leagues": "Amatör ligler için tasarlandı",
    "Flutter app": "Flutter uygulaması",
    "Everything a league organiser needs": "Bir lig organizatörünün ihtiyacı olan her şey",
    "Enter a match event once and the whole league stays up to date.":
        "Maç olayını bir kez girin; bütün lig güncel kalsın.",
    "Match day": "Maç günü",
    "Teams, squads and 7-a-side lineups with formation view":
        "Takımlar, kadrolar ve diziliş görünümüyle 7 kişilik ilk yediler",
    "Live scoring from an operator screen: goals, cards, substitutions":
        "Operatör ekranından canlı skor: gol, kart, oyuncu değişikliği",
    "Match clock, half-time and full-time control": "Maç saati, devre arası ve maç sonu kontrolü",
    "Forfeit and VAR decisions": "Hükmen mağlubiyet ve VAR kararları",
    "League and content": "Lig ve içerik",
    "Automatic standings, top scorers and player stats":
        "Otomatik puan tablosu, gol krallığı ve oyuncu istatistikleri",
    "PDF match reports and full season reports": "PDF maç raporları ve tam sezon raporları",
    "Ready-to-post social graphics: results, fixtures, tables":
        "Paylaşıma hazır sosyal medya görselleri: sonuçlar, fikstür, puan tablosu",
    "Monthly bonus-point system for teams": "Takımlar için aylık bonus puan sistemi",
    "Our streaming app sends matches to YouTube Live. Events logged on its camera screen are written straight into Prolig, so the stream and the league table always agree.":
        "Yayın uygulamamız maçları YouTube Live'a gönderir. Kamera ekranından girilen olaylar doğrudan Prolig'e yazılır; böylece yayın ile puan tablosu her zaman uyumludur.",
    "View Baykul Broadcaster": "Baykul Broadcaster'ı incele",
    "Inside the app": "Uygulamanın içinden",
    "Real screens from real matches": "Gerçek maçlardan gerçek ekranlar",
    "Unedited screenshots from the Kocaeli league. Player names are blurred for privacy.":
        "Kocaeli ligine ait, üzerinde oynanmamış ekran görüntüleri. Oyuncu adları gizlilik için bulanıklaştırılmıştır.",
    "Live scoring": "Canlı skor",
    "Score, clock and one-tap goals, cards and substitutions.":
        "Skor, süre ve tek dokunuşla gol, kart ve oyuncu değişikliği.",
    "Standings": "Puan tablosu",
    "The table updates the moment a result is logged.": "Sonuç girildiği anda tablo güncellenir.",
    "Social graphics": "Sosyal medya görselleri",
    "Daily results, fixtures and tables, generated ready to post.":
        "Günün sonuçları, fikstür ve puan tablosu paylaşıma hazır üretilir.",
    "Built with Claude. Next: powered by it.": "Claude ile geliştirildi. Sırada: Claude ile çalışması.",
    "Prolig was built with Anthropic's Claude. The next step is bringing Claude into the product itself.":
        "Prolig, Anthropic'in Claude'u ile geliştirildi. Sıradaki adım, Claude'u ürünün içine yerleştirmek.",
    "League app shipped to closed beta": "Lig uygulaması kapalı betaya çıktı",
    "Scoring, standings, stats, reports and social graphics.":
        "Skor, puan tablosu, istatistikler, raporlar ve sosyal medya görselleri.",
    "Closed beta with a league in Kocaeli": "Kocaeli'de bir ligle kapalı beta",
    "A local league runs its matches on Prolig and feeds back what to improve.":
        "Yerel bir lig maçlarını Prolig üzerinden yürütüyor ve nelerin iyileştirilmesi gerektiğini bildiriyor.",
    "AI match summaries and commentary": "Yapay zekâ ile maç özetleri ve yorumlar",
    "Automatic, Turkish-first match reports written from the live event data.":
        "Canlı maç verisinden otomatik yazılan, öncelikle Türkçe maç raporları.",
    "Performance insights and social posts": "Performans analizleri ve sosyal medya gönderileri",
    "Player and team insights, plus a ready-to-publish post for every match.":
        "Oyuncu ve takım analizleri, ayrıca her maç için yayına hazır bir gönderi.",
    "Running a league?": "Bir lig mi yönetiyorsunuz?",
    "Prolig is in closed beta. If you organise a league or tournament and want to try it, write to us.":
        "Prolig kapalı beta aşamasında. Bir lig ya da turnuva düzenliyor ve denemek istiyorsanız bize yazın.",
    "Prolig is a product by OFS Dış Ticaret Ltd. Şti.": "Prolig, bir OFS Dış Ticaret Ltd. Şti. ürünüdür.",
    "League standings table in the Prolig app": "Prolig uygulamasında lig puan tablosu",
    "Live scoring screen": "Canlı skor ekranı",
    "League standings table": "Lig puan tablosu",
    "Auto-generated match results graphic": "Otomatik üretilen maç sonuçları görseli",

    # --- Baykul Broadcaster ---
    "Baykul Broadcaster — Live streaming for amateur football | OFS":
        "Baykul Broadcaster — Amatör futbol için canlı yayın | OFS",
    "Baykul Broadcaster turns a phone into a broadcast camera: YouTube Live streaming with real-time score overlays and in-stream match logging. A product by OFS.":
        "Baykul Broadcaster telefonu yayın kamerasına dönüştürür: gerçek zamanlı skor grafikleriyle YouTube Live yayını ve yayın sırasında maç verisi girişi. Bir OFS ürünüdür.",
    "Live in Kocaeli · Closed beta": "Kocaeli'de yayında · Kapalı beta",
    "Turn a phone into a broadcast camera.": "Telefonunuzu yayın kamerasına dönüştürün.",
    "Baykul Broadcaster streams matches straight to YouTube Live with real-time score and lineup overlays. Goals, cards and substitutions are logged on the camera screen without stopping the broadcast.":
        "Baykul Broadcaster maçları gerçek zamanlı skor ve kadro grafikleriyle doğrudan YouTube Live'a yayınlar. Gol, kart ve oyuncu değişiklikleri yayın durmadan kamera ekranından girilir.",
    "Watch a real match": "Gerçek bir maç izleyin",
    "Streaming a league match in Kocaeli": "Kocaeli'de bir lig maçı yayınlanıyor",
    "Videos streamed": "Yayınlanan video",
    "Live with a local league": "Yerel bir ligle yayında",
    "YouTube subscribers": "YouTube abonesi",
    "Native app": "Yerel (native) uygulama",
    "A camera and a scoring console in one": "Kamera ve skor konsolu tek uygulamada",
    "One person with one phone can film the match and keep the score at the same time.":
        "Tek kişi, tek telefonla hem maçı çekebilir hem de skoru tutabilir.",
    "Broadcast": "Yayın",
    "Direct YouTube Live broadcast setup from the app": "Uygulamadan doğrudan YouTube Live yayını kurulumu",
    "Real-time score and lineup overlays on the stream": "Yayında gerçek zamanlı skor ve kadro grafikleri",
    "Stream health monitoring with automatic retry": "Yayın sağlığı takibi ve otomatik yeniden deneme",
    "Runs on a standard Android phone and a tripod": "Standart bir Android telefon ve tripodla çalışır",
    "Match logging": "Maç verisi girişi",
    "Log goals, cards and substitutions mid-stream": "Yayın sırasında gol, kart ve değişiklik girin",
    ", without leaving the camera view": "; kamera görüntüsünden çıkmadan",
    "Every event syncs instantly": "Her olay anında eşitlenir",
    "to Prolig: score, standings, player stats": "— Prolig'e: skor, puan tablosu, oyuncu istatistikleri",
    "Start the match, half-time and second half from the same panel":
        "Maçı, devre arasını ve ikinci yarıyı aynı panelden başlatın",
    "Overlays driven by the same data as the league app":
        "Grafikler lig uygulamasıyla aynı veriden beslenir",
    "Real match, real stream": "Gerçek maç, gerçek yayın",
    "Already on air": "Zaten yayında",
    "A local league in Kocaeli streams its matches with Baykul Broadcaster and publishes them on the league's YouTube channel.":
        "Kocaeli'de yerel bir lig, maçlarını Baykul Broadcaster ile yayınlıyor ve ligin YouTube kanalında paylaşıyor.",
    "YouTube channel ↗": "YouTube kanalı ↗",
    "Instagram ↗": "Instagram ↗",
    "Prolig Kocaeli · Full match on YouTube": "Prolig Kocaeli · Maçın tamamı YouTube'da",
    "Our league management app. Everything logged during the broadcast lands in Prolig: standings, top scorers, match reports and social graphics update on their own.":
        "Lig yönetim uygulamamız. Yayın sırasında girilen her şey Prolig'e düşer: puan tablosu, gol krallığı, maç raporları ve sosyal medya görselleri kendiliğinden güncellenir.",
    "View Prolig": "Prolig'i incele",
    "On the touchline": "Saha kenarında",
    "No production crew needed": "Yayın ekibine gerek yok",
    "A phone on a tripod is the whole setup. The app shows the live picture with the score overlay, and the match panel sits on the same screen.":
        "Bütün kurulum, tripod üzerindeki bir telefondan ibaret. Uygulama canlı görüntüyü skor grafiğiyle gösterir; maç paneli de aynı ekrandadır.",
    "This photo was taken during a league match in Kocaeli.": "Bu fotoğraf Kocaeli'de bir lig maçı sırasında çekildi.",
    "Want to stream your league?": "Liginizi yayınlamak ister misiniz?",
    "Baykul Broadcaster is in closed beta. If you organise a league or tournament and want to try it, write to us.":
        "Baykul Broadcaster kapalı beta aşamasında. Bir lig ya da turnuva düzenliyor ve denemek istiyorsanız bize yazın.",
    "Baykul Broadcaster is a product by OFS Dış Ticaret Ltd. Şti.":
        "Baykul Broadcaster, bir OFS Dış Ticaret Ltd. Şti. ürünüdür.",
    "A phone on a tripod streaming a 7-a-side match with Baykul Broadcaster":
        "Tripod üzerindeki bir telefon, Baykul Broadcaster ile 7 kişilik bir maçı yayınlıyor",
    "Play Bonzalex – Red Bull FC, streamed with Baykul Broadcaster":
        "Baykul Broadcaster ile yayınlanan Bonzalex – Red Bull FC maçını oynat",
    "Baykul Broadcaster running on a phone on a tripod beside the pitch":
        "Saha kenarında tripod üzerindeki telefonda çalışan Baykul Broadcaster",
}

missing = set()


def tr(text):
    key = html.unescape(text).strip()
    key = re.sub(r"\s+", " ", key)
    if not key or not re.search(r"[A-Za-z]", key) or key in KEEP:
        return None
    if key.startswith("http") or key in ("website", "width=device-width, initial-scale=1.0") or key in TR.values():
        return None
    if key in TR:
        return TR[key]
    missing.add(key)
    return None


def translate(page):
    s = open(os.path.join(ROOT, page), encoding="utf-8").read()

    # <script> ve <svg> bloklarını koru
    stash = []

    def keep(m):
        stash.append(m.group(0))
        return f"\x00{len(stash) - 1}\x00"

    s = re.sub(r"(?s)<script.*?</script>|<svg.*?</svg>", keep, s)

    # Metin düğümleri
    def node(m):
        raw = m.group(1)
        t = tr(raw)
        if t is None:
            return m.group(0)
        lead = raw[: len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):]
        return lead + html.escape(t, quote=False) + trail

    # Metin, bir etiketle ya da korunan bir blokla (ikon) sınırlanmış olabilir
    s = re.sub(r"(?<=[>\x00])([^<>\x00]+)(?=[<\x00])", node, s)

    # Öznitelikler
    def attr(m):
        t = tr(m.group(2))
        return m.group(0) if t is None else f'{m.group(1)}"{html.escape(t)}"'

    s = re.sub(r'((?:alt|aria-label|content)=)"([^"]*)"', attr, s)
    s = re.sub(r"<title>([^<]+)</title>", lambda m: f"<title>{html.escape(tr(m.group(1)) or m.group(1), quote=False)}</title>", s)

    s = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], s)

    # Dil, yollar ve bağlantılar
    s = s.replace('<html lang="en"', '<html lang="tr"')
    s = s.replace('href="assets/', 'href="../assets/').replace('src="images/', 'src="../images/').replace('href="images/', 'href="../images/')
    s = s.replace('href="/"', 'href="/tr/"').replace('href="/#products"', 'href="/tr/#products"')
    name = "" if page == "index.html" else page
    s = s.replace(f'<meta property="og:url" content="https://ofsenterprise.com/{name}">',
                  f'<meta property="og:url" content="https://ofsenterprise.com/tr/{name}">')

    # Dil değiştirici: TR aktif, EN bağlantı
    s = re.sub(
        r'<div class="flex items-center mr-3 text-sm font-semibold" data-lang-switch>.*?</div>',
        f'<div class="flex items-center mr-3 text-sm font-semibold" data-lang-switch><a href="../{name}" hreflang="en" lang="en" class="text-gray-400 hover:text-emerald-700" title="English">EN</a><span class="mx-1.5 text-gray-300">|</span><span class="text-gray-900">TR</span></div>',
        s, flags=re.S)

    os.makedirs(os.path.join(ROOT, "tr"), exist_ok=True)
    open(os.path.join(ROOT, "tr", page), "w", encoding="utf-8").write(s)


for p in PAGES:
    translate(p)

if missing:
    print("ÇEVRİLMEMİŞ METİNLER:")
    for m in sorted(missing):
        print("  ·", m)
else:
    print("Tamam: tr/ klasörü üretildi, çevrilmemiş metin yok.")
