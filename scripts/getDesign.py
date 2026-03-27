import re
 
def extract_design(s):
    match = re.search(r'__(.*?)__', s)
    if match:
        return match.group(1)
    return None

