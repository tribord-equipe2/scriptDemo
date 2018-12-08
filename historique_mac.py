import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from collections import Counter
import re
import sys

client = str()
routeur = sys.argv[1]

client = routeur.upper()

if not re.fullmatch(r"(?:[A-F0-9]{2}:){5}[A-F0-9]{2}",client):
	sys.stdout.write("Argument invalide")
	sys.stdout.flush()
	sys.exit()

#initialiser la base de donee

cred = credentials.Certificate("cle_db.json")

firebase_admin.initialize_app(cred,{ "databaseURL" : "https://routeur-18013.firebaseio.com/"})

#extraction des donnees de tout les bancs
dataBancs = db.reference("/Bancs").get()
dataCommerces = db.reference("/Commerces").get()


#contientlesentrees "arrive" dans la db
macList = list()
#contient les entrees depart
macListDepart = list()

#dataBancs dict
#itere dans toutes les entrees de tout les bancs
for i in dataBancs.keys():
	#dict
	banc = dataBancs[i]
	for j in banc.keys():
		donee = banc[j]
		if donee["adresse"] == client:
			donee["lieu"] = i
			macList += [donee]
			
if dataCommerces:
	for i in dataCommerces.keys():
		#dict
		banc = dataCommerces[i]
		for j in banc.keys():
			donee = banc[j]
			if donee["adresse"] == client:
				donee["lieu"] = i
				macList += [donee]


print("Historique de deplacement du client :\n\n")

for i in sorted(macList,key = lambda k: k["heure"]):
	if i["type"] == "ajout":
		type = "arrive"
	else:
		type = "depart"
	heure = i["heure"]
	lieu = i["lieu"]
	print(f"{heure}   {type} {lieu}")