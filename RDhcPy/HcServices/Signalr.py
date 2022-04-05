from signalrcore.hub_connection_builder import HubConnectionBuilder
import asyncio
import queue
import requests
from Cache.GlobalVariables import GlobalVariables
import Constant.constant as const
import logging
import threading
from Contracts.ITransport import ITransport
from Helper.System import System, eliminate_current_progress
import datetime
import time


def get_token():
    cache = GlobalVariables()
    try:
        renew_token = const.SERVER_HOST + const.TOKEN_URL
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'X-DormitoryId': cache.DormitoryId,
                   'Cookie': "RefreshToken={refresh_token}".format(refresh_token=cache.RefreshToken)}
        response = requests.post(
            renew_token, json=None, headers=headers).json()
        token = response['token']
        headers['Cookie'] = "Token={token}".format(token=token)
        # print(token)
        return token
    except Exception as e:
        print(f'Error get SignalR token: {e}')
        logging.Logger.error(f'Error get SignalR token: {e}')
        return None


class Signalr(ITransport):
    __hub: HubConnectionBuilder
    __globalVariables: GlobalVariables
    __logger: logging.Logger
    __lock: threading.Lock

    def __init__(self, log: logging.Logger):
        super().__init__()
        self.__logger = log
        self.__globalVariables = GlobalVariables()
        self.__lock = threading.Lock()

    def __build_connection(self):
        self.__hub = HubConnectionBuilder() \
            .with_url(const.SERVER_HOST + const.SIGNALR_SERVER_URL,
                      options={
                          "access_token_factory": get_token,
                          "headers": {
                          }
                      }) \
            .build()
        # .configure_logging(logging.DEBUG, socket_trace=True) \
        return self

    def __on_receive_event(self):
        self.__hub.on("Receive", self.__receive_event_callback)

    def __receive_event_callback(self, data):
        with self.__lock:
            # print(f"=========================>>>>>>>>>>>>>>>>>>>>> {data[1]}")
            if data[1] == const.SIGNALR_APP_COMMAND_ENTITY:
                self.receive_command_data_queue.put(data)
            # self.receive_response_data_queue.put(data)

    def __on_disconnect_event(self):
        self.__hub.on_close(self.__disconnect_event_callback)

    def __disconnect_event_callback(self):
        print("Disconnect to signalr server")
        self.__logger.debug("Disconnect to signalr server")
        self.reconnect()

    def __on_connect_event(self):
        self.__hub.on_open(self.__connect_event_callback())

    def __connect_event_callback(self):
        print("Try connect to signalr server")
        self.__logger.debug("Try connect to signalr server")

    async def disconnect(self):
        try:
            self.__hub.stop()
        except:
            eliminate_current_progress()

    def send(self, destination, data_send):
        entity = data_send[0]
        message = data_send[1]
        self.__hub.send("Send", [destination, entity, message])

    def connect(self):
        connect_success = False
        while self.__globalVariables.RefreshToken == "":
            time.sleep(1)
        self.__build_connection()
        self.__on_connect_event()
        self.__on_disconnect_event()
        self.__on_receive_event()
        while not connect_success:
            try:
                self.__hub.start()
                self.__globalVariables.SignalrConnectSuccessFlag = True
                connect_success = True
            except Exception as err:
                self.__logger.error(
                    f"Exception when connect with signalr server: {err}")
                print(f"Exception when connect with signalr server:")
                print(err)
                self.__globalVariables.SignalrConnectSuccessFlag = False
            time.sleep(3)

    def reconnect(self):
        try:
            time.sleep(20)
            self.__hub.start()
            print("Reconnect to signalr server successfully")
            self.__logger.debug("Reconnect to signalr server successfully")
        except:
            print("Fail to reconnect to signalr server")
            self.__logger.error("Fail to reconnect to signalr server")
            eliminate_current_progress()

    def receive(self):
        pass
