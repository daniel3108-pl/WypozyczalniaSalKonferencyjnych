from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.WarstwaBiznesowa.SystemMailingowy.Obserwator import Obserwator


class Publikujacy(ABC):
    @abstractmethod
    def zarejestruj(self, obserwator: 'Obserwator'):
        pass

    @abstractmethod
    def wyrejestruj(self, obserwator: 'Obserwator'):
        pass

    @abstractmethod
    def powiadomObeserwatora(self, obiekt: "Obserwator"):
        pass