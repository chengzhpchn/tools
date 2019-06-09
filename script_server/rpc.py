# -*- coding:utf-8 -*-

import json

timeout = 3000

class SyncStatus:
    Unknown=0
    SyncWaiting=1
    SyncTimeOut=2
    SyncSuccess=3
    
class Sender:
    ScriptSystem=0
    ControlSystem=1
    
class Command:
    def __init__(self):
        self.Id = ""
        self.Function = ""
        self.Parameters = []
        self.TimeOut = timeout
        self.SyncStatus = 0
        self.Sender = 0
    
    def to_json(self):
        return json.dumps({
            "Id" : self.Id,
            "Function" : self.Function,
            "Parameters" : self.Parameters,
            "TimeOut" : self.TimeOut,
            "SyncStatus" : self.SyncStatus,
            "Sender" : self.Sender
        })
    
    @classmethod    
    def from_json(cls, data):
        '''
        for response
        '''
        dict = json.loads(data)
        obj = cls()
        obj.id = dict["Id"]
        obj.Function = dict["Function"]
        obj.Parameters = dict["Parameters"]
        obj.SyncStatus = dict.get("SyncStatus", SyncStatus.SyncSuccess)
        return obj

def AGV_RPC(func):
    def wrapper(*args, **kwargs):
        api = args[0]
        func_name, args, on_ack = func(*args, **kwargs)
        
        cmd = Command()
        cmd.Function = func_name
        cmd.Parameters = args
        data = cmd.to_json()
        api.conn.sendall("\x02"+data+"\x03")
        
        client_data = api.conn.recv(2048)
        if client_data[0] == "\x02" and client_data[-1] == "\x03":
            ack = Command.from_json(client_data[1:-1])
            if (cmd.Function != ack.Function):
                raise Exception("Function not match for cmd and ack") 
            return on_ack(ack.Parameters)
        raise Exception("Invalid data:%s" % client_data) 
    return wrapper

__all__ = ['AGV_RPC']
    
