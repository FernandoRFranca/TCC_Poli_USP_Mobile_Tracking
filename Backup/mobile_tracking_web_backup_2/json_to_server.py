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
    #truck = {'truck_id': 'truck_1','evento': "Telemetria",'timestamp': round(time.time(), 0), 'data': {'rotacao': 0, 'porta': False, 'bau': False, 'janela': False, 'conectado': False, 'estaBloqueiado': False, 'bloqueiomanual': False, 'latitude': -23.6246758, 'longitude': -46.7015654}}
    truck = {'truck_id': 'truck_1','evento': "Telemetria",'timestamp': round(time.time(), 0), 'data': {'rotacao': 0, 'porta': False, 'bau': False, 'janela': False, 'conectado': False, 'estaBloqueiado': False, 'bloqueiomanual': False, 'latitude': -23.5269379, 'longitude': -46.7639624}}
    #truck = {"truck_id":"truck_1","evento":"Telemetria","timestamp": round(time.time(), 0),"data":{"latitude":-23.5709292,"longitude":-46.744901,"conectado":True,"atualizado":True,"acelerador":0,"embreagem":1,"rotacao":3500,"pedal":222,"temperatura_agua":24,"pedal_freio_1":1,"pedal_freio_2":1,"cruise_control":1,"epc":1,"ac_on_off":1,"consumo_combustivel":329,"torque":23.72,"velocidade_fina":112.55,"marcha":2,"pedal_embreagem":0,"pedal_freio":0,"modo_cruzeiro":0,"pedal_sim":1,"ref_cruzeiro":73,"erro_hardware":26,"freio_est":1,"luz_bateria":1,"tanque":100,"reserva":1,"velocidade_grosso":100,"temp_ambiente_delay":54,"temp_ambiente":35,"temp_oleo":30,"temp_agua":27,"hodometro":1278523,"seta_esquerda":1,"seta_direita":1,"pisca_alerta":1,"re":0,"porta_motorista":0,"porta_passageiro":1,"porta_te":1,"porta_td":1,"capo":1,"porta_malas":1,"backlight":62}}
    example_json = json.dumps(truck)
    return example_json

async def hello():
    
    import traceback
        
    uri = "ws://127.0.0.1:5005"
    #uri = "ws://35.192.96.220:5005"
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
#asyncio.get_event_loop().run_forever()