import requests
import mysql.connector

# Connexion à la base de donnée

database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="book"
)

mycursor = database.cursor()
# mycursor.execute("CREATE DATABASE IF NOT EXISTS book")
mycursor.execute("CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(255),"
                 " auteur VARCHAR(255), editeur VARCHAR(255), date_publication INT, description VARCHAR(255),"
                 " nombre_page INT, langue VARCHAR(255), categorie VARCHAR(255))")

# Paramètre généraux

isbn = input("Votre numéro ISBN: ")
query = 'isbn:' + isbn
params = {"q": query}

# GOOGLE

try:

    print('------Google------')
    urlGoogle = 'https://www.googleapis.com/books/v1/volumes'
    responseGoogle = requests.get(urlGoogle, params=params)
    resultGoogle = responseGoogle.json()
    concate = resultGoogle["items"]
    for details in concate:
        titreGoogle = details["volumeInfo"]["title"]
        auteurGoogle = details["volumeInfo"]["authors"][0]
        editeurGoogle = details["volumeInfo"]["publisher"]
        dateGoogle = details["volumeInfo"]["publishedDate"]
        descGoogle = details["volumeInfo"]["description"]
        pageGoogle = str(details["volumeInfo"]["pageCount"])
        languageGoogle = details["volumeInfo"]["language"]
        print("Titre du livre: " + titreGoogle)
        print("Auteurs: " + auteurGoogle)
        print("Editeur: " + editeurGoogle)
        print("Date de publication: " + dateGoogle)
        print("Description du livre: " + descGoogle)
        print("Nombre de page: " + pageGoogle)
        print("Langue du livre: " + languageGoogle)

# OPENLIBRARY

    print('------OpenLibrary------')
    urlOpenLibrary = "https://openlibrary.org/api/books?bibkeys=ISBN:" + isbn + "&callback=mycallback"
    responseOpenLibrary = requests.get(urlOpenLibrary, params=params)
    resultOpenLibrary = responseOpenLibrary.text
    print(resultOpenLibrary)

# ALTMETRICS

    print('------AltMetrics------')
    urlAltMetrics = "https://api.altmetric.com/v1/isbn/" + isbn
    responseAltMetrics = requests.get(urlAltMetrics, params=params)
    resultAltMetrics = responseAltMetrics.json()
    print(resultAltMetrics)
    categorieAltMetrics = resultAltMetrics["type"]
    print("Titre du livre: " + resultAltMetrics["title"])
    print("Auteur: " + resultAltMetrics["authors_or_editors"][0])
    print("Catégorie: " + categorieAltMetrics)


# Requete inserer dans une table

    sql = "INSERT INTO books (id, nom, auteur, date_publication, description, nombre_page, langue, categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = ("", titreGoogle, auteurGoogle, dateGoogle, descGoogle, pageGoogle, languageGoogle, categorieAltMetrics)
    mycursor.execute(sql, val)
    database.commit()
    print(mycursor.rowcount, "Enregistrement importés.")

except FileNotFoundError:
    print("Fichier introuvable")
except IOError:
    print("erreur d’ouverture")


# 9782709624930
# import requests
# import isbnlib
# from isbnlib.registry import bibformatters
# from isbnlib import meta
#
# # rint(isbnlib.cover(isbn))
#
# try:
#     with open('fichierSource.csv', 'r+') as file:
#         for ligne in file:
#             cleaned = ligne.rstrip()
#             #Open Library
#             print("OpenLibrary")
#             url = "https://openlibrary.org/api/books?bibkeys=ISBN:"+cleaned+"&callback=mycallback"
#             payload = {}
#             headers = {}
#             response = requests.request("GET", url, headers=headers, data=payload)
#             print(response.text)
#
#             #GoogleBooks
#             print("Google Books")
#             query = 'isbn:'+cleaned
#             params = {"q": query}
#             url = r'https://www.googleapis.com/books/v1/volumes'
#             response = requests.get(url, params=params)
#             print(response.text)
#             # data = json.load(response.json())
#             # print(response.json()['items'][0]['volumeInfo']['title'])
#             # print(data)
#             #AltMetrics
#             print("AltMetrics")
#             url = "https://api.altmetric.com/v1/isbn/"+cleaned
#             payload = {}
#             headers = {}
#             response = requests.request("GET", url, headers=headers, data=payload)
#             print(response.text)
#
#             SERVICE = "bnf"
#             print("BNF")
#             # now you can use the service
#             isbn = cleaned
#             try:
#                 bibtex = bibformatters["json"]
#                 print(bibtex((isbn, SERVICE)))
#             except AttributeError:
#                 print("erreur BNF")
#
#             print("Worldcat")
#             # now you can use the service
#             service = "worldcat"
#             isbn = cleaned
#             try:
#                 bibtex = bibformatters["bibtex"]
#                 print(bibtex(meta(isbn, SERVICE)))
#             except AttributeError:
#                 print("erreur Worldcat")
#
#
