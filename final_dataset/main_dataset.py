import csv
from scipy.io import loadmat
import mne
import pandas as pd
import os


def load_csv_to_list(csv_filepath):
    """
    Reads a CSV file and converts it into a list of tuples.

    Parameters:
    - csv_filepath: Path to the CSV file.

    Returns:
    - A list of tuples, where each tuple contains [image number, cocoId].
    """
    data = []
    with open(csv_filepath, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for idx, row in enumerate(reader):
            # Convert the first, second columns to int 
            if row[0] == '':
                print(f"Row index: {idx} is blank")
                continue
            else:
                data.append((int(row[0]), int(row[1])))
    return data


def load_mat_file(file_path):
    """
    Loads a .mat file.

    Parameters:
    - file_path: Path to the .mat file.

    Returns:
    - The contents of the .mat file.
    """
    mat_contents = loadmat(file_path)
    return mat_contents


def get_nsd_id(mat_contents, subject, session, id):
    """
    Returns the NSD image ID for a given subject, session, and id.

    Parameters:
    - mat_contents: The contents loaded from the .mat file.
    - subject: The subject number (1-indexed).
    - session: The session number (1-indexed).
    - id: The index within the session (0-999).

    Returns:
    - Image ID corresponding to the specified subject, session, and id.
    """

    if subject % 2 == 0:  # For even subjects, use shared images
        indices = mat_contents['sharedix'][0]
    else:
        indices = mat_contents['subjectim'][subject - 1]  # Adjust for 0-indexing

    # Fetch and return the image ID using the global index.
    return indices[id]


def get_coco_id(csv_data, index):
    """
    Returns the COCO ID for a given index from CSV data.

    Parameters:
    - csv_data: A list of tuples/lists where each tuple/list contains [image number, cocoId].
    - index: The 0-based image number to find the COCO ID for.

    Returns:
    - The COCO ID corresponding to the given index.
    """
    for row in csv_data:
        if row[0] == index:
            return row[1]
    return None  # Return None if the index is not found


def load_fiff_epochs(fiff_file_path):
    """
    Load FIFF data file as epochs.
    
    Parameters:
    - fiff_file_path: Path to the FIFF file.
    
    Returns:
    - epochs: Loaded MNE epochs object.
    """
    try:
        epochs = mne.read_epochs(fiff_file_path, preload=True)
        print("Epochs loaded successfully.")
        return epochs
    except Exception as e:
        print(f"Failed to load epochs from file {fiff_file_path}: {e}")
        return None


def generate_dataset(fiff_file_path, csv_file_path, conversion_csv_data, mat_contents):
    """
    Generates a dataset by combining EEG data with image IDs and timing information.

    Parameters:
    - fiff_file_path: Path to the FIFF file containing EEG data.
    - csv_file_path: Path to the CSV file containing trial information.
    - conversion_csv_data: List of tuples containing mapping from image number to COCO ID.
    - mat_contents: Contents of the .mat file containing NSD experiment design.

    Returns:
    - A pandas DataFrame containing the combined dataset.
    """
    epochs = load_fiff_epochs(fiff_file_path)
    if epochs is None:
        return pd.DataFrame()  # Return an empty DataFrame in case of failure

    csv_data = pd.read_csv(csv_file_path)

    if len(epochs) != len(csv_data):
        print(f"Warning: The number of epochs ({len(epochs)}) does not match the number of trials ({len(csv_data)}).")

    # Extract subject and session from FIFF file name
    base_name = os.path.basename(fiff_file_path)
    subject, session = base_name.split('_')[0][4:], base_name.split('_')[1].split('.')[0][7:]

    subject = int(subject) 
    session = int(session)  

    dataset = []

    for i, row in csv_data.iterrows():
        trial = i + 1
        # 240 trials per block
        block = trial // 240 + 1  

        # Extract EEG data for the trial
        eeg_data = epochs[i].get_data(copy=False)  # Extracting EEG data for the ith trial

        # Extract other attributes
        nsd_id = get_nsd_id(mat_contents, subject, session, row['code'])
        coco_id = get_coco_id(conversion_csv_data, row['code']-1)
        curr_time = row['onset'] / 512 if 'onset' in row else None

        # Append to the dataset
        dataset.append({
            "subject_id": subject,
            "session": session,
            "block": block,
            "trial": trial,
            "73k_id": nsd_id,
            "coco_id": coco_id,
            "eeg": eeg_data.squeeze(),  
            "curr_time": curr_time
        })

    # Convert dataset to DataFrame
    dataset_df = pd.DataFrame(dataset)
    return dataset_df


conversion_csv_filepath = 'nsd_coco_conversion.csv'  
conversion_csv_data = load_csv_to_list(conversion_csv_filepath)

nsd_mat_file_path = 'nsd_expdesign.mat'
nsd_mat_contents = load_mat_file(nsd_mat_file_path)

eeg_fiff_file_path = '../final_eeg_files/subj04_session2.fif'
eeg_csv_file_path = '../subj04_session2.csv'

dataset = generate_dataset(eeg_fiff_file_path, eeg_csv_file_path, conversion_csv_data, nsd_mat_contents)
dataset.to_csv('final_dataset.csv', index=False)

