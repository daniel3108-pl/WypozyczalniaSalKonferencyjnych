from abc import ABC, abstractmethod
from enum import Enum
from typing import *


class TypModelu(Enum):
    KontoFirmowe = 1
    KontoPrywatne = 2
    Rezerwacje = 3
    Sale = 4
    Terminy = 5

class KontrolerModeluInterface(ABC):
    """
        Interface dla klas kontrolera Modelu bazy danych do uzycia przez warstwe prezentacji,
        Tutaj ma miec miejsca validacja danych (sprawdzac czy format jest ok jak jest ok to do bazy danych)
    """
    @abstractmethod
    def dodajObiekt(self, obiekt: object) -> int:
        pass

    @abstractmethod
    def usunObiekt(self, id: int) -> None:
        pass

    @abstractmethod
    def pobierzObiekt(self, id: int) -> object:
        pass

    @abstractmethod
    def pobierzWszystkieObiekty(self) -> List[object]:
        pass

    @abstractmethod
    def zaktualizujObiekt(self, stary_id: int, nowy: object) -> None:
        pass