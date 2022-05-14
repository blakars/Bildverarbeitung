import cv2 as cv
import numpy as np
from tkinter import filedialog

#Variablen definieren (Polygon-Array und Zähler-Variable)
coordinates=[]

#Funktion für Mausklick
def onClick(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        coordinates.append((x,y))
        cv.circle(img1,(x,y),4,(0,0,255),-1)

#Funktion zum Laden eines Bildes
def loadPicture():
    imgLoad = filedialog.askopenfilename(initialdir="/Users/kabla/OneDrive/Desktop/Studium/SS22/TI-4/Bildverarbeitung/Praktikum/a3", filetypes=(("png files", "*.png"),("jpg files", "*.jpg")))
    img = cv.imread(imgLoad,flags=cv.IMREAD_UNCHANGED)
    return img

#Main
img1 = loadPicture()
cv.namedWindow("Window")


while True:
    cv.setMouseCallback("Window",onClick)
    cv.imshow("Window",img1)
    key = cv.waitKey(1)

    #wenn "q" -> break
    if key == 113:
        break
    
    #wenn "s" -> Alpha-Kanal hinzufügen und freigestelltes Bild abspeichern
    elif key == 115:
        img2=cv.imread('RGBA1.png',flags=cv.IMREAD_UNCHANGED)
        rows,cols,channels=img2.shape
        x1,y1=coordinates[0]

        if rows % 2 ==0 and cols % 2 ==0:
            roi=img1[y1-rows//2:y1+rows//2,x1-cols//2:x1+cols//2]
        elif rows %2 == 0 and cols % 2!=0:
            roi=img1[y1-rows//2:y1+rows//2,x1-cols//2-1:x1+cols//2]
        elif rows %2 != 0 and cols % 2 ==0:
            roi=img1[y1-rows//2-1:y1+rows//2,x1-cols//2:x1+cols//2]
        else:
            roi=img1[y1-rows//2-1:y1+rows//2,x1-cols//2-1:x1+cols//2]
        
        res = cv.matchTemplate(roi,img2,cv.TM_SQDIFF)
        #cv.normalize(res,res,0,1,cv.NORM_MINMAX,-1)
        min_val,max_val,min_loc,max_loc=cv.minMaxLoc(res)

        #res = cv.absdiff(roi,img2)
        #res = res.astype(np.uint8)
        #percentage = (np.count_nonzero(res)*100)/res.size

        mask=img2[...,3]
        mask_inverted=cv.bitwise_not(mask)
        img1_bg=cv.bitwise_and(roi,roi,mask=mask_inverted)
        img2_fg=cv.bitwise_and(img2,img2,mask=mask)

        new=cv.add(img1_bg,img2_fg)

        if rows % 2 ==0 and cols % 2 ==0:
            img1[y1-rows//2:y1+rows//2,x1-cols//2:x1+cols//2]=new
        elif rows %2 == 0 and cols % 2!=0:
            img1[y1-rows//2:y1+rows//2,x1-cols//2-1:x1+cols//2]=new
        elif rows %2 != 0 and cols % 2 ==0:
            img1[y1-rows//2-1:y1+rows//2,x1-cols//2:x1+cols//2]=new
        else:
            img1[y1-rows//2-1:y1+rows//2,x1-cols//2-1:x1+cols//2]=new

        org = (30,30)
        img1 = cv.putText(img1,str(min_val),org,cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv.LINE_AA)

cv.destroyAllWindows()