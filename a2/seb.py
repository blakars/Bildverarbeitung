#-----------------------------------------------------------
#Program    :Ray_Sebastian_91044_Aufgabe_2.py
#Written by :Sebastian Ray
#Date       :21.04.2022
#Description:Read an image. Cut out a new Image using key combinations (mouse) and convert to RGBA (A=alpha)
#-----------------------------------------------------------
#pip install numpy
from cv2 import waitKey
import numpy as np
import cv2 as cv
import time
import pdb                  #Breakpoints
from tkinter import *
from tkinter import filedialog


#declare variable
windowName = "cutOuthWally"
imgSave = "newCutWally"
polyCoordinates = np.array([[0,0]])                         #Stores the coordinates of a polygon
polyCoordinates = np.delete(polyCoordinates,0,axis=0)       #workaround -> No Idea how to create an empty array
ctr = 0


def rescaleFrame(frame, scale=0.50):                                    #Adjust the size of an image
    """Changes the size of an images"""
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)    #resize the image


def loadNewPicture():
    #Opens a new directory
    imgLoad = filedialog.askopenfilename(initialdir="/Users/kabla/OneDrive/Desktop/Studium/SS22/TI-4/Bildverarbeitung/Praktikum/a2", filetypes=(("png files", "*.png"),("jpg files", "*.jpg")))
    print("New image loaded!")    
    cv.namedWindow(windowName)                          #creates a window that can be used as a placeholder for images
    img1 = cv.imread(imgLoad)                           #loads an image from an specified file. Second Argument is an flag 
    img = rescaleFrame(img1,0.7)
    return img


img = loadNewPicture()


#mouse callback function
def draw_circle(event,x,y,flags,param):             #(event,x-coordinate,y-coordiante,flags,optional)
    global polyCoordinates
    if event == cv.EVENT_LBUTTONUP:                 #mouse events. 
        cv.circle(img,(x,y),3,(0,0,255),-1)         #draw a circle.(img where drawn,centre,radius,color,thickness,?,?)
        
        if len(polyCoordinates) < 20:
            print("x=",x," y=",y)
            polyCoordinates = np.append(polyCoordinates,[[x,y]], axis=0)    #Puts the points into an array
            if len(polyCoordinates) < 2:
                None
            else:
                cv.line(img,polyCoordinates[-2],(x,y),(0,0,255),thickness=2)    #Draws the lines between the points
        else:
            print("Stop, dont't overdo it. 20 Points are enough!!!")


cv.setMouseCallback(windowName,draw_circle)         #set mouse handler for specified wondow (windows Name,callback function for mouse event)


print("\n-------- Start Programm --------")
print("_________________________________")
print("|\t's' save picture\t|\n|\t'n' load new picture\t|\n|\t'q' exit program\t|\n|_______________________________|")


while(1):
    cv.imshow(windowName,img)                       #display an image in a new Window. Image shown in original size
    key = cv.waitKey(20) & 0xFF                     #waits for an key event (115=s) or an delay in millisecond (ms)
    #load picture
    if key == 110:
        img = loadNewPicture()
    #save image
    elif key == 115:                                  #save image
        if len(polyCoordinates) < 3:
            print("ERROR: You have to choose 3 Point, but only",len(polyCoordinates),"were given...")
        else:
            print("Image is cut out and saved...")
            cv.line(img,polyCoordinates[0],polyCoordinates[-1],(0,0,255),thickness=2)   #Draws the last stroke. Last point to first point

            mask = np.zeros(img.shape[:2], dtype='uint8')       #Blank Black Picture
            cv.fillPoly(mask, [polyCoordinates], (255,0,0))     #Fills the area bounded by one or more polygons (Image,PolygonArray,color)
            cutout = cv.bitwise_and(img,img,mask = mask)        #Return the cutout. Original Window size and position
            #cv.imshow('Rest', cutout)
            rect = cv.boundingRect(polyCoordinates)             #returns (x,y,w,h). Calculation of the new window size
            cropped = cutout[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]   #Crop the image to smaller image
            
            cv.imshow("Cropped Image" , cropped)
            
            rgba = cv.cvtColor(cropped, cv.COLOR_RGB2RGBA)     #Converts an image from one color space to another
            print("=> RGBA Picture-Data: ",rgba.shape)

            cv.imwrite(imgSave+str(ctr)+'.png',cropped)         #saves an image to a specified file(filename,image)
            
            polyCoordinates=np.array([[0,0]])                       #clears the array content
            polyCoordinates = np.delete(polyCoordinates,0,axis=0)   #workaround -> No Idea how to create an empty array

            ctr=ctr+1
    #program termination
    elif key == 113:                                
        print("\n-------- Programm is terminated --------\n")
        break    


cv.destroyAllWindows() 