import re

class Get_IO:
    def __init__(self, file):
        self.file = file

    def get_inputs(self):

        inputs_list = []

        with open(self.file, "r") as f:
            for line in f:
                line = line.strip()
                cat_str = re.match(r'input\s+(\w+);', line)
                
                if cat_str:
                    print(f"Input {cat_str.group(1)} from file {self.file} add to list")

                    inputs_list.append(cat_str.group(1))
                
        return inputs_list   

    def get_outputs(self):

        outputs_list = []

        with open(self.file, "r") as f:
            for line in f:
                line = line.strip()
                cat_str = re.match(r'output\s+(\w+);', line)

                if cat_str:
                    print(f"Output {cat_str.group(1)} from {self.file} add to list")

                    outputs_list.append(cat_str.group(1)) 
                    
        return outputs_list  
    
    def gat_cells_ids(self):
        
        gates_id = []

        with open(self.file, "r") as f:
            for line in f:
                line = line.strip()
                
                cat_str = re.match(r'\w+_X\d+\s+_(\d+)_\s*\(', line)

                if cat_str:
                    gates_id.append(cat_str.group(1))
            
            return gates_id

file = "c499.v"

teste = Get_IO(file)
inputs = teste.get_inputs()

for i in inputs:
    print(i)

outputs = teste.get_outputs()

for o in outputs:
    print(o)

cells = teste.gat_cells_ids()
print(cells)