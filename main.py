import subprocess 
import re
import os 

import read_v
import ed_tcl
import dir

file_tcl = "t.tcl"
dir_circuits = 'c17/'
dir_out = 'out_c17/'

circuits = dir.get_files(dir_circuits)

def name_str(string):
    id = re.match(r'^([^_]+)', string)

    if id:
        return id.group(1)

def open_sta(tcl_script, n_save, out_dir):
    n_save = f"{n_save}.txt"
    output_path = os.path.join(out_dir, n_save)

    with open(output_path, "w") as f:
          subprocess.run(
            ["sta", tcl_script],
            stdout=f,
            stderr=subprocess.STDOUT,  # STDOUT serve para mostrar os erros
            text=True
        )

for circuit in circuits:
    file_verilog = f"{circuit}"   

    verilog_reader = read_v.Get_IO(file_verilog, dir_circuits)

    module_design = verilog_reader.verilog_module()
    inputs_sinals = verilog_reader.get_inputs()
    outputs_signals = verilog_reader.get_outputs()
    cells_name = verilog_reader.gat_cells_ids()

    number_paths = ed_tcl.number_outputs(outputs_signals)

    design_path = f"{dir_circuits}{file_verilog}"

    script_sta = ed_tcl.Edit_tcl(
        file_tcl,        
        design_path,     
        module_design,   
        number_paths,    
        inputs_sinals,   
        outputs_signals  
    )

    script_sta.ed_device()
    script_sta.link_design()
    script_sta.paths_total()
    script_sta.parse_inputs()
    script_sta.parse_outputs()

    name_txt = name_str(file_verilog)
    print(f"TXT name {name_txt}")

    try:
        open_sta(file_tcl, name_txt, dir_out)
        print(f"Circuit {file_verilog} analyzes in STA")
    
    except:
        print("Erro to run OpenSTA")
        
    