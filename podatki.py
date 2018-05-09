import re
import requests
import os
import json
import csv


faks_url = "http://studentski.net/studij/fakultete-in-visoke-sole.html"
faks_directory="faks"

#program, ki shrani text v datoteko                
def shrani_text(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    pot = os.path.join(directory, filename)
    with open(pot, 'w', encoding = 'utf-8') as mapa:
        mapa.write(text)
    return None


#osnovni podatki
def download_url(url):
    datoteka  = requests.get(url)
    datoteka_text = datoteka.text
    datoteka_ime = "faks.html"
    shrani_text(datoteka_text, faks_directory, datoteka_ime )

    return None

#vzorec osnovnih podatkov
osnovni_vzorec = re.compile(
   " <span class=\"bld\">\d\.\d "
   "(?P<Naziv>.*)"
   "</span><ul class=\"std\"><li>Naslov: "
   "(?P<Ulica>.*)"
   ", "
   "(?P<Postna_stevilka>\d\d\d\d) "
   "(?P<Kraj>\w+)"
   "&nbsp.*Izvaja: <a class=\"p\" href=\""
    "(?P<Spletna_stran>.*\.html)"
    )


#vzorec_smeri = re.compile()


def seznam_iz_podatkov(imenik, vzorec):
    a=0
    sez=[]
    for ime_datoteke in os.listdir(imenik):
        pot = os.path.join(imenik, ime_datoteke)
        with open(pot, encoding = 'utf-8') as datoteka:
            vsebina = datoteka.read()
        for ujemanje in vzorec.finditer(vsebina):
            podatki = ujemanje.groupdict()
            sez.append(podatki)
            a+=1
        print(a)
    return sez

seznam_podatkov = seznam_iz_podatkov('faks', osnovni_vzorec)

def download_faksi(podatki):
    dolzina = len(podatki)
    for i in range(0, dolzina):
        faks_url = 'http://studentski.net' + podatki[i]["Spletna_stran"]
        stran = requests.get(faks_url)
        text = stran.text
        datoteka_ime = '{}.html'.format(podatki[i]["Naziv"])
        shrani_text(text, 'univerze', datoteka_ime)
        print(i)

    return None



def sestavi_slovarje(seznam1, seznam2):
    dolzina = len(seznam1)
    for i in range(0, dolzina):
        seznam1[i].update(seznam2[i])
    return seznam1




#funkcija, ki bo spojila skupaj dva seznama slovarjev, ki imata enak ključ
def merge_lists(slovar1, slovar2, key):
    merged = {}
    for item in slovar1+slovar2:
        if item[key] in merged:
            merged[item[key]].update(item)
        else:
            merged[item[key]] = item
    return [val for (_, val) in merged.items()]





imena = []
    

def zapisi_csv(podatki, polja, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)
    
