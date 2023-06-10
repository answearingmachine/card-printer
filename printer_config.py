# this is technically another script file, but all it does is
# set a bunch of constant values for the other to reference.
# You can edit them here.


# the middle part of the google docs url.
#SHEET_ID = "1tvTXSsFDK5xAVALQPdDPJOitBufJE6UB_MN4q5nbLXk"
SHEET_ID = "1tvTXSsFDK5xAVALQPdDPJOitBufJE6UB_MN4q5nbLXk"

# Name of the game format.
# (if I was a good programmer this wouldd be per-sheet)
FORMAT_NAME = "Inscryption PvP Augmented v0.4 beta"

# the first part of the google docs url.
url_base = f"https://docs.google.com/spreadsheets/d/"

# ignore this; used for some internal modules
url_base += SHEET_ID+"/gviz/tq?tqx=out:csv&sheet="

# The name of the bottom tab with the sigils.
sigils_url = url_base+"Sigils"

# The name of the bottom tab with the cards.
cards_url = url_base+"Cards"

# shut up
info_url = url_base+"info"

# min # of cost to show as number instead of draw.
# e.g., since bones is 5, a 4 bone cost is drawn as IIII,
# while a 5 bone cost is drawn as 5xI.
# configurable per cost, and for custom costs.
COSTTHRESH = {
    "blood": 5,
    "bone": 5,
    "energy": 5,

    "shattered_garnet": 4,
    "shattered_ruby": 4,
    "shattered_rubies": 4,
    "shattered_topaz": 4,
    "shattered_emerald": 4,
    "shattered_sapphire": 4,
    "shattered_amethyst": 4,
    "shattered_prism" : 4,

    # I've got a hunch.
    "shattered" : 4,
    
    "garnet": 4,
    "ruby": 4,
    "topaz": 4,
    "emerald": 4,
    "sapphire": 4,
    "amethyst": 4,
    "prism": 4,
    
    "clowny": 1,
    "nuclear": 1,
    "malware": 1,
    "pure": 1,

    "valor": 1,

    "teeth": 4
}
# 1 means it will always use 1xR

# All the gems, so they get to be all happy together :)
# also this is a terrible way of handling this
HAPPYGEMS = ["garnet", "garnets",
             "ruby", "rubies",
             "topaz", "topazes", # what even is the plural of this
             "emerald", "emeralds",
             "sapphire", "sapphires",
             "amethyst", "amethysts",
             "prism", "prisms",
             "shattered_garnet", "shattered_garnets",
             "shattered_ruby", "shattered_rubies",
             "shattered_topaz", "shattered_topazes",
             "shattered_emerald", "shattered_emeralds",
             "shattered_sapphire", "shattered_sapphires",
             "shattered_amethyst", "shattered amethysts",
             "shattered_prism", "shattered prisms"]

# Sigils that need to reference another card by name.
TOKENSIGILS = ["Fledgling","Frozen Away","Creeping Outwards","Loose Tail"]

# All-caps markers for special sigil types/interactions.
METASIGILS = ["CELL","CONDUIT","TRANSFORM","RAINBOW","LATCH"]
# some of these are still unused lol

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

##################

# starting a new section
# maybe eventually I'll have it support custom styles

# for now though this just controls some text boundaries
TEXTW_SIGIL = 750
TEXTW_FLAVOR = 820
TEXTW_CREDIT = 640

FORMATPOS = (560,1483)

