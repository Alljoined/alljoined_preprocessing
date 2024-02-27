"""
Steps 8 through 20 
"""

import mne
from mne.preprocessing import ICA
import os
import scipy.signal
import numpy as np 
import argparse

parser = argparse.ArgumentParser(description='Preprocess EEG data')
parser.add_argument('input_file', type=str, help='Input file name', default='subj04_session2.fif')
args = parser.parse_args()

# Load the BDF file
fif_file_path = os.path.join('eeg_data', 'fif', args.input_file) 
raw = mne.io.read_raw_fif(fif_file_path, preload=True)

# Apply standard montage
montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(montage)

# Filter data (Step 9)
raw.filter(l_freq=0.01, h_freq=40, fir_design='firwin')
raw.notch_filter(freqs=50)

# DC Removal (Step 11) and Linear Detrend (Step 16)
raw.apply_function(lambda x: x - np.mean(x))
scipy.signal.detrend(raw._data, axis=0, type='linear')

# Detect events and Epoching (Step 10)
events = mne.find_events(raw)
epochs = mne.Epochs(raw, events, event_id=None, tmin=-0.05, tmax=0.65, preload=True)

# Automated Artifact Rejection (Step 12): Setting threshold to 700 µV
# todo: check also for -700e-6
reject_criteria = dict(eeg=700e-6)  # 700 µV = 700e-6 V
epochs.drop_bad(reject=reject_criteria)

# Remove 'Status' channel (Step 8). 
# Removing it here because you need this channel for earlier steps like creating epochs
raw.drop_channels(['Status'])

# ICA for artifact correction (Steps 14 and 15)
# As is typically done with ICA, the data are first scaled to unit variance and whitened using principal components analysis (PCA)
# before performing the ICA decomposition. It uses the # of components needed to explain 95% of the variance
ica = ICA(n_components=0.95, random_state=97)
ica.fit(epochs)
ica.apply(epochs)

# Rereferencing (Step 17)
epochs.set_eeg_reference('average')

# Baseline correction (Step 18)
# Baseline correction before ICA is not recommended by the MNE-Python developers, as it doesn’t guarantee optimal results.
epochs.apply_baseline(baseline=(-0.05, 0))

# Saving the preprocessed data
preprocessed_file_path = os.path.join('eeg_data', 'final_eeg', args.input_file)
os.makedirs(os.path.dirname(preprocessed_file_path), exist_ok=True)
epochs.save(preprocessed_file_path)
