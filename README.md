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

1. Get the raw bdf file from Biosemi device. Put it in bdf/
2. Run the first part of parse-bdf-event-codes-to-fif.ipynb to retrieve stimulus data
3. Run the second part of parse-bdf-event-codes-to-fif.ipynb to merge the double trigger data into a combined format. We use double trigger because BioSemi only support 8 bits.
4. Run the third part of parse-bdf-event-codes-to-fif.ipynb to convert parsed_csv to fif format
5. Run fif-eeg-preprocessing.py to preprocess the .fif data. This performs band filtering, epoch detection, PCA, eye blink removal, baseline correction
