from PIL import Image
from PIL import ImageDraw
import sys
import os
import math

PALETTENAME = "palette_energyconvert.png"

THRESHOLD = 5.0

paletteImg = Image.open(PALETTENAME).convert("RGBA")
w,h = paletteImg.size
if h!=2:
    error("palette image was supposed to be 2 pixels high")
#end if

n = w
    
oldPalette = []
newPalette = []
for i in range(w):
    oldPalette.append(paletteImg.getpixel((i,0)))
#end for
for i in range(w):
    newPalette.append(paletteImg.getpixel((i,1)))
#end for

paletteImg.close()

oldSprites = os.listdir("old")
for f in oldSprites:
    print(f)
    Img = Image.open("old/"+f).convert("RGBA")

    w,h = Img.size

    for y in range(h):
        for x in range(w):
            p = Img.getpixel((x,y))
            # i wonder how inefficient this is
            for i in range(n):
                if math.dist(p,oldPalette[i]) < THRESHOLD:
                    p = newPalette[i]
                    Img.putpixel((x,y),p)
                #end if
            #end for
        #end for
    #end for
    #Img.show()
    Img.save("new/"+f)
    Img.close()
#end for
    

    
