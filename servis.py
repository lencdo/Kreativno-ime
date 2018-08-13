

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

@route('/registracija_podjetje')
def registracija():
    return template('registracija_podjetje.html', osebe=cur)

@route('/registracija_student')
def registracija():
    return template('registracija_student.html', osebe=cur)

@route('/prijava')
def prijava():
    return template('prijava.html', osebe=cur)

@route("/")
def index():
    return template("index.html", osebe=cur)

@route('/prosta_dela')
def prosta_dela():
    return template('prosta_dela.html', rezultat_iskanja={})

@route('/student')
def student():
    return template("student.html", osebe=cur)

@route('/prosta_dela_student')
def prosta_dela():
    return template('prosta_dela_student.html', osebe=cur)

@route("/podjetje")
def prosta_dela():
    return template('podjetje.html', osebe=cur)
   

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
    return template('prosta_dela.html', rezultat_iskanja=vrni)

@post('/registracija_podjetje/')
def registracija_podjetje():
    #Registriraj novo podjetje
    naziv = request.forms.get('naziv')
    kraj = request.forms.get('kraj')
    postna_stevilka = request.forms.get('stevilka')
    drzava = request.forms.get('drzava')
    panoga = request.forms.get('panoga')
    kartica = request.forms.get('kartica')
    uporabnisko = request.forms.get('uporabnisko')
    geslo1 = request.forms.get('geslo1')
    geslo2 = request.forms.get('geslo2')

    print(naziv, kraj, postna_stevilka, drzava, panoga, kartica, uporabnisko, geslo1, geslo2)

    cur.execute("SELECT 1 FROM podjetja WHERE uporabnisko_ime=%s", [uporabnisko])
    if cur.fetchone():
        # Uporabnik že obstaja
        print('uporabnik ze obstaja')
        return template("registracija_podjetje.html")
    elif not geslo1 == geslo2:
        return template("registracija_podjetje.html")
    else:
        # Vse je v redu, vstavi novega uporabnika v bazo
        cur.execute("INSERT INTO podjetja (drzava, ime, kraj, bancni_racun, panoga, geslo, uporabnisko_ime) VALUES (%s, %s, %s, %s, %s, %s, %s)",
              [drzava, naziv, kraj, kartica, panoga, geslo2, uporabnisko])
        return template("index.html")

@post('/registriracija_student/')
def registriraj_se():
    #Registriraj novega študenta
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
    kreditna_kartica=request.forms.get('kartica')
    izobrazba=request.forms.get('faks')

    print(ime, priimek, spol, kraj, drzava, postna_stevilka, uporabnisko_ime, geslo1, geslo2, rojstni_datum)

    cur.execute("SELECT 1 FROM studenti WHERE uporabnisko_ime=%s", [uporabnisko_ime])
    if cur.fetchone():
        # Uporabnik že obstaja
        print('uporabnik ze obstaja')
        return template("registracija_podjetje.html")
    elif not geslo1 == geslo2:
        return template("registracija_podjetje.html")
    else:
        # Vse je v redu, vstavi novega uporabnika v bazo
        cur.execute("INSERT INTO studenti(ime, priimek, spol, rojstni_dan, drzava, kraj, postna_stevilka, kreditna_kartica, uporabnisko_ime, geslo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
              (ime, priimek, spol, rojstni_datum, drzava, kraj, postna_stevilka, kreditna_kartica, uporabnisko_ime, geslo1))
        return template("index.html")
 
        # Daj uporabniku cookie
##        bottle.response.set_cookie('username', username, path='/', secret=secret)
##        bottle.redirect("/")


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
