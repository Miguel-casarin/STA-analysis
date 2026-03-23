import sqlite3 as sql
import re
import os

import dir
import ext_data

# Puxa os arquivos do diretorio
desins_path = "out_c17/"
files = dir.get_files(desins_path)

# conecta o banco
sta_db = sql.connect("sta.db")
cursor = sta_db.cursor()


def inset_cells_info(id, cell, cell_type, size, delay, time, path):
    cursor.execute(
        """
        INSERT INTO CELLS_INFO (id, cell, type, size, delay, time, path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (id, cell, cell_type, size, delay, time, path),
    )
    sta_db.commit()


def insert_path_info(id, path, startpoint, endpoint, slack, arrival):
    cursor.execute(
        """
        INSERT INTO PATH_INFO (id, path, startpoint, endpoint, slack, arival)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (id, path, startpoint, endpoint, slack, arrival),
    )
    sta_db.commit()


def get_circuit_id(filename: str):
    m = re.search(r"(\d+)(?=\.txt$)", filename)
    if m:
        return m.group(1)
    return None


# Loop principal: para cada arquivo de STA
for design in files:
    full_path = os.path.join(desins_path, design)
    circuit_id = get_circuit_id(design)
    if circuit_id is None:
        continue  

    rt = ext_data.Read_timing(full_path)

    cells = rt.get_cells()
    slacks = rt.get_slack()
    arrivals = rt.get_arrival_times()
    startpoints = rt.get_startpint()
    endpoints = rt.get_endpoint()

    # path_id é o índice do caminho crítico 
    for path_id in sorted(cells.keys()):
        path_num = path_id  

        sp = startpoints.get(path_id, [{}])[0].get("startpoint")
        ep = endpoints.get(path_id, [{}])[0].get("endpoint")
        sl = slacks.get(path_id, [{}])[0].get("slack")
        arr = arrivals.get(path_id)

        # Insere uma linha em PATH_INFO para este caminho
        insert_path_info(
            id=circuit_id,
            path=path_num,
            startpoint=sp,
            endpoint=ep,
            slack=sl,
            arrival=arr,
        )

        # Insere uma linha em CELLS_INFO para cada célula deste caminho
        for c in cells[path_id]:
            inset_cells_info(
                id=circuit_id,
                cell=c["cell_id"],
                cell_type=c["type"],
                size=c["size"],
                delay=c["ac_delay"],
                time=c["time"],
                path=path_num,
            )

sta_db.close()
