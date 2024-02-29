# alljoined_preprocessing

## Folder Structure

Below is a description of the main files and directories:

    ├── eeg_data/                       # Data files are stored here
        ├── bdf/                        # Raw bdf files
            ├── subj01_session01.bdf
            ├── subj02_session01.bdf
        └── raw_csv/                    # The stimulus data retrieved from bdf
            ├── subj01_session01.csv
            ├── subj02_session01.csv
        └── parsed_csv/                 # Parsed stimulus data with double triggers merged
            ├── subj01_session01.csv
            ├── subj02_session01.csv
        └── fif/                        # Parsed stimulus data converted to .fif format
            ├── subj01_session01.fif
            ├── subj02_session01.fif
        └── final_eeg/                  # Final preprocesses EEG data in .fif format
            ├── subj01_session01.fif
            ├── subj02_session01.fif
    ├── process_cell.py
    └── README.md           # The file you're reading now

## Preprocessing pipeline

1. Get the raw bdf file from Biosemi device. Link to the datasets are [here](https://drive.google.com/drive/u/0/folders/1yPFhX04nh2EnHBSEAjHyBmnWpP7oJQ21). Put it in bdf/
2. Run the first part of parse-bdf-event-codes-to-fif.ipynb to retrieve stimulus data
3. Run the second part of parse-bdf-event-codes-to-fif.ipynb to merge the double trigger data into a combined format. We use double trigger because BioSemi only support 8 bits.
4. Run the third part of parse-bdf-event-codes-to-fif.ipynb to convert parsed_csv to fif format. 
Do the steps below for each of the frequency ranges: 0.5/125, 55/95, 14/70, 5/95
5. Modify the frequency in fif-eeg-preprocessing.py, on this line: 
raw.filter(l_freq=0.5, h_freq=125)
Then modify the path and replace low, high with actual values. For 0.5, use 05: 
preprocessed_file_path = os.path.join('eeg_data', 'final_eeg_low_high', f"{root_name}_epo.fif" )
6. Run fif-eeg-preprocessing.py to preprocess the .fif data. This performs band filtering, epoch detection, PCA, eye blink removal, baseline correction. 
7. Change eeg_fiff_folder to the correct one in final_dataset/main_dataset.py, on this line: 
eeg_fiff_folder = '../eeg_data/final_eeg'
Then change output_csv_path to point to also include the frequency range in the name: 
output_csv_path = os.path.join(eeg_csv_folder, '../combined_dataset.csv')
8. Run final_dataset/main_dataset.py to create a csv of all the data for that frequency range 
9. Update csv_file_path to the csv path you create above in final_dataset/create_huggingface_dataset.py 
10. Run final_dataset/create_huggingface_dataset.py to create and upload the dataset 

