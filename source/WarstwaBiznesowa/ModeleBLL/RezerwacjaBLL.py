
class RezerwacjaBLL:

    def __init__(self, id: int = None, do_zap: float = None, id_rez: int = None, id_sali: int = None, id_terminu: int = None):

        if not isinstance(id, int) or not id >= 0:
            raise TypeError("Niepoprawny typ danych dla pola id")
        if not isinstance(id_sali, int) or not id_sali >= 0:
            raise TypeError("Niepoprawny typ danych dla pola id_sali")
        if not isinstance(id_terminu, int) or not id_terminu >= 0:
            raise TypeError("Niepoprawny typ danych dla pola id_terminu")
        if not isinstance(id_rez, int) or not id_rez >= 0:
            raise TypeError("Niepoprawny typ danych dla pola id_rezerwujacego")
        if not isinstance(do_zap, int) and not isinstance(do_zap, float) or not do_zap >= 0:
            raise TypeError("Niepoprawny typ danych dla pola do_zaplaty")


        self.Id_Rezerwacji: int = id
        self.Id_Sali: int = id_sali
        self.do_Zaplaty: float = do_zap
        self.Id_Rezerwujacego: int = id_rez
        self.Id_Terminu: int = id_terminu

    def toDict(self):
        return { "Id_Rezerwacji": self.Id_Rezerwacji, "Id_Sali": self.Id_Sali,
                 "Do_zaplaty": self.do_Zaplaty, 'Id_Rezerwujacego': self.Id_Rezerwujacego,
                 'Id_Terminu': self.Id_Terminu }
