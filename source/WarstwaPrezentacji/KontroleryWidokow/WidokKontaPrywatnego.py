import json

from flask_classful import FlaskView, route
from flask import render_template, jsonify, request, session, redirect, url_for, flash
from source.WarstwaBiznesowa.PosrednikBazyDanych import PosrednikBazyDanych
from source.WarstwaBiznesowa.KontroleryModeli.KontrolerModeluInterface import TypModelu
from source.WarstwaBiznesowa.ModeleBLL.KontoPrywatneBLL import KontoPrywatneBLL
from source.WarstwaBiznesowa.SystemMailingowy.SystemMailingowy import SystemMailingowy
from source.WarstwaBiznesowa.ModeleBLL.RezerwacjaBLL import RezerwacjaBLL
from source.WarstwaBiznesowa.ModeleBLL.SalaBLL import SalaBLL
import os
from datetime import datetime
from source.WarstwaBiznesowa.wyjatki import *


class WidokKontaPrywatnego(FlaskView):
    """
    Klasa odpowiedzialna za renderowanie widokow dla interfejsu konta prywatnego
    """
    @route('/')
    def stronaPoczatkowa(self):
        """
        Wyswietla strone poczatkowa jestli uzytkownik prywatny jest zalogowany
        w przeciwnym wypadku przekirowuje do logowanie do konta prywatnego
        :return: Szablon html strony poczatkowej interfejsu prywatnego lub przekierowanie do logowania
        """
        if "email" in session.keys() and "konto_id" in session.keys():
            email = session.get('email')
            kontoid = session.get('konto_id')
            return render_template('WidokKontaPrywatnego/index.html', email=email, id=kontoid)
        else:
            return redirect(url_for("WidokStronyStartowej:Logowanie_doKontaPrywatnego"))


    @route("/daneKonta/", methods=["GET", "POST"])
    def daneKonta(self):
        """
        Pokazuje strone z danymi uzytkownika do edycji (Metoda GET),
        Metoda POST (gdy w polu methodid post'a jest "edytuj") - aktualizuje dane konta prywatnego na podstawie zmian w formularzu
        Metoda POST (gdy w polu methodid jest "usun") - usuwa konto prywatne
        :return:
        """
        if 'konto_id' in session.keys():
            bazadanych = PosrednikBazyDanych(TypModelu.KontoPrywatne)
            user: KontoPrywatneBLL = bazadanych.pobierzObiekt(session['konto_id'])
            user.Rezerwacje = None
            if request.method == "GET":
                return render_template("WidokKontaPrywatnego/daneKonta.html", text_lists=user.toDict())
            else:
                if request.form.get('methodid') == "edytuj":
                    nowe_dane = request.form
                    for k, v in nowe_dane.items():
                        setattr(user, k, v)
                    try:
                        bazadanych.zaktualizujObiekt(session['konto_id'], user)
                    except BladZapisuDoBazyDanych as e:
                        flash("Nie udalo sie zapisac twoich danych")
                        return redirect(url_for('WidokKontaPrywatnego:daneKonta'))

                    session.pop("email")
                    session.pop("konto_id")
                    flash("Zaktualizowano dane konta. Zaloguj sie ponownie!")
                    return redirect(url_for('WidokStronyStartowej:Logowanie_doKontaPrywatnego'))
                elif request.form.get('methodid') == "usun":
                    try:
                        bazadanych.usunObiekt(session['konto_id'])
                    except BladWBazieDanychError as e:
                        flash(str(e))
                        return redirect(url_for('WidokKontaPrywatnego:daneKonta'))

                    session.pop("email")
                    session.pop("konto_id")
                    flash("Usunięto twoje konto :( ")
                    return redirect(url_for('WidokStronyStartowej:StronaPoczatkowa'))
        else:
            return redirect(url_for("WidokStronyStartowej:Logowanie_doKontaPrywatnego"))

    @route("/mojeRezerwacje/")
    def mojeRezerwacje(self):
        """
        Wyswietla widok wszystkich rezerwacji uzytkownika zalogowanego
        :return: renderuje szablon html dla listy rezerwacji lub przekierowanie do logowania
        """
        if 'konto_id' in session.keys():
            rezerwacje = PosrednikBazyDanych(TypModelu.Rezerwacje).pobierzWszystkieObiekty()
            moje_rezerwacje = [r for r in rezerwacje if r.Id_Rezerwujacego == session['konto_id']]
            moje_rezer = []
            sale_db = PosrednikBazyDanych(TypModelu.Sale)
            firmy_db = PosrednikBazyDanych(TypModelu.KontoFirmowe)
            terminy_db = PosrednikBazyDanych(TypModelu.Terminy)
            for r in moje_rezerwacje:
                try:
                    termin = terminy_db.pobierzObiekt(r.Id_Terminu)
                    if not termin:
                        continue

                    sala = sale_db.pobierzObiekt(r.Id_Sali)
                    firma = firmy_db.pobierzObiekt(sala.Id_Wynajmujacego)
                    moje_rezer.append({"id_rezerwacji": r.Id_Rezerwacji, "firma": firma.Nazwa_Firmy,
                                       "cena": sala.Cena, "Adres": sala.Adres,
                                       "terminod": datetime.strftime(termin.Data_i_godzina_Rozpoczecia, "%d.%m.%Y %H:%M"),
                                      "termindo": datetime.strftime(termin.Data_i_godzina_Zakonczenia, "%d.%m.%Y %H:%M")})
                except BladWKontrolerzeModeliError as e:
                    flash("Coś poszło nie tak w pobieraniu twoich rezerwacji, sprobuj ponownie")
                    return redirect(url_for("WidokKontaPrywatnego:stronaPoczatkowa"))

            return render_template("WidokKontaPrywatnego/mojeRezerwacje.html", mojerezer=moje_rezer)
        else:
            return redirect(url_for("WidokStronyStartowej:Logowanie_doKontaPrywatnego"))

    @route("/ofertySal/")
    def ofertySal(self):
        """
        Wyswietla liste dostepnych ofert sal
        :return: szablon html dla widoku ofert sal
        """
        if 'konto_id' in session.keys():
            database = PosrednikBazyDanych(TypModelu.Sale)
            firmDb = PosrednikBazyDanych(TypModelu.KontoFirmowe)
            sale_obj = database.pobierzWszystkieObiekty()
            sale = [s.toDict() for s in sale_obj if s.Wolna and s]

            for s in sale:
                try:
                    s['id_wynajmujacego'] = firmDb.pobierzObiekt(s['id_wynajmujacego']).Nazwa_Firmy
                except BladWKontrolerzeModeliError as e:
                    flash("Coś poszło nie tak w trakcie wydobywania danych sal")
                    return redirect(url_for("WidokKontaPrywatnego:stronaPoczatkowa"))

            return render_template("WidokKontaPrywatnego/ofertySal.html",
                                   text_lists={'sale': sale}, oferty_sal=sale)
        else:
            return redirect(url_for("WidokStronyStartowej:Logowanie_doKontaPrywatnego"))

    @route("/ofertySal/<int:id>/", methods=['GET', 'POST'])
    def szczegolyOferty(self, id):
        """
        Wyswietla szczegoly oferty o id podanym w url. (dla metody GET)
        dla metody POST, po wybraniu terminu tworzy obiekt rezerwacji dla wybranego terminu w sali wyswietlanej wczesniej
        :param id: identyfikator wybranej sali
        :return: szablon html wyswietlajacy szczeguly sali, lub redirect do tej samej strony dla GET
        """
        if 'konto_id' in session.keys():
            if request.method == "GET":
                saleDB = PosrednikBazyDanych(TypModelu.Sale)
                sala = saleDB.pobierzObiekt(id)
                salaDict = sala.toDict()
                terminy = salaDict.get('terminy')
                try:
                    firma = PosrednikBazyDanych(TypModelu.KontoFirmowe).pobierzObiekt(salaDict['id_wynajmujacego'])
                    salaDict['id_wynajmujacego'] = firma.Nazwa_Firmy
                except BladWKontrolerzeModeliError as e:
                    flash("Nie znaleziono podanej sali")
                    return render_template("WidokKontaPrywatnego/ofertySal.html")

                if salaDict.get("wolna"):
                    return render_template("WidokKontaPrywatnego/szczegolyOferty.html", sala=salaDict, terminy=terminy)
                else:
                    return redirect(url_for("WidokKontaPrywatnego:ofertySal"))
            else:
                id_sali = int(request.form['idsali'])
                id_terminu = request.form['termin']
                sala: SalaBLL = PosrednikBazyDanych(TypModelu.Sale).pobierzObiekt(id_sali)
                rezerwacjeDB = PosrednikBazyDanych(TypModelu.Rezerwacje)
                system_mailingowy = SystemMailingowy(rezerwacjeDB.kontrolerModelu)
                try:
                    rezerwacja = RezerwacjaBLL(0, float(sala.Cena), int(session['konto_id']), int(id_sali), int(id_terminu))
                    rezerwacjeDB.dodajObiekt(rezerwacja)
                except (TypeError, ValueError, BladZapisuDoBazyDanych) as e:
                    flash("Błąd modelu rezerwacji!")
                    return render_template("WidokKontaPrywatnego/ofertySal.html")
                        
                flash("Zarezewowano poprawnie salę.")
                return redirect(url_for("WidokKontaPrywatnego:szczegolyOferty", id=id_sali))
        else:
            return redirect(url_for("WidokStronyStartowej:Logowanie_doKontaPrywatnego"))

    @route("/szczegolyRezerwacji/<int:id>/", methods=["GET", "POST"])
    def szczegolyRezerwacji(self, id):
        """
        Methoda wyswietlajaca szczegoly rezerwacji (Metoda GET) lub usuwajaca rezerwacje dla metody POST
        :param id: id rezerwacji w bazie danych
        :return: szablon html ze szczegolami sali, redirect do strony z lista rezerwacji
        """
        if 'konto_id' in session.keys():
            if request.method == "GET":
                try:
                    rezerwacje_db = PosrednikBazyDanych(TypModelu.Rezerwacje)
                    rezer = rezerwacje_db.pobierzObiekt(id).toDict()
                    sala = PosrednikBazyDanych(TypModelu.Sale).pobierzObiekt(rezer.get('Id_Sali')).toDict()
                    firma = PosrednikBazyDanych(TypModelu.KontoFirmowe).pobierzObiekt(sala.get('id_wynajmujacego')).toDict()
                    termin = PosrednikBazyDanych(TypModelu.Terminy).pobierzObiekt(rezer.get('Id_Terminu')).toDict()
                    if not termin:
                        return redirect(url_for("WidokKontaPrywatnego:mojeRezerwacje"))
                    rezer['sala'] = sala
                    rezer['firmaWynajmujaca'] = firma.get('Nazwa_Firmy')
                    rezer['terminOd'] = termin.get('Data_i_godzina_Rozpoczecia')
                    rezer['terminDo'] = termin.get('Data_i_godzina_Zakonczenia')
                    return render_template("WidokKontaPrywatnego/szczegolyRezerwacji.html", rezer=rezer)
                except BladWKontrolerzeModeliError as e:
                    flash("Coś się popsuło w kontrolerze w serwerze! Spróbuj ponownie")
                    return redirect(url_for("WidokKontaPrywatnego:mojeRezerwacje"))
            else:
                posrednik = PosrednikBazyDanych(TypModelu.Rezerwacje)
                mail = SystemMailingowy(posrednik.kontrolerModelu)
                try:
                    posrednik.usunObiekt(id)
                    flash("Pomyślnie dokonano rezygnacji")
                    return redirect(url_for("WidokKontaPrywatnego:mojeRezerwacje"))
                except (BladWBazieDanychError, BladWKontrolerzeModeliError) as e:
                    flash("Nie można zrezygnować z oferty na mniej niż 2 dni przed!")
                    return redirect(url_for("WidokKontaPrywatnego:szczegolyRezerwacji", id=id))
        else:
            return redirect(url_for("WidokStronyStartowej:Logowanie_doKontaPrywatnego"))

    @route("/wylogujsie/")
    def wylogujsie(self):
        """
        Metoda wylogowuje uzytkownika z konta (usuwa z sesji jego dane)
        :return: przekierowanie do strony poczatkowej dla niezalogowanego uzytkownika
        """
        if 'email' in session.keys() and 'konto_id' in session.keys():
            session.pop("email")
            session.pop("konto_id")
            flash('Wylogowano sie z konta prywatnego')
            return redirect(url_for("WidokStronyStartowej:StronaPoczatkowa"))