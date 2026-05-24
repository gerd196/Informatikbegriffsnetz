# ReadME für gede    
2026-05-24, G. Fessler  
gede = Google-EDE  

## Zweck  
gede erstellt aus den Dateien des Informatik-Begriffsnetzes der Gesellschaft für Informatik in Google-Drive im Verzeichnis **Begriffe2.0** (inklusive Unterverzeichnissen) statische HTML5-basierte Dateien zur Veröffentlichung im Internet.  

## Randbedingungen  
gede benötigt **Perl 5** und **Pandoc** (pandoc.org), beide müssen auf dem Rechner installiert sein. Pandoc muss über den Suchpfad aufrufbar sein.  

gede wurde hauptsächlich mit Perl 5.42 und Pandoc 3.5 unter Linux getestet. Es sollte auch unter älteren Verseionen von Perl 5 (mindestens ab 5.18) lauffähig sein.  

Da die Stabilität sowohl von Microsoft .docx-Dateien als auch deren Erstellung beim Download durch Google nicht garantierbar ist, wird das laufend gepflegte Konvertierungstool Pandoc für die Konvertierung der Google-Docs-Dateien in ein durch gede verarbeitbares Format verwendet. Wegen der Instabilitäten sollte jeweils die neueste Version von Pandoc verwendet werden.  

## Grobarchitektur  
gede arbeitet auf einem entzippten Download aus Google-Drive.  
Es wandelt die entzippten Microsoft-docx-Dateien mit Pandoc zuerst in ein verarbeitbares Format um und erzeugt daraus HTML 5 und zugehörige Dateien im Verzeichnis **web2.0** sowie in Unterverzeichnissen.  
Die Google-Docs-Dateien müssen den Kodierrichtlinien für Version 2.0 des Informatikbegriffsnetzes entsprechen, um umgewandelt werden zu können.  

## Installation  
gede in einem Verzeichnis im Suchpfad ablegen und bei unixoiden Systemen ausführbar machen.  
In Windows entweder eine **Batch-Datei** zum Aufrufen anlegen oder gede mit **perl -w gede** aufrufen.  
In Windows ist es üblich, gede in gede.pl umzubenennen.  

## Nutzung  
0. perl 5 ab Versison 5.18) und Pandoc (ab Version 3.5) auf dem Rechner installieren  
1. In Google Drive im Informatik-Begriffsnetz anmelden.  
2. Das Google-Docs-Verzeichnis Begriffe2.0 in einer Verzeichnisübersicht anzeigen.  
3. Rechtsklick auf Verzeichnis Begriffe2.0 → Herunterladen.  
4. Von Google-Drive erstellte .zip-Datei an geeigneter Stelle abspeichern.  
5. Heruntergeladene .zip-Datei entpacken, dabei soll das Verzeichnis **Begriffe2.0** entstehen.  
6. Inhalt des Verzeichnisses Begriffe2.0 kurz prüfen.  
7. In einem Terminal (bzw. Eingabeaufforderung, cmd) in dem Verzeichnis gede aufrufen, in dem das Verzeichnis Begriffe2.0 enthalten ist.  
8. gede erstellt dann das Verzeichnis **web2.0** in diesem Verzeichnis, in dem die erstellten HTML5-Dateien usw. enthalten sind.  
9. Ausgaben von gede und erstellte Dateien im Verzeichnis web2.0 prüfen.  
10. Erstellte Dateien in web2.0 auf Webserver hochladen.  

## Hinweise
Der Aufruf **gede -?** gibt eine Kurzanleitung aus.  
Es wurde versucht, gede portabel zu programmieren, so dass es auch auf nicht-Linux-Rechnern funktionieren sollte.
