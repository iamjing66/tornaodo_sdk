import tornado
from tornado import options, websocket
import logging

import application
from handlers.redisServer.RedisInterface import RedisData, C_ServerEventCache


class ProStatus:


    def __init__(self):
        self.GlobalUUID = 1
        self.connector = {"editor": {}, "app": {}}  # 记录当前连接的user
        self.dicusers_id = {}
        self.dicusers = {}

        #tornado.ioloop.IOLoop.instance().call_later(5, self.PrintWebsocket)


    def PrintWebsocket(self):

        print("connector",self.connector)
        print("dicusers_id", self.dicusers_id)
        print("dicusers", self.dicusers)
        print("=======================*")
        for user in self.dicusers.keys():
            print("user = " , user)
        print("=======================#")
        tornado.ioloop.IOLoop.instance().call_later(5, self.PrintWebsocket)


    def user_connect(self, user, uid, client_model):

        #logging.info("[websocket] logining users = %s" % self.connector)

        #通过redis判断是否存在相同的账号(websocket id ,服务器地址)
        #写分服事务，通过redis
        #self.user_kick(uid,client_model)

        # 踢下线
        self.syncTrigger(client_model, uid, "100", '0')

        #记录新用户（websocket id ,服务器地址）redis
        #绑定新用户
        uuid = application.App.SUID + str(self.GlobalUUID)
        self.dicusers[user] = [uuid, uid, client_model]
        self.GlobalUUID += 1
        self.dicusers_id[uuid] = user
        self.connector[client_model][uid] = uuid

        #缓存新记录
        rd = RedisData(2)
        rds = rd.redis_pool()
        key = str(uid) + "$" + client_model
        value = uuid + "$" + application.App.RedisServerAddress
        rds.hset("websocket",key,value)

        logging.info("[websocket] login Succ = uuid = %s - %s dicusers_id = %s" % (str(uuid),application.App.RedisServerAddress,self.dicusers_id))


    def user_kick(self,uuid):

        #logging.info("[websocket] kick user = uuid = %s dicusers_id = %s" % (str(uuid),str(self.dicusers_id)))
        if uuid in self.dicusers_id.keys():
            #该账号有记录
            cuser = self.dicusers_id[uuid]
            if cuser.ws_connection:
                cuser.write_message("-88@")
                logging.info("[websocket] kick user = uuid = %s" % (str(uuid) ))
            #清除老记录
            self.user_dispose(cuser,1)


    def user_dispose(self,user,kick):

        if user in self.dicusers.keys():

            uuid = self.dicusers[user][0]
            uid = self.dicusers[user][1]
            clientmodel = self.dicusers[user][2]

            logging.info("[user_dispose] uuid = %s uid = %s clientmodel = %s kick = %d" % (uuid,str(uid),str(clientmodel),kick))

            if user in self.dicusers.keys():
                del self.dicusers[user]
            if uuid in self.dicusers_id.keys():
                del self.dicusers_id[uuid]
            if uid in self.connector[clientmodel].keys():
                del self.connector[clientmodel][uid]


            if kick == 0:
                key = str(uid) + "$" + clientmodel
                rd = RedisData(2)
                rds = rd.redis_pool()
                rds.hdel("websocket", key)

            #del self.connector[clientmodel][uid]

            # key = str(uid) + "$" + clientmodel
            # rd = RedisData(2)
            # rds = rd.redis_pool()

            #rds.hdel("websocket",key)

            # if kick == 0:
            #     globalRedisU.redisurl_delete(uid,clientmodel)

            logging.info("[websocket] disconnect = uuid = %s " % (str(uuid)))


    # def user_remove(self, uid, client_model):
    #     logging.info("[websocket] quit request = %s - %s - %s" % (str(uid), str(client_model),self.connector))
    #     #logging.info(self.connector)
    #     if uid in self.connector[client_model].keys():
    #         self.connector[client_model].pop(str(uid))
    #         logging.info("[websocket] quit Succ = %s - %s - %s" % (str(uid), str(client_model), self.connector))
    #     #logging.info(self.connector)
    #     #logging.info("用户退出: %s" % str(uid))


    def syncTrigger(self,pam_apptype,uid,code,pam):

        logging.info("[redis] pam_apptype = %s - uid = %s code = %s pam = %s connector = %s" % (str(pam_apptype), str(uid),str(code),str(pam),str(self.connector)))
        if str(uid) in self.connector[pam_apptype]:
            uuid = self.connector[pam_apptype][str(uid)]
            self.DoSyncThing(uuid,code,pam)
        else:
            rd = RedisData(2)
            rds = rd.redis_pool()
            key = str(uid) + "$" + pam_apptype
            #异步通知
            value = rds.hget("websocket", key)
            logging.info("value = %s key = %s " % (value, key))
            if value != None:
                value = value.decode()
                arr = value.split('$')
                key1 = arr[1] + "$CFD"
                cpam = str(code) + "$" + str(pam)
                C_ServerEventCache.SetEvent(key1, arr[0], cpam)


    def DoSyncThing(self,uuid,code,pam):

        if code == "100":
            self.user_kick(uuid)
        elif uuid in self.dicusers_id.keys():
            cuser = self.dicusers_id[uuid]
            cuser.write_message(str(code)+"@" + str(pam))


    #同步消息推送(当前服)
    def trigger(self, pam_apptype, uid, code, pam):
        ''' 客户端推送内容 '''
        logging.info(f"uid: {uid} ,client: {pam_apptype}, code: {code}")
        if code == "106":   #分服通知
            self.syncTrigger(pam_apptype,uid,code,pam)
        else:
            if str(uid) in self.connector[pam_apptype]:
                uuid = self.connector[pam_apptype][str(uid)]
                cuser = self.dicusers_id[uuid]
                cuser.write_message(str(code) + "@" + pam)



    def DoMessage_Mail(self,uuid,pam):

        if uuid in self.dicusers_id.keys():
            cuser = self.dicusers_id[uuid]
            cuser.write_message("106@" + pam)





pro_status = ProStatus()


class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):

        # ip = self.request.host_name
        # port = options.options.port
        #self.write_message("-99@none")  # + globalRedisU.redis_serverip_get()
        logging.info("[websocket] open")

    def on_message(self, message: str):
        # message = -99@uid$(editor/clinet)
        logging.info("[websocket]receivemsg = %s" % message)
        ip = self.request.host_name
        port = options.options.port
        s1 = message.split("@")
        user_info = s1[1].split("$")
        uid = user_info[0]
        client_model = user_info[1]
        if s1[0] == "-99":
            pro_status.user_connect(self, uid, client_model)
        elif s1[0] == "-96":
            print("KeepAlive")
            self.write_message("-96@")
        # elif s1[0] == "-89":
        #     logging.info("用户退出")
        #     pro_status.user_remove(str(uid), client_model)
        #     logging.info(pro_status.connector)
        # self.write_message("-88@")
        # logging.info("用户重复登录1: %s" % str(self.uid))

    def on_close(self):

        logging.info("[websocket] close users = %s" % pro_status.dicusers_id.keys())
        pro_status.user_dispose(self,0)

    def check_origin(self, origin):
        return True
