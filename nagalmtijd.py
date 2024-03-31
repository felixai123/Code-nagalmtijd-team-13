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

workbook = xlsxwriter.Workbook('metingen.xlsx') #maakt of opent een excel bestand
worksheet = workbook.add_worksheet() # maakt of opent een excel tab in de excel bestand

# Verander de huidige directory naar de map met de geluidsbestanden
os.chdir("E:\\project\\blok3\\metingen")

exceldata = []  # Lijst om de nagalmtijden in op te slaan
row_names = []  # Lijst om de rijnamen bij te houden

# Opmaak voor vetgedrukte tekst
bold = workbook.add_format({'bold': True})

for k in range(57):  # Bereik tot 57 (aantal 4 kante meters wat we gemeten hebben)
    for l in range(3):  # Bereik tot 3 (aantal metingen per 4 kante meters)
        #leest het bestand en haalt de gegevens eruit
        # Dynamisch genereren van bestandsnaam op basis van iteratievariabelen k en l
        wavefile = wave.open(str(k+1) + "_" + str(l+1) + ".wav")

        # Haal gegevens uit het bestand
        lenght = wavefile.getnframes()

        ydata = []
        gemdata = []
        td = -1
        tstart = 0
        teind = 0
        
        #dus wat hij zegt is dat hij alle code wat in de for loop zit net zo vaak herhaald als de lengte van de data
        for i in range(0, lenght):
            #hier leest hij de data
            wavedata = wavefile.readframes(1)
            data = struct.unpack("<h", wavedata)
            #hier pakt hij de eerste data in de varriabelle
            y = data[0]

            #als de data in het begin van de lijst ooit 0 word, dan komt er -60 db bij
            if y == 0:
                ydata.append(-60)
                continue

            
            y = 20 * log10(abs(y) / 2 ** 15)
            ydata.append(y)

            #hij pakt het gemiddelde van de sinusoide van de afgelopen kwart seconden
            if i >= 11025:
                #haalt elke de eerste data uit de lijst ydata als i groter of gelijk is aan kwart seconden
                ydata.pop(0)
                #telt de hele lijst van ydata bij elkaar op en doet dat gedeelt door de aantal data van ydata. om de gemiddelde
            gemdata.append(sum(ydata) / len(ydata))

            #dit is een laat bar, dit doen we omdat we anderssuper veel getallen krijgen. (dit is dan makkelijker aftelezen)
            #hier zegt ie dat "te" gelijk is aan de aantal seconden in het bestand door de data.
            te = round(i / 44100, 1)
            if te != td:
                print(str(te) + " s verwerkt")
                #verhoogt "td" met 0,1 seconden
                td = te
        #hij kijkt in alle data van gemdata (de gemiddelde data) 
        for i in range(len(gemdata)):
            #zodra hij een halve seconde berijkt neemt de code aan dat de geluidsbox is begonnen
            if i >= 22050 and tstart == 0:
                #dB waarde waarmee het begint
                dBstart = gemdata[22050]
                if gemdata[i] <= dBstart - 3 and gemdata[i] >= dBstart - 3.1:
                    #pakt het beginstijd van de nagalmtijd als de gemiddelde waarde van de data met 3 dB dropt
                    tstart = i
            if i >= 22050 and teind == 0:
                if gemdata[i] <= dBstart - 13 and gemdata[i] >= dBstart - 13.1:
                    #pakt het eind tijd van de nagalmtijd als de gemmidelde waarde van de data met 13 dB dropt vergeleken met de orginele waarde
                    teind = i
                    break
        #44100 is 1 seconde, berekent de nagalmtijd
        t = (teind - tstart) / 44100
        print("nagalmtijd is " + str(6 * t))
        exceldata.append(6 * t)
        
        # Voeg de rijnaam toe aan de lijst
        row_names.append(f"meting {k+1}")

        if len(exceldata) % 3 == 0:
            # Als de lengte van exceldata een veelvoud van 3 is, voeg dan een nieuwe rij toe in het werkblad
            row = len(exceldata) // 3 - 1
            worksheet.write(row, 0, row_names[-3], bold)  # Schrijf de rijnaam (vetgedrukt)
            worksheet.write(row, 1, exceldata[-3])  # Schrijf de eerste waarde van de set
            worksheet.write(row, 2, exceldata[-2])  # Schrijf de tweede waarde van de set
            worksheet.write(row, 3, exceldata[-1])  # Schrijf de derde waarde van de set
        
        """
        x = np.linspace(0, len(gemdata)/44100,len(gemdata))
        plt.plot(x,gemdata)
        plt.ylabel("dB")
        plt.xlabel("t(s)")
        plt.show
        """
       
print(exceldata)
workbook.close()
