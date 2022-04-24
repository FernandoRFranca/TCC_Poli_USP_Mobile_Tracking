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
db_name_1 = script_path + "\\" + telemetria_name
db_name_2 = script_path + "\\" + macro_name
print(db_name_1)
print(db_name_2)
USERS = set()

def add_query_results_to_dict(rows_vec):
    if (rows_vec[0][1] == "Telemetria"):
        dict_struct = {
            'truck_id': rows_vec[0][0],
            'evento': rows_vec[0][1],
            'timestamp': rows_vec[0][2],
            'rotacao': rows_vec[0][3],
            'porta': rows_vec[0][4],
            'bau': rows_vec[0][5],
            'janela': rows_vec[0][6],
            'conectado': rows_vec[0][7],
            'estaBloqueiado': rows_vec[0][8],
            'bloqueiomanual': rows_vec[0][9],
            'latitude': rows_vec[0][10],
            'longitude': rows_vec[0][11]
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
        SELECT truck_id, evento, max(timestamp), rotacao, porta, bau, janela, conectado, estaBloqueiado, bloqueiomanual, latitude, longitude 
        FROM telemetria 
        WHERE 1=1 
        AND timestamp is not NULL""").fetchall()
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