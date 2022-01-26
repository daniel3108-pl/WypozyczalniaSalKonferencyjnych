from .KontroleryModeli.KontrolerKontaPrywatnego import KontrolerKontaPrywatnego
from .KontroleryModeli.KontrolerKontaFirmowego import *
from .KontroleryModeli.KontrolerSal import *
from .KontroleryModeli.KontrolerTerminow import *
from .KontroleryModeli.KontrolerRezerwacji import *
from .KontroleryModeli.KontrolerModeluInterface import KontrolerModeluInterface, TypModelu
from .SystemMailingowy.Obserwator import Obserwator


class PosrednikBazyDanych:

    def __init__(self, typ: TypModelu):
        self.kontrolerModelu: KontrolerModeluInterface = None

        if BazaDanych.db_session is None:
            raise Exception("Baza danych niezostała zainicjowana!")

        if typ == TypModelu.KontoPrywatne:
            self.kontrolerModelu = KontrolerKontaPrywatnego()
        elif typ == TypModelu.KontoFirmowe:
            self.kontrolerModelu = KontrolerKontaFirmowego()
        elif typ == TypModelu.Rezerwacje:
            self.kontrolerModelu = KontrolerRezerwacji()
        elif typ == TypModelu.Sale:
            self.kontrolerModelu = KontrolerSal()
        elif typ == TypModelu.Terminy:
            self.kontrolerModelu = KontrolerTerminow()
        else:
            raise TypeError("Niepoprawny typ modelu")

    def dodajObiekt(self, obiekt: object) -> int:
        return self.kontrolerModelu.dodajObiekt(obiekt)

    def usunObiekt(self, id: int):
        self.kontrolerModelu.usunObiekt(id)

    def zaktualizujObiekt(self, stary_id: int, nowy: object):
        self.kontrolerModelu.zaktualizujObiekt(stary_id, nowy)

    def pobierzObiekt(self, id: str):
        return self.kontrolerModelu.pobierzObiekt(id)

    def pobierzWszystkieObiekty(self):
        return self.kontrolerModelu.pobierzWszystkieObiekty()

    @staticmethod
    def przygotujBazeDanych(db_uri: str, check_same_thread: bool = False):
        BazaDanych.przygotujBazeDanych(db_uri, check_same_thread)