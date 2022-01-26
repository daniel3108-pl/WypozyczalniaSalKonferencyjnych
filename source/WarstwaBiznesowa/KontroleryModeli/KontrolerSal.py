
from source.BazaDanych.BazaDanych import BazaDanych
from source.BazaDanych.Modele.Termin import Termin
from source.WarstwaBiznesowa.KontroleryModeli.KontrolerModeluInterface import KontrolerModeluInterface
from sqlalchemy.orm import scoped_session
from source.BazaDanych.BazaDanych import BazaDanych
from source.BazaDanych.Modele.Sala import Sala
from source.WarstwaBiznesowa.KontroleryModeli.KontrolerModeluInterface import KontrolerModeluInterface
from source.WarstwaBiznesowa.ModeleBLL.SalaBLL import SalaBLL
from source.WarstwaBiznesowa.ModeleBLL.TerminBLL import TerminBLL
from source.WarstwaBiznesowa.SystemMailingowy import Obserwator
from source.WarstwaBiznesowa.SystemMailingowy.Publikujacy import Publikujacy
from typing import List
from source.WarstwaBiznesowa.wyjatki import *


class KontrolerSal(KontrolerModeluInterface, Publikujacy):

    def __init__(self):
        if BazaDanych.db_session is None:
            raise BladWBazieDanychError("Baza danych niezostała zainicjowana!")

        self.__sesja: scoped_session = BazaDanych.db_session
        self.__obserwatorzy: List[Obserwator] = []

    def dodajObiekt(self, obiekt: SalaBLL) -> int:
        nowyObiekt = Sala(obiekt.Adres, obiekt.Cena, obiekt.Rozmiar, obiekt.Liczba_miejsc, obiekt.Wyposazenie,
                          obiekt.Dodatkowe_informacje, obiekt.Wolna, obiekt.Id_Wynajmujacego)
        try:
            self.__sesja.add(nowyObiekt)
            self.__sesja.commit()
            if len(self.__obserwatorzy) > 0:
                self.powiadomObeserwatora(obiekt)
            self.__sesja.refresh(nowyObiekt)
            self.__sesja.remove()
            return nowyObiekt.Id_sali

        except Exception as e:
            raise BladZapisuDoBazyDanych(e)
        finally:
            self.__sesja.remove()


    def usunObiekt(self, id: int):
        try:
            self.__sesja.query(Sala).filter(Sala.Id_sali == id).delete()
            self.__sesja.query(Termin).filter(Termin.Id_Sali == id).delete()
            self.__sesja.commit()
            self.__sesja.remove()
        except Exception as e:
            self.__sesja.remove()
            raise BladWBazieDanychError(e)

    def pobierzObiekt(self, id: str) -> SalaBLL:
        sala = self.__sesja.query(Sala).filter(Sala.Id_sali == id).one_or_none()
        self.__sesja.remove()

        terminysali = self.__sesja.query(Termin).filter(Termin.Id_Sali == id)
        terminy = None
        if terminysali is not None:
            terminy = [ ]
            for x in terminysali:
                try:
                    terminy.append(TerminBLL(
                       x.Id_Terminu, x.Data_i_godzina_Rozpoczecia, x.Data_i_godzina_Zakonczenia, x.Wolny, x.Id_Sali
                    ))
                except (ValueError, TypeError) as e:
                    continue
        if not terminy:
            return None

        try:
            pobrany = SalaBLL(sala.Id_sali, sala.Adres, sala.Cena, sala.Rozmiar, sala.Liczba_miejsc, sala.Wyposazenie,
                          sala.Dodatkowe_informacje, sala.Wolna, sala.Id_Wynajmujacego, terminy) if sala is not None else None
        except (TypeError, ValueError) as e:
            raise BladWKontrolerzeModeliError(e)
            
        if pobrany is None:
            raise BladWKontrolerzeModeliError("Nie znaleziono")

        return pobrany

    def pobierzWszystkieObiekty(self) -> List[SalaBLL]:
        data = self.__sesja.query(Sala)
        self.__sesja.remove()
        sale = []
        for x in data:
            terminy = []
            for y in x.terminy:
                try:
                    terminy.append(TerminBLL(y.Id_Terminu, y.Data_i_godzina_Rozpoczecia, y.Data_i_godzina_Zakonczenia, y.Wolny,
                              y.Id_Sali))
                except (TypeError, ValueError) as e:
                    continue

            if not terminy:
                continue

            sala = SalaBLL(x.Id_sali, x.Adres, x.Cena, x.Rozmiar, x.Liczba_miejsc, x.Wyposazenie, x.Dodatkowe_informacje,
                        x.Wolna, x.Id_Wynajmujacego, terminy)
            sale.append(sala)

        return sale

    def zaktualizujObiekt(self, stary_id: int, nowy: SalaBLL):
        """
        Do nowego obiektu, terminy dajemy tylko te dodatkowe, nie dawac starych, bo sie powtorza
        """
        stary = self.__sesja.query(Sala).filter(Sala.Id_sali == stary_id).one_or_none()
        if stary is None:
            raise BladWKontrolerzeModeliError("Nie mozna zaktualizowac modelu")
        try:
            stary.Adres = nowy.Adres
            stary.Cena = nowy.Cena
            stary.Rozmiar = nowy.Rozmiar
            stary.Liczba_miejsc = nowy.Liczba_miejsc
            stary.Wyposazenie = nowy.Wyposazenie
            stary.Dodatkowe_informacje = nowy.Dodatkowe_informacje
            stary.Id_Wynajmujacego = nowy.Id_Wynajmujacego
            stary.Wolna = nowy.Wolna
            if hasattr(nowy, 'terminy') and len(nowy.terminy) > 0:
                terminy = [Termin(t.Data_i_godzina_Rozpoczecia, t.Data_i_godzina_Zakonczenia,
                              t.wolny, t.Id_Sali) for t in nowy.terminy]
                for t in terminy:
                    stary.terminy.append(t)

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



    # def __init__(self, id, adres, cena, rozmiar, licz_miej, wypos, dod, id_wyn):
    #     self.id = id
    #     self.Adres = adres
    #     self.Cena = cena
    #     self.Rozmiar = rozmiar
    #     self.Liczba_miejsc = licz_miej
    #     self.Wyposazenie = wypos
    #     self.Dodatkowe_informacje = dod
    #     self.Id_Wynajmujacego = id_wyn

    # self.Id_Terminu = id
    # self.Data_i_godzina_Rozpoczecia = od
    # self.Data_i_godzina_Zakonczenia = do
    # self.wolny = wolny
    # self.Id_Sali = id_sali