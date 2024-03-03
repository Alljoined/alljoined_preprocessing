import os
from dotenv import load_dotenv
from datasets import load_dataset

CACHE_DIR="/Users/jonathan/Documents/coding/alljoined/alljoined_preprocessing/final_dataset/huggingface"

load_dotenv()
HF_PUSH=os.getenv("HF_PUSH")

print("Uploading dataset")
hf_dataset = load_dataset(CACHE_DIR)
hf_dataset.push_to_hub("Alljoined/v1", token=HF_PUSH)