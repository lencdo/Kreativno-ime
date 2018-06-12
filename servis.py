
#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import *

# uvozimo ustrezne podatke za povezavo
import auth_public as auth

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

@get('/')
def index():
    #cur.execute("SELECT * FROM oseba ORDER BY priimek, ime")
    return template('index.html', osebe=cur)

@get('/registracija')
def registracija():
    return template('registracija.html', osebe=cur)

@post('registriraj_se')
def registriraj_se():
    """Registriraj novega uporabnika."""
    uporabnisko_ime = bottle.request.forms.uporabnisko_ime
    ime = bottle.request.forms.ime
    password1 = bottle.request.forms.password1
    password2 = bottle.request.forms.password2
    # Ali uporabnik že obstaja?
    c = baza.cursor()
    c.execute("SELECT 1 FROM uporabnik WHERE username=?", [username])
    if c.fetchone():
        # Uporabnik že obstaja
        return bottle.template("register.html",
                               username=username,
                               ime=ime,
                               napaka='To uporabniško ime je že zavzeto')
    elif not password1 == password2:
        # Geslo se ne ujemata
        return bottle.template("register.html",
                               username=username,
                               ime=ime,
                               napaka='Gesli se ne ujemata')
    else:
        # Vse je v redu, vstavi novega uporabnika v bazo
        password = password_md5(password1)
        c.execute("INSERT INTO studenti(ime, priimek, kraj, uporabnisko_ime, password) VALUES (?, ?, ?)",
                  (username, ime, password))
        # Daj uporabniku cookie
        bottle.response.set_cookie('username', username, path='/', secret=secret)
        bottle.redirect("/")


######################################################################
# Glavni program

# priklopimo se na bazo5
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8081)
