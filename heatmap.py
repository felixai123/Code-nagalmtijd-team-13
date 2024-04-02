# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:27:52 2024

@author: jarno
"""

import matplotlib.pyplot as plt
import pandas as pd

file = r'E:\project\blok3\metingo\gemiddelde.xlsx'

# Lees de data die in een excel document staan. Header=None geeft aan dat er geen specifieke header moet zijn
# waar die op moet letten.
data_df = pd.read_excel(file, header=None)

#1 num_rows geeft aan hoeveel blokjes je wil hebben op de y-as
#2 num_cols is hoeveel blokjes je wil creëren op de x-as. Dit doe je door de eerste rij in het excel document
#2 te delen door het aantal blokjes in je y-as. Het maakt de maximale aantal blokjes dat ONDER je maximum
#2 aantal data zit. Heb je 50 data getallen en je num_rows = 7, dan is num_cols ook 7 en gaat de laatste 
#2 datapunt verloren. (dit gebeurt door de //, omdat die alleen hele getallen geeft)
#3 data_df.iloc zorgt ervoor dat de heatmap een rechthoek is. values.reshape zet de num_rows en num_cols
#3 om in een numpy array EN zet daarna de 1D waardes van num_rows en num_cols om in 2D waardes met de rows
#3 die gekregen worden van num_rows en de columns van num_cols.
num_rows = 8
num_cols = 11
data = data_df.iloc[:num_rows * num_cols].values.reshape(num_rows, num_cols)

#1 De plt.figure maakt een plaatje aan van de heatmap en de figsize zegt in welke ratio die heatmap moet zijn
#2 plt.imshow laat het plaatje ook echt zien (soort van op de plt.show manier) van de data die eerder is 
#2 samengesteld. De cmap bepaalt welke kleuren er gebruikt worden, kan je zien bij de staaf rechts van de 
#2 heatmap. De interpolation bepaalt hoe ieder "blokje" eruit komt te zien, bv "nearest" geeft een duidelijk
#2 verschil tussen ieder blokje met een harde lijn, terwijl bicubic meer een gradient tussen de blokjes weergeeft.
#2 aspect='auto' zorgt ervoor dat de heatmap zo groot mogelijk zichtbaar wordt gemaakt in je ratio.
#2-Bonus <Hier kan mee gespeeld worden tussen: nearest, bilinear, bicubic, lanczos, hamming & hanning>
plt.figure(figsize=(16, 9))
plt.imshow(data, cmap='Reds', interpolation='bicubic', aspect='auto')


#1 Je maakt eerst een for loop die van 0 tot de lengte van num_rows gaat (in dit geval 6)
#2 In die for loop zit nog een for loop die van 0 tot de lengte van num_cols gaat
#3 plt.text maakt een nummer aan, met j en i op de x en y assen. (dus voor ieder getal in i en j, gaat het in het
#3 juiste vakje). 2f betekent dat die 2 decimalen achter de comma moet zetten. ha en va betekenen simpelweg
#3 dat de horizontale as en de verticale as centraal moeten zijn, dus het getal staat in het midden van je vakje
#3 Kleur is zwart.
for i in range(num_rows):
    for j in range(num_cols):
        plt.text(j, i, f'{data[i, j]:.2f}', ha='center', va='center', color='black')

#1 plt.colorbar maakt een staaf aan die de hele range van data neemt en aangeeft welke kleur erbij hoort.
#2 plt.title maakt een titel aan
#3 plt.xlabel geeft aan hoe breed de ruimte is
#4 plt.ylabel geeft de lengte van de ruimte aan
plt.colorbar(label='Intensity')
plt.title('Heatmap KENK-gemiddelde')
plt.xlabel('Breedte')
plt.ylabel('Lengte')

#1 Origineel bij een heatmap is er een zwarte rand aan de buitenkant. plt.gca().spines pakt die lijn
#1-4 en maakt het onzichtbaar. Als je zin hebt, kan je de False naar True vervangen (of # ervoor doen)
#1-4 en kijken wat er gebeurt. Ik raad Left aan om te laten zien.
#5 .tick_params pakt zowel de x als de y as hun lijnen om aan te geven waar blokjes randen zijn en maakt de
#5 lengte 0. Dit zorgt ervoor dat je ze niet kan zien en de ruimte gebruikt kan worden voor iets anders.
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().tick_params(axis='both', which='both', length=0)

# plt.xticks([]) haalt de nummers weg uit de x as, omdat we de breedte willen aangeven van de ruimte.
plt.xticks([])
# plt.yticks([]) haalt de nummers weg uit de y as, zodat we de lengte kunnen aangeven van de ruimte.
plt.yticks([])

# Ik maak hier een ruwe text aan en positioneer deze precies boven de "Breedte" en geef aan wat het moet
# zeggen (24m). Zoals eerder, de ha en va zorgen ervoor dat het centraal staat, al is dit minder belangrijk.
# De size is 15, om het duidelijker in beeld te krijgen.
plt.text(num_cols/2 - 0.6, -0.65, '11m', ha='center', va='center', size="15")
# Hetzelfde als bij degene hierboven, alleen draai ik deze 90 graden, zodat het geldt voor de Lengte.
plt.text(-0.6, num_rows/2 - 0.615, '8m', ha='center', va='center', rotation=90, size="15")

# plt.ylim zorgt ervoor dat ik de x as "Breedte" kan bewegen ten opzichte van de heatmap, waardoor ik het
# beter kan plaatsen onder de 24m.
plt.ylim(-0.7, num_rows - 0.5)
# plt.xlim doet precies hetzelfde als ylim, maar dan voor de y as. Daarna is het een beetje spelen met nummers
plt.xlim(-0.7, num_cols - 0.5)

# Deze is toevallig overbodig, omdat er al een plaatje van wordt gemaakt door python zelf, maar nu geven we
# de echte opdracht om het te laten zien, niet hopen dat python het zelf bedenkt om te laten zien.
plt.show()