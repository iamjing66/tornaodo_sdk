import json
import logging

class InterfaceLanguage():

    def __init__(self):
        self.languageData = {}

        with open("config/language/language_ch.json", "r", encoding='UTF-8') as f:
            #print("f = " , str(f.read()))
            self.languageData = json.load(f)

        print("languageJson = " , str(self.languageData))



    def GetMsg(self,SID ,languageStr = "ch"):
        #print("self.languageData = ",self.languageData)
        #logging.info("GetMsg SID = %s self.languageData = %s" % (SID,str(self.languageData)))

        if SID not in self.languageData.keys():
            return ""
        return self.languageData[SID]