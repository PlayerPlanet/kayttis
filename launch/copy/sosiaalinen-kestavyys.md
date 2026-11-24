# Hanax ja sosiaalinen kestävyys

Lyhyesti: Hanax vähentää kotiin liittyvää huolta, auttaa ihmisiä asumaan kotonaan turvallisemmin ja toimii laitteiden kanssa, jotka kotona jo on. Tavallista hanaa ei tarvitse vaihtaa älyhanaan, asennukseen ei tarvita putkimiestä, ja tavoitteena on, ettei kodin tieto lähde kotoa.

Jokaisen perustelun alla kerrotaan, mihin se nojaa: **Mistä tiedämme** viittaa omiin testeihimme (RT7 = pilottitesti, RT8 = käyttäjätesti, 8 henkilöä) tai toimivaan prototyyppiin. **Oletus** tarkoittaa perusteltua päättelyä, jota emme ole vielä testanneet. HX-01 Anturi ja HX-P Paneeli ovat **konseptimalleja**.

## 1. Ikääntyvä asuu kotonaan turvallisemmin

Liesi ja hana ovat laitteita, jotka jäävät päälle harvoin mutta joista voi seurata paljon. Kun niiden tila näkyy eteisen paneelista yhdellä vilkaisulla, kotona asuminen on turvallisempaa myös silloin, kun muisti ei ole entisensä.

- **Mistä tiedämme:** Testaajat pitivät liettä ja isoja kodinkoneita kriittisimpinä laitteina (RT7). Mukana oli 76- ja 80-vuotias testihenkilö, jotka asuvat omassa kodissaan (RT8).
- **Oletus:** Hanax tukee ikääntyvien kotona asumista. Emme ole testanneet tätä muistisairaiden kanssa.

## 2. Läheisten mielenrauha

Moni aikuinen huolehtii vanhempiensa kodista. Hanax antaa tavan tarkistaa puhelimesta, että kaikki on kiinni, ilman että tarvitsee soittaa ja kysyä.

- **Mistä tiedämme:** Useat testaajat kertoivat hankkivansa laitteen vanhemmilleen (RT7). Testeissä mainittiin myös isovanhempien ja yksin kotona olevien lasten laitteiden seuranta (RT7).
- **Oletus:** Seuranta tapahtuu sovitusti. Pilottitestissä kysyttiin, voiko kämppis vakoilla toista, joten näkymä näyttää laitteet, ei ihmisiä, ja pääsystä sovitaan yhdessä.

## 3. Vähemmän vesivahinkoja ja hukkaa

Estetty vesivahinko säästää rakennusmateriaalia, purku- ja korjaustyötä sekä kuivatukseen kuluvaa energiaa. Se säästää myös asukkaan väliaikaisen muuton ja arjen katkon.

- **Mistä tiedämme:** Koko konsepti lähti astianpesukoneen auki jääneestä hanasta ja siitä, ettei kotivakuutus aina korvaa vahinkoa (RT7). Prototyyppi lukee jo oikean astianpesukoneen hanan venttiiliä killan keittiössä.
- **Oletus:** Hanax vähentää vahinkoja. Vaikutusta ei voi mitata ennen kuin tuotetta käytetään oikeissa kodeissa.

## 4. Toimivia laitteita ei vaihdeta

Hanaxin oivallus on, että tavallinen hana on mekaaninen venttiili ilman elektroniikkaa. Sen sijaan, että hana vaihdettaisiin älyhanaan tai sulkuventtiiliin, anturi katsoo sitä kameralla. Toimiva hana, liesi ja kahvinkeitin saavat jäädä paikalleen.

- **Mistä tiedämme:** Prototyypin kameramalli lukee killan keittiön mekaanista venttiiliä ilman, että hanaan on koskettu. Asennuksen vaivattomuus oli testaajille tärkeää (RT8).
- **Oletus:** Yksi anturi kuluttaa vähemmän materiaalia kuin laitteiden vaihtaminen älyversioihin. Emme ole tehneet elinkaarilaskelmaa.

## 5. Energiansäästö

Kun näet, että valot tai kahvinkeitin jäivät päälle, sammutat ne. Pörssisähköllä tällä on suora merkitys kotitalouden menoihin.

- **Mistä tiedämme:** Useampi testihenkilö seuraa sähkön hintaa pörssisähkön takia tai haluaa säästää sähköä, ja sähkönkulutuksen näyttämistä toivottiin (RT8). Prototyyppi lukee kahvinkeittimien älypistorasioita.
- **Oletus:** Säästön suuruus riippuu kodista. Emme lupaa euromääriä.

## 6. Yksityisyys ja tietojen omistajuus

Kodin laitteiden käyttö kertoo paljon asukkaiden arjesta, ja kamera kotona herättää perustellusti kysymyksiä. Siksi HX-01 on suunniteltu katsomaan yhtä kohdetta läheltä (5–30 cm), ei huonetta, ja tavoitteena on, että kuva käsitellään kotona ja eteenpäin lähtee vain tila: auki tai kiinni. Tavoitteena on myös, että Hanax toimii ilman pilveä ja tarvittavat tiedot säilytetään Suomessa. Paikallinen tila tarkoittaa, että laite toimii, vaikka palvelu joskus lakkaisi.

- **Mistä tiedämme:** Testaajat kysyivät pilvestä, tietoturvasta ja palvelun jatkuvuudesta ja toivoivat ulkoverkosta riippumatonta tilaa (RT8).
- **Prototyypissä:** Raspberry Pi lukee laitteet paikallisesti killan keittiössä, ja hanaluokittelija katsoo vain hanan kohdalta rajattua aluetta kuvasta.
- **Tavoite:** pilvettömyys, Suomi-säilytys ja kuvan käsittely anturissa. Näitä ei ole vielä toteutettu.

## 7. Saavutettava käyttöliittymä

Tila ei ole koskaan pelkän värin varassa. Oranssi on ainoa väri ja tarkoittaa päällä. POIS näkyy ääriviivana, KAIKKI KIINNI valintamerkkinä ilman väriä, ja EI TIETOA katkoviivana. Kaikki lukevat aina myös sanoina. Laitteet nimetään niin kuin ihminen ne nimeää: "keittiön hana", ei "sensori #3". Tämä auttaa värisokeita, ikääntyviä ja ketä tahansa kiireessä.

- **Mistä tiedämme:** Pilottitestissä kysyttiin, kumpi väreistä tarkoittaa pois päältä (RT7). Siksi luovuimme vihreästä "kaikki kiinni" -tilana. Testihenkilöt ymmärsivät näkymän ilman ohjeita (RT7, RT8).

## 8. Itse asennus laskee kynnystä

Kun putkimiestä tai sähkömiestä ei tarvita, Hanax on mahdollinen myös niille, joilla ei ole varaa tai halua tilata asentajaa. HX-01 kiinnittyy magneetilla tai tarralla, ja sen mukana on joustava pidike putkeen tai hanan runkoon.

- **Mistä tiedämme:** Hankala ja maksullinen asennus oli yksi suurimmista käyttöönoton esteistä (RT8). Tavoitehinta 50–150 € sensoreineen koettiin sopivaksi (RT8).
- **Oletus:** Asennus onnistuu ilman työkaluja. Tätä ei ole vielä testattu, koska HX-01 on konseptimalli.

## Mitä emme väitä

Emme väitä Hanaxin estävän tulipaloja tai vahinkoja varmasti, emme lupaa vakuutusetuja emmekä anna lukuja säästöistä. HX-01 ja HX-P ovat konseptimalleja, ja Hanax on kurssikonsepti. Sen vaikutukset näkyisivät vasta oikeassa käytössä.
