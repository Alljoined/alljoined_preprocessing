import mne
import os
import numpy as np 
import argparse

# experiment with 0.5/125, 55/95, 14/70, 5/95
DATA_PATH="/srv/eeg_reconstruction/shared/biosemi-dataset"
LOW_FREQ = 0.1
HI_FREQ = 100
output_path = os.path.join(DATA_PATH, 'final_eeg', str(LOW_FREQ).replace('.', '') + "_" + str(HI_FREQ))

parser = argparse.ArgumentParser(description='Preprocess EEG data')
parser.add_argument('input_file', type=str, help='Input file name', default='subj04_session2_eeg.fif')
args = parser.parse_args()

# Load the BDF file
fif_file_path = os.path.join(DATA_PATH, 'fif', args.input_file) 
raw = mne.io.read_raw_fif(fif_file_path, preload=True)

chan_order = ['Fp1', 'Fp2', 'AF7', 'AF3', 'AFz', 'AF4', 'AF8', 'F7', 'F5', 'F3',
				  'F1', 'F2', 'F4', 'F6', 'F8', 'FT9', 'FT7', 'FC5', 'FC3', 'FC1', 
				  'FCz', 'FC2', 'FC4', 'FC6', 'FT8', 'FT10', 'T7', 'C5', 'C3', 'C1',
				  'Cz', 'C2', 'C4', 'C6', 'T8', 'TP9', 'TP7', 'CP5', 'CP3', 'CP1', 
				  'CPz', 'CP2', 'CP4', 'CP6', 'TP8', 'TP10', 'P7', 'P5', 'P3', 'P1',
				  'Pz', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO3', 'POz', 'PO4', 'PO8',
				  'O1', 'Oz', 'O2']
raw.pick_channels(chan_order, ordered=True)

# Apply standard montage
montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(montage)

# Filter data (Step 9)
raw.filter(l_freq=LOW_FREQ, h_freq=HI_FREQ)
raw.notch_filter(freqs=60)

# Detect events and Epoching
events = mne.find_events(raw)
epochs = mne.Epochs(raw, events, event_id=None, tmin=-0.05, tmax=0.60, baseline=(None,0), preload=True)

### Sort the data ###
data = epochs.get_data()
events = epochs.events[:,2]
img_cond = np.unique(events)
del epochs

# Select only a maximum number of EEG repetitions
if data_part == 'test':
    max_rep = 20
else:
    max_rep = 2
# Sorted data matrix of shape:
# Image conditions × EEG repetitions × EEG channels × EEG time points
sorted_data = np.zeros((len(img_cond),max_rep,data.shape[1],
    data.shape[2]))
for i in range(len(img_cond)):
    # Find the indices of the selected image condition
    idx = np.where(events == img_cond[i])[0]
    # Randomly select only the max number of EEG repetitions
    idx = shuffle(idx, random_state=seed, n_samples=max_rep)
    sorted_data[i] = data[idx]
del data
epoched_data.append(sorted_data[:, :, :, 50:])
img_conditions.append(img_cond)
del sorted_data
