from flask_classful import FlaskView, route
from flask import render_template, session, request, redirect, url_for, flash
import os

from source.WarstwaBiznesowa.ModeleBLL.KontoFirmoweBLL import KontoFirmoweBLL
from source.WarstwaBiznesowa.ModeleBLL.SalaBLL import SalaBLL
from source.WarstwaBiznesowa.ModeleBLL.TerminBLL import TerminBLL
from source.WarstwaBiznesowa.PosrednikBazyDanych import PosrednikBazyDanych, TypModelu
from datetime import datetime

from source.WarstwaBiznesowa.SystemMailingowy.SystemMailingowy import SystemMailingowy


class WidokKontaFirmowego(FlaskView):
    """
    Klasa kontrolujaca widoki dla interfejsu Konta firmowego
    """
    @route('/')
    def stronaPoczatkowa(self):
        """
        Wyswietla strone poczatkowa dla konta firmowego jesli jest uzytkownik zalogowany
        :return: szablon html ze strona poczatkowa konta firmowego lub przekierowanie do logowania
        """
        if "email" in session.keys() and "konto_id" in session.keys():
            return render_template('WidokKontaFirmowego/index.html')
        else:
            flash("Musisz sie zalogowac byc przejsc do tej podstrony")
            return redirect(url_for('WidokStronyStartowej:Logowanie_doKontaFirmowego'))

    @route('/daneKonta/', methods=["GET", "POST"])
    def daneKonta(self):
        """
        Wyswietla formularz z danymi uzytkownika (GET)
        Edytuje zmienione dane przez uzytkownika (POST) i przekeirowuje do logowania ponownie
        :return: szablon formularza edycji konta firmowego, przekierowanie do logowania do konta
        """
        if 'konto_id' in session.keys():
            bazadanych = PosrednikBazyDanych(TypModelu.KontoFirmowe)
            user = bazadanych.pobierzObiekt(session['konto_id'])
            user.Sale = None
            if request.method == "GET":
                return render_template("WidokKontaFirmowego/daneKonta.html", user=user.toDict())
            else:
                nowe_dane = request.form.get('psw')
                user.Haslo = nowe_dane
                bazadanych.zaktualizujObiekt(session['konto_id'], user)

                session.pop("email")
                session.pop("konto_id")
                flash("Zaktualizowano dane konta. Zaloguj sie ponownie!")
                return redirect(url_for('WidokStronyStartowej:Logowanie_doKontaFirmowego'))
        else:
            flash("Musisz sie zalogowac byc przejsc do tej podstrony")
            return redirect(url_for('WidokStronyStartowej:Logowanie_doKontaFirmowego'))


    @route('/mojeOferty/')
    def mojeOferty(self):
        """
        Wyswietla liste z ofertami wystawionymi przez konto zalogowanego
        :return: szablon html dla list ofert uzytkownika
        """
        if 'konto_id' in session.keys():
            baza = PosrednikBazyDanych(TypModelu.Sale)
            saleBaza = baza.pobierzWszystkieObiekty()
            sale = [s.toDict() for s in saleBaza if s.Id_Wynajmujacego == session['konto_id']]
            return render_template("WidokKontaFirmowego/mojeOferty.html", mojesale=sale)
        else:
            flash("Musisz sie zalogowac byc przejsc do tej podstrony")
            return redirect(url_for('WidokStronyStartowej:Logowanie_doKontaFirmowego'))

    @route('/nowaOferta/', methods=["GET", "POST"])
    def nowaOferta(self):
        """
        Metoda GET - Wyswietla formularz do uzupelnienia danych nowej sali,
        Metoda POST - Dodaje nowa sale na podstawie podanych danych przez uzytkownika i przekirowuje do listy wystawionych ofert przez konto
        :return: szablon html z formularzem dodawania nowej sali / przekierowanie do strony z ofertami konta
        """
        if 'konto_id' in session.keys():
            if request.method == "GET":
                return render_template("WidokKontaFirmowego/nowaOferta.html")
            else:
                req = request.form
                try:
                    nowaSala = SalaBLL(0, req['add'], float(req['cena']), float(req['roz']), int(req['miejsca']), req['wypos'], req['dod'], True, int(session['konto_id']))
                except (TypeError, ValueError) as e:
                    flash("Błąd modelu sali!")
                    return render_template("WidokKontaFirmowego/nowaOferta.html")
                    
                terminyod = req['termod'].split(", ")
                terminydo = req['termdo'].split(", ")
                bazaDanych = PosrednikBazyDanych(TypModelu.Sale)
                id_sali = bazaDanych.dodajObiekt(nowaSala)
                terminydb = PosrednikBazyDanych(TypModelu.Terminy)
                for i in range(len(terminyod)):
                    try:
                        nowyTerm = TerminBLL(0, datetime.strptime(terminyod[i], "%d.%m.%Y %H:%M"),
                                         datetime.strptime(terminydo[i], "%d.%m.%Y %H:%M"),
                                         wolny=True, id_sali=id_sali)
                        terminydb.dodajObiekt(nowyTerm)
                    except (TypeError, ValueError) as e:
                        flash("Błąd modelu terminów!")
                        return redirect(url_for('WidokKontaFirmowego:mojeOferty'))
                                                
                flash("Poprawnie dodano nową salę")
                return redirect(url_for('WidokKontaFirmowego:mojeOferty'))
        else:
            flash("Musisz sie zalogowac byc przejsc do tej podstrony")
            return redirect(url_for('WidokStronyStartowej:Logowanie_doKontaFirmowego'))

    @route('/rezerwacjeMoichOfert/')
    def rezerwacjeMoichOfert(self):
        """
        Wyswietla liste rezerwacji, ktore zostaly utworzone na sale wystawione przez zalogowanego uzytkownika firmowego
        :return: szablon html z lista rezerwacji
        """
        if 'konto_id' in session.keys():
            kontoPrywDB = PosrednikBazyDanych(TypModelu.KontoPrywatne)
            saleDB = PosrednikBazyDanych(TypModelu.Sale)
            terminyDB = PosrednikBazyDanych(TypModelu.Terminy)

            Rezerwacje = PosrednikBazyDanych(TypModelu.Rezerwacje).pobierzWszystkieObiekty()
            sale = [s for s in saleDB.pobierzWszystkieObiekty()
                            if s.Id_Wynajmujacego == session['konto_id']]
            sale_id = [s.id_sali for s in sale]
            Rezerwacje = [r for r in Rezerwacje if r.Id_Sali in sale_id]

            rezer = []
            for rez in Rezerwacje:
                rezerwujacy = kontoPrywDB.pobierzObiekt(rez.Id_Rezerwujacego)
                sala = saleDB.pobierzObiekt(rez.Id_Sali)
                termin = terminyDB.pobierzObiekt(rez.Id_Terminu)
                rezer.append({
                    'id_sali': rez.Id_Sali, 'imie': rezerwujacy.Imie, 'nazwisko': rezerwujacy.Nazwisko,
                    'Adres': sala.Adres, 'Email': rezerwujacy.Adres_Email, 'Cena': sala.Cena,
                    'Od': termin.Data_i_godzina_Rozpoczecia, 'Do': termin.Data_i_godzina_Zakonczenia
                })
                print(rezer)
            return render_template("WidokKontaFirmowego/rezerwacjeMoichOfert.html", mojerezer=rezer)
        else:
            flash("Musisz sie zalogowac byc przejsc do tej podstrony")
            return redirect(url_for('WidokStronyStartowej:Logowanie_doKontaFirmowego'))

    @route('/szczegolyMojejOferty/<int:id>/', methods=["GET", "POST"])
    def szczegolyMojejOferty(self, id):
        """
        Metoda GET - Wyswietla strone ze szczegolami sali o podanym id wystawionymi przez konto uzytkownika
        Metoda POST :
            - gdy w form pole methodid == "nowytermin" - dodaje podane nowe terminy przez uzytkownika w formularzu terminow
            - gdy w form pole methodid == "usun" - usuwa sale z bazy danych
        :param id: Id sali
        :return: szablon html ze szczegolami oferty, prezkierowanie do szczegolow oferty lub do listy ofert uzytkownika zalogowanego
        """
        if 'konto_id' in session.keys():

            if request.method == "GET":
                saleBD = PosrednikBazyDanych(TypModelu.Sale)
                sala = saleBD.pobierzObiekt(id).toDict()
                print(sala.get('terminy'))
                return render_template("WidokKontaFirmowego/szczegolyMojejOferty.html", sala=sala)

            elif request.method == "POST":

                if request.form['methodid'].lower() == "nowytermin":
                    terminyDB = PosrednikBazyDanych(TypModelu.Terminy)
                    try:
                        print(request.form['termod'])
                        print(request.form['termdo'])
                        nowy = TerminBLL(0, request.form['termod'], request.form['termdo'], True, int(id))
                        terminyDB.dodajObiekt(nowy)
                    except (TypeError, ValueError) as e:
                        flash("Błąd podałeś niepoprawne dane do terminów!")
                        return redirect(url_for('WidokKontaFirmowego:szczegolyMojejOferty', id=id))
                        
                    flash("Poprawnie dodano nowy termin")
                    return redirect(url_for('WidokKontaFirmowego:szczegolyMojejOferty', id=id))

                elif request.form['methodid'].lower() == "usun":
                    saleDB = PosrednikBazyDanych(TypModelu.Sale)
                    rezerwacjeDB = PosrednikBazyDanych(TypModelu.Rezerwacje)
                    if len([r for r in rezerwacjeDB.pobierzWszystkieObiekty() if r.Id_Sali == id]) != 0:
                        flash("Nie można usunąć sali, która ma nadal oczekującą rezerwację")
                        return redirect(url_for('WidokKontaFirmowego:szczegolyMojejOferty', id=id))
                    else:
                        saleDB.usunObiekt(id)
                        flash("Usunięto salę poprawnie")
                        return redirect(url_for('WidokKontaFirmowego:mojeOferty'))

                else:
                    saleBD = PosrednikBazyDanych(TypModelu.Sale)
                    sala = saleBD.pobierzObiekt(id).toDict()
                    flash("Nie poprawna methoda post")
                    return render_template("WidokKontaFirmowego/szczegolyMojejOferty.html", sala=sala)
        else:
            flash("Musisz sie zalogowac byc przejsc do tej podstrony")
            return redirect(url_for('WidokStronyStartowej:Logowanie_doKontaFirmowego'))

    @route('/wylogujsie/')
    def wylogujsie(self):
        """
        Wylogowuje uzytkownika / usuwa dane z sesji
        :return: przekierowanie do strony startowej dla uzytkownika niezalogowanego
        """
        if 'email' in session.keys() and 'konto_id' in session.keys():
            session.pop("email")
            session.pop("konto_id")
            flash('Wylogowano sie z konta firmowego')
            return redirect(url_for("WidokStronyStartowej:StronaPoczatkowa"))
        else:
            flash("Musisz sie zalogowac byc przejsc do tej podstrony")
            return redirect(url_for('WidokStronyStartowej:Logowanie_doKontaFirmowego'))