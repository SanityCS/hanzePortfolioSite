# hanzePortfolioSite
 
## Belangrijk!
Zorg ervoor dat alle requirements vanuit de requirements.txt zijn geïnstalleerd, zonder veel van deze packages werkt de website niet hoe hij moet werken

## Inloggegevens
admin account:
    * Username : admin
    * Password : d&QAzB&P@3LM2hDpGfwJhR4E%zG*E9

fake account (om te laten zien dat je alleen posts aan kan maken als admin):
    * Username : nietadmin
    * Password : 1234

# Functionaliteiten

De website runt volledig op python, naast 1 simpel JavaScript blokje. Dit JavaScript blokje is ervoor gemaakt zodat de flash messages van flask verdwijnen na 3 seconden.

De website heeft een database met 2 tabellen, deze database runt op sqlite3

# Installatie

* Installeer alle requirements uit requirements.txt

* Omdat de website tailwind gebruikt is er geen specifiek CSS document waar alle styles in staan, de styles zijn allemaal direct in het HTML document geïntegreerd. Als het goed is er daarom ook geen installatie van tailwind of andere frameworks nodig. Het zou vanaf de download direct moeten runnen.

* Om alle functionaliteiten te laten werken is het belangrijk om een .env file aan te maken genaamt .env (de naam is volledig leeg). 

* Voer in dit bestand de volgende key in: app_key=ea579ce9def1ffca2d3dfd78a6aa9c9760b270950268405b

main.py runt de Flask server
Voer deze uit met het commando:
```bash
py .\main.py
```
init_db.py initializeerd de database
Voer deze uit met het commando:
```bash
py .\init_db.py
```

