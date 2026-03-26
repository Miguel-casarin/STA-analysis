import os 

def find_base_line(designs_path):
    # Guarda os circuitos base line 
    originals = []

    files = os.listdir(designs_path)
    for file in files:
        id = file.split("_")[0]
        if set(id) == {"0"}:
            print(f"FILE {file} ad to base line")
            originals.append(file)

    return originals