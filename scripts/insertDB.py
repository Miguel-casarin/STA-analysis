import sqlite3 as sql
import re
import os

from scripts import dir
from scripts import ext_data
from scripts import getBase
from scripts import getFeatures
from scripts import getDesign

# Puxa os arquivos do diretorio
desins_path = "staOutputs/"
files = dir.get_files(desins_path)

# Diretorio para buscar o base line 
dir_circuits = 'inputs/'
dir_lib ='circuitLibrays/ed_Nangate.lib'
baselines = getBase.find_base_line(dir_circuits)

# conecta o banco
sta_db = sql.connect("sta.db")
cursor = sta_db.cursor()


def inset_cells_info(id, design, cell, cell_type, size, delay, time, path):
    cursor.execute(
        """
        INSERT INTO CELLS_INFO (id, design, cell, type, size, delay, time, path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (id, design, cell, cell_type, size, delay, time, path),
    )

    print(f"ADDING TO CELLS_INFO: \n{id} {design} {cell} {cell_type} {size} {delay} {time} {path}\n")
    sta_db.commit()


def insert_path_info(id, design, path, startpoint, endpoint, slack, arrival):
    cursor.execute(
        """
        INSERT INTO PATH_INFO (id, path, startpoint, endpoint, slack, arival)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (id, design, path, startpoint, endpoint, slack, arrival),
    )

    print(f"ADDING TO PATH_INFO: \n{id} {design} {path} {startpoint} {endpoint} {slack} {arrival} \n")
    sta_db.commit()

def insert_features(id, design, cell, fain, faout, nl, deep):
    cursor.execute(
        """
        INSERT INTO FEATURES_DESIGNS (id, design, cell, fain, faout, nl, deep)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (id, design, cell, fain, faout, nl, deep),
    )
    print(f"ADDING TO FEATURES_DESIGNS: \n{id} {design} {cell} {fain} {faout} {nl} {deep}\n")
    sta_db.commit()







# Aqui ta o erro de inserção e de pular arquivos de sizes distintos
# O lop percorre os primeiros caracteries do nome do arquivo ignora os diferentes sizes pq seus caracteries são iguais
# essa parte precisa ser refatorada para considerar id_design_size









# Primeira parte do nome do arquivo 
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
# Inserindo os base lines 
for design in baselines:
    print(f"Baseline: {design}")

    verilog_path = os.path.join(dir_circuits, design)
    
    circuit_id = design.split("__", 1)[0]   

    
    features = getFeatures.Circuits_features(verilog_path, dir_lib)
    fanin = features.fan_in()                # dict: cell -> fan_in
    fanout = features.fan_out()              # dict: cell -> fan_out
    logic_level = features.compute_logic_levels()  # dict: cell -> nl
    deep = features.comput_deep()            # dict: cell -> deep

    # insere uma linha por célula
    for cell_name in fanin.keys():
        f_in = fanin.get(cell_name, 0)
        f_out = fanout.get(cell_name, 0)
        nl = logic_level.get(cell_name)
        dp = deep.get(cell_name)

        insert_features(
            id=circuit_id,
            cell=cell_name,
            fain=f_in,
            faout=f_out,
            nl=nl,
            deep=dp,
        )

    
sta_db.close()
