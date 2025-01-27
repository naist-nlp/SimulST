# This file is to extract the outputs after you get the batch processed file

import json
from tqdm import tqdm
import hashlib

# Save per instruction
def create_hash(request_id):
    return hashlib.md5(request_id.encode()).hexdigest()

# Choose file path
### First try 
# batch_file_path = '/project/nlp-work7/mana-ma/LLM-Corpus/en-de/train/batch_en-de.jsonl'
###2回目以降 Second and after tries
batch_file_path = '/project/nlp-work7/mana-ma/LLM-Corpus/en-de/train/new_batch_en-de.jsonl'

# Path for original source and target lang
tst_path = 'e.g., train.en'
ja_tst_path = 'e.g., train.de'

# Path for the newly created data
output_dir = 'e.g., /en-de/train/'


def main():
    # Open and read the tst_jsonl files to see whether the original source line exits in hash
    with open(tst_path, 'r', encoding='utf-8') as tst_file:
        english_sentences = [line.strip() for line in tst_file]

    # Get the outputs from batch processed file
    with open(batch_file_path, 'r', encoding='utf-8') as batch_file:
        cache = dict()
        count = 0
        for _data in batch_file:
            try:
                data = json.loads(_data)
                response_content = json.loads(data['response']['body']['choices'][0]['message']['content'].replace('\n', ''))
                cache[data['custom_id']] = response_content
            except:
                cache[data['custom_id']] = 'Error'
                print(f'Cache Error: {count}')
                count +=1
             
    with open(ja_tst_path, 'r') as file, open(tst_path, 'r') as file2:
        pair_dict = dict()
        ja_lines = file.readlines()
        en_lines = file2.readlines()
        assert len(ja_lines) == len(en_lines)

        for ja_line, en_line in zip(ja_lines, en_lines):
            ja_line = ja_line.strip()
            en_line = en_line.strip()
            pair_dict[en_line] = ja_line

    # Initialize lists to store content
    rewrite_text = []
    segmented_en = []
    segmented_ja = []
    count = 0
    # Extract necessary information for each custom_id
    for sentence in tqdm(english_sentences):
        hash_id = create_hash(sentence)
        assert hash_id in cache, sentence

        # When the process doesn't go as expected
        if "salami technique" in str(cache[hash_id]).lower():
            rewrite_text.append(pair_dict[sentence])
            segmented_en.append(sentence)
            segmented_ja.append(pair_dict[sentence])

        else:
            try:
                response_content = cache[hash_id]
                assert "salami technique" not in str(response_content).lower()

                outputs = response_content['output']
                segment_pairs = response_content['segmented_pairs']
                
                rewrite_text.append(outputs)
                segmented_en.append(' / '.join([en for en, _ in segment_pairs]))
                segmented_ja.append(' / '.join([ja for _, ja in segment_pairs]))
            except:
                print(f'Error: {count}')
                print(f'hash_id: {hash_id}')
                print(f"Sentence: {sentence}")
                print(f"response_content:\n{response_content}")
                count +=1
                print('------------')
                rewrite_text.append('Error')
                segmented_en.append('Error')
                segmented_ja.append('Error')

    # Write results to output files
    with open(f'{output_dir}/output.rewrite', 'w', encoding='utf-8') as f:
        for text in rewrite_text:
            f.write(text + '\n')

    with open(f'{output_dir}/sep.en', 'w', encoding='utf-8') as f:
        for text in segmented_en:
            f.write(text + '\n')

    with open(f'{output_dir}/sep.ja', 'w', encoding='utf-8') as f:
        for text in segmented_ja:
            f.write(text + '\n')


if __name__ == '__main__':
    main()