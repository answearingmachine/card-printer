# this is technically another script file, but all it does is
# set a bunch of constant values for the other to reference.
# You can edit them here.


# the middle part of the google docs url.
#SHEET_ID = "1tvTXSsFDK5xAVALQPdDPJOitBufJE6UB_MN4q5nbLXk"
SHEET_ID = "1tvTXSsFDK5xAVALQPdDPJOitBufJE6UB_MN4q5nbLXk"

# Unused.
SHEET_NAME = "CARDSHEET"

# the first part of the google docs url.
url_base = f"https://docs.google.com/spreadsheets/d/"

# ignore this; used for some internal modules
url_base += SHEET_ID+"/gviz/tq?tqx=out:csv&sheet="

# The name of the bottom tab with the sigils.
sigils_url = url_base+"Sigils"

# The name of the bottom tab with the cards.
cards_url = url_base+"Cards"

# min # of cost to show as number instead of draw.
# e.g., since bones is 5, a 4 bone cost is drawn as IIII,
# while a 5 bone cost is drawn as 5xI.
# configurable per cost, and for custom costs.
COSTTHRESH = {
    "blood": 5,
    "bone": 5,
    "energy": 13,

    "shattered garnet": 4,
    "shattered ruby": 4,
    "shattered topaz": 4,
    "shattered emerald": 4,
    "shattered sapphire": 4,
    "shattered amethyst": 4,
    
    "garnet": 4,
    "ruby": 4,
    "topaz": 4,
    "emerald": 4,
    "sapphire": 4,
    "amethyst": 4,
    
    "clowny": 1,
    "nuclear": 1,
    "malware": 1,
    "pure": 1,

    "valor": 1,

    "teeth": 4
}
# 1 means it will always use 1xR

# Sigils that need to reference another card by name.
TOKENSIGILS = ["Fledgling","Frozen Away","Creeping Outwards","Loose Tail"]

#SIGILCOLUMNS = [6,7,8] # list of column indicies that have sigils (0-indexed)
# probably don't touch these because I think I left the other ones hardcoded lol

COLUMNS = {
    "name": 0,
    "temple": 1,
    "tier": 2,
    "cost": 3,
    "power": 4,
    "health": 5,
    "sigils": 6,

    "token": 9,
    "traits": 10,
    "tribes": 11,
    "flavor": 12,
    "illus_credit": 14   
}