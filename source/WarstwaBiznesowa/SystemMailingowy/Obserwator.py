from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.WarstwaBiznesowa.SystemMailingowy.Publikujacy import Publikujacy

class Obserwator(ABC):

    @abstractmethod
    def zaktualizuj(self, obiektModelu: "Publikujacy"):
        pass