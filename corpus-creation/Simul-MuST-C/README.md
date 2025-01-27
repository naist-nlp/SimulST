# Simul-MuST-C

This directory contains the code used for the corpus creation of Simul-MuST-C.

We make the prompt and code used to create Simul-MuST-C available and do not releasing the dataset at this time due to licensing restrictions related to the MuST-C license, as stated in the paper.

However, we deeply value the potential for researchers to utilize our dataset to simulaneous speech translation community. Once the MuST-C licensing issue is resolved, we plan to negotiate with the relevant parties to explore the possibility of releasing the dataset.

ACL Anthology: https://aclanthology.org/2024.emnlp-main.1238/

## Usage

### Step 0.
Prepare OpenAI Batch API (https://platform.openai.com/docs/guides/batch).
1. create your account at OpenAI and charge enough budget.
2. prepare MuST-C corpus (currently not available).

### Step 1.
`create_jsonl.py` to create jsonl files for batch processing.
- set the file path as the source sentences in MuST-C at `file_paths = []`.

### Step 2.
`upload_jsonl.py` for uploading the files that created at Step 1. for batch processing. 
- set the `OPENAI_ORGANIZATION_KEY`, `OPENAI_API_KEY`, and `file_path = [.../*.jsonl]`.

### Step 3.
`extract.py` to extract the outputs from the batch-processed file.
- set the `batch_file_path = [.../batch_***.jsonl]` which is batch-processed file.
- set the `tst_path` as the source sentences in MuST-C and `ja_tst_path` for the target sentences in MuST-C.
- set the `output_dir` as the output directory path.
- get the files as below.
    - `output.rewrite` is outputs from the thrid step. Translation outputs that are monotonic to the source and are used as Simul-MuST-C's target sentences.
    - `sep.en` is outputs from the first step that let LLM to break down into smaller segments.
    - `sep.ja` is outputs from the second step that let LLM to translate each segments from the first step.

### Additional
`batch_merge.py` to merge first try file to second and later tries file, second or more tries happens when the outputs contain errors. 
When an error happens, do Step 1. and Step 2. again to get desirable outputs.
- set `orig_cache_file` as first try file path.
- set `new_cache_file` as second or more tries file path.
- set `write_cache_file` as merged file path.

## Citation

Bibkey (ACLAnthology.bib): `makinae-etal-2024-simul`

BibTeX:
```
@inproceedings{makinae-etal-2024-simul,
    title = "Simul-{M}u{ST}-{C}: Simultaneous Multilingual Speech Translation Corpus Using Large Language Model",
    author = "Makinae, Mana  and
      Sakai, Yusuke  and
      Kamigaito, Hidetaka  and
      Watanabe, Taro",
    editor = "Al-Onaizan, Yaser  and
      Bansal, Mohit  and
      Chen, Yun-Nung",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.emnlp-main.1238/",
    doi = "10.18653/v1/2024.emnlp-main.1238",
    pages = "22185--22205",
    abstract = "Simultaneous Speech Translation (SiST) begins translating before the entire source input is received, making it crucial to balance quality and latency. In real interpreting situations, interpreters manage this simultaneity by breaking sentences into smaller segments and translating them while maintaining the source order as much as possible. SiST could benefit from this approach to balance quality and latency. However, current corpora used for simultaneous tasks often involve significant word reordering in translation, which is not ideal given that interpreters faithfully follow source syntax as much as possible. Inspired by conference interpreting by humans utilizing the salami technique, we introduce the Simul-MuST-C, a dataset created by leveraging the Large Language Model (LLM), specifically GPT-4o, which aligns the target text as closely as possible to the source text by using minimal chunks that contain enough information to be interpreted. Experiments on three language pairs show that the effectiveness of segmented-base monotonicity in training data varies with the grammatical distance between the source and the target, with grammatically distant language pairs benefiting the most in achieving quality while minimizing latency."
}
```