# Lehdistötiedote

*Julkaisuvapaa [päivämäärä]*

## Tavallinen hana. Hanax tietää, onko se auki.

**Aalto-yliopiston Käyttäjälähtöinen tuotekehitysprojekti -kurssin opiskelijat esittelevät Hanaxin, tuotekonseptin, joka kertoo eteisen paneelista ja puhelimesta, jäikö hana, liesi tai valot päälle. Tavallisessa hanassa ei ole elektroniikkaa, joten älykotituotteet eivät näe sitä. Hanax lukee venttiilin asennon kameralla. Konseptin toimiva prototyyppi lukee jo oikeita laitteita kiltahuoneen keittiössä, ja sen tilan voi katsoa livenä.**

Hanax syntyi yhdestä arkisesta huolesta: astianpesukoneen hana jäi auki. Vesivahinko on kallis, eikä kotivakuutus aina korvaa sitä, jos syy on unohdus. Ongelmaa tutkiessaan ryhmä huomasi, että sama huoli koskee liettä, uunia, kahvinkeitintä ja valoja. Kiireessä niitä ei ehdi kiertää tarkistamassa.

Ratkaisun ydin on havainto: tavallinen hana on mekaaninen venttiili ilman elektroniikkaa. Älykotisovellukset näkevät vain älylaitteet. Hanaxin anturi ei koske hanaan, vaan katsoo venttiiliä kameralla ja päättelee sen asennon kuvasta.

### Todiste: prototyyppi killan keittiössä

Prototyypissä Raspberry Pi -tietokone lukee kiltahuoneen keittiössä kahden kahvinkeittimen älypistorasioita ja valojen tilaa. Kameramalli lukee astianpesukoneen hanan mekaanisen venttiilin asennon; venttiiliin lisättiin 24.11. punainen teippi, jotta malli erottaa sen paremmin. Tilat näkyvät web-sovelluksessa livenä, ja jokaisen tilan vieressä näkyy, milloin se on viimeksi tarkistettu. Laitteiden sammuttaminen sovelluksesta on prototyypissä simuloitu: sovellus lukee oikeita laitteita mutta ei ohjaa niitä.

### Konsepti: HX-01 Anturi ja HX-P Paneeli

Tuotteeksi ryhmä on suunnitellut kaksi laitetta, jotka ovat **konseptimalleja**, eivät valmiita tuotteita. HX-01 Anturi on 48 × 48 × 17 mm kamerapala, joka kiinnittyy magneetilla tai tarralla hanan viereen. Sen mitat perustuvat ESP32-CAM-moduuliin, jonka ryhmä tuo loppudemoon nähtäväksi. HX-P Paneeli on eteisen seinälle tarkoitettu näyttö, jossa on yksi titaaninen nuppi: painamalla kaiken saa pois. Samat tiedot näkyvät puhelinsovelluksessa.

### Rakennettu käyttäjien kanssa

Konsepti muuttui pilottitestin ja kahdeksan käyttäjätestin myötä. Pilottitestissä kysyttiin, kumpi väri tarkoittaa "pois päältä", joten Hanax ei koskaan kerro tilaa pelkällä värillä: oranssi on ainoa väri ja tarkoittaa päällä, ja "kaikki kiinni" näytetään valintamerkillä. Testaajat halusivat sammuttaa laitteita, eivät vain katsoa niitä, ja tarkistaa kodin myös bussista, joten paneelin rinnalle tuli puhelinsovellus. Käyttäjätesteissä 30–80-vuotiaat omistusasujat Helsingistä, Espoosta, Vantaalta ja Oulusta pitivät suurimpana esteenä hankalaa asennusta ja epäilivät pilvipalveluja. Siksi anturi suunnitellaan itse kiinnitettäväksi, ja tavoitteena on, että Hanax toimii paikallisesti ilman pilveä ja tarvittavat tiedot säilytetään Suomessa.

Ensisijainen käyttäjäryhmä ovat omakotitalossa asuvat keski-ikäiset, joilla on kiireinen arki. Hanaxista kiinnostuivat myös mökkien omistajat ja lyhytvuokraajat, ja moni testaaja kertoi, että hankkisi sen ikääntyville vanhemmilleen.

Tavoitehinta on 50–150 euroa sensoreineen. Käyttäjätesteissä tätä haarukkaa pidettiin sopivana.

Hanax esitellään kurssin loppudemossa [päivämäärä ja paikka]. Ständillä voi katsoa killan keittiön tilan livenä ja nähdä ESP32-CAM-moduulin konseptimallien vieressä.

### Tietoa Hanaxista

Hanax on Aalto-yliopiston Käyttäjälähtöinen tuotekehitysprojekti -kurssin ryhmän 1 tuotekonsepti (2026). Se ei ole kaupallinen tuote, eikä sitä ole myynnissä. HX-01 ja HX-P ovat konseptimalleja, ja kuvat niistä ovat renderöintejä. Hinta on tavoite, ei vahvistettu hinta. Pilvettömyys ja tietojen säilytys Suomessa ovat tavoitteita.

**Lisätietoja:**
[yhteyshenkilö]
[sähköposti]
kayttis.kiirikki.fi
