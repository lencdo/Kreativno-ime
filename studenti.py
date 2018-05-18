import csv
from random import randint


#vzame csv datoteko študentov in dodav vrstico Izobrazba, ki vsebuje ID izobrazbe (naziv univerze in smer)
def odpri_csv(datoteka, nova_datoteka):
    with open(datoteka, 'r', encoding = 'utf-8') as a, open(nova_datoteka, 'w', encoding = 'utf-8') as b:
        csvreader = csv.DictReader(a)
        imena = csvreader.fieldnames + ["Izobrazba"] 
        csvwriter = csv.DictWriter(b, imena)
        csvwriter.writeheader()
        for izobrazba, vrstica in enumerate(csvreader, -1):
            csvwriter.writerow(dict(vrstica, Izobrazba=randint(0, 335)))
    return None
            
