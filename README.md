# Radiofixauto – auto elektryk

Statyczna strona-wizytówka (HTML / CSS / JS, bez budowania i bez zależności) przygotowana pod hosting na Hostingerze.

## Zasada: tylko potwierdzone dane

Na stronie znajdują się wyłącznie informacje potwierdzone w podanej wizytówce Google Maps:
nazwa **Radiofixauto auto elektryk** i współrzędne **51.9552285, 19.2790293**.
Adres, telefon, godziny, usługi, opinie, zdjęcia i logo **nie zostały wymyślone** – miejsca na nie są przygotowane (patrz niżej).

## Struktura

```
index.html            strona główna (hero, objawy usterek, kroki kontaktu, kontakt/mapa/formularz, FAQ)
404.html              strona błędu 404
assets/css/style.css  style (tokeny kolorów w :root)
assets/js/main.js     menu mobilne, reveal on scroll, walidacja formularza
assets/img/           favicon, apple-touch-icon i og-image.png (grafiki typograficzne – to NIE jest logo firmy)
robots.txt, sitemap.xml, manifest.webmanifest, .htaccess
scripts/set-domain.sh podmiana domeny po wdrożeniu
scripts/check.sh      kontrola przed wdrożeniem (czy nie zostały placeholdery)
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

## Treści informacyjne

Sekcje „Objawy usterek", „Jak się z nami skontaktować" i FAQ to ogólne treści pomocnicze dla kierowców oraz opis samej strony.
**Nie opisują oferty firmy** (żadnych usług, cen, czasów ani gwarancji). Treść FAQ jest zduplikowana w JSON-LD (`FAQPage`) –
zmieniając jedno, zmień drugie. Sekcje można swobodnie usunąć lub rozbudować po uzyskaniu danych od klienta.

## SEO – co jest zrobione

Title, description, canonical, hreflang, robots meta, Open Graph + Twitter Card (z obrazem 1200×630), JSON-LD
(`WebSite`, `WebPage`, `AutoRepair` z nazwą i współrzędnymi, `FAQPage`), jedno H1 i logiczne H2/H3, semantyczny HTML,
`robots.txt`, `sitemap.xml`, manifest, nagłówki bezpieczeństwa i cache w `.htaccess`.

## SEO – co zrobić po wdrożeniu

1. `./scripts/set-domain.sh https://twoja-domena.pl`, a potem `./scripts/check.sh`.
2. Dodać stronę w Google Search Console, zweryfikować domenę i wysłać `sitemap.xml`.
3. W wizytówce Google (Profil Firmy) wpisać adres strony. Dane NAP (nazwa, adres, telefon) muszą być identyczne na stronie, w wizytówce i w JSON-LD.
4. Po uzyskaniu adresu i telefonu uzupełnić `address`, `telephone`, `openingHoursSpecification` w JSON-LD oraz dodać nazwę miejscowości do title/H1/description (to najsilniejszy sygnał lokalnego SEO).
5. Uzupełnić sekcję usług (osobne podstrony usług dopiero, gdy będą potwierdzone treści).
