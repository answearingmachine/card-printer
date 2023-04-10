from PIL import Image
from PIL import ImageDraw
import sys
import os

COLOR = (0, 192, 255) # mess with this idk what you want it to be

oldSprites = os.listdir("old")
for f in oldSprites:
    print(f)
    Img = Image.open("old/"+f).convert("RGBA")

    w,h = Img.size

    for y in range(h):
        for x in range(w):
            r,g,b,a = Img.getpixel((x,y))
            Img.putpixel((x,y),(COLOR+(a,)))
        #end for
    #end for
    #Img.show()
    Img.save("new/"+f)
#end for
    

    
