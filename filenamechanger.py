# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 18:41:53 2024

@author: Jarno
"""

import os
#zoekt in de juiste folder
os.chdir(r"E:\\project\\blok3\\metingo")

#140 was in dit geval meer dan aantal bestanden
for i in range(140):
    #loopt 3 extra keer omdat wij 3 opnames per blokje hebben gedaan
    for j in range(3):
        #de oude naam
        old_name = "meting"+ str(i+1) + "-" + str(j+1) + ".wav"
        #de nieuwe naam
        new_name = str(i+1) + "_" + str(j+1) + ".wav"
        
        #wat try: betekent is, dat hij zegt dat hij moet proberen door alle bestanden heen te gaan in de volder maar de bepaalde voorwaarde niet voldoet, dan zegt except dat hij dat overslaat
        try:
            #veranderd de oude naam naar de nieuwe
            os.rename(old_name, new_name)
            print("Bestandsnaam gewijzigd van", old_name, "naar", new_name)
        except FileNotFoundError:
            print("Bestand", old_name, "niet gevonden. Overslaan...")
