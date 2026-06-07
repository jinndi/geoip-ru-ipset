# geoip-ru-ipset
Списки незаблокированных и заблокированных российских IP-адресов для ipset


## 📖 О проекте

Репозиторий содержит автоматически обновляемые списки российских IP-адресов, разделённые на:

- незаблокированные IP-адреса;
- заблокированные IP-адреса.

В качестве источника используется база российских сетей RU GeoIP из v2fly и списки заблокированных IP из Antifilter. Во время сборки выполняется исключение заблокированных диапазонов из общего списка российских адресов, после чего формируются отдельные списки для IPv4 и IPv6.

Списки могут использоваться в ipset, nftables, маршрутизации, DPI-обходе, прокси-серверах и других сетевых сценариях.

**Обновление** выполняется автоматически каждый день в 00:00 МСК.


## 📦 Источники данных

### RU GeoIP (все известные российские IP-адреса)

- https://raw.githubusercontent.com/v2fly/geoip/refs/heads/release/text/ru.txt

### Block Lists (известные заблокированные IP-адреса из базы Antifilter)

- https://antifilter.download/list/ip.lst
- https://antifilter.download/list/ipresolve.lst
- https://antifilter.download/list/allyouneed.lst


## 📁 Выходные файлы

```
data/
 ├── ru-no-blocked.txt  // IPv4 не заблокированные (clean)
 ├── ru-no-blocked6.txt // IPv6 не заблокированные (clean)
 ├── ru-blocked.txt     // IPv4 заблокированные (blocked)
 ├── ru-blocked6.txt    // IPv6 заблокированные (blocked)
```

## 📥 Готовые списки

Актуальные сгенерированные файлы:

- 🟢 IPv4 (clean): https://raw.githubusercontent.com/jinndi/geoip-ru-ipset/main/data/ru-no-blocked.txt
- 🟢 IPv6 (clean): https://raw.githubusercontent.com/jinndi/geoip-ru-ipset/main/data/ru-no-blocked6.txt 
- 🔴 IPv4 (blocked): https://raw.githubusercontent.com/jinndi/geoip-ru-ipset/main/data/ru-blocked.txt
- 🔴 IPv6 (blocked): https://raw.githubusercontent.com/jinndi/geoip-ru-ipset/main/data/ru-blocked6.txt
