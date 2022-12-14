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
erm_data_paths = []

transcend_dir = '/autofs/cluster/transcend'
erm_dir = op.join(transcend_dir, 'MEG', 'erm')
paradigm = 'AttenAud'

directory_of_interest = op.join(transcend_dir, 'MEG', paradigm)

for path, directory_names, filenames in os.walk(directory_of_interest):
    last_6_digits = path[-6:] #check last 6 characters of folder name which can be an ID or a date
    if last_6_digits.isnumeric(): #only look into those that have either the participant ID or a date
        for filename in filenames:
            if paradigm + '_run' not in filename: #check for paradigm name and run
                continue
            else:
                if 'raw.fif' in filename: # if it is a raw.fif file, 
                    subject_id = filename[:6]
                    subject_ids.append(subject_id) 
                    data_path = os.path.join(path, filename) 
                    data_paths.append(data_path) #write both file and path to dataframe
                    raw = mne.io.read_raw_fif(data_path) #open .fif file with MNE python 
                    date = raw.info['meas_date'].date() #Locate date of data collection
                    data_dates.append(date.strftime("%Y%m%d"))
                    erm_filename = subject_id +'_erm_raw.fif'
                    subject_erm_path = os.path.join(erm_dir, subject_id,date.strftime("%Y%m%d"),erm_filename)
                    # check if subject ERM folder exists
                    if os.path.exists(subject_erm_path):
                        erm_path = subject_erm_path
                    else:
                        erm_path = 'Missing ERM data'
                
                    erm_data_paths.append(erm_path)
                    
# combine all info in data frame and save to csv
paths_and_date_df = pd.DataFrame(data={'Subject': subject_ids, 'Date_collected': data_dates,
                                'Data_path': data_paths, 'ERM_data_paths': erm_data_paths})
                    
today_formatted = datetime.datetime.today().strftime('%Y%m%d')
paths_and_date_savename = paradigm + f'_alignment_updated_{today_formatted}_v2.csv'
paths_and_date_df.to_csv(paths_and_date_savename)