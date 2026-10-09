"""Buduje wielostronicową stronę z dane.json + _szablony/.

Uruchom z dowolnego katalogu:  python _narzedzia/buduj.py

Układ:  _szablony/uklad.html (wspólna rama: head, nagłówek, stopka)
        _szablony/strony/<id>.html (treść każdej podstrony)
        _szablony/404.html
Wynik (nie edytuj ręcznie): index.html, oferta/, wiedza/, realizacje/, kontakt/, 404.html, sitemap.xml, robots.txt.
Znaczniki {{NAZWA}} podmienia funkcja pola(). Nieznany znacznik przerywa budowanie.
Dane firmy są w dane.json: tam je zmieniaj. Brakujące dane (telefon, adres, godziny, e-mail, zdjęcia)
pokazują się jako „do uzupełnienia"; po wpisaniu wartości w dane.json znikają same.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "dane.json").read_text(encoding="utf-8"))
F = D["firma"]

e = escape  # skrót: escapowanie tekstu do HTML

DNI_EN = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 0: "Sunday"}

SVG_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>'
SVG_PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>'

# ikony kart (styl kreskowy 24×24, kolorowane w CSS)
IKONY = {
    "start": '<path d="M12 3v8M6.3 6.5a8 8 0 1 0 11.4 0"/>',
    "akumulator": '<rect x="2" y="7" width="17" height="10" rx="2"/><path d="M22 10.5v3M7 12h5M9.5 9.5v5"/>',
    "ostrzezenie": '<path d="M12 3 2.5 20h19z"/><path d="M12 10v5M12 17.6v.4"/>',
    "blyskawica": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "wtyczka": '<path d="M9 2v5M15 2v5M6 7h12v4a6 6 0 0 1-12 0zM12 17v5"/>',
    "ogien": '<path d="M12 22c4 0 7-2.8 7-6.5 0-3-2-5-3.5-7-.5 2-1.5 3-3 3 0-3-1-6-3-8.5C8.5 6 5 9.5 5 15.5 5 19.2 8 22 12 22z"/>',
    "klucz": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.1L3 17.7 6.3 21l6.3-6.3a4 4 0 0 0 5.1-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
}

TODO = '<span class="todo">do uzupełnienia</span>'


def ikona(nazwa: str) -> str:
    return f'<svg viewBox="0 0 24 24">{IKONY[nazwa]}</svg>'


def wersja(sciezka: str) -> str:
    """Znacznik ?v= z hasha pliku, żeby przeglądarka pobrała nową wersję po zmianie."""
    h = hashlib.sha1((ROOT / sciezka).read_bytes()).hexdigest()[:8]
    return f"{sciezka}?v={h}"


def przed_startem() -> bool:
    """Dopóki adres to example.com, strona jest roboczym szkicem: noindex i robots bez zgody na indeksację."""
    return "example.com" in D["strona"]["url"]


def tel_e164(tel: str) -> str:
    return "+48" + re.sub(r"\D", "", tel)


def bazowy_url() -> str:
    return D["strona"]["url"].rstrip("/") + "/"


def trasa_url() -> str:
    return f'https://www.google.com/maps/dir/?api=1&destination={F["lat"]},{F["lng"]}'


def mapy_url() -> str:
    return "https://www.google.com/maps?cid=" + F["mapy_cid"]


def sloty() -> list[dict]:
    """Godziny z dane.json, które mają ustawione dni tygodnia (do statusu i schema.org)."""
    return [g for g in F.get("godziny", []) if not g.get("zamkniete") and g.get("dni_tyg")]


# ---------- przyciski i bloki zależne od dostępnych danych ----------

def cta(klasa: str = "") -> str:
    """Główny przycisk: telefon, a dopóki go nie ma – wyznaczenie trasy (potwierdzona lokalizacja)."""
    kl = f"btn {klasa}".strip()
    if F["telefon"]:
        return f'<a class="{kl}" href="tel:{tel_e164(F["telefon"])}">{SVG_TEL}Zadzwoń: {e(F["telefon"])}</a>'
    return f'<a class="{kl}" href="{e(trasa_url())}" target="_blank" rel="noopener">{SVG_PIN}Wyznacz trasę</a>'


def cta_naglowek() -> str:
    if F["telefon"]:
        return (f'<a class="btn btn--sm top__cta" href="tel:{tel_e164(F["telefon"])}" aria-label="Zadzwoń: {e(F["telefon"])}">'
                f'{SVG_TEL}<span>{e(F["telefon"])}</span></a>')
    return (f'<a class="btn btn--sm top__cta" href="{e(trasa_url())}" target="_blank" rel="noopener" aria-label="Wyznacz trasę w Mapach Google">'
            f'{SVG_PIN}<span>Wyznacz trasę</span></a>')


def cta_menu() -> str:
    if F["telefon"]:
        return f'<a class="nav__tel" href="tel:{tel_e164(F["telefon"])}">Zadzwoń: {e(F["telefon"])}</a>'
    return f'<a class="nav__tel" href="{e(trasa_url())}" target="_blank" rel="noopener">Wyznacz trasę</a>'


def godziny_tekst() -> str:
    """Krótki opis godzin (np. „Poniedziałek – sobota 08:00–18:00"), pusty gdy brak danych."""
    czesci = []
    for g in F.get("godziny", []):
        czesci.append(f'{g["dni"]}: zamknięte' if g.get("zamkniete") else f'{g["dni"]} {g["od"]}–{g["do"]}')
    return "; ".join(czesci)


def godziny_html() -> str:
    if not F.get("godziny"):
        return f'<div><dt>Godziny otwarcia</dt><dd>{TODO}</dd></div>'
    wiersze = []
    for g in F["godziny"]:
        wartosc = "Zamknięte" if g.get("zamkniete") else f'{g["od"]}–{g["do"]}'
        wiersze.append(f'<div><dt>{e(g["dni"])}</dt><dd>{wartosc}</dd></div>')
    return "\n          ".join(wiersze)


def godziny_json() -> str:
    if not sloty():
        return ""
    dane = [{"d": g["dni_tyg"], "od": g["od"], "do": g["do"]} for g in sloty()]
    return '<script type="application/json" id="godziny-dane">' + json.dumps(dane) + "</script>"


def status_html() -> str:
    if not sloty():
        return ""
    return ('<p class="status reveal" id="status" aria-live="polite" hidden>'
            '<span class="status__dot" aria-hidden="true"></span><span id="status-tekst"></span></p>')


def adres_tekst() -> str:
    if not F["ulica"]:
        return ""
    return f'{F["ulica"]}, {F["kod"]} {F["miejscowosc"]}'.strip(", ")


def lead() -> str:
    czesci = []
    if adres_tekst():
        czesci.append(f"{e(adres_tekst())}.")
    else:
        czesci.append("Sprawdź lokalizację na mapie, wyznacz trasę i napisz do nas.")
    if godziny_tekst():
        czesci.append(f"Godziny otwarcia: {e(godziny_tekst())}.")
    return " ".join(czesci)


def cta_opis() -> str:
    zdania = ["Zadzwoń i opisz usterkę." if F["telefon"] else "Opisz usterkę w formularzu kontaktowym albo sprawdź dojazd na mapie."]
    if godziny_tekst():
        zdania.append(f"Godziny otwarcia: {e(godziny_tekst())}.")
    return " ".join(zdania)


def pasek_html() -> str:
    tel = (f'<a href="tel:{tel_e164(F["telefon"])}"><strong>{e(F["telefon"])}</strong></a>' if F["telefon"]
           else f"<strong>Telefon</strong> {TODO}")
    godz = (f"<strong>{e(godziny_tekst())}</strong> Godziny otwarcia" if godziny_tekst()
            else f"<strong>Godziny</strong> {TODO}")
    lok = (f"<strong>{e(adres_tekst())}</strong> Lokalizacja" if adres_tekst()
           else f'<strong>Dojazd</strong> <a class="link link--w" href="{e(trasa_url())}" target="_blank" rel="noopener">Wyznacz trasę w Mapach Google</a>')
    return "\n    ".join([
        f"<li><strong>{e(F['branza'])}</strong> {e(F['nazwa'])}</li>",
        f"<li>{lok}</li>",
        f"<li>{godz}</li>",
        f"<li>{tel}</li>",
    ])


def karta_tel() -> str:
    if F["telefon"]:
        return (f'<p class="karta__duze"><a href="tel:{tel_e164(F["telefon"])}">{e(F["telefon"])}</a></p>'
                '<p class="karta__male">Najszybszy sposób na umówienie wizyty.</p>')
    return f'<p class="karta__duze">{TODO}</p><p class="karta__male">Do tego czasu napisz do nas przez formularz poniżej.</p>'


def karta_adres() -> str:
    adres = (f'<address>{e(F["ulica"])}<br>{e(F["kod"])} {e(F["miejscowosc"])}</address>' if F["ulica"]
             else f"<address>{TODO}</address>")
    return (f'{adres}<a class="link" href="{e(trasa_url())}" target="_blank" rel="noopener">Wyznacz trasę w Mapach Google</a>')


def email_blok() -> str:
    if F.get("email"):
        return f'E-mail: <a href="mailto:{e(F["email"])}">{e(F["email"])}</a>'
    return f"E-mail: {TODO}"


def stopka_kontakt() -> str:
    linie = []
    linie.append(f'<a href="tel:{tel_e164(F["telefon"])}">{e(F["telefon"])}</a>' if F["telefon"] else f"Telefon: {TODO}")
    linie.append(e(F["ulica"]) + "<br>" + e(f'{F["kod"]} {F["miejscowosc"]}') if F["ulica"] else f"Adres: {TODO}")
    return "<br>".join(linie)


def opis_stopki() -> str:
    if F["miejscowosc"]:
        return f'{e(F["branza"])} w miejscowości {e(F["miejscowosc"])}.'
    return e(F["nazwa_pelna"]) + "."


def tel_atrybut() -> str:
    return f' data-tel="{e(F["telefon"])}"' if F["telefon"] else ""


# ---------- treści z dane.json ----------

def faq_html() -> str:
    out = []
    for p in D["faq"]:
        out.append(f'<details>\n        <summary>{e(p["q"])}</summary>\n        <p>{p["a"]}</p>\n      </details>')
    out.append('<details>\n        <summary><span class="todo">Pytanie do uzupełnienia</span></summary>\n'
               '        <p><span class="todo">Odpowiedź do uzupełnienia</span></p>\n      </details>')
    return "\n      ".join(out)


def artykuly_html() -> str:
    out = []
    for a in D["artykuly"]:
        akapity = "".join(f"<p>{e(t)}</p>" for t in a["tresc"])
        out.append(
            f'<article class="artykul reveal" id="{e(a["id"])}">\n'
            f'        <p class="artykul__znacznik">{e(a["kategoria"])}</p>\n'
            f'        <h3>{e(a["tytul"])}</h3>\n        {akapity}\n      </article>'
        )
    return "\n      ".join(out)


def artykuly_podglad_html() -> str:
    out = []
    for a in D["artykuly"][:3]:
        out.append(
            f'<a class="usluga reveal" href="/wiedza/#{e(a["id"])}">\n'
            f'        <span class="usluga__ikona" aria-hidden="true">{ikona(a["ikona"])}</span>\n'
            f'        <h3>{e(a["tytul"])}</h3>\n'
            f'        <p>{e(a["tresc"][0])}</p>\n'
            f'        <span class="usluga__link">Czytaj dalej →</span>\n      </a>'
        )
    return "\n      ".join(out)


def zdjecie(i: int, klasa: str = "") -> str:
    z = D["zdjecia"][i]
    return (
        f'<a class="foto {klasa}" href="/assets/img/realizacje/{z["plik"]}.webp" data-lightbox aria-label="Powiększ zdjęcie: {e(z["alt"])}">'
        f'<img src="/assets/img/realizacje/{z["plik"]}-s.webp" alt="{e(z["alt"])}" width="{z["w"]}" height="{z["h"]}" loading="lazy" decoding="async"></a>'
    )


def galeria_html() -> str:
    if D["zdjecia"]:
        return "\n      ".join(zdjecie(i) for i in range(len(D["zdjecia"])))
    ramki = ['<div class="foto foto--pusty" role="img" aria-label="Miejsce na zdjęcie z warsztatu"><span class="todo">Zdjęcie do uzupełnienia</span></div>'] * 6
    return "\n      ".join(ramki)


def sekcja_realizacje() -> str:
    """Podgląd galerii na stronie głównej: tylko gdy są prawdziwe zdjęcia."""
    if not D["zdjecia"]:
        return ""
    miniatury = "\n      ".join(zdjecie(i) for i in range(min(4, len(D["zdjecia"]))))
    return f"""<section class="sekcja sekcja--alt" aria-labelledby="h-real">
  <div class="wrap">
    <header class="sekcja__glowa sekcja__glowa--rzad reveal">
      <div>
        <p class="eyebrow">Realizacje</p>
        <h2 id="h-real">Z naszego warsztatu</h2>
      </div>
      <a class="btn btn--ghost" href="/realizacje/">Wszystkie zdjęcia</a>
    </header>
    <div class="podglad reveal">
      {miniatury}
    </div>
  </div>
</section>"""


def nawigacja(aktywna: str) -> str:
    out = []
    for s in D["strony"]:
        cur = ' aria-current="page"' if s["id"] == aktywna else ""
        out.append(f'<a href="{s["sciezka"]}"{cur}>{e(s["menu"])}</a>')
    return "\n      ".join(out)


# ---------- dane strukturalne ----------

def bez_tagow(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).replace("{{TRASA}}", "").replace("{{MAPY_URL}}", "")


def jsonld(strona_id: str) -> str:
    firma: dict = {
        "@type": "AutoRepair",
        "name": F["nazwa_pelna"],
        "geo": {"@type": "GeoCoordinates", "latitude": F["lat"], "longitude": F["lng"]},
        "hasMap": mapy_url(),
    }
    if F["telefon"]:
        firma["telephone"] = tel_e164(F["telefon"])
    if F["ulica"]:
        firma["address"] = {
            "@type": "PostalAddress",
            "streetAddress": F["ulica"],
            "postalCode": F["kod"],
            "addressLocality": F["miejscowosc"],
            "addressCountry": "PL",
        }
    if sloty():
        firma["openingHoursSpecification"] = [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": [DNI_EN[d] for d in g["dni_tyg"]], "opens": g["od"], "closes": g["do"]}
            for g in sloty()
        ]
    if not przed_startem():
        firma["url"] = bazowy_url()
    graf = [firma]
    if strona_id == "wiedza":
        graf.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": p["q"], "acceptedAnswer": {"@type": "Answer", "text": bez_tagow(p["a"])}}
                for p in D["faq"]
            ],
        })
    dane = {"@context": "https://schema.org", "@graph": graf}
    return json.dumps(dane, ensure_ascii=False, indent=2).replace("</", "<\\/")


def pola(strona: dict | None = None) -> dict[str, str]:
    """Znaczniki dostępne w szablonach. Nowy znacznik dopisz tutaj."""
    s = D["strona"]
    p = strona or {"id": "", "sciezka": "/", "title": s["title"], "description": s["description"]}
    kanon = bazowy_url().rstrip("/") + p["sciezka"]
    return {
        "LANG": s.get("jezyk", "pl-PL"),
        "NAZWA": e(F["nazwa"]),
        "NAZWA_PELNA": e(F["nazwa_pelna"]),
        "BRANZA": e(F["branza"]),
        "TITLE": e(p["title"]),
        "DESCRIPTION": e(p["description"]),
        "CANONICAL": kanon,
        "OG_IMAGE": bazowy_url() + "assets/img/og-image.png",
        "ROBOTS_META": '<meta name="robots" content="noindex, nofollow">' if przed_startem() else '<meta name="robots" content="index, follow, max-image-preview:large">',
        "FONTS": wersja("assets/css/fonts.css"),
        "CSS": wersja("assets/css/style.css"),
        "JS": wersja("assets/js/main.js"),
        "NAV": nawigacja(p["id"]),
        "CTA": cta(),
        "CTA_LG": cta("btn--lg"),
        "CTA_NAGLOWEK": cta_naglowek(),
        "CTA_MENU": cta_menu(),
        "CTA_OPIS": cta_opis(),
        "LEAD": lead(),
        "PASEK": pasek_html(),
        "STATUS": status_html(),
        "GODZINY_JSON": godziny_json(),
        "GODZINY": godziny_html(),
        "KARTA_TEL": karta_tel(),
        "KARTA_ADRES": karta_adres(),
        "EMAIL_BLOK": email_blok(),
        "STOPKA_KONTAKT": stopka_kontakt(),
        "OPIS_STOPKI": opis_stopki(),
        "TEL_ATRYBUT": tel_atrybut(),
        "LAT": str(F["lat"]),
        "LNG": str(F["lng"]),
        "TRASA": e(trasa_url()),
        "MAPY_URL": mapy_url(),
        "MAPY_CID": F["mapy_cid"],
        "JSONLD": jsonld(p["id"]),
        "FAQ": faq_html(),
        "ARTYKULY": artykuly_html(),
        "ARTYKULY_PODGLAD": artykuly_podglad_html(),
        "GALERIA": galeria_html(),
        "SEKCJA_REALIZACJE": sekcja_realizacje(),
        "FORM_ACTION": e(D["formularz"].get("endpoint", "")),
        "ID_STRONY": p["id"],
    }


def zloz(szablon: str, wartosci: dict[str, str]) -> str:
    # kilka przebiegów: treść podstrony zawiera znaczniki, które dopiero układ i bloki rozwijają
    for _ in range(6):
        def podmien(m: re.Match) -> str:
            klucz = m.group(1)
            if klucz not in wartosci:
                sys.exit("Nieznany znacznik {{" + klucz + "}} w szablonie: dopisz go w pola() w _narzedzia/buduj.py")
            return wartosci[klucz]

        nowy = re.sub(r"\{\{(\w+)\}\}", podmien, szablon)
        if nowy == szablon:
            break
        szablon = nowy
    return szablon


def zapisz(sciezka: str, tresc: str) -> None:
    cel = ROOT / sciezka
    cel.parent.mkdir(parents=True, exist_ok=True)
    cel.write_text(tresc, encoding="utf-8", newline="\n")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows przy przekierowaniu wyjścia domyślnie używa cp1252
    uklad = (ROOT / "_szablony" / "uklad.html").read_text(encoding="utf-8")
    wynik = []
    for st in D["strony"]:
        w = pola(st)
        w["TRESC"] = (ROOT / "_szablony" / "strony" / f'{st["id"]}.html').read_text(encoding="utf-8")
        cel = "index.html" if st["sciezka"] == "/" else st["sciezka"].strip("/") + "/index.html"
        zapisz(cel, zloz(uklad, w))
        wynik.append(cel)

    w404 = pola()
    w404["TRESC"] = (ROOT / "_szablony" / "404.html").read_text(encoding="utf-8")
    zapisz("404.html", zloz(uklad, w404).replace("<title>", "<title>Nie znaleziono strony – ", 1)
           .replace('<meta name="robots" content="noindex, nofollow">', "")
           .replace('<meta name="robots" content="index, follow, max-image-preview:large">', "")
           .replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1))

    url = bazowy_url().rstrip("/")
    wpisy = "\n".join(f"  <url><loc>{url}{s['sciezka']}</loc></url>" for s in D["strony"])
    zapisz(
        "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + wpisy + "\n</urlset>\n",
    )
    if przed_startem():
        zapisz("robots.txt", "User-agent: *\nDisallow: /\n")
    else:
        zapisz("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {url}/sitemap.xml\n")

    print("Zbudowano:", ", ".join(wynik), "+ 404.html, sitemap.xml, robots.txt")
    if przed_startem():
        print('UWAGA: strona.url w dane.json to example.com, więc strona ma noindex. Wpisz prawdziwy adres przed publikacją.')


if __name__ == "__main__":
    main()
