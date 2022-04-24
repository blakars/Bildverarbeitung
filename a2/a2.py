import cv2 as cv
import numpy as np
from tkinter import filedialog

#Variablen definieren (Polygon-Array und Zähler-Variable)
polygon=[]
counter=0

#Funktion für Mausklick
def onClick(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img,(x,y),4,(0,0,255),-1)
        polygon.append([x,y])
        if len(polygon) < 2:
            None
        else:
            cv.line(img,polygon[-2],polygon[-1],(0,0,255),thickness=2)

#Funktion zum Laden eines Bildes
def loadPicture():
    imgLoad = filedialog.askopenfilename(initialdir="/Users/kabla/OneDrive/Desktop/Studium/SS22/TI-4/Bildverarbeitung/Praktikum/a2", filetypes=(("png files", "*.png"),("jpg files", "*.jpg")))
    img = cv.imread(imgLoad)
    return img   

#Main
img = loadPicture()
cv.namedWindow("Window")
cv.setMouseCallback("Window",onClick)

while True:
    cv.imshow("Window",img)
    key = cv.waitKey(1)

    #wenn "q" -> break
    if key == 113:
        break
    
    #wenn "n" -> neues Bild laden
    elif key == 110:
        img = loadPicture()
    
    #wenn "s" -> Alpha-Kanal hinzufügen und freigestelltes Bild abspeichern
    elif key == 115:
        if polygon ==[]:
            print("Zunächst Polygon per Mausklick definieren")

        else:
            #Erstelle 0-Array für Alphakanal von Größe img-shape
            alphablank = np.zeros((img.shape[0],img.shape[1]), dtype='uint8')

            #Überschreibe polygon-Pixel des Alphakanal-Array mit "255"=transparent 
            cv.fillPoly(alphablank,np.array([polygon]),255)

            #Füge Alphakanal hinzu
            imgRGBA=cv.cvtColor(img,cv.COLOR_RGB2RGBA)
            
            #Setze Alphakanal auf das oben erstellte "Transparenz-Array"
            imgRGBA[:,:,3]=alphablank

            #Bild anzeigen, abspeichern, Counter für Datei-Bezeichnung erhöhen und Polygon-Array leeren
            cv.imshow("Ergebnis",imgRGBA)
            cv.imwrite('RGBA'+str(counter)+'.png',imgRGBA)
            counter+=1
            polygon=[]

cv.destroyAllWindows()