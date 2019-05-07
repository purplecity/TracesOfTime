"""
GET  ../xxx/xxx?param1=xxx&param2=xxx
POST ../xxx/xxx  body={}
"""

import re
import logging
import json
import tornado.web
import tornado.gen
from urllib.parse import urlparse
from urllib.parse import parse_qs
from BackendServer import ServerProxy
from Util.Excpt import *

global _url_config, _url_re

_url_config = {}
_url_re = {}

def _getUrlConfig():
    import os
    global _url_config

    url_config_file = os.path.dirname(os.path.realpath(__file__)) + '/url_config.json'
    if not _url_config:
        with open(url_config_file, 'r') as fs:
            _url_config = json.load(fs)
    return _url_config

def _getUrlRe():
    global _url_config, _url_re
    if _url_config:
        for key in _url_config:
            _url_re[re.compile('^'  + key + '$')] = key
    return _url_re

class RestfulParser:
    def __init__(self, url):
        self.url = url
        result = urlparse(url)
        self.scheme = result.scheme
        self.host = result.hostname
        self.port = result.port
        self.path = result.path
        self.query = result.query
        self.method = result.path.split('/')[-1] if '' != result.path else ''
        self.kwargs = dict(
                [(k, v[0]) for k, v in parse_qs(result.query).items()])

class RequestParser:
    def __init__(self):
        self.path = ''

    def __call__(self, request):
        rest = RestfulParser(request.uri)
        self.path = rest.path
        kwargs = rest.kwargs
        cnttype = 'None'
        if 'Content-Type' in request.headers:
            cnttype = request.headers['Content-Type'].lower()
        body = None
        if -1 != cnttype.find('application/json') and request.body:
            body = json.loads(request.body)
        return (kwargs, body)

class HandlerAll(tornado.web.RequestHandler):
    def initialize(self):
        self.req_parser = RequestParser()

    @tornado.gen.coroutine
    #tornado会把写定url中的通配符  对应于 实际请求来的url中的位置 当做args传参
    def get(self, *args, **kwargs):
        try:
            err_rep = {"data": None, "code": 400, "message": "Your request is invalid."}
            http_method = 'GET'
            url_result = self.req_parser(self.request)
            path = self.req_parser.path
            url_config = _getUrlConfig()
            url_re = _getUrlRe()

            for prog in url_re:
                res = prog.match(path)
                if not res:
                    continue
                key = url_re.get(prog)
                handler = url_config.get(key)
                if not handler:
                    logging.error('not defined handler for this url')
                    raise InnerUrlConfigError()
                if not handler.get(http_method):
                    logging.error('not defined method for this url')
                    raise InnerUrlConfigError()

                proxy = ServerProxy()
                call = getattr(proxy, handler[http_method]['method'], None)
                params = eval(handle[http_method]['params'] % args)
                #字符串打印  旧的python打印方法 把args传入method[http_method]['params']
                if not call:
                    logging.error("ServerProxy have't relevant method")
                    raise InnerServerNotFindUrlMethodError()
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                if url_result[0]:
                    self.write(call(**url_result[0], **params))
                else:
                    self.write(call(**params))
                return None
        except Exception as err:
            logging.warning('{} exception: {}'.format(http_method, err))
            self.write(err_rep)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        try:
            err_rep = {"data": None, "code": 400, "message": "Your request is invalid."}
            http_method = 'POST'
            url_result = self.req_parser(self.request)
            path = self.req_parser.path
            url_config = _getUrlConfig()
            url_re = _getUrlRe()

            for prog in url_re:
                res = prog.match(path)
                if not res:
                    continue
                key = url_re.get(prog)
                handle = url_config.get(key)
                if not handle:
                    logging.error('not defined handle for this url')
                    raise InnerUrlConfigError()
                if not handle.get(http_method):
                    logging.error('not defined method for this url')
                    raise InnerUrlConfigError()

                proxy = ServerProxy()
                call = getattr(proxy, handle[http_method]['method'], None)
                params = url_result[1] if url_result[1] else {}
                if not call:
                    logging.error("ServerProxy have't relevant method")
                    raise InnerServerNotFindUrlMethodError()
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(call(**params))
                return None
        except Exception as err:
            logging.warning('{} exception: {}'.format(http_method, err))
            self.write(err_rep)

def BindHandlers(app, host):
    url_config = _getUrlConfig()
    app.add_handlers(host, [(url, HandlerAll) for url in url_config.keys()])
