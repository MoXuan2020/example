# -*- coding: utf-8 -*-
from mod.client.system.clientSystem import ClientSystem
from mod.common.mod import Mod
from mod.server.system.serverSystem import ServerSystem
from typing import Callable, List, Optional, Type


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


class ServerEvent(Event):
    ...


class ClientEvent(Event):
    ...


class System(ServerSystem, ClientSystem):
    ...


class EventBus:
    MOD_NAME: str
    dist: int
    system: System

    def register(self, instance: EventBus) -> None:
        ...

    def unregister(self, instance: EventBus) -> None:
        ...
