import re

class KontoFirmoweBLL:

    def __init__(self, id: int = None, name: str = None, mail: str = None, phone: str = None, psw: str = None, kontobank: str = None, sale: list =[]):
        if not isinstance(id, int) or not id >= 0:
            raise TypeError("Niepoprawny typ danych dla pola id")
        if not isinstance(name, str) or len(name) < 3:
            raise TypeError("Niepoprawny typ danych dla pola imie")
        if not isinstance(mail, str) or re.match(r'^\w+@[a-zA-Z_0-9]+?\.[a-zA-Z]{2,3}$', mail) is None:
            print(mail)
            raise TypeError("Niepoprawny typ danych dla pola Email")
        if not isinstance(psw, str) or len(psw) < 4:
            raise TypeError("Niepoprawny typ danych dla pola haslo lub za krotkie")
        if not isinstance(phone, str) or re.match(r'[0-9]{3}-[0-9]{3}-[0-9]{3}', phone) is None:
            print(phone)
            raise TypeError("Niepoprawny typ danych dla pola Numer_Telefonu")
        if not isinstance(kontobank, str) or len(kontobank) != 26:
            raise TypeError("Niepoprawny typ danych dla pola KontoDoWplat")

        self.ID_Konta: int = id
        self.Nazwa_Firmy: str = name
        self.Adres_Email: str = mail
        self.Haslo: str = psw
        self.Numer_Telefonu: str = phone
        self.KontoDoWplat: str = kontobank
        self.Sale: list = sale

    def toDict(self):
        return { "id": self.ID_Konta,
                "nazwafirmy": self.Nazwa_Firmy,
                "email": self.Adres_Email,
                "numertelefonu": self.Numer_Telefonu,
                "haslo": self.Haslo,
                "kontoBank": self.KontoDoWplat,
                "sale": [ s.toDict() for s in self.Sale ] if self.Sale else None}
