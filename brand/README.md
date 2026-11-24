# Hanax

**Lähde kotoa huoletta.** Hanax näyttää yhdellä vilkaisulla, jäikö hana, liesi tai valot päälle: eteisen paneelista ja puhelimesta.

Hanax syntyi yhdestä arkisesta pelosta: astianpesukoneen hana jäi auki. Vesivahinko on kallis, eikä kotivakuutus aina korvaa sitä. Tutkiessamme ongelmaa huomasimme, että sama huoli koskee liettä, uunia, kahvinkeitintä ja valoja. Nimi tulee hanasta, josta kaikki alkoi.

Hanax on Aalto-yliopiston käytettävyyskurssin ryhmän 1 tuotekonsepti (2026). Tämä brändikirja on kaikkien materiaalien lähde: video, laskeutumissivu, julisteet, sovellus ja some.

## Kenelle

- **Ensisijainen:** omakotitalossa asuvat keski-ikäiset, joilla on kiireinen arki. Talossa on monta kerrosta ja monta laitetta, ja kotoa lähtiessä on muistettava paljon.
- **Toissijainen:** mökkien omistajat ja lyhytvuokraajat (Airbnb), joilla kohde on pitkään tyhjillään.
- **Ostajana usein lapsi**, joka hankkii Hanaxin vanhemmilleen.

## Mitä lupaamme

| Ydinviesti | Perustelu käyttäjätesteistä |
| --- | --- |
| Näet kaiken yhdellä vilkaisulla. | Testihenkilöt ymmärsivät paneelin heti ilman ohjeita (RT7). |
| Toimii laitteiden kanssa, jotka sinulla jo on. | Sensorit kiinnittyvät tavalliseen hanaan, lieteen tai pistorasiaan; uusia älylaitteita ei tarvita (RT8). |
| Asennat itse, ilman putkimiestä. | Hankala tai maksullinen asennus oli suurin käyttöönoton este (RT8). |
| Kotisi tiedot pysyvät kotona. | Toimii paikallisesti ilman pilveä; tiedot säilytetään Suomessa (RT8). |
| Yksi painike: kaikki pois. | Testeissä toivottiin yhtä katkaisijaa, josta kaiken saa pois (RT7). |

**Älä lupaa** vakuutusalennuksia, sertifikaatteja, valmista hintaa tai toimitusaikaa. Hintahaarukka, jota testihenkilöt pitivät sopivana: 50–150 € sensoreineen. Puhu siitä "tavoitteena", ei hintana.

## Ääni ja sävy

Hanax puhuu kuin rauhallinen naapuri, joka tietää talotekniikasta: konkreettisesti, lyhyesti, ilman pelottelua.

- **Rauhoita, älä pelottele.** Kerro mitä tapahtui ja mitä voit tehdä. ✅ "Liesi jäi päälle. Sammuta se täältä." ❌ "VAARA! Talosi voi palaa!"
- **Puhuttele sinuksi.** "Näet", "lähdet", "sammutat".
- **Nimeä asiat niin kuin ihminen ne nimeää.** "Keittiön hana", ei "sensori #3".
- **Lyhyet lauseet.** Yksi asia lauseessa. Ei huutomerkkejä, ei emojeja.
- **Kerro tuoreus.** Tila ilman aikaa on puolikas tieto: "Kiinni · tarkistettu 12 s sitten".

## Värit

Paletti tulee kodinkoneen paneelista: yönsininen kuori, vesi ja merkkivalo.

| Token | Rooli |
| --- | --- |
| `--ink` / `--bg` | Yönsininen ja vihertävä valkoinen. Pohja kaikelle. |
| `--vesi` | Brändiväri: linkit, ensisijaiset painikkeet. |
| `--merkkivalo` | **Päällä / huomio.** Kuin lieden merkkivalo. Vain täyttönä, tekstinä `--merkkivalo-ink`. |
| `--kiinni` | **Kaikki kiinni / turvassa.** |
| `--vaara` | Vain hälytykset (vuoto, yhteys katki). |

### Tilasääntö (tärkein sääntö)

Käyttäjätesteissä kysyttiin, kumpi väri tarkoittaa "pois päältä". Siksi tilaa ei koskaan kerrota pelkällä värillä:

| Tila | Väri | Teksti | Ikoni |
| --- | --- | --- | --- |
| Päällä | `--merkkivalo` täyttö | PÄÄLLÄ | täytetty ikoni + merkkivalopallo |
| Pois | `--surface-2`, `--muted` | POIS | ääriviivaikoni |
| Kaikki kiinni | `--kiinni` | KAIKKI KIINNI | valintamerkki |
| Ei tietoa | `--surface-2` katkoviivalla | EI TIETOA · 5 min | kysymysmerkki |

Päällä on oranssi, ei vihreä: vihreä tarkoittaa Hanaxissa aina "turvassa".

## Typografia

- **Familjen Grotesk** (näyttö, 600–700): otsikot ja iskulauseet. Tiivis, pohjoismainen groteski.
- **Figtree** (leipä, 400–600): kaikki muu teksti.
- **JetBrains Mono** (lukemat, 500): kellonajat, watit, aikaleimat. Tabulaariset numerot.

Tyyliluokat: `.t-display-xl` 72/0.95, `.t-display-l` 48/1.0, `.t-heading` 28/1.15, `.t-lead` 20/1.5, `.t-body` 16/1.55, `.t-label` 13 versaali +0.06em, `.t-readout` 15 mono. Fontit ovat OFL-lisensoituja ja palvelimella itse (`brand/fonts/`), ei Google-pyyntöjä.

## Logo

- **Merkki:** pyöristetty neliö (laitepaneeli), nuppi osoittimella ja oranssi merkkivalo. Se kysyy saman kuin tuote: onko jokin päällä?
- **Sanamerkki:** "hanax" gemenoin, Familjen Grotesk Bold, ääriviivoina.
- Tiedostot: `logo/hanax-lockup.svg`, `hanax-lockup-on-dark.svg`, `hanax-mark.svg`, `hanax-mark-on-dark.svg`, `hanax-wordmark.svg`.
- **Suoja-alue:** merkin kulmasäteen verran (¼ merkin korkeudesta) joka puolella.
- **Pienin koko:** merkki 16 px, lockup 96 px leveä.
- **Älä** venytä, kierrä, vaihda merkkivalon väriä tai sijoita kuvan päälle ilman tasaista pohjaa.

## Muodot ja tila

Kulmat `--radius-l` (20 px) vastaa logon kulmaa. Pyöreät painikkeet ovat nuppeja (`--radius-pill`). Kortit erottuvat pinnan värillä, ei varjolla; `--shadow-panel` vain kelluville elementeille. Väli 8 px:n askelin (`--space-*`).

## Kuvat ja video

Oikea koti ja oikea arki: eteinen, keittiön hana, lieden merkkivalo, kiire bussiin. Ei kuvapankkiperheitä. Lähikuvat laitteista, joissa merkkivalo näkyy. Värimäärittely viileä ja luonnollinen.

## Tiedostot

`brand/tokens.json` (lähde) → `brand/tokens.css` (`uv run python brand/build_tokens.py`), `brand/fonts/`, `brand/logo/`.
