from najaeda import netlist

netlist.reset()
netlist.load_liberty(["Nangate45_typ.lib"])
top = netlist.load_verilog(["c17.v"])

# every terminal of every cell of TOP
for inst in top.get_child_instances():
    print(f"Instance: {inst.get_name()}")
    for term in inst.get_terms():
        print(f"  Pin: {term.get_name()} ({term.get_direction()})")
        print(f"    Net: {term.get_upper_net().get_name()}")

print("---")

# every port of TOP
for term in top.get_terms():
    print(f"  Pin: {term.get_name()} ({term.get_direction()})")
    print(f"    Net: {term.get_lower_net().get_name()}")

# graphviz visualizer from example 3
top.dump_full_dot(f"{top.get_name()}.dot")
# show graph with:
#   dot -Tpng c17.dot -o c17.png
# and then open the png
