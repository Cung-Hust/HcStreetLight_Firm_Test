import Constant.constant as const
from requests.exceptions import HTTPError
from requests.structures import CaseInsensitiveDict
import asyncio
import aiohttp
import logging


class HttpRequest:
    __header: CaseInsensitiveDict
    __body: dict
    __url: str
    __cookie: dict
    
    @property
    def body(self):
        return self.__body
    
    @property
    def header(self):
        return self.__header
    
    @property 
    def url(self):
        return self.__url

    @header.setter
    def header(self, header: CaseInsensitiveDict):
        self.__header = header

    @body.setter
    def body(self, body: dict):
        self.__body = body

    @url.setter
    def url(self, url: str):
        self.__url = url


class Http:
    def create_new_http_header(self, domitory_id: str = "", cookie: str = ""):
        new_http_header = CaseInsensitiveDict()
        new_http_header["Accept"] = "application/json"
        new_http_header["X-DormitoryId"] = domitory_id
        new_http_header["Cookie"] = cookie
        return new_http_header
    
    def create_new_http_request(self, url: str = None, body_data: dict = {}, header: CaseInsensitiveDict = {}):
        new_http_request = HttpRequest()
        new_http_request.body = body_data
        new_http_request.header = header
        new_http_request.url = url
        return new_http_request

    async def get(self, session: aiohttp.ClientSession, req: HttpRequest):
        resp = None
        try:
            async with session.get(req.url, headers=req.header, json=req.body) as resp:
                resp.raise_for_status()
                await resp.json()
                return resp
        except HTTPError as err:  
            return ""
        except Exception as err:
            return ""


    async def post(self, session: aiohttp.ClientSession, req: HttpRequest):
        try:
            async with session.post(req.url, headers=req.header, json=req.body) as resp:
                resp.raise_for_status()
                await resp.json()
                return resp
        except HTTPError as err:
            return ""
        except Exception as err:
            return ""
    
    async def put(self, session: aiohttp.ClientSession, req: HttpRequest):
        resp = None
        try:
            async with session.put(req.url, headers=req.header, json=req.body) as resp:
                resp.raise_for_status()
                await resp.json()
        except HTTPError as err:  
            return ""
        except Exception as err:
            return ""
        return resp

    async def delete(self, session: aiohttp.ClientSession, req: HttpRequest):
        resp = None
        try:
            async with session.delete(req.url, headers=req.header, json=req.body) as resp:
                resp.raise_for_status()
                await resp.json()
        except HTTPError as err:  
            return ""
        except Exception as err:
            return ""
        return resp

