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



    def user_connect(self, user, uid, client_model):

        #logging.info("[websocket] logining users = %s" % self.connector)

        #通过redis判断是否存在相同的账号(websocket id ,服务器地址)
        #写分服事务，通过redis
        #self.user_kick(uid,client_model)

        #记录新用户（websocket id ,服务器地址）redis
        #绑定新用户

        uuid = application.App.SUID + str(self.GlobalUUID)
        self.dicusers[user] = [uuid, uid, client_model]
        self.GlobalUUID += 1
        self.dicusers_id[uuid] = user
        self.connector[client_model][uid] = uuid

        rd = RedisData(2)
        rds = rd.redis_pool()
        key = str(uid) + "$" + client_model
        #处理踢掉线
        value = rds.hget("websocket",key)
        print("value = " , value)
        if value != None:
            value = value.decode()
            #老账号要被顶替
            arr = value.split('$')
            key1 = arr[1] + "C1"

            C_ServerEventCache.SetEvent(key1,arr[0],'0')


        #缓存新记录
        value = uuid + "$" + application.App.RedisServerAddress
        rds.hset("websocket",key,value)

        logging.info("[websocket] login Succ = uuid = %s - %s" % (str(uuid),application.App.RedisServerAddress))


    def user_kick(self,uuid):

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


            del self.dicusers[user]
            del self.dicusers_id[uuid]
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

    #同步消息推送(当前服)
    def trigger(self, pam_apptype, uid, code, pam):
        ''' 客户端推送内容 '''
        logging.info(f"uid: {uid} ,client: {pam_apptype}, code: {code}")
        key = str(uid)+"$"+pam_apptype
        rd = RedisData(2)
        rds = rd.redis_pool()
        value = rds.hget("websocket", key)
        if value:
            value = str(value, encoding="utf-8")
            uuid = str(value.split('$')[0])
            cuser = self.dicusers_id[uuid]
            cuser.write_message(str(code) + "@" + pam)


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
