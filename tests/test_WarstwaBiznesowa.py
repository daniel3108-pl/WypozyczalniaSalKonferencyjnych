"""
Moduł odpowiadający za klasy testów PyTest zwiazanych z funkcjonalnoscia warstwy biznesowej
"""
import os.path

import config
from source.BazaDanych.BazaDanych import BazaDanych
from source.WarstwaBiznesowa.ModeleBLL.KontoPrywatneBLL import KontoPrywatneBLL
from source.WarstwaBiznesowa.ModeleBLL.KontoFirmoweBLL import KontoFirmoweBLL
from source.WarstwaBiznesowa.ModeleBLL.SalaBLL import SalaBLL
from source.WarstwaBiznesowa.ModeleBLL.RezerwacjaBLL import RezerwacjaBLL
from source.WarstwaBiznesowa.ModeleBLL.TerminBLL import TerminBLL
from source.WarstwaBiznesowa.PosrednikBazyDanych import PosrednikBazyDanych
from source.WarstwaBiznesowa.KontroleryModeli.KontrolerModeluInterface import TypModelu
from source.WarstwaBiznesowa.KontroleryModeli import (
    KontrolerKontaPrywatnego as KKP, KontrolerKontaFirmowego as KKF,
    KontrolerSal as KS, KontrolerTerminow as KT, KontrolerRezerwacji as KR
)
from source.BazaDanych.Modele import (
    KontoPrywatne as KP, KontoFirmowe as KF, Termin as T, Sala as S, Rezerwacja as R
)
from pytest import mark, raises, main, fixture
import datetime


BAZADANYCH_TEST_URI = config.TEST_DATABASE_URI


def get_time_from(as_str: bool = True):
    """
    Funkcja zwaracjaca date przykladowa do testow
    :return: aktualna data i czas
    """
    date = datetime.datetime.now() + datetime.timedelta(minutes=10)
    return datetime.datetime.strftime(date, "%d.%m.%Y %H:%M") if as_str else date


def get_time_to(as_str: bool = True, delta: int = 20):
    """
    Funkcja zwaracjaca date przykladowa do testow
    :return: aktualna data i czas + 20 minut
    """
    date = datetime.datetime.now() + datetime.timedelta(minutes=delta)
    return datetime.datetime.strftime(date, "%d.%m.%Y %H:%M") if as_str else date


class TestModeleBll:
    """
    Klasa dla testow zwiazanych z modelami warstwy biznesowej
    """
    @mark.parametrize(
        ("id", "nazwa", "mail", "telefon", "haslo", "bank"),
        (
                [0, "He", "dsds@dsds.com", "322-122-323", "dadaads", "434321434343434343343433"],
                [0, 1, "dsds@dsds.com","323-121-232", "dadaads", "434321434343434343343433"],
                [0, "asddd", "d2323", "232-233-123", "adsadasd", "434321434343434343343433"],
                [0, "dasd", "dsds@dsds.com", "233-123", "adsadasd",  "434321434343434343343433"],
                ["sa", "dasd", "dsds@dsds.com",  "232-233-123", "adsadasd", "434321434343434343343433"],
                [0, "dasdd", "dsds@dsds.com",  "232-233-123", "ads", "434321434343434343343433"],
                [0, "dasdd", "dsds@dsds.com", "232-233-123", "ads22312", "434321434sad"],
                [0, "dasdd", "dsds@dsds.com", "232-233-123", "ads323232", "d434321434343434343343433dsa"],
                [-1, "dasdd", "dsds@dsds.com", "232-233-123", "ads323232", "434321434343434343343433"]
        ))
    def test_konto_firmowe_init(self, id, nazwa, mail, telefon, haslo, bank):
        """
        Testuje poprawnosc walidacji danych w modelu KontoFirmoweBLL
        """
        with raises((TypeError, ValueError)):
            konto = KontoFirmoweBLL(id, nazwa, mail, telefon, haslo, bank)

    @mark.parametrize(
    ("id", "nm", "sur", "mail", "psw", "phone"),
    (
        [0, "Hello", "de", "dsds@dsds.com", "dadaads", "323-121-232"],
        [0, 1, "de", "dsds@dsds.com", "dadaads", "323-121-232"],
        [0, "dasd", "asdd", "d2323", "adsadasd", "232-233-123"],
        [0, "dasd", "asdd", "d2323", "adsadasd", "233-123"],
        ["sa","dasd", "asdd", "d2323", "adsadasd", "232-233-123"],
        [0, "dasd", "asdd", "d2323", "ads", "232-233-123"],
        [-1, "Hello", "deasdasd", "dsds@dsds.com", "dadaads", "323-121-232"]
    ))
    def test_konto_prywatne_init(self, id, nm, sur, mail, psw, phone):
        """
        Testuje poprawnosc walidacji danych w modelu KontoPrywatneBLL
        """
        with raises((TypeError, ValueError)):
            konto = KontoPrywatneBLL(id, nm, sur, mail, psw, phone)

    @mark.parametrize(
        ('id','adres', 'cena', 'rozmiar','licz_miej', 'wypos', 'dod', 'wolna', 'id_wyn'),
        (
            ("as", "sasdasas", 43.20, 32, 12, "dssddsds", "dssd", True, 1),
            (0, 23, 43.20, 32, 12, "dssddsds", "dssd", True, 1),
            (0, "sasdasas", "hello", 32, 12, "dssddsds", "dssd", True, 1),
            (0, "sasdasas", 43.20, "das", 12, "dssddsds", "dssd", True, 1),
            (0, "sasdasas", 43.20, 32, "12332", "dssddsds", "dssd", True, 1),
            (0, "sasdasas", 43.20, 32, 12, list(), "dssd", True, 1),
            (0, "sasdasas", 43.20, 32, 12, "dssddsds", 32123.2323, True, 1),
            (0, "sasdasas", 43.20, 32, 12, "dssddsds", "dssd", "dasad", 1),
            (0, "sasdasas", -43.20, 32, -12, "dssddsds", "dssd", True, 1),
            (0, "sasdasas", 43.20, -32, 12, "dssddsds", "dssd", True, 1),
            (0, "sasdasas", 43.20, 32, -12, "dssddsds", "dssd", True, 1),
            (-1, "sasdasas", 43.20, 32, 12, "dssddsds", "dssd", True, 1),
        )
    )
    def test_sala_init(self, id, adres, cena, rozmiar, licz_miej, wypos, dod, wolna, id_wyn):
        """
        Testuje poprawnosc walidacji danych w modelu SalaBLL
        """
        with raises((TypeError)):
            sala = SalaBLL(id, adres, cena, rozmiar, licz_miej, wypos, dod, wolna, id_wyn)

    @mark.parametrize(
        ('id', 'od', 'do', 'wolny', 'id_sali'),
        (
            ("dsd", get_time_from(), get_time_to(), True, 2),
            (0, "daads", get_time_to(), True, 2),
            (0, get_time_from(), 323223, True, 2),
            (0, get_time_from(), get_time_to(), "dsds", 2),
            (0, get_time_from(), get_time_to(), True, "asads"),
            (0, get_time_to(), get_time_from(), True, 2),
            (0, "12/03/2021 13:32", get_time_to(), True, 2),
            (0, "11.01.2021 13:32", get_time_to(), True, 2),
        )
    )
    def test_termin_init(self, id, od, do, wolny, id_sali):
        """
        Testuje poprawnosc walidacji danych w modelu TerminBLL
        """
        with raises((TypeError, ValueError)):
            termin = TerminBLL(id, od, do, wolny, id_sali)

    @mark.parametrize(
        ('id', 'do_zap', 'id_rez', 'id_sali', 'id_terminu'),
        (
            ("dsdsd", 23.23, 1, 2, 1),
            (0, "dasdas", 1, 2, 1),
            (0, 23.23, "dassda", 2, 1),
            (0, 23.23, 1, None, 1),
            (0, 23.23, 1, 2, "adsdasad"),
            (0, -12, 1, 2, 1),
            (0, 12, 1, 2, -1),
            (0, 12, -1, 2, 1),
            (-1, 12, 1, 2, 1),
        )
    )
    def test_rezewacja_init(self, id, do_zap, id_rez, id_sali, id_terminu):
        """
        Testuje poprawnosc walidacji danych w modelu RezerwacjaBLL
        """
        with raises((TypeError)):
            rezerwacja = RezerwacjaBLL(id, do_zap, id_rez, id_sali, id_terminu)

    def test_konto_prywatne_init_poprwane(self):
        wyjatek = False
        try:
            konto = KontoPrywatneBLL(0, "Hello", "surname", "mail333@mail.com", "434-434-433", "password")
        except TypeError as e:
            wyjatek = True

        assert not wyjatek, "Nie powinno wyrzucac wyjatku przy poprawnych danych dla konta prywatnego bll"


    def test_konto_firmowe_init_poprwane(self):
        wyjatek = False
        try:
            konto = KontoFirmoweBLL(0, "Hello", "mail333@mail.com", "434-434-433", "password", "22222222222222222222222222")
        except TypeError as e:
            wyjatek = True

        assert not wyjatek, "Nie powinno wyrzucac wyjatku przy poprawnych danych dla konta firmowego bll"

    def test_sala_init_poprwane(self):
        wyjatek = False
        try:
            salabll = SalaBLL(0, "dasdas", 55.23, 54.23, 44, "dasd", "", True, 1)
        except TypeError as e:
            wyjatek = True

        assert not wyjatek, "Nie powinno wyrzucac wyjatku przy poprawnych danych dla sali bll"

    def test_temin_init_poprwane(self):
        wyjatek = False
        try:
            terminbll = TerminBLL(0, get_time_from(as_str=False), get_time_to(as_str=False, delta=30), True, 1)
        except TypeError as e:
            wyjatek = True

        assert not wyjatek, "Nie powinno wyrzucac wyjatku przy poprawnych danych dla terminu bll"

    def test_rezerwacja_init_poprwane(self):
        wyjatek = False
        try:
            rezerwacjaBLL = RezerwacjaBLL(0, 45, 1, 1, 2)
        except TypeError as e:
            wyjatek = True

        assert not wyjatek, "Nie powinno wyrzucac wyjatku przy poprawnych danych dla rezrwacji bll"


class TestPosrednikBazyDanych:
    """
    Klasa odpowiadajaca za testy posrednika bazy danych
    """

    def afterAll(self):
        pass

    @fixture(scope="class", autouse=True)
    def beforeAll(self, request):
        """
        Uruchamia sie przed wszystkimi testami, inicjalizuje baze danych do testow
        :param request:
        :return:
        """
        BazaDanych.przygotujBazeDanych(BAZADANYCH_TEST_URI)
        # Dodawanie danych
        request.addfinalizer(self.afterAll)

    @mark.parametrize(
        ("input", "expected", "excpet"),
        (
            (TypModelu.KontoPrywatne, KKP.KontrolerKontaPrywatnego, False),
            (TypModelu.KontoFirmowe, KKF.KontrolerKontaFirmowego, False),
            (TypModelu.Sale, KS.KontrolerSal, False),
            (TypModelu.Rezerwacje, KR.KontrolerRezerwacji, False),
            (TypModelu.Terminy, KT.KontrolerTerminow, False),
            ("dsaasd", None, True)
        )
    )
    def test_typu_kontolera(self, input, expected, excpet):
        """
        Testuje czy PosrednikBazyDanych poprawnie wybiera typ kontrolera modelu z bazy danych
        :param input: TypModelu
        :param expected: Typ kontrolera modelu
        :param excpet: czy ma wystapic wyjatek
        """
        if not excpet:
            posrednik = PosrednikBazyDanych(input)
            assert isinstance(posrednik.kontrolerModelu, expected), "Nie poprawny rodzaj kontrolera"
        else:
            with raises(TypeError):
                posrednik = PosrednikBazyDanych(input)


class TestKontrolerKontaPrywatnego:
    """
    Klasa testujaca dzialanie kontrolera konta prywatnego
    """

    def afterAll(self):
        pass

    @fixture(scope="class", autouse=True)
    def beforeAll(self, request):
        """
        Uruchamia sie przed wszystkimi testami, inicjalizuje baze danych do testow
        :param request:
        :return:
        """
        BazaDanych.przygotujBazeDanych(BAZADANYCH_TEST_URI)
        # Dodawanie danych
        user1 = KP.KontoPrywatne("test1", "test2", "mail@mail.com", "434-434-434", "password")
        BazaDanych.db_session.add(user1)
        user2 = KP.KontoPrywatne("test2", "test3", "mail2@mail.com", "222-434-434", "qwerrtyu")
        BazaDanych.db_session.add(user2)
        BazaDanych.db_session.commit()
        BazaDanych.db_session.remove()
        request.addfinalizer(self.afterAll)


    def test_dodawania(self):
        """
        Sprawdza dodawanie konta prywatnego do bazy danych
        :return:
        """
        kontroler = KKP.KontrolerKontaPrywatnego()
        konto = KontoPrywatneBLL(0, "Hello", "surname", "mail333@mail.com", "434-434-433", "password")
        id_nowego = kontroler.dodajObiekt(konto)
        konto = BazaDanych.db_session.query(KP.KontoPrywatne).filter(KP.KontoPrywatne.ID_Konta == id_nowego).one_or_none()
        assert konto is not None, "Nie dodano poprawnie konta"

        BazaDanych.db_session.refresh(konto)
        BazaDanych.db_session.query(KP.KontoPrywatne).filter(KP.KontoPrywatne.ID_Konta == id_nowego).delete()
        BazaDanych.db_session.commit()
        BazaDanych.db_session.remove()

    def test_pobierz(self):
        """
        Sprawdza czy pobierane z bazy konta maja poprawne dane
        :return:
        """
        kontroler = KKP.KontrolerKontaPrywatnego()
        konto1: KontoPrywatneBLL = kontroler.pobierzObiekt(1)

        assert konto1 is not None and konto1.Imie == "test1" and konto1.Nazwisko == "test2" and konto1.Adres_Email == "mail@mail.com", \
        "Pobrano niepoprwane dane z bazy danych"

    def test_pobierzWszystkie(self):
        """
        Sprawdza czy poprawnie pobierana jest lista wszystkich kont z bazy danych
        :return:
        """
        kontroler = KKP.KontrolerKontaPrywatnego()
        wszystkie = kontroler.pobierzWszystkieObiekty()
        assert isinstance(wszystkie, list), "Nie zwrocilo listy"
        assert len(wszystkie) == 2, "Lista jest za krotka dla podanych danych {}".format(len(wszystkie))
        for k in wszystkie:
            assert BazaDanych.db_session.query(KP.KontoPrywatne).filter(KP.KontoPrywatne.ID_Konta == k.ID_Konta).one_or_none() is not None, \
                    "Brak odpowiadajacego konta w bazie danych"

    def test_zaktualizujObiekt(self):
        """
        Sprawdza czy poprawnie zmieniane sa dane konta w bazie danych
        :return:
        """
        kontroler = KKP.KontrolerKontaPrywatnego()
        konto1: KontoPrywatneBLL = kontroler.pobierzObiekt(1)
        konto1.Imie = "Marian"
        konto1.Nazwisko = "Pazdzioch"
        kontroler.zaktualizujObiekt(1, konto1)
        kontoNowe = BazaDanych.db_session.query(KP.KontoPrywatne).filter(KP.KontoPrywatne.ID_Konta == 1).one_or_none()
        assert kontoNowe.Imie == "Marian" and kontoNowe.Nazwisko == "Pazdzioch", "Nie zmienilo danych konta"

    def test_usunObiekt(self):
        """
        Sprawdza czy poprawnie jest usuwane konto z bazy danych
        :return:
        """
        kontroler = KKP.KontrolerKontaPrywatnego()
        konto = BazaDanych.db_session.query(KP.KontoPrywatne).filter(KP.KontoPrywatne.ID_Konta == 1).one_or_none()
        try:
            kontroler.usunObiekt(konto.ID_Konta)
        except:
            assert False, "Niepowinno wyrzucic wyjatku"
        assert not BazaDanych.db_session.query(KP.KontoPrywatne).filter(KP.KontoPrywatne.ID_Konta == 1).one_or_none(), \
            "Nie usunieto poprawnie konta prywatnego"


class TestKontrolerKontaFirmowego:
    """
    Klasa testujaca dzialanie kontrolera konta firmowego

    """

    def afterAll(self):
        pass

    @fixture(scope="class", autouse=True)
    def beforeAll(self, request):
        """
        Uruchamia sie przed wszystkimi testami, inicjalizuje baze danych do testow
        :param request:
        :return:
        """
        BazaDanych.przygotujBazeDanych(BAZADANYCH_TEST_URI)
        # Dodawanie danych
        user1 = KF.KontoFirmowe("test1", "mail@mail.com", "434-434-434", "password", "22222222222222222222222222")
        BazaDanych.db_session.add(user1)
        user2 = KF.KontoFirmowe("test2", "mail2@mail.com", "222-434-434", "qwerrtyu", "22222222222222222222222222")
        BazaDanych.db_session.add(user2)
        BazaDanych.db_session.commit()
        BazaDanych.db_session.remove()
        request.addfinalizer(self.afterAll)

    def test_dodawania(self):
        """
        Sprawdza czy poprawnie sie dodaje konto firmowe do bazy
        :return:
        """
        kontroler = KKF.KontrolerKontaFirmowego()
        konto = KontoFirmoweBLL(0, "Hello", "mail333@mail.com", "434-434-433", "password", "22222222222222222222222222")
        id_nowego = kontroler.dodajObiekt(konto)
        konto = BazaDanych.db_session.query(KF.KontoFirmowe).filter(KF.KontoFirmowe.ID_Konta == id_nowego).one_or_none()
        assert konto is not None, "Nie dodano poprawnie konta"

        BazaDanych.db_session.refresh(konto)
        BazaDanych.db_session.query(KF.KontoFirmowe).filter(KF.KontoFirmowe.ID_Konta == id_nowego).delete()
        BazaDanych.db_session.commit()
        BazaDanych.db_session.remove()

    def test_pobierz(self):
        """
        Sprwadza czy poprawnie pobierane sa konta firmowe z bazy danych
        :return:
        """
        kontroler = KKF.KontrolerKontaFirmowego()
        konto1: KontoFirmoweBLL = kontroler.pobierzObiekt(1)

        assert konto1 is not None and konto1.Nazwa_Firmy == "test1" and konto1.Adres_Email == "mail@mail.com", \
            "Nie pobrano poprawnego konta firmowego"

    def test_pobierzWszystkie(self):
        """
        Sprawdza czy pobieranie listy wszystkich kont firmowych zwraca poprawny wynik
        :return:
        """
        kontroler = KKF.KontrolerKontaFirmowego()
        wszystkie = kontroler.pobierzWszystkieObiekty()
        assert isinstance(wszystkie, list), "Nie zwrocilo listy"
        assert len(wszystkie) == 2, "Lista jest za krotka dla podanych danych {}".format(len(wszystkie))
        for k in wszystkie:
            assert BazaDanych.db_session.query(KF.KontoFirmowe).filter(KF.KontoFirmowe.ID_Konta == k.ID_Konta).one_or_none() is not None, \
                "Pobrane konto nie odpowiada zadnemu z bazy danych"

    def test_zaktualizujObiekt(self):
        """
        Sprawdza czy poprawnie zmieniane sa dane konta firmowego w bazie danych
        :return:
        """
        kontroler = KKF.KontrolerKontaFirmowego()
        konto1: KontoFirmoweBLL = kontroler.pobierzObiekt(1)
        konto1.Nazwa_Firmy = "Marian"
        konto1.Haslo = "Pazdzioch"
        kontroler.zaktualizujObiekt(1, konto1)
        kontoNowe = BazaDanych.db_session.query(KF.KontoFirmowe).filter(KF.KontoFirmowe.ID_Konta == 1).one_or_none()
        assert kontoNowe.Nazwa_Firmy == "Marian" and kontoNowe.Haslo == "Pazdzioch", "Nie zmienilo danych konta"

    def test_usunObiekt(self):
        """
        Sprawdza czy poprawnie jest usuwane konto firmowe z bazy danych
        :return:
        """
        kontroler = KKF.KontrolerKontaFirmowego()
        konto = BazaDanych.db_session.query(KF.KontoFirmowe).filter(KF.KontoFirmowe.ID_Konta == 1).one_or_none()
        try:
            kontroler.usunObiekt(konto.ID_Konta)
        except:
            assert False, "Niepowinno wyrzucic wyjatku"
        assert not BazaDanych.db_session.query(KF.KontoFirmowe).filter(KF.KontoFirmowe.ID_Konta == 1).one_or_none(), \
            "Nie usunieto poprawnie konta firmowego"


class TestKontrolerSali:
    """
    Klasa testujaca dzialanie kontrolera sali
    """

    def afterAll(self):
        pass

    @fixture(scope="class", autouse=True)
    def beforeAll(self, request):
        """
        Uruchamia sie przed wszystkimi testami, inicjalizuje baze danych do testow
        :param request:
        :return:
        """
        BazaDanych.przygotujBazeDanych(BAZADANYCH_TEST_URI)
        # Dodawanie danych
        user1 = KF.KontoFirmowe("test1", "mail@mail.com", "434-434-434", "password", "22222222222222222222222222")
        BazaDanych.db_session.add(user1)
        user2 = KF.KontoFirmowe("test2", "mail2@mail.com", "222-434-434", "qwerrtyu", "22222222222222222222222222")
        BazaDanych.db_session.add(user2)
        sala1 = S.Sala("sdaasdasd", 12.2, 23.3, 32, "ddddd", "ddddd", True, 1)
        BazaDanych.db_session.add(sala1)
        termin1 = T.Termin(get_time_from(as_str=False), get_time_to(as_str=False, delta=60), True, 1)
        BazaDanych.db_session.add(termin1)
        BazaDanych.db_session.commit()
        BazaDanych.db_session.remove()
        request.addfinalizer(self.afterAll)

    def test_dodawania(self):
        """
        Sprawdza czy poprawnie dodawana jest sala do bazy danych
        :return:
        """
        kontroler = KS.KontrolerSal()
        salabll = SalaBLL(0, "dasdas", 55.23, 54.23, 44, "dasd", "", True, 1)
        id_nowego = kontroler.dodajObiekt(salabll)
        sala = BazaDanych.db_session.query(S.Sala).filter(S.Sala.Id_sali == id_nowego).one_or_none()
        assert sala is not None, "Nie dodano poprawnie sali"

        BazaDanych.db_session.refresh(sala)
        BazaDanych.db_session.query(S.Sala).filter(S.Sala.Id_sali == id_nowego).delete()
        BazaDanych.db_session.commit()
        BazaDanych.db_session.remove()

    def test_pobierz(self):
        """
        Sprawdza czy poprawnie jest pobierana sala z bazy danych czy dane sie zgadzaja
        :return:
        """
        kontroler = KS.KontrolerSal()
        sala1: SalaBLL = kontroler.pobierzObiekt(1)

        assert sala1 is not None and sala1.Id_Wynajmujacego == 1 and sala1.Adres == "sdaasdasd" and sala1.Wolna,\
            "Nie pobrano poprawnej sali"

    def test_pobierzWszystkie(self):
        """
        Sprawdza czy pobierana lista wszystkich sal jest poprawana i wszystkie sale sa w bazie danych
        :return:
        """
        kontroler = KS.KontrolerSal()
        wszystkie = kontroler.pobierzWszystkieObiekty()
        assert isinstance(wszystkie, list), "Nie zwrocilo listy"
        assert len(wszystkie) == 1, "Lista jest za krotka lub za dluga dla podanych danych {}".format(len(wszystkie))
        for s in wszystkie:
            assert BazaDanych.db_session.query(S.Sala).filter(S.Sala.Id_sali == s.id_sali).one_or_none() is not None, \
                "Nie znaleziono odpowiadajacej sali w bazie danych"

    def test_zaktualizujObiekt(self):
        """
        Sprawdza czy aktualizacja sali w bazie danych jest poprawnie wykonywana
        :return:
        """
        kontroler = KS.KontrolerSal()
        sala1: SalaBLL = kontroler.pobierzObiekt(1)
        sala1.Adres = "asddasasdasdasdasdasd"
        sala1.Cena = 32323.21
        kontroler.zaktualizujObiekt(1, sala1)
        salaNowa: S.Sala = BazaDanych.db_session.query(S.Sala).filter(S.Sala.Id_sali == 1).one_or_none()
        assert salaNowa.Adres == "asddasasdasdasdasdasd" and salaNowa.Cena == 32323.21, "Nie zmienilo danych sali"

    def test_usunObiekt(self):
        """
        Sprawdza czy usuwanie sali z bazy danych jest poprwane
        :return:
        """
        kontroler = KS.KontrolerSal()
        try:
            kontroler.usunObiekt(1)
        except:
            assert False, "Niepowinno wyrzucic wyjatku"
        assert not BazaDanych.db_session.query(S.Sala).filter(S.Sala.Id_sali == 1).one_or_none(), "Nie usunieto Sali poprawie"


time_from = get_time_from(as_str=False)


class TestKontrolerTerminow:
    """
    Klasa testujaca dzialanie kontrolera terminow

    """

    def afterAll(self):
        pass

    @fixture(scope="class", autouse=True)
    def beforeAll(self, request):
        """
        Uruchamia sie przed wszystkimi testami, inicjalizuje baze danych do testow
        :param request:
        :return:
        """
        BazaDanych.przygotujBazeDanych(BAZADANYCH_TEST_URI)
        # Dodawanie danych
        user1 = KF.KontoFirmowe("test1", "mail@mail.com", "434-434-434", "password", "22222222222222222222222222")
        BazaDanych.db_session.add(user1)
        sala1 = S.Sala("sdaasdasd", 12.2, 23.3, 32, "ddddd", "ddddd", True, 1)
        BazaDanych.db_session.add(sala1)

        global time_from
        time_from = get_time_from(as_str=False)

        termin1 = T.Termin(time_from, get_time_to(as_str=False), True, 1)
        BazaDanych.db_session.add(termin1)
        BazaDanych.db_session.commit()
        BazaDanych.db_session.remove()
        request.addfinalizer(self.afterAll)

    def test_dodawania(self):
        """
        Sprawdza czy terminy poprwanie sa dodawane do bazy danych
        :return:
        """
        kontroler = KT.KontrolerTerminow()
        terminbll = TerminBLL(0, get_time_from(as_str=False), get_time_to(as_str=False, delta=30), True, 1)
        id_nowego = kontroler.dodajObiekt(terminbll)
        term = BazaDanych.db_session.query(T.Termin).filter(T.Termin.Id_Terminu == id_nowego).one_or_none()
        assert term is not None, "Nie dodano poprawnie terminu"

        BazaDanych.db_session.refresh(term)
        BazaDanych.db_session.query(T.Termin).filter(T.Termin.Id_Terminu == id_nowego).delete()
        BazaDanych.db_session.commit()
        BazaDanych.db_session.remove()

    def test_pobierz(self):
        """
        Sprawdza czy pobrany termin z bazy danych ma poprawne dane
        :return:
        """
        kontroler = KT.KontrolerTerminow()
        termin: TerminBLL = kontroler.pobierzObiekt(1)

        global time_from
        assert termin is not None and termin.Id_Sali == 1 and termin.Data_i_godzina_Rozpoczecia == time_from, \
            "Pobrany termin nie zwrocil poprawnych danych"

    def test_pobierzWszystkie(self):
        """
        Sprawdza czy pobierana lista terminow jest poprawna i odpowiada tej z bazy danych
        :return:
        """
        kontroler = KT.KontrolerTerminow()
        wszystkie = kontroler.pobierzWszystkieObiekty()
        assert isinstance(wszystkie, list), "Nie zwrocilo listy"
        assert len(wszystkie) == 1, "Lista jest za krotka lub za dluga dla podanych danych {}".format(len(wszystkie))
        print(wszystkie[0].toDict())
        for t in wszystkie:
            assert isinstance(t, TerminBLL), "obiekt w liscie nie jest terminem"
            assert T.Termin.query.filter_by(Id_Terminu=t.Id_Terminu).first(), "Nie ma odpowiadajacego terminu w bazie danych"

    def test_zaktualizujObiekt(self):
        """
        Sprawdza czy dane terminu sie poprawnie aktualizuja w bazie danych
        :return:
        """
        kontroler = KT.KontrolerTerminow()
        termin1: TerminBLL = kontroler.pobierzObiekt(1)
        termin1.wolny = False
        kontroler.zaktualizujObiekt(1, termin1)
        terminNowy: T.Termin = BazaDanych.db_session.query(T.Termin).filter(T.Termin.Id_Terminu == 1).one_or_none()
        assert not terminNowy.Wolny, "Nie zmienilo danych terminu"

    def test_usunObiekt(self):
        """
        Sprawdza czy termin jest poprawnie usuwany z bazy danych
        :return:
        """
        kontroler = KT.KontrolerTerminow()
        try:
            kontroler.usunObiekt(1)
        except Exception as e:
            assert False, "Niepowinno wyrzucic wyjatku {}".format(e)
        assert not BazaDanych.db_session.query(T.Termin).filter(T.Termin.Id_Terminu == 1).one_or_none(), \
            "Nie usunieto poprwanie terminu"

        sala = BazaDanych.db_session.query(S.Sala).filter(S.Sala.Id_sali == 1).first()
        assert not sala.Wolna, "Nie sprawiono, ze sala bez terminow jest niedostepna"


class TestKontrolerRezerwacji:
    """
    Klasa testujaca dzialanie kontrolera rezerwacji
    """

    def afterAll(self):
        pass

    @fixture(scope="class", autouse=True)
    def beforeAll(self, request):
        """
        Uruchamia sie przed wszystkimi testami, inicjalizuje baze danych do testow
        :param request:
        :return:
        """
        BazaDanych.przygotujBazeDanych(BAZADANYCH_TEST_URI)
        # Dodawanie danych
        user1 = KF.KontoFirmowe("test1", "mail@mail.com", "434-434-434", "password", "22222222222222222222222222")
        BazaDanych.db_session.add(user1)
        sala1 = S.Sala("sdaasdasd", 12.2, 23.3, 32, "ddddd", "ddddd", True, 1)
        BazaDanych.db_session.add(sala1)
        user2 = KP.KontoPrywatne("test1", "test2", "mail@massd.com", "545-545-545", "password")
        BazaDanych.db_session.add(user2)
        global time_from
        time_from = get_time_from(as_str=False)
        termin1 = T.Termin(time_from, get_time_to(as_str=False), True, 1)
        termin2 = T.Termin(time_from, get_time_to(as_str=False, delta=60), True, 1)
        BazaDanych.db_session.add(termin1)
        BazaDanych.db_session.add(termin2)

        rezerwacja1 = R.Rezerwacja(23.00, 1, 1, 1)
        BazaDanych.db_session.add(rezerwacja1)

        BazaDanych.db_session.commit()
        BazaDanych.db_session.remove()
        request.addfinalizer(self.afterAll)

    def test_dodawania(self):
        """
        Sprawdza czy dodawanie rezerwacji do bazy danych dziala poprawnie
        :return:
        """
        kontroler = KR.KontrolerRezerwacji()
        rezerwacjaBLL = RezerwacjaBLL(0, 45, 1, 1, 2)
        id_nowego = kontroler.dodajObiekt(rezerwacjaBLL)
        rezer = R.Rezerwacja.query.filter_by(Id_Rezewacji=id_nowego).first()
        assert rezer is not None, "Nie dodano poprawnie rezerwacji"

        termin = BazaDanych.db_session.query(T.Termin).filter(T.Termin.Id_Terminu == 2 ).first()
        assert not termin.Wolny, "Nie ustawilo terminu na zajety"


    def test_pobierz(self):
        """
        Sprawdza czy pobierana rezerwacja jest prawidłowa i posiada odpowiednie dane jak w bazie danych
        :return:
        """
        kontroler = KR.KontrolerRezerwacji()
        rezer: RezerwacjaBLL = kontroler.pobierzObiekt(1)

        assert rezer is not None and rezer.Id_Sali == 1 and rezer.Id_Rezerwujacego == 1 and rezer.do_Zaplaty == 23.00,\
            "Nie pobralo poprawnie rezerwacji"

    def test_pobierzWszystkie(self):
        """
        Sprawdza czy lista rezerwacji jest poprawna i jest zgodna z baza danych
        :return:
        """
        kontroler = KR.KontrolerRezerwacji()
        wszystkie = kontroler.pobierzWszystkieObiekty()
        assert isinstance(wszystkie, list), "Nie zwrocilo listy"
        assert len(wszystkie) == 2, "Lista jest za krotka lub za dluga dla podanych danych {}".format(len(wszystkie))
        for r in wszystkie:
            assert isinstance(r, RezerwacjaBLL), "obiekt w tabllicy nie jest rezerwacja"
            assert R.Rezerwacja.query.filter_by(Id_Rezewacji=r.Id_Rezerwacji).first(), \
                "Nie znaleziono rezerwacji w bazie danych o takim id jak w tablicy"

    def test_zaktualizujObiekt(self):
        """
        Sprawdza czy aktualizacja rezerwacji dziala poprawnie i czy zmiany sa zapisywane w bazie danych
        :return:
        """
        kontroler = KR.KontrolerRezerwacji()
        rezer1: RezerwacjaBLL = kontroler.pobierzObiekt(1)
        rezer1.do_Zaplaty = 0
        kontroler.zaktualizujObiekt(1, rezer1)
        rezerNowy: R.Rezerwacja = BazaDanych.db_session.query(R.Rezerwacja).filter(R.Rezerwacja.Id_Rezewacji == 1).one_or_none()
        assert rezerNowy.do_Zaplaty == 0, "Nie zmienilo danych rezerwacji"

    def test_usunObiekt(self):
        """
        Sprawdza czy usuwanie rezerwacji z bazy danych dziala poprawnie
        :return:
        """
        kontroler = KR.KontrolerRezerwacji()
        try:
            kontroler.usunObiekt(1)
        except:
            assert False, "Niepowinno wyrzucic wyjatku"

        sala = BazaDanych.db_session.query(S.Sala).filter(S.Sala.Id_sali == 1).first()
        termin = BazaDanych.db_session.query(T.Termin).filter(T.Termin.Id_Terminu == 1).first()
        assert not BazaDanych.db_session.query(R.Rezerwacja).filter(R.Rezerwacja.Id_Rezewacji == 1).one_or_none(), \
            "Nie usunieto rezerwacji"
        assert sala.Wolna and termin.Wolny, "Nie ustawilo sali i terminu na wolny"


if __name__ == "__main__":
    main()