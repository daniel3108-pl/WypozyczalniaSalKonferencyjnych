
from datetime import datetime, timedelta
import re
from typing import *

class TerminBLL:
    def __init__(self, id: int, od: datetime, do: datetime, wolny: bool, id_sali: int):

        if not isinstance(id, int) or not id >=0:
            raise TypeError("Niepoprawny typ danych dla pola id")
        if not isinstance(id_sali, int) or not id_sali >= 0:
            raise TypeError("Niepoprawny typ danych dla pola id_sali")
        if not isinstance(od, str) and not isinstance(od, datetime):
            raise TypeError("Niepoprawny typ danych dla Data i godzina rozpoczecia")
        if not isinstance(do, str) and not isinstance(do, datetime):
            raise TypeError("Niepoprawny typ danych dla Data i godzina zakonczenia")
        if not isinstance(wolny, bool):
            raise TypeError("Niepoprawny typ danych dla pola wolny")

        try:
            od = datetime.strptime(od, "%d.%m.%Y %H:%M") if isinstance(od, str) else od
            do = datetime.strptime(do, "%d.%m.%Y %H:%M") if isinstance(do, str) else do
        except ValueError as e:
            raise e
        if (od - datetime.now()).days < 0:
            raise ValueError("Czas od i do nie moze byc starszy niz dzisiejsza data")
        if (do - od).days < 0:
            raise ValueError("Czas zakonczenia nie moze byc wczesniej niz czas rozpoczecia")


        self.Id_Terminu: int = id
        self.Data_i_godzina_Rozpoczecia: datetime = od
        self.Data_i_godzina_Zakonczenia: datetime = do
        self.wolny: bool = wolny
        self.Id_Sali: int = id_sali

    def toDict(self):
        return { "id": self.Id_Terminu, "Data_i_godzina_Rozpoczecia": datetime.strftime(self.Data_i_godzina_Rozpoczecia, "%d.%m.%Y %H:%M"),
                 "Data_i_godzina_Zakonczenia": datetime.strftime(self.Data_i_godzina_Zakonczenia, "%d.%m.%Y %H:%M"),
                 "wolny": self.wolny, "id_sali": self.Id_Sali}
