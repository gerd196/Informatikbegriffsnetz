# ReadME für gede    
2026-07-27, G. Fessler  
gede = Google-EDE, EDE = Elektronische Daten Erweiterung (2005)  

## Zweck  
gede erstellt aus den Dateien des Informatik-Begriffsnetzes der Gesellschaft für Informatik in Google-Drive im Verzeichnis **Begriffe2.0** (inklusive Unterverzeichnissen) statische HTML5-basierte Dateien zur Veröffentlichung im Internet.  
Ziel ist, dass die Pflege des Informatik-Begriffsnetzes vollständig im Google-Drive stattfindet, zur Veröffentlichung des jeweiligen Stands die Google-Drive-Dateien heruntergeladen werden, durch gede umgewandelt werden und die erstellten Dateien auf den Webserver hochgeladen werden.  

## Randbedingungen  
gede benötigt **Perl 5** und **Pandoc** (pandoc.org), beide müssen auf dem Rechner installiert sein. Pandoc muss über den Suchpfad aufrufbar sein.  

gede wurde hauptsächlich mit Perl 5.42 und Pandoc 3.9 unter Linux getestet. Es sollte auch unter älteren Verseionen von Perl 5 (mindestens ab 5.18) lauffähig sein.  

gede nutzt UTF-8 für Ausgaben. Unter Windows muss deshalb die Nutzung von UTF-8 in der Eingabeaufforderung freigeschaltet werden.  
Gemäß Google geht das so:  
* Einstellungen > Zeit und Sprache > Sprache und Region  
* > Adminstrative Spracheinstellungen  
* > Verwaltung > Systemgebietsschema ämdern  
* x Beta: Unicode UTF-8 für welweite Sprachunterstützung verwenden  
* ok  
* Reboot von Windows  

gede nutzt teilweise Farben zur Strukturierung von Ausgaben. Bei weißen Zeichen auf schwarzem Hintergrund kann das zu schwer lesbaren Texten führen. Getestet wurde gede mit schwarzen Zeichen auf weißem Hintergrund  
* Eventuell Farbschema der Konsole/Eingabeaufforderung anpassen.  

Da die Stabilität sowohl von Microsoft .docx-Dateien als auch deren Erstellung beim Download durch Google nicht garantierbar ist, wird das laufend gepflegte Konvertierungstool Pandoc für die Konvertierung der Google-Docs-Dateien in ein durch gede verarbeitbares Format verwendet. Wegen der Instabilitäten sollte jeweils die neueste Version von Pandoc verwendet werden.  

## Grobarchitektur  
gede arbeitet auf einem entzippten Download aus Google-Drive.  
Es wandelt die entzippten Microsoft-docx-Dateien mit Pandoc zuerst in ein verarbeitbares HTML-Format um und erzeugt daraus HTML 5 und zugehörige Dateien im Verzeichnis **web2.0** sowie in Unterverzeichnissen.  

Da die ZIP-Programme der Betriebssystemhersteller oft eigene Vorstellungen bezüglich der Ablage der entpackten Dateien haben, sollte zum Entpacken **7-ZIP** verwendet werden.  

Die Google-Docs-Dateien müssen den Kodierrichtlinien für Version 2.0 des Informatikbegriffsnetzes entsprechen, um umgewandelt werden zu können.  

## Installation  
gede in einem Verzeichnis im Suchpfad ablegen und bei unixoiden Systemen ausführbar machen.  
In Windows entweder eine **Batch-Datei** zum Aufrufen anlegen oder gede mit **perl -w gede ** *-optionen* aufrufen.  
Falls gede unter dem Namen D:\bin\gede gespeichert wurde, können in der Batch-Datei folgende Kommandos verwendet werden:  
  
>@ECHO OFF  
>perl -w D:\bin\gede %*  
>pause  
  
und gede mit  
  
>gede -optionen  
  
aufgerufen werden.  

Bei Windows-Nutzern ist es üblich (aber nicht notwendig) **gede** in **gede.pl** umzubenennen.  

## Nutzung  
0. perl 5 (ab Versison 5.18) und Pandoc (ab Version 3.5) auf dem Rechner installieren  
1. In Google Drive im Informatik-Begriffsnetz anmelden.  
2. Das Google-Docs-Verzeichnis Begriffe2.0 in einer Verzeichnisübersicht anzeigen.  
3. Rechtsklick auf Verzeichnis Begriffe2.0 → Herunterladen.  
4. Von Google-Drive erstellte .zip-Datei an geeigneter Stelle abspeichern.  
5. Heruntergeladene .zip-Datei entpacken, dabei soll das Verzeichnis **Begriffe2.0** entstehen.  
6. Inhalt des Verzeichnisses Begriffe2.0 kurz prüfen.  
7. In einem Terminal (bzw. Eingabeaufforderung, cmd) gede in dem Verzeichnis aufrufen, in dem das Verzeichnis Begriffe2.0 enthalten ist.  
8. gede erstellt dann das Verzeichnis **web2.0** in diesem Verzeichnis, in dem die erstellten HTML5-Dateien usw. enthalten sind.  
9. Ausgaben von gede und erstellte Dateien im Verzeichnis web2.0 prüfen.  
10. Erstellte Dateien in web2.0 auf Webserver hochladen.  

## Hinweise
Der Aufruf **gede -?** gibt eine Kurzanleitung aus.  
Es wurde versucht, gede portabel zu programmieren, so dass es auch auf nicht-Linux-Rechnern funktionieren sollte.  

## Hinweise zur Architektur von gede  

### Begriffsdefinitionen  
Begriffsdefinitionen werden in Google-Docs als Dateien erstellt.  
* Pro Datei genau ein Begriff  
* Wurzelverzeichnis in Google-Docs: Begriffe2.0  
* Hierarchische Strukturierung der Dateien unter dem Verzeichnis Begriffe2.0 möglich.  
* Jede Begriffsdatei in Google-Docs muss gemäß **ZZTemplate20** aufgebaut sein und der **Kodierrichtlinie** entsprechen.  
* Im Web anzuzeigende Bilder usw. in einer Begriffsdefinition sollten in der Google-Docs-Datei enthalten sein.  

### Download  
In Google-Docs:  
* Rechtsklick auf Verzeichnisname *Begriffe2.0* (oder die drei senkrechten Punkte rechts oder Tastenkombination <ALT>-A).  
* > Herunterladen  
* Warten bis Google den Download bereitgestellt hat.  
* Datei Begriffe2.0-....zip in geeignetem Verzeichnis speichern.  
Im Verzeichnis:  
* Falls im Verzeichnis ein Unterverzeichnis **Begriffe2.0** vorhanden ist, dieses **löschen**, um Probleme mit Altlasten zu vermeiden
* In dieses Verzeichnis wechseln und die Datei Begriffe2.0-....zip (vorzugsweise) mit 7-ZIP entpacken. Dabei entsteht ein Unterverzeichnis Begriffe2.0  
* gede aufrufen.  

### gede 1. Schritt  
1. Auswertung der Optionen im Aufruf (&CheckArgs, &ProcessOption)  
2. Initialisierung des Skripts (&Init, &PruefePandoc-Aufruf)  
3. Prüfung bzw. Herstellung der Randbedingungen (Begriffe2.0, web2.0, web2.0/media, &CheckBaseDir, &ErstelleOutDirs)  
4. Prüfung des Verzeichnisses, in dem die heruntergaldenen Dateien abgelegt sind (&CheckInputDir)  
5. Rekursiver Durchgang durch den heruntergekladenen Dateibaum (&LiesBegriffe, &ProcessDateiname, &ProcessVerzeichnisName)  
6. Kategorisierung der Dateien und Verzeichnisse anhand von Dateinamen und Extensionen (&KategorisiereDateiname)  
    Zuordnung von Absolutem Dateinamen im Filesystem zum Basenamen (Dateiname ohne Extension) für .docx-Dateien in %AbsDatinameToBasename  
7. Konvertierung von .docx-Datei in HTML-Fragmente durch Pandoc (&ProcessDocx, &ProcessPandocSTDERR, &ProcessNediaExtraction, &ProcesPandocLog)  
8. Ablage des erzeugten HTML-Fragments (&ProcessPandocHTML  
    Ablage in %HTMLByFilename  

### gede 2. Schritt  
HTML-Fragmente in Tabellenform umwandeln (&ProcessPandocHTMLs)  

1. Jedes einzelne HTML-Fragment Tokenisieren (&ProcessHTMLFragment,&TokenizePandocHTML)  
        HTML-Kommentare werden entfernt, Token sind Tags und HTML-Inhalte  
2. Pro .docx-Datei Aufteilen an tr- und /tr-Token in Zeilen (&TokenZuTabelle, &TokenZuZeilen)  
3. Aufgeteilte Zeilen an th bzw. td, /th, /td-Token in Zellen aufteilen (&TokenZuZellen) und in Tabelle einfügen  
4. Ablegen der Begriffsdaten als Viersturiger Baum in @BegriffeAlsTabellen  

### gede 3. Schritt  
Erste Prüfung und Umformung der Begriffstabellen in interne Datenbank (Perl: Hash, assoziativer Array, %BegriffeByBegriffsID)  

1. Prüfen, ob überhaupt verarbeitbare Daten vorliegen (&BegriffstabellenZuHash)  
2. Tabellen Hash umwandelt (&TabelleZuHash, &PruefeUndExtrahiereZeile)  
    
### gede 4. Schritt 
Syntaktische und (teilweise) sematische Analyse und Überprüfung des Inhalts der übernommenen Begriffe (&AnalysiereBegriffe, &AnalysiereBegriff)  

1. Analysieren aller Begriffe in %BegriffeByBegriffsId, Identifikation und Extraktion weiterer Ids und der Zusatz-Views (&AnalysiereBegriffe, &AnalysiereBegriffsId, &AnalysiereBegriff, &AnalysiereBegriffsText, &AnalysiereEngisch,&AnalysiereSynonyme, &AnalysiereFreigaben, &AnalysiereViews, %BegriffeZuBegriffsIds, %BegriffeByBegriffsIdA, $AlleIds, %ViewsFlach, %ViewsBaum).  


### gede letzter Schritt  
1. Gesammelte Ausgabe der Warnungen (und eventuell gesammelter Debug-Meldungen, &PrintWarnsDebugs, &PrintHinweise)  
2. Ausgabe statistischer Daten (&PrintTagStatistik, &PrintViews, &PrintStatistics)  

## Ungeklärte Punkte
Werden Englisch-Id bzw. Synonyme-Id benötigt?  
Unterviews in BegriffsIds?  
* / in Views in BegriffsIds zulassen?  
* Besser: __  
* Problem: Begriffs-Id == Dateiname  
Auch Buchstaben-Zugriffsweg in Zusatz-Views angeben?  
ALT-Attribut für Bilder usw.  
Pflege des CSS  
Pflege der nicht-Begriff-Webseiten  

