#Gartic Screen size : ~1900 * 1000
#Small pencil click size : ~4*4 pixels
#So we'll resize to at best 475*250
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
#   Upper-left corner coordinates : 801,405
#   Lower-right coordinates : 2070,1109
#   Middle of Black color : 595,530
#   Middle of dark grey : 655,530
#   Middle of white color : 595,600
#
#   Conclusions :
#       Canvas size : 1200*700
#       left color offset : 60px
#       Down color offset : 70px
#

import mouse
import cv2

def getIndexFromClosestColor(pixel):
    currentIndex = 0;
    closestIndex = -1;
    closestDistance = 256*3;
    for val in garticColors:
        distance = abs(pixel[0]-val[0])+abs(pixel[1]-val[1])+abs(pixel[2]-val[2]);
        if (distance < closestDistance):
            closestDistance = distance;
            closestIndex = currentIndex;
        currentIndex+=1;

    return closestIndex;


#Getting the image, resizing it so it can be appropriately used for gartic
img = cv2.imread('./semiramis_wp.jpg', cv2.IMREAD_COLOR);
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
rescaledSize = (475,250);
resized = cv2.resize(img, rescaledSize, interpolation = cv2.INTER_AREA);

#cv2.imshow('Resized',resized);

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

for i in range (0,250):
    for j in range (0,1):
        pixelMapIndex = getIndexFromClosestColor(img[j,i]);
        #print(j,i)
        list_of_coordinates[pixelMapIndex].append((j,i))
        #print(j,i)
        #print(pixelMapIndex);
        #print(img[j,i][0]);


for z in range (0,len(garticColors)):
    print("######################")
    print(z)
    print("######################")
    #Move mouse to correct color on screen
    #Mouve mose to firstColorX+(z%3)*decalageXentre2Couleurs ; firstColorY+ (z/3)*decalageYentre2Couleurs
    #click, wait a little, release
    #wait a little bit of time
    for val in list_of_coordinates[z]:
        print(val[1]);
        #move mouse to *basePositionX*+val[0]*4 ; *basePositionY*+val[1]*4
        #click, wait a little, release

cv2.waitKey(0);
cv2.destroyAllWindows();
