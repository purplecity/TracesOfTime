import requests
import logging
from Utils.Excpt import InfuraRequestError

class InfuraRequest:

    def __init__(self):
        from Utils import getConfig
        self._InfuraInfo = getConfig()["InfuraInfo"]
        self._request_counter = itertools.count()

    def postInfuraRequest(self, *args,type = "json",method = ""):
        try:
            payload = {"jsonrpc":"2.0"}
            payload["method"] = method
            payload["params"] = list(args)
            payload["id"] = next(self._request_counter)
            headers = {"Content-Type": "application/json"}
            headers["User-Agent"] = self._InfuraInfo["headers"]

            ret = requests.post(self._InfuraInfo["url"], json = payload, headers = headers, timeout = self._InfuraInfo["timeout"])
            if type == "json":
                return ret.json()
            else:
                return ret.text()
        except Exception as err:
            logging.error("getTransactionCount error")
            raise InfuraRequestError()

infuraRequest = InfuraRequest()
