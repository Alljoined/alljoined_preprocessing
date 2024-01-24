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

file_path = os.path.join(args.data_rootDir, 'before',
    'sub-'+format(args.sub,'02'), 'ses-'+format(args.session,'02'), 
    'sub-'+format(args.sub,'02')+'_ses-'+format(args.session,'02')+'.csv')

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

def process_row(row, img_idx, hit_status, reaction_time):
    new_row = row.copy()
    new_row[0] = img_idx
    new_row['Hit Status'] = hit_status
    new_row['Reaction Time'] = reaction_time

    return new_row

raw_eeg_csv = pd.read_csv(file_path)
processed_df = pd.DataFrame(columns=raw_eeg_csv.columns)

i = 4
block_number = 1

while i < raw_eeg_csv.shape[0] - 2:
    
    # New block, increment block number and add a block code to new csv
    if raw_eeg_csv.iloc[i, 0] == 'Epoch' and i > 100:

        block_number += 1
        i+=3
        block_row = raw_eeg_csv.iloc[i]
        block_row[0] = 5000
        processed_df = processed_df._append(block_row, ignore_index=True)
        
    first_row_value = raw_eeg_csv.iloc[i, 0]
    third_row_value = raw_eeg_csv.iloc[i+2, 0]

    # 254 - Oddball - Correct - hit 
    if third_row_value == '254' and first_row_value == str(block_number+150):
        hit_sataus = 1
        reaction_time = raw_eeg_csv.iloc[i+2, 2] - raw_eeg_csv.iloc[i, 2]
        img_idx = ((block_number - 1) % 8) * 120 + int(raw_eeg_csv.iloc[i+1, 0])
        modified_row = process_row(raw_eeg_csv.iloc[i], img_idx, hit_sataus, reaction_time)
        processed_df = processed_df._append(modified_row, ignore_index=True)
        code_row = raw_eeg_csv.iloc[i+2]
        code_row[0] = '254'
        processed_df = processed_df._append(code_row, ignore_index=True)
    
    # # 251 - Oddball - Miss - no hit
    elif third_row_value == '251' and first_row_value == str(block_number+150):
        hit_sataus = 0
        reaction_time = raw_eeg_csv.iloc[i+2, 2] - raw_eeg_csv.iloc[i, 2]
        img_idx = ((block_number - 1) % 8) * 120 + int(raw_eeg_csv.iloc[i+1, 0])
        modified_row = process_row(raw_eeg_csv.iloc[i], img_idx, hit_sataus, reaction_time)
        processed_df = processed_df._append(modified_row, ignore_index=True)
        code_row = raw_eeg_csv.iloc[i+2]
        code_row[0] = '251'
        processed_df = processed_df._append(code_row, ignore_index=True)
        
    # 252 - Correct - no hit  
    elif third_row_value == '252' and first_row_value == str(block_number):
        hit_sataus = 0
        reaction_time = raw_eeg_csv.iloc[i+2, 2] - raw_eeg_csv.iloc[i, 2]
        img_idx = ((block_number - 1) % 8) * 120 + int(raw_eeg_csv.iloc[i+1, 0])
        modified_row = process_row(raw_eeg_csv.iloc[i], img_idx, hit_sataus, reaction_time)
        processed_df = processed_df._append(modified_row, ignore_index=True)
        code_row = raw_eeg_csv.iloc[i+2]
        code_row[0] = '252'
        processed_df = processed_df._append(code_row, ignore_index=True)
        
    # 253 - False hit 
    elif third_row_value == '253' and first_row_value == str(block_number):
        hit_sataus = 1
        reaction_time = raw_eeg_csv.iloc[i+2, 2] - raw_eeg_csv.iloc[i, 2]
        img_idx = ((block_number - 1) % 8) * 120 + int(raw_eeg_csv.iloc[i+1, 0])
        modified_row = process_row(raw_eeg_csv.iloc[i], img_idx, hit_sataus, reaction_time)
        processed_df = processed_df._append(modified_row, ignore_index=True)
        code_row = raw_eeg_csv.iloc[i+2]
        code_row[0] = '253'
        processed_df = processed_df._append(code_row, ignore_index=True)
    
    # Jump 3 rows for next trial
    i += 3

# Save data
final_output_path = file_path.replace('before', 'after').replace('.csv', '_preletswave.csv')
processed_df.to_csv(final_output_path, index=False)