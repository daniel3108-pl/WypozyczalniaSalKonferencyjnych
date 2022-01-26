import re


class KontoPrywatneBLL:

    def __init__(self, id: int = None, name: str = None, surname: str = None, mail: str = None, phone: str = None, psw: str = None, rezerwacje=[]):

        # Walidacja danych dla konta prywatnego, chyba najprostsza metoda
        # isinstacne(obiekt, typ) sprawdza czy typ danych sie zgadza
        # raise TypeError, wyrzuca wyjatek typu TypeError
        # len(obiekt) dlugosc stringa lub tablicy,  re.match
        # w widokach w Warstwie Prezentacji try: except TypeError as e: wyrzuca info dla frontendu
        if not isinstance(id, int) or not id >= 0:
            raise TypeError("Nie poprawny typ danych dla pola id")
        if not isinstance(name, str) or len(name) < 3:
            raise TypeError("Nie poprawny typ danych dla pola imie")
        if not isinstance(surname, str) or len(surname) < 3:
            raise TypeError("Nie poprawny typ danych dla pola nazwisko")
        if not isinstance(mail, str) or re.match(r'^\w+@[a-zA-Z_0-9]+?\.[a-zA-Z]{2,3}$', mail) is None:
            print(mail)
            raise TypeError("Nie poprawny typ danych dla pola Email")
        if not isinstance(psw, str) or len(psw) < 4:
            raise TypeError("Nie poprawny typ danych dla pola haslo lub za krotkie")
        if not isinstance(phone, str) or re.match(r'[0-9]{3}-[0-9]{3}-[0-9]{3}', phone) is None:
            print(phone)
            raise TypeError("Nie poprawny typ danych dla pola Numer_Telefonu")

        self.ID_Konta: int = id
        self.Imie: str = name
        self.Nazwisko: str = surname
        self.Adres_Email: str = mail
        self.Haslo: str = psw
        self.Numer_Telefonu: str = phone
        self.Rezerwacje: list = rezerwacje

    def toDict(self):
        return { "id": self.ID_Konta, "imie": self.Imie, "nazwisko": self.Nazwisko, "AdresEmail": self.Adres_Email,
                 "haslo": self.Haslo, "numer_tel": self.Numer_Telefonu,
                 "rezerwacje": [r.toDict() for r in self.Rezerwacje] if self.Rezerwacje else None }
