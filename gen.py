#!/usr/bin/env python3
"""Gold & FX multilingual static site generator (ar, en, fr, tr, id, es).
Usage:  SITE_URL=https://yourdomain.com ADSENSE_CLIENT=ca-pub-XXXX AD_SLOT=123 CONTACT_EMAIL=you@mail.com python gen.py
Output: docs/  (publish with GitHub Pages: branch main, folder /docs)
"""
import os, json, html, datetime, shutil

SITE_URL = os.environ.get("SITE_URL", "https://example.com").rstrip("/")
BASE = os.environ.get("BASE_PATH", "").rstrip("/")          # e.g. /repo if no custom domain
ADSENSE = os.environ.get("ADSENSE_CLIENT", "")               # ca-pub-XXXXXXXXXXXXXXXX
AD_SLOT = os.environ.get("AD_SLOT", "")                      # in-page unit slot id (optional)
EMAIL = os.environ.get("CONTACT_EMAIL", "contact@example.com")
DOMAIN = os.environ.get("DOMAIN", "")                        # writes CNAME if set
OUT = os.environ.get("OUT_DIR", "docs")

LANGS = ["ar", "en", "fr", "tr", "id", "es"]
NATIVE = ["العربية", "English", "Français", "Türkçe", "Indonesia", "Español"]
LOC = {"ar": "ar-u-nu-latn", "en": "en", "fr": "fr", "tr": "tr", "id": "id", "es": "es"}
SEP = "¦"

RAW = {
"name": "ذهب وعملات¦Gold & FX¦Or & Devises¦Altın & Döviz¦Emas & Kurs¦Oro y Divisas",
"home_h1": "أسعار الذهب والعملات اليوم¦Gold Prices & Currency Rates Today¦Prix de l'or et taux de change aujourd'hui¦Bugün Altın Fiyatları ve Döviz Kurları¦Harga Emas & Kurs Hari Ini¦Precio del oro y tipos de cambio hoy",
"home_p": "اختر دولتك أو زوج العملات لمعرفة السعر المباشر مع رسم بياني وحاسبة مجانية.¦Pick your country or currency pair for live prices, a chart and free calculators.¦Choisissez votre pays ou une paire de devises pour les prix en direct, un graphique et des calculateurs gratuits.¦Ülkenizi veya döviz çiftinizi seçin: canlı fiyat, grafik ve ücretsiz hesaplayıcılar.¦Pilih negara atau pasangan mata uang untuk harga langsung, grafik, dan kalkulator gratis.¦Elige tu país o par de divisas: precios en vivo, gráfico y calculadoras gratis.",
"home_desc": "أسعار الذهب لكل دولة وتحويل العملات مباشرة مع حاسبة الزكاة ورسوم بيانية.¦Live gold prices by country, currency converter, zakat calculator and charts.¦Prix de l'or par pays, convertisseur de devises, calculateur de zakat et graphiques en direct.¦Ülkelere göre canlı altın fiyatları, döviz çevirici, zekat hesaplayıcı ve grafikler.¦Harga emas langsung per negara, konverter mata uang, kalkulator zakat, dan grafik.¦Precios del oro por país, conversor de divisas, calculadora de zakat y gráficos en vivo.",
"gold_nav": "الذهب¦Gold¦Or¦Altın¦Emas¦Oro",
"fx_nav": "العملات¦Currencies¦Devises¦Döviz¦Kurs¦Divisas",
"zakat_nav": "حاسبة الزكاة¦Zakat Calculator¦Calculateur de zakat¦Zekat Hesaplayıcı¦Kalkulator Zakat¦Calculadora de zakat",
"gold_title": "سعر الذهب اليوم في {c} — عيار 24 و21 و18¦Gold Price Today in {c} — 24K, 22K, 21K, 18K¦Prix de l'or aujourd'hui en {c} — 24, 22, 21, 18 carats¦{c} Altın Fiyatları Bugün — 24, 22, 21, 18 Ayar¦Harga Emas Hari Ini di {c} — 24K, 22K, 21K, 18K¦Precio del oro hoy en {c} — 24K, 22K, 21K, 18K",
"gold_h1": "سعر الذهب اليوم في {c}¦Gold Price Today in {c}¦Prix de l'or aujourd'hui en {c}¦{c} Altın Fiyatı Bugün¦Harga Emas Hari Ini di {c}¦Precio del oro hoy en {c}",
"gold_desc": "سعر جرام الذهب في {c} بـ{cur} لكل العيارات، مباشر مع رسم بياني لآخر 30 يوماً وحاسبة المصنعية والضريبة.¦Live gold price per gram in {c} in {cur} for every karat, with a 30-day chart and a making-charge & tax calculator.¦Prix du gramme d'or en {c} en {cur} pour chaque carat, en direct, avec graphique sur 30 jours et calculateur frais de façon et TVA.¦{c} için {cur} cinsinden tüm ayarlarda canlı gram altın fiyatı, 30 günlük grafik ve işçilik-KDV hesaplayıcı.¦Harga emas per gram di {c} dalam {cur} untuk semua karat, langsung dengan grafik 30 hari dan kalkulator ongkos & pajak.¦Precio del gramo de oro en {c} en {cur} para cada quilate, en vivo, con gráfico de 30 días y calculadora de mano de obra e impuestos.",
"karat": "عيار {k}¦{k}K¦{k} carats¦{k} ayar¦{k} karat¦{k} quilates",
"per_gram": "سعر الجرام¦Price per gram¦Prix au gramme¦Gram fiyatı¦Harga per gram¦Precio por gramo",
"karat_h": "العيار¦Karat¦Carat¦Ayar¦Karat¦Quilate",
"ounce": "الأونصة عالمياً¦Global ounce¦Once (monde)¦Küresel ons¦Ons global¦Onza global",
"upd": "آخر تحديث¦Last update¦Dernière mise à jour¦Son güncelleme¦Pembaruan terakhir¦Última actualización",
"err": "تعذر التحديث، أعد تحميل الصفحة¦Update failed, reload the page¦Échec de la mise à jour, rechargez la page¦Güncellenemedi, sayfayı yenileyin¦Gagal memperbarui, muat ulang halaman¦No se pudo actualizar, recarga la página",
"calc_h": "حاسبة شراء الذهب¦Gold purchase calculator¦Calculateur d'achat d'or¦Altın alım hesaplayıcı¦Kalkulator beli emas¦Calculadora de compra de oro",
"weight": "الوزن (جرام)¦Weight (grams)¦Poids (grammes)¦Ağırlık (gram)¦Berat (gram)¦Peso (gramos)",
"making": "المصنعية %¦Making charge %¦Frais de façon %¦İşçilik %¦Ongkos pembuatan %¦Mano de obra %",
"tax": "الضريبة %¦Tax / VAT %¦TVA %¦KDV %¦Pajak %¦Impuesto %",
"total": "الإجمالي¦Total¦Total¦Toplam¦Total¦Total",
"weights_h": "سعر أوزان شائعة (جرام)¦Common weights (grams)¦Poids courants (grammes)¦Sık kullanılan ağırlıklar (gram)¦Berat umum (gram)¦Pesos habituales (gramos)",
"chart_h": "آخر 30 يوماً¦Last 30 days¦30 derniers jours¦Son 30 gün¦30 hari terakhir¦Últimos 30 días",
"chart_wait": "الرسم البياني يتجمع يومياً وسيظهر بعد عدة أيام.¦The chart builds up daily and will appear after a few days.¦Le graphique se construit chaque jour et apparaîtra dans quelques jours.¦Grafik her gün oluşur, birkaç gün sonra görünecek.¦Grafik terkumpul setiap hari dan muncul beberapa hari lagi.¦El gráfico se completa cada día y aparecerá en unos días.",
"chg": "التغير¦Change¦Variation¦Değişim¦Perubahan¦Cambio",
"faq_h": "أسئلة شائعة¦FAQ¦Questions fréquentes¦Sık sorulan sorular¦Pertanyaan umum¦Preguntas frecuentes",
"q1": "لماذا يختلف السعر عن محل الصاغة؟¦Why does the price differ from the jeweler's?¦Pourquoi le prix diffère-t-il de celui du bijoutier ?¦Fiyat kuyumcudan neden farklı?¦Mengapa harga berbeda dengan toko emas?¦¿Por qué el precio difiere del de la joyería?",
"a1": "المحلات تضيف المصنعية والضريبة وهامش الربح، أما السعر هنا فهو الذهب الخام المحسوب من السعر العالمي.¦Jewelers add making charges, tax and margin; the price here is raw gold computed from the global spot price.¦Les bijoutiers ajoutent frais de façon, taxes et marge ; ici c'est l'or brut calculé d'après le cours mondial.¦Kuyumcular işçilik, vergi ve kâr marjı ekler; buradaki fiyat küresel ons fiyatından hesaplanan ham altındır.¦Toko emas menambahkan ongkos, pajak, dan margin; harga di sini adalah emas murni dari harga spot dunia.¦Las joyerías añaden mano de obra, impuestos y margen; aquí es oro en bruto calculado con el precio mundial.",
"q2": "ما الفرق بين العيارات؟¦What is the difference between karats?¦Quelle différence entre les carats ?¦Ayarlar arasındaki fark nedir?¦Apa beda antar karat?¦¿Qué diferencia hay entre quilates?",
"a2": "العيار هو نقاء الذهب من 24 جزءاً: عيار 24 شبه خالص، وعيار 21 يحتوي 87.5% ذهباً، وعيار 18 يحتوي 75%.¦Karat measures purity out of 24: 24K is nearly pure, 21K is 87.5% gold, 18K is 75%.¦Le carat mesure la pureté sur 24 : 24 carats est presque pur, 21 carats = 87,5 % d'or, 18 carats = 75 %.¦Ayar saflığı 24 üzerinden gösterir: 24 ayar neredeyse saf, 21 ayar %87,5, 18 ayar %75 altındır.¦Karat menunjukkan kemurnian dari 24: 24K hampir murni, 21K berisi 87,5% emas, 18K 75%.¦El quilate mide la pureza sobre 24: 24K es casi puro, 21K tiene 87,5 % de oro y 18K, 75 %.",
"q3": "كم مرة يتحدث السعر؟¦How often does the price update?¦À quelle fréquence le prix est-il mis à jour ?¦Fiyat ne sıklıkla güncellenir?¦Seberapa sering harga diperbarui?¦¿Con qué frecuencia se actualiza el precio?",
"a3": "يتحدث تلقائياً كل بضع دقائق عند فتح الصفحة.¦It refreshes automatically every few minutes while the page is open.¦Il se rafraîchit automatiquement toutes les quelques minutes.¦Sayfa açıkken birkaç dakikada bir otomatik yenilenir.¦Diperbarui otomatis setiap beberapa menit saat halaman terbuka.¦Se actualiza automáticamente cada pocos minutos con la página abierta.",
"others": "الذهب في دول أخرى¦Gold in other countries¦L'or dans d'autres pays¦Diğer ülkelerde altın¦Emas di negara lain¦Oro en otros países",
"fx_title": "تحويل {a} إلى {b} — سعر الصرف اليوم¦{a} to {b} — Exchange Rate Today¦{a} en {b} — taux de change aujourd'hui¦{a} / {b} Kuru Bugün¦{a} ke {b} — Kurs Hari Ini¦{a} a {b} — tipo de cambio hoy",
"fx_h1": "تحويل {a} إلى {b}¦{a} to {b} converter¦Convertir {a} en {b}¦{a} - {b} çevirici¦Konversi {a} ke {b}¦Convertir {a} a {b}",
"fx_desc": "سعر صرف {a} مقابل {b} مباشر، مع محوّل مجاني ورسم بياني وجدول مبالغ شائعة.¦Live {a} to {b} exchange rate with a free converter, chart and common amounts table.¦Taux {a} vers {b} en direct, avec convertisseur gratuit, graphique et tableau de montants courants.¦Canlı {a} / {b} kuru; ücretsiz çevirici, grafik ve sık kullanılan tutarlar tablosu.¦Kurs {a} ke {b} langsung dengan konverter gratis, grafik, dan tabel jumlah umum.¦Tipo de cambio {a} a {b} en vivo, con conversor gratis, gráfico y tabla de importes habituales.",
"amount": "المبلغ¦Amount¦Montant¦Tutar¦Jumlah¦Importe",
"swap": "عكس الاتجاه¦Swap direction¦Inverser¦Ters çevir¦Tukar arah¦Invertir",
"common": "مبالغ شائعة¦Common amounts¦Montants courants¦Sık kullanılan tutarlar¦Jumlah umum¦Importes habituales",
"pairs_h": "أزواج العملات الشائعة¦Popular currency pairs¦Paires de devises populaires¦Popüler döviz çiftleri¦Pasangan mata uang populer¦Pares de divisas populares",
"zakat_h1": "حاسبة الزكاة على الذهب والفضة والنقد¦Zakat Calculator for Gold, Silver & Cash¦Calculateur de zakat : or, argent et argent liquide¦Altın, Gümüş ve Nakit Zekat Hesaplayıcı¦Kalkulator Zakat Emas, Perak & Uang Tunai¦Calculadora de zakat: oro, plata y efectivo",
"zakat_desc": "احسب زكاتك بسعر اليوم: النصاب 595 جرام فضة (أو 85 جرام ذهب) والمقدار 2.5%.¦Calculate your zakat at today's prices: nisab 595 g of silver (or 85 g of gold), rate 2.5%.¦Calculez votre zakat aux prix du jour : nisab 595 g d'argent (ou 85 g d'or), taux 2,5 %.¦Zekatınızı güncel fiyatlarla hesaplayın: nisap 595 gr gümüş (veya 85 gr altın), oran %2,5.¦Hitung zakat dengan harga hari ini: nisab 595 g perak (atau 85 g emas), tarif 2,5%.¦Calcula tu zakat a precios de hoy: nisab 595 g de plata (u 85 g de oro), tasa 2,5 %.",
"z_gold": "ذهب (جرام، ما يعادل عيار 24)¦Gold (grams, 24K equivalent)¦Or (grammes, équivalent 24 carats)¦Altın (gram, 24 ayar karşılığı)¦Emas (gram, setara 24K)¦Oro (gramos, equivalente 24K)",
"z_silver": "فضة (جرام)¦Silver (grams)¦Argent (grammes)¦Gümüş (gram)¦Perak (gram)¦Plata (gramos)",
"z_cash": "نقد وأرصدة¦Cash & savings¦Argent liquide et épargne¦Nakit ve birikim¦Uang tunai & tabungan¦Efectivo y ahorros",
"z_debt": "ديون مستحقة عليك¦Debts you owe¦Dettes à payer¦Borçlar¦Utang¦Deudas",
"z_cur": "العملة¦Currency¦Devise¦Para birimi¦Mata uang¦Divisa",
"z_nisab": "قيمة النصاب (بالفضة)¦Nisab value (silver basis)¦Valeur du nisab (base argent)¦Nisap değeri (gümüş esaslı)¦Nilai nisab (basis perak)¦Valor del nisab (base plata)",
"z_wealth": "صافي مالك¦Your net wealth¦Votre patrimoine net¦Net varlığınız¦Total kekayaan bersih¦Tu patrimonio neto",
"z_due": "الزكاة الواجبة¦Zakat due¦Zakat due¦Ödenecek zekat¦Zakat wajib¦Zakat a pagar",
"z_notdue": "لم تبلغ النصاب، لا زكاة عليك¦Below nisab, no zakat due¦Sous le nisab, pas de zakat¦Nisabın altında, zekat yok¦Di bawah nisab, tidak wajib zakat¦Bajo el nisab, sin zakat",
"z_note": "للإرشاد فقط؛ استشر عالماً موثوقاً في حالتك الخاصة.¦For guidance only; consult a trusted scholar for your own case.¦À titre indicatif ; consultez un savant de confiance pour votre cas.¦Yalnızca bilgi amaçlıdır; kendi durumunuz için güvenilir bir âlime danışın.¦Hanya panduan; konsultasikan ke ulama tepercaya untuk kasus Anda.¦Solo orientativo; consulta a un erudito de confianza para tu caso.",
"disc": "الأسعار استرشادية مبنية على السعر العالمي وسعر الصرف وقد تختلف عن السوق المحلي.¦Prices are indicative, based on global spot and FX rates, and may differ from local markets.¦Prix indicatifs basés sur le cours mondial et les taux de change ; ils peuvent différer du marché local.¦Fiyatlar yol göstericidir; küresel fiyat ve kura dayanır, yerel piyasadan farklı olabilir.¦Harga bersifat indikatif berdasarkan harga dunia & kurs, bisa berbeda dengan pasar lokal.¦Precios orientativos basados en el precio mundial y los tipos de cambio; pueden diferir del mercado local.",
"share": "مشاركة¦Share¦Partager¦Paylaş¦Bagikan¦Compartir",
"about": "من نحن¦About¦À propos¦Hakkımızda¦Tentang¦Acerca de",
"privacy": "الخصوصية¦Privacy¦Confidentialité¦Gizlilik¦Privasi¦Privacidad",
"contact": "اتصل بنا¦Contact¦Contact¦İletişim¦Kontak¦Contacto",
"about_p": "موقع مجاني يعرض أسعار الذهب والعملات من مصادر بيانات عامة، هدفه معلومة واضحة وسريعة وأدوات حساب بسيطة.¦A free site showing gold prices and currency rates from public data sources, aiming for clear, fast information and simple calculators.¦Un site gratuit qui affiche les prix de l'or et les taux de change à partir de sources publiques, avec une information claire et rapide.¦Genel veri kaynaklarından altın fiyatlarını ve döviz kurlarını gösteren ücretsiz bir site; amaç net ve hızlı bilgi ile basit hesaplayıcılardır.¦Situs gratis yang menampilkan harga emas dan kurs dari sumber data publik, dengan informasi jelas, cepat, dan kalkulator sederhana.¦Sitio gratuito que muestra precios del oro y tipos de cambio desde fuentes públicas, con información clara y rápida.",
"privacy_p": "قد نستخدم ملفات تعريف الارتباط وخدمات إعلانية مثل Google AdSense. تستخدم Google وشركاؤها ملفات الكوكيز لعرض إعلانات بناءً على زياراتك لهذا الموقع ولمواقع أخرى، ويمكنك إيقاف الإعلانات المخصصة من إعدادات الإعلانات في Google. لا نجمع بيانات شخصية؛ يُحفظ في متصفحك بيانات تقنية بسيطة فقط لتسريع التحميل.¦We may use cookies and advertising services such as Google AdSense. Google and its partners use cookies to serve ads based on your visits to this and other sites; you can opt out of personalized ads in Google Ads Settings. We do not collect personal data; only simple technical data is stored in your browser to speed up loading.¦Nous pouvons utiliser des cookies et des services publicitaires tels que Google AdSense. Google et ses partenaires utilisent des cookies pour diffuser des annonces selon vos visites sur ce site et d'autres ; vous pouvez désactiver les annonces personnalisées dans les paramètres Google Ads. Nous ne collectons pas de données personnelles ; seules des données techniques simples sont stockées dans votre navigateur.¦Çerezler ve Google AdSense gibi reklam hizmetleri kullanabiliriz. Google ve ortakları, bu ve diğer sitelere yaptığınız ziyaretlere göre reklam göstermek için çerez kullanır; kişiselleştirilmiş reklamları Google Reklam Ayarları'ndan kapatabilirsiniz. Kişisel veri toplamayız; tarayıcınızda yalnızca yüklemeyi hızlandıran basit teknik veriler saklanır.¦Kami dapat menggunakan cookie dan layanan iklan seperti Google AdSense. Google dan mitranya memakai cookie untuk menampilkan iklan berdasarkan kunjungan Anda ke situs ini dan situs lain; Anda dapat menonaktifkan iklan personalisasi di Pengaturan Iklan Google. Kami tidak mengumpulkan data pribadi; hanya data teknis sederhana disimpan di browser untuk mempercepat pemuatan.¦Podemos usar cookies y servicios publicitarios como Google AdSense. Google y sus socios usan cookies para mostrar anuncios según tus visitas a este y otros sitios; puedes desactivar los anuncios personalizados en la configuración de anuncios de Google. No recopilamos datos personales; solo se guardan en tu navegador datos técnicos simples para acelerar la carga.",
"contact_p": "للتواصل: {email}¦Contact us: {email}¦Contactez-nous : {email}¦İletişim: {email}¦Hubungi kami: {email}¦Contáctanos: {email}",
}
TR = {}
for k, v in RAW.items():
    parts = v.split(SEP)
    assert len(parts) == 6, (k, len(parts))
    TR[k] = parts

def t(key, lang, **kw):
    s = TR[key][LANGS.index(lang)]
    for a, b in kw.items():
        s = s.replace("{" + a + "}", str(b))
    return s

# slug, currency, hero karat, names(ar|en|fr|tr|id|es)
COUNTRIES = [
("saudi-arabia", "SAR", 21, "السعودية|Saudi Arabia|Arabie saoudite|Suudi Arabistan|Arab Saudi|Arabia Saudita"),
("uae", "AED", 21, "الإمارات|United Arab Emirates|Émirats arabes unis|Birleşik Arap Emirlikleri|Uni Emirat Arab|Emiratos Árabes Unidos"),
("egypt", "EGP", 21, "مصر|Egypt|Égypte|Mısır|Mesir|Egipto"),
("kuwait", "KWD", 21, "الكويت|Kuwait|Koweït|Kuveyt|Kuwait|Kuwait"),
("qatar", "QAR", 21, "قطر|Qatar|Qatar|Katar|Qatar|Catar"),
("bahrain", "BHD", 21, "البحرين|Bahrain|Bahreïn|Bahreyn|Bahrain|Baréin"),
("oman", "OMR", 21, "عُمان|Oman|Oman|Umman|Oman|Omán"),
("jordan", "JOD", 21, "الأردن|Jordan|Jordanie|Ürdün|Yordania|Jordania"),
("iraq", "IQD", 21, "العراق|Iraq|Irak|Irak|Irak|Irak"),
("morocco", "MAD", 18, "المغرب|Morocco|Maroc|Fas|Maroko|Marruecos"),
("algeria", "DZD", 18, "الجزائر|Algeria|Algérie|Cezayir|Aljazair|Argelia"),
("tunisia", "TND", 18, "تونس|Tunisia|Tunisie|Tunus|Tunisia|Túnez"),
("palestine", "ILS", 21, "فلسطين|Palestine|Palestine|Filistin|Palestina|Palestina"),
("turkey", "TRY", 22, "تركيا|Türkiye|Turquie|Türkiye|Turki|Turquía"),
("indonesia", "IDR", 24, "إندونيسيا|Indonesia|Indonésie|Endonezya|Indonesia|Indonesia"),
("france", "EUR", 18, "فرنسا|France|France|Fransa|Prancis|Francia"),
("spain", "EUR", 18, "إسبانيا|Spain|Espagne|İspanya|Spanyol|España"),
("usa", "USD", 24, "الولايات المتحدة|United States|États-Unis|Amerika Birleşik Devletleri|Amerika Serikat|Estados Unidos"),
("uk", "GBP", 22, "المملكة المتحدة|United Kingdom|Royaume-Uni|Birleşik Krallık|Britania Raya|Reino Unido"),
("germany", "EUR", 24, "ألمانيا|Germany|Allemagne|Almanya|Jerman|Alemania"),
("italy", "EUR", 18, "إيطاليا|Italy|Italie|İtalya|Italia|Italia"),
("india", "INR", 22, "الهند|India|Inde|Hindistan|India|India"),
("pakistan", "PKR", 22, "باكستان|Pakistan|Pakistan|Pakistan|Pakistan|Pakistán"),
("malaysia", "MYR", 22, "ماليزيا|Malaysia|Malaisie|Malezya|Malaysia|Malasia"),
("canada", "CAD", 24, "كندا|Canada|Canada|Kanada|Kanada|Canadá"),
("australia", "AUD", 24, "أستراليا|Australia|Australie|Avustralya|Australia|Australia"),
("japan", "JPY", 24, "اليابان|Japan|Japon|Japonya|Jepang|Japón"),
("switzerland", "CHF", 24, "سويسرا|Switzerland|Suisse|İsviçre|Swiss|Suiza"),
("russia", "RUB", 24, "روسيا|Russia|Russie|Rusya|Rusia|Rusia"),
("china", "CNY", 24, "الصين|China|Chine|Çin|Tiongkok|China"),
("brazil", "BRL", 24, "البرازيل|Brazil|Brésil|Brezilya|Brasil|Brasil"),
]
CUR = {
"USD": ("2", "الدولار الأمريكي|US Dollar|Dollar américain|ABD Doları|Dolar AS|Dólar estadounidense"),
"EUR": ("2", "اليورو|Euro|Euro|Euro|Euro|Euro"),
"SAR": ("2", "الريال السعودي|Saudi Riyal|Riyal saoudien|Suudi Riyali|Riyal Saudi|Rial saudí"),
"AED": ("2", "الدرهم الإماراتي|UAE Dirham|Dirham des EAU|BAE Dirhemi|Dirham UEA|Dírham de los EAU"),
"EGP": ("0", "الجنيه المصري|Egyptian Pound|Livre égyptienne|Mısır Lirası|Pound Mesir|Libra egipcia"),
"KWD": ("3", "الدينار الكويتي|Kuwaiti Dinar|Dinar koweïtien|Kuveyt Dinarı|Dinar Kuwait|Dinar kuwaití"),
"QAR": ("2", "الريال القطري|Qatari Riyal|Riyal qatari|Katar Riyali|Riyal Qatar|Rial catarí"),
"BHD": ("3", "الدينار البحريني|Bahraini Dinar|Dinar bahreïni|Bahreyn Dinarı|Dinar Bahrain|Dinar bahreiní"),
"OMR": ("3", "الريال العماني|Omani Rial|Rial omanais|Umman Riyali|Rial Oman|Rial omaní"),
"JOD": ("3", "الدينار الأردني|Jordanian Dinar|Dinar jordanien|Ürdün Dinarı|Dinar Yordania|Dinar jordano"),
"IQD": ("0", "الدينار العراقي|Iraqi Dinar|Dinar irakien|Irak Dinarı|Dinar Irak|Dinar iraquí"),
"MAD": ("2", "الدرهم المغربي|Moroccan Dirham|Dirham marocain|Fas Dirhemi|Dirham Maroko|Dírham marroquí"),
"DZD": ("0", "الدينار الجزائري|Algerian Dinar|Dinar algérien|Cezayir Dinarı|Dinar Aljazair|Dinar argelino"),
"TND": ("3", "الدينار التونسي|Tunisian Dinar|Dinar tunisien|Tunus Dinarı|Dinar Tunisia|Dinar tunecino"),
"ILS": ("2", "الشيكل|Israeli Shekel|Shekel israélien|İsrail Şekeli|Shekel Israel|Shéquel israelí"),
"TRY": ("2", "الليرة التركية|Turkish Lira|Livre turque|Türk Lirası|Lira Turki|Lira turca"),
"IDR": ("0", "الروبية الإندونيسية|Indonesian Rupiah|Roupie indonésienne|Endonezya Rupisi|Rupiah Indonesia|Rupia indonesia"),
"GBP": ("2", "الجنيه الإسترليني|British Pound|Livre sterling|İngiliz Sterlini|Pound Inggris|Libra esterlina"),
"INR": ("0", "الروبية الهندية|Indian Rupee|Roupie indienne|Hindistan Rupisi|Rupee India|Rupia india"),
"PKR": ("0", "الروبية الباكستانية|Pakistani Rupee|Roupie pakistanaise|Pakistan Rupisi|Rupee Pakistan|Rupia pakistaní"),
"MYR": ("2", "الرينغيت الماليزي|Malaysian Ringgit|Ringgit malaisien|Malezya Ringgiti|Ringgit Malaysia|Ringgit malayo"),
"CAD": ("2", "الدولار الكندي|Canadian Dollar|Dollar canadien|Kanada Doları|Dolar Kanada|Dólar canadiense"),
"AUD": ("2", "الدولار الأسترالي|Australian Dollar|Dollar australien|Avustralya Doları|Dolar Australia|Dólar australiano"),
"JPY": ("0", "الين الياباني|Japanese Yen|Yen japonais|Japon Yeni|Yen Jepang|Yen japonés"),
"CHF": ("2", "الفرنك السويسري|Swiss Franc|Franc suisse|İsviçre Frangı|Franc Swiss|Franco suizo"),
"RUB": ("0", "الروبل الروسي|Russian Ruble|Rouble russe|Rus Rublesi|Rubel Rusia|Rublo ruso"),
"CNY": ("2", "اليوان الصيني|Chinese Yuan|Yuan chinois|Çin Yuanı|Yuan Tiongkok|Yuan chino"),
"BRL": ("2", "الريال البرازيلي|Brazilian Real|Réal brésilien|Brezilya Reali|Real Brasil|Real brasileño"),
}
HUBS = {"USD", "EUR", "GBP", "TRY", "SAR", "AED", "EGP", "IDR"}
KARATS = [24, 22, 21, 18, 14]

def cname(code, lang): return CUR[code][1].split("|")[LANGS.index(lang)]
def dec(code): return int(CUR[code][0])
def country_name(c, lang): return c[3].split("|")[LANGS.index(lang)]
def esc(s): return html.escape(s, quote=True)

PAIRS = [(a, b) for a in CUR for b in CUR if a != b and (a in HUBS or b in HUBS)]

CSS = r"""
:root{--g:#b8901a;--gb:#c9a227;--d:#1b1b1b;--bg:#faf8f2;--c:#fff;--m:#6b6b6b;--ln:#eee;--hd:#161616}
@media(prefers-color-scheme:dark){:root{--g:#e0b93c;--gb:#e0b93c;--d:#eee;--bg:#121212;--c:#1d1d1d;--m:#9a9a9a;--ln:#2c2c2c;--hd:#000}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:system-ui,"Segoe UI",Tahoma,Arial,sans-serif;background:var(--bg);color:var(--d);line-height:1.75}
header{background:var(--hd);padding:10px 14px}
.top{max-width:820px;margin:0 auto;display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;justify-content:space-between}
.top a.logo{color:var(--gb);text-decoration:none;font-weight:800;font-size:1.2rem}
nav{display:flex;gap:12px;flex-wrap:wrap}nav a{color:#ddd;text-decoration:none;font-size:.9rem}
.lang{font-size:.8rem}.lang a{color:#bbb;margin:0 4px;text-decoration:none}.lang a.on{color:var(--gb);font-weight:700}
main{max-width:820px;margin:0 auto;padding:14px}
h1{font-size:1.45rem;margin:.5em 0}h2{font-size:1.15rem;margin:1.6em 0 .4em}h3{font-size:1rem;margin:1em 0 .2em}
.card{background:var(--c);border-radius:12px;padding:14px;margin:12px 0;box-shadow:0 1px 4px #0002}
.hero{text-align:center}.big{font-size:2rem;font-weight:800;color:var(--g);direction:ltr;unicode-bidi:isolate}
.m{color:var(--m);font-size:.85rem}.up{color:#1a9b4b}.dn{color:#d33}
table{width:100%;border-collapse:collapse}td,th{padding:9px 5px;border-bottom:1px solid var(--ln);text-align:center}
th{background:rgba(184,144,26,.12)}td b{direction:ltr;unicode-bidi:isolate;display:inline-block}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.grid a{background:var(--c);padding:11px;border-radius:10px;text-align:center;text-decoration:none;color:var(--d);box-shadow:0 1px 3px #0002;font-size:.92rem}
input,select{width:100%;padding:10px;font-size:1rem;border:1px solid #bbb;border-radius:8px;margin:5px 0 10px;background:var(--c);color:var(--d)}
.row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
button,.btn{display:inline-block;background:var(--gb);color:#111;border:0;border-radius:8px;padding:9px 16px;font-size:.95rem;text-decoration:none;cursor:pointer}
.mm{display:flex;justify-content:space-between;direction:ltr;font-size:.8rem;color:var(--m)}
.ad{min-height:100px;margin:14px 0;text-align:center;overflow:hidden}
footer{text-align:center;color:var(--m);font-size:.8rem;padding:24px 12px}footer a{color:var(--m);margin:0 6px}
@media(max-width:480px){.row{grid-template-columns:1fr}}
"""

JS = r"""
(function(){
var P=window.PAGE,OZ=31.1035,$=function(i){return document.getElementById(i)};
function nf(v,d){try{return new Intl.NumberFormat(P.loc,{minimumFractionDigits:d,maximumFractionDigits:d}).format(v)}catch(e){return v.toFixed(d)}}
function dd(v){return v>=1000?0:v>=100?2:v>=1?3:v>=0.01?4:6}
function j(u){return fetch(u).then(function(r){if(!r.ok)throw 0;return r.json()})}
function hist(){return j(P.base+'/data/history.json').catch(function(){return []})}
function live(H){
  try{var c=JSON.parse(localStorage.getItem('lv')||'null');if(c&&Date.now()-c.t<300000)return Promise.resolve(c)}catch(e){}
  return Promise.all([j('https://api.gold-api.com/price/XAU'),j('https://api.gold-api.com/price/XAG').catch(function(){return null}),j('https://open.er-api.com/v6/latest/USD')])
  .then(function(a){var d={t:Date.now(),xau:a[0].price,xag:a[1]?a[1].price:null,r:a[2].rates};try{localStorage.setItem('lv',JSON.stringify(d))}catch(e){}return d})
  .catch(function(){var l=H[H.length-1];if(l)return {t:Date.parse(l.t||l.d),xau:l.xau,xag:l.xag,r:l.r,stale:1};throw 0})
}
function chart(el,pts,d){
  if(!el)return;if(pts.length<2){el.textContent=P.wait;return}
  var W=640,Hh=190,p=8,mn=Math.min.apply(null,pts),mx=Math.max.apply(null,pts),rg=(mx-mn)||1;
  var path=pts.map(function(v,i){return (i?'L':'M')+(p+i*(W-2*p)/(pts.length-1)).toFixed(1)+' '+(Hh-p-(v-mn)/rg*(Hh-2*p)).toFixed(1)}).join('');
  el.innerHTML='<svg viewBox="0 0 '+W+' '+Hh+'" width="100%" role="img"><path d="'+path+'" fill="none" stroke="var(--g)" stroke-width="2.5" stroke-linejoin="round"/></svg><div class="mm"><span>'+nf(mn,d)+'</span><span>'+nf(mx,d)+'</span></div>';
}
function change(el,pts){
  if(!el||pts.length<2)return;var c=(pts[pts.length-1]/pts[0]-1)*100;
  el.innerHTML=P.chg+': <b class="'+(c>=0?'up':'dn')+'">'+(c>=0?'+':'')+nf(c,2)+'%</b>';
}
function series(H,fn){var o=[];H.slice(-30).forEach(function(e){try{var v=fn(e);if(isFinite(v)&&v>0)o.push(v)}catch(x){}});return o}
function pg(d,k,cur){return d.xau/OZ*k/24*d.r[cur]}
function stamp(d){var u=$('upd');if(u)u.textContent=new Date(d.t).toLocaleString(P.loc,{dateStyle:'medium',timeStyle:'short'})}
function gold(H,d){
  document.querySelectorAll('[data-k]').forEach(function(e){e.textContent=nf(pg(d,+e.dataset.k,P.cur),P.dec)});
  if($('oz'))$('oz').textContent=nf(d.xau,2);
  if($('usd'))$('usd').textContent=nf(d.r[P.cur],dd(d.r[P.cur]));
  var tb=$('wt');if(tb){var ws=[1,5,8,10,20,50,100],h='';ws.forEach(function(w){h+='<tr><td>'+w+'</td>';P.cols.forEach(function(k){h+='<td><b>'+nf(w*pg(d,k,P.cur),P.dec)+'</b></td>'});h+='</tr>'});tb.innerHTML=h}
  var pts=series(H,function(e){return pg(e,P.hk,P.cur)});pts.push(pg(d,P.hk,P.cur));
  chart($('chart'),pts,P.dec);change($('chg'),pts);
  var g=$('gr'),kk=$('kk'),mk=$('mk'),tx=$('tx'),rs=$('res');
  function f(){var w=parseFloat(g.value)||0,m=parseFloat(mk.value)||0,x=parseFloat(tx.value)||0;rs.textContent=nf(w*pg(d,+kk.value,P.cur)*(1+m/100)*(1+x/100),P.dec)+' '+P.cur}
  [g,kk,mk,tx].forEach(function(e){e.oninput=f;e.onchange=f});f();
}
function rate(H,d){
  var r=d.r[P.to]/d.r[P.from];
  $('rate').textContent='1 '+P.from+' = '+nf(r,dd(r))+' '+P.to;
  var a=$('amt'),o=$('out');function f(){o.textContent=nf((parseFloat(a.value)||0)*r,dd(r)>3?4:2)+' '+P.to}a.oninput=f;f();
  var tb=$('ct'),h='';[1,5,10,50,100,500,1000].forEach(function(v){h+='<tr><td>'+nf(v,0)+' '+P.from+'</td><td><b>'+nf(v*r,dd(r)>3?4:2)+'</b> '+P.to+'</td><td>'+nf(v/r,dd(1/r)>3?4:2)+' '+P.from+'</td></tr>'});tb.innerHTML=h;
  var pts=series(H,function(e){return e.r[P.to]/e.r[P.from]});pts.push(r);chart($('chart'),pts,dd(r));change($('chg'),pts);
}
function zakat(H,d){
  var c=$('zc'),ids=['zg','zs','zm','zd'];
  function f(){var cur=c.value,rt=d.r[cur],g=pg(d,24,cur)*(parseFloat($('zg').value)||0),
    s=d.xag?d.xag/OZ*rt*(parseFloat($('zs').value)||0):0,w=g+s+(parseFloat($('zm').value)||0)-(parseFloat($('zd').value)||0),
    ns=d.xag?595*d.xag/OZ*rt:85*pg(d,24,cur),k=dec(cur);
    $('zn').textContent=nf(ns,k);$('zw').textContent=nf(w,k);
    $('zr').textContent=w>=ns?(nf(w*0.025,k)+' '+cur):P.notdue;}
  function dec(cur){return P.decs&&P.decs[cur]!=null?P.decs[cur]:2}
  ids.concat(['zc']).forEach(function(i){$(i).oninput=f;$(i).onchange=f});f();
}
function share(){var b=$('share');if(!b)return;b.onclick=function(){var u=location.href,tt=document.title;
  if(navigator.share){navigator.share({title:tt,url:u}).catch(function(){})}else{window.open('https://wa.me/?text='+encodeURIComponent(tt+' '+u),'_blank')}}}
share();
if('serviceWorker' in navigator){navigator.serviceWorker.register(P.base+'/sw.js').catch(function(){})}
if(P.type==='home'){live([]).then(function(d){if($('oz'))$('oz').textContent=nf(d.xau,2)}).catch(function(){});return}
hist().then(function(H){return live(H).then(function(d){
  stamp(d);if(d.stale&&$('upd'))$('upd').textContent+=' *';
  if(P.type==='gold')gold(H,d);else if(P.type==='rate')rate(H,d);else if(P.type==='zakat')zakat(H,d);
})}).catch(function(){if($('upd'))$('upd').textContent=P.err});
})();
"""

SW = """const C='gfx-v1';
self.addEventListener('install',e=>{self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(self.clients.claim())});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==location.origin)return;
  e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(C).then(x=>x.put(e.request,c));return r}).catch(()=>caches.match(e.request)));
});
"""

ICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="110" fill="#161616"/><circle cx="256" cy="256" r="150" fill="#c9a227"/><circle cx="256" cy="256" r="118" fill="none" stroke="#161616" stroke-width="14"/><text x="256" y="300" font-size="150" font-family="Arial" font-weight="700" text-anchor="middle" fill="#161616">Au</text></svg>"""

def ad(lang):
    if ADSENSE and AD_SLOT:
        return f'<div class="ad"><ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE}" data-ad-slot="{AD_SLOT}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>'
    return ""

def href(lang, rel): return f"{BASE}/{lang}/{rel}"
def url(lang, rel): return f"{SITE_URL}{BASE}/{lang}/{rel}"

def page(lang, rel, title, desc, body, cfg):
    d = "rtl" if lang == "ar" else "ltr"
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{url(l, rel)}">' for l in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{url("en", rel)}">'
    sw = "".join(f'<a href="{href(l, rel)}"{" class=on" if l == lang else ""} hreflang="{l}">{n}</a>' for l, n in zip(LANGS, NATIVE))
    adsense_head = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>' if ADSENSE else ""
    cfg = dict(cfg, loc=LOC[lang], base=BASE, err=t("err", lang), wait=t("chart_wait", lang), chg=t("chg", lang), notdue=t("z_notdue", lang))
    return f"""<!doctype html><html lang="{lang}" dir="{d}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#161616">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url(lang, rel)}">{alts}
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{url(lang, rel)}">
<link rel="manifest" href="{BASE}/manifest.json"><link rel="icon" href="{BASE}/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{BASE}/style.css">{adsense_head}</head><body>
<header><div class="top"><a class="logo" href="{href(lang, 'index.html')}">🪙 {esc(t('name', lang))}</a>
<nav><a href="{href(lang, 'index.html')}#gold">{t('gold_nav', lang)}</a><a href="{href(lang, 'index.html')}#fx">{t('fx_nav', lang)}</a><a href="{href(lang, 'zakat.html')}">{t('zakat_nav', lang)}</a></nav>
<div class="lang">{sw}</div></div></header><main>{body}</main>
<footer><p>{t('disc', lang)}</p><p><a href="{href(lang, 'about.html')}">{t('about', lang)}</a><a href="{href(lang, 'privacy.html')}">{t('privacy', lang)}</a><a href="{href(lang, 'contact.html')}">{t('contact', lang)}</a></p><p>© {datetime.date.today().year} {esc(t('name', lang))}</p></footer>
<script>window.PAGE={json.dumps(cfg, ensure_ascii=False)}</script><script src="{BASE}/app.js" defer></script></body></html>"""

def faq_block(lang):
    items = [(t(f"q{i}", lang), t(f"a{i}", lang)) for i in (1, 2, 3)]
    h = f"<h2>{t('faq_h', lang)}</h2>" + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in items)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return h + '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>"

def gold_page(lang, c):
    slug, cur, hk, _ = c
    name, cn = country_name(c, lang), cname(cur, lang)
    cols = sorted({24, hk, 18}, reverse=True)
    rows = "".join(f'<tr><td>{t("karat", lang, k=k)}</td><td><b data-k="{k}">…</b> {cur}</td></tr>' for k in KARATS)
    opts = "".join(f'<option value="{k}"{" selected" if k == hk else ""}>{t("karat", lang, k=k)}</option>' for k in KARATS)
    wh = "".join(f"<th>{t('karat', lang, k=k)}</th>" for k in cols)
    others = "".join(f'<a href="{href(lang, "gold/" + o[0] + ".html")}">{esc(country_name(o, lang))}</a>' for o in COUNTRIES if o[0] != slug)
    body = f"""<h1>{esc(t('gold_h1', lang, c=name))}</h1>
<div class="card hero"><div class="m">{t('per_gram', lang)} · {t('karat', lang, k=hk)}</div><div class="big"><span data-k="{hk}">…</span> {cur}</div>
<div class="m">{t('upd', lang)}: <span id="upd">…</span></div><div id="chg" style="margin-top:6px"></div>
<p><button id="share" type="button">{t('share', lang)}</button></p></div>
{ad(lang)}
<div class="card"><table><tr><th>{t('karat_h', lang)}</th><th>{t('per_gram', lang)}</th></tr>{rows}</table>
<p class="m">{t('ounce', lang)}: $<b id="oz">…</b> · 1 USD = <b id="usd">…</b> {cur}</p></div>
<h2>{t('chart_h', lang)}</h2><div class="card" style="direction:ltr"><div id="chart"></div></div>
<h2>{t('weights_h', lang)}</h2><div class="card"><table><tr><th>g</th>{wh}</tr><tbody id="wt"></tbody></table></div>
{ad(lang)}
<h2>{t('calc_h', lang)}</h2><div class="card"><div class="row"><div><label>{t('weight', lang)}</label><input id="gr" type="number" inputmode="decimal" value="10"></div>
<div><label>{t('karat_h', lang)}</label><select id="kk">{opts}</select></div>
<div><label>{t('making', lang)}</label><input id="mk" type="number" inputmode="decimal" value="0"></div>
<div><label>{t('tax', lang)}</label><input id="tx" type="number" inputmode="decimal" value="0"></div></div>
<div class="m">{t('total', lang)}</div><div class="big" id="res">…</div></div>
{faq_block(lang)}
<h2>{t('others', lang)}</h2><div class="grid">{others}</div>"""
    cfg = {"type": "gold", "cur": cur, "dec": dec(cur), "hk": hk, "cols": cols}
    return page(lang, f"gold/{slug}.html", t("gold_title", lang, c=name), t("gold_desc", lang, c=name, cur=cn), body, cfg)

def rate_page(lang, a, b):
    an, bn = cname(a, lang), cname(b, lang)
    rel = f"rate/{a.lower()}-{b.lower()}.html"
    related = [(a, x) for x in sorted(HUBS) if x not in (a, b) and (a, x) in PAIRS][:6] + [(x, b) for x in sorted(HUBS) if x not in (a, b) and (x, b) in PAIRS][:6]
    rel_html = "".join(f'<a href="{href(lang, f"rate/{p.lower()}-{q.lower()}.html")}">{p} → {q}</a>' for p, q in related)
    body = f"""<h1>{esc(t('fx_h1', lang, a=an, b=bn))}</h1>
<div class="card hero"><div class="big" id="rate">…</div><div class="m">{t('upd', lang)}: <span id="upd">…</span></div><div id="chg" style="margin-top:6px"></div>
<p><button id="share" type="button">{t('share', lang)}</button></p></div>
{ad(lang)}
<div class="card"><label>{t('amount', lang)} ({a})</label><input id="amt" type="number" inputmode="decimal" value="1"><div class="big" id="out">…</div>
<p><a class="btn" href="{href(lang, f'rate/{b.lower()}-{a.lower()}.html')}">⇄ {t('swap', lang)} ({b} → {a})</a></p></div>
<h2>{t('chart_h', lang)}</h2><div class="card" style="direction:ltr"><div id="chart"></div></div>
<h2>{t('common', lang)}</h2><div class="card"><table><tr><th>{a}</th><th>{b}</th><th>{b} → {a}</th></tr><tbody id="ct"></tbody></table></div>
{ad(lang)}
<h2>{t('pairs_h', lang)}</h2><div class="grid">{rel_html}</div>"""
    cfg = {"type": "rate", "from": a, "to": b}
    return page(lang, rel, t("fx_title", lang, a=an, b=bn), t("fx_desc", lang, a=an, b=bn), body, cfg)

def zakat_page(lang):
    opts = "".join(f'<option value="{k}">{k} — {esc(cname(k, lang))}</option>' for k in CUR)
    body = f"""<h1>{esc(t('zakat_h1', lang))}</h1><p>{t('zakat_desc', lang)}</p>
<div class="card"><label>{t('z_cur', lang)}</label><select id="zc">{opts}</select>
<div class="row"><div><label>{t('z_gold', lang)}</label><input id="zg" type="number" inputmode="decimal" value="0"></div>
<div><label>{t('z_silver', lang)}</label><input id="zs" type="number" inputmode="decimal" value="0"></div>
<div><label>{t('z_cash', lang)}</label><input id="zm" type="number" inputmode="decimal" value="0"></div>
<div><label>{t('z_debt', lang)}</label><input id="zd" type="number" inputmode="decimal" value="0"></div></div>
<p class="m">{t('z_nisab', lang)}: <b id="zn">…</b> · {t('z_wealth', lang)}: <b id="zw">…</b></p>
<div class="m">{t('z_due', lang)}</div><div class="big" id="zr">…</div><p class="m">{t('upd', lang)}: <span id="upd">…</span></p>
<p class="m">{t('z_note', lang)}</p><p><button id="share" type="button">{t('share', lang)}</button></p></div>{ad(lang)}"""
    return page(lang, "zakat.html", t("zakat_h1", lang) + " | " + t("name", lang), t("zakat_desc", lang), body, {"type": "zakat", "cur": "USD", "dec": 2, "decs": {k: dec(k) for k in CUR}})

def home_page(lang):
    gl = "".join(f'<a href="{href(lang, "gold/" + c[0] + ".html")}">{esc(country_name(c, lang))}</a>' for c in COUNTRIES)
    featured = [("USD", "EGP"), ("USD", "SAR"), ("USD", "TRY"), ("USD", "IDR"), ("EUR", "USD"), ("USD", "AED"), ("EUR", "TRY"), ("SAR", "EGP"), ("USD", "MAD"), ("EUR", "EGP"), ("USD", "IQD"), ("USD", "DZD"), ("GBP", "USD"), ("USD", "INR"), ("USD", "PKR"), ("EUR", "GBP"), ("USD", "JPY"), ("USD", "CNY")]
    fl = "".join(f'<a href="{href(lang, f"rate/{p.lower()}-{q.lower()}.html")}">{p} → {q}</a>' for p, q in featured if (p, q) in PAIRS)
    body = f"""<h1>{esc(t('home_h1', lang))}</h1><p>{t('home_p', lang)}</p>
<div class="card hero"><div class="m">XAU / USD · {t('ounce', lang)}</div><div class="big">$<span id="oz">…</span></div></div>{ad(lang)}
<h2 id="gold">{t('gold_nav', lang)}</h2><div class="grid">{gl}</div>
<h2 id="fx">{t('pairs_h', lang)}</h2><div class="grid">{fl}</div>
<h2>{t('zakat_nav', lang)}</h2><p><a class="btn" href="{href(lang, 'zakat.html')}">{t('zakat_h1', lang)}</a></p>"""
    return page(lang, "index.html", f"{t('name', lang)} — {t('home_h1', lang)}", t("home_desc", lang), body, {"type": "home"})

def info_page(lang, key):
    txt = t(key + "_p", lang, email=EMAIL) if key != "contact" else t("contact_p", lang, email=EMAIL)
    body = f"<h1>{t(key, lang)}</h1><div class='card'><p>{esc(txt)}</p></div>"
    return page(lang, f"{key}.html", f"{t(key, lang)} | {t('name', lang)}", esc(txt)[:150], body, {"type": "info"})

ROOT = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gold & FX</title><link rel="canonical" href="%(site)s%(base)s/en/index.html">
%(alts)s
<script>var m={ar:1,en:1,fr:1,tr:1,id:1,es:1},l=(navigator.language||'en').slice(0,2).toLowerCase();if(!m[l])l='en';location.replace('%(base)s/'+l+'/index.html')</script>
<meta http-equiv="refresh" content="2;url=%(base)s/en/index.html"></head><body><p>%(links)s</p></body></html>"""

def write(path, s):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f: f.write(s)

def main():
    if os.path.isdir(os.path.join(OUT, "ar")):
        for l in LANGS: shutil.rmtree(os.path.join(OUT, l), ignore_errors=True)
    urls = []
    for l in LANGS:
        write(f"{l}/index.html", home_page(l)); urls.append((l, "index.html"))
        write(f"{l}/zakat.html", zakat_page(l)); urls.append((l, "zakat.html"))
        for k in ("about", "privacy", "contact"):
            write(f"{l}/{k}.html", info_page(l, k)); urls.append((l, f"{k}.html"))
        for c in COUNTRIES:
            write(f"{l}/gold/{c[0]}.html", gold_page(l, c)); urls.append((l, f"gold/{c[0]}.html"))
        for a, b in PAIRS:
            write(f"{l}/rate/{a.lower()}-{b.lower()}.html", rate_page(l, a, b)); urls.append((l, f"rate/{a.lower()}-{b.lower()}.html"))
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{url(l, "index.html")}">' for l in LANGS)
    links = " ".join(f'<a href="{href(l, "index.html")}">{n}</a>' for l, n in zip(LANGS, NATIVE))
    write("index.html", ROOT % {"site": SITE_URL, "base": BASE, "alts": alts, "links": links})
    write("style.css", CSS); write("app.js", JS); write("sw.js", SW); write("icon.svg", ICON)
    write("manifest.json", json.dumps({"name": "Gold & FX", "short_name": "Gold & FX", "start_url": f"{BASE}/index.html", "display": "standalone",
                                       "background_color": "#161616", "theme_color": "#161616",
                                       "icons": [{"src": f"{BASE}/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"}]}))
    today = datetime.date.today().isoformat()
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
          "".join(f"<url><loc>{url(l, r)}</loc><lastmod>{today}</lastmod></url>" for l, r in urls) + "</urlset>")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}{BASE}/sitemap.xml\n")
    if ADSENSE:
        write("ads.txt", f"google.com, {ADSENSE.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n")
    if DOMAIN: write("CNAME", DOMAIN + "\n")
    hp = os.path.join(OUT, "data", "history.json")
    if not os.path.exists(hp): write("data/history.json", "[]")
    write(".nojekyll", "")
    print("pages:", len(urls))

if __name__ == "__main__":
    main()
