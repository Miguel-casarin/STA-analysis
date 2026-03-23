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
            path INTEGER,
            startpoint TEXT,
            endpoint TEXT,
            slack FLOAT,
            arival FLOAT
        );
    """

    cursor.execute(create_cells_info)
    cursor.execute(create_path_info)
    cursor.close()

    print(f"DB {name} created")

make_db(db_name)