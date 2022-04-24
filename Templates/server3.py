# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 09:11:35 2019

@author: zfern
"""

#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import sqlite3
import os

global db_name
db_name = "trucks.db"

logging.basicConfig(filename='server_log.log',level=logging.DEBUG)

STATE = {"value": 0}

USERS = set()


def create_db(db_name):
    
    import traceback
    
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("""CREATE TABLE trucks (
                     evento text,
                     timestamp int,
                     rotacao int,
                     porta text,
                     bau text,
                     janela text,
                     conectado text,
                     estaBloqueiado text,
                     bloqueiomanual text,
                     latitude real,
                     longitude real
        )""")
        conn.commit()
        conn.close()
        return 0
    except:
        print("Erro ao criar DB.")
        print("")
        traceback.print_exc()        

def insert_row_into_db(db_name,row):
    
    import traceback
    
    #len_row = len(row)
    #row_string = ""
    """for i in range(0,len_row):
        try:
            if (i < len_row-1):
                row_string = row_string + "%s, " % row[i]
                print("row_string = ", row_string)
            elif (i == len_row-1):
                row_string = row_string + "%s" % row[i]
                print("row_string = ", row_string)
            else:
                print("Erro de escrita na função insert_row_into_db (ELSE)")
        except:
            print("Erro de escrita na função insert_row_into_db (EXCEPT)")"""
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        #print("row_string = ",row_string)
        c.execute("""INSERT INTO trucks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
        conn.commit()
        conn.close()
    except:
        print("Exception: Erro na função insert_row_into_db")
        traceback.print_exc()
    return 0

def create_example_json():
    
    import json
    
    #truck = {'truck_id': 1,'left door': 'opened', 'right door': 'closed', 'engine': 'ON', 'gps': "[0.5,-0.5]", 'speed': 100}
    truck = {'evento': "Telemetria",'timestamp': 0, 'data': {'rotacao': 0, 'porta': False, 'bau': False, 'janela': False, 'conectado': False, 'estaBloqueiado': False, 'bloqueiomanual': False, 'latitude': 1, 'longitude': 1}}
    example_json = json.dumps(truck)
    return example_json

def json_to_row(json_data):
    
    import json
    
    row = []
    
    dict_inst = json.loads(json_data)
    
    """row.append(dict_inst["truck_id"])
    row.append(dict_inst["left door"])
    row.append(dict_inst["right door"])
    row.append(dict_inst["engine"])
    row.append(dict_inst["gps"])
    row.append(dict_inst["speed"])"""
    
    row.append(dict_inst['evento']) #string
    row.append(dict_inst['timestamp']) #int
    row.append(dict_inst['data']['rotacao']) #int
    row.append(dict_inst['data']['porta']) #boolean
    row.append(dict_inst['data']['bau']) #boolean
    row.append(dict_inst['data']['janela']) #boolean
    row.append(dict_inst['data']['conectado']) #boolean
    row.append(dict_inst['data']['estaBloqueiado']) #boolean
    row.append(dict_inst['data']['bloqueiomanual']) #boolean
    row.append(dict_inst['data']['latitude']) #real
    row.append(dict_inst['data']['longitude']) #real
    
    
    """for key in dict_inst:
        row.append(dict_inst[key])"""
    
    return row

def print_all_lines_from_db(db_name):
    
    import traceback
    
    erro = 1
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        while (erro == 1):
            try:
                nome_do_db = "trucks"
                c.execute("""SELECT *
                             FROM %s""" % nome_do_db)
                print(c.fetchall())
                print('\n')
                conn.commit()
                conn.close()
                erro = 0
            except:
                erro = 1
                print("Erro = 1.")
        return 0
    except:
        print("Erro de execução da função: print_all_lines_from_db(db_name)")
        traceback.print_exc()
        return 0

def state_event():
    
    return json.dumps({"type": "state", **STATE})


def users_event():
    
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    
    USERS.remove(websocket)
    await notify_users()


async def handler(websocket, path):
    
    import logging
    import traceback
    
    logging.basicConfig(filename='server_log.log',level=logging.DEBUG)
    
    
    print("Logging and lib import okay!")
    print("")
    
    # Register.
    USERS.add(websocket)
    first_msg_flag = True
    key_value = ""
    print("Registration and flags initialization okay!")
    print("")
    
    try: # Processa
        print("Try 1.\n")
        while True:
            print("While True:\n")
        #async for recv_msg in websocket: # Pode trocar por while True:
            db_exist = os.path.isfile(db_name)
            recv_msg = await websocket.recv()
            if (recv_msg == "exit"):
                print("if exit\n")
                first_msg_flag = False
                greeting =  "Hello " + recv_msg
                await websocket.send(greeting)
                break
            elif (recv_msg == "xml_key" and first_msg_flag == True):
                print("elif xml_key and first = True")
                first_msg_flag = False
                key_value = recv_msg
                greeting =  "Hello " + recv_msg
                await websocket.send(greeting)
            elif (key_value == "xml_key" and first_msg_flag == False):
                print("elif xml_key and first = False")
                print("===  Loop XML  ===")
                print("")
                # 3 estados possíveis: Comando, último estado e enviar macro para o caminhão.
                greeting =  "Hello " + recv_msg
                await websocket.send(greeting)
            elif (recv_msg == "json_key" and first_msg_flag == True):
                print("elif json_key and first = True")
                first_msg_flag = False
                key_value = recv_msg
                greeting =  "Hello " + recv_msg
                await websocket.send(greeting)
            elif (key_value == "json_key" and first_msg_flag == False):  
                print("elif json_key and first = False")
                print("===  Loop JSON  ===")
                print("")
                print("recv_msg = ", recv_msg)  
                print("Inserting JSON to default DB.")
                try:
                    if (db_exist == False):
                        create_db(db_name)
                        print("Criou DB")
                        await asyncio.sleep(1)
                        row_recv = json_to_row(recv_msg)
                        print("Passou por row_recv.")
                        print("row_recv = ", row_recv)
                        insert_row_into_db(db_name, row_recv)
                        print("Passou por insert_row_into_db.")
                        print_all_lines_from_db(db_name)
                    elif(db_exist):
                        row_recv = json_to_row(recv_msg)
                        print("Passou por row_recv.")
                        print("row_recv = ", row_recv)
                        insert_row_into_db(db_name, row_recv)
                        print("Passou por insert_row_into_db.")
                        print_all_lines_from_db(db_name)
                    else:
                        print("Erro desconhecido: server_listen error.")
                except:
                    print("Erro ao tentar inserir JSON no Database.")
                    traceback.print_exc()            
            
                greeting =  "Hello " + recv_msg
            
                await websocket.send(greeting)
                print(greeting)
            else:
                print("Erro de conexão: Chave Inválida.")
                logging.error("Erro de conexão: Chave Inválida. Received: {}".format(recv_msg))
                break
        
        
        # Implement logic here.
        """await asyncio.wait([ws.send("Hello!") for ws in USERS])
        await asyncio.sleep(10)"""
    finally:
        # Unregister.
        await USERS.remove(websocket)


start_server = websockets.serve(handler, "0.0.0.0", 5005)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()