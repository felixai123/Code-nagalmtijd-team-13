# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:12:32 2024

@author: jarno
"""
import wave, struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from math import log10
import os
import xlsxwriter
"""
Belangrijk!!!!!
Alle bestanden moeten in de goeie volgorde qwa naam zijn, bijv. 1_1, 1_,2, 1_3, 2_1 ...
"""

workbook = xlsxwriter.Workbook('metingen.xlsx') #maakt of opent een excel bestand
worksheet = workbook.add_worksheet() # maakt of opent een excel tab in de excel bestand

# Verander de huidige directory naar de map met de geluidsbestanden
os.chdir("E:\\project\\blok3\\metingen")

exceldata = []  # Maakt de lijst om de nagalmtijden in op te slaan
row_names = []  # Maakt de lijst om de rijnamen bij te houden

# Opmaak voor vetgedrukte tekst in excel (dit word gedaan met bijvoorbeeld de teksten: meting 1, meting 2 etc.)
bold = workbook.add_format({'bold': True})

for k in range(57):  # Bereik tot 57 (aantal vierkante meters wat we gemeten hebben)
    for l in range(3):  # Bereik tot 3 (aantal metingen per vierkante meters)
        #leest het bestand en haalt de gegevens eruit
        # Dynamisch genereren van bestandsnaam op basis van iteratievariabelen k en l
        wavefile = wave.open(str(k+1) + "_" + str(l+1) + ".wav") #ik doe +1 omdat de iteratievariabelen k en l bij 0 beginnen, en je wilt bij 1 beginnen

        #Haalt de antaal verschillende data uit het bestand
        lenght = wavefile.getnframes()

        
        ydata = []
        gemdata = []
        td = -1
        tstart = 0
        teind = 0
        
        #dus wat hij zegt is dat hij alle code wat in de for loop zit net zo vaak herhaald als de lengte van de data (dus 0 tot max aantal data)
        for i in range(0, lenght):
            #hier leest hij de data
            #In de context van wavefile.readframes(1), leest het 1 argument één frame van het audiobestand in. Dit betekent dat het audiobestand wordt gelezen frame voor frame.
            wavedata = wavefile.readframes(1)
            """
            struct.unpack: Dit is de functie van de struct-module die wordt gebruikt om binair gestructureerde gegevens te interpreteren en te converteren naar Python-datatypen.
            "<h": Dit is het formaat van de gegevens waarin wordt aangegeven hoe de binaire gegevens moeten worden geïnterpreteerd. In dit geval staat h voor een enkelvoudige 16-bit signed integer (kleine 'h' staat voor een 16-bit signed integer).
            wavedata: Dit zijn de binaire gegevens die moeten worden geïnterpreteerd en omgezet naar Python-datatypen.
            Dus de uitdrukking struct.unpack("<h", wavedata) neemt de binaire gegevens in de variabele wavedata, interpreteert deze als een enkelvoudige 16-bit signed integer (kleine endianness) en retourneert deze als een Python-datatuple.
            Een tuple in Python is een gegevenstype dat lijkt op een lijst, maar onveranderlijk is, wat betekent dat de elementen niet kunnen worden gewijzigd nadat de tuple is gemaakt. Een tuple kan elementen van verschillende datatypen bevatten en kan een willekeurig aantal elementen bevatten. In het geval van struct.unpack, retourneert het een tuple met één element, omdat we slechts één gegevenstype specificeren in de structuur (<h staat voor een enkele 16-bit signed integer).
            Dus, als we struct.unpack("<h", wavedata) uitvoeren, retourneert het een tuple met één element dat de geïnterpreteerde waarde van wavedata bevat. Dit betekent dat data een tuple is met één element.
            """
            data = struct.unpack("<h", wavedata)
            #hier pakt hij de eerste data in de varriabelle (dus tuple)
            y = data[0]

            #als de data in het begin van de lijst ooit 0 word, dan komt er -60 db de lijst ydata en door de functie "continue" slaat hij alles over wat na deze if statement komt
            if y == 0:
                ydata.append(-60)
                continue

            #haalt de absolute waarde van in dB uit y (dus de eerste data uit de tuple)
            y = 20 * log10(abs(y) / 2 ** 15)
            #voegd de y waarde (aantal dB in de eerste tuple) bij de lijst ydata
            ydata.append(y)

            #hij pakt het gemiddelde van de sinusoide van de afgelopen kwart seconden
            if i >= 11025:
                #haalt elke keer de eerste data uit de lijst ydata als i groter of gelijk is aan kwart seconden
                ydata.pop(0)
            #telt de hele lijst van ydata bij elkaar op en doet dat gedeelt door de aantal data van ydata. om de gemiddelde van alle dB waardes eruit te krijgen
            gemdata.append(sum(ydata) / len(ydata))

            #dit is een laat bar, dit doen we omdat we anders super veel getallen krijgen. (dit is dan makkelijker aftelezen)
            #hier zegt ie dat "te" gelijk is aan de aantal data in het bestand gedeelt door de aantal data per seconden. Voor CD-kwaliteit audio is de standaard sample rate 44100 samples per seconde. Dit betekent dat er 44100 samples worden genomen van het analoge audiosignaal in één seconde tijd. en ,1 betekent dat hij afrond op 1 cijfer achter de comma
            te = round(i / 44100, 1)
            #als "te" niet gelijk is aan "td", dus als "td" (-1 betekent het einde van de lijst, dus in dit geval)  niet gelijk is aan het aantal seconden
            if te != td:
                #print elke keer aantal seconden
                print(str(te) + " s verwerkt")
                #verhoogt "td" met 0,1 seconden
                td = te
        #hij kijkt in alle data van gemdata (de gemiddelde dB waardes) 
        for i in range(len(gemdata)):
            #zodra hij een halve seconde berijkt neemt de code aan dat de geluidsbox is begonnen
            if i >= 22050 and tstart == 0:
                #dB waarde waarmee het begint
                dBstart = gemdata[22050]
                #dus hij kijkt of de i waarde in de lijst gemdata (gemiddelde dB waarde) of dat kleiner of gelijk is aan begin dB waarde (dBstart) - 3 en of het groter of gelijk is aan dBstart -3.1
                if gemdata[i] <= dBstart - 3 and gemdata[i] >= dBstart - 3.1:
                    #pakt het begintijd van de nagalmtijd als de gemiddelde waarde van de dB waarde met 3 dB dropt
                    tstart = i
            #zodra hij een halve seconde berijkt neemt de code aan dat de geluidsbox is geindigd
            if i >= 22050 and teind == 0:
                #dus hij kijkt of de i waarde in de lijst gemdata (gemiddelde dB waarde) of dat kleiner of gelijk is aan begin dB waarde (dBstart) - 13 en of het groter of gelijk is aan dBstart -13.1
                if gemdata[i] <= dBstart - 13 and gemdata[i] >= dBstart - 13.1:
                    #pakt het eind tijd van de nagalmtijd als de gemmidelde waarde van de data met 13 dB dropt vergeleken met de orginele waarde
                    teind = i
                    #stopt de for loop "for i in range(len(gemdata)):"
                    break
        #44100 is 1 seconde, berekent de nagalmtijd
        t = (teind - tstart) / 44100
        print("nagalmtijd is " + str(6 * t))
        #voegd de nagalmtijd aan de lijst van nagalmtijd waardes, die uiteindelijk in de excel document komen
        exceldata.append(6 * t)
        
        # Voeg de rijnaam toe aan de lijst
        row_names.append(f"meting {k+1}")

        #elke keer als er een rij van drie nagalmtijden in de excel document komen gaat hij naar de volgende regel (dit heb ik gedaan omdat we op elke positie 3 keer gemeten opgenomen hebben)
        if len(exceldata) % 3 == 0:
            # Als de lengte van exceldata een veelvoud van 3 is, voeg dan een nieuwe rij toe in het werkblad
            row = len(exceldata) // 3 - 1
            worksheet.write(row, 0, row_names[-3], bold)  # Schrijf de rijnaam (vetgedrukt)
            worksheet.write(row, 1, exceldata[-3])  # Schrijf de eerste waarde van de set
            worksheet.write(row, 2, exceldata[-2])  # Schrijf de tweede waarde van de set
            worksheet.write(row, 3, exceldata[-1])  # Schrijf de derde waarde van de set
        
        #dit is vom de grafiek van dB door de tijd (heb dit uitgezet omdat hij anders 120 grafieken maakt)
        """
        x = np.linspace(0, len(gemdata)/44100,len(gemdata))
        plt.plot(x,gemdata)
        plt.ylabel("dB")
        plt.xlabel("t(s)")
        plt.show
        """

print(exceldata)
workbook.close()
