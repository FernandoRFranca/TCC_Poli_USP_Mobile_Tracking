# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 16:37:17 2019

@author: zfern
"""

#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import sqlite3

def from_db_to_xml():
    return 0

async def listen_to_client(websocket, path):
    name = await websocket.recv()
    print(name)

    greeting =  "Hello " + name

    await websocket.send(greeting)
    print(greeting)
    
"""async def consumer_handler(websocket, path):
    async for message in websocket:
        await consumer(message)"""

"""def consumer(msg):
    print("Recebeu: " + msg)"""

start_server = websockets.serve(listen_to_client, "0.0.0.0", 5005)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()