#!/usr/bin/env python
# coding: utf-8

# In[7]:


import cv2
import numpy as np


# In[8]:


#Definition von globalen Variablen, Laden des Ursprungsbildes
breite_neu = 1000
hoehe_neu= 500
img = cv2.imread('Waldo.JPG')
pgon=[]
cv2.namedWindow('image')

#Funktion für Maus-Klick
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        
        #Prüfen ob schon 4x geklickt, falls nein -> Malen des Punkts und Abspeichern der Koordinaten in Liste
        if len(pgon) < 4:
            cv2.circle(img,(x,y),4,(0,0,255),-1)
            pgon.append([x,y])
            print(len(pgon)) #print nur zum Debuggen
            print("x:",x,"  y:",y) #print nur zum Debuggen
            
        #Falls ja -> Fehlermeldung
        else:
            print("Too many arguments.")

#Initialisieren der Maus-Funktion für entsprechendes image-Fenster            
cv2.setMouseCallback('image',draw_circle)

#Dauer-Schleife
while True:
    #Bild anzeigen und Tastatur abfragen
    cv2.imshow('image',img)
    key = cv2.waitKey(1)
    
    #Falls "s" (=115) eingegeben wird:
    if key == 115:
        #Prüfung, dass 4 Punkte gewählt wurden
        if len(pgon) < 4:
            print("Zunächst 4 Punkte wählen.")
            
        #Falls 4 Punkte gewählt, dann werden die 4 Punkt-Koordinaten in eine numpy-Matrix überführt (m1)
        #wichtig: Reihenfolge der Punkte von oben links bis unten links analog zur "gemappten"-Matrix des neuen Bildes (m2)
        else:
            obli = [pgon[0][0],pgon[0][1]]
            obre = [pgon[1][0],pgon[1][1]]
            unre = [pgon[2][0],pgon[2][1]]
            unli = [pgon[3][0],pgon[3][1]]
            
            m1=np.float32([obli,obre,unre,unli])
            m2=np.float32([[0,0],[breite_neu,0],[breite_neu,hoehe_neu],[0,hoehe_neu]])
            
            #mit getPerspectiveTransform werden die Polygon-Koordinaten auf die Koordinaten des neuen rechteckigen Bildes gemappt
            #mit warpPerspective wird dann das entsprechende neue Bild erstellt und 
            #anschließend mit imwrite gespeichert und imshow angezeigt
            m3=cv2.getPerspectiveTransform(m1,m2)
            new_image=cv2.warpPerspective(img,m3,(breite_neu,hoehe_neu))
            cv2.imwrite('Waldo_neu.jpg',new_image)
            cv2.imshow('image_new',new_image)
            
            print(m1)
            print(m2)
    
    #Falls "q" (=113) eingegeben wird, wird Programm über break beendet
    if key == 113:
        break

cv2.destroyAllWindows()


# In[ ]:




