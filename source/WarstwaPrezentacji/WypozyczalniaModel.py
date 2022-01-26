

from flask import *
import config as Konfiguracje

from .KontroleryWidokow.WidokStronyStart import WidokStronyStartowej
from .KontroleryWidokow.WidokKontaFirmowego import WidokKontaFirmowego
from .KontroleryWidokow.WidokKontaPrywatnego import WidokKontaPrywatnego
from source.WarstwaBiznesowa.PosrednikBazyDanych import PosrednikBazyDanych


class WypozyczalniaModel(Flask):
    """
    Klasa tworzaca obiekt aplikacji Wypozyczalnia, ktory jest serwerem Flask
    """
    def __init__(self, name: str):
        """
        Konstruktor Wypozyczalni
        :param name: Parametr nazwa pliku, z ktorego jest uruchamiany serwer (plik o nazwie __main__, uruchamiany z terminala)
        """
        super().__init__(name, template_folder=Konfiguracje.TEMPLATE_FOLDER)

        self.config['SECRET_KEY'] = Konfiguracje.SECRET_KEY
        self.config['PERMANENT_SESSION_LIFETIME'] = Konfiguracje.PERMANENT_SESSION_LIFETIME
        PosrednikBazyDanych.przygotujBazeDanych(Konfiguracje.PRODUCTION_DATABASE_URI,
                                                Konfiguracje.CHECK_SAME_THREAD_DB)

        WidokStronyStartowej.register(self, route_base="/")
        WidokKontaPrywatnego.register(self, route_base="/WidokKontPryw")
        WidokKontaFirmowego.register(self, route_base="/WidokKontFirm")

    def start(self):
        """
        Uruchamia serwer o podanym w konfiguracji ip, porcie i czy ma byc w trybie debug
        :return:
        """
        self.run(host=Konfiguracje.HOST, port=Konfiguracje.PORT, debug=Konfiguracje.DEBUG)
