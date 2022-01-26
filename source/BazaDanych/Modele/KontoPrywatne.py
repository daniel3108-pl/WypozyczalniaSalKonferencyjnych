from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from source.BazaDanych.BazaDanych import BazaDanych
from source.BazaDanych.Modele.Rezerwacja import Rezerwacja

class KontoPrywatne(BazaDanych.Base):
    __tablename__ = 'KontaPrywatne'

    ID_Konta = Column(Integer, primary_key=True)
    Imie = Column(String(200))
    Nazwisko = Column(String(200))
    Adres_Email = Column(String(50), unique=True)
    Haslo = Column(String(50))
    Numer_Telefonu = Column(String(16))

    rezerwacje = relationship('Rezerwacja', backref="Rezerwacje.Id_Rezerwujacego")

    def __init__(self, name=None, surname=None, mail=None, phone=None, psw=None, rezerw=[]):
        self.Imie = name
        self.Nazwisko = surname
        self.Adres_Email = mail
        self.Haslo = psw
        self.Numer_Telefonu = phone
        self.rezerwacje = rezerw

