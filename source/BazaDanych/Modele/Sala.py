from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from source.BazaDanych.BazaDanych import BazaDanych
from source.BazaDanych.Modele.Termin import Termin

class Sala(BazaDanych.Base):
    __tablename__ = "Sale"

    Id_sali = Column(Integer, primary_key=true)
    Adres = Column(String(200), nullable=false)
    Cena = Column(REAL, nullable=false)
    Rozmiar = Column(REAL)
    Liczba_miejsc = Column(Integer)
    Wyposazenie = Column(String(300))
    Dodatkowe_informacje = Column(String(300))
    Wolna = Column(BOOLEAN, nullable=False)
    Id_Wynajmujacego = Column(Integer, ForeignKey('KontaFirmowe.ID_Konta', ondelete="CASCADE"), nullable=false)

    terminy = relationship('Termin', backref="Terminy.Id_Sali")

    def __init__(self, adres, cena, rozmiar, licz_miej, wypos, dod, wolna, id_wyn, terminy=[]):
        self.Adres = adres
        self.Cena = cena
        self.Rozmiar = rozmiar
        self.Liczba_miejsc = licz_miej
        self.Wyposazenie = wypos
        self.Dodatkowe_informacje = dod
        self.Wolna = wolna
        self.Id_Wynajmujacego = id_wyn
        self.terminy = terminy

