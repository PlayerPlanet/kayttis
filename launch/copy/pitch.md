# Hanax: puhekäsikirjoitukset (v2)

Kaava kaikessa: **yksi väite, yksi todiste, yksi toiminto.**

- **Väite:** Tavallinen hana. Hanax tietää, onko se auki.
- **Todiste:** prototyyppi killan keittiössä. Raspberry Pi lukee kahden kahvinkeittimen älypistorasioita ja valoja, kameramalli lukee astianpesukoneen mekaanista venttiiliä (punainen teippi lisätty 24.11.), web-sovellus näyttää tilan livenä.
- **Toiminto:** Katso livenä.

Sävy: rauhallinen insinööri, ei mainosmies. Lyhyet lauseet, sinuttelu, ei pelottelua. Puhu hitaammin kuin luulet.

Rehellisyyssäännöt: HX-01 ja HX-P ovat **konseptimalleja** (sano se aina, kun näytät renderöintejä). Lukemat ovat oikeita, sammutus sovelluksesta on simuloitu. Hinta on **tavoite**. Pilvettömyys ja tietojen säilytys Suomessa ovat **tavoite**.

## 1. Hissipuhe (30 s)

> Tavallinen hana. Siinä ei ole sähköä eikä sirua, joten älykotituotteet eivät näe sitä. Hanax näkee. Pieni kamera-anturi lukee venttiilin asennon, ja eteisen paneeli ja puhelin kertovat yhdellä vilkaisulla, jäikö hana, liesi tai valot päälle. Paneelin nuppia painamalla kaikki menee pois. Laitteet ovat vielä konseptimalleja, mutta todiste toimii jo: killan keittiössä Raspberry Pi lukee kahvinkeittimiä ja valoja, ja kameramalli astianpesukoneen hanaa. Katso livenä. Lähde kotoa huoletta.

## 2. Ständipuhe (2 min)

**Väite (15 s)**
Tavallinen hana. Siinä ei ole elektroniikkaa. Silti Hanax tietää, onko se auki.

**Ongelma ja käyttäjä (25 s)**
Kaikki alkoi astianpesukoneen hanasta, joka jäi auki. Vesivahinko on kallis, eikä kotivakuutus aina korvaa sitä. Sama huoli koskee liettä, kahvinkeitintä ja valoja. Opiskelijat yksiöissä eivät innostuneet, mutta omakotitalossa asuvat, mökkien omistajat ja aikuiset lapset vanhemmilleen innostuivat. Ongelma kasvaa talon mukana.

**Todiste (35 s)**
*(Käännä näyttö kuulijaan päin.)* Tämä on killan keittiö juuri nyt. Raspberry Pi lukee kahden kahvinkeittimen älypistorasioita ja valoja. Kamera katsoo astianpesukoneen hanaa, ja malli lukee venttiilin asennon kuvasta. Laitoimme venttiiliin punaisen teipin, jotta malli näkee sen paremmin. Katso aikaleimaa: "tarkistettu 8 s sitten". Lukemat ovat oikeita. Sammutus sovelluksesta on simuloitu, koska emme halua katkaista killan kahvinkeittimiä.

**Konsepti (25 s)**
*(Osoita renderöintejä ja ESP32-CAM-moduulia pöydällä.)* Tuotteena tämä olisi kaksi laitetta. HX-01 Anturi on 48 millin kamerapala, joka kiinnittyy magneetilla hanan viereen. Sisällä on tällainen ESP32-CAM-moduuli. HX-P Paneeli on eteisessä, ja sen nuppia painamalla kaikki menee pois. Molemmat ovat konseptimalleja. Samat tiedot näkyvät puhelimessa.

**Käyttäjäpalaute (10 s)**
Testeissä kysyttiin, kumpi väri tarkoittaa pois. Siksi tila lukee aina sanana, ja kaikki kiinni on valintamerkki, ei vihreä.

**Lopetus (10 s)**
Tavoitehinta on 50–150 euroa sensoreineen. Katso livenä, kokeile nuppia. Hanax: lähde kotoa huoletta.

## 3. Esitys (4–5 min), dia kerrallaan

Roolit: `[Puhuja 1]` väite ja ongelma, `[Puhuja 2]` oivallus ja tuote, `[Puhuja 3]` todiste, toimintaperiaate ja palaute, `[Puhuja 4]` kestävyys ja hinta. Ajat ovat suuntaa antavia, yhteensä noin 4 min 40 s. Samat tekstit ovat diojen puhujamuistiinpanoissa.

### Dia 1: Tavallinen hana. Hanax tietää, onko se auki. (15 s)
**[Puhuja 1]** Hei, olemme ryhmä 1. Tavallinen hana. Siinä ei ole sähköä, ei sirua, ei sovellusta. Silti Hanax tietää, onko se auki. Kuvassa on konseptimalli: seinäpaneeli ja pieni kamera-anturi. Ja todiste on killan keittiössä juuri nyt. Tämä on Hanax.

### Dia 2: Hana jäi auki (20 s)
**[Puhuja 1]** Kaikki alkoi yhdestä hanasta. Astianpesukoneen hana jäi auki. Vesivahinko on kallis, eikä kotivakuutus aina korvaa sitä, jos syy on unohdus. Sama huoli koskee liettä, uunia, kahvinkeitintä ja valoja. Ja kun seisot ovella takki päällä, vastaus on aina sama: en tiedä. Kiireessä niitä ei ehdi kiertää tarkistamassa.

### Dia 3: Kenelle (20 s)
**[Puhuja 1]** Pilottitestissä opiskelijat yksiöissään eivät innostuneet. Ongelma kasvaa talon mukana. Kahdeksan käyttäjätestin jälkeen ensisijainen käyttäjämme on omakotitalossa asuva keski-ikäinen, jolla on kiireinen arki. Toinen ryhmä ovat mökkien omistajat ja lyhytvuokraajat. Ja yllätys: moni testaaja sanoi hankkivansa tämän vanhemmilleen. Ostaja on usein aikuinen lapsi.

### Dia 4: Oivallus (25 s)
**[Puhuja 2]** Tässä on koko idea. Tavallinen hana on mekaaninen venttiili. Siinä ei ole elektroniikkaa, joten älykotisovellus ei näe sitä lainkaan: se näkee vain älylaitteet. Testaajat kysyivät suoraan, miten tämä eroaa Google Homesta. Vastaus: Hanax ei vaadi uutta hanaa. Se katsoo venttiiliä kameralla ja lukee sen asennon kuvasta. Arkinen tehtävä, vaikea ongelma.

### Dia 5: Tuote, konseptimalli (25 s)
**[Puhuja 2]** Tuotteessa on kaksi osaa. HX-01 Anturi on 48 millin kamerapala, joka kiinnittyy magneetilla tai tarralla hanan viereen ja katsoo venttiiliä. HX-P Paneeli on eteisen seinällä. Siinä on yksi titaaninen nuppi: paina, ja kaikki menee pois. Samat tiedot näkyvät puhelimessa, kun olet jo bussissa. Huomatkaa: nämä ovat konseptimalleja, renderöityjä kuvia. Mitat on kuitenkin otettu oikeasta prototyyppiraudasta.

### Dia 6: Sisällä (20 s)
**[Puhuja 2]** Tässä anturi avattuna. Etulasi, kamera, ESP32-moduuli, akku ja magneetti. Konsepti perustuu ESP32-CAM-moduuliin, ja se on piirretty juuri tämän piirilevyn mittojen ympärille. Sama moduuli on pöydällä ständillä, joten voitte katsoa, mitä tämän kuoren sisällä oikeasti olisi.

### Dia 7: Livenä killan keittiöstä (40 s)
**[Puhuja 3]** Nyt todiste. Tämä ei ole renderöinti. Killan keittiössä Raspberry Pi lukee oikeasti kahden kahvinkeittimen älypistorasioita ja valojen tilaa. Kameramalli lukee astianpesukoneen hanan mekaanisen venttiilin asennon. Lisäsimme venttiiliin 24.11. punaisen teipin, jotta malli näkee sen paremmin. Kaikki näkyy livenä web-sovelluksessa aikaleimoineen. Rehellisyyden nimissä: lukemat ovat oikeita, mutta sammutus sovelluksesta on simuloitu. Emme halunneet katkaista killan kahvinkeittimiä kesken keiton. Ja HX-01 ja HX-P ovat konseptimalleja. Katso livenä ständillä.

### Dia 8: Näin se toimii (20 s)
**[Puhuja 3]** Käytössä kolme vaihetta. Kiinnität anturin magneetilla tai tarralla hanan viereen, niin että venttiili näkyy kameralle. Tila luetaan kotona, kuvasta tai pistorasian virrasta. Ja näet sen paneelista ja puhelimesta, aina aikaleiman kanssa: kiinni, tarkistettu 12 sekuntia sitten. Tila ilman aikaa on puolikas tieto.

### Dia 9: Rakennettu käyttäjien kanssa (35 s)
**[Puhuja 3]** Hanax muuttui jokaisen testin jälkeen. Pilottitestissä kysyttiin, kumpi väri tarkoittaa pois. Siksi tila lukee nyt aina sanana, ja oranssi on ainoa väri: päällä. Kaikki kiinni ei ole vihreä vaan valintamerkki. Moni halusi sammuttaa, ei vain katsoa: siitä tuli paneelin nuppi, paina ja kaikki pois. Kotia ei näe bussista, joten paneelin rinnalle tuli puhelinsovellus. Käyttäjätesteissä asennus pelotti, joten anturi kiinnittyy itse. Pilvi epäilytti, joten käsittely on paikallista, ja pilvettömyys on tavoitteemme.

### Dia 10: Sosiaalinen kestävyys (25 s)
**[Puhuja 4]** Sosiaalinen kestävyys. Kun liesi ja hana näkyvät yhdellä vilkaisulla, ikääntyvän on helpompi asua omassa kodissaan. Aikuinen lapsi voi sovitusti tarkistaa, että vanhempien kotona kaikki on kiinni. Toimivaa hanaa ei tarvitse vaihtaa älyhanaan, ja jokainen estetty vesivahinko säästää materiaalia ja korjaustyötä. Ja tila ei ole koskaan pelkän värin varassa: "keittiön hana", ei "sensori 3".

### Dia 11: Tavoitehinta (20 s)
**[Puhuja 4]** Tavoitteemme on 50–150 euroa sensoreineen. Se on tavoite, ei hinta. Testaajat pitivät haarukkaa sopivana, ja muutaman kympin hinta olisi saanut heidät epäilemään laatua. Itse asennus pitää kokonaiskustannuksen pienenä. Hanax on kurssikonsepti, ei myynnissä.

### Dia 12: Lähde kotoa huoletta (15 s)
**[Puhuja 1]** Tavallinen hana. Hanax tietää, onko se auki. Tulkaa ständille katsomaan livenä: killan keittiön hana, kahvinkeittimet ja valot, ja ESP32-CAM-moduuli konseptimallien vieressä. Hanax. Lähde kotoa huoletta. Kiitos.

## 4. Kysymyksiin vastaaminen

Vastaa lyhyesti, sitten hiljaa. Jos et tiedä, sano se ja kerro, mitä testit sanoivat. Erota aina, mikä toimii prototyypissä ja mikä on konseptia.

### Konsepti ja laitteet

1. **Onko HX-01 oikea laite?**
   Ei vielä. HX-01 Anturi ja HX-P Paneeli ovat konseptimalleja: renderöityjä kuvia, joiden mitat perustuvat oikeaan prototyyppirautaan. Toimiva osa on prototyyppi killan keittiössä. Ständillä on ESP32-CAM-moduuli ja raakakomponentit konseptikuvien vieressä, jotta näet, mistä anturi rakentuisi.

2. **Mikä ESP32-CAM on?**
   Edullinen, postimerkin kokoinen piirilevy (27 × 40,5 mm), jossa on mikro-ohjain, wifi ja pieni kamera. HX-01 on mitoitettu sen ympärille: 48 × 48 × 17 mm kuori, jossa on lisäksi akku, magneetti ja merkkivalo. Prototyypissä kuvaa ei vielä oteta ESP32-CAM:lla vaan killan keittiön kameralla, jota Raspberry Pi lukee.

3. **Miksi kamera eikä venttiiliin kiinnitettävä anturi?**
   Koska tavallisessa hanassa ei ole mitään, mihin kytkeytyä. Venttiiliin asennettava anturi tai sähköinen sulkuventtiili vaatii usein putkiasennuksen, ja asennus oli käyttäjätesteissä suurin este (RT8). Kamera ei koske hanaan: se katsoo venttiilin asentoa sivusta 5–30 cm päästä. Sama anturi voisi lukea myös lieden nupin tai merkkivalon. Heikkous on, että venttiilin pitää näkyä kameralle, ja valaistus vaikuttaa. Siksi lisäsimme prototyypin venttiiliin punaisen teipin.

4. **Kuvaako kamera kotiani?**
   Anturi on suunniteltu katsomaan yhtä kohdetta läheltä, ei huonetta. Tavoitteena on, että kuva käsitellään kotona ja eteenpäin lähtee vain tila: auki tai kiinni. Prototyypissä kuva käsitellään Raspberry Pillä keittiössä, ja hanaluokittelija katsoo vain hanan kohdalta rajattua aluetta. Pilvettömyys on tavoite, ei vielä valmis ominaisuus.

5. **Kuinka tarkka kameramalli on?**
   Prototyyppitasolla. Malli on opetettu killan keittiön kuvilla, mutta kaikki kiinni-esimerkit ovat yhdeltä noin kolmen tunnin jaksolta, joten aineisto on suppea. Siksi jokaisen tilan vieressä on aikaleima, ja jos malli ei näe venttiiliä, Hanax sanoo "EI TIETOA" eikä arvaa.

6. **Miten anturi saa virtaa?**
   Konseptissa akulla ja USB-C:llä. Akun kestoa emme ole mitanneet, joten emme lupaa sitä.

### Tuote ja käyttö

7. **Miten Hanax eroaa Google Homesta tai muista älykotisovelluksista?**
   Ne näkevät älylaitteet. Tavallinen hana on mekaaninen venttiili ilman elektroniikkaa, joten ne eivät näe sitä. Hanax lukee sen kameralla ja tuo hanan, lieden ja pistorasiat samaan näkymään.

8. **Entä Verisure tai muut hälytysjärjestelmät?**
   Ne vartioivat murtoa ja paloa. Hanax vastaa aiempaan kysymykseen: jäikö jotain päälle, kun lähdit.

9. **Mitä prototyyppi oikeasti tekee?**
   Raspberry Pi lukee killan keittiössä kahden kahvinkeittimen älypistorasioita ja valoja, ja kameramalli lukee astianpesukoneen hanan venttiilin asennon. Tila näkyy livenä web-sovelluksessa. Sammuttaminen sovelluksesta ja kaikki pois -nuppi ovat simuloituja.

10. **Mitä värit tarkoittavat?**
    Oranssi on ainoa väri, ja se tarkoittaa päällä, kuin lieden merkkivalo. Kaikki kiinni on valintamerkki, ei vihreää. Tila lukee aina myös sanana. Tämä tuli suoraan pilottitestistä, jossa kysyttiin, kumpi väri tarkoittaa pois.

11. **Mihin tietoni menevät?**
    Prototyypissä tila luetaan paikallisesti Raspberry Pillä. Tavoitteena on, että Hanax toimii ilman pilveä, ja jos etäkäyttöön tarvitaan palvelin, tiedot säilytetään Suomessa. Kumpikin on tavoite.

12. **Voiko kämppis tai puoliso vakoilla minua tällä?**
    Hanax näyttää laitteiden tilan, ei ihmisiä. Pilottitestissä tämä kysyttiin, joten suunnittelemme, että näkymään pääsevät vain kodin asukkaat ja ne läheiset, joista on yhdessä sovittu.

13. **Pitääkö asennukseen tilata putkimies?**
    Ei pitäisi. Anturi on suunniteltu kiinnitettäväksi magneetilla tai tarralla hanan viereen. Tätä ei ole vielä testattu oikeissa kodeissa.

14. **Paljonko se maksaa? Onko kuukausimaksu?**
    Tavoitehinta on 50–150 euroa sensoreineen, ja testaajat pitivät sitä sopivana. Kuukausimaksusta ei ole päätetty. Hanax on kurssikonsepti, ei myynnissä.

15. **Miksen vain muista itse?**
    Muistat useimmiten. Hanax on niitä aamuja varten, kun bussi lähtee neljän minuutin päästä, ja niitä hetkiä, kun olet jo matkalla ja epäilys herää.

16. **Miten sosiaalinen kestävyys näkyy?**
    Ikääntyvä voi asua kotona turvallisemmin, läheisillä on rauhallisempi mieli, toimivaa hanaa ei tarvitse vaihtaa, ja käyttöliittymä on selkeä myös ilman värinäköä.

17. **Toimiiko se mökillä tai vuokra-asunnossa?**
    Konseptina kyllä, ja testeissä tämä nousi esiin. Mökille ei palata heti, joten päälle jäänyt laite on siellä isompi asia. Vaihtuville vieraille eteisen paneeli sopii paremmin kuin sovellus.
