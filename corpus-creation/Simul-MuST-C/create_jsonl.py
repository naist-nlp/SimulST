# This is for creating jsonl files for batch processing

import json
import os
import sys
import ast
import hashlib
import argparse
import glob
from tqdm import tqdm
import time
from typing import List
from tqdm import tqdm

import json
import os

# Save per instruction
def create_hash(request_id):
    return hashlib.md5(request_id.encode()).hexdigest()

# file path you want to process, e.g., train.en
file_paths = []

# Maximum number of lines
max_lines_per_file = 50000

# Process per file
for file_path in tqdm(file_paths):
    # A set that collects unique sentences
    unique_lines = set()

    # Read the file and add set
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            unique_lines.add(line.strip())

    # Create the basic name for JSON Lines files, modify as you like
    base_name = os.path.basename(file_path)
    jsonl_base_name = os.path.splitext(base_name)[0] + '_part'
    lang_pair = file_path.split('/')[5] 
    data_type = file_path.split('/')[7] 
    lang = lang_pair.split('-')[1]
    if lang == 'ja':
        language = 'Japanese'
    elif lang == 'zh':
        language = 'Chinese'
    elif lang == 'de':
        language = 'German'

    # Create output directory if it doesn't exist
    output_dir = 'Path for output directory'
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the file indes and line counter
    file_index = 1
    line_counter = 0

    # Write to JSON Lines file
    for i, text in enumerate(unique_lines, start=1):
        # Open the new file
        if line_counter % max_lines_per_file == 0:
            if line_counter > 0:
                f.close()
            jsonl_file_name = f"{jsonl_base_name}{file_index}.jsonl"
            jsonl_file_path = os.path.join(output_dir, jsonl_file_name)
            f = open(jsonl_file_path, 'w', encoding='utf-8')
            file_index += 1
        
        # Create request data
        request_data = {
            "custom_id": create_hash(f"{text}"),  # ID that unique within the file
            "method": "POST",  # fixed
            "url": "/v1/chat/completions",  # fixed 
            "body": {
                "model": "",  # Choose the GPT model, e.g., gpt-4o-2024-05-13
                "messages": [  
                    {
                        "role": "system",
                        "content": f"You will be provided with a sentence in English, and your task is to interpret it into {language}. Always answer in the following JSON format:{{'segmented_pairs:List[Tuple[English, {language}]], 'output':{language}}}"                                                                                                                                                     
                    },
                    {
                        "role": "user",
                        "content": f"Instructions:\n'Salami Technique' in simultaneous interpretation refers to a technique where the interpreter breaks down the source language input into smaller, manageable segments that each contain enough information to be accurately interpreted.\n1. Break down the following sentence into smaller segments for easier simultaneous interpretation.\n2. Translate each segment into {language}.\n3. Connect the translated segments.\n----------------------\nInputs:\n{text}\n"
                    }
                ],
                "temperature": 0.5,
                "top_p": 0.0,
                "seed": 0,
                "n": 1,
                "max_tokens": 2000,
                "response_format": { "type": "json_object" }
            }
        }

        f.write(json.dumps(request_data, ensure_ascii=False) + '\n')
        line_counter += 1

    f.close()
