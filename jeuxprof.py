import requests
import isbnlib
from isbnlib.registry import bibformatters
from isbnlib import meta

# rint(isbnlib.cover(isbn))

try:
    with open('fichierSource.csv', 'r+') as file:
        for ligne in file:
            cleaned = ligne.rstrip()
            #Open Library
            print("OpenLibrary")
            url = "https://openlibrary.org/api/books?bibkeys=ISBN:"+cleaned+"&callback=mycallback"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.text)

            #GoogleBooks
            print("Google Books")
            query = 'isbn:'+cleaned
            params = {"q": query}
            url = r'https://www.googleapis.com/books/v1/volumes'
            response = requests.get(url, params=params)
            print(response.text)
            # data = json.load(response.json())
            # print(response.json()['items'][0]['volumeInfo']['title'])
            # print(data)
            #AltMetrics
            print("AltMetrics")
            url = "https://api.altmetric.com/v1/isbn/"+cleaned
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.text)

            SERVICE = "bnf"
            print("BNF")
            # now you can use the service
            isbn = cleaned
            try:
                bibtex = bibformatters["bibtex"]
                print(bibtex(meta(isbn, SERVICE)))
            except AttributeError:
                print("erreur BNF")

            print("Worldcat")
            # now you can use the service
            service = "worldcat"
            isbn = cleaned
            try:
                bibtex = bibformatters["bibtex"]
                print(bibtex(meta(isbn, SERVICE)))
            except AttributeError:
                print("erreur Worldcat")


except FileNotFoundError:
    print("Fichier introuvable")
except IOError:
    print("erreur d’ouverture")

