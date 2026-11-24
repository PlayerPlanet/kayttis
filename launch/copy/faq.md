# Usein kysyttyä

**Mikä Hanax on?**
Tavallinen hana. Hanax tietää, onko se auki. Hanax näyttää eteisen paneelista ja puhelimesta, jäikö hana, liesi tai valot päälle, ja voit sammuttaa kaiken yhdellä nupin painalluksella.

**Miten Hanax näkee tavallisen hanan?**
Tavallinen hana on mekaaninen venttiili ilman elektroniikkaa, joten älykotisovellukset eivät näe sitä. Hanaxin anturi katsoo venttiiliä kameralla ja lukee sen asennon kuvasta. Pistorasiaan kytketyt laitteet, kuten kahvinkeitin, luetaan virrasta.

**Mitä HX-01 ja HX-P ovat?**
Konseptimalleja. HX-01 Anturi on 48 × 48 × 17 mm kamerapala, joka kiinnittyy magneetilla tai tarralla hanan viereen. HX-P Paneeli on eteisen seinälle tarkoitettu näyttö, jossa on titaaninen nuppi: paina, ja kaikki menee pois. Kuvat niistä ovat renderöintejä, eivät valokuvia valmiista tuotteista.

**Mihin anturin mitat perustuvat?**
ESP32-CAM-moduuliin, edulliseen piirilevyyn, jossa on mikro-ohjain, wifi ja kamera. HX-01 on mitoitettu sen ympärille. Moduuli on nähtävillä loppudemossa konseptikuvien vieressä.

**Mitä prototyyppi tekee nyt?**
Killan keittiössä Raspberry Pi lukee kahden kahvinkeittimen älypistorasioita ja valoja, ja kameramalli lukee astianpesukoneen hanan venttiilin asennon. Tila näkyy livenä web-sovelluksessa. Sammuttaminen sovelluksesta on simuloitu.

**Kuvaako kamera kotiani?**
Anturi on suunniteltu katsomaan yhtä kohdetta 5–30 cm päästä, ei huonetta. Tavoitteena on, että kuva käsitellään kotona ja eteenpäin lähtee vain tila: auki tai kiinni. Prototyypissä kuva käsitellään paikallisesti Raspberry Pillä.

**Miksi kamera eikä venttiiliin asennettava anturi?**
Kamera ei koske hanaan, joten putkiasennusta ei tarvita. Asennus oli käyttäjätesteissä suurin käyttöönoton este. Kameran pitää kuitenkin nähdä venttiili.

**Voinko ostaa Hanaxin?**
Et. Hanax on Aalto-yliopiston Käyttäjälähtöinen tuotekehitysprojekti -kurssin ryhmän 1 tuotekonsepti (2026). Prototyypin tilan voi katsoa livenä loppudemossa.

**Kenelle Hanax on tehty?**
Ensisijaisesti omakotitalossa asuville, joilla on kiireinen arki ja monta laitetta muistettavana. Se sopii myös mökille ja lyhytvuokrakohteeseen. Moni testaaja hankkisi sen vanhemmilleen.

**Tarvitsenko uudet älylaitteet tai putkimiehen?**
Et. Anturi suunnitellaan kiinnitettäväksi itse olemassa olevan laitteen viereen. Itse asennusta ei ole vielä testattu oikeissa kodeissa.

**Mitä Hanax maksaa?**
Tavoitehinta on 50–150 euroa sensoreineen. Käyttäjätesteissä tätä pidettiin sopivana. Lopullista hintaa ei ole.

**Onko kuukausimaksua?**
Sitä ei ole päätetty. Tavoitteena on, että Hanax toimii myös ilman pilvipalvelua.

**Mihin tietoni tallentuvat?**
Prototyyppi lukee laitteet paikallisesti. Tavoitteena on, että Hanax toimii kotona ilman pilveä, ja jos etäkäyttöön tarvitaan palvelinta, tiedot säilytetään Suomessa.

**Miten tiedän, että tila on ajan tasalla?**
Jokaisen tilan vieressä näkyy, milloin se viimeksi tarkistettiin, esimerkiksi "KIINNI · tarkistettu 12 s sitten". Jos tietoa ei tule, Hanax näyttää "EI TIETOA" eikä arvaa.

**Mitä värit tarkoittavat?**
Oranssi on ainoa väri ja tarkoittaa päällä, kuin lieden merkkivalo. POIS näkyy ääriviivana. KAIKKI KIINNI näkyy valintamerkkinä ilman väriä. Tila lukee aina myös sanana, joten värejä ei tarvitse muistaa.

**Voinko sammuttaa kaiken kerralla?**
Konseptissa kyllä: paneelin nuppia painamalla. Sitä toivottiin testeissä. Prototyypissä toiminto on simuloitu.

**Miten Hanax eroaa älykotisovelluksista ja hälytysjärjestelmistä?**
Älykotisovellukset näkevät älylaitteet, hälytysjärjestelmät vartioivat murtoa ja paloa. Hanax vastaa yhteen kysymykseen: jäikö jotain päälle, kun lähdit. Ja se näkee tavallisen hanan.
