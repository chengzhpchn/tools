# -*- coding:utf-8 -*-
from rpc import AGV_RPC

class RemoteAPI:
    def __init__(self, conn):
        self.conn = conn
        
    @AGV_RPC
    def GetForkState(self):
        def OnAck(ack):
            state, height, have_goods = ack
            return  state, height, have_goods
        return "GetForkState", [], OnAck
        
    @AGV_RPC
    def SetForkState(self, TargetHeight, Liftmode):
        def OnAck(ack):
            return ack
        return "SetForkState", [TargetHeight, Liftmode], OnAck

__all__ = ['RemoteAPI']
