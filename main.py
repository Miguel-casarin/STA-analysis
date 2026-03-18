import read_v
import ed_tcl
import dir

file_tcl = "t.tcl"
dir_circuits = 'c17/'

circuits = dir.get_files(dir_circuits)

for circuit in circuits:
    file_verilog = f"{circuit}"   

    # passa também o diretório para o Get_IO
    verilog_reader = read_v.Get_IO(file_verilog, dir_circuits)

    module_design = verilog_reader.verilog_module()
    inputs_sinals = verilog_reader.get_inputs()
    outputs_signals = verilog_reader.get_outputs()
    cells_name = verilog_reader.gat_cells_ids()

    number_paths = ed_tcl.number_outputs(outputs_signals)

    # caminho completo para escrever no t.tcl
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
