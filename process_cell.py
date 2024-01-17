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
    'sub-'+format(args.sub,'02')+'_ses-'+format(args.session,'02')+'_.csv')

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

def apply_changes(df, row_index, hit_status, block_number):
    # Change the third row's first column value to original image
    df.iloc[row_index+2, 0] = ((block_number - 1) % 8) * 120 + df.iloc[row_index+2, 1]

    # Add new columns
    df.loc[row_index+2, 'Hit Status'] = hit_status
    df.loc[row_index+2, 'Reaction Time'] = df.iloc[row_index+2, 2] - df.iloc[row_index, 2]

    # Delete the first two rows
    df = df.drop([row_index, row_index+1]).reset_index(drop=True)
    return df

def process_csv(file_path, block_number):
    df = pd.read_csv(file_path)

    i = 0
    while i < len(df) - 2:
        first_row_value = df.iloc[i, 0]
        third_row_value = df.iloc[i+2, 0]

        # 254 - Oddball - Correct - hit 
        if third_row_value == 254 and first_row_value == block_number + 150:
            df = apply_changes(df, i, 1, block_number)
        
        # 251 - Oddball - Miss - no hit
        elif third_row_value == 251 and first_row_value == block_number + 150:
            df = apply_changes(df, i, 0, block_number)
            
        # 252 - Correct - no hit  
        elif third_row_value == 252 and first_row_value == block_number:
            df = apply_changes(df, i, 0, block_number)
            
        # 253 - False hit - discard 
        elif third_row_value == 253 and first_row_value == block_number:
            df = df.drop([i, i+1, i+2]).reset_index(drop=True)
            continue
        
        # Jump 3 rows for next trial
        i += 3    
    return df

# Iterate over block numbers 1 to 16 and process the CSV 
for block_number in range(1, 17):
    df = process_csv(file_path, block_number)

# Save data
final_output_path = file_path.replace('before', 'after').replace('.csv', '_final_processed.csv')
df.to_csv(final_output_path, index=False)