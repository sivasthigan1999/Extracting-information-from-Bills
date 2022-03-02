import cv2
import pytesseract
import re
import numpy as np
import json

### Image preprocessing
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

         if a!=0:
             b = b.split()
             if len(b)==12:
                 x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                 cv2.putText(img,b[11],(x,y-3),cv2.FONT_HERSHEY_SIMPLEX,0.3,(50,50,255),1)
                 cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 1)


texts = re.split("[\n]",istr)

items=[]
items1=[]
items2=[]
items3=[]
items4=[]
items5=[]
items6=[]
items7=[]
items8=[]
dict1={}

## Regex is used to find patterns
for i in texts:
  x=re.search(r"[A-Z 0-9] [A-Za-z|]+ [0-9]{1,3}[.,][0-9]{1}",i) ## for items
  y=re.search(r"[a-z]: [A-Z]",i) ## for table
  z = re.search(r"[a-z] \+: [A-Z]", i) ## for Staff
  w = re.search(r"[0-9]+:[0-9]+", i)  ## for date and time
  v = re.search(r"[a-z]. [0-9]{4}.[0-9]{2}", i)  ## for Total and subtotal
  u = re.search(r"-[0-9]+.[.][0-9]+", i) ## for MPM values
  t = re.search(r"% [A-Z]+.[A-Z]", i) ## for % values
  s = re.search(r"[a-z]\/", i)## for Tax


  # Items
  if(x):
    detectx = i.split(' ', 1)[1]
    items.append(detectx)

  # Table
  if(y):
     detecty=i.split(' ')
     items2.append(detecty)

  # Staff
  if(z):
     detectz=i.split(' ')
     items3.append(detectz)

  # Date and Time
  if(w):
     detectw=i.split(' ')
     items4.append(detectw)

  # Total and subtotal
  if (v):
      detectv = i.split(' ')
      items5.append(detectv)

  # MPM values
  if (u):
      detectv = i.split(' ')
      items6.append(detectv)

  # % Values
  if (t):
      detectt = i.split(' ')
      items7.append(detectt)

  # Tax
  if (s):
      detects = i.split(' ')
      items8.append(detects)

###for ITEMS


for j in items:
     match = re.split(r"(\d+.\d+)",j)
     match1 = list(filter(lambda x: x!='', match))
     items1.append(match1)




for value in items1:
    v = {value[0]: value[1]}
    dict1.update(v)

#print(dict1)


#staff
del items3[0][1]
#print(items3)


##date and time
del items4[0][1]
del items4[0][-2]
#print(items4)

##  Total and subtotal
#print(items5)

##MPM Values
MPMBey=items6[0][0]+items6[0][1]+items6[0][2]+items6[0][3]
MPMDining=items6[1][0]+items6[1][1]+items6[1][2]
#print(items6)

#% Values
#print(items7)

#Tax
#print(items8)


output={items2[0][0]:items2[0][1], items3[0][0]:items3[0][1],items4[0][0]:items4[0][1]+' '+items4[0][2],items4[0][-2]:items4[0][-1],'Consumed items':[dict1], MPMBey: items6[0][-1],MPMDining:items6[1][-1],items5[0][0]:items5[0][1],items5[1][0]:items5[1][1],items7[0][0]+items7[0][1]:items7[0][2],items7[1][0]+items7[1][1]:items7[1][2],items8[0][0]+items8[0][1]:items8[0][2],'Total':items5[2][2]}
print(output)

json_string = json.dumps(output)
with open('output_data.json', 'w') as outfile:
    outfile.write(json_string)


cv2.imshow('img', img )
cv2.waitKey(0)