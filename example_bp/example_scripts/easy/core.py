# -*- coding: utf-8 -*-
import inspect

import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from mod.common.mod import Mod


class Dist(object):
    server = 0
    client = 1


class Easy(Mod):

    def __init__(self, name, version=None, dist=None):
        self.name = name
        self.version = version
        self.dist = dist or [Dist.server, Dist.client]

    def __call__(self, cls):
        if Dist.server in self.dist:
            cls.init_server = self.InitServer()(init_server)
            cls.destroy_server = self.DestroyServer()(destroy_server)
        if Dist.client in self.dist:
            cls.init_client = self.InitClient()(init_client)
            cls.destroy_client = self.DestroyClient()(destroy_client)
        return self.Binding(self.name, self.version)(cls)


class Event(object):

    def __init__(self, name, priority=0, custom=False, broadcast=False, dist=None):
        self.name = name
        self.priority = priority
        self.custom = custom
        self.broadcast = broadcast
        self.dist = dist or [Dist.server, Dist.client]

    def __call__(self, func):
        func.name = self.name
        func.priority = self.priority
        func.custom = self.custom
        func.broadcast = self.broadcast
        func.dist = self.dist
        return func


class Server(serverApi.GetServerSystemCls()):
    api = serverApi


class ServerEvent(Event):

    def __init__(self, name, priority=0, custom=False, broadcast=False):
        super(ServerEvent, self).__init__(name, priority, custom, broadcast, [Dist.server])


def init_server(self):
    self.system = serverApi.GetSystem(self.MOD_NAME, 'server') or serverApi.RegisterSystem(self.MOD_NAME, 'server', '%s.easy.core.Server' % self.__module__.split('.')[0])
    for _, func in inspect.getmembers(self, lambda member: inspect.ismethod(member) and Dist.server in getattr(member, 'dist', [])):
        if not func.custom:
            self.system.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), func.name, self, func, func.priority)
        elif not func.broadcast:
            self.system.ListenForEvent(self.MOD_NAME, 'client', func.name, self, func, func.priority)
        else:
            self.system.ListenForEvent(self.MOD_NAME, 'server', func.name, self, func, func.priority)


def destroy_server(self):
    for _, func in inspect.getmembers(self, lambda member: inspect.ismethod(member) and Dist.server in getattr(member, 'dist', [])):
        if not func.custom:
            self.system.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), func.name, self, func, func.priority)
        elif not func.broadcast:
            self.system.UnListenForEvent(self.MOD_NAME, 'client', func.name, self, func, func.priority)
        else:
            self.system.UnListenForEvent(self.MOD_NAME, 'server', func.name, self, func, func.priority)


class Client(clientApi.GetClientSystemCls()):
    api = clientApi


class ClientEvent(Event):

    def __init__(self, name, priority=0, custom=False, broadcast=False):
        super(ClientEvent, self).__init__(name, priority, custom, broadcast, [Dist.client])


def init_client(self):
    self.system = clientApi.GetSystem(self.MOD_NAME, 'client') or clientApi.RegisterSystem(self.MOD_NAME, 'client', '%s.easy.core.Client' % self.__module__.split('.')[0])
    for _, func in inspect.getmembers(self, lambda member: inspect.ismethod(member) and Dist.client in getattr(member, 'dist', [])):
        if not func.custom:
            self.system.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), func.name, self, func, func.priority)
        elif not func.broadcast:
            self.system.ListenForEvent(self.MOD_NAME, 'server', func.name, self, func, func.priority)
        else:
            self.system.ListenForEvent(self.MOD_NAME, 'client', func.name, self, func, func.priority)


def destroy_client(self):
    for _, func in inspect.getmembers(self, lambda member: inspect.ismethod(member) and Dist.client in getattr(member, 'dist', [])):
        if not func.custom:
            self.system.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), func.name, self, func, func.priority)
        elif not func.broadcast:
            self.system.UnListenForEvent(self.MOD_NAME, 'server', func.name, self, func, func.priority)
        else:
            self.system.UnListenForEvent(self.MOD_NAME, 'client', func.name, self, func, func.priority)


class EventBus(object):
    MOD_NAME = None
    system = None

    def register(self, instance):
        instance.MOD_NAME = self.MOD_NAME
        if isinstance(self.system, Server):
            init_server(instance)
        if isinstance(self.system, Client):
            init_client(instance)

    def unregister(self, instance):
        if isinstance(self.system, Server):
            destroy_server(instance)
        if isinstance(self.system, Client):
            destroy_client(instance)


class ServerEventBus(EventBus):
    pass


class ClientEventBus(EventBus):
    pass


class ScreenEventBus(clientApi.GetScreenNodeCls(), ClientEventBus):
    pass
