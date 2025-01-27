# This file is for uploading the files that created at previous step for batch processing 

from openai import OpenAI
import os

OPENAI_ORGANIZATION_KEY=''
OPENAI_API_KEY=''
client = OpenAI(organization=OPENAI_ORGANIZATION_KEY, api_key=OPENAI_API_KEY)

# Uploading the files, the below is an example
lang_pairs = ['en-zh']
file_names = ['train']
file_number = [1, 2, 3, 4, 5, 6, 7]

for lang_pair in lang_pairs:
    for file_name in file_names:
        for num in file_number:
            # Write the file path you want to process
            file_path = f'{lang_pair}/{file_name}/{lang_pair}_{file_name}_part{num}.jsonl'
            
            if os.path.exists(file_path):

                # Upload your batch file
                batch_input_file = client.files.create(
                    file=open(file_path, "rb"), 
                    purpose="batch")

                # Creating the batch
                batch_input_file_id = batch_input_file.id
                client.batches.create(
                        input_file_id=batch_input_file_id,
                        endpoint="/v1/chat/completions",
                        completion_window="24h",
                        metadata={
                            "description": "Write any comments as you like"
                        }
                    )
                print(f"Batch created successfully, {lang_pair}, {file_name},{num}")
                
            else:
                print(f"File {file_path} does not exist. Skipping to the next file.")