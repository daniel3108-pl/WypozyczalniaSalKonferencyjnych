import pytest, os, sys, config
from source.BazaDanych.BazaDanych import BazaDanych
from sqlalchemy.orm import scoped_session

DB_URI = "sqlite:///{}".format(os.path.join(config.PATH, "tests", "testowa.sqlite3"))


class TestBazaDanych:
    """
    Klasa testujaca klase Baza Danych z warstwy Bazy Danych
    """
    def afterAll(self):
        """
        Metoda usuwajaca testowy plik dla bazy danych
        :return:
        """
        if os.path.isfile(DB_URI.replace("sqlite:///", "")):
            os.remove(DB_URI.replace("sqlite:///", ""))

    @pytest.fixture(scope="class", autouse=True)
    def beforeAll(self, request):
        """
        Metoda pozwalajaca na wykonanie po tescie w tej klasie metody afterALL
        """
        request.addfinalizer(self.afterAll)

    def test_przygotujBazeDanych(self):
        BazaDanych.przygotujBazeDanych(DB_URI)
        assert isinstance(BazaDanych.db_session, scoped_session), "Baza danych nie zostala poprawnie zainicjowana"
        assert os.path.isfile(DB_URI.replace("sqlite:///", "")), "Nie utworzono poprawnie pliku sqlite3"
        assert set(BazaDanych.Base.metadata.tables.keys()) == set(["KontaFirmowe", "KontaPrywatne", "Rezerwacje", "Sale", "Terminy"]), "Nie dodano wszystkich tabel"


