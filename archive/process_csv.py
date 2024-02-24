import pandas as pd
import argparse
import os

# =============================================================================
# Input arguments
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('--sub', default=1, type=int)
parser.add_argument('--session', default=1, type=int)
parser.add_argument('--data_rootDir', default='eeg_data', type=str)
args = parser.parse_args()

file_path = os.path.join(args.data_rootDir, 'before', 'sub-'+format(args.sub)+'_ses-'+format(args.session)+'_raw.csv')

# Print input arguments
print('\n\n\n>>> Cell Cleaning <<<')
print('\nInput arguments:')
for key, val in vars(args).items():
    print('{:16} {}'.format(key, val))

# =============================================================================
# Process CSV

# Every trial has 3 rows - First Trigger, Second Trigger, Trigger Number
# Change it to one row per trial (Keeping the last row)
# =============================================================================

def create_new_row(row, img_idx, reaction_time):
    new_row = row.copy()
    new_row.iloc[0] = str(img_idx)
    new_row['Reaction Time'] = reaction_time

    return new_row

raw_eeg_df = pd.read_csv(file_path)
new_df = pd.DataFrame(columns=raw_eeg_df.columns)

i = 4
block_number = 1
block_trigger_offset = 150
error_count = 0

while i < raw_eeg_df.shape[0] - 2:
    
    # New block, increment block number and add a block code to new csv
    if raw_eeg_df.iloc[i, 0] == 'Epoch' and i > 100:

        block_number += 1
        i+=3
        # block_row = raw_eeg_df.iloc[i].copy()
        # block_row.iloc[0] = 50000
        # new_df = new_df._append(block_row, ignore_index=True)
        
    first_row_value = raw_eeg_df.iloc[i, 0]
    third_row_value = raw_eeg_df.iloc[i+2, 0]

    # 254 - Oddball - Correct - hit 
    if third_row_value == '254' and first_row_value == str(block_number+block_trigger_offset):
        reaction_time = raw_eeg_df.iloc[i+2, 2] - raw_eeg_df.iloc[i, 2]
        img_idx = ((block_number - 1) % 8) * 120 + int(raw_eeg_df.iloc[i+1, 0])
        # modified_row = create_new_row(raw_eeg_df.iloc[i], 20000, reaction_time)
    
    # # 251 - Oddball - Miss - no hit
    elif third_row_value == '251' and first_row_value == str(block_number+block_trigger_offset):
        reaction_time = raw_eeg_df.iloc[i+2, 2] - raw_eeg_df.iloc[i, 2]
        img_idx = ((block_number - 1) % 8) * 120 + int(raw_eeg_df.iloc[i+1, 0])
        # modified_row = create_new_row(raw_eeg_df.iloc[i], 20000, reaction_time)
        
    # 252 - Correct - no hit  
    elif third_row_value == '252' and first_row_value == str(block_number):
        reaction_time = raw_eeg_df.iloc[i+2, 2] - raw_eeg_df.iloc[i, 2]
        img_idx = ((block_number - 1) % 8) * 120 + int(raw_eeg_df.iloc[i+1, 0])
        modified_row = create_new_row(raw_eeg_df.iloc[i], img_idx, reaction_time)
        new_df = new_df._append(modified_row, ignore_index=True)
        
    # 253 - False hit 
    elif third_row_value == '253' and first_row_value == str(block_number):
        reaction_time = raw_eeg_df.iloc[i+2, 2] - raw_eeg_df.iloc[i, 2]
        img_idx = ((block_number - 1) % 8) * 120 + int(raw_eeg_df.iloc[i+1, 0])
        modified_row = create_new_row(raw_eeg_df.iloc[i], img_idx, reaction_time)
        new_df = new_df._append(modified_row, ignore_index=True)

    else:
        if error_count < 10:
            error_count += 1
            print('Error: ', i, raw_eeg_df.iloc[i, 0], raw_eeg_df.iloc[i+2, 0])

    # Jump 3 rows for next trial
    i += 3

# Save data
final_output_path = file_path.replace('before', 'after').replace('raw.csv', 'parsed.csv')
new_df.to_csv(final_output_path, index=False)

