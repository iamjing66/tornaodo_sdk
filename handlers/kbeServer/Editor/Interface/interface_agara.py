import tornado.escape
import Global
import time
from handlers.base import BaseHandler
from AgaraTorken.RtcTokenBuilder import RtcTokenBuilder,Role_Attendee


class AgaraTorkenHandler(BaseHandler):

    def get(self):

        channelName = self.get_argument("channelname")
        uid = int(self.get_argument("uid"))

        json_bck = {
            "Code" : "OK",
            "Torken" : ""
        }

        expireTimeInSeconds = 3600
        currentTimestamp = int(time.time())
        privilegeExpiredTs = 0 #currentTimestamp + expireTimeInSeconds

        try:
            token = RtcTokenBuilder.buildTokenWithUid(Global.Agara_appID, Global.Agara_appCertificate, channelName, uid, Role_Attendee,privilegeExpiredTs)
            json_bck["Torken"] = token
        except Exception as e:
            #print("AgaraTorken Get Err : ", e)
            json_bck["Code"] = "Err"

        self.write(json_bck)



class AgaraAppIPHandler(BaseHandler):

    def get(self):


        self.write(Global.Agara_appID)