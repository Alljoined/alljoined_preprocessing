import csv
from scipy.io import loadmat


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
    # Assuming each subject has a unique set of images per session
    # and each session has 1000 images.
    # Calculate the global index offset based on subject and session.
    if subject % 2 == 0:  # For even subjects, use shared images
        indices = mat_contents['sharedix'][0]
    else:
        indices = mat_contents['subjectim'][subject - 1]  # Adjust for 0-indexing

    # Calculate the global index considering each session has 1000 images.
    # Adjusting for 0-indexing and assuming sessions are sequentially stored.
    global_index = (session - 1) * 1000 + id

    # Fetch and return the image ID using the global index.
    return indices[global_index]


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


csv_filepath = 'nsd_coco_conversion.csv'  
csv_data = load_csv_to_list(csv_filepath)
mat_file_path = 'nsd_expdesign.mat'
mat_contents = load_mat_file(mat_file_path)


nsd_id = get_nsd_id(mat_contents, 5, 1, 1)
print(f"NSD id: {nsd_id}")
print(f"COCO id: {get_coco_id(csv_data, nsd_id)}")
