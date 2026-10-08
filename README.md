# Radiofixauto – auto elektryk

Statyczna strona-wizytówka (HTML / CSS / JS, bez budowania i bez zależności) przygotowana pod hosting na Hostingerze.

## Zasada: tylko potwierdzone dane

Na stronie znajdują się wyłącznie informacje potwierdzone w podanej wizytówce Google Maps:
nazwa **Radiofixauto auto elektryk** i współrzędne **51.9552285, 19.2790293**.
Adres, telefon, godziny, usługi, opinie, zdjęcia i logo **nie zostały wymyślone** – miejsca na nie są przygotowane (patrz niżej).

## Struktura

```
index.html            strona główna (hero + kontakt/mapa/formularz)
404.html              strona błędu 404
assets/css/style.css  style (tokeny kolorów w :root)
assets/js/main.js     menu mobilne, reveal on scroll, walidacja formularza
assets/img/           favicon (neutralny monogram – to NIE jest logo firmy)
robots.txt, sitemap.xml, .htaccess
scripts/set-domain.sh podmiana domeny po wdrożeniu
```

## Co uzupełnić po otrzymaniu danych od klienta

| Dane | Gdzie |
|---|---|
| Domena | `./scripts/set-domain.sh https://twoja-domena.pl` (canonical, OG, robots, sitemap) |
| Adres, telefon, e-mail, godziny | `index.html` → sekcja `#kontakt`, wiersze z `data-todo` (usuń `hidden`) |
| Przycisk „Zadzwoń" | zakomentowany w hero (`index.html`) |
| Usługi | sekcja `#uslugi` (`hidden`) + link w nawigacji (zakomentowany) |
| Schema.org | blok JSON-LD w `<head>`: `address`, `telephone`, `openingHoursSpecification`, `url`, `image` |
| Logo / zdjęcia / og:image | `assets/img/`, tag `og:image` w `<head>` |
| Formularz | atrybut `data-endpoint` w `<form id="contact-form">` (np. Formspree lub własny skrypt PHP). Bez niego formularz uczciwie informuje, że nie jest aktywny |
| Zgoda RODO / polityka prywatności | treść checkboxa w formularzu – do zatwierdzenia przez klienta |

## Wdrożenie na Hostingerze

Wgraj zawartość repozytorium do `public_html` (Menedżer plików / FTP / Git w hPanel).
