# analyze_microscopic_pictures

Veel analyses van afbeeldingen worden nog met de hand uitgevoerd. Ook aan de Universiteit van Utrecht. Deze voert veel analyses uit op microscopie afbeeldingen van Nano deeltjes, bijvoorbeeld bij de analyse van zeolieten. Deze analyse gaat vaak nog semi-manueel, waarbij de onderzoeker met behulp van een programma de foto analyseren.
Zeolieten zijn kristallen die bestaan uit Aluminium, Silica en zuurstof. Deze kristallen kunnen worden gevonden in de natuur of gesynthetiseerd in een lab voor katalytische toepassingen. Zeolieten worden met name gebruikt bij het kraken van olie, het degraderen van plastics en het opslaan van CO2.
Na de synthese van zeolieten worden er microscopische foto’s gemaakt en geanalyseerd. Omdat de analyse manueel in een programma wordt uitgevoerd, kost dit veel tijd. Als het verder  geautomatiseerd wordt, zal dit veel tijd besparen. Daarnaast zal het automatiseren van het proces ook een uniforme analyse verzekeren. 
Het doel van het programma is ronde amorfe deeltjes in een microscopische afbeelding van zeolieten te tellen en meten.

# Functionaliteiten

Het algoritme moet aan een aantal gestelde eisen voldoen, om zijn taak goed te kunnen vervullen. Deze eisen worden in dit onderdeel beschreven.

- Een afbeelding kan ingeladen worden, zodat het algoritme het kan gebruiken.
- De cirkels in een afbeelding worden geteld en gemeten.
- Er worden geen extra cirkels geteld en gemeten. 
- Er wordt geen grote marge aan cirkels niet gevonden.
- Het uitvoeren van de berekening kost de gebruiker minder tijd dan de analyse manueel uit te voeren.
- De totale uitvoertijd van de berekening is snel genoeg om het programma bruikbaar te maken, door maximaal tien minuten te duren.
- Er is een GUI die het programma gebruiksvriendelijk maakt.
- De gebruiker kan (via de GUI) dynamisch een afbeelding inladen om te analyseren.

# Ontwerp
**algoritme**

Eerst zoekt het algoritme naar lijnen in een afbeelding.
Het algoritme berekent de grijswaarde van elke pixel. 
Het past een gaussiaans ruis onderdrukkend filter toe.
Het vindt randen met hoog verschild in grijswaarde door middel van Sobel’s edge detection.
Schakelt alle waardes die op de vector loogrecht op de rand richting geen lokaal maximum zijn, uit.
Zet alle waardes onder een onderwaarde uit. Zet alle waardes onder de bovenwaarde uit als ze niet (indirect) verbonden zijn met een pixel die dat wel is.

Daarna zoekt het algoritme door de gevonden lijnen naar cirkels van een bepaalde radius.
Het algoritme tekent een cirkel van de gegeven radius. Het aantal getekende pixels wordt opgeslagen. 
Het algoritme tekent een cirkel rond elke waarde die aan staat. 
Het algoritme zoekt naar plekken waar meer lijnen overheen zijn getekend dan 50% het aantal getekende pixels in een cirkel.
Doorzoekt de 2dimensionale lokale buurt voor het maximum.

Vervolgens doorzoekt het de 3dimensionale lokale buurt voor het bepalen van de meest passende radius.
Het maximum wordt samen met zijn radius opgeslagen.
Het aantal gevonden cirkels komt overeen met het aantal gevonden maxima en de gemiddelde diameter wordt met behulp van de zoom berekend.

**Applicatie**

Wanneer de applicatie geopend wordt, kan je afbeelding inladen. 
Nadat de gebruiker de afbeelding heeft ingeladen, vraagt de applicatie naar een aantal instellingen. 
Wanneer de instellingen zijn doorgegeven, opent de applicatie het menu waar de gebruiker het algoritme aan kan zetten.
Wanneer het algoritme klaar is, toont de applicatie de resultaten.

