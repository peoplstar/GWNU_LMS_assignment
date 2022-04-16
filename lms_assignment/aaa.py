import json

with open(r'lms_assignment/real.json', 'r+', encoding = "UTF-8") as f: 
    tmp = json.load(f)
    data = {}
    data['20171473'] = tmp
    f.close()
    
with open(r'lms_assignment/test1.json', 'w', encoding = "UTF-8") as f1: 
    json.dump(data, f1, ensure_ascii = False, default = str, indent = 4)
    # Write json.dump(data, f1)
 