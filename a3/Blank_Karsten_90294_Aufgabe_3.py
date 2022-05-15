import cv2 as cv
import numpy as np
from tkinter import filedialog

#Variablen definieren (Polygon-Array und Zähler-Variable)
coordinates=[]

#Funktion für Mauskmove und -klick
def onMove(event,x,y,flags,param):
    if event == cv.EVENT_MOUSEMOVE:
        img1C=img1.copy()
        if rows % 2 ==0 and cols % 2 ==0:
            roi=img1C[y-rows//2:y+rows//2,x-cols//2:x+cols//2]
        elif rows %2 == 0 and cols % 2!=0:
            roi=img1C[y-rows//2:y+rows//2,x-cols//2-1:x+cols//2]
        elif rows %2 != 0 and cols % 2 ==0:
            roi=img1C[y-rows//2-1:y+rows//2,x-cols//2:x+cols//2]
        else:
            roi=img1C[y-rows//2-1:y+rows//2,x-cols//2-1:x+cols//2]

        mask=img2[...,3]
        mask_inverted=cv.bitwise_not(mask)
        img1_bg=cv.bitwise_and(roi,roi,mask=mask_inverted)
        img2_fg=cv.bitwise_and(img2,img2,mask=mask)

        new=cv.add(img1_bg,img2_fg)

        if rows % 2 ==0 and cols % 2 ==0:
            img1C[y-rows//2:y+rows//2,x-cols//2:x+cols//2]=new
        elif rows %2 == 0 and cols % 2!=0:
            img1C[y-rows//2:y+rows//2,x-cols//2-1:x+cols//2]=new
        elif rows %2 != 0 and cols % 2 ==0:
            img1C[y-rows//2-1:y+rows//2,x-cols//2:x+cols//2]=new
        else:
            img1C[y-rows//2-1:y+rows//2,x-cols//2-1:x+cols//2]=new

        #cv.circle(imgCopy,(x,y),4,(0,0,255),-1)
        #roiGray=cv.cvtColor(roi, cv.COLOR_RGBA2GRAY)
        #img2Gray=cv.cvtColor(img2,cv.COLOR_RGBA2GRAY)
        res = cv.matchTemplate(roi,img2,cv.TM_SQDIFF_NORMED)
        min_val,max_val,min_loc,max_loc=cv.minMaxLoc(res)
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
    
    #wenn "s" -> Alpha-Kanal hinzufügen und freigestelltes Bild abspeichern
    '''
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
        
        res = cv.matchTemplate(roi,img2,cv.TM_SQDIFF,mask=img2[...,3])
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
        img1 = cv.putText(img1,str(max_val),org,cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv.LINE_AA)
        '''

cv.destroyAllWindows()