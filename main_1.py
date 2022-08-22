
#Reference:
    #This code is a modification of the Anshul Sachdev in this below link: 
    #https://medium.com/acmvit/how-to-project-an-image-in-perspective-view-of-a-background-image-opencv-python-d101bdf966bc

import cv2
import matplotlib.pyplot as plt
import numpy as np

posit=[] 
posit2=[]
c=0
# After selecting positions, please use ESC key to close the windows 
def draw_circle(event,x,y,flags,param):
    global posit,c
    if event == cv2.EVENT_LBUTTONUP:
        cv2.circle(billboard,(x,y),3,(0,0,255),-1)
        posit.append([x,y])
        if(c!=3):
            posit2.append([x,y])
        elif(c==3):
            posit2.insert(2,[x,y])
        c+=1      
#import Highway image 
billboard = cv2.imread('Highway billboard.jpg')
#import oil painting image 
oil = cv2.imread('Oil painting.jpg')
img=oil
#choose coordinates of oil paintig before transformation 
pts=np.array([[635, 151], [610, 1131], [1368, 984],[1374, 386]])
x,y,w,h = cv2.boundingRect(pts)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image',draw_circle)

while(True):
    cv2.imshow('image',billboard)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
height, width = billboard.shape[:2]

pts1=np.float32([[635, 151], [1374, 386], [610, 1131], [1368, 984]])
pts2=np.float32(posit)
h, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC,5.0)
height, width, ch = billboard.shape
Persp = cv2.warpPerspective(oil, h, (width, height))
mask1 = np.zeros(billboard.shape, dtype=np.uint8)
cv2.fillConvexPoly(mask1, np.int32(posit2), (255,)*(billboard.shape[2]))
Persp = cv2.bitwise_and(Persp, mask1)
mask1= cv2.bitwise_not(mask1)
maskedimage = cv2.bitwise_and(billboard, mask1)
plt.imshow(mask1)
plt.imshow(maskedimage)
plt.imshow(Persp)
finalimage = cv2.bitwise_or(Persp, maskedimage)
plt.imshow(finalimage)
plt.imshow(billboard)
cv2.imwrite('finalimage.png',finalimage)