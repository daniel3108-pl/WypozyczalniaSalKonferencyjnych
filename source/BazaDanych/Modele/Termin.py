from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from source.BazaDanych.BazaDanych import BazaDanych

class Termin(BazaDanych.Base):
    __tablename__ = "Terminy"

    Id_Terminu = Column(Integer, primary_key=True)
    Data_i_godzina_Rozpoczecia = Column(DATETIME, nullable=false)
    Data_i_godzina_Zakonczenia = Column(DATETIME, nullable=false)
    Wolny = Column(BOOLEAN, nullable=false)
    Id_Sali = Column(Integer, ForeignKey('Sale.Id_sali', ondelete="CASCADE"), nullable=false)

    def __init__(self, od, do, wolny, id_sali):
        self.Data_i_godzina_Rozpoczecia = od
        self.Data_i_godzina_Zakonczenia = do
        self.Id_Sali = id_sali
        self.Wolny = wolny

