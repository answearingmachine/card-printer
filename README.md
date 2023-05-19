# Inscryption Augmented Card Graphic Generator
script to automatically assemble playing card graphics from data hosted on a spreadsheet.
I did not make most of these graphics. Most of them are attributed to Pixel Profligate (#5078). Other known contributors include, in no particular order:
- Redd#9637
- bluemem#2008
- Jghbug7#8304
- OkaOka#3352
- Yoyo4real#6565

## How to use

There are plans to collaborate and make a web-hosted interface for generating individual cards, but for now this version is intended to be manually installed and run, as it sources from a Google Office spreadsheet that it treats as a database. 

**To install:**

* Install [Python](https://www.python.org/downloads/release/python-3113/)
* Install Pillow (Open command prompt and enter `Python3 -m pip install Pillow`)
* Install Pandas (`Python3 -m pip install Pandas`)
* Download the repository, unzip if necessary, and run `addtext.py` to use.

**To make custom cards:**

* Create a copy of the [card info spreadsheet](https://docs.google.com/spreadsheets/d/1tvTXSsFDK5xAVALQPdDPJOitBufJE6UB_MN4q5nbLXk/)
	* In the top left, click **File** → **Make a Copy**
	* NOTE: The included spreadsheet has data validation to limit entries to the four temples included in the base game. You will need to edit it to support custom temples.
* Edit `printerconfig.py` and replace the ID part of the url (in line 8) with that of your own sheet copy.
* Refer to the instructions in `printerconfig.py` for adding custom costs and certain types of custom sigils. 