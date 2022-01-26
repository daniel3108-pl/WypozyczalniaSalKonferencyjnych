import re


class SalaBLL:

    def __init__(self, id: int, adres: str, cena: float, rozmiar: float, licz_miej: int, wypos: str, dod: str, wolna: bool, id_wyn: int, terminy: list=None):

        if not isinstance(id, int) or not id >= 0:
            raise TypeError("Nie poprawny typ danych dla pola id")
        if not isinstance(adres, str) or len(adres) < 4:
            raise TypeError("Nie poprawny typ danych dla pola adres")
        if not isinstance(cena, float) and not isinstance(cena, int) or not cena > 0:
            raise TypeError("Nie poprawny typ danych dla pola cena")
        if not isinstance(rozmiar, float) and not isinstance(rozmiar, int) or not rozmiar > 0:
            raise TypeError("Nie poprawny typ danych dla pola Rozmiar")
        if not isinstance(licz_miej, int) or not licz_miej > 0:
            raise TypeError("Nie poprawny typ danych dla pola Liczba miejsc")
        if not isinstance(wypos, str) or len(wypos) < 4:
            raise TypeError("Nie poprawny typ danych dla pola Wyposażenie")
        if not isinstance(dod, str):
            raise TypeError("Nie poprawny typ danych dla pola Dodatkowe informacje")
        if not isinstance(wolna, bool):
            raise TypeError("Nie poprawny typ danych dla pola Wolna")
        if not isinstance(id_wyn, int) or not id_wyn >= 0:
            raise TypeError("Nie poprawny typ danych dla pola id wynajmu")
        if not isinstance(terminy, list) and terminy:
            raise TypeError("Nie poprawny typ danych dla pola Terminy")

        self.id_sali: int = id
        self.Adres: str = adres
        self.Cena: float = cena
        self.Rozmiar: float = rozmiar
        self.Liczba_miejsc: int = licz_miej
        self.Wyposazenie: str = wypos
        self.Dodatkowe_informacje: str = dod
        self.Wolna: bool = wolna
        self.Id_Wynajmujacego: int = id_wyn
        self.terminy: list = terminy

    def toDict(self):
        return { "id_sali": self.id_sali, 'Adres': self.Adres, 'Cena': self.Cena, 'Rozmiar': self.Rozmiar,
                 'LiczbaMiejsc': self.Liczba_miejsc, 'Wyposazenie': self.Wyposazenie, 'Dodatkowe_info': self.Dodatkowe_informacje,
                 'id_wynajmujacego': self.Id_Wynajmujacego, 'wolna':self.Wolna, 'terminy': [t.toDict() for t in self.terminy] if self.terminy else None}


