# Hanax: laitteiston renderöinnit

**Nämä ovat konseptimalleja (konseptimallit), eivät valmiita tuotteita.** HX-01 ja HX-P ovat kurssiprojektin konsepteja. Mitat ja materiaalit noudattavat `brand/README.md`:n osiota "Laitteisto (konseptimallit)".

Kaikki kuvat on tuotettu proseduraalisesti three.js:llä (0.160.0) headless Chromessa. Lähdekoodi on kansiossa `brand/renders-src/` (`npm install`, sitten `node render.mjs`; videot: `node render.mjs --video hx01-turntable hxp-reveal`).

| Tiedosto | Koko | Sisältö |
|---|---|---|
| `hx01-hero.png` | 2400×1600 | HX-01 Anturi 3/4-kuvakulmasta, merkkivalo palaa |
| `hx01-front.png` | 2400×1600 | HX-01 suoraan edestä |
| `hx01-front-callouts.png` | 2400×1600 | Sama, mittaviivat ja merkinnät (48 MM, KAMERA Ø 9 MM, MERKKIVALO, HX-01) |
| `hx01-exploded.png` | 2400×1600 | Räjäytyskuva syvyysakselilla: ETULASI, KAMERA, ESP32-MODUULI, AKKU, MAGNEETTI |
| `hx01-macro-led.png` | 2400×1600 | Lähikuva oikeasta yläkulmasta: merkkivalo ja harjattu alumiini |
| `hx01-cutout.png` | 1600×1600 | HX-01 läpinäkyvällä taustalla (alfa) |
| `hxp-hero.png` | 2400×1600 | HX-P Paneeli seinällä 3/4-kuvakulmasta, näyttö ja valorengas päällä |
| `hxp-front.png` | 2400×1600 | HX-P suoraan edestä, käyttöliittymä luettavissa |
| `hxp-knob-macro.png` | 2400×1600 | Lähikuva titaaninupista: pyällys, osoitinura, oranssi rengas |
| `hxp-cutout.png` | 2000×1400 | HX-P läpinäkyvällä taustalla (alfa) |
| `family.png` | 2400×1600 | Molemmat laitteet yhdessä, oikeassa mittasuhteessa |
| `hx01-turntable.mp4` | 1920×1080, 6 s | Saumaton silmukka, 30° edestakainen kierto |
| `hxp-reveal.mp4` | 1920×1080, 5 s | Näyttö syttyy mustasta, valopyyhkäisy, valorengas syttyy |

Mitat mallissa (mm): HX-01 48 × 48 × 17, kulmasäde 12, kamera Ø 9, merkkivalo Ø 3. HX-P 168 × 104 × 12, kulmasäde 16, nuppi Ø 28 ja 10 mm ulkonema. Merkkivalon väri `#ff9a2e` on kuvien ainoa väri.
