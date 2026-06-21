# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from mod.client.system.clientSystem import ClientSystem
from mod.client.ui.screenNode import ScreenNode
from mod.common.mod import Mod
from mod.server.system.serverSystem import ServerSystem
from typing import Callable, List, Optional, Type, Union


class Dist:
    server: int
    client: int


class Easy(Mod):
    name: str
    version: Optional[str]
    dist: List[int]

    def __init__(self, name: str, version: Optional[str] = None, dist: Optional[List[int]] = None) -> None:
        ...

    def __call__(self, cls: Type[EventBus]) -> Type[EventBus]:
        ...


class Event:
    name: str
    priority: int
    custom: bool
    broadcast: bool
    dist: List[int]

    def __init__(self, name: str, priority: int = 0, custom: bool = False, broadcast: bool = False, dist: Optional[List[int]] = None) -> None:
        ...

    def __call__(self, func: Callable) -> Callable:
        ...


class Server(ServerSystem):
    api = serverApi


class ServerEvent(Event):
    ...


class Client(ClientSystem):
    api = clientApi


class ClientEvent(Event):
    ...


class EventBus:
    MOD_NAME: str
    system: Union[Server, Client]

    def register(self, instance: EventBus) -> None:
        ...

    def unregister(self, instance: EventBus) -> None:
        ...


class ServerEventBus(EventBus):
    system: Server


class ClientEventBus(EventBus):
    system: Client


class ScreenEventBus(ScreenNode, ClientEventBus):
    ...
