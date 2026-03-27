import re
import shutil
import os

# Parâmetros padrão (podem ser alterados aqui)
file = "c17.v"
output_dir = "../inputs"
saved_name = file.split(".")[0]
size = 4

class Extract_info:
    def __init__(self, file, start_block, end_block, process_line):
        self.input_file = file
        self.start_block = start_block  
        self.end_block = end_block
        self.process_line = process_line
        self.cells = []

    def read_block(self):
        if not self.start_block:
            raise ValueError("start_block (module name) is None/empty")

        in_block = False
        start_re = re.compile(rf"^\s*module\s+{re.escape(self.start_block)}\b")

        with open(self.input_file, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue

                if not in_block:
                    if start_re.match(s):
                        in_block = True
                    continue

                if s == self.end_block:
                    break

                result = self.process_line(s)
                if result:
                    self.cells.append(result)

class Edit_verilog:
    def __init__(self, original_file, output_dir):
        self.original_file = original_file
        self.output_dir = output_dir 
        
    def duplicated_and_reneme(self, new_name):
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            
            original = self.original_file
            new_path = os.path.join(self.output_dir, new_name)
            new = shutil.copy(original, new_path)
            if new:
                print(f"File duplicated to {new_path}\n")
                return new
                
        except Exception as e:
            print(f"error during duplication original file: {e}")

    def upsize_selected_gates(self, new_file, gate_ids_to_upsize, size):
        gate_ids_to_upsize = {str(g) for g in gate_ids_to_upsize}

        with open(new_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Ex.: "NAND2_X1 _4_ (" -> troca o "X1" por "X<size>" apenas se o id estiver selecionado.
        inst_re = re.compile(r"^(?P<lead>\s*\S+_X)(?P<x>\d+)(?P<tail>\s+_(?P<id>\d+)_\s*\()")
        edited = 0
        for i, line in enumerate(lines):
            m = inst_re.match(line)
            if not m:
                continue
            inst_id = m.group("id")
            if inst_id not in gate_ids_to_upsize:
                continue
            if m.group("x") == str(size):
                continue
            lines[i] = f"{m.group('lead')}{size}{m.group('tail')}{line[m.end():]}"
            edited += 1

        if edited:
            with open(new_file, "w", encoding="utf-8") as f:
                f.writelines(lines)
        return edited

def return_verilog_module(file):
    with open(file, encoding="utf-8") as f:
        text = f.read()

    m = re.search(r"\bmodule\s+(\w+)\s*\(", text, re.S)
    if not m:
        print("erro to copy verilog module name")
        return None

    module_name = m.group(1)
    print(f"Module name: {module_name}")
    return module_name

def get_gates(line):
    pattern = r'^(\S+\s+_\d+_)\s*\($'

    try:
        match = re.match(pattern, line)
        if match:
            return match.group(1)
    except:
        print("there is a erro during reading the cells files")


def get_cell_name(list_gates):
    ids = []
    for gate in list_gates:
        match = re.search(r'_(\d+)_', gate)
        if match:
            ids.append(match.group(1))
    return ids


def gates_from_file(verilog_file):
    module = return_verilog_module(verilog_file)
    circuit = Extract_info(
        verilog_file,
        start_block=module,
        end_block="endmodule",
        process_line=get_gates,
    )
    circuit.read_block()
    ids = get_cell_name(circuit.cells)
    return ids


def mask_to_bitstring(mask, width):
    # Convenção: Gate1 = ids[0] é o bit menos significativo (bit mais à direita).
    return format(mask, f"0{width}b")


def gates_for_mask(ids, mask):
    selected = []
    for bit_index, gate_id in enumerate(ids):
        if (mask >> bit_index) & 1:
            selected.append(gate_id)
    return selected


def generate_combinations(verilog_file, size, output_dir=None, mode="all", max_cases=10_000):
    ids = gates_from_file(verilog_file)
    n = len(ids)
    if n == 0:
        raise RuntimeError("Nenhuma instância de gate encontrada no módulo.")

    if mode not in {"all", "neighbors"}:
        raise ValueError("mode deve ser 'all' ou 'neighbors'")

    # Número de casos:
    # - all: todas as combinações (2^n)
    # - neighbors: base + todos com 1 bit ligado (1 + n)
    if mode == "all":
        total = 1 << n
        masks = range(total)
    else:
        masks = [0] + [(1 << i) for i in range(n)]
        total = len(masks)

    if total > max_cases:
        raise RuntimeError(
            f"Geração resultaria em {total} arquivos (n={n}). "
            f"Aumente max_cases se isso for intencional."
        )

    editor = Edit_verilog(verilog_file, output_dir)

    print(f"Gates (ordem Gate1..Gate{n}): {ids}")
    print(f"Modo: {mode} | size: X{size} | casos: {total}")

    created = 0
    total_edited = 0

    st_name = 0
    for mask in masks:
        bits = mask_to_bitstring(mask, n)
        new_name = f"{st_name}__{saved_name}__X{size}.v"
        new_file = editor.duplicated_and_reneme(new_name)
        selected = gates_for_mask(ids, mask)
        edited = editor.upsize_selected_gates(new_file, selected, size)
        created += 1
        total_edited += edited
        st_name += 1
    print(f"Arquivos criados: {created} | Linhas editadas: {total_edited}")


if __name__ == "__main__":
    # Ex.:
    # - mode="neighbors" -> gera 000000 + 000001 + 000010 + ...
    # - mode="all" -> gera todas as combinações (2^n)
    generate_combinations(file, size=size, output_dir=output_dir, mode="all")