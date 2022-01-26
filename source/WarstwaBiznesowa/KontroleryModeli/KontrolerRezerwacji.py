import datetime

from source.BazaDanych.Modele.Rezerwacja import Rezerwacja
from source.BazaDanych.BazaDanych import BazaDanych
from source.WarstwaBiznesowa.ModeleBLL.RezerwacjaBLL import RezerwacjaBLL
from source.WarstwaBiznesowa.KontroleryModeli.KontrolerModeluInterface import KontrolerModeluInterface
from source.WarstwaBiznesowa.ModeleBLL.KontoPrywatneBLL import KontoPrywatneBLL
from source.WarstwaBiznesowa.SystemMailingowy.Obserwator import Obserwator
from source.WarstwaBiznesowa.SystemMailingowy.Publikujacy import Publikujacy
from typing import *
from sqlalchemy.orm import scoped_session
from source.WarstwaBiznesowa.wyjatki import *
from source.BazaDanych.Modele.Termin import Termin
from source.BazaDanych.Modele.Sala import Sala


class KontrolerRezerwacji(KontrolerModeluInterface, Publikujacy):

    def __init__(self):
        if BazaDanych.db_session is None:
            raise BladWBazieDanychError("Baza danych niezostała zainicjowana!")

        self.__sesja: scoped_session = BazaDanych.db_session
        self.__obserwatorzy: List[Obserwator] = []

    def dodajObiekt(self, obiekt: RezerwacjaBLL) -> int:
        nowyObiekt = Rezerwacja(obiekt.do_Zaplaty, obiekt.Id_Rezerwujacego, obiekt.Id_Sali, obiekt.Id_Terminu)
        terminy_sali = [t for t in self.__sesja.query(Termin).filter(Termin.Id_Sali == obiekt.Id_Sali) if t.Wolny]
        id = None
        try:
            self.__sesja.add(nowyObiekt)
            self.__sesja.commit()
            self.__sesja.refresh(nowyObiekt)
            id = nowyObiekt.Id_Rezewacji
            termin = self.__sesja.query(Termin).filter(Termin.Id_Terminu==obiekt.Id_Terminu).first()
            termin.Wolny = False
            if len(terminy_sali) == 1:
                sala = self.__sesja.query(Sala).filter(Sala.Id_sali == obiekt.Id_Sali).first()
                sala.Wolna = False
            self.__sesja.commit()
        except Exception as e:
            self.__sesja.remove()
            raise BladZapisuDoBazyDanych(e)
        finally:
            self.__sesja.remove()

        if len(self.__obserwatorzy) > 0:
            self.powiadomObeserwatora(obiekt)

        return id


    def usunObiekt(self, id: int):
        obiekt = self.pobierzObiekt(id)
        termin = self.__sesja.query(Termin).filter(Termin.Id_Terminu==obiekt.Id_Terminu).first()

        # if (datetime.datetime.now() - termin.Data_i_godzina_Rozpoczecia).days > 2:
        #     raise BladWKontrolerzeModeliError("Nie mozna zrezygnowac z sali na 2 dni przed terminem")
        obiekt.do_Zaplaty = 0

        if len(self.__obserwatorzy) > 0:
            self.powiadomObeserwatora(obiekt)
        try:
            self.__sesja.query(Rezerwacja).filter(Rezerwacja.Id_Rezewacji == id).delete()
            termin = self.__sesja.query(Termin).filter(Termin.Id_Terminu == obiekt.Id_Terminu).first()
            termin.Wolny = True
            sala = self.__sesja.query(Sala).filter(Sala.Id_sali==obiekt.Id_Sali).first()
            sala.Wolna = True
            self.__sesja.commit()
            self.__sesja.remove()
        except Exception as e:
            raise BladWBazieDanychError(e)
        finally:
            self.__sesja.remove()

    def pobierzObiekt(self, id: str) -> RezerwacjaBLL:
        rezerwacja = self.__sesja.query(Rezerwacja).filter(Rezerwacja.Id_Rezewacji == id).one_or_none()
        self.__sesja.remove()
        try:
            pobrany = RezerwacjaBLL(rezerwacja.Id_Rezewacji, rezerwacja.do_Zaplaty, rezerwacja.Id_Rezerwujacego,
                                 rezerwacja.Id_Sali, rezerwacja.Id_Terminu) if rezerwacja is not None else None
        except (TypeError, ValueError) as e:
            raise BladWKontrolerzeModeliError(e)
            
        if pobrany is None:
            raise BladWKontrolerzeModeliError("Nie znaleziono")
        return pobrany

    def pobierzWszystkieObiekty(self) -> List[RezerwacjaBLL]:
        data = self.__sesja.query(Rezerwacja)
        rezerwacje = []
        for r in data:
            Termin.Data_i_godzina_Rozpoczecia
            termin = self.__sesja.query(Termin).filter(Termin.Id_Terminu == r.Id_Terminu).first()
            if (termin.Data_i_godzina_Rozpoczecia - datetime.datetime.now()).days < 0:
                continue
            rezerwacje.append(RezerwacjaBLL(r.Id_Rezewacji, r.do_Zaplaty, r.Id_Rezerwujacego,
                                 r.Id_Sali, r.Id_Terminu))

        self.__sesja.remove()
        return rezerwacje

    def zaktualizujObiekt(self, stary_id: int, nowy: RezerwacjaBLL):
        stary = self.__sesja.query(Rezerwacja).filter(Rezerwacja.Id_Rezewacji == stary_id).one_or_none()
        if stary is None:
            raise BladWKontrolerzeModeliError("Nie mozna zaktualizowac modelu")
        try:
            stary.do_Zaplaty = nowy.do_Zaplaty
            stary.Id_Rezerwujacego = nowy.Id_Rezerwujacego
            stary.Id_Sali = nowy.Id_Sali
            stary.Id_Terminu = nowy.Id_Terminu
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

    # def __init__(self, id, do_zap, id_rez, id_sali, id_terminu):
    #     self.Id_Rezerwacji = id
    #     self.Id_Sali = id_sali
    #     self.do_Zaplaty = do_zap
    #     self.Id_Rezerwujacego = id_rez
    #     self.Id_Terminu = id_terminu