from source.BazaDanych.Modele.KontoPrywatne import KontoPrywatne
from source.BazaDanych.BazaDanych import BazaDanych
from sqlalchemy.orm import scoped_session
from source.WarstwaBiznesowa.KontroleryModeli.KontrolerModeluInterface import KontrolerModeluInterface
from source.WarstwaBiznesowa.ModeleBLL.KontoPrywatneBLL import KontoPrywatneBLL
from source.WarstwaBiznesowa.ModeleBLL.RezerwacjaBLL import RezerwacjaBLL
from source.WarstwaBiznesowa.SystemMailingowy.Publikujacy import Publikujacy
from source.WarstwaBiznesowa.SystemMailingowy.Obserwator import Obserwator
from typing import *
from source.WarstwaBiznesowa.wyjatki import *
from source.BazaDanych.Modele.Rezerwacja import Rezerwacja


class KontrolerKontaPrywatnego(KontrolerModeluInterface, Publikujacy):

    def __init__(self):
        if BazaDanych.db_session is None:
            raise BladWBazieDanychError("Baza danych niezostała zainicjowana!")

        self.__sesja: scoped_session = BazaDanych.db_session
        self.__obserwatorzy: List[Obserwator] = []

    def dodajObiekt(self, obiekt: KontoPrywatneBLL) -> int:
        nowyObiekt = KontoPrywatne(obiekt.Imie, obiekt.Nazwisko, obiekt.Adres_Email, obiekt.Numer_Telefonu, obiekt.Haslo)
        try:
            self.__sesja.add(nowyObiekt)
            self.__sesja.commit()
            if len(self.__obserwatorzy) > 0:
                self.powiadomObeserwatora(obiekt)
            self.__sesja.refresh(nowyObiekt)
            return nowyObiekt.ID_Konta
        except Exception as e:
            raise BladZapisuDoBazyDanych(e)
        finally:
            self.__sesja.remove()


    def usunObiekt(self, id: int):
        if self.__sesja.query(Rezerwacja).filter(Rezerwacja.Id_Rezerwujacego == id).one_or_none():
            raise BladWBazieDanychError("Nie mozna usunac konta z aktywnymi rezerwacjami")
        try:
            self.__sesja.query(KontoPrywatne).filter(KontoPrywatne.ID_Konta == id).delete()
            self.__sesja.commit()
            self.__sesja.remove()
        except Exception as e:
            self.__sesja.remove()
            raise BladWBazieDanychError(e)

    def pobierzObiekt(self, id: int) -> KontoPrywatneBLL:
        konto = self.__sesja.query(KontoPrywatne).filter(KontoPrywatne.ID_Konta == id).one_or_none()

        rezerwacje = None
        if hasattr(konto, "rezerwacje"):
            try:
                rezerwacje = [
                    RezerwacjaBLL(
                        x.Id_Rezewacji, x.do_Zaplaty, x.Id_Rezerwujacego,
                        x.Id_Sali, x.Id_Terminu
                    )
                    for x in konto.rezerwacje
                ]
            except Exception as e:
                raise BladWKontrolerzeModeliError(e)
                
        self.__sesja.remove()
        try:
            pobrany = KontoPrywatneBLL(konto.ID_Konta, konto.Imie, konto.Nazwisko,
                                   konto.Adres_Email, konto.Numer_Telefonu,
                                   konto.Haslo, rezerwacje) if konto is not None else None
        except (TypeError, ValueError) as e:
            raise BladWKontrolerzeModeliError(e)
            
        if pobrany is None:
            raise BladWKontrolerzeModeliError("Nie znaleziono")
        return pobrany

    def pobierzWszystkieObiekty(self) -> List[KontoPrywatneBLL]:
        data = self.__sesja.query(KontoPrywatne)
        konta = []
        for konto in data:
            rezerwacje = None
            if hasattr(konto, "rezerwacje"):
                try:
                    rezerwacje = [
                        RezerwacjaBLL(
                            x.Id_Rezewacji, x.do_Zaplaty, x.Id_Rezerwujacego,
                            x.Id_Sali, x.Id_Terminu
                        )
                        for x in konto.rezerwacje
                    ]
                except (TypeError, ValueError)  as e:
                    raise BladWKontrolerzeModeliError(e)
                    
            print(konto.Numer_Telefonu)
            try:
                konta.append(KontoPrywatneBLL(konto.ID_Konta, konto.Imie, konto.Nazwisko,
                             konto.Adres_Email, konto.Numer_Telefonu,
                             konto.Haslo, konto.rezerwacje))
            except (TypeError, ValueError)  as e:
                    raise BladWKontrolerzeModeliError(e)
                    
        self.__sesja.remove()
        return konta

    def zaktualizujObiekt(self, stary_id: int, nowy: KontoPrywatneBLL):
        stary = self.__sesja.query(KontoPrywatne).filter(KontoPrywatne.ID_Konta == stary_id).one_or_none()
        if stary is None:
            raise BladWKontrolerzeModeliError("Nie mozna zaktualizowac modelu")
        try:
            stary.Imie = nowy.Imie
            stary.Nazwisko = nowy.Nazwisko
            stary.Adres_Email = nowy.Adres_Email
            stary.Numer_Telefonu = nowy.Numer_Telefonu
            stary.Haslo = nowy.Haslo
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

    # self.ID_Konta = id
    # self.Imie = name
    # self.Nazwisko = surname
    # self.Adres_Email = mail
    # self.Haslo = psw
    # self.Numer_Telfonu = phone

