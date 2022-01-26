from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .SingletonMeta import SingletonMeta


class BazaDanych(metaclass=SingletonMeta):

    db_session: scoped_session = None
    Base: declarative_base = declarative_base()

    @classmethod
    def przygotujBazeDanych(cls, db_uri: str, check_same_thread: bool = False):
        cls.__engine = create_engine(db_uri, connect_args={"check_same_thread": check_same_thread})
        cls.db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=cls.__engine))

        cls.Base.query = cls.db_session.query_property()
        from .Modele import KontoFirmowe, KontoPrywatne, Rezerwacja, Sala, Termin
        cls.Base.metadata.create_all(bind=cls.__engine)
