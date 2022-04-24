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
import sys
from time import sleep

global db_name_1, db_name_2

script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
print(script_path)
sleep(1)
telemetria_name = "telemetria.db"
macro_name = "macro.db"
db_name_1 = os.path.join(script_path, telemetria_name)
db_name_2 = os.path.join(script_path, macro_name)
print(db_name_1)
print(db_name_2)

global command_buffer_dict # Guarda os comandos recebidos em um buffer p/ poder transmitir p/ Tablet.
global blocking_state_dict # Guarda o estado dos caminhões com base na comparação entre BD e ultimo comando.
command_buffer_dict = {}
blocking_state_dict = {}


USERS = set()

#truck = {'truck_id': 1, 'left door': 'opened', 'right door': 'closed', 'engine': 'ON', 'gps': [0.5,-0.5], 'speed': 100}

def create_db(db_name):
    
    if (db_name ==  db_name_1):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("""CREATE TABLE telemetria (
                     truck_id text,
                     evento text,
                     timestamp int,
                     latitude real,
                     longitude real,
                     accuracy real,
                     conectado int,
                     atualizado int,
                     acelerador int,
                     embreagem int,
                     rotacao real,
                     pedal real,
                     temperatura_agua real,
                     pedal_freio_1 int,
                     pedal_freio_2 int,
                     cruise_control int,
                     epc int,
                     ac_on_off int,
                     consumo_combustivel real,
                     torque real,
                     velocidade_fina real,
                     marcha int,
                     pedal_embreagem int,
                     pedal_freio int,
                     modo_cruzeiro int,
                     pedal_sim int,
                     ref_cruzeiro real,
                     erro_hardware int,
                     freio_est int,
                     luz_bateria int,
                     tanque real,
                     reserva int,
                     velocidade_grosso real,
                     temp_ambiente_delay real,
                     temp_ambiente real,
                     temp_oleo real,
                     temp_agua real,
                     hodometro int,
                     seta_esquerda int,
                     seta_direita int,
                     pisca_alerta int,
                     re int,
                     porta_motorista int,
                     porta_passageiro int,
                     porta_te int,
                     porta_td int,
                     capo int,
                     porta_malas int,
                     backlight int,
                     estaBloqueiado int,
                     bloqueiomanual int                     
        )""")
        conn.commit()
        conn.close()
    if (db_name == db_name_2):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("""CREATE TABLE macro (
                     truck_id text,
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
    
    try:
        conn = sqlite3.connect(db_name)
        connect = True
        c = conn.cursor()
        #print("row_string = ",row_string)
        if (db_name == db_name_2):
            c.execute("""INSERT INTO macro VALUES (?, ?, ?, ?, ?, ?);""", (row[0], row[1], row[2], row[3], row[4], row[5]))
        elif (db_name == db_name_1):
            c.execute("""INSERT INTO telemetria VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37], row[38], row[39], row[40], row[41], row[42], row[43], row[44], row[45], row[46], row[47], row[48], row[49], row[50]))
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
    import time
    
    #truck = {'truck_id': 1,'left door': 'opened', 'right door': 'closed', 'engine': 'ON', 'gps': "[0.5,-0.5]", 'speed': 100}
    #truck = {'id': "truck_1",'evento': "Telemetria",'timestamp': 0, 'data': {'rotacao': 0, 'porta': False, 'bau': False, 'janela': False, 'conectado': False, 'estaBloqueiado': False, 'bloqueiomanual': False, 'latitude': 1, 'longitude': 1}}
    truck = {"truck_id":"truck_1","evento":"Telemetria","timestamp": round(time.time(), 0),"data":{"latitude":-23.5709292,"longitude":-46.744901,"conectado":True,"atualizado":True,"acelerador":0,"embreagem":1,"rotacao":3500,"pedal":222,"temperatura_agua":24,"pedal_freio_1":1,"pedal_freio_2":1,"cruise_control":1,"epc":1,"ac_on_off":1,"consumo_combustivel":329,"torque":23.72,"velocidade_fina":112.55,"marcha":2,"pedal_embreagem":0,"pedal_freio":0,"modo_cruzeiro":0,"pedal_sim":1,"ref_cruzeiro":73,"erro_hardware":26,"freio_est":1,"luz_bateria":1,"tanque":100,"reserva":1,"velocidade_grosso":100,"temp_ambiente_delay":54,"temp_ambiente":35,"temp_oleo":30,"temp_agua":27,"hodometro":1278523,"seta_esquerda":1,"seta_direita":1,"pisca_alerta":1,"re":0,"porta_motorista":0,"porta_passageiro":1,"porta_te":1,"porta_td":1,"capo":1,"porta_malas":1,"backlight":62}}
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
        row.append(dict_inst['truck_id']) #string
        row.append(dict_inst['evento']) #string
        row.append(dict_inst['timestamp']) #int
        row.append(dict_inst['data']['latitude']) #real
        row.append(dict_inst['data']['longitude']) #real
        row.append(dict_inst['data']['mensagem'])
    else:
        row.append(dict_inst['truck_id']) #string
        row.append(dict_inst['evento']) #string
        row.append(dict_inst['timestamp']) #int
        row.append(dict_inst['data']['latitude']) #real
        row.append(dict_inst['data']['longitude']) #real
        row.append(dict_inst['data']['accuracy']) #float
        row.append(dict_inst['data']['conectado']) #boolean
        row.append(dict_inst['data']['atualizado']) #boolean
        row.append(dict_inst['data']['acelerador']) #boolean
        row.append(dict_inst['data']['embreagem']) #boolean
        row.append(dict_inst['data']['rotacao']) #float
        row.append(dict_inst['data']['pedal']) #float
        row.append(dict_inst['data']['temperatura_agua'])
        row.append(dict_inst['data']['pedal_freio_1'])
        row.append(dict_inst['data']['pedal_freio_2'])
        row.append(dict_inst['data']['cruise_control'])
        row.append(dict_inst['data']['epc'])
        row.append(dict_inst['data']['ac_on_off'])
        row.append(dict_inst['data']['consumo_combustivel'])
        row.append(dict_inst['data']['torque'])
        row.append(dict_inst['data']['velocidade_fina'])
        row.append(dict_inst['data']['marcha'])
        row.append(dict_inst['data']['pedal_embreagem'])
        row.append(dict_inst['data']['pedal_freio'])
        row.append(dict_inst['data']['modo_cruzeiro'])
        row.append(dict_inst['data']['pedal_sim'])
        row.append(dict_inst['data']['ref_cruzeiro'])
        row.append(dict_inst['data']['erro_hardware'])
        row.append(dict_inst['data']['freio_est'])
        row.append(dict_inst['data']['luz_bateria'])
        row.append(dict_inst['data']['tanque'])
        row.append(dict_inst['data']['reserva'])
        row.append(dict_inst['data']['velocidade_grosso'])
        row.append(dict_inst['data']['temp_ambiente_delay'])
        row.append(dict_inst['data']['temp_ambiente'])
        row.append(dict_inst['data']['temp_oleo'])
        row.append(dict_inst['data']['temp_agua'])
        row.append(dict_inst['data']['hodometro'])
        row.append(dict_inst['data']['seta_esquerda'])
        row.append(dict_inst['data']['seta_direita'])
        row.append(dict_inst['data']['pisca_alerta'])
        row.append(dict_inst['data']['re'])
        row.append(dict_inst['data']['porta_motorista'])
        row.append(dict_inst['data']['porta_passageiro'])
        row.append(dict_inst['data']['porta_te'])
        row.append(dict_inst['data']['porta_td'])
        row.append(dict_inst['data']['capo'])
        row.append(dict_inst['data']['porta_malas'])
        row.append(dict_inst['data']['backlight'])
        row.append(dict_inst['data']['estaBloqueiado'])
        row.append(dict_inst['data']['bloqueiomanual'])        
    
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
                #nome_do_db = db_name[:-3]
                if ("telemetria" in db_name):
                    nome_da_tabela = "telemetria"
                elif ("macro" in db_name):
                    nome_da_tabela = "macro"
                else:
                    nome_da_tabela = "telemetria"
                    print("[Error] Nome do db não contem palavras 'telemetria' ou 'macro'.")
                c.execute("""SELECT *
                             FROM %s""" % nome_da_tabela)
                print(c.fetchall())
                print('\n')
                conn.commit()
                conn.close()
                erro = 0
            except:
                traceback.print_exc()
                erro = 1
                print("Erro = 1.")
                break
        return 0
    except:
        print("Erro de execução da função: print_all_lines_from_db(db_name)")
        traceback.print_exc()
        return 0

async def server_listen(websocket, path):
    
    #from time import sleep
    import logging
    import traceback
    import json
    
    logging.basicConfig(filename='server_log.log',level=logging.DEBUG)

    while True:

        recv_msg = await websocket.recv() # Espera JSON p/ iniciar thread.

        try: # Checa se é JSON
            recv_msg_dict = json.loads(recv_msg)
            truck_id_name = recv_msg_dict['truck_id']
            try:
                if (blocking_state_dict[truck_id_name] == 0 or blocking_state_dict == 1):
                    print("")
                    print("blocking_state_dict já existente.")
                    print("")
            except:
                blocking_state_dict[truck_id_name] = 0
                print("")
                print("blocking_state_dict = ", blocking_state_dict)
                print("")
            print("truck_id = ", truck_id_name)
        except:
            print("[Critical Error] Unable to convert received data to dict format. Closing socket...")
            traceback.print_exc()
            break

        if (recv_msg_dict["evento"] == "comando"): # Se for um comando
            truck_id_name = recv_msg_dict['truck_id']
            command_buffer_dict[truck_id_name] = recv_msg_dict
            blocking_state_dict[truck_id_name] = recv_msg_dict['data']['command_id']
            print("command_buffer_dict = ", command_buffer_dict)
            print("blocking_state_dict = ", blocking_state_dict)
        else:
            db_exist = (os.path.isfile(db_name_1) and os.path.isfile(db_name_2))
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
                        #print_all_lines_from_db(db_name_2)
                    else:
                        insert_row_into_db(db_name_1, row_recv)
                        print("Passou por insert_row_into_db.")
                        #print_all_lines_from_db(db_name_1)
                elif(db_exist):
                    row_recv = json_to_row(recv_msg)
                    print("Passou por row_recv.")
                    print("row_recv = ", row_recv)
                    if (row_recv[1] == "Macro"):
                        insert_row_into_db(db_name_2, row_recv)
                        print("Passou por insert_row_into_db.")
                        #print_all_lines_from_db(db_name_2)
                    else:
                        insert_row_into_db(db_name_1, row_recv)
                        print("Passou por insert_row_into_db.")
                        #print_all_lines_from_db(db_name_1)
                else:
                    print("Erro desconhecido: server_listen error.")
            except:
                print("Erro ao tentar inserir JSON no Database.")
                traceback.print_exc()            
        
        #greeting =  "Hello " + recv_msg
        
        """await websocket.send(greeting)
        print(greeting)
        print("")"""
        greeting = str(blocking_state_dict[truck_id_name])
        print("Enviando vetor de estados: ", blocking_state_dict)
        await websocket.send(greeting)
        print("Enviou: ", blocking_state_dict)
    print("Socket closed.")
    

start_server = websockets.serve(server_listen, "0.0.0.0", 5005)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
#print(json_to_row(create_example_json()))