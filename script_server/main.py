#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
from protocol import RemoteAPI

host='127.0.0.1'
port=23333


def serve(host, port):
    ip_port = (host, port)

    sk = socket.socket()
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sk.bind(ip_port)
    sk.listen(5)

    print 'server waiting...'
    conn,addr = sk.accept()
    print 'server working...'
    sk.close()
    api = RemoteAPI(conn)
    try:
        exec_script(api)
    finally:
        conn.close()

def exec_script(api):
    state, height, have_goods = api.GetForkState()
    print state, height, have_goods
    
    ack = api.SetForkState(1000, 1)
    print ack

if __name__ == "__main__":
    serve(host, port)
