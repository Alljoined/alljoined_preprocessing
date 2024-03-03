import os
import h5py
import numpy as np
from PIL import Image
import pandas as pd
from datasets import Dataset
from dotenv import load_dotenv

load_dotenv()
# HF_PUSH = os.getenv("HF_PUSH")

DATASET_PATH = '../combined_dataset.csv'

def fetch_image(nsd_id, file_path="stimulus/coco_images_224_float16.hdf5"):
    with h5py.File(file_path, 'r') as hdf5_file:
        image_data = (hdf5_file['images'][nsd_id-1, ...] * 255).astype(np.uint8)
        image_data = np.transpose(image_data, (1, 2, 0))  # Transpose to (224, 224, 3)
        return Image.fromarray(image_data)


def generate_hf_dataset(df, file_path="stimulus/coco_images_224_float16.hdf5"):
    for _, row in df.iterrows():
        image = fetch_image(row['73k_id'], file_path)
        yield {
            'EEG': row['eeg'], 
            'image': image,
            'subject_id': row['subject_id'],
            'session': row['session'],
            'block': row['block'],
            'trial': row['trial'],
            '73k_id': row['73k_id'],
            'coco_id': row['coco_id'],
            'curr_time': row['curr_time'],
        }

df = pd.read_csv(DATASET_PATH)

print("Creating hf dataset")
CACHE_DIR = "."
hf_dataset = Dataset.from_generator(generator=generate_hf_dataset, gen_kwargs={"df": df}, cache_dir=CACHE_DIR)

# print("Uploading dataset")
# hf_dataset = load_dataset(CACHE_DIR)
# hf_dataset.push_to_hub("daekun/alljoined_dataset", token=HF_PUSH)