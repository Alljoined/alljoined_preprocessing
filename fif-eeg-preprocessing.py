"""
Steps 8 through 20 
"""

import mne
from mne.preprocessing import ICA
import os
import scipy.signal
import numpy as np 


input_file = 'subj04_session2.fif'

# Load the BDF file
fif_file_path = os.path.join('eeg_data', 'fif', input_file) 
input_file_name = os.path.basename(fif_file_path)
raw = mne.io.read_raw_fif(fif_file_path, preload=True)
print(raw._data.shape)

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
reject_criteria = dict(eeg=700e-6)  # 700 µV = 700e-6 V
epochs.drop_bad(reject=reject_criteria)

# Remove 'Status' channel (Step 8). 
# Removing it here because you need this channel for earlier steps like creating epochs
raw.drop_channels(['Status'])

# ICA for artifact correction (Steps 14 and 15)
ica = ICA(n_components=0.95, random_state=97)
ica.fit(epochs)
ica.apply(epochs)

# Rereferencing (Step 17)
epochs.set_eeg_reference('average')

# Baseline correction (Step 18)
epochs.apply_baseline(baseline=(-0.05, 0))

# Saving the preprocessed data
preprocessed_file_path = fif_file_path.replace('fif', 'final_eeg_files')
os.makedirs(os.path.dirname(preprocessed_file_path), exist_ok=True)
epochs.save(preprocessed_file_path)

# Zipping the preprocessed data (Step 20)
# with zipfile.ZipFile(os.path.join(output_dir, 'preprocessed_data.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
#     zipf.write(preprocessed_file_path, arcname='preprocessed-epochs.fif')

# print("Preprocessing complete. Data saved and zipped.")
