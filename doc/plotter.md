plotter.md

#Grundidee
1. RDF rein, Serialisierung egal > Usecase: RDF/XML
2. RDF verarbeiten
  * Place-URIs ausfindig machen: Jede Subject- & Object-URI prüfen > Dump (GeoNames, GND, ...)
  * Ablage in Datenbank (Place-URI-Dumps [URI, Type, Label, Lat. & Long.]) um URI-Abgleiche zu unterstützen
  * Für jede Place-URI: 
    * Label und 
    * Koordinaten (Breiten- und Längengrad) holen 
  * Ergebnisse als JSON zurückgeben
3. JSON-Rückgabe auf Map plotten


#Datenbanken
* Triplestore
  * Sesame (http://www.openrdf.org/)
    * http://www.jenitennison.com/2011/01/25/getting-started-with-rdf-and-sparql-using-sesame-and-python.html
  * Fuseki (https://jena.apache.org/documentation/serving_data/) 

##AUFGABE: Datenspeicher
* Place-URIs speichern [URI{1}, Type{1}, Label{1-N}, Lat.{1} & Long.{1}]
* Bereits angefüllt mit GeoNames & GND 
  * Dump auf Place-URIs prüfen und in Datenbank abspeichern (Python, Perl etc.)


#Python

##Blogs und Websites
* https://www.oclc.org/developer/news/2016/making-sense-of-linked-data-with-python.en.html
* http://www.michelepasin.org/blog/2011/02/24/survey-of-pythonic-tools-for-rdf-and-linked-data-programming/

##AUFGABE: Requests und POST-Handling
* HTTP-Requests (urllib2)

##AUFGABE: Verarbeitung von RDF / LOD
###RDFLib : parsen, serialisieren und verarbeiten von RDF
* https://github.com/RDFLib/rdflib
* Unterstützte Formate: "RDF/XML, N3, NTriples, N-Quads, Turtle, TriX, RDFa and Microdata"
* SPARQL Funktionalität

##AUFGABE: Response
* JSON (json)


#JavaScript

##AUFGABE: GUI

##AUFGABE: Plotting
* AJAX: Wenn RDF Verarbeitung abgeschlossen > POST an URL > via AJAX auf URL lauschen und bei POST Daten an Map-API senden
* Asynchron (pref) vs. Synchron: 
  * Sobald JSON da, kann jedes Ort-Object asynchron geplottet werden
  * Unabhängige Verarbeitungsschritte (keine sequenzielle Verarbeitung)
