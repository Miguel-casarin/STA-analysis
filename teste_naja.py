from najaeda import netlist

netlist.load_liberty(["Nangate45_typ.lib"])
top = netlist.load_verilog(["c17.v"])

for inst in top.get_child_instances():
    print(f"Instance: {inst.get_name()}")
    for term in inst.get_model().get_terms():
        print(f"  Pin: {term.get_name()} ({term.get_direction()})")

