import dir
import os
import re

deigns_path = 'out_c17/'
files = dir.get_files(deigns_path)

class Read_timing:
    def __init__(self, sta_file):
        self.sta_file = sta_file 
    
    def get_slack(self):
        pcritic_id = 0
        result = {}

        pattern_slack = re.compile(r"^\s*([+-]?\d+\.\d+)\s+slack\b")

        with open(self.sta_file, "r") as f:
            for line in f:
                line.strip()

                if line.startswith("Startpoint"):
                    pcritic_id +=1

                    result[pcritic_id] = []

                match = pattern_slack.search(line)
                if match and pcritic_id > 0:
                    slack = float(match.group(1))  
                    result[pcritic_id].append({
                        "slack": slack
                    })
        return result
    
    def get_arrival_times(self):
        arrivals = {}
        path_id = 0
        current_arrival = None
        inside_path = False

        with open(self.sta_file, "r") as f:
            for line in f:
                line = line.strip()

                if line.startswith("Startpoint:"):
                    # salva o caminho anterior
                    if current_arrival is not None:
                        arrivals[path_id] = current_arrival

                    path_id += 1
                    current_arrival = None
                    inside_path = True

                elif "data arrival time" in line and inside_path:
                    if current_arrival is None:  # pega só o primeiro
                        value = float(line.split()[0])
                        if value > 0:
                            current_arrival = value

            # salva o último caminho
            if current_arrival is not None:
                arrivals[path_id] = current_arrival

        return arrivals

    def get_startpint(self):
        pcritic_id = 0
        result = {}

        pattern_stp = re.compile(r"Startpoint:\s+(\S+)")

        with open(self.sta_file, "r") as f:
            for line in f:
                line.strip()

                if line.startswith("Startpoint"):
                    pcritic_id +=1
                    result[pcritic_id] = []

                    match = pattern_stp.search(line)
                    if match and pcritic_id > 0:
                        start_point = match.group(1)
                        result[pcritic_id].append({
                            "startpoint": start_point
                        })
        return result

    def get_endpoint(self):
        pcritic_id = 0
        result = {}

        parthen_end = re.compile(r"Endpoint:\s+(\S+)")

        with open(self.sta_file, "r") as f:
            for line in f:
                line.strip()

                if line.startswith("Startpoint"):
                    pcritic_id += 1

                    result[pcritic_id] = []

                match = parthen_end.search(line)
                if match and pcritic_id > 0:
                    end = match.group(1)
                    result[pcritic_id].append({
                        "endpoint": end
                    })
        return result
    
    # Retorna um dicionario com: id, delay ac, tipo e size
    def get_cells(self):
        pcritic_id = 0
        result = {}

        pattern_cells = re.compile(
            r"^\s*([\d\.]+)\s+([\d\.]+)\s+[v\^]\s+(_\d+_)/\S+\s+\(([A-Z]+)\d*_?(X\d+)\)"
        ) 
        
        with open(self.sta_file, "r") as f:
            for line in f:
                line.strip()

                # Diferencia os caminhos criticos
                if line.startswith("Startpoint"):
                    pcritic_id += 1 # Id do caminho critico

                    result[pcritic_id] = []
                
                match = pattern_cells.search(line)
                if match and pcritic_id > 0:
                    delay = float(match.group(1))
                    s_time = float(match.group(2))
                    id_cell = match.group(3)
                    cell_type = match.group(4)
                    cell_size = match.group(5)

                    result[pcritic_id].append({
                        "cell_id": id_cell,
                        "type": cell_type,
                        "size": cell_size,
                        "ac_delay": delay,
                        "time": s_time
                    })
        return result
        
    
#file = f"000000.txt"

""""
debug = Read_timing(file)
cells = debug.get_cells()
slack = debug.get_slack()
arival = debug.get_arrival_times()
start_point = debug.get_startpint()
end_point = debug.get_endpoint()
"""

def debug(sta_file):
    rt = Read_timing(sta_file)

    cells       = rt.get_cells()
    slack       = rt.get_slack()
    arrivals    = rt.get_arrival_times()
    startpoints = rt.get_startpint()
    endpoints   = rt.get_endpoint()

    for cid in sorted(cells.keys()):
        print(f"\n=== Caminho crítico {cid} ===")
        sp = startpoints.get(cid, [{}])[0].get("startpoint", "-")
        ep = endpoints.get(cid, [{}])[0].get("endpoint", "-")
        sl = slack.get(cid, [{}])[0].get("slack", "-")
        arr = arrivals.get(cid, "-")

        print(f"Startpoint : {sp}")
        print(f"Endpoint   : {ep}")
        print(f"Slack      : {sl}")
        print(f"Arrival    : {arr}")
        print("Células:")
        for c in cells[cid]:
            print(
                f"  {c['cell_id']}  {c['type']}{c['size']}  "
                f"delay={c['ac_delay']}  time={c['time']}"
            )
        print("-" * 40)

for sta_file in files:
    full_path = os.path.join(deigns_path, sta_file)
    print("_" * 50)
    print(f"{sta_file}")
    print("_" * 50)
    debug(full_path)