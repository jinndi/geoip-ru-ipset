# geoip-ru
Списки незаблокированных и заблокированных российских IP-адресов


## 📖 О проекте

Репозиторий содержит автоматически обновляемые списки российских IP-адресов, разделённые на:

- незаблокированные IP-адреса;
- заблокированные IP-адреса.

В качестве источника используется база российских сетей RU GeoIP из Loyalsoldier и списки заблокированных IP из Antifilter (download + network), Re-filter (1andrevich) и OpenCCK (все группы). Во время сборки выполняется исключение заблокированных диапазонов из общего списка российских адресов, после чего формируются отдельные списки для IPv4 и IPv6.

Списки могут использоваться в ipset, маршрутизации и других сетевых сценариях.

**Обновление** выполняется автоматически каждый день


## 📦 Источники данных

### RU GeoIP (все известные российские IP-адреса из базы Loyalsoldier)

```
Диапазоны IPv4 и IPv6 в одном файле.
Данные собраны из альтернативных источников в попытке повысить точность.
Для повышения эффективности были удалены дубликаты и объединены подсети.
```

**Что означает «альтернативных источников»?**

Официальные файлы делегирования региональных регистраторов (RIR) показывают только то, кому подсеть принадлежит юридически, но ничего не знают о том, где эти IP-адреса используются фактически. Этот список пытается учесть реальное географическое положение серверов на основе тестов и коммерческих баз.

Для конфигурации маршрутизации коммерческая гео-локация - это самый разумный выбор. Она гарантирует, что всё, что должно работать напрямую в РФ (включая контентные серверы зарубежных компаний, расположенные внутри страны), будет доступно на максимальной скорости провайдера, а заблокированные ресурсы алгоритм чисто вырежет из этой базы.

- https://raw.githubusercontent.com/Loyalsoldier/geoip/release/text/ru.txt

### Block Lists (известные заблокированные IP-адреса)

  **antifilter.download**

  - https://antifilter.download/list/ip.lst
  - https://antifilter.download/list/ipresolve.lst
  - https://antifilter.download/list/allyouneed.lst

  **community.antifilter.download**

  - https://community.antifilter.download/list/community.lst

  **Re-filter 1andrevich**

  - https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ipsum.lst

  **antifilter.network**
  
  - https://antifilter.network/download/ip.lst
  - https://antifilter.network/download/ipsmart.lst
  - https://antifilter.network/download/ipsum.lst
  - https://antifilter.network/download/subnet.lst

  **OpenCCK**

  - https://iplist.opencck.org/?format=text&data=cidr4&group=ai&group=anime&group=art&group=casino&group=discord&group=education&group=finance&group=games&group=hosting&group=jetbrains&group=messengers&group=music&group=news&group=porn&group=shop&group=socials&group=tools&group=torrent&group=video&group=youtube

  - https://iplist.opencck.org/?format=text&data=cidr6&group=ai&group=anime&group=art&group=casino&group=discord&group=education&group=finance&group=games&group=hosting&group=jetbrains&group=messengers&group=music&group=news&group=porn&group=shop&group=socials&group=tools&group=torrent&group=video&group=youtube

## 📁 Выходные файлы

```
data/
 ├── ru-no-blocked.txt  // IPv4 не заблокированные (clean)
 ├── ru-no-blocked6.txt // IPv6 не заблокированные (clean)
 ├── ru-blocked.txt     // IPv4 заблокированные (blocked)
 ├── ru-blocked6.txt    // IPv6 заблокированные (blocked)
ru-no-blocked.srs // IPv4+IPv6 не заблокированные для sing-box
ru-blocked.srs // IPv4+IPv6 заблокированные для sing-box
```

## 📥 Готовые списки

### Актуальные сгенерированные файлы для ipset и прочего испльзования (txt):

- 🟢 IPv4 (clean): https://raw.githubusercontent.com/jinndi/geoip-ru-ipset/main/data/ru-no-blocked.txt
- 🟢 IPv6 (clean): https://raw.githubusercontent.com/jinndi/geoip-ru-ipset/main/data/ru-no-blocked6.txt 
- 🔴 IPv4 (blocked): https://raw.githubusercontent.com/jinndi/geoip-ru-ipset/main/data/ru-blocked.txt
- 🔴 IPv6 (blocked): https://raw.githubusercontent.com/jinndi/geoip-ru-ipset/main/data/ru-blocked6.txt


### Актуальные сгенерированные файлы для sing-box (srs):

**ru-no-blocked.srs**

```
https://cdn.jsdelivr.net/gh/jinndi/geoip-ru@main/ru-no-blocked.srs
```

```
https://github.com/jinndi/geoip-ru/raw/main/ru-no-blocked.srs
```

**ru-blocked.srs**

```
https://cdn.jsdelivr.net/gh/jinndi/geoip-ru@main/ru-blocked.srs
```

```
https://github.com/jinndi/geoip-ru/raw/main/ru-blocked.srs
```