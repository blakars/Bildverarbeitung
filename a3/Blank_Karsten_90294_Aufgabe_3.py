import cv2 as cv
import numpy as np
from tkinter import filedialog


#Funktion für Mauskmove
def onMove(event,x,y,flags,param):
    if event == cv.EVENT_MOUSEMOVE:
        #Erstelle Kopie des Ursprungsbildes = Wird zum dynamischen Aktualisieren verwendet
        img1C=img1.copy()

        #Je nachdem wie groß das zu überlagernde Bild (=Wally-Kopf) ist,
        #muss die Region of Interest (roi) unterschiedlich gewählt werden
        if rows % 2 ==0 and cols % 2 ==0:
            roi=img1C[y-rows//2:y+rows//2,x-cols//2:x+cols//2]
        elif rows %2 == 0 and cols % 2!=0:
            roi=img1C[y-rows//2:y+rows//2,x-cols//2-1:x+cols//2]
        elif rows %2 != 0 and cols % 2 ==0:
            roi=img1C[y-rows//2-1:y+rows//2,x-cols//2:x+cols//2]
        else:
            roi=img1C[y-rows//2-1:y+rows//2,x-cols//2-1:x+cols//2]

        #Maske aus Alphakanal erzeugen und invertieren
        #Bitwise-And-Verknüpfung zur Erzeugung des
        #Ergebnisses für die Region of Interest (mittels cv.add)
        mask=img2[...,3]
        mask_inverted=cv.bitwise_not(mask)
        img1_bg=cv.bitwise_and(roi,roi,mask=mask_inverted)
        img2_fg=cv.bitwise_and(img2,img2,mask=mask)

        new=cv.add(img1_bg,img2_fg)

        #Je nachdem wie groß Input-Bild/ROI, wird im Gesamtbild
        #der entsprechende Bereich mit dem Ergebnis ersetzt
        if rows % 2 ==0 and cols % 2 ==0:
            img1C[y-rows//2:y+rows//2,x-cols//2:x+cols//2]=new
        elif rows %2 == 0 and cols % 2!=0:
            img1C[y-rows//2:y+rows//2,x-cols//2-1:x+cols//2]=new
        elif rows %2 != 0 and cols % 2 ==0:
            img1C[y-rows//2-1:y+rows//2,x-cols//2:x+cols//2]=new
        else:
            img1C[y-rows//2-1:y+rows//2,x-cols//2-1:x+cols//2]=new

        #Berechnung der Übereinstimmung von Hintergrund-Bild mit
        #Wally-Kopf / überlagerndem Bild mittels matchTemplate
        #und Ausgabe des Ergebnisses über putText
        res = cv.matchTemplate(roi,img2,cv.TM_SQDIFF_NORMED)
        #min_val,max_val,min_loc,max_loc=cv.minMaxLoc(res)
        org = (30,30)
        img1C = cv.putText(img1C,str(res),org,cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv.LINE_AA)
        cv.imshow("Window",img1C)

#Funktion zum Laden eines Bildes
def loadPicture():
    imgLoad = filedialog.askopenfilename(initialdir="/Users/kabla/OneDrive/Desktop/Studium/SS22/TI-4/Bildverarbeitung/Praktikum/a3", filetypes=(("png files", "*.png"),("jpg files", "*.jpg")))
    img = cv.imread(imgLoad,flags=cv.IMREAD_UNCHANGED)
    return img

#Main
img1 = loadPicture()
cv.namedWindow("Window")
img2=cv.imread('RGBA1.png',flags=cv.IMREAD_UNCHANGED)
rows,cols,channels=img2.shape

while True:
    cv.imshow("Window",img1)
    cv.setMouseCallback("Window",onMove)
    key = cv.waitKey(0)

    #wenn "q" -> break
    if key == 113:
        break

cv.destroyAllWindows()