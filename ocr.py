import cv2
import pytesseract
import re
import numpy as np
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
img=cv2.imread('bill.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img = img[107:1011, 140:556]
img=cv2.resize(img,(450,700))
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
kernel = np.ones((1, 1), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)
cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
print(img.shape)
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


searchObj = re.split("\n",istr)


items=[]

for i in searchObj:
  x=re.search(r"[A-Z] [0-9]{1,5}[.,][0-9]{2}$",i)                 # x=re.search(r"[A-Z] [0-9]{1,5}[.,][0-9]{2}$",i)
  if(x):
    rest_i = i.split(' ', 1)[1]
    items.append(rest_i)

print(items)
#print(text)
print(istr)
cv2.imshow('img', img)
cv2.waitKey(0)