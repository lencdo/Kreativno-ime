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


#osnovni podatki - shranimo html spletne strani
def download_url(url):
    datoteka  = requests.get(url)
    datoteka_text = datoteka.text
    datoteka_ime = "faks.html"
    shrani_text(datoteka_text, faks_directory, datoteka_ime )

    return None

#da dobimo imenik faks pokličemo naslednjo funkcijo
#download_url(faks_url)

#vzorec osnovnih podatkov
#dodamo del spletne strani, ki nam bo v pomoč pri iskanju podrobnejših podatkov
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


#vzorec za smeri
vzorec_smeri = re.compile(
    "<td class=\"ac\">\d+<\/td>\s*<td>.*<span class=\"bld\">"
    "(?P<Smer>.*)"
    "<\/span> \("
    "(?P<Stopnja>\w*)"
    "\)<\/a>"
    )


#iz imenika pregleda vsako datoteko (html) in izlušči z vzorcem podatke,
#ki jih pretvori v seznam slovarjev
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

#glavni seznam slovarjev fakultet 
seznam_podatkov = seznam_iz_podatkov('faks', osnovni_vzorec)


#podobno kot pri download_url shrani html datoteko za vsak faks posebej,
#iz katerih bomo v nadaljevanju pridobili smeri
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

#da dobimo imenik univerze kličemo naslednjo funkcijo
#download_faksi(seznam_podatkov)

#podobna koda kot seznam_iz_podatkov, le da doda še naziv, da bomo lahko
#kasneje smeri združili s podatki univerze po ključu Naziv
def smeri_iz_podatkov(imenik, vzorec):
    a=0
    sez=[]
    for ime_datoteke in os.listdir(imenik):
        pot = os.path.join(imenik, ime_datoteke)
        with open(pot, encoding = 'utf-8') as datoteka:
            vsebina = datoteka.read()
        for ujemanje in vzorec.finditer(vsebina):
            podatki = ujemanje.groupdict()
            podatki["Naziv"] = str(ime_datoteke)[:-5]
            sez.append(podatki)
            a+=1
        print(a)
    return sez

seznam_smeri = smeri_iz_podatkov("univerze", vzorec_smeri)



#funkcija, ki nam bo zlila skupaj oba seznama slovarjev
def zlij_skupaj(seznam1, seznam2, ključ):
    for item1 in seznam1:
        for item2 in seznam2:
            if item1[ključ] == item2[ključ]:
                item1.update(item2)
            else:
                pass
    return(seznam1)

seznam1 = zlij_skupaj(seznam_smeri, seznam_podatkov, "Naziv")


def izbrisi(seznam, ključ):
    dolzina = len(seznam)
    for i in range(0, dolzina):
        seznam[i].pop(ključ)
    return(seznam)

#ker je ključ Spletna_stran odveč, ga odstranimo
seznam2 = izbrisi(seznam1, "Spletna_stran")

def ID(seznam):
    dolzina = len(seznam)
    for i in range(0, dolzina):
        seznam[i]["ID"] = i
    return(seznam)


seznam = ID(seznam2)


imena = [
    "ID",
    "Naziv",
    "Ulica",
    "Kraj",
    "Postna_stevilka",
    "Smer",
    "Stopnja"
    ]
    

def zapisi_csv(podatki, polja, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)
    
