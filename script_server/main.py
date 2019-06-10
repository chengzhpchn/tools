#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
from protocol import RemoteAPI, PalletTarget, PalletCurrent

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
    current = api.GetPalletState()
    if current == PalletCurrent.BOTTOM:
        target = api.SetPalletState(PalletTarget.TOP)
        assert(target == PalletTarget.TOP)
    elif current == PalletCurrent.TOP:
        target = api.SetPalletState(PalletTarget.BOTTOM)
        assert (target == PalletTarget.BOTTOM)

if __name__ == "__main__":
    serve(host, port)
