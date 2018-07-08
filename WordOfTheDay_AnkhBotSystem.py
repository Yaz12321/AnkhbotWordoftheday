#---------------------------------------
#	Import Libraries
#---------------------------------------
import  sys, json, os, codecs ,clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

import re
#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "WordOfTheDay"
Website = "https://github.com/Yaz12321"
Creator = "Yaz12321"
Version = "1.0"
Description = "Display Word of the Day on stream"

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
#   Version Information
#---------------------------------------

# Version:

# > 1.0 < 
    # Official Release

class Settings:
    # Tries to load settings from file if given 
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig') 
        else: #set variables if no settings file
            self.OnlyLive = False

            
    # Reload settings on save through UI
    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,  encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return


#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
    # Globals
    global MySettings

    # Load in saved settings
    MySettings = Settings(settingsFile)
    global wordcount
    wordcount = {'Empty':0}

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return


global wordcount
wordcount = {'Empty':0}
global TopWord
TopWord = ""
global TopCount
TopCount = 0

def Reset():
    global wordcount
    wordcount = {'Empty':0}
    global TopWord
    TopWord = ""
    global TopCount
    TopCount = 0
    return

def Clear():
    path = os.path.dirname(os.path.abspath(__file__))
    f = open("{}/TopWord.txt".format(path),"w+")
    f.write("Word of the day is:")
    f.close()
    return
    
        
def Execute(data):
    path = os.path.dirname(os.path.abspath(__file__))
    if data.IsChatMessage():
       
        #check if command is in "live only mode"
        if MySettings.OnlyLive:

            #set run permission
            startCheck = data.IsLive()
            
        else: #set run permission
            startCheck = True
        
        #check if user has permission
        if startCheck:
            cleanString = re.sub('\W+',' ', data.Message )
            words = cleanString.split()
            for word in words:
                if len(word) > 3:
                
                    if word in wordcount.keys():
                        global wordcount
                        wordcount[word] = wordcount[word] + 1
                    else:
                        global wordcount
                        wordcount[word] = 1

            tcount = max(wordcount.values())
            twords = [i for i, j in enumerate(wordcount.values()) if j == tcount]
            tword = wordcount.keys()[twords[0]]

            if tcount > TopCount:
                global TopWord
                TopWord = tword
                global TopCount
                TopCount = tcount
                
                f = open("{}/TopWord.txt".format(path),"w+")
                f.write("Word of the day is: {} - {}".format(TopWord.upper(),TopCount))
                f.close()

                    
                    
    return

def Tick():
    return

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
    return
