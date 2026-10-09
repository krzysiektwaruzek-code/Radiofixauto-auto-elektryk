# Radiofixauto – auto elektryk – strona www

Statyczna strona (HTML + CSS + JS, bez frameworka), w tym samym układzie i stylu co projekt `serwis-milejowiec`.
**Wszystkie dane firmy są w `dane.json`.** Po każdej zmianie danych, szablonów, CSS lub JS:

```
python _narzedzia/buduj.py
```

Skrypt generuje `index.html`, `oferta/`, `wiedza/`, `realizacje/`, `kontakt/`, `404.html`, `sitemap.xml` i `robots.txt`
(nie edytuj ich ręcznie) i odświeża `?v=` przy CSS/JS. Lokalny podgląd: `python -m http.server` w katalogu repo
(ścieżki w HTML są absolutne, więc plików nie otwieraj przez `file://`).

## Struktura

```
dane.json                 dane firmy, FAQ, artykuły, lista podstron
_szablony/uklad.html      wspólna rama (head, menu, stopka, lightbox)
_szablony/strony/*.html   treść podstron (start, oferta, wiedza, realizacje, kontakt)
_szablony/404.html        treść strony błędu
_narzedzia/buduj.py       składa stronę, sitemap i robots (znaczniki {{NAZWA}} dopisuj w pola())
_zrodla/ZRODLA.md         skąd pochodzi każda dana (wewnętrzne, .htaccess blokuje publikację)
assets/css, js, fonts     style, skrypty i lokalne fonty (Barlow Condensed, Inter, licencja OFL)
```

## Zasada: tylko potwierdzone dane

Na stronie są wyłącznie dane z wizytówki Google (nazwa, współrzędne) oraz telefon, adres i godziny podane przez
zleceniodawcę (patrz `_zrodla/ZRODLA.md`). E-mail, usługi, ceny, opinie i zdjęcia nie zostały wymyślone
i są oznaczone na stronie jako „do uzupełnienia". Treści w „Wiedza" to ogólne poradniki dla kierowców, a nie opis oferty firmy.

## Co uzupełnić po otrzymaniu danych od klienta

| Dane | Gdzie |
|---|---|
| E-mail (telefon, adres i godziny są już wpisane) | `dane.json` → `firma`. Znikają znaczniki „do uzupełnienia", przyciski „Wyznacz trasę" zamieniają się w „Zadzwoń", uzupełnia się JSON-LD |
| Godziny otwarcia | `dane.json` → `firma.godziny`, np. `{"dni": "Poniedziałek – sobota", "od": "08:00", "do": "18:00", "dni_tyg": [1,2,3,4,5,6]}` (0 = niedziela; wpis zamknięty: `{"dni": "Niedziela", "zamkniete": true}`). Włącza się też status „Teraz otwarte" |
| Zdjęcia | pliki WebP w `assets/img/realizacje/` (`r01.webp` + miniatura `r01-s.webp`) i wpisy w `dane.json` → `zdjecia` (`plik`, `w`, `h`, `alt`). Pojawi się galeria, lightbox i podgląd na stronie głównej |
| Usługi, cennik | `_szablony/strony/oferta.html` i `start.html` (pola `todo`) |
| FAQ, poradniki | `dane.json` → `faq`, `artykuly` |
| Formularz | `dane.json` → `formularz.endpoint` (np. Formspree lub własny skrypt PHP) |
| Logo, og:image | `assets/img/` (obecne grafiki są tylko typograficzne i nie są logo firmy) |
| Zgoda RODO / polityka prywatności | checkbox w `_szablony/strony/kontakt.html`, treść do zatwierdzenia przez klienta |

## Publikacja

Dopóki `strona.url` w `dane.json` to `example.com`, strona ma `noindex`, a `robots.txt` zabrania indeksowania.
Przed publikacją na Hostingerze wpisz tam prawdziwy adres (https://domena) i przebuduj. Wtedy włączają się
indeksacja, `canonical`, Open Graph i `sitemap.xml` z właściwą domeną. Zawartość repo (bez `_narzedzia`, `_szablony`, `_zrodla`,
które blokuje `.htaccess`) wgraj do `public_html`.

Po wdrożeniu: dodać stronę w Google Search Console, wysłać `sitemap.xml` i wpisać adres strony w Profilu Firmy.
Najsilniejszy sygnał lokalnego SEO to zgodne dane NAP (nazwa, adres, telefon) na stronie, w wizytówce i w JSON-LD.
