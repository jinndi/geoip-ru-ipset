import os
import requests
from ipaddress import ip_network, ip_address, summarize_address_range
from tqdm import tqdm

RU_URL = "https://raw.githubusercontent.com/v2fly/geoip/refs/heads/release/text/ru.txt"

BLOCKED_URLS = [
    "https://antifilter.download/list/ip.lst",
    "https://antifilter.download/list/ipresolve.lst",
    "https://antifilter.download/list/allyouneed.lst"
]

# -----------------------------
# PARSER (CIDR + single IP)
# -----------------------------
def parse(line):
    line = line.strip()
    if not line:
        return None

    try:
        if "/" in line:
            n = ip_network(line, strict=False)
            return (int(n.network_address), int(n.broadcast_address))
        else:
            ip = ip_address(line)
            return (int(ip), int(ip))
    except:
        return None


# -----------------------------
# DOWNLOAD
# -----------------------------
def download(url):
    print(f"[+] Downloading {url}")
    r = requests.get(url, timeout=120)
    r.raise_for_status()

    out = []
    for line in r.text.splitlines():
        p = parse(line)
        if p:
            out.append(p)

    return out


# -----------------------------
# LOAD DATA
# -----------------------------
ru = download(RU_URL)

blocked = []
for url in BLOCKED_URLS:
    data = download(url)
    print(f"    {len(data)} entries")
    blocked.extend(data)


# -----------------------------
# SORT (CRITICAL FOR SPEED)
# -----------------------------
def sort_ranges(ranges):
    return sorted(ranges, key=lambda x: (x[0], x[1]))


ru = sort_ranges(ru)
blocked = sort_ranges(blocked)


# -----------------------------
# RIPE-STYLE SWEEP SUBTRACT
# -----------------------------
def subtract(a, b):
    clean = []
    removed = []

    i = 0
    n = len(b)

    for s, e in tqdm(a, desc="sweep"):
        cur = s

        while cur <= e:

            while i < n and b[i][1] < cur:
                i += 1

            if i < n and b[i][0] <= cur <= b[i][1]:
                bs, be = b[i]

                removed.append((max(cur, bs), min(e, be)))
                cur = be + 1
                continue

            nxt = b[i][0] if i < n else e + 1
            stop = min(e, nxt - 1)

            clean.append((cur, stop))
            cur = stop + 1

    return clean, removed


# -----------------------------
# MERGE (IMPORTANT OPTIMIZATION)
# -----------------------------
def merge(ranges):
    if not ranges:
        return []

    ranges = sorted(ranges)
    out = []

    cs, ce = ranges[0]

    for s, e in ranges[1:]:
        if s <= ce + 1:
            ce = max(ce, e)
        else:
            out.append((cs, ce))
            cs, ce = s, e

    out.append((cs, ce))
    return out


# -----------------------------
# RANGE -> CIDR (fast RIPE style)
# -----------------------------
def to_cidrs(ranges):
    out = []
    for s, e in ranges:
        out.extend(summarize_address_range(ip_address(s), ip_address(e)))
    return out


def sort_cidrs(cidrs):
    return sorted(
        (str(x) for x in cidrs),
        key=lambda x: (
            ip_network(x).version,
            int(ip_network(x).network_address),
            int(ip_network(x).prefixlen)
        )
    )


# -----------------------------
# SPLIT IPv4 / IPv6
# -----------------------------
V4_MAX = 2**32

ru_v4 = [x for x in ru if x[1] < V4_MAX]
ru_v6 = [x for x in ru if x[1] >= V4_MAX]

bl_v4 = [x for x in blocked if x[1] < V4_MAX]
bl_v6 = [x for x in blocked if x[1] >= V4_MAX]


# -----------------------------
# PROCESS
# -----------------------------
print("\n[IPv4]")
clean4, rem4 = subtract(ru_v4, bl_v4)

print("\n[IPv6]")
clean6, rem6 = subtract(ru_v6, bl_v6)


# -----------------------------
# OPTIMIZE (IMPORTANT STEP)
# -----------------------------
clean4 = merge(clean4)
clean6 = merge(clean6)
rem4 = merge(rem4)
rem6 = merge(rem6)


# -----------------------------
# CIDR CONVERT
# -----------------------------
print("\n[+] CIDR conversion...")

clean4 = sort_cidrs(to_cidrs(clean4))
clean6 = sort_cidrs(to_cidrs(clean6))

rem4 = sort_cidrs(to_cidrs(rem4))
rem6 = sort_cidrs(to_cidrs(rem6))


# -----------------------------
# SAVE
# -----------------------------
os.makedirs("data", exist_ok=True)

with open("data/ru-no-blocked.txt", "w") as f:
    f.write("\n".join(clean4))

with open("data/ru-no-blocked6.txt", "w") as f:
    f.write("\n".join(clean6))

with open("data/ru-blocked.txt", "w") as f:
    f.write("\n".join(rem4))

with open("data/ru-blocked6.txt", "w") as f:
    f.write("\n".join(rem6))


# -----------------------------
# STATS
# -----------------------------
print("\n✔ DONE")
print("IPv4 no blocked:", len(clean4))
print("IPv6 no blocked:", len(clean6))
print("IPv4 blocked:", len(rem4))
print("IPv6 blocked:", len(rem6))