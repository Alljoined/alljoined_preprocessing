import os
import h5py
import numpy as np
from PIL import Image
import pandas as pd
from datasets import Features, Dataset, Sequence, Value, Image as DatasetsImage
from dotenv import load_dotenv


DSET_NAME = "05_125"
DATASET_PATH = '../eeg_data/final_hdf5/' + DSET_NAME
COCO_PATH = 'stimulus/datasets--pscotti--mindeyev2/snapshots/183269ab73b49d2fa10b5bfe077194992934e4e6/coco_images_224_float16.hdf5'

load_dotenv()
HF_PUSH = os.getenv("HF_PUSH")


def fetch_image(nsd_id, image_path=COCO_PATH):
    with h5py.File(image_path, 'r') as hdf5_file:
        image_data = (hdf5_file['images'][nsd_id-1, ...] * 255).astype(np.uint8)
        image_data = np.transpose(image_data, (1, 2, 0))  # Transpose to (224, 224, 3)
        return Image.fromarray(image_data)

def generate_hf_dataset(df_path, image_path=COCO_PATH):
    df = pd.read_hdf(df_path, key="df")
    for _, row in df.iterrows():
        image = fetch_image(row['73k_id'], image_path)  # Adjust fetch_image as needed
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


def aggregate_hf_datasets(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".h5"):
            df_path = os.path.join(folder_path, file_name)
            yield from generate_hf_dataset(df_path)


print("Creating hf dataset")
hf_dataset = Dataset.from_generator(generator=aggregate_hf_datasets, gen_kwargs={"folder_path": DATASET_PATH}, features=Features({
    'EEG': Sequence(feature=Sequence(feature=Value('float64'))),
    'image': DatasetsImage(),
    'subject_id': Value('int32'),
    'session': Value('int32'),
    'block': Value('int32'),
    'trial': Value('int32'),
    '73k_id': Value('int32'),
    'coco_id': Value('int32'),
    'curr_time': Value('float32'),
}), cache_dir="huggingface")


hf_dataset.push_to_hub("Alljoined/" + DSET_NAME, token=HF_PUSH)