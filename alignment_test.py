#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 17:41:32 2022

@author: jwt30
"""
import pandas as pd
import datetime
import os
import os.path as op
import mne

subject_ids = []
data_dates = []
data_paths = []

transcend_dir = '/autofs/cluster/transcend'

directory_of_interest = op.join(transcend_dir, 'MEG', 'AttenAud')

for path, directory_names, filenames in os.walk(directory_of_interest):
    last_6_digits = path[-6:] #check last 6 characters of folder name which can be an ID or a date
    if last_6_digits.isnumeric(): #only look into those that have either the participant ID or a date
        for filename in filenames:
            if 'AttenAud_run' not in filename: #check for paradigm name and run
                continue
            else:
                if 'raw.fif' in filename: # if it is a raw.fif file, write both file and path to dataframe
                    subject_id = filename[:6]
                    subject_ids.append(subject_id)
                    data_path = os.path.join(path, filename)
                    data_paths.append(data_path)
                    raw = mne.io.read_raw_fif(data_path)
                    date = raw.info['meas_date'].date()
                    data_dates.append(date.strftime("%Y%m%d"))
                    
# build fixation-ERM dataframe
paths_and_date_df = pd.DataFrame(data={'Subject': subject_ids, 'Date_collected': data_dates,
                                'Data_path': data_paths})
                    
today_formatted = datetime.datetime.today().strftime('%Y%m%d')
paths_and_date_savename = f'Fixation_ERM_MRI_alignment_updated_{today_formatted}.csv'
paths_and_date_df.to_csv(paths_and_date_savename)