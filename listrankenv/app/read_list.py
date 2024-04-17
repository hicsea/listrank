import json
import os
import ListItem

def read_list(txt_filename):
    # Derive JSON filename from TXT filename
    json_filename = txt_filename.replace('.txt', '.json')
    
    # Check if JSON file exists
    if os.path.exists(json_filename):
        # JSON file exists, load existing data
        with open(json_filename, 'r') as json_file:
            data = json.load(json_file)
    else:
        # JSON file does not exist, create from TXT file
        data = {}
        with open(txt_filename, 'r') as txt_file:
            for line in txt_file:
                item_name = line.strip()
                data[item_name] = 800  # Set default score
        
        # Write new JSON file
        with open(json_filename, 'w') as json_file:
            json.dump(data, json_file)

    # Create ListItem instances from data
    list_items = [ListItem(name, score) for name, score in data.items()]
    return list_items


