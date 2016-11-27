Produktų meniu puslapis
=======================

Apibrėžimas
-----------

Meniu (Grafiškai) ::

 - Kategorija (6)
   - Kategorija (3)
     - Produktas (€0.50)
     - Kategorija (2)
       - Produktas (€1.10)
       - Produktas (€6.25)
     -Kategorija (1)
       - Produktas (€3.33)
   - Kategorija (2)
     - Produktas (€1.10)
     - Produktas (€9.99)
   - Kategorija (0)
   - Kategorija (0)
 - Kategorija (1)
   - Produktas (€5.55)
   - Kategorija (0)

Taisyklės:
- Meniu yra medis
- Meniu viršutinis lygmuo yra kategorija
- Kiekviena kategorija gali turėti N vaikinių elementų
- Elementas gali būti arba kita kategorija arba produktas
- Produktas negali turėti vaikinių elementų
- Tiek produktas, tiek kategorija turi turėti `active` lauką
- Jeigu kategorijos `active` laukas yra `False`, tai nerodoma tiek kategorija,
 tiek visi jos vaikiniai elementai

Būtini produkto laukai:
- `name`
- `active`
- `price`

Būtini kategorijos laukai:
- `name`
- `active`


Užduotis
--------

Sukurti web aplikaciją:
- kuri prisijungusiems vartotojams leistų sukurti tokį meniu. Nebūtina,
 kurti kažkokį labai mandrą UI. Užtenka labai bazinio varianto.
- neprisijungusiems parodytų read-only medžio versiją (Su pavadinimais,
 kainomis, kategorijų ir produktų atitraukimu ir pan.). Puslapis turėtų
 atrodyti struktūriškai panašiai į "Meniu" sekciją.
- Prisijungusiems redagavimo srityje rodo visus produktus ir visas
 kategorijas. Neprisijungusiems tik aktyvius elementus
- Galite negaišti daug laiko autorizacijai. Jeigu Web karkasas nepateikia
 kažkokių patogių įrankių tam, tai "prisijungusius" ir "neprisijungusius"
 vartotojus galima atskirti tiesiog pagal adresus. Veiksmai daromi po
 "admin/\*" adresu yra ale prisijungusių vartotojų. O visi kiti veiksmai yra
 ale paprastų vartotojų.


Vaizdavimas
-----------

Kategorija (N): "Kategorija" yra `name` laukas. N yra produktų, esančių
kategorijos viduje, skaičius.

Produktas (€X.XX): "Produktas" yra `name` laukas.  €X.XX yra `price` laukas.


Pastabos
--------
- Naudoti PostgreSQL DB
- Naudoti Python kaip backend technologiją. Tinka bet kuris WEB karkasas.
 Django, Flask, Pyramid ir pan. Galima naudoti ir kažką kitą (Ruby, JVM, Go,
 Node.js), bet tada pateikite instrukcijas, kaip tą pasileisti Unix (OS X)
 aplinkoje
- palaikyti apie 10000 produktų. Kūrimo UI neprivalo būti intuityvus ir
 nepretenzingas, bet peržvalgos puslapis (neprisijungusiems vartotojams) turi
 nelūžti ir būti sugeneruotas per protingą laiko tarpą (kelios sekundės)
