

#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import *

# uvozimo ustrezne podatke za povezavo
import auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

# odkomentiraj, če želiš sporočila o napakah
# debug(True)
##@get("/css/<filepath:re:.*\.css>")
##def css(filepath):
##    return static_file(filepath, root="./static/css")
##
##@get("/fonts/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
##def font(filepath):
##    return static_file(filepath, root="static/fonts")
##
##@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
##def img(filepath):
##    return static_file(filepath, root="static/images")
##
##@get("/js/<filepath:re:.*\.js>")
##def js(filepath):
##    return static_file(filepath, root="static/js")
##
##@get("/sass/<filepath:re:.*\.scss>")
##def sass(filepath):
##    return static_file(filepath, root="static/sass")

@get('/assets/<filename:path>')
def static(filename):
    return static_file(filename, root='assets')



@route('/registracija')
def registracija():
    return template('registracija.html', osebe=cur)

@route('/prijava')
def prijava():
    return template('prijava.html', osebe=cur)

def vrni_dela():
    c = conn.cursor()
    c.execute("SELECT * FROM studenti WHERE kraj=%s", ["Kranj"])
    res=c.fetchall()
    return(res)

@route("/")
def index():
    return template("index.html", osebe=cur)

@route('/prosta_dela')
def prosta_dela():
    return template('prosta_dela.html', osebe=cur)

@post('/')
def index():
    ##"""Išči prosta dela."""
    kratkotrajno = request.forms.get('vrsta1')
    dolgotrajno = request.forms.get('vrsta2')
    pocitnisko = request.forms.get('vrsta3')
    L = tuple(filter(None, [kratkotrajno, dolgotrajno, pocitnisko]))
    print(L)
    dol=len(L)
    if dol == 0:
        L=('kratkotrajno', 'dolgotrajno', 'pocitnisko')

    delovnik1 = request.forms.get('delovnik1')
    delovnik2 = request.forms.get('delovnik2')
    delovnik3 = request.forms.get('delovnik3')
    delovnik4 = request.forms.get('delovnik4')
    D = tuple(filter(None, [delovnik1, delovnik2, delovnik3, delovnik4]))
    dol2=len(D)
    if dol2 == 0:
        D=('dopoldne', 'popoldne', 'izmensko', 'med vikendom')
    print(D)

    postavka = request.forms.get('postavka')
    print("radi", kratkotrajno, dolgotrajno, pocitnisko, delovnik1, delovnik2, delovnik3, delovnik4, postavka)
    c=conn.cursor()
    c.execute("SELECT * FROM prosta_dela WHERE delovnik IN %s AND vrsta IN %s AND urna_postavka >= %s" , [D, L, postavka])
    vrni=c.fetchall()
    print(vrni)


@post('/registriraj_se/')
def registriraj_se():
    """Registriraj novega uporabnika."""
    ime = request.forms.get('q15_name15[first]')
    priimek = request.forms.get('q15_name15[last]')
    spol = request.forms.get('q28_areYou')
    kraj = request.forms.get('q33_address[city]')
    drzava = request.forms.get('q33_address[country]')
    postna_stevilka = request.forms.get('q33_address[postal]')
    uporabnisko_ime = request.forms.get('q34_email')
    geslo1 = request.forms.get('q30_email30')
    geslo2 = request.forms.get('q30_email30')
    rojstni_datum = request.forms.get('datuum')
    kreditna_kartica="13212312321312"
    
    print(ime, priimek, spol, kraj, drzava, postna_stevilka, uporabnisko_ime, geslo1, geslo2, rojstni_datum)
    #return template('poskus', osebe=cur)
    password2 = request.forms.password2
    # Ali uporabnik že obstaja?
    c = conn.cursor()
##    c.execute("SELECT 1 FROM uporabnik WHERE username=?", [username])
##    if c.fetchone():
##        # Uporabnik že obstaja
##        #return bottle.template("register.html",
##        print('uporabnik ze obstaja')
##    elif not password1 == password2:
##        # Geslo se ne ujemata
##        return bottle.template("register.html",
##                            username=username,
##                               ime=ime,
##                               napaka='Gesli se ne ujemata')
 #   else:
        # Vse je v redu, vstavi novega uporabnika v bazo
  #  password = password_md5(password1)5
    c.execute("INSERT INTO studenti(ime, priimek, spol, rojstni_dan, drzava, kraj, postna_stevilka, kreditna_kartica, uporabnisko_ime, geslo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
              (ime, priimek, spol, rojstni_datum, drzava, kraj, postna_stevilka, kreditna_kartica, uporabnisko_ime, geslo1))
        # Daj uporabniku cookie
##        bottle.response.set_cookie('username', username, path='/', secret=secret)
##        bottle.redirect("/")

##@post('/registriraj_se/')
##def isci_sluzbe():
##    """Poišči službe"""
##    ime = request.forms.get('q15_name15[first]')
##    priimek = request.forms.get('q15_name15[last]')
##    spol = request.forms.get('q28_areYou')
##    kraj = request.forms.get('q33_address[city]')
##    drzava = request.forms.get('q33_address[country]')
##    postna_stevilka = request.forms.get('q33_address[postal]')
##    uporabnisko_ime = request.forms.get('q34_email')
##    geslo1 = request.forms.get('q30_email30')
##    geslo2 = request.forms.get('q30_email30')
##    rojstni_datum = request.forms.get('datuum')
##    kreditna_kartica="13212312321312"

######################################################################
# Glavni program

# priklopimo se na bazo5
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

@get('/assets/<filename:path>')
def static(filename):
    return static_file(filename, root='assets')

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)
