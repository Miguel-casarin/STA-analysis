read_liberty ed_Nangate.lib
read_verilog c17.v
link_design c17

create_clock -name virt_clk -period 1.1

set_input_delay 0 -clock virt_clk [get_ports {
	N1 N2 N3 N6 N7
}]

set_output_delay 1 -clock virt_clk [get_ports {
	N22 N23
}]

report_checks -path_delay max -group_count 2
