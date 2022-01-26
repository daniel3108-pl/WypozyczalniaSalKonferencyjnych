
## System do udostępniania sal konferencyjnych
<br><br>


## Krótki opis projektu

Projekt był wykonywany w ramach kursu Inżynierii Oprogramowania na Politechnice Śląskiej. <br>
Zadaniem było: stworzyć aplikację zajmującą się udostępnianiem sal konferencyjnych użytkownikom.
<br>
System został podzielony na dwa interfejsy dla Konta wynajmującego własne sale i dla tego konta, które rezerwuje salę od wynajmujących.
Projekt jest względnie uproszczoną wersją aplikacji tego typu żeby dostosować to uczelnianych warunków i ograniczonego czasu, także
nie wszystko zostało zaimplementowane co mogło być a także część kodu zawiera małe błędy lub nie dopatrzenia. Kod jest daleki od stanu produkcujnego.

## Architektura projektu

Projekt został napisany według architektury 3-warstwowej, podzielony na warstwy dostępu do bazy danych, biznesową oraz prezentacji,
W programie zastosowane zostały wzroce projektowe: Obserwator - dla systemu mailingowego, Proxy (Pośrednik) - dla warstwy biznesowej odpowiedzialnej za działanie logiki aplikacji. Singleton - dla obiektu komunikującego się z bazą danych bezpośrednio poprzez framework ORM (SQLAlchemy). 

## Skład wykonujący aplikację:

* https://github.com/kamiltlalka
* https://github.com/barteekp

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
docker run -d -p 5000:5000 `nazwa`
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
