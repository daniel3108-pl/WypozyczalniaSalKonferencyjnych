from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from source.BazaDanych.BazaDanych import BazaDanych
from source.BazaDanych.Modele.Sala import Sala

class KontoFirmowe(BazaDanych.Base):
    __tablename__ = 'KontaFirmowe'

    ID_Konta = Column(Integer, primary_key=True)
    Nazwa_Firmy = Column(String(200), unique=True)
    Adres_Email = Column(String(50), unique=True)
    Haslo = Column(String(50))
    Numer_Telefonu = Column(String(16))
    KontoDoWplat = Column(String(25))
    Sale = relationship("Sala", backref="Sale.Id_Wynajmujacego")

    def __init__(self, name=None, mail=None, phone=None, psw=None, kontobank=None, sale=[]):
        self.Nazwa_Firmy = name
        self.Adres_Email = mail
        self.Haslo = psw
        self.Numer_Telefonu = phone
        self.KontoDoWplat = kontobank
        self.Sale = sale
