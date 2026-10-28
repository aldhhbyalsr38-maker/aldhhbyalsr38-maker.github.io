# Gold & FX — دليل التشغيل السريع

1. أنشئ مستودعاً على GitHub وارفع كل محتويات هذا المجلد (docs, gen.py, update.py, .github).
2. Settings → Pages → Branch: main، Folder: /docs.
3. Settings → Actions → General → Workflow permissions → Read and write.
4. Actions → update-data → Run workflow (يجمع الأسعار كل 6 ساعات ويبني الرسوم البيانية).
5. بعد شراء الدومين أعد التوليد (مثال):
   SITE_URL=https://yourdomain.com DOMAIN=yourdomain.com CONTACT_EMAIL=you@mail.com python gen.py
6. بعد موافقة AdSense:
   SITE_URL=... ADSENSE_CLIENT=ca-pub-XXXXXXXXXXXXXXXX AD_SLOT=1234567890 python gen.py
   (يولّد ads.txt ويضيف كود AdSense ووحدات الإعلان تلقائياً)
7. ارفع الناتج، وأرسل sitemap.xml إلى Google Search Console.
