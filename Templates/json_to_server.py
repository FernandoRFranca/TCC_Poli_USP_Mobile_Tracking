# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 22:23:39 2019

@author: zfern
"""

import asyncio
import websockets
from time import sleep

def create_example_json():
    
    import json
    import time
    
    #truck = {'truck_id': 1,'left door': 'opened', 'right door': 'closed', 'engine': 'ON', 'gps': 'teste', 'speed': 100}
    truck = {'id': 'truck_1','evento': "Telemetria",'timestamp': round(time.time(), 0), 'data': {'rotacao': 0, 'porta': False, 'bau': False, 'janela': False, 'conectado': False, 'estaBloqueiado': False, 'bloqueiomanual': False, 'latitude': -23.6246758, 'longitude': -46.7015654}}
    example_json = json.dumps(truck)
    return example_json

async def hello():
    
    import traceback
        
    uri = "ws://35.222.251.236:5005"
    #first = True # Para versão do servidor com key, usar essa linha!
    first = False # else
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                if first:
                    name = "json_key"
                    await websocket.send(name)
                    first = False
                else:
                    name = create_example_json()
                    await websocket.send(name)
                    print(f"> {name}\n")
        
                greeting = await websocket.recv()
                print(f"< {greeting}\n")
                sleep(10)
            except:
                print("Connection error.")
                traceback.print_exc()
                sleep(1)
                break

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()