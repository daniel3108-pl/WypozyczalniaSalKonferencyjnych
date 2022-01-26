from .Obserwator import Obserwator

from source.WarstwaBiznesowa.ModeleBLL.KontoPrywatneBLL import KontoPrywatneBLL
from source.WarstwaBiznesowa.ModeleBLL.KontoFirmoweBLL import KontoFirmoweBLL
from source.WarstwaBiznesowa.ModeleBLL.RezerwacjaBLL import RezerwacjaBLL
from source.WarstwaBiznesowa.ModeleBLL.SalaBLL import SalaBLL
import json
import smtplib
import config as Konfiguracje
from source.WarstwaBiznesowa.PosrednikBazyDanych import PosrednikBazyDanych
from source.WarstwaBiznesowa.KontroleryModeli.KontrolerModeluInterface import TypModelu
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Publikujacy import Publikujacy


class SystemMailingowy(Obserwator):

    IDTracker = 0

    def __init__(self, publikujacy: "Publikujacy"):
        self.__publikujacy = publikujacy
        self.__publikujacy.zarejestruj(self)

        SystemMailingowy.IDTracker += 1
        self.ID = SystemMailingowy.IDTracker

    @staticmethod
    def wyslijMailaWeryfikujacego(kod, email):
        to = email
        gmail_user = Konfiguracje.SYS_MAIL
        gmail_pwd = Konfiguracje.SYS_MAIL_PSW
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(gmail_user, gmail_pwd)
        header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + f'Subject:Kod weryfikacyjny - {email} \n'
        msg = header + f'\n Witaj:\n{to}\nOto twoj kod weryfikacyjny: {kod}\nDziekujemy za korzystanie z naszych uslug.  \n\n'
        smtpserver.sendmail(gmail_user, to, msg)
        smtpserver.quit()

    def wyslijMailaOUtworzeniuKonta(self, obiekt):
        to = obiekt.Adres_Email
        gmail_user = Konfiguracje.SYS_MAIL
        gmail_pwd = Konfiguracje.SYS_MAIL_PSW
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(gmail_user, gmail_pwd)
        header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + f'Subject:Utworzenie Konta - {to} \n'
        msg = header + f'\n Witaj:\n {to} \nUtworzylismy ci nowe konto:\n{json.dumps(obiekt.toDict(), indent=4)}\nDziekujemy za korzystanie z naszych uslug. \n\n'
        smtpserver.sendmail(gmail_user, to, msg)
        smtpserver.quit()

    def wyslijMailaZRezerwacja(self, rezerwacja, wynajmujacy, rezerwujacy):
        rezerwujacy_to = rezerwujacy.Adres_Email
        wynajmujacy_to = wynajmujacy.Adres_Email
        gmail_user = Konfiguracje.SYS_MAIL
        gmail_pwd = Konfiguracje.SYS_MAIL_PSW
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(gmail_user, gmail_pwd)
        #----------Mail Rezerwujacy-------------------------------------
        header_rezerw = 'To:' + rezerwujacy_to + '\n' + 'From: ' + gmail_user + '\n' + f'Subject:Potwierdzenie Rezerwacji\n'
        msg_rezerw = header_rezerw + f'\n Gratulacje uzytkowniku, zarezerwowales sale:\n{json.dumps(rezerwacja.toDict(), indent=4)} od {json.dumps(wynajmujacy.toDict(), indent=4)}\nDziekujemy za wybranie naszego serwisu. \n\n'
        smtpserver.sendmail(gmail_user, rezerwujacy_to, msg_rezerw)
        
        #----------Mail Wynajmujacy-------------------------------------
        header_wynajem = 'To:' + wynajmujacy_to + '\n' + 'From: ' + gmail_user + '\n' + f'Subject:Wynajem Twojej Sali\n'
        msg_wynajem = header_wynajem + f'\n Uzytkownik:{json.dumps(rezerwujacy.toDict(), indent=4)}\n Zarezerwowal twoja sale: \n{json.dumps(rezerwacja.toDict(), indent=4)}\n'
        smtpserver.sendmail(gmail_user, wynajmujacy_to, msg_wynajem)
        smtpserver.quit()

    def wyslijMailaORezygnacji(self, rezerwacja, wynajmujacy, rezygnujacy):
        rezerwujacy_to = rezygnujacy.Adres_Email
        wynajmujacy_to = wynajmujacy.Adres_Email
        gmail_user = Konfiguracje.SYS_MAIL
        gmail_pwd = Konfiguracje.SYS_MAIL_PSW
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(gmail_user, gmail_pwd)
        #----------Mail Rezerwujacy-------------------------------------
        header_rezerw = 'To:' + rezerwujacy_to + '\n' + 'From: ' + gmail_user + '\n' + f'Subject:Rezygnacja z Rezerwacji\n'
        msg_rezerw = header_rezerw + f'\n Zrezygnowales z sali :\n{json.dumps(rezerwacja.toDict(), indent=4)}\n.Szkoda ze nie chcesz ;((( \n\n'
        smtpserver.sendmail(gmail_user, rezerwujacy_to, msg_rezerw)
        
        #----------Mail Wynajmujacy-------------------------------------
        header_wynajem = 'To:' + wynajmujacy_to + '\n' + 'From: ' + gmail_user + '\n' + f'Subject:Wynajem Twojej Sali - {wynajmujacy_to} \n'
        msg_wynajem = header_wynajem + f'\n Uzytkownik:{json.dumps(rezygnujacy.toDict(), indent=4)}\n Zrezygnowal z rezerwacji sali: \n{json.dumps(rezerwacja.toDict(), indent=4)} ehhh\n'
        smtpserver.sendmail(gmail_user, wynajmujacy_to, msg_wynajem)
        smtpserver.quit()

    def zaktualizuj(self, obiektModelu: object):
        if isinstance(obiektModelu, KontoPrywatneBLL) or isinstance(obiektModelu, KontoFirmoweBLL):
            print("Wysylam maila o nowym koncie")
            self.wyslijMailaOUtworzeniuKonta(obiektModelu)
        elif isinstance(obiektModelu, RezerwacjaBLL):
            sala = PosrednikBazyDanych(TypModelu.Sale).pobierzObiekt(obiektModelu.Id_Sali)
            wynajmujacy = PosrednikBazyDanych(TypModelu.KontoFirmowe).pobierzObiekt(sala.Id_Wynajmujacego)
            rezerwujacy = PosrednikBazyDanych(TypModelu.KontoPrywatne).pobierzObiekt(obiektModelu.Id_Rezerwujacego)
            wynajmujacy.Sale = None
            rezerwujacy.Rezerwacje = None
            print(obiektModelu.do_Zaplaty)
            if obiektModelu.do_Zaplaty != 0:
                self.wyslijMailaZRezerwacja(obiektModelu, wynajmujacy, rezerwujacy)
            elif obiektModelu.do_Zaplaty == 0:
                print("Mail o rezygnacji")
                self.wyslijMailaORezygnacji(obiektModelu, wynajmujacy, rezerwujacy)