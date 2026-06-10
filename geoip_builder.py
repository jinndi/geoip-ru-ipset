import os
import requests
from ipaddress import ip_network, ip_address, summarize_address_range
from tqdm import tqdm

RU_URL = "https://ipbl.herrbischoff.com/geoip/ru.netset"

BLOCKED_URLS = [
  # antifilter.download
  "https://antifilter.download/list/ip.lst",
  "https://antifilter.download/list/ipresolve.lst",
  "https://antifilter.download/list/allyouneed.lst",

  # community.antifilter.download
  "https://community.antifilter.download/list/community.lst",

  # Re-filter
  "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ipsum.lst",

  # antifilter.network
  "https://antifilter.network/download/ip.lst",
  "https://antifilter.network/download/ipsmart.lst",
  "https://antifilter.network/download/ipsum.lst",
  "https://antifilter.network/download/subnet.lst"
  # "https://antifilter.network/download/ip6.lst"
]

def parse(line):
  line = line.strip()
  if not line or line.startswith("#"):
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

def merge(ranges):
  if not ranges:
    return []
  # Сортируем по началу диапазона, затем по концу
  ranges = sorted(ranges, key=lambda x: (x[0], x[1]))
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

# Быстрый вычитатель без циклов внутри диапазонов (работает мгновенно и для IPv6)
def subtract(a, b):
  clean = []
  removed = []
  
  i = 0
  n = len(b)
  
  for s, e in tqdm(a, desc="subtracting"):
    cur = s
    while cur <= e and i < n:
      # Пропускаем блокировки, которые остались позади текущего указателя cur
      if b[i][1] < cur:
        i += 1
        continue
          
      # Блокировка пересекается с текущим диапазоном
      if b[i][0] <= e:
        # Если перед блокировкой есть чистый кусок - сохраняем его
        if cur < b[i][0]:
          clean.append((cur, b[i][0] - 1))
        
        # Записываем то, что было вырезано
        rem_start = max(cur, b[i][0])
        rem_end = min(e, b[i][1])
        removed.append((rem_start, rem_end))
        
        # Сдвигаем cur за край текущей блокировки
        cur = b[i][1] + 1
        if cur > e:
          break
      else:
        # Блокировка находится дальше, чем конец нашего текущего диапазона 'e'
        break
    
    # Если после всех блокировок в рамках текущего диапазона остался хвост
    if cur <= e:
      clean.append((cur, e))
          
  return clean, removed

def to_cidrs(ranges):
  out = []
  for s, e in ranges:
    out.extend(summarize_address_range(ip_address(s), ip_address(e)))
  return out

# Оптимизированная сортировка (парсим сеть только ОДИН раз для каждого элемента)
def sort_cidrs(cidrs):
  def sorting_key(cidr_obj):
    return (cidr_obj.version, int(cidr_obj.network_address), int(cidr_obj.prefixlen))

  # Создаем объекты один раз, сортируем и возвращаем строки
  objects = [ip_network(x) for x in cidrs]
  objects.sort(key=sorting_key)
  return [str(x) for x in objects]

# --- MAIN PROCESS ---

ru = download(RU_URL)
blocked = []
for url in BLOCKED_URLS:
  data = download(url)
  print(f"    {len(data)} entries")
  blocked.extend(data)

V4_MAX = 2**32

print("\n[+] Merging input ranges (preparation)...")
ru_v4 = merge([x for x in ru if x[1] < V4_MAX])
ru_v6 = merge([x for x in ru if x[1] >= V4_MAX])

bl_v4 = merge([x for x in blocked if x[1] < V4_MAX])
bl_v6 = merge([x for x in blocked if x[1] >= V4_MAX])

print("\n[IPv4]")
clean4, rem4 = subtract(ru_v4, bl_v4)

print("\n[IPv6]")
clean6, rem6 = subtract(ru_v6, bl_v6)

# Повторный мерж на выходе (на всякий случай, хотя после subtract они уже чистые)
clean4 = merge(clean4)
clean6 = merge(clean6)
rem4 = merge(rem4)
rem6 = merge(rem6)

print("\n[+] CIDR conversion...")
clean4 = sort_cidrs(to_cidrs(clean4))
clean6 = sort_cidrs(to_cidrs(clean6))
rem4 = sort_cidrs(to_cidrs(rem4))
rem6 = sort_cidrs(to_cidrs(rem6))

os.makedirs("data", exist_ok=True)

with open("data/ru-no-blocked.txt", "w") as f:
  f.write("\n".join(clean4))
with open("data/ru-no-blocked6.txt", "w") as f:
  f.write("\n".join(clean6))
with open("data/ru-blocked.txt", "w") as f:
  f.write("\n".join(rem4))
with open("data/ru-blocked6.txt", "w") as f:
  f.write("\n".join(rem6))

print("\n✔ DONE")
print("IPv4 no blocked:", len(clean4))
print("IPv4 blocked:", len(rem4))
print("IPv6 no blocked:", len(clean6))
print("IPv6 blocked:", len(rem6))