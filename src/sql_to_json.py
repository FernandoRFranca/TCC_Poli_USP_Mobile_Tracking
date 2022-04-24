import asyncio
import websockets
import sqlite3
import os
import sys
import json
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
USERS = set()

def add_query_results_to_dict(rows_vec):
    if (rows_vec[0][1] == "Telemetria" or rows_vec[0][1] == "changeLocation"):
        dict_struct = {
            'truck_id': rows_vec[0][0],
            'evento': rows_vec[0][1],
            'timestamp': rows_vec[0][2],
            'latitude': rows_vec[0][3],
            'longitude': rows_vec[0][4],
            'accuracy': rows_vec[0][5],
            'conectado': rows_vec[0][6],
            'atualizado': rows_vec[0][7],
            'acelerador': rows_vec[0][8],
            'embreagem': rows_vec[0][9],
            'rotacao': rows_vec[0][10],
            'pedal': rows_vec[0][11],
            'temperatura_agua': rows_vec[0][12],
            'pedal_freio_1': rows_vec[0][13],
            'pedal_freio_2': rows_vec[0][14],
            'cruise_control': rows_vec[0][15],
            'epc': rows_vec[0][16],
            'ac_on_off': rows_vec[0][17],
            'consumo_combustivel': rows_vec[0][18],
            'torque': rows_vec[0][19],
            'velocidade_fina': rows_vec[0][20],
            'marcha': rows_vec[0][21],
            'pedal_embreagem': rows_vec[0][22],
            'pedal_freio': rows_vec[0][23],
            'modo_cruzeiro': rows_vec[0][24],
            'pedal_sim': rows_vec[0][25],
            'ref_cruzeiro': rows_vec[0][26],
            'erro_hardware': rows_vec[0][27],
            'freio_est': rows_vec[0][28],
            'luz_bateria': rows_vec[0][29],
            'tanque': rows_vec[0][30],
            'reserva': rows_vec[0][31],
            'velocidade_grosso': rows_vec[0][32],
            'temp_ambiente_delay': rows_vec[0][33],
            'temp_ambiente': rows_vec[0][34],
            'temp_oleo': rows_vec[0][35],
            'temp_agua': rows_vec[0][36],
            'hodometro': rows_vec[0][37],
            'seta_esquerda': rows_vec[0][38],
            'seta_direita': rows_vec[0][39],
            'pisca_alerta': rows_vec[0][40],
            're': rows_vec[0][41],
            'porta_motorista': rows_vec[0][42],
            'porta_passageiro': rows_vec[0][43],
            'porta_te': rows_vec[0][44],
            'porta_td': rows_vec[0][45],
            'capo': rows_vec[0][46],
            'porta_malas': rows_vec[0][47],
            'backlight': rows_vec[0][48],
            'estaBloqueiado': rows_vec[0][49],
            'bloqueiomanual': rows_vec[0][50]
        }
        return dict_struct
    elif (rows_vec[0][1] == "Macro"):
        dict_struct = {
            'truck_id': rows_vec[0][0],
            'evento': rows_vec[0][1],
            'timestamp': rows_vec[0][2],
            'latitude': rows_vec[0][3],
            'longitude': rows_vec[0][4],
            'mensagem': rows_vec[0][5]
        }
        return dict_struct
    else:
        return 0

def get_json_from_db(db_name):
    if (db_name == db_name_1):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        rows = c.execute("""
        SELECT truck_id, evento, max(timestamp), latitude, longitude, accuracy, conectado, atualizado, acelerador, embreagem, rotacao, pedal, temperatura_agua, pedal_freio_1, pedal_freio_2, cruise_control, epc, ac_on_off, consumo_combustivel, torque, velocidade_fina, marcha, pedal_embreagem, pedal_freio, modo_cruzeiro, pedal_sim, ref_cruzeiro, erro_hardware, freio_est, luz_bateria, tanque, reserva, velocidade_grosso, temp_ambiente_delay, temp_ambiente, temp_oleo, temp_agua, hodometro, seta_esquerda, seta_direita, pisca_alerta, re, porta_motorista, porta_passageiro, porta_te, porta_td, capo, porta_malas, backlight, estaBloqueiado, bloqueiomanual
        FROM telemetria 
        WHERE 1=1 
        AND timestamp is not NULL
        AND evento in ('changeLocation')""").fetchall()
        print(rows)
        dict_struct = add_query_results_to_dict(rows)
        conn.commit()
        conn.close()
        return json.dumps(dict_struct) #CREATE JSON
    elif (db_name == db_name_2):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        rows = c.execute("""
        SELECT truck_id, evento, max(timestamp), latitude, longitude, mensagem 
        FROM macro 
        WHERE 1=1 
        AND timestamp is not NULL""").fetchall()
        print(rows)
        dict_struct = add_query_results_to_dict(rows)
        print(dict_struct)
        conn.commit()
        conn.close()
        return json.dumps(dict_struct) #CREATE JSON
    else:
        print("Erro de consulta SQL. Retornando 0.")
        return 0

async def server_listen(websocket, path):
    

    import logging
    import traceback
    from asyncio import sleep
    
    logging.basicConfig(filename='server_log2.log',level=logging.DEBUG)
        
    while True:
        request_msg = await websocket.recv()
        await sleep(1)
        if (request_msg == "macro"):
            try:
                json_to_client = get_json_from_db(db_name_2)
                try:
                    int_test = int(json_to_client)
                    print("int_test = ", int_test)
                    print("[Warning] Não enviado pois vetor contém None.")
                    logging.info("[Warning] Não enviado pois vetor contém None.")
                except:
                    try:
                        await websocket.send(json_to_client)
                        print("JSON enviado com sucesso.")
                    except:
                        logging.error("Erro ao tentar enviar JSON para o Javascript no Browser. Error ID: 2")
                        print("Erro ao tentar enviar JSON para o Javascript no Browser. Error ID: 2")
                        traceback.print_exc()
            except:
                print("request_msg = macro")
                print("Erro ao tentar enviar JSON para o Javascript no Browser. Error ID: 1")
                traceback.print_exc()
                logging.error(traceback.print_exc())
        elif (request_msg == "telemetria"):
            try:
                json_to_client = get_json_from_db(db_name_1)
                await websocket.send(json_to_client)
                print("JSON enviado com sucesso.")
            except:
                print("request_msg = telemetria")
                print("Erro ao tentar enviar JSON para o Javascript no Browser.")
                traceback.print_exc()
                logging.error(traceback.print_exc())
        elif (request_msg["evento"] == "comando"):
            try:
                pass # Parei aqui!!
            except:
                pass
        else:
            print("Recebeu request_msg invalida.")
            logging.error("Recebeu request_msg invalida.")
    
        greeting =  "Request: " + request_msg
    
        #await websocket.send(greeting)
        print(greeting)
    

start_server = websockets.serve(server_listen, "0.0.0.0", 5004)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
#print(json_to_row(create_example_json()))