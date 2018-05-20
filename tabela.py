import auth


import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import csv

def ustvari_tabelo_studenti():
    cur.execute("""
        CREATE TABLE studenti (
            id INTEGER PRIMARY KEY,
            ime TEXT NOT NULL,
            priimek TEXT NOT NULL,
            kraj TEXT NOT NULL,
            spol TEXT NOT NULL,
            kreditna_kartica TEXT NOT NULL,
            znanja TEXT,
            rojstni_dan TEXT NOT NULL,
            izobrazba INTEGER
        );
    """)
    conn.commit()

def pobrisi_tabelo_studenti():
    cur.execute("""
        DROP TABLE studenti;
    """)
    conn.commit()

def uvozi_podatke_studenti():
    with open("studenti1.csv", encoding="utf8") as f:
        rd = csv.reader(f, delimiter=',')
        next(rd) # izpusti naslovno vrstico
        for r in rd:
            print(r)
            #r = [None if x in ('', '-') else x for x in r] nevem ali je potrebno
            cur.execute("""
                INSERT INTO studenti
                (id, ime, priimek, kraj, spol, kreditna_kartica,
                 znanja, rojstni_dan, izobrazba)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, r)
            #cur.fetchone()
    conn.commit()


def ustvari_tabelo_univerze():
    cur.execute("""
        CREATE TABLE univerze (
            id INTEGER PRIMARY KEY,
            naziv TEXT NOT NULL,
            ulica TEXT NOT NULL,
            kraj TEXT NOT NULL,
            postna_stevilka INTEGER NOT NULL,
            smer TEXT NOT NULL,
            stopnja TEXT NOT NULL
        );
    """)
    conn.commit()

def pobrisi_tabelo_univerze():
    cur.execute("""
        DROP TABLE univerze;
    """)
    conn.commit()


def uvozi_podatke_univerze():
    with open("univerze.csv", encoding="utf8") as f:
        rd = csv.reader(f, delimiter=",")
        next(rd)# izpusti naslovno vrstico
        for r in rd:
            #r = [None if x in ('', '-') else x for x in r]
            try:
                cur.execute("""
                INSERT INTO univerze
                (id, naziv, ulica, kraj, postna_stevilka, smer, stopnja)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, r)
                print(r)
            except:
                continue
    conn.commit()



conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
