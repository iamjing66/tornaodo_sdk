#!/usr/bin/env python
# coding=utf-8

import logging
import logging.handlers
import signal

import socket
import json

import os

import Global
import tornado.ioloop
import tornado.options
import tornado.httpserver
from urllib.request import urlopen
from application import App
import redis
from tornado.options import define, options

from handlers.wechatGZH.wxtoken import WxShedule

define("port", default = 9001, help = "run on the given port", type = int)


def init_logging():
    tornado.options.parse_command_line()
    from tornado.log import LogFormatter


    file_handler = logging.handlers.TimedRotatingFileHandler(Global.settings["log_file"], when="MIDNIGHT", interval=1, backupCount=30)
    access_log = logging.getLogger()
    datefmt = '[%Y-%m-%d %H:%M:%S %z]'
    fmt = '%(asctime)s [%(levelname)s %(name)s pid:%(process)d port:{port} %(filename)s:%(lineno)d] %(message)s'.format(port=options.port or '')
    formatter = LogFormatter(color=True, fmt=fmt, datefmt=datefmt)

    # # 输出格式
    # formatter = logging.Formatter(
    #     "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [%(lineno)d]  %(message)s"
    # )


    file_handler.setFormatter(formatter)
    access_log.addHandler(file_handler)

def kill_server(sig, frame):
    logging.info('Caught signal: %s stop server(%s)' % (sig, options.port))
    tornado.ioloop.IOLoop.instance().stop()


def register_signal():
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    signal.signal(signal.SIGINT, kill_server)
    signal.signal(signal.SIGQUIT, kill_server)
    signal.signal(signal.SIGHUP, kill_server)


def main():
    # 执行定时任务，定时刷新获取 access_token和jsapi_ticket
    # wx_shedule = WxShedule()
    # wx_shedule.excute()

    tornado.options.parse_command_line()
    print("options.port = ", options.port)
    http_server = tornado.httpserver.HTTPServer(App)
    http_server.listen(options.port)

    ENV = os.getenv("ENV", "test")
    if ENV == "test":
        thisIP = get_host_ip()
    else:
        thisIP = json.load(urlopen('http://httpbin.org/ip'))['origin']
    thisPort = options.port
    App.DoInit(thisIP,thisPort)

    print("Development server is running at http://127.0.0.1:%s" % options.port)
    print("Quit the server with Control-C")
    tornado.ioloop.IOLoop.instance().start()


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('10.0.0.1',8080))
        ip= s.getsockname()[0]
    finally:
        s.close()
    return ip


init_logging()



if __name__ == "__main__":
    main()
