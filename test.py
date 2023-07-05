import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
from datetime import datetime
import os

def get_fuel_prices(url):
    # Senden einer GET-Anfrage an die Webseite
    response = requests.get(url)

    # Überprüfung, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        # HTML-Inhalt der Webseite extrahieren
        soup = BeautifulSoup(response.content, 'html.parser')

        # Finde alle Elemente, die den Spritpreis enthalten
        fuel_price_elements = soup.find_all('div', class_='price-text price text-color-ct-blue')
        # Finde alle Elemente, die den Namen der Tankstelle enthalten
        station_name_elements = soup.find_all('span', class_='fuel-station-location-name')
        street_elements = soup.find_all('div', class_='fuel-station-location-street')
        city_plz_elements = soup.find_all('div', class_='fuel-station-location-city')
        # Extrahiere die Preise aus den Elementen
        fuel_prices = [element.text.strip() for element in fuel_price_elements]
        station_names = [element.text.strip() for element in station_name_elements]
        street_names = [element.text.strip() for element in street_elements]
        city_plz_names = [element.text.strip() for element in city_plz_elements]

        return fuel_prices, station_names, street_names, city_plz_names

    else:
        print("Fehler beim Abrufen der Webseite.")
        return None

# Liste der Regionen
regions = ['76135+Karlsruhe%2FBeiertheim', '76829+Landau+in+der+Pfalz', '67433+Neustadt+an+der+Weinstraße&spritsorte']

# URL-Format für die Spritpreis-Webseite
url_format = f"https://www.clever-tanken.de/tankstelle_liste?lat=&lon=&ort={{region}}&spritsorte=5&r=5"

# for region in regions:
#     # URL für die aktuelle Region erstellen
#     url = url_format.format(region=region)
#     print(url)
#     # Abrufen der Spritpreise für die aktuelle Region
#     prices,names = get_fuel_prices(url)
#
#     if prices and names:
#         print(f"Aktuelle Spritpreise in {region}:")
#         for i, (price,name) in enumerate(zip(prices,names)):
#             print(f"Tankstelle {i+1}: {name} - Preis: {price}")
#         print()
#     else:
#         print(f"Fehler beim Abrufen der Spritpreise für {region}.")


current_date = date.today().strftime("%Y-%m-%d")
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
current_month = date.today().strftime("%Y-%m")
print(current_month)
# Name der CSV-Datei mit Datum
csv_file = f"spritpreise_{current_month}.csv"
print (csv_file)

csv_exists = os.path.isfile(csv_file)

# CSV-Datei öffnen und als Schreibmodus speichern
# with open(csv_file, 'a', newline='',encoding='utf-8-sig') as file:
#     writer = csv.writer(file)
#     # Schreiben der Spaltenüberschrift in die CSV-Datei (nur einmal für jede Region)
#     for region in regions:
#         # URL für die aktuelle Region erstellen
#         url = url_format.format(region=region)
#
#         # Abrufen der Spritpreise und Tankstellennamen für die aktuelle Region
#         prices, names , streets, plz_city = get_fuel_prices(url)
#
#         if prices and names and streets and plz_city:
#             if not csv_exists:
#                 # Schreiben der Spaltenüberschrift in die CSV-Datei (nur einmal, wenn die Datei neu erstellt wird)
#                 writer.writerow(["Uhrzeit","Datum","Region","Strasse","Ort_PLZ","Tankstelle","Preis"])
#                 csv_exists = True
#
#             for i, (price, name,street,plz) in enumerate(zip(prices, names, streets, plz_city)):
#                 # Schreiben der Daten in die CSV-Datei
#                 writer.writerow([current_datetime, current_date, region,street,plz, name, price])
#
#     print(f"Die Spritpreise wurden erfolgreich in die CSV-Datei '{csv_file}' gespeichert.")