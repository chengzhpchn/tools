# -*- coding:utf-8 -*-
from rpc import AGV_RPC

class PalletTarget:
    BOTTOM = 0
    TOP    = 1

class PalletCurrent:
    BOTTOM = 0
    WAIT_FOR_RISING = 1
    RISING = 2
    TOP = 3
    WAIT_FOR_FALLING = 4
    FALLING = 5

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
            return ack[0]
        return "SetForkState", [TargetHeight, Liftmode], OnAck

    @AGV_RPC
    def SetPalletState(self, Target):
        '''
        :param Target: see PalletTarget
        :return: Target
        '''
        def OnAck(ack):
            Target = ack[0]
            return Target

        return "SetPalletState", [Target], OnAck

    @AGV_RPC
    def GetPalletState(self):
        '''
        :param:
        :return: current: see PalletCurrent
        '''
        def OnAck(ack):
            current = ack[0]
            return current

        return "GetPalletState", [], OnAck

