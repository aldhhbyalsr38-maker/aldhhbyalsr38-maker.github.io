#!/usr/bin/env python3
"""Daily snapshot of gold/silver/FX into docs/data/history.json (run by GitHub Actions)."""
import json, os, urllib.request, datetime
OUT = os.environ.get("OUT_DIR", "docs")
CODES = "USD EUR SAR AED EGP KWD QAR BHD OMR JOD IQD MAD DZD TND ILS TRY IDR".split()
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "gold-fx-bot"}), timeout=30) as r:
        return json.load(r)
xau = get("https://api.gold-api.com/price/XAU")["price"]
try: xag = get("https://api.gold-api.com/price/XAG")["price"]
except Exception: xag = None
rates = get("https://open.er-api.com/v6/latest/USD")["rates"]
now = datetime.datetime.now(datetime.timezone.utc)
e = {"d": now.date().isoformat(), "t": now.isoformat(), "xau": xau, "xag": xag, "r": {c: rates[c] for c in CODES if c in rates}}
p = os.path.join(OUT, "data", "history.json")
os.makedirs(os.path.dirname(p), exist_ok=True)
try: H = json.load(open(p))
except Exception: H = []
H = [x for x in H if x.get("d") != e["d"]] + [e]
json.dump(H[-400:], open(p, "w"), separators=(",", ":"))
print("saved", e["d"], len(H))
