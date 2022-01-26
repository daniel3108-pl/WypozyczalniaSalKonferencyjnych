import random

from flask_classful import FlaskView, route
from flask import render_template, request, redirect, url_for, session, flash

from source.WarstwaBiznesowa.ModeleBLL.KontoFirmoweBLL import KontoFirmoweBLL
from source.WarstwaBiznesowa.ModeleBLL.KontoPrywatneBLL import KontoPrywatneBLL
from source.WarstwaBiznesowa.PosrednikBazyDanych import PosrednikBazyDanych, TypModelu
from source.WarstwaBiznesowa.SystemMailingowy.SystemMailingowy import SystemMailingowy
from source.WarstwaBiznesowa.wyjatki import *
import os

class WidokStronyStartowej(FlaskView):
    """
    Klasa odpowiedzialna za widoki stron interfejsu strony startowej
    """
    @route('/logowanieKontoFrimowe/', methods=["GET", "POST"])
    def Logowanie_doKontaFirmowego(self):
        """
        Metoda wywolujaca strone logowania dla metody GET dla konta firmowego, i logujaca uzytkownika dla metody POST dal podanych danych w formularzu http
        :return: szablon strony html z formularzem logowaniu lub przekierowuje do interfejsu konta firmowego gdy uzytkownik sie zalogowal
        """
        if request.method == "GET":
            return render_template('StronaStartowa/FormularzLogowaniaFirm.html')
        else:
            passwd = request.form['psw']
            mail = request.form['mail']
            baza = PosrednikBazyDanych(typ=TypModelu.KontoFirmowe)
            konta = baza.pobierzWszystkieObiekty()
            konto = [x for x in konta if x.Adres_Email == mail]
            if len(konto) == 1 and konto[0].Haslo == passwd:
                session["email"] = mail
                session["konto_id"] = konto[0].ID_Konta
                print(session["konto_id"])
                return redirect(url_for("WidokKontaFirmowego:stronaPoczatkowa"))
            else:
                flash("Bledne dane logowania")
                return redirect(url_for("WidokStronyStartowej:Logowanie_doKontaFirmowego"))

    @route('/logowanieKontoPryw/', methods=["GET", "POST"])
    def Logowanie_doKontaPrywatnego(self):
        """
        Metoda wywolujaca strone logowania dla metody GET dla konta prywatnego,
        i logujaca uzytkownika dla metody POST dla podanych danych w formularzu http
        :return: szablon html z formularzem logowania lub przekierowanie do interfejsu konta prywatnego gyd uzytkownik sie zaloguje
        """
        if request.method == "GET":
            return render_template('StronaStartowa/FormularzLogowaniaPryw.html')
        else:
            passwd = request.form['psw']
            mail = request.form['mail']
            baza = PosrednikBazyDanych(typ=TypModelu.KontoPrywatne)
            konta = baza.pobierzWszystkieObiekty()
            konto = [x for x in konta if x.Adres_Email == mail]
            if len(konto) == 1 and konto[0].Haslo == passwd:
                session["email"] = mail
                session["konto_id"] = konto[0].ID_Konta
                print(session["konto_id"])
                return redirect(url_for("WidokKontaPrywatnego:stronaPoczatkowa"))
            else:
                flash("Bledne dane logowania")
                return redirect(url_for("WidokStronyStartowej:Logowanie_doKontaPrywatnego"))

    @route('/weryfikujEmailFirmowy/', methods=["GET", "POST"])
    def potwierdzEmailFirmowy(self):
        """
        Metoda wywolujaca strone do podania kodu weryfikujacego email dla metody GET dla konta firmowego,
        lub dla metody POST sprawdza kod i tworzy konto jestli byl on poprawny
        :return: szablon html dla formularza do wpisania kodu, lub przekierowanie do logowania do konta firmowego
        """
        if request.method == "GET":
            return render_template('StronaStartowa/weryfikacjaEmaila.html')
        else:
            kontodict = session.get('accountToSave')
            kod = session.get('kodweryfikujacy')
            if request.form['kod'] == kod:
                try:
                    noweKonto = KontoFirmoweBLL(0, kontodict["nazwafirmy"], kontodict['email'], kontodict['numertelefonu'],
                                            kontodict['haslo'], kontodict['kontoBank'])
                except TypeError as e:
                    flash("Błąd modelu konta firmowego!")
                    return redirect(url_for("WidokStronyStartowej:Rejestracja_KontaFirmowego"))
                    
                bazadanych = PosrednikBazyDanych(TypModelu.KontoFirmowe)
                mailing = SystemMailingowy(bazadanych.kontrolerModelu)
                try:
                    id = bazadanych.dodajObiekt(noweKonto)
                except BladZapisuDoBazyDanych as e:
                    flash("Istnieje już konto o podanym adresie email.")
                    return redirect(url_for("WidokStronyStartowej:Rejestracja_KontaFirmowego"))
                session.pop('kodweryfikujacy')
                session.pop('accountToSave')
                flash("Poprawnie zalozono konto, Mozesz sie zalogowac")
                return redirect(url_for("WidokStronyStartowej:Logowanie_doKontaFirmowego"))
            else:
                flash("Nie poprawny kod")
                return redirect(url_for("WidokStronyStartowej:potwierdzEmailFirmowy"))

    @route('/weryfikujEmailPrywatny/', methods=["GET", "POST"])
    def potwierdzEmailPrywatny(self):
        """
        Metoda wywolujaca strone do podania kodu weryfikujacego email dla metody GET dla konta prywatnego,
        lub dla metody POST sprawdza kod i tworzy konto jestli byl on poprawny
        :return: szablon html dla formularza do wpisania kodu, lub przekierowanie do logowania do konta prywatnego
        """
        if request.method == "GET":
            return render_template('StronaStartowa/weryfikacjaEmaila.html')
        else:
            kontodict = session.get('accountToSave')
            kod = session.get('kodweryfikujacy')
            if request.form['kod'] == kod:
                try:
                    noweKonto = KontoPrywatneBLL(0, kontodict["imie"], kontodict['nazwisko'], kontodict["AdresEmail"],
                                              kontodict['numer_tel'], kontodict['haslo'])
                except TypeError as e:
                    flash("Błąd podzcas przekazywania danych w sesji serwera! Spróbuj zarejestrować się jeszcze raz")
                    return redirect(url_for("WidokStronyStartowej:Rejestracja_KontaPrywatnego"))
                    
                bazadanych = PosrednikBazyDanych(TypModelu.KontoPrywatne)
                mailing = SystemMailingowy(bazadanych.kontrolerModelu)
                try:
                    id = bazadanych.dodajObiekt(noweKonto)
                except BladZapisuDoBazyDanych as e:
                    flash("Istnieje już konto o podanym adresie email.")
                    return redirect(url_for("WidokStronyStartowej:Rejestracja_KontaPrywatnego"))

                session.pop('kodweryfikujacy')
                session.pop('accountToSave')
                flash("Poprawnie zalozono konto, Mozesz sie zalogowac")
                return redirect(url_for("WidokStronyStartowej:Logowanie_doKontaPrywatnego"))
            else:
                flash("Nie poprawny kod")
                return redirect(url_for("WidokStronyStartowej:potwierdzEmailPrywatny"))

    @route('/zarejestrujKontoFirmowe/', methods=["GET", "POST"])
    def Rejestracja_KontaFirmowego(self):
        """
        Metoda dla GET wyswietla formularz utworzenia konta firmowego, dla metody POST tworzy obiekt konta firmowego,
        losuje kod weryfikacyjny email i wysyla go na mail'a po czym przekierowuje do strony z weryfikacja kodu
        :return: szablon html dla tworzenia konta/ przekierowanie do strony z potwierdzeniem email'a
        """
        if request.method == "GET":
            return render_template('StronaStartowa/FormularzKontaFirm.html')
        else:
            try:
                nowyObiekt = KontoFirmoweBLL(0, request.form['nazwa'], request.form['mail'].strip(),
                                          request.form["tel"].strip(), request.form['psw'], request.form["bank"].strip())
            except TypeError as e:
                flash("Nie poprawny format danych, proszę sprawdź czy dane zgadzają się.")
                return redirect(url_for("WidokStronyStartowej:Rejestracja_KontaFirmowego"))
            
            session["accountToSave"] = nowyObiekt.toDict()
            kod = str(random.randint(1000, 9999))
            session["kodweryfikujacy"] = kod
            SystemMailingowy.wyslijMailaWeryfikujacego(kod, request.form['mail'].strip())
            return redirect(url_for("WidokStronyStartowej:potwierdzEmailFirmowy"))

    @route('/zarejestrujKontoPrywatne/', methods=["GET", "POST"])
    def Rejestracja_KontaPrywatnego(self):
        """
        Metoda dla GET wyswietla formularz utworzenia konta prywatnego, dla metody POST tworzy obiekt konta prywatnego,
        losuje kod weryfikacyjny email i wysyla go na mail'a po czym przekierowuje do strony z weryfikacja kodu
        :return: szablon html dla tworzenia konta/ przekierowanie do strony z potwierdzeniem email'a
        """
        if request.method == "GET":
            return render_template('StronaStartowa/FormularzKontaPryw.html')
        else:
            try:
                nowyObiekt = KontoPrywatneBLL(0, request.form['imie'], request.form['nazw'], request.form['mail'].strip(),
                                          request.form["tel"].strip(), request.form['psw'])
            except TypeError as e:
                flash("Nie poprawny format danych, proszę sprawdź czy dane zgadzają się.")
                return redirect(url_for("WidokStronyStartowej:Rejestracja_KontaPrywatnego"))

            session["accountToSave"] = nowyObiekt.toDict()
            kod = str(random.randint(1000, 9999))
            session["kodweryfikujacy"] = kod
            SystemMailingowy.wyslijMailaWeryfikujacego(kod, request.form['mail'].strip())
            return redirect(url_for("WidokStronyStartowej:potwierdzEmailPrywatny"))

    @route('/')
    def StronaPoczatkowa(self):
        """
        Metoda renderuje strone poczatkowa.
        :return: szablon html strony poczatkowej aplikacji dla niezalogowanego uzytkownika
        """
        return render_template('StronaStartowa/index.html')
