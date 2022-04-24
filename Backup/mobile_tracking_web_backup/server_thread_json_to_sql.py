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
import os

global db_name_1, db_name_2
db_name_1 = "telemetria.db"
db_name_2 = "macro.db"

USERS = set()

#truck = {'truck_id': 1, 'left door': 'opened', 'right door': 'closed', 'engine': 'ON', 'gps': [0.5,-0.5], 'speed': 100}

def create_db(db_name):
    
    if (db_name ==  db_name_1):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("""CREATE TABLE telemetria (
                     id text,
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
    if (db_name == db_name_2):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("""CREATE TABLE macro (
                     id text,
                     evento text,
                     timestamp int,
                     latitude real,
                     longitude real,
                     mensagem text
        )""")
        conn.commit()
        conn.close()

def insert_row_into_db(db_name,row):
    
    import traceback
    
    connect = False
    
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
        connect = True
        c = conn.cursor()
        #print("row_string = ",row_string)
        if (db_name == db_name_2):
            c.execute("""INSERT INTO macro VALUES (?, ?, ?, ?, ?, ?);""", (row[0], row[1], row[2], row[3], row[4], row[5]))
        else:
            c.execute("""INSERT INTO telemetria VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
        conn.commit()
        conn.close()
    except:
        print("Exception: Erro na função insert_row_into_db")
        traceback.print_exc()
        if connect:
            conn.close()
    return 0

def create_example_json():
    
    import json
    
    #truck = {'truck_id': 1,'left door': 'opened', 'right door': 'closed', 'engine': 'ON', 'gps': "[0.5,-0.5]", 'speed': 100}
    truck = {'id': "truck_1",'evento': "Telemetria",'timestamp': 0, 'data': {'rotacao': 0, 'porta': False, 'bau': False, 'janela': False, 'conectado': False, 'estaBloqueiado': False, 'bloqueiomanual': False, 'latitude': 1, 'longitude': 1}}
    example_json = json.dumps(truck)
    return example_json

def json_to_row(json_data):
    
    import json
    
    row = []
    
    dict_inst = json.loads(json_data)
    
    key = dict_inst['evento']
    
    """row.append(dict_inst["truck_id"])
    row.append(dict_inst["left door"])
    row.append(dict_inst["right door"])
    row.append(dict_inst["engine"])
    row.append(dict_inst["gps"])
    row.append(dict_inst["speed"])"""
    if (key == "Macro"):
        row.append(dict_inst['id']) #string
        row.append(dict_inst['evento']) #string
        row.append(dict_inst['timestamp']) #int
        row.append(dict_inst['data']['latitude']) #real
        row.append(dict_inst['data']['longitude']) #real
        row.append(dict_inst['data']['mensagem'])
    else:
        row.append(dict_inst['id']) #string
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
                nome_do_db = db_name[:-3]
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

async def server_listen(websocket, path):
    
    #from time import sleep
    import logging
    import traceback
    
    logging.basicConfig(filename='server_log.log',level=logging.DEBUG)
        
    while True:
        db_exist = (os.path.isfile(db_name_1) and os.path.isfile(db_name_2))
        recv_msg = await websocket.recv()
        if (recv_msg == "exit"):
            break
        print(recv_msg)  
        print("Inserting JSON to default DB.")
        try:
            if (db_exist == False):
                create_db(db_name_1)
                print("Criou DB Telemetria")
                create_db(db_name_2)
                print("Criou DB Macro")
                await asyncio.sleep(1)
                row_recv = json_to_row(recv_msg)
                print("Passou por row_recv.")
                print("row_recv = ", row_recv)
                if (row_recv[1] == "Macro"):
                    insert_row_into_db(db_name_2, row_recv)
                    print("Passou por insert_row_into_db.")
                    print_all_lines_from_db(db_name_2)
                else:
                    insert_row_into_db(db_name_1, row_recv)
                    print("Passou por insert_row_into_db.")
                    print_all_lines_from_db(db_name_1)
            elif(db_exist):
                row_recv = json_to_row(recv_msg)
                print("Passou por row_recv.")
                print("row_recv = ", row_recv)
                if (row_recv[1] == "Macro"):
                    insert_row_into_db(db_name_2, row_recv)
                    print("Passou por insert_row_into_db.")
                    print_all_lines_from_db(db_name_2)
                else:
                    insert_row_into_db(db_name_1, row_recv)
                    print("Passou por insert_row_into_db.")
                    print_all_lines_from_db(db_name_1)
            else:
                print("Erro desconhecido: server_listen error.")
        except:
            print("Erro ao tentar inserir JSON no Database.")
            traceback.print_exc()            
    
        greeting =  "Hello " + recv_msg
    
        await websocket.send(greeting)
        print(greeting)
    

start_server = websockets.serve(server_listen, "0.0.0.0", 5005)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
#print(json_to_row(create_example_json()))