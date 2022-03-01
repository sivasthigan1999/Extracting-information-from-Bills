import cv2
import pytesseract
import re
import numpy as np
import json
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
img=cv2.imread('bill.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
img=cv2.threshold(img, 150, 350, cv2.THRESH_BINARY)


img1 = cv2.bitwise_not(img[1])
kernel = np.ones((2,1), np.uint8)
img1 = cv2.dilate(img1, kernel, iterations=1)
img1 = cv2.bitwise_not(img1)



img = img1[107:1011, 140:556]
img=cv2.resize(img,(550,950))
imageH,imageW=img.shape
boxes = pytesseract.image_to_data(img)
istr=pytesseract.image_to_string(img)
for a,b in enumerate(boxes.splitlines()):
         #print(b)
         if a!=0:
             b = b.split()
             if len(b)==12:
                 x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                 cv2.putText(img,b[11],(x,y-3),cv2.FONT_HERSHEY_SIMPLEX,0.3,(50,50,255),1)
                 cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 1)
print(istr)
cv2.imshow('img', img )
cv2.waitKey(0)