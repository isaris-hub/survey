# SurveyPro

SurveyPro is een eenvoudige Django-applicatie voor het maken en beheren van enquêtes.

## Functies
- Beheer enquêtes via de webinterface.
- Ondersteuning voor open vragen, meerkeuzevragen en schaalvragen.
- Verstuur uitnodigingen met unieke links voor respondenten.
- Verzamel en bekijk antwoorden, exporteer resultaten naar CSV.

## Installatie
1. Maak en activeer een virtuele omgeving: `python -m venv .venv && source .venv/bin/activate`.
2. Installeer afhankelijkheden met `pip install -r requirements.txt`.
3. Voer migraties uit met `python manage.py migrate`.
4. Voeg superuser toe met `python manage.py createsuperuser`.
5. Voeg een test enquete toe met `python manage.py seed_data`.

## Gebruik
Start de ontwikkelserver met:
```bash
python manage.py runserver
```
Bezoek vervolgens [http://localhost:8000](http://localhost:8000) om in te loggen en enquêtes te beheren.

## Tests
Voer de tests uit met:
```bash
python manage.py test
```

