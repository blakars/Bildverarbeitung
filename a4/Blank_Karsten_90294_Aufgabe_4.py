import cv2 as cv
import numpy as np
from tkinter import filedialog

#Funktion zum Laden eines Bildes
def loadPicture():
    imgLoad = filedialog.askopenfilename(initialdir="/Users/kabla/OneDrive/Desktop/Studium/SS22/TI-4/Bildverarbeitung/Praktikum/a4", filetypes=(("png files", "*.png"),("jpg files", "*.jpg")))
    img = cv.imread(imgLoad,flags=cv.IMREAD_UNCHANGED)
    return img   

#Funktion für die Template-Suche
def templateSearch():
    #Suchbild laden und in RGB konvertieren (Suchbild braucht kein Alphakanal) und Höhe/Breite des Suchbilds bestimmen
    suchbild = loadPicture()
    cv.namedWindow("Suchbild")
    suchbild=cv.cvtColor(suchbild,cv.COLOR_RGBA2RGB)
    h2,w2=suchbild.shape[:2]
    
    #Templatebild laden und Höhe/Breite des Templatebilds bestimmen
    templatebild = loadPicture()
    cv.namedWindow("Template-Bild")
    h,w = templatebild.shape[:2]

    #Alphakanal von Templatebild separieren für Maske
    base = templatebild[:,:,0:3]
    alpha = templatebild[:,:,3]

    #Templatematching-Verfahren erzeugt Heatmap 
    correlation = cv.matchTemplate(suchbild,base,cv.TM_CCORR_NORMED,mask=alpha)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(correlation)
    top_left = max_loc
    bottom_right = (top_left[0]+w,top_left[1]+h)
    cv.namedWindow("Heat-Map")
    correlation = cv.resize(correlation,(w2,h2),interpolation=cv.INTER_AREA)
    
    #Normalisieren der Heatmap und Überlagern der Heatmap mit Template
    correlationC=None
    correlationC=cv.normalize(correlation,correlationC,alpha=0,beta=255,norm_type=cv.NORM_MINMAX,dtype=cv.CV_8U)
    cv.imshow("Heat-Map",correlationC)
    correlationC=cv.cvtColor(correlationC,cv.COLOR_GRAY2RGB)
    roi=correlationC[top_left[1]:top_left[1]+h,top_left[0]:top_left[0]+w]
    mask_inverted=cv.bitwise_not(alpha)
    correlationC_bg=cv.bitwise_and(roi,roi,mask=mask_inverted)
    correlationC_fg=cv.bitwise_and(base,base,mask=alpha)
    new=cv.add(correlationC_bg,correlationC_fg)
    correlationC[top_left[1]:top_left[1]+h,top_left[0]:top_left[0]+w]=new
    cv.imshow("Suchbild",suchbild)
    cv.imshow("Template-Bild",templatebild)
    cv.imshow("Heat-Map ueberlagert",correlationC)


#Main
templateSearch()
while True:
    key = cv.waitKey(1)

    #wenn "q" -> break
    if key == 113:
        break
    
    #wenn "n" -> neues Bild laden
    elif key == 110:
        templateSearch()

cv.destroyAllWindows()