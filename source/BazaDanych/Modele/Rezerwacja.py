from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from source.BazaDanych.BazaDanych import BazaDanych

class Rezerwacja(BazaDanych.Base):
    __tablename__ = "Rezerwacje"

    Id_Rezewacji = Column(Integer, primary_key=True)
    do_Zaplaty = Column(REAL)
    Id_Rezerwujacego = Column(Integer, ForeignKey('KontaPrywatne.ID_Konta', ondelete="CASCADE"), nullable=false)
    Id_Sali = Column(Integer, ForeignKey('Sale.Id_sali'), nullable=false)
    Id_Terminu = Column(Integer, ForeignKey('Terminy.Id_Terminu'), nullable=false)

    def __init__(self, do_zap, id_rez, id_sali, id_terminu):
        self.Id_Sali = id_sali
        self.do_Zaplaty = do_zap
        self.Id_Rezerwujacego = id_rez
        self.Id_Terminu = id_terminu