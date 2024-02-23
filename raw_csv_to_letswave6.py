import pandas as pd

Post_letsWave6_columns = [
    "subject_id",
    "session",
    "block",
    "curr_time",
    "is_oddball",
    "pressed",
    "reaction_time"
]

EVENT_CODES = {
    "BLOCK_START": 65536,
    "CORRECT_REJ": 252, # Not oddball, no press
    "CORRECT_HIT": 254, # Oddball, pressed
    "FALSE_ALARM": 253, # Not oddball, press
    "MISS": 251,
    "ODDBALL_START": 151, # Oddball codes go from 151 to 166
    "ODDBALL_END": 166
}

def log_error(message, row, trial):
    print(f"Error: {message} occured in row {row}, corresponding trial: {trial}")

def convert_raw_eeg_csv_to_letswave6(
        subject_id,
        session,
        raw_eeg_df: pd.DataFrame,
        sample_rate: int = 512
        ) -> pd.DataFrame:
    """
    Converts the raw_eeg_csv form of [onset, sig, code] 
        to the Post_LetsWave6 Format
    """
    # We skip two rows, one is start signal, second is block start
    inital_rows_to_skip = 2 
    rows_per_trial = 3
    output = pd.DataFrame(columns=Post_letsWave6_columns)
    block = 1

    for i in range(inital_rows_to_skip, len(raw_eeg_df), rows_per_trial):
        is_oddball = False
        pressed = False

        trial = raw_eeg_df.iloc[i: i + rows_per_trial]

        # Signal to indicate type of event
        trial_block_code = trial.iloc[0]["code"]
        # Signal to indicate if a user pressed a key
        trial_user_response_code = trial.iloc[2]["code"]
       
        # TODO: Charles originally said that it would be trial.iloc[1]
        #       though there is a discrepancy with other scripts, 
        #       so for now i'll use trial.iloc[0]
        curr_time = trial.iloc[0]["onset"] / sample_rate
        reaction_time = (trial.iloc[2]["onset"] - trial.iloc[0]["onset"]) / sample_rate

        if trial_block_code == block:
            # Regular trial event is occuring
            if trial_user_response_code == EVENT_CODES["FALSE_ALARM"]:
                pressed = True
        elif trial_block_code == EVENT_CODES["BLOCK_START"]:
            # New block is starting
            block += 1
            continue
        elif trial_block_code >= EVENT_CODES["ODDBALL_START"] and \
                trial_block_code <= EVENT_CODES["ODDBALL_END"]:
            is_oddball = True
            if trial_user_response_code == EVENT_CODES["CORRECT_HIT"]:
                pressed = True
        elif trial_block_code != block:
            log_error(f"Unexpected code: expected {block} - got {trial_block_code}",
                      i, trial)
        
        new_entry = {
            "subject_id": subject_id,
            "session": session,
            "block": block, 
            "curr_time": curr_time,
            "is_oddball": is_oddball,
            "pressed": pressed,
            "reaction_time": reaction_time
        }
        output.loc[(i - inital_rows_to_skip) // rows_per_trial] = new_entry
    
    return output

if __name__ == "__main__":
    raw_eeg_df = pd.read_csv("tests/subj04_session2.csv")
    eeg_letswave6 = convert_raw_eeg_csv_to_letswave6(
        subject_id=4,
        session=2,
        raw_eeg_df=raw_eeg_df
    )
    eeg_letswave6.to_csv("tests/sub04_session2_letswave6.csv", index=False)
