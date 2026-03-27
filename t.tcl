read_liberty circuitLibrays/ed_Nangate.lib
read_verilog inputs/63__c17__X2.v
link_design c17

create_clock -name virt_clk -period 1.1
set_driving_cell -lib_cell BUF_X4 [all_inputs]
set_load 1.140290 [all_outputs]
set_input_delay 0 -clock virt_clk [get_ports {N1 N2 N3 N6 N7}]

set_output_delay 1 -clock virt_clk [get_ports {N22 N23}]

report_checks -digits 5 -path_delay max -group_count 2

exit

