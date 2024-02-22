# This script will read a raw bdf file from /raw, and get the triggers from the file. It will then save it to a .csv file in /raw-triggers
import mne
import pandas as pd

# Path to your BDF file
bdf_file_path = '/Users/jonathan/Documents/coding/alljoined/alljoined_preprocessing/raw/sub-05/subj05_session1.bdf'

# Read the BDF file
raw = mne.io.read_raw_bdf(bdf_file_path, preload=True)
raw.copy().pick(picks="stim").plot(start=3, duration=6)
events = mne.find_events(raw, stim_channel='STI 014')

# Convert the events array to a DataFrame
events_df = pd.DataFrame(events, columns=['Time', 'Duration', 'Trigger'])

# Save to CSV
csv_file_path = 'events.csv'
events_df.to_csv(csv_file_path, index=False)
