#!/usr/bin/env python3
"""
Liest die als Parameter angegebene Datei zeilenweise.
Jede Zeile wird als Dateinamen verwendet.
Jeder dieser Dateinamen wird als HTML-Textdatei des Informatik-Begriffsnetzes eingelesen und
es wird analysiert, ob diese eine reine UTF-8-Datei ist oder ob diese mit 8-bit-ASCII-Zeichen 
verseucht ist (Mojibake). 
Als Ausgabe wird standardmäßig der Name der Datei ausgegeben, gefolgt von einem Doppelpunkt
und dem Text UTF-8 bzw. Zeichensalat (Mojibake)?
Durch Optionen können andere Ausgaben angefordert werden.
"""
Lizenz = "Dieser Quellkode steht unter der GNU GENERAL PUBLIC LICENSE 3 oder neuer."
Copyright = """Dieses Skript ist freie Software, die Sie unter bestimmten Bedingungen weitergeben dürfen. Diese stehen im Quellkode.
Für dieses Python-Skript besteht KEINERLEI GARANTIE, weder für MARKTREIFE noch für eine VERWENDBARKEIT FÜR EINEN BESTIMMTEN ZWECK."""
SkriptName = "utf8analyse"
SkriptRelease = "1"
SkriptVersion = "1"
SkriptDatum = "2026-03-15"
Autor = "Gerhard Fessler"
SkriptId = f"{SkriptName} {SkriptRelease}({SkriptVersion}), {SkriptDatum}, Copyright (c) {Autor}"
Usage = f"Aufruf:    {SkriptName} [option] ... dateiname"
UsageLong = f"""{__doc__}
{Usage}

Optionen:
   -a, --allezeichen: Gibt abschließend alle in den eingelesenen Dateien gefundenen Zeichen aus
   -h, --help, -?: Gibt diese Information aus
   -m, --mehr: Gibt mehr Daten aus. kann mehrfach angegeben werden
   -n, --nichtfiltern: Filtert bei Ausgaben ASCII-Standardzeichen nicht aus
   -q, --quiet: Gibt weniger Daten aus. Kann mehrfach angegeben werden
   -s, --single: dateiname ist eine direkt zu verarbeitende Datei
   -v, --version: Skriptname, Version und Format des Aufrufs ausgebenn
   -z, --zeilenweise: Liest Dateien Zeile für Zeile

dateiname:
Textdatei, enthält die Dateinamen der Dateien, deren UTF-8-Kompatibilität analysiert wird.
   - Ein Dateiname pro Zeile.

Beispiele:
   {SkriptName} -?
   {SkriptName} HTML-Dateinamen.txt
""" # UsageLong
# höchster Fehler: 8

########### Grundfunktionalitäten #############################################

import sys
import os

O = {
    "AlleZeichen" : False,
    "AusgabeLevel" : 1,
    "Direktdatei" : False,
    "Filtern" : True,
    "Zeilenweise" : False,
    } # Optionen

UTF8Zeichen = r""" abcdefghijklmnopqrstuvwxyzäöüßABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ0123456789|!"#&*,-./:;<=>@(´`”)+_[“„’]»%カバン板看®©€–…?{'}åø—""" + "\t\n\r\\"
UTF8ZeichenSet = frozenset(UTF8Zeichen)

ASCIICTRLNames = { 
    0: "NUL", 1: "SOH", 2: "STX", 3: "ETX", 4: "EOT", 5: "ENQ", 6: "ACK", 7: "BEL", 
    8: "BS", 9: "TAB", 10: "LF", 11: "VT", 12: "FF", 13: "CR", 14: "SO", 15: "SI", 
    16: "DLE", 17: "DC1", 18: "DC2", 19: "DC3", 20: "DC4", 21: "NAK", 22: "SYN", 23: "ETB", 
    24: "CAN", 25: "EM", 26: "SUB", 27: "ESC", 28: "FS", 29: "GS", 30: "RS", 31: "US", 
    127: "DEL", 
} 

# ANSI-Zeichen: Ausgabe einfärben
AEV = "" # ANSI Erweiterte Ausgaben Vordergrund
AEH = "\033[106m" # ANSI Erweiterte Ausgaben Hintergrund (cyan)
AEV1 = "" # ANSI Erweiterte Ausgaben Vordergrund
AEH1 = "\033[47m" # ANSI Erweiterte Ausgaben Hintergrund (grau)
AEV2 = "\033[0;32m" # ANSI Erweiterte Ausgaben Vordergrund (grün)
AEH2 = "\033[102m" # ANSI Erweiterte Ausgaben Hintergrund (grün)
AEV3 = "" # ANSI Erweiterte Ausgaben Vordergrund
AEH3 = "\033[103m" # ANSI Erweiterte Ausgaben Hintergrund (gelb)
AEV4 = "\033[2;92m" # ANSI Erweiterte Ausgaben Vordergrund (dunkelgrün)
AEH4 = "\033[42m" # ANSI Erweiterte Ausgaben Hintergrund (dunkelgrün)
AFV = "" # ANSI Fehler Vordergrund
AFH = "\033[101m" # ANSI Fehler Hintergrund (rot)
AR  = "\033[0m" # ANSI Reset
AWV = "" # ANSI Warnung Vordergrund
AWH = "\033[103m" # ANSI Warnung Hintergrund (gelb)

MengeAllerZeichen = set()

def PrintSkriptId():
    """Ausgabe der Identifikation des Skripts"""
    print(SkriptId)
    return None

def PrintUsage():
    """Ausgabe einer kurzen Anleitung zum Aufruf des Skripts"""
    print()
    print(Usage)
    print()
    return None

def PrintUsageLong():
    """Ausgabe ausführlicherer Informationen zum Skript"""
    print(Copyright)
    print(UsageLong)
    return None

def BeendeSkript(ExitCode):
    """Beenden des Skripts"""
    sys.exit(ExitCode)
    return None

def Warnung(WarnText):
    """Ausgabe einer Warnung auf STDERR"""
    print(f"    {AWH}{AWV}>>>> WARNUNG:{AR}", WarnText, file=sys.stderr)
    return None

def Fehler(FehlerText, ExitCode=1):
    """Ausgabe eines Fehlers auf STDERR und beenden des Skripts mit Fehlercode"""
    print(f"    {AFH}{AFV}#### FEHLER:{AR} ", FehlerText, file=sys.stderr)
    print()
    BeendeSkript(ExitCode)
    return None

def ExtrahiereCMDlineArgumente():
    """Wertet Aufruf des Skripts aus. Gibt Optionen und den Dateinamen getrennt zurück"""
    Optionen = []
    Argumente = []
    for Argument in sys.argv[1:]:
        if ( len(Argument) < 1 ):
            continue
        if ( Argument[0] == "-" ):
            Optionen.append(Argument)
        else:
            Argumente.append(Argument)
    return (Optionen, Argumente)

########### Skriptspezifische Funktionalitäten ################################

def OptionenAuswerten(Optionen):
    """Auswertung der Optionen aus dem Aufruf des Skripts"""
    EinzelOptionen = []
    for Text in Optionen:
        TextPur = Text.strip()
        if ( len(Text) < 1 ):
            Warnung(f"'{TextPur}': Leere Zeichenkette als Option, ignoriert")
            continue
        IndexDoppelMinus = TextPur.find("--")
        if ( IndexDoppelMinus >= 0 ):
            if ( len(TextPur) < 3):
                Warnung(f"'{TextPur}': Optionenzeichenkette fehlt, ignoriert")
                continue
            EinzelOptionen.append(TextPur)
            continue
        IndexMinus = TextPur.find("-")
        if ( IndexMinus >= 0 ):
            if ( len(TextPur) < 2):
                Warnung(f"'{TextPur}': - ohne Optionszeichen, ignoriert")
                continue
            for Zeichen in TextPur[1:]:
                EinzelOptionen.append(Zeichen)
            continue
        Warnung(f"'{Text}': Kein '-' in Optionenzeichenkette gefunden, ignoriert")
    for Option in EinzelOptionen:
        if ( (Option == "a") or (Option == "A") or (Option == "--allezeichen") or (Option == "--all") ):
            O["AlleZeichen"] = True
            continue
        if ( (Option == "--help") or (Option == "h") or (Option == "?") ):
            PrintUsageLong()
            BeendeSkript(0)
        if ( (Option == "m") or (Option == "M") or (Option == "--mehr") ):
            O["AusgabeLevel"] += 1
            continue
        if ( (Option == "n") or (Option == "N") or (Option == "--nichtfiltern") ):
            O["Filtern"] = False
            continue
        if ( (Option == "q") or (Option == "Q") or (Option == "--quiet") ):
            O["AusgabeLevel"] -= 1
            continue
        if ( (Option == "s") or (Option == "S") or (Option == "--single") ):
            O["Direktdatei"] = True
            continue
        if ( (Option == "--version") or (Option == "v") ):
            PrintScriptId()
            BeendeSkript(0)
        if ( (Option == "z") or (Option == "Z") or (Option == "--zeilenweise") ):
            O["Zeilenweise"] = True
            continue
        Warnung(f"'{Option}': Unbekannte Option, ignoriert")
    return None

def PruefeArgumente(Argumente):
    """Prüft, dass genau ein Dateiname angegeben ist und liefert diesen zurück, sofern dieser lesbar und nicht leer ist""" 
    DateinamenDateiname = ""
    LesbareDateien = []

    if ( len(Argumente) < 1 ):
        Fehler("dateiname nicht angegeben",1)
    if ( len(Argumente) > 1 ):
        Fehler(f"Mehr als ein dateiname angegeben: {Argumente}",2)

    DateinamenDateiname = Argumente[0].strip()
    if ( not os.path.isfile(DateinamenDateiname) ):
        Fehler(f"Auf '{DateinamenDateiname}' kann nicht als Datei zugegriffen werden",3)
    if ( not os.access(DateinamenDateiname, os.R_OK) ):
        Fehler(f"Datei '{DateinamenDateiname}' kann nicht gelesen werden",4)
    DateiGroesse = os.path.getsize(DateinamenDateiname)
    if ( DateiGroesse < 1 ):
        Fehler(f"Datei '{DateinamenDateiname}' ist leer",5)
    return DateinamenDateiname

def LeseDateinamen(DateinamenDateiname):
    """Liest die Dateinamen, die in der DateinamenDateiname enthalten sind, und gibt diese als Liste zurück"""
    DateinamenListe = []
    DateinamenZahl = 0
    try:
        with open(DateinamenDateiname, "r") as DateinamenDatei:
            for Zeile in DateinamenDatei:
                StrippedZeile = Zeile.strip()
                if ( len(StrippedZeile) < 1 ): 
                    continue
                DateinamenZahl += 1
                DateinamenListe.append(StrippedZeile)
    except Exception as Ausnahme:
        Fehler(f"Fehler {Ausnahme} beim Öffnen bzw. Lesen der Datei '{DateinamenDateiname}'. Keine Dateinamen eingelesen. Textdatei?",6)
        return []
    if ( O["AusgabeLevel"] > 1 ):
        print(f"{AEH2}{DateinamenDateiname}{AR}: {DateinamenZahl} Dateinamen eingelesen")
    return DateinamenListe

def LeseDateiByte(Dateiname):
    """Liest die Datei Dateiname als Bytes und gibt deren Inhalt als str zurück"""
    DateiInhalt = b""
    try:
        with open(Dateiname, "rb") as Datei:
            DateiInhalt = Datei.read()
    except Exception as Ausnahme:
        Warnung(f"{Ausnahme} beim Öffnen bzw. Lesen der Datei '{Dateiname}'.")
    if ( O["AusgabeLevel"] > 1 ):
        ZahlDerZeichen = len(DateiInhalt)
        ZahlUnterschiedlicherZeichen = len(set(DateiInhalt))
        print(f"{AEH1}{Dateiname}{AR}: {ZahlDerZeichen} Byte eingelesen, {ZahlUnterschiedlicherZeichen} unterschiedliche Zeichen")
    return DateiInhalt

def LeseDateiUTF8Str(Dateiname):
    """Liest die Datei Dateiname als UTF-8 und gibt deren Inhalt als str zurück"""
    DateiInhalt = ""
    try:
        with open(Dateiname, "r", encoding="utf-8", newline='') as Datei:
            DateiInhalt = Datei.read()
    except Exception as Ausnahme:
        Warnung(f"{Ausnahme} beim Öffnen bzw. Lesen der Datei '{Dateiname}'.")
    if ( O["AusgabeLevel"] > 1 ):
        ZahlDerZeichen = len(DateiInhalt)
        ZahlUnterschiedlicherZeichen = len(set(DateiInhalt))
        print(f"{AEH1}{Dateiname}{AR}: {ZahlDerZeichen} UTF-8-Zeichen eingelesen, {ZahlUnterschiedlicherZeichen} unterschiedliche Zeichen")
    return DateiInhalt

def LeseDateiUTF8Zeilenweise(Dateiname):
    """Liest die Datei Dateiname zeilenweise als UTF-8 und gibt deren Inhalt als str zurück"""
    DateiInhalt = ""
    Zeilen = []
    Zeilenzahl = 0
    try:
        with open(Dateiname, "r", encoding="utf-8", newline='') as Datei:
            for Zeile in Datei:
                Zeilenzahl += 1
                Zeilen.append(Zeile)
                if ( O["AusgabeLevel"] > 3 ):
                    print(f"{Dateiname}({Zeilenzahl}): {Zeile}")
    except Exception as Ausnahme:
        Warnung(f"{Ausnahme} beim Öffnen bzw. Lesen der Datei '{Dateiname}'")
    DateiInhalt = ''.join(Zeilen)
    if ( O["AusgabeLevel"] > 1 ):
        ZahlDerZeichen = len(DateiInhalt)
        ZahlUnterschiedlicherZeichen = len(set(DateiInhalt))
        print(f"{AEH1}{Dateiname}{AR}: {ZahlDerZeichen} UTF-8-Zeichen in {Zeilenzahl} Zeilen eingelesen, {ZahlUnterschiedlicherZeichen} unterschiedliche Zeichen")
    return DateiInhalt

###############################################################################

def UTF2Lesbar(Zeichen):
    """Macht aus dem einzelnen UTF-8-Zeichen Zeichen einen les- und nachvollziehbaren str"""
    if ( len(Zeichen) < 1 ):
        Fehler("Interner Fehler in UTF2Lesbar: Kein UTF-8-Zeichen übergeben",7)
    if ( len(Zeichen) < 1 ):
        Fehler("Interner Fehler in UTF2Lesbar: Mehr als ein UTF-8-Zeichen übergeben",8)
    Zeichenlesbar = Zeichen
    if ( Zeichen == " " ):
        Zeichenlesbar = " (SPACE)"
        return Zeichenlesbar
    OrdZeichen = ord(Zeichen)
    HexZeichen = hex(OrdZeichen)
    if ( OrdZeichen in ASCIICTRLNames ):
        Zeichenlesbar = f"({ASCIICTRLNames[OrdZeichen]}, {HexZeichen})"
        return Zeichenlesbar
    if ( Zeichen.isprintable() ):
        if ( OrdZeichen > 128 ):
            Zeichenlesbar += " (" + str(OrdZeichen) + ", " + HexZeichen + ")"
        return Zeichenlesbar
    # Zeichen nicht druckbar
    Zeichenlesbar = "(" + str(OrdZeichen) + ", " + HexZeichen + ")"
    return Zeichenlesbar

def PrintUTF8Zeichen(ZeichenMenge):
    for Zeichen in sorted(list(ZeichenMenge)):
        Zeichenlesbar = UTF2Lesbar(Zeichen)
        print(Zeichenlesbar)
    return None

def PrintZeichenDict(ZeichenDict):
    '''Gibt die in der Datei vorhadenen Zeichen inklusive deren Häufigkeit aus''' 
    Keys = sorted(list(ZeichenDict))
    ZahlDerZeichen = len(Keys)
    for Key in Keys:
        Haeufigkeit = ZeichenDict[Key]
        DruckKey = UTF2Lesbar(Key)
        if ( O["Filtern"] and (Key in UTF8ZeichenSet) ):
            continue
        print(f"{AEH}{DruckKey}{AR}: {Haeufigkeit}")
    return None

def AnalysiereUTF8(Inhalt):
    '''Analysiert str Inhalt auf nur akzeptable UTF-8-Zeichen'''
    NichtUTF8ZeichenMenge = set()

    global MengeAllerZeichen
    MengeAllerZeichen |= set(Inhalt)

    ZeichenDict = dict();
    for Zeichen in Inhalt:
        if ( Zeichen in ZeichenDict ):
            ZeichenDict[Zeichen] += 1
        else:
            ZeichenDict[Zeichen] = 1
        if ( Zeichen not in UTF8ZeichenSet ):
            NichtUTF8ZeichenMenge.add(Zeichen)

    return ZeichenDict, NichtUTF8ZeichenMenge

def VerarbeiteDatei(Dateiname):
    '''Liest Datei ein, analysiert den UTF-8-Status und gibt Ergebnis aus'''
    if ( O["Zeilenweise"] ):
        Inhalt = LeseDateiUTF8Zeilenweise(Dateiname)
    else:
        Inhalt = LeseDateiUTF8Str(Dateiname)

    (ZeichenDict, NichtUTF8ZeichenMenge) = AnalysiereUTF8(Inhalt)

    if ( len(NichtUTF8ZeichenMenge) > 0 ):
        Status = f"{AWH}Zeichensalat (Mojibake)?{AR}"
    else:
        Status = f"{AEV2}UTF-8{AR}"

    if ( O["AusgabeLevel"] < 1 ):
        if ( len(NichtUTF8ZeichenMenge) > 0 ):
            print(f"{Dateiname}: {Status}")
            PrintZeichenDict(ZeichenDict)
        return None

    print(f"{Dateiname}: {Status}")
    PrintZeichenDict(ZeichenDict)
    return None

###############################################################################
###############################################################################

(Optionen, Argumente) = ExtrahiereCMDlineArgumente()

if ( len(Optionen) > 0 ):
    OptionenAuswerten(Optionen)

if ( O["AusgabeLevel"] > 1 ):
    PrintSkriptId()
    print()

DateinamenDateiname = PruefeArgumente(Argumente)

if ( O["Direktdatei"] ):
    Dateinamen = [DateinamenDateiname]
else:
    Dateinamen = LeseDateinamen(DateinamenDateiname)

for Dateiname in Dateinamen:
    VerarbeiteDatei(Dateiname)

if ( O["AlleZeichen"]):
    print()
    print("Insgesamt gefundene Zeichen:")
    PrintUTF8Zeichen(MengeAllerZeichen)
