from source.BazaDanych.Modele.KontoFirmowe import KontoFirmowe
from source.BazaDanych.BazaDanych import BazaDanych
from sqlalchemy.orm import scoped_session
from .KontrolerModeluInterface import KontrolerModeluInterface
from source.WarstwaBiznesowa.ModeleBLL.KontoFirmoweBLL import KontoFirmoweBLL
from source.WarstwaBiznesowa.ModeleBLL.RezerwacjaBLL import RezerwacjaBLL
from source.WarstwaBiznesowa.SystemMailingowy.Publikujacy import Publikujacy
from source.WarstwaBiznesowa.SystemMailingowy.Obserwator import Obserwator
from typing import *
from source.WarstwaBiznesowa.ModeleBLL.SalaBLL import SalaBLL
from source.WarstwaBiznesowa.wyjatki import *



class KontrolerKontaFirmowego(KontrolerModeluInterface, Publikujacy):

    def __init__(self):
        if BazaDanych.db_session is None:
            raise BladWBazieDanychError("Baza danych niezostała zainicjowana!")

        self.__sesja: scoped_session = BazaDanych.db_session
        self.__obserwatorzy: List[Obserwator] = []

    def dodajObiekt(self, obiekt: KontoFirmoweBLL) -> int:
        nowyObiekt = KontoFirmowe(obiekt.Nazwa_Firmy, obiekt.Adres_Email, obiekt.Numer_Telefonu, obiekt.Haslo,  obiekt.KontoDoWplat) 
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
        try:
            self.__sesja.query(KontoFirmowe).filter(KontoFirmowe.ID_Konta == id).delete()
            self.__sesja.commit()
            self.__sesja.remove()
        except Exception as e:
            self.__sesja.remove()
            raise BladWBazieDanychError(e)

    def pobierzObiekt(self, id: int) -> KontoFirmoweBLL:
        konto = self.__sesja.query(KontoFirmowe).filter(KontoFirmowe.ID_Konta == id).one_or_none()
        if konto is None:
            self.__sesja.remove()
            raise BladWKontrolerzeModeliError('Nie znaleziono')

        if hasattr(konto, 'Sale'):
            try:
                sale = [SalaBLL(x.Id_sali, x.Adres, x.Cena, x.Rozmiar, x.Liczba_miejsc, x.Wyposazenie, x.Dodatkowe_informacje,
                                x.Wolna, x.Id_Wynajmujacego) for x in konto.Sale]
            except (TypeError, ValueError) as e:
                raise BladWKontrolerzeModeliError(e)
        else:
            sale = None
        self.__sesja.remove()

        pobrany = None
        try:
            pobrany = KontoFirmoweBLL(konto.ID_Konta, konto.Nazwa_Firmy, konto.Adres_Email,
                                  konto.Numer_Telefonu, konto.Haslo, konto.KontoDoWplat, sale) if konto is not None else None
        except (TypeError, ValueError) as e:
            raise BladWKontrolerzeModeliError(e)

        return pobrany

    def pobierzWszystkieObiekty(self) -> List[KontoFirmoweBLL]:
        data = self.__sesja.query(KontoFirmowe)
        self.__sesja.remove()
        if hasattr(data, 'Sale'):
            try:
                sale = [SalaBLL(x.Id_sali, x.Adres, x.Cena, x.Rozmiar, x.Liczba_miejsc, x.Wyposazenie, x.Dodatkowe_informacje,
                                x.Wolna, x.Id_Wynajmujacego) for x in data.Sale]
            except (TypeError, ValueError)  as e:
                raise BladWKontrolerzeModeliError(e)
        else:
            sale = None
        return [KontoFirmoweBLL(x.ID_Konta, x.Nazwa_Firmy, x.Adres_Email, x.Numer_Telefonu,
                                x.Haslo, x.KontoDoWplat, sale) for x in data]


    def zaktualizujObiekt(self, stary_id: int, nowy: KontoFirmoweBLL):
        stary = self.__sesja.query(KontoFirmowe).filter(KontoFirmowe.ID_Konta == stary_id).one_or_none()
        if stary is None:
            raise Exception("Nie mozna zaktualizowac modelu")
        try:
            stary.Nazwa_Firmy = nowy.Nazwa_Firmy
            stary.KontoDoWplat = nowy.KontoDoWplat
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



