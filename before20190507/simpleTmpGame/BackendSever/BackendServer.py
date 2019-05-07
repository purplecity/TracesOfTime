import os
import sys
import daemon
import logging
from Util import getConfig

def logInit():
    fmt = '%(asctime)-15s [%(levelname)s] '
    fmt += '%(filename)s:%(funcName)s:%(lineno)d %(message)s'
    level = getConfig()['log_level']
    logging.basicConfig(format = fmt, level = eval(level))

def pidfile():
    os.makedirs('/tmp/PCE', mode = 0o755, exist_ok = True)
    return '/tmp/PCE/PCE_BackendServer.pid'

def sysInit():
    fs = open(pidfile(), 'w')
    fs.write(str(os.getpid()))
    fs.close()

def startServer(cryptopwd):
    from  BackendServer.ServerProxy import ServerProxy
    ServerProxy.CryptoPWD = cryptopwd
    import tornado
    import tornado.web
    APP = tornado.web.Application()
    config = getConfig()
    host = config['backend_host']
    port = config['backend_port']
    from BackendServer.Handler import bindHandlers
    bindHandlers(APP, host)
    APP.listen(port)
    tornado.ioloop.IOLoop.current().start()
    logging.info('backend server started')


def main(argv1):
    logInit()
    sysInit()
    with daemon.DaemonContext(stderr = sys.stderr):
        startServer(argv1)

if '__main__' == __name__:
    argv1 = sys.argv[1]
    main(argv1)
