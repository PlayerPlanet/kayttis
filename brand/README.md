# Hanax

**Tavallinen hana. Hanax tietää, onko se auki.**
Lähde kotoa huoletta: Hanax näyttää eteisen paneelista ja puhelimesta, jäikö hana, liesi tai valot päälle.

Hanax syntyi yhdestä arkisesta pelosta: astianpesukoneen hana jäi auki. Vesivahinko on kallis, eikä kotivakuutus aina korvaa sitä. Sama huoli koskee liettä, uunia, kahvinkeitintä ja valoja. Nimi tulee hanasta, josta kaikki alkoi.

Hanax on Aalto-yliopiston Käyttäjälähtöinen tuotekehitysprojekti -kurssin ryhmän 1 tuotekonsepti (2026). Lyhyt muoto: *Aalto-yliopisto · Käyttäjälähtöinen tuotekehitysprojekti 2026 · Ryhmä 1*. Brändikirja v2 (dark-first) on kaikkien materiaalien lähde.

## Yksi väite, yksi todiste, yksi toiminto

Jokainen materiaali rakentuu samasta kolmikosta:

1. **Väite:** *Tavallinen hana. Hanax tietää, onko se auki.* Mekaaninen venttiili ilman elektroniikkaa, ja silti tila on tiedossa. Arkinen tehtävä, vaikea ongelma.
2. **Todiste:** prototyyppi toimii oikeassa keittiössä. Raspberry Pi killan keittiössä lukee kahden kahvinkeittimen pistorasioita ja valoja, ja kameramalli lukee astianpesukoneen hanan venttiilin. Näytä se leikkaamattomana: aikaleimat, oikeat lukemat.
3. **Toiminto:** *Katso livenä* (demo osastolla / kayttis.kiirikki.fi).

Väitteet pitää aina pystyä jäljittämään demoon. Jos jokin on suunnitelma eikä toimi vielä, sano se: **konseptimalli**, **tavoite**, **suunniteltu**.

## Kenelle

- **Ensisijainen:** omakotitalossa asuvat keski-ikäiset, joilla on kiireinen arki.
- **Toissijainen:** mökkien omistajat ja lyhytvuokraajat.
- **Ostajana usein aikuinen lapsi** vanhemmilleen.

## Mitä lupaamme

| Ydinviesti | Perustelu |
| --- | --- |
| Näet kaiken yhdellä vilkaisulla. | Testihenkilöt ymmärsivät paneelin heti ilman ohjeita (RT7). |
| Toimii laitteiden kanssa, jotka sinulla jo on. | Anturi lukee tavallisen hanan, lieden tai pistorasian; prototyyppi lukee jo mekaanista venttiiliä kameralla (demo). |
| Asennat itse, ilman putkimiestä. | Asennus oli suurin käyttöönoton este (RT8). *Suunniteltu.* |
| Kotisi tiedot pysyvät kotona. | Paikallinen käsittely (prototyyppi: Raspberry Pi kotiverkossa). Pilvettömyys ja Suomi-säilytys ovat *tavoite*. |
| Yksi nuppi: kaikki pois. | Testeissä toivottiin yhtä katkaisijaa (RT7). Paneelin fyysinen nuppi. |

**Älä lupaa** vakuutusalennuksia, sertifikaatteja, valmista hintaa (tavoite 50–150 € sensoreineen) tai toimitusaikaa. Renderöidyt laitteet ovat **konseptimalleja**.

## Ääni

Rauhallinen insinööri, ei mainosmies. Lyhyet lauseet, konkreettiset luvut, ei huutomerkkejä eikä emojeja. Puhuttele sinuksi. Nimeä asiat niin kuin ihminen ne nimeää ("keittiön hana"). Kerro aina tuoreus: "KIINNI · tarkistettu 12 s sitten".

## Art direction (v2)

Mallina Figure (elokuvallinen teollinen minimalismi), Oura (materiaalit) ja Physical Intelligence (arkinen tehtävä todisteena).

- **Pimeys on pinta.** Lähes musta grafiitti, valo tulee kohteesta. Syvyys syntyy kerroksista ja valon putoamisesta, ei liukuväreistä tai korttivarjoista.
- **Lähes monokromi.** Grafiitti, titaani, huurrettu lasi. **Merkkivalon oranssi on ainoa väri**, ja sitä on yksi kohde kerrallaan.
- **Laite sankarina.** Lähikuvat materiaaleista, reunoista ja merkkivalosta; vahva siluetti; räjäytyskuva sisällöstä.
- **Tekninen tarkkuus koristeena.** Hiusviivaruudukot, mittaviivat, mono-versaali speksit (`HX-01 · ANTURI · 48 × 48 × 17 MM`), juoksevat aikaleimat.
- **Liike on paljastus.** Hidas, kontrolloitu: valo pyyhkäisee pinnan, merkkivalo syttyy. Kunnioita `prefers-reduced-motion`-asetusta.
- **Todiste rinnalla.** Kauniin kuvan vieressä aina oikea mittaus tai leikkaamaton klippi.
- **Vältä:** neonvihreää, violetti-sininen-liukuvärejä, lasimorfismia ilman syytä, emojeja ja kuvapankkiperheitä.

## Värit

| Token | Rooli |
| --- | --- |
| `--bg` `--surface` `--surface-2` `--raised` | Grafiitin neljä kerrosta. |
| `--ink` / `--muted` | Teksti ja toissijainen teksti. |
| `--line` / `--line-strong` | Hiusviivat ja ruudukot / kontrollien reunat. |
| `--titaani` | Metallin korostus: nuppi, kehyksen reuna. |
| `--merkkivalo` | **Ainoa väri.** PÄÄLLÄ / huomio. Täyttö, hehku tai piste. |
| `--vaara` | Vain todelliset hälytykset. |

Vaalea teema (paperi) on painotuotteille ja sovelluksen vaalealle tilalle.

### Tilasääntö

Tilaa ei koskaan kerrota pelkällä värillä (RT7: "kumpi väri tarkoittaa pois?"):

| Tila | Ilme | Teksti |
| --- | --- | --- |
| Päällä | `--merkkivalo` täyttö + hehku, täytetty ikoni | PÄÄLLÄ |
| Pois | `--surface-2`, ääriviivaikoni | POIS |
| Kaikki kiinni | `--ink`-valintamerkki, ei väriä | KAIKKI KIINNI |
| Ei tietoa | katkoviiva | EI TIETOA · 5 min |

## Typografia

**Geist** (otsikot 500–600, tiukka välistys −0.035…−0.045 em; leipä 400) ja **Geist Mono** (speksit versaalina +0.08 em, lukemat tabulaarisina). Molemmat OFL, palvelimella itse. Tyyliluokat: `.t-display-xl` 88/0.92, `.t-display-l` 56/0.98, `.t-heading` 28, `.t-lead` 20, `.t-body` 16, `.t-spec` 12 mono, `.t-readout` 15 mono.

## Logo

Grafiittilaatta, titaaninen nuppi osoittimella ja oranssi merkkivalo; sanamerkki "hanax" Geist SemiBold, ääriviivoina. Tiedostot `logo/`: `hanax-lockup(-on-dark).svg`, `hanax-mark(-on-dark).svg`, `hanax-wordmark(-on-dark).svg`. Suoja-alue ¼ merkin korkeudesta. Pienin koko: merkki 16 px, lockup 96 px.

## Laitteisto (konseptimallit)

Mitat ja materiaalit pohjautuvat oikeaan prototyyppiraudaan (ESP32-CAM), jotta konsepti on uskottava.

### HX-01 Anturi
- **Muoto:** pyöristetty neliö 48 × 48 × 17 mm, kulmasäde 12 mm (sama suhde kuin logossa), etupinta kevyesti kupera.
- **Materiaalit:** anodisoitu grafiittialumiini, harjattu; etuna huurrettu musta lasi.
- **Etupuoli:** 9 mm kameralinssi (musta lasi, ohut titaanirengas) hieman keskilinjan alapuolella; oikeassa yläkulmassa 3 mm merkkivalo (oranssi, valonjohde).
- **Takana:** magneetti ja 3M-tarra; mukana joustava pidike putkeen tai hanan runkoon.
- **Alareuna:** USB-C, pieni kaiverrus `HX-01`.
- **Sisällä:** ESP32-luokan moduuli kameralla (27 × 40,5 mm), akku. Lukee mekaanisen venttiilin asennon kuvasta, tai virran pistorasiasta.
- **Toimii kun:** venttiili näkyy kameralle 5–30 cm etäisyydeltä.

### HX-P Paneeli
- **Muoto:** ohut seinäpaneeli 168 × 104 × 12 mm, kulmasäde 16 mm, eteiseen silmien korkeudelle.
- **Materiaalit:** grafiittialumiinikehys, etuna tummennettu lasi; näyttö 6" matta.
- **Oikealla kyljellä:** 28 mm titaaninen **nuppi** (logon nuppi): käännä selataksesi, paina: *kaikki pois*. Nupin ympärillä ohut oranssi merkkivalorengas, joka palaa kun jokin on päällä.
- **Näyttö:** huoneet ja laitteet tilasäännön mukaan, ylhäällä "2 PÄÄLLÄ" tai "KAIKKI KIINNI".

## Kuvat ja video

Studio: musta tausta, yksi pehmeä yläsivuvalo ja kapea reunavalo; lähikuvat merkkivalosta ja nupista. Arki: oikea keittiö ja eteinen illan valossa; merkkivalo kuvan ainoa värillinen piste. Todiste: leikkaamaton ruutu- tai kamerakuva, jossa näkyy aikaleima.

## Tiedostot

`brand/tokens.json` (lähde) → `brand/tokens.css` (`uv run python brand/build_tokens.py`), `brand/fonts/`, `brand/logo/`.
