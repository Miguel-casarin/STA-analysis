import os


def find_base_line(designs_path):
    """Retorna um baseline por design.

    Padrão de nome dos arquivos: id__design__size.ext
    Ex.: 0__c17__X2.v, 0__c17__X4.v, 1__c17__X2.v, ...

    - baseline: arquivos cujo id é só zeros ("0", "00", ...)
    - se existir mais de um size para o mesmo design (c17), retorna apenas 1.
    """

    originals = []          # lista de arquivos escolhidos como baseline
    seen_designs = set()    # designs para os quais já escolhemos um baseline

    files = os.listdir(designs_path)

    # ordena para ter comportamento determinístico (pega sempre o mesmo size)
    for file in sorted(files):
        # ignora coisas que não sejam verilog
        if not file.endswith(".v"):
            continue

        parts = file.split("__")
        if len(parts) < 3:
            continue  # não segue o padrão id__design__size

        id_part, design_part = parts[0], parts[1]

        # id precisa ser composto só de '0' (baseline)
        if not id_part or set(id_part) != {"0"}:
            continue

        # já escolhemos um baseline para esse design (c17, etc.)
        if design_part in seen_designs:
            continue

        seen_designs.add(design_part)
        originals.append(file)
        print(f"FILE {file} ad to base line")

    return originals