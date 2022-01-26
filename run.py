"""
Kod Zródłowy do projektu IO Wypożyczalnia Sal Konferencyjnych
Informatyka Katowice Grupa 2 Sekcja 5

Bartosz Padkowski
Daniel Świetlik
Kamil Tlałka
Jan Słowik
Piotr Jankowski
Cezary Szumerowski

ten plik - modul, ktory uruchamia aplikacje flask lub testy jednostkowe
"""

import os, sys
import sqlite3
import config
import pytest as pt
import tests.test_WarstwaBiznesowa

def main():
    """
    Funkcja main uruchamiajaca aplikacje webowa projektu
    :return:
    """
    from source.WarstwaPrezentacji.WypozyczalniaModel import WypozyczalniaModel

    os.chdir(config.PATH)
    app = WypozyczalniaModel(__name__)
    try:
        app.start()
    except KeyboardInterrupt as e:
        print(e)
    except sqlite3.ProgrammingError as e2:
        print(e2)

def runTests():
    """
    Funkcja uruchamiajaca testy.
    :return:
    """
    result = pt.main(["", "tests"])
    return result

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] in ("--run-tests", "-rt", "-run-tests") and not config.DO_UNIT_TESTS_BEFORE:
            runTests()
        elif sys.argv[1] in ("-h", "--help", "--h"):
            print("""Poprawne komendy dla pliku:
            run.py ; uruchamia aplikacje webowa
            run.py --run-tests ; uruchamia testy jednostkowe
            run.py --help ; uruchamia ten widok
            """)
        else:
            print("Niepoprawny argument wpisz python run.py --help, żeby wyświetlić poprawne")

    elif config.DO_UNIT_TESTS_BEFORE:
        results = runTests()
        if len(results) == 0:
            main()
        else:
            print("Testy nie zostaly zaakceptowane, server sie nie uruchomi.\n" +
                  "Jesli nie chcesz by testy byly sprawdzane zmien DO_UNIT_TESTS_BEFORE na False w pliku config")
    elif not config.DO_UNIT_TESTS_BEFORE and len(sys.argv) == 1:
        config.DATABASE_URI = config.PRODUCTION_DATABASE_URI
        main()
    else:
        print("Niepoprawne argumenty, config.DO_UNIT_TESTS i argument --run-tests nie moga byc razem uruchamiane!")
