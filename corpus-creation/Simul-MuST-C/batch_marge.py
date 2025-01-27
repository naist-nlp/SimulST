# This file is to merge first try file to second and later tries file, 
# second or more tries happens when the outputs contain errors 

import re

def main():
    
    orig_cache_file = 'first try file path, e.g., batch_en-de.jsonl'
    new_cache_file = 'second or more tries file path, e.g., batch_en-de_error_output.jsonl'
    write_cache_file = 'marged file path, e.g., new_batch_en-de.jsonl'

    pattern = r'"custom_id":\s*"([a-f0-9]{32})"'
    with open(new_cache_file) as f:
        new_cache = dict()
        for line in f:
            match = re.search(pattern, line)
            hash_id = match.group(1)
            new_cache[hash_id] = line
   
    write_cache = []
    with open(orig_cache_file) as f:
        for line in f:
            match = re.search(pattern, line)
            hash_id = match.group(1)
            if hash_id in new_cache:
                write_cache.append(new_cache[hash_id])
            else:
                write_cache.append(line)

    with open(write_cache_file, 'w') as f:
        for line in write_cache:
            f.write(line)

if __name__ == '__main__':
    main()