import pandas as pd
from raw_csv_to_letswave6 import convert_raw_eeg_to_letswave6, Post_letsWave6_columns 

raw_csv_columns = ["onset", "sig", "code"]

def test_regular_event():
    subject = 4
    session = 3
    rate = 512
    sample_data = [
        [368, 65536, 65734],
        [637, 0, 201],
        [1020,0,1],
        [1037,0,39],
        [1366,0,252]
    ]

    sample_df = pd.DataFrame(sample_data, columns=raw_csv_columns)
    test_df = convert_raw_eeg_to_letswave6(
        subject_id=subject,
        session=session,
        raw_eeg_df=sample_df,
        sample_rate=rate
    )
    expected_data = [[subject, session, 1, 1020/rate, False, False, (1366-1020) / rate]]
    expected_df = pd.DataFrame(expected_data, 
                               columns=Post_letsWave6_columns)

    assert(test_df.equals(expected_df))

def test_oddball_correct_hit():
    subject = 4
    session = 3
    rate = 512
    sample_data = [
        [368, 65536, 65734],
        [637, 0, 201],
        [1024,0,151],
        [1280,0,5],
        [1536,0,254],
    ]

    sample_df = pd.DataFrame(sample_data, columns=raw_csv_columns)
    test_df = convert_raw_eeg_to_letswave6(
        subject_id=subject,
        session=session,
        raw_eeg_df=sample_df,
        sample_rate=rate
    )
    expected_data = [[subject, session, 1, 1024/rate, True, True, (1536-1024) / rate]]
    expected_df = pd.DataFrame(expected_data, 
                               columns=Post_letsWave6_columns)

    assert(test_df.equals(expected_df))

def test_oddball_miss():
    subject = 4
    session = 3
    rate = 512
    sample_data = [
        [368, 65536, 65734],
        [637, 0, 201],
        [1024,0,151],
        [1280,0,111],
        [1536,0,251],
    ]

    sample_df = pd.DataFrame(sample_data, columns=raw_csv_columns)
    test_df = convert_raw_eeg_to_letswave6(
        subject_id=subject,
        session=session,
        raw_eeg_df=sample_df,
        sample_rate=rate
    )
    expected_data = [[subject, session, 1, 1024/rate, True, False, (1536-1024) / rate]]
    expected_df = pd.DataFrame(expected_data, 
                               columns=Post_letsWave6_columns)

    assert(test_df.equals(expected_df))

def test_regular_event_false_alarm():
    subject = 4
    session = 3
    rate = 512
    sample_data = [
        [368, 65536, 65734],
        [637, 0, 201],
        [1024,0,2],
        [1280,0,1],
        [1536,0,253],
    ]

    sample_df = pd.DataFrame(sample_data, columns=raw_csv_columns)
    test_df = convert_raw_eeg_to_letswave6(
        subject_id=subject,
        session=session,
        raw_eeg_df=sample_df,
        sample_rate=rate
    )
    expected_data = [[subject, session, 1, 1024/rate, False, True, (1536-1024) / rate]]
    expected_df = pd.DataFrame(expected_data, 
                               columns=Post_letsWave6_columns)

def test_block_change():
    subject = 4
    session = 3
    rate = 512
    sample_data = [
        [368, 65536, 65734],
        [637, 0, 201],
        [1024,0,1],
        [1280,0,39],
        [1536,0,252],
        # block change event:
        [1792,0,65536],
        [2048,65536,65734],
        [2304,0,202],
        # regular event again
        [2560,0,2],
        [2816,0,48],
        [3072,0,252],
    ]

    sample_df = pd.DataFrame(sample_data, columns=raw_csv_columns)
    test_df = convert_raw_eeg_to_letswave6(
        subject_id=subject,
        session=session,
        raw_eeg_df=sample_df,
        sample_rate=rate
    )
    expected_data = [
        [subject, session, 1, 1024/rate, False, False, (1536-1024) / rate],
        [subject, session, 2, 2560/rate, False, False, (3072-2560) / rate], 
    ]
    expected_df = pd.DataFrame(expected_data, 
                               columns=Post_letsWave6_columns)
    print(test_df)
    print(expected_df)
    assert(test_df.equals(expected_df))  

