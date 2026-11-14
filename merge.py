import urllib.request

SOURCES = [
    "https://iptv-org.github.io/iptv/countries/ir.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ir_telewebion.m3u",
    "https://iptv-org.github.io/iptv/languages/fas.m3u",
]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")

out = ["#EXTM3U"]
seen = set()
ok = 0

for src in SOURCES:
    try:
        text = fetch(src)
    except Exception as e:
        print("FAILED:", src, e)
        continue
    ok += 1
    info = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#EXTM3U"):
            continue
        if line.startswith("#"):
            info.append(line)
            continue
        if line not in seen:
            seen.add(line)
            out.extend(info)
            out.append(line)
        info = []

if ok < len(SOURCES):
    raise SystemExit("Some sources failed, keeping the old playlist")

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

print(len(seen), "channels written")
