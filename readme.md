# Kod Źródłowy Projektu - Python + Flask

<br>

## System do udostępniania sal konferencyjnych
<br><br>
### Informatyka Katowice Grupa 2 Sekcja 5
### Skład sekcji: 
* Daniel Świetlik (Przedstawiciel)
* Bartosz Padkowski
* Jan Słowik
* Cezary Szumerowski
* Kamil Tlałka
* Piotr Jankowski

### Wykorzystane technologie
* Python 3.8
* Flask
* SQLAlchemy
* SQLite3
* HTML, CSS, JavaScript, JQuery, Bootstrap
* Docker

### Struktura Projektu:
* run.py - plik uruchamiajacy serwer flask
* config.py - plik z ustawieniami aplikacji
* source/WarstwaPrezentacji/ - katalog z kontrolerami widoków oraz szablony html i model aplikacji
* source/WarstwaBiznesowa/ - katalog z kontrolerami dostepu do bazy danych i modelami dla warswty biznesowej oraz systemu mailingowego
* source/BazaDanych/ - katalog z obiektem tworzącym połączenie z Bazą Danych oraz modele ORM tabel do bazy danych
* Dockerfile - jeśli wygodniej jest skorzystać z dockera, to jest to plik do utworzenia kontenera. "Uruchamia samą aplikację bez testów"

```commandline
# Uruchomienie serwera flask
python run.py

# uruchamienie testów jednostkowych
python run.py --run-tests 
```
```commandline
# tworzenie wirtualnego środowiska bez pycharma
python -m venv `nazwa`

# uruchomienie go
source `nazwa`/bin/activate

# wyjscie ze srodowiska
deactivate
```
```commandline
# instalacja frameworkow, najlepiej zrobić dodatkowy virtual environment jak powyżej
pip install -r requirements.txt 
```
### Docker mini How-To
Przed użyciem komend trzeba uruchomić daemona Docker'a
```commandline
# Tworzenie image do kontenera
# Bedac w katalogu z Dockerfile

docker build -t `nazwa` .
```
```commandline
# Uruchomienie kontenera
docker run -d -p 7675:7675 `nazwa`
```
```commandline
# Logi z konsoli kontenera
docker logs `nazwa`
```
```commandline
# Zatrzymanie kontenera
docker stop `nazwa`
```
```commandline
# Usuniecie kontenera
docker image rm `nazwa`
```