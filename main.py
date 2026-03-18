import read_v
import ed_tcl


file_verilog = "c17.v"
file_tcl = "t.tcl"

verilog_reader = read_v.Get_IO(file_verilog)

# chama os métodos, em vez de guardar a referência
module_design = verilog_reader.verilog_module()
inputs_sinals = verilog_reader.get_inputs()
outputs_signals = verilog_reader.get_outputs()
cells_name = verilog_reader.gat_cells_ids()

# agora outputs_signals é uma lista, como a função espera
number_paths = ed_tcl.number_outputs(outputs_signals)

script_sta = ed_tcl.Edit_tcl(
    file_tcl,        # tcl_file
    file_verilog,    # design (arquivo verilog)
    module_design,   # link_device (nome do módulo verilog)
    number_paths,    # número de caminhos
    inputs_sinals,   # lista de inputs
    outputs_signals  # lista de outputs
)

# se quiser realmente editar o t.tcl, chame os métodos:
script_sta.ed_device()
script_sta.link_design()
script_sta.paths_total()
script_sta.parse_inputs()
script_sta.parse_outputs()
