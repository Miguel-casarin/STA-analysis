import sqlite3 as s

db_name = f"sta.db"

def make_db(name):
    conection = s.connect(db_name)

    # Conecta com o banco
    cursor = conection.cursor()

    create_cells_info = """
        CREATE TABLE CELLS_INFO (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT,
            design TEXT,
            cell TEXT,
            type TEXT,
            size TEXT,
            delay FLOAT,
            time FLOAT,
            path INTEGER
        );
    """

    create_path_info = """
        CREATE TABLE PATH_INFO (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT,
            design TEXT,
            path INTEGER,
            startpoint TEXT,
            endpoint TEXT,
            slack FLOAT,
            arival FLOAT
        );
    """

    create_features_design = """
        CREATE TABLE FEATURES_DESIGNS (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT,
            design TEXT,
            cell TEXT,
            fain INTEGER,
            faout INTEGER,
            nl INTEGER,
            deep INTEGER
        );
"""

    cursor.execute(create_cells_info)
    cursor.execute(create_path_info)
    cursor.execute(create_features_design)
    cursor.close()
    
    print(f"DB {name} created")

make_db(db_name)