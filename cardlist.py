import math
import pandas as pd
import sys

from printer_config import *

AMTS = {
    "Side Deck" : "3",
    "Common" : "3",
    "Uncommon" : "1",
    "Rare" : "1",
    "Talking" : "1"
}

def fetchCardByName(name):
    # I am a piece of garbage (sung in G blues scale)
    #print(pd.read_csv(cards_url))
    
    cdf = pd.read_csv(cards_url).to_dict('split')
    found = False
    n=len(cdf["data"])
    idn = 0
    try:
        for i in range(n):
            if cdf["data"][i][COLUMNS["name"]].lower()==name.lower():
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

def printCardList():
    cdf = pd.read_csv(cards_url).to_dict('split')
    n=len(cdf["data"])

    outputString = ""
    currentTemple = ""
    currentTier = ""
    for i in range(n):
        thisCard = cdf["data"][i]
        temple = thisCard[COLUMNS["temple"]]
        tier = thisCard[COLUMNS["tier"]]
        
        if thisCard[COLUMNS["temple"]] != currentTemple:
            outputString += "## "+temple+"\n"
            currentTemple = temple
        #end if
        if thisCard[COLUMNS["tier"]] != currentTier:
            outputString += "### "+tier+"\n"
            currentTier = tier
        #end if
        outputString += thisCard[COLUMNS["name"]]+" - "
        outputString += AMTS[tier]+"\n"
    #end for

    file = open("cardlist.txt","w")
    file.write(outputString)
    file.write("hjdkfhjksd")
    file.close()

printCardList()

