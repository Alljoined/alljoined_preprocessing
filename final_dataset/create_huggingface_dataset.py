import os
import h5py
import numpy as np
from PIL import Image
import pandas as pd
from datasets import Features, Dataset, Sequence, Value, Image as DatasetsImage
from dotenv import load_dotenv
import re


DSET_NAME = "05_125"
load_dotenv()
HF_PUSH = os.getenv("HF_PUSH")

DATASET_PATH = '../eeg_data/combined_dataset.h5'
COCO_PATH = 'stimulus/datasets--pscotti--mindeyev2/snapshots/183269ab73b49d2fa10b5bfe077194992934e4e6/coco_images_224_float16.hdf5'

def fetch_image(nsd_id, file_path=COCO_PATH):
    with h5py.File(file_path, 'r') as hdf5_file:
        image_data = (hdf5_file['images'][nsd_id-1, ...] * 255).astype(np.uint8)
        image_data = np.transpose(image_data, (1, 2, 0))  # Transpose to (224, 224, 3)
        return Image.fromarray(image_data)


def generate_hf_dataset(df, file_path=COCO_PATH):
    for _, row in df.iterrows():
        image = fetch_image(row['73k_id'], file_path)
        yield {
            'EEG': row["eeg"], 
            'image': image,
            'subject_id': row['subject_id'],
            'session': row['session'],
            'block': row['block'],
            'trial': row['trial'],
            '73k_id': row['73k_id'],
            'coco_id': row['coco_id'],
            'curr_time': row['curr_time'],
        }

        break

df = pd.read_hdf(DATASET_PATH, key="df")

print("Creating hf dataset")
hf_dataset = Dataset.from_generator(generator=generate_hf_dataset, gen_kwargs={"df": df}, cache_dir="huggingface")

hf_dataset.push_to_hub("Alljoined/" + DSET_NAME, token=HF_PUSH)