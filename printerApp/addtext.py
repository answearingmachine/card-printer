# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import pandas as pd
import sys
import os

from datetime import date

import configparser
cfg = configparser.ConfigParser()

#print(os.path.dirname(__file__))

dir_path = dir_path = os.path.dirname(__file__)[:-10].replace("\\","/")

cfg.read(dir_path+"printerconfig.ini")

#print(cfg.sections())
#print(dir_path)

# kids do NOT ever learn from me
main_url = cfg.get("sheet.info","url_base")+cfg.get("sheet.info","SHEET_ID")
cards_url = main_url+cfg.get("sheet.info","url_extend")+cfg.get("sheet.info","cards_tab")
sigils_url = main_url+cfg.get("sheet.info","url_extend")+cfg.get("sheet.info","sigils_tab")
info_url = main_url+cfg.get("sheet.info","url_extend")+cfg.get("sheet.info","info_tab")

SDF = (pd.read_csv(sigils_url)).to_dict('split')
CDF = (pd.read_csv(cards_url)).to_dict('split')

COLUMN_NAME = cfg.getint("sheet.info","COLUMN_NAME")
COLUMN_TEMPLE = cfg.getint("sheet.info","COLUMN_TEMPLE")
COLUMN_TIER = cfg.getint("sheet.info","COLUMN_TIER")
COLUMN_COST = cfg.getint("sheet.info","COLUMN_COST")
COLUMN_POWER = cfg.getint("sheet.info","COLUMN_POWER")
COLUMN_HEALTH = cfg.getint("sheet.info","COLUMN_HEALTH")
COLUMN_SIGILS = cfg.getint("sheet.info","COLUMN_SIGILS")
COLUMN_TOKEN = cfg.getint("sheet.info","COLUMN_TOKEN")
COLUMN_TRAITS = cfg.getint("sheet.info","COLUMN_TRAITS")
COLUMN_TRIBES = cfg.getint("sheet.info","COLUMN_TRIBES")
COLUMN_FLAVOR = cfg.getint("sheet.info","COLUMN_FLAVOR")
COLUMN_CREDIT = cfg.getint("sheet.info","COLUMN_CREDIT")
COLUMN_UPDATED = cfg.getint("sheet.info","COLUMN_UPDATED")

# meta sigils (cells etc)
METASIGILS = []
for i in cfg.get("sigils","METASIGILS").split(","):
    METASIGILS.append(i)
#end for

# meta sigils 2
BOXSIGILS = []
for i in cfg.get("sigils","BOXSIGILS").split(","):
    BOXSIGILS.append(i)
#end for

TOKENSIGILS = []
for i in cfg.get("sigils","TOKENSIGILS").split(","):
    TOKENSIGILS.append(i)
#end for

HAPPYGEMS = []
for i in cfg.get("cost.thresholds","HAPPYGEMS").split(","):
    HAPPYGEMS.append(i)
#end for

COLORSIGILS = []
for i in cfg.get("sigils","COLORSIGILS").split(","):
    COLORSIGILS.append(i)
#end for

DECALTRAITS = []
for i in cfg.get("sigils","DECALTRAITS").split(","):
    DECALTRAITS.append(i)
#end for

# fonts
nameFont = ImageFont.truetype(dir_path+'assets/fonts/Poly-Regular.ttf', 63)
statFont = ImageFont.truetype(dir_path+'assets/fonts/Cambria.otf', 109)
textFont = ImageFont.truetype(dir_path+'assets/fonts/Cambria.otf', 33)
boldFont = ImageFont.truetype(dir_path+'assets/fonts/Cambria-Bold.ttf', 33)
italFont = ImageFont.truetype(dir_path+'assets/fonts/Cambria-Italic.ttf', 33)
artsFont = ImageFont.truetype(dir_path+'assets/fonts/Poly-Regular.ttf', 42)
formatFont = ImageFont.truetype(dir_path+'assets/fonts/Cambria.otf', 20)

# backup
"""
nameFont = ImageFont.truetype(dir_path+'assets/fonts/Poly-Regular.ttf', 63)
statFont = ImageFont.truetype(dir_path+'assets/fonts/Cambria.ttf', 109)
textFont = ImageFont.truetype(dir_path+'assets/fonts/Cambria.ttf', 33)
boldFont = ImageFont.truetype(dir_path+'assets/fonts/Cambria-Bold.ttf', 33)
italFont = ImageFont.truetype(dir_path+'assets/fonts/Cambria-Italic.ttf', 33)
artsFont = ImageFont.truetype(dir_path+'assets/fonts/Poly-Regular.ttf', 42)
formatFont = ImageFont.truetype(dir_path+'assets/fonts/Cambria.ttf', 20)
"""

def fetchSigilText(name,liveUpdate=False):
    #sdf = (pd.read_csv(sigils_url)).to_dict('split')
    if liveUpdate:
        sdf = (pd.read_csv(sigils_url)).to_dict('split')
    else:
        sdf = SDF
    #end if
    text = "Unknown sigil: "+str(name)
    found = False
    # Okay so I don't know about the data structures well enough
    # to do anything other than a really bad for loop
    for i in sdf["data"]:
        if i[0]==name:
            text = i[1]
            found = True
            break
        # end if
    # end for
    if not found:
        print("Unknown sigil: "+name)
    # end if
    return text
# end def

def fetchCardByName(name):
    #cdf = pd.read_csv(cards_url).to_dict('split')
    cdf = CDF
    found = False
    n=len(cdf["data"])
    idn = 0
    try:
        for i in range(n):
            if cdf["data"][i][int(COLUMN_NAME)].lower()==name.lower():
                idn = i
                found = True
                break
            # end if
        # end for
    except:
        print("Wacky error occurred! Is your sheet publicly viewable?")
    if not found:
        print("Failed to find card by name: "+name)
    # end if
    return idn
# end def

def printAllCards(start=-1,end=99999,mode=0,fmt=""):
    #cdf = (pd.read_csv(cards_url)).to_dict('split')

    if mode & 4: #live update mode
        cdf = (pd.read_csv(cards_url)).to_dict('split')
        livePreview = True
    else:
        cdf = CDF
        livePreview = False
    # end if

    lastPrintDateList = (pd.read_csv(info_url)).to_dict('split')["data"][2][0].split("/")
    lastPrintDate = date(int(lastPrintDateList[2][0:4]),int(lastPrintDateList[0]),int(lastPrintDateList[1]))

    sortOutput = (mode & 1)

    #end = min(len(cdf["data"]),end)
    counter = 0
    if end == 99999 and start != -1:
        # specifying one card
        cardRange = [start]
    else:
        cardRange = range(max(start,0),min(len(cdf["data"]),end+1))
    # end if
    for index in cardRange:
        card = cdf["data"][index]

        #print("Trying to print: "+str(card[COLUMN_NAME]))

        # rembered how to do binary flag checks :)
        if mode & 2:
            # see if this is already up to date, and ignore.

            try:
                cardDateList = card[COLUMN_UPDATED].split("/")
                cardDate = date(int(cardDateList[2][0:4]),int(cardDateList[0]),int(cardDateList[1]))
            except:
                print("weird date format")
                cardDate = date(1970,1,1)
            #end try

            if cardDate <= lastPrintDate:
                #print("LOL SKIP THIS ONE")
                continue
            #end if
        #end if

        cardInfo = {
            "name": str(card[COLUMN_NAME]),
            "temple": str(card[COLUMN_TEMPLE]),
            "tier": str(card[COLUMN_TIER]),
            "power": card[COLUMN_POWER],
            "health": card[COLUMN_HEALTH],
            "token": str(card[COLUMN_TOKEN]), # todo lol
            "flavor": str(card[COLUMN_FLAVOR]),

            "cost":   [],
            "sigils": [],
            "traits": [],
            "tribes": [],

            "artist": str(card[COLUMN_CREDIT]),
        }

        # Power and health
        # Not reading the X value??
        # redesign to ignore it
        if str(card[COLUMN_POWER]) == str(math.nan):
            #print("yeah there's no power here")
            cardInfo["power"] = 0
        # end if
        if str(card[COLUMN_HEALTH]) == str(math.nan):
            #print("yeah there's no health here")
            cardInfo["health"] = 0
        # end if

        # Cost (this will get complicated)
        rawCostString = str(card[COLUMN_COST]).lower()
        #print("cost: "+rawCostString)
        if rawCostString != "free" and not ("nan" in rawCostString):
            typeSplit = rawCostString.split("+")
            #print(typeSplit)
            for i in range(len(typeSplit)):
                typeSplit[i] = typeSplit[i].strip()
                typeSplit[i] = typeSplit[i].split(" ")
                # ruby mox fix...
                for j in range(len(typeSplit[i])):
                    if typeSplit[i][j] == "rubies":
                        typeSplit[i][j] = "ruby"
                    # end if
                # end for
                typeSplit[i][0] = int(typeSplit[i][0])
                if typeSplit[i][1] == "shattered":
                    typeSplit[i][1] += "_"+typeSplit[i][2]
                # end if
            # end for
            #print("SPLIT BY TYPE: "+str(typeSplit))
            cardInfo["cost"] = typeSplit
        # end if

        # Sigils - reworking now
        try:
            sigilsRaw = card[COLUMN_SIGILS].split(",")
            for i in sigilsRaw:
                i = i.strip()
                if i == "":
                    continue
                # end if
                try:
                    dumbString = i+"o"
                    cardInfo["sigils"].append(i)
                except TypeError:
                    #print("NOT A STRING")
                    integer = 1
                # end try
            # end for
        except AttributeError:
            #print("no sigils")
            integer = 1
        # end try


        # Traits
        try:
            traitsRaw = card[COLUMN_TRAITS].split(",")
            for i in traitsRaw:
                i = i.strip()
                if i == "":
                    continue
                # end if
                try:
                    dumbString = i+"o"
                    cardInfo["traits"].append(i)
                except TypeError:
                    integer = 1
                # end try
            # end for
        except AttributeError:
            integer = 1
        # end try

        # Tribes - probably fine
        try:
            dumbString = card[11]+"o"
            tribes = card[11].split(" ")
            for i in tribes:
                cardInfo["tribes"].append(i)
            # end for
        except TypeError:
            #print("NOT A STRING")
            integer = 1
        # end try
        
        #print(cardInfo)
        if sortOutput:
            TTSPath=cardInfo["temple"]+"/"+cardInfo["tier"]+"/"
            printCard(cardInfo,prefix=confirmDirectory(dir_path+"output/"+TTSPath),fmt=fmt,liveUpdate=livePreview)
        else:
            printCard(cardInfo,prefix=confirmDirectory(dir_path+"output/reprint/"),fmt=fmt,liveUpdate=livePreview)
        counter+=1
    # end for
    print("Done! Printed "+str(counter)+" cards.")
# end def

def printCard(info,savePath="output",show=False,prefix="01x 001 ",fmt="",liveUpdate=False):
    # A new card to inscrybe.
    img = Image.new("RGBA",(112,156))
    
    # The background colors.
    bgPath = dir_path+"/assets/bg/bg_"
    if info["tier"]=="Rare" or info["tier"]=="Talking":
        bgPath += "rare_"
    else:
        bgPath += "common_"
    # end if
    bgPath += info["temple"].lower()
    bgPath += ".png"

    try:
        bgImg = Image.open(bgPath)
    except FileNotFoundError:
        bgImg = Image.open(dir_path+"/assets/bg/zerror.png")
    img.paste(bgImg,(13,27))
    bgImg.close()

    # It needs a photo...
    try:
        artImg = Image.open(dir_path+"/assets/art/"+info["name"]+".png")
    except FileNotFoundError:
        print("could not find portrait: "+info["name"]+".png")
        artImg = Image.open(dir_path+"/assets/art/nothing lol.png")
    # end try
    img.paste(artImg,(13,27),artImg.convert("RGBA"))
    artImg.close()

    # And a proper frame to accompany it.
    framePath = dir_path+"/assets/frames/frame_"
    if info["tier"]=="Talking":
        framePath += "uncommon"
    elif info["tier"]=="Side Deck":
        framePath += "common"
    else:
        framePath += info["tier"].lower()
    # end if
    framePath += "_"
    framePath += info["temple"].lower()
    framePath += ".png"
    try:
        frameImg = Image.open(framePath)
    except FileNotFoundError:
        frameImg = Image.open(dir_path+"/assets/frames/zerror.png")
    img.paste(frameImg,(0,0),frameImg.convert("RGBA"))
    frameImg.close()

    # Without having met the other text functions, this color sample is meaningless.
    # Pay it no mind for now.
    colorSample = img.getpixel((66,18))

    # Let us begin to inscrybe it.
    I0 = ImageDraw.Draw(img)

    # First, the card's cost.
    costx = 99
    costy = 14
    costn = len(info["cost"])
    for ii in range(costn):
        i = info["cost"][ii] # i made it too lazy first time so this lets me
                             # have ii as a numeric index still
        string = i[1]
        try:
            costImg = Image.open(dir_path+"/assets/cost/"+string+".png")
        except FileNotFoundError:
            try:
                string = string[:-1]
                costImg = Image.open(dir_path+"/assets/cost/"+string+".png")
            except:
                print("Unknown cost: "+string)
                costImg = Image.open(dir_path+"/assets/cost/zerror.png")
            # end try
        # end try
        w = costImg.getbbox()[2]
        h = costImg.getbbox()[3]

        try:
            threshold = cfg.getint("cost.thresholds",string)
        except:
            print("didn't find cost limits for "+string)
            threshold = 2
        #end try
            
        # just a few
        if i[0] < threshold:
            for j in range(i[0]):
                img.paste(costImg,
                          ((costx-(w-1)),costy-(h//2-4)),
                          costImg.convert("RGBA")
                          )
                costx -= (w-1)
            costx -= 2
        else:
            # many
            numberString = str(i[0])
            img.paste(costImg,
                      ((costx-(w-1)),costy-(h//2-4)),
                      costImg.convert("RGBA")
                      )
            costx -= ((w-1)+6)
            alphaPaste(img,costx,costy+1,dir_path+"assets/cost/x.png")
            costx-=6
            for j in range(len(numberString)):
                chrj = numberString[-j-1]
                symbolString = dir_path+"assets/cost/"+chrj+".png"
                alphaPaste(img,costx,costy,symbolString)
                costx -= 6
            # end for
            costx += (w-4)
        # end if
        costImg.close()

        # I don't remember where I put the separator
        # so im just gonna do it backwards lol
        # this is to put mox gems together btw
        if costn > 1 and ii < costn-1:
            string2 = info["cost"][ii+1][1]
            #print(string2)
            if string in HAPPYGEMS and string2 in HAPPYGEMS:
                costx += 2
            #end if
        #end if
    # end for

    # Scale it up to fit.
    img = img.resize((1120,1560),resample=Image.Dither.NONE)
    I1 = ImageDraw.Draw(img)
    
    # Next, the power and health. The numbers.
    # variable stat checker
    #print(info["traits"])
    normalPower = True
    if info["traits"] != []:
        for i in info["traits"]:
            if "Power" in i:
                normalPower = False
                try:
                    alphaPaste(img,144,1351,dir_path+"assets/variable/"+i.strip()+".png")
                except FileNotFoundError:
                    print("unknown variable power: "+i)
                    normalPower = True
                # end try
            # end if
        # end for
    # end if
    if normalPower:
        shadowText(I1,148,1331,str(int(info["power"])),statFont,anchor="la")
    # end if
    
    shadowText(I1,968,1331,str(int(info["health"])),statFont,anchor="ra")

    # Next, we will add the sigils.
    sigilx = 150
    sigily = 920

    # check to see if we need any of the special overlays (currently conduits and mox)

    gem = False
    if "Mox" in info["tribes"]:
        gem = "!"
        if "Orange Gem" in info["sigils"] or "Blue Gem" in info["sigils"] or "Green Gem" in info["sigils"]:
            if "Orange Gem" in info["sigils"]:
                gem += "O"
            # end if
            if "Blue Gem" in info["sigils"]:
                gem += "B"
            # end if
            if "Green Gem" in info["sigils"]:
                gem += "G"
            # end if
        elif "Magnificent Gem" in info["sigils"]:
            gem += "OBG"
        elif "Prism Gem" in info["sigils"]:
            gem = "P"
        elif "Gem Shard" in info["sigils"]:
            gem = "S"
        # end if
    # end if

    conduit = False
    """
    for isig in info["sigils"]:
        if "Conduit" in isig: # this might get reworked
            conduit = True
        # end if
    # end for
    """
    if "Conduit" in info["tribes"]:
        conduit = True
    # end if

    # draw
    
    if conduit and gem:
        alphaPaste(img,50,840,dir_path+"assets/misc/gems/gemconduit.png")
        if gem=="!":
            gem=""
        # end if

        # this is a terrible way to fix this
        if "Orange Conduit" in info["sigils"]:
            gem += "O"
        # end if
        if "Blue Conduit" in info["sigils"]:
            gem += "B"
        # end if
        if "Green Conduit" in info["sigils"]:
            gem += "G"
        # end if
        if "Prism Conduit" in info["sigils"]:
            gem += "P"
        elif gem == "":
            gem = "S"
        # end if
        gemImg = dir_path+"assets/misc/gems/gem"+gem+".png"
        alphaPaste(img,530,850,gemImg)
    elif gem:
        if gem == "P":
            alphaPaste(img,40,840,dir_path+"assets/misc/gems/moxband_prism.png")
        elif gem == "S":
            alphaPaste(img,40,840,dir_path+"assets/misc/gems/moxband_shard.png")
        else:
            alphaPaste(img,40,840,dir_path+"assets/misc/gems/moxband_3empty.png")
            if "O" in gem:
                alphaPaste(img,440,850,dir_path+"assets/misc/gems/gemO.png")
            # end if
            if "B" in gem:
                alphaPaste(img,530,850,dir_path+"assets/misc/gems/gemB.png")
            # end if
            if "G" in gem:
                alphaPaste(img,610,850,dir_path+"assets/misc/gems/gemG.png")
            # end if
        # end if
    elif conduit:
        alphaPaste(img,50,850,dir_path+"assets/misc/conduit_large.png")
    # end if

    nsig = len(info["sigils"])
    # see
    # python's thing where you can just make a for loop go through something without ever making a numerical iterator is really convenient, but ever more it seems like I always inevitably end up having to go back and make one anyway.
    specialSigil = False
    dontPutTheExtraLineThere = False
    for isign in range(nsig):
        isig = info["sigils"][isign]
        #print(isig)
        # see if this is a wacky meta sigil like cell or latcher
        if isig in METASIGILS:
            if isig != "INFOBOX":
                alphaPaste(img,0,sigily,dir_path+"assets/misc/"+isig+".png")
                sigily+=120
            # end if

            # special dark box for latch sigils
            if isig in BOXSIGILS: # some day replace this with a proper check for if we add more like this
                if isign == nsig-1:
                    print("Malformed card! You put a conditional with no sigils after it!")
                    # technically as it stands you can do this anyways with the other conditionals and there's no errors
                    # but i need an error handler lol
                    print("("+info["name"]+")")
                    continue
                #end if

                nextSigilLines = len(fetchSigilText(info["sigils"][isign+1],liveUpdate).split("\n")) # if i ever get auto line breaks this part will get fucked so uh dont let me forget
                #print("latching: "+info["sigils"][isign+1]+" ("+str(nextSigilLines)+" lines)")
                if nextSigilLines==1:
                    nextSigilLines=2 # need room at least for the icon
                #end if

                darkBox = Image.open(dir_path+"/assets/misc/META_DARKBOX.png")
                cropHeight = (nextSigilLines*35)+30
                if cropHeight%10==5:
                    cropHeight+=5
                #end if
                darkBoxC = darkBox.crop((0,0,1120,cropHeight))
                img.paste(darkBoxC,(0,sigily),darkBoxC.convert("RGBA"))
                darkBox.close()
                darkBoxEnd = Image.open(dir_path+"/assets/misc/META_DARKBOX_END.png")
                img.paste(darkBoxEnd,(0,sigily+cropHeight-10),darkBoxEnd.convert("RGBA"))

                sigily+=(20)
                specialSigil = True

            #end if
            continue
        #end if
        
        if specialSigil:
            if isig in COLORSIGILS:
                try:
                    sigilImg = recolorImage(Image.open(dir_path+"/assets/sigils/"+isig+"_outline.png"),(255,255,255))
                except FileNotFoundError:
                    sigilImg = recolorImage(Image.open(dir_path+"/assets/sigils/"+isig+".png"),(255,255,255))
                    print("No outline variant for sigil: "+isig)
                except FileNotFoundError:
                    sigilImg = recolorImage(Image.open(dir_path+"/assets/sigils/zerror.png"),(255,255,255))
                    print("No icon for sigil: "+isig)
                #end try
            else:
                try:
                    sigilImg = recolorImage(Image.open(dir_path+"/assets/sigils/"+isig+".png"),(255,255,255))
                except FileNotFoundError:
                    sigilImg = recolorImage(Image.open(dir_path+"/assets/sigils/zerror.png"),(255,255,255))
                    print("No icon for sigil: "+isig)
                #end try
            #end if
        else:
            # fetch icon and paste
            try:
                sigilImg = Image.open(dir_path+"/assets/sigils/"+isig+".png")
            except FileNotFoundError:
                sigilImg = Image.open(dir_path+"/assets/sigils/zerror.png")
                print("No icon for sigil: "+isig)
            #end try
        #end if

        img.paste(sigilImg,(sigilx,sigily),sigilImg.convert("RGBA"))
        sigilImg.close()

        # write name
        text = fetchSigilText(isig,liveUpdate)
        if isig in TOKENSIGILS:
            try:
                halves = text.split("(new card)")
                text = halves[0]+'\"'+info["token"]+'\"'+halves[1]
            except IndexError:
                text = "missingno"
                print("Improper token slecification on sigil: "+isig)
        # end if
        try:
            textLines = text.split("\n")
        
            n = len(textLines)
            if n == 1:
                textOffset = 15
                singleLine = True
            else:
                textOffset = -5
                singleLine = False
        except AttributeError:
            textOffset = 15
            singleLine = True
            textLines = ["missingno"]
            
        if specialSigil:
            textColor = (255,255,255)
        else:
            textColor = (0,0,0)
        #end if

        # print name
        l = I1.textlength(isig+": ",boldFont)
        I1.text((sigilx+80, sigily+textOffset),
                isig+": ",
                fill=textColor,
                font=boldFont,
                anchor="la"
                )

        # print first line of sigil text
        # (might be the only line)
        I1.text((sigilx+80+l, sigily+textOffset),
                textLines[0],
                fill=textColor,
                font=textFont,
                anchor="la"
                )
        # and now the rest of them
        if singleLine == False:
            # skip the first one
            for i in range(n)[1:]:
                I1.text((sigilx+80, sigily+textOffset+40*i),
                textLines[i],
                fill=textColor,
                font=textFont,
                anchor="la"
                )
            sigily += (n-2)*40     
        sigily += 80
        # TODO: figure out inline italics for tribe names

        if specialSigil:
            specialSigil = False
            dontPutTheExtraLineThere = True
            sigily+=10
        #end if
    # end for

    if info["sigils"] != [] and not dontPutTheExtraLineThere:
        alphaPaste(img,150,sigily-(sigily%10),dir_path+"/assets/misc/Separator_large.png")
        sigily += 10
    # end if

    # Do let me know of any traits this card might have.
    hasTraits = False
    for itrait in info["traits"]:
        if itrait in DECALTRAITS:
            #print("oh shit its a fake one")
            alphaPaste(img,0,0,dir_path+"/assets/misc/"+itrait+".png")
            continue
        # end if
        hasTraits = True
        textLines = fetchSigilText(itrait,liveUpdate).split("\n")
        n = len(textLines)

        for i in textLines:
            I1.text((sigilx,sigily),
            i,
            fill=(0,0,0),
            font=textFont,
            anchor="la"
            )
            sigily += 35
        sigily += 5
    # end for
    if hasTraits:
        sigily = (math.ceil(sigily/10))*10
        alphaPaste(img,150,sigily,dir_path+"/assets/misc/Separator_large.png")
        sigily += 10
    # end if
    
    # Now we shall say which tribes it belongs to.
    #151,1296
    tribeString = info["tier"]+" "+info["temple"]
    if info["tribes"] != []:
        tribeString+=" -"
        for i in info["tribes"]:
            tribeString += " "+i
        # end for
    # end if
    I1.text((151,1295),
            tribeString,
            fill=colorSample,
            font=textFont,
            anchor="la"
            )

    # At last, grace it with a description. Something for flavor.
    if info["flavor"] != "BLANK":
        #ftext = info["flavor"]
        #print(italFont.getlength(ftext))
        
        I1.text((561,sigily),
                info["flavor"],
                fill=(0,0,0),
                font=italFont,
                anchor="ma"
                )
    #end if

    # Name the card.
    shadowText(I1,136,136,info["name"],nameFont)

    # Please, sign your work.
    artistName = info["artist"]
    if artistName != "nan":
        dumbString = artistName + "o"
        shadowText(I1,560,1375,"Illus. "+artistName,artsFont,anchor="ma")
    else:
        print("no artist credit found for "+info["name"])

    # Do not let us forget what this is for in the end.
    if fmt != "":
        #print(fmt)
        tx = cfg.getint("text.format","GAMEFORMAT_X")
        ty = cfg.getint("text.format","GAMEFORMAT_Y")
        I1.text((tx,ty),fmt,fill=colorSample,font=formatFont,anchor="ma")
    #end if
        
    # uhhh yeah
    if show:
        img.show()
    # end if
    if info["name"]!="nan":
        filePath = prefix+info["name"]+".png"
        img.save(filePath)
    # end if

# end def

def shadowText(image,x,y,text,font,anchor="la"):
    # maximum laziness
    image.text((x+5,y+5), text, fill=(0,0,0), font=font, anchor=anchor)
    image.text((x,y), text, fill=(255,255,255), font=font, anchor=anchor)
# end def

def alphaPaste(image,x,y,path):
    paste = Image.open(path)
    image.paste(paste,(x,y),paste.convert("RGBA"))
    paste.close()
# end def

# I think this is just unfinished lol
def textlines_even(font,text,maxw):
    words = text.strip().split(" ")
    n = len(words)
    for i in range(n):
        print("TODO LOL")
    #end for
#end def

def confirmDirectory(path):
    if os.path.exists(path):
        return path
    else:
        os.makedirs(path)
        return path
    #end if
#end def

def recolorImage(img,color):
    img = img.convert("RGBA")
    w,h = img.size
    nr,ng,nb = color
    for y in range(h):
        for x in range(w):
            r,g,b,a = img.getpixel((x,y))
            img.putpixel((x,y),(nr,ng,nb,a))
        #end for
    #end for
    return img
#end def

#end def
    
def main():
    while True:
        gameFormatString = cfg.get("sheet.info","FORMAT_NAME") +" - "+ str(date.today())
        a = input("print cards\n[start],[end]\n").split(",")
        n = len(a)

        if n>0:
            # I hate dynamic typing I hate dynamic typing
            if type(a[0]) == type("aa"):
                s = fetchCardByName(a[0])
            elif type(a[0]) == type(2):
                s = int(s)
            #end if

            if n>1:
                try:
                    e = int(a[1])-2
                except ValueError:
                    # again try name
                    e = fetchCardByName(a[1])
                # end try
            # end if
        # end if
        
        if n == 0:
            # print all
            printAllCards()
        elif n == 1:
            # print one
            printAllCards(start=s,fmt=gameFormatString)
        elif n == 2:
            # print range
            printAllCards(start=s,end=e,fmt=gameFormatString)
        elif n == 3:
            printAllCards(start=s,end=e,mode=int(a[2]),fmt=gameFormatString)
        else:
            print("too many arguments what")
        # end if
    # end while
# end def
main()