from source.BazaDanych.Modele.KontoPrywatne import KontoPrywatne
from source.BazaDanych.BazaDanych import BazaDanych
from source.WarstwaBiznesowa.KontroleryModeli.KontrolerModeluInterface import KontrolerModeluInterface
from source.WarstwaBiznesowa.ModeleBLL.KontoPrywatneBLL import KontoPrywatneBLL
from source.WarstwaBiznesowa.SystemMailingowy.Obserwator import Obserwator
from source.WarstwaBiznesowa.SystemMailingowy.Publikujacy import Publikujacy
from source.WarstwaBiznesowa.ModeleBLL.TerminBLL import TerminBLL
from source.BazaDanych.Modele.Termin import Termin
from sqlalchemy.orm import scoped_session
from typing import List
from source.WarstwaBiznesowa.wyjatki import *
from source.BazaDanych.Modele.Sala import Sala


class KontrolerTerminow(KontrolerModeluInterface, Publikujacy):

    def __init__(self):
        if BazaDanych.db_session is None:
            raise BladWBazieDanychError("Baza danych niezostała zainicjowana!")

        self.__sesja: scoped_session = BazaDanych.db_session
        self.__obserwatorzy: List[Obserwator] = []

    def dodajObiekt(self, obiekt: TerminBLL) -> int:
        nowyObiekt = Termin(obiekt.Data_i_godzina_Rozpoczecia, obiekt.Data_i_godzina_Zakonczenia,
                            obiekt.wolny, obiekt.Id_Sali)
        try:
            self.__sesja.add(nowyObiekt)
            self.__sesja.commit()
            if len(self.__obserwatorzy) > 0:
                self.powiadomObeserwatora(obiekt)
            self.__sesja.refresh(nowyObiekt)
            sala = self.__sesja.query(Sala).filter(Sala.Id_sali == obiekt.Id_Sali).first()
            sala.Wolna = True
        except Exception as e:
            raise BladZapisuDoBazyDanych(e)
        finally:
            self.__sesja.remove()

        return nowyObiekt.Id_Terminu

    def usunObiekt(self, id: int):
        termin = self.__sesja.query(Termin).filter(Termin.Id_Terminu == id).first()
        id_sali = termin.Id_Sali
        try:
            self.__sesja.query(Termin).filter(Termin.Id_Terminu == id).delete()
            self.__sesja.commit()
            sala = self.__sesja.query(Sala).filter(Sala.Id_sali == id_sali).first()
            if not sala.terminy:
                sala.Wolna = False
            self.__sesja.commit()
            self.__sesja.remove()
        except Exception as e:
            self.__sesja.remove()
            raise BladWBazieDanychError(e)


    def pobierzObiekt(self, id: int) -> TerminBLL:
        termin = self.__sesja.query(Termin).filter(Termin.Id_Terminu == id).one_or_none()
        self.__sesja.remove()
        try:
            pobrany = TerminBLL(termin.Id_Terminu, termin.Data_i_godzina_Rozpoczecia, termin.Data_i_godzina_Zakonczenia,
                            termin.Wolny, termin.Id_Sali) if termin is not None else None
        except (TypeError, ValueError) as e:
            return None

        return pobrany



    def pobierzWszystkieObiekty(self) -> List[TerminBLL]:
        data = self.__sesja.query(Termin)
        self.__sesja.remove()
        terminy = []
        for x in data:
            try:
                terminy.append(TerminBLL(x.Id_Terminu, x.Data_i_godzina_Rozpoczecia, x.Data_i_godzina_Zakonczenia,
                         x.Wolny, x.Id_Sali))
            except (ValueError, TypeError) as e:
                continue
        return terminy

    def zaktualizujObiekt(self, stary_id: int, nowy: TerminBLL):
        stary = self.__sesja.query(Termin).filter(Termin.Id_Terminu == stary_id).one_or_none()
        if stary is None:
            raise BladWKontrolerzeModeliError("Nie mozna zaktualizowac modelu")
        try:
            stary.Data_i_godzina_Rozpoczecia = nowy.Data_i_godzina_Rozpoczecia
            stary.Data_i_godzina_Zakonczenia = nowy.Data_i_godzina_Zakonczenia
            stary.Id_Sali = nowy.Id_Sali
            stary.Wolny = nowy.wolny
            self.__sesja.commit()
            self.__sesja.remove()
        except Exception as e:
            self.__sesja.remove()
            raise BladZapisuDoBazyDanych(e)

    def zarejestruj(self, obserwator: Obserwator):
        self.__obserwatorzy.append(obserwator)

    def wyrejestruj(self, obserwator: Obserwator):
        self.__obserwatorzy.remove(obserwator)

    def powiadomObeserwatora(self, obiekt):
        for o in self.__obserwatorzy:
            o.zaktualizuj(obiekt)


