import urllib.request

GROUPS = {
    "playlist.m3u": [  # Iran / Persian
        "https://iptv-org.github.io/iptv/countries/ir.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ir_telewebion.m3u",
        "https://iptv-org.github.io/iptv/languages/fas.m3u",
    ],
    "azerbaijan.m3u": [  # Azerbaijan
        "https://iptv-org.github.io/iptv/countries/az.m3u",
        "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlists/playlist_azerbaijan.m3u8",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/az.m3u",
    ],
}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")

written = 0

for filename, sources in GROUPS.items():
    out = ["#EXTM3U"]
    seen = set()
    failed = False
    for src in sources:
        try:
            text = fetch(src)
        except Exception as e:
            print("FAILED:", src, e)
            failed = True
            break
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
    if failed:
        print("Keeping old", filename)
        continue
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(filename, ":", len(seen), "channels")
    written += 1

if written == 0:
    raise SystemExit("All groups failed")
