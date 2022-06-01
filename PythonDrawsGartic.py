#Gartic Screen size : ~1900 * 1000
#Small pencil click size : ~4*4 pixels
#So we'll resize to at best 500*250
#
#Steps :
#1. Get image we want to draw (to the right scale)
#   1.1. Get reference image on disk
#   1.2. Resize it in memory (roughly) to the Gartic Area
#
#2. Make it into maps of different gartic colors
#   2.1. Define the colors that can be used by Gartic in a map
#   2.2. For each pixel, calculate the distance from each possible color. Put it in a coordinateMap corresponding to this color.
#
#3. Draw it on the screen
#   3.1. For each color map, pick the color in gartic (moving and clicking)
#   3.2. Put each pixel, one by one, by clicking, waiting a bit, releasing, then moving to the next
#
#
# Added functionalities :
#-Flags changed on keypress (pause, restart,...)
#-Possibility to change the reference image "on the fly" (by changing it in the directory probably, or an increment in a list with like temp1.png, temp2.png...)

#Notes :
# https://www.thepythoncode.com/article/control-mouse-python
#   Upper-left corner coordinates : 1200,600
#   Lower-right coordinates : 3120,1670
#   Middle of Black color : 900,800
#   Middle of dark grey : 985,800
#   Middle of white color : 900,900
#
#   Conclusions :
#       Canvas size : 2000*1050
#       left color offset : 85px
#       Down color offset : 100px
#
#
#
#   Since with the lowest pencil size there is still too much pixels/drawing is too slow, we'll divide again, using the 2nd size of pencil (circle of 16px of radius)

import mouse
import cv2
import pyautogui
import time

pyautogui.PAUSE = 0

def getIndexFromClosestColor(p_pixel):
    currentIndex = 0;
    closestIndex = -1;
    closestDistance = 256*3;
    for val in garticColors:
        distance = abs(p_pixel[0]-val[0])+abs(p_pixel[1]-val[1])+abs(p_pixel[2]-val[2]);
        if (distance < closestDistance):
            closestDistance = distance;
            closestIndex = currentIndex;
        currentIndex+=1;

    return closestIndex;


#Mouve mose to firstColorX+(z%3)*decalageXentre2Couleurs ; firstColorY+ (z/3)*decalageYentre2Couleurs
def moveToColorIndex(p_index):
    l_indexX = p_index%3
    l_indexY = int(p_index/3)
    pyautogui.moveTo(900 + (85 * l_indexX) ,800 + (100 * l_indexY))

    return True


#Getting the image, resizing it so it can be appropriately used for gartic
img = cv2.imread('./Utility_Debug.png');
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
rescaledSize = (125,63);
resized = cv2.resize(img, rescaledSize, interpolation = cv2.INTER_AREA);

cv2.imshow('Resized',resized);
cv2.waitKey(1);



garticColors = {
    (0,0,0),                  #Black              0
    (102,102,102),            #DarkGray           1
    (0,80,205),               #DarkBlue           2
    (255,255,255),            #White              3
    (170,170,170),            #LightGray          4
    (38,201,255),             #LightBlue          5
    (1,116,32),               #DarkGreen          6
    (153,0,0),                #DarkRed            7
    (150,65,18),              #DarkBrown          8
    (17,176,60),              #LightGreen         9
    (255,0,19),               #LightRed           10
    (255,120,41),             #Orange             11
    (176,112,28),             #LightBrown         12
    (153,0,78),               #Magenta/DarkPurple 13
    (203,90,87),              #DarkBeige          14
    (255,193,38),             #Yellow             15
    (255,0,143),              #Pink               16
    (254,175,168)             #Beige              17
}

#Initialize the list of lists
list_of_coordinates = []
for i in range (0,len(garticColors)):
    list_of_coordinates.append([]);

#print(len(garticColors));
print("Went past")

for i in range (0,62):
    for j in range (0,124):
        pixelMapIndex = getIndexFromClosestColor(resized[i,j]);
        #print(j,i)
        list_of_coordinates[pixelMapIndex].append((i,j))
        #print(j,i)
        #print(pixelMapIndex);
        #print(img[j,i][0]);

pyautogui.moveTo(1200,650)
pyautogui.click()

print("Mapped")

for z in range (0,len(garticColors)):
    print("######################")
    print(z)
    print("######################")


    #Move mouse to correct color on screen
    moveToColorIndex(z)
    pyautogui.click()

    #Waiting a bit after each color change just to be sure not to drag the color on the whole screen
    time.sleep(0.1)
    for val in list_of_coordinates[z]:
        xToPrint = 1200 + (val[0] * 16)
        yToPrint = 600 + (val[1] * 16)
        #print(str(xToPrint)+";"+str(yToPrint))
        if (xToPrint >= 1200 and xToPrint <= 3120 and yToPrint >= 600 and yToPrint <= 1650):
            pyautogui.moveTo(xToPrint ,yToPrint)
            pyautogui.click()
            time.sleep(0.00002)
        #print(str(val[1])+";"+str(val[0]));
        #move mouse to *basePositionX*+val[0]*4 ; *basePositionY*+val[1]*4
        #click, wait a little, release

cv2.destroyAllWindows();
