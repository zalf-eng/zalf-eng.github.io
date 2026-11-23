"""Rekap jumlah pembaca harian dari penghitung Abacus ke stats/pembaca.json."""
import datetime
import glob
import json
import os
import time
import urllib.error
import urllib.request

NS = "zalf-eng.github.io"
OUT = "stats/pembaca.json"


def ambil(key):
    url = f"https://abacus.jasoncameron.dev/get/{NS}/{key}"
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return json.load(r).get("value", 0)
    except urllib.error.HTTPError as e:
        return 0 if e.code == 404 else None
    except Exception:
        return None


def main():
    artikel = {}
    for path in sorted(glob.glob("_posts/*.md")):
        slug = os.path.basename(path)[11:-3]
        artikel[slug] = ambil("p-" + slug[:60])
        time.sleep(0.5)
    total = ambil("total")
    tanggal = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d")

    data = {"riwayat": []}
    if os.path.exists(OUT):
        with open(OUT) as f:
            data = json.load(f)
    data["riwayat"] = [r for r in data["riwayat"] if r["tanggal"] != tanggal]
    data["riwayat"].append({"tanggal": tanggal, "total": total, "artikel": artikel})
    data["riwayat"] = data["riwayat"][-120:]
    data["keterangan"] = "Angka kumulatif sejak penghitung dipasang (23 Nov 2026). Pembaca minggu ini = angka hari ini dikurangi angka 7 hari lalu. null = gagal dibaca."

    os.makedirs("stats", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
