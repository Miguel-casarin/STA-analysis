read_liberty ed_Nangate.lib
read_verilog ripplecarry2b.v
link_design ripple_adder

create_clock -name virt_clk -period 1.1

set_input_delay 0 -clock virt_clk [get_ports {
	a b
}]

set_output_delay 1 -clock virt_clk [get_ports {
	s cout
}]

report_checks -path_delay max -group_count 2
