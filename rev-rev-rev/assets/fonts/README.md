# বাংলা PDF font

Noto Sans Bengali-এর variable font Google Fonts-এর official repository থেকে নেওয়া হয়েছে:

- Source: https://github.com/google/fonts/tree/main/ofl/notosansbengali
- License: [SIL Open Font License 1.1](OFL.txt)
- Downloaded: 2026-10-29

`scripts/build_pdf.py` একই variable font থেকে weight 400 ও 700-এর static instance তৈরি করে। PDF-তে প্রয়োজনীয় font glyph embedded থাকে; reader-এর device-এ font install করতে হয় না।

নতুন বাংলা দৃশ্যগুলো HarfBuzz দিয়ে text shape করে SVG glyph outline হিসেবে রাখে। তাই PNG/SVG/PDF-এ যুক্তাক্ষর একই থাকে। Arrow ও কিছু Latin symbol-এর fallback হিসেবে স্থানীয় DejaVu Sans-এর অপরিবর্তিত copy সংযুক্ত; তার [copyright ও license](DejaVu-LICENSE.txt) একই folder-এ আছে।
