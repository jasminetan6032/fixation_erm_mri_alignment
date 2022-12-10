import fixation_erm_mri_alignment_config as cfg
import pandas as pd
import os
import os.path as op
import fnmatch
import numpy as np
import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
"""
THIS SCRIPT ASSUMES THAT AN FMRI (RESTING STATE) WILL ALWAYS BE ACQUIRED WITH A STRUCTURAL MRI (MEMPRAGE)
include all subjects who had MEG fixation and ERM (hopefully)
desire for functionality where list may be updated via a search function (ex: search by year)
desired format...

    subject ID | visit # | fix date | fix path | erm path ...
    | sMRI date rank 1 | sMRI date rank 2 | sMRI date rank 3 | fMRI date rank 1 | fMRI date rank 2
    
    Breakdown/mapping
    rank_1 -> the closest
    rank_2 -> the second-closest
    rank_3 -> the third-closest (in this case, the furthest or least-close)
    
"""

def find_closest_one_match(sid, matches, recons_dir, rsmri_dir):
    # there is only one entry in recons for this subject - so it must match...
    # check if subject's recons folder has a date associated with it
    match = matches[0]
    if '_' in match:
        match_split = match.split('_')
        smri_rank1_date = match_split[1]
    else:
        # it is just the subject ID...
        # no date, however there is a path
        smri_rank1_date = 'undetermined'
    subject_rsmri_matches = fnmatch.filter(os.listdir(rsmri_dir), f'{sid}*')
    if len(subject_rsmri_matches) == 0:
        fmri_rank1_date = 'None'
        fmri_rank1_path = 'None'
    else:
        if op.exists(op.join(rsmri_dir, f'{sid}_{smri_rank1_date}')):
            fmri_rank1_date = smri_rank1_date
            fmri_rank1_path = op.join(rsmri_dir, f'{sid}_{smri_rank1_date}')
    smri_rank1_path = op.join(recons_dir, match)

    return smri_rank1_date, smri_rank1_path, fmri_rank1_date, fmri_rank1_path


def find_closest_matches(sid, matches, fix_datestr, fixdate_parsed, recons_dir, rsmri_dir, n_matches):
    global fmri_rank2_date, fmri_rank2_path
    matches_with_dates = fnmatch.filter(os.listdir(recons_dir), f'{sid}_????????')
    """
    if len(matches_with_dates) != n_matches:
        # there are some subject visits with and without dates...
        applicable_matches = [am for am in matches if am in matches_with_dates]
    else:
    """

    # begin the process of matching...
    mri_parsed_dates = [parser.parse(mvf.split('_')[1]) for mvf in matches_with_dates]

    mri_relative_timedeltas = [relativedelta(mvfpd, fixdate_parsed) for mvfpd in mri_parsed_dates]

    utcnow = datetime.datetime.utcnow()
    mri_absolute_timedeltas = [abs(utcnow + mvfrtd - utcnow) for mvfrtd in mri_relative_timedeltas]


    indices = np.argsort(mri_absolute_timedeltas)  # maximum is the closest, minimum is the farthest
    # mri_visits_sorted = mri_absolute_timedeltas[indices] # last element is the closest, first is the farthest
    mri_visits_sorted = np.array(matches_with_dates)[indices]

    smri_rank1_date = mri_visits_sorted[0].split('_')[1]
    smri_rank1_path = op.join(recons_dir, f'{sid}_{smri_rank1_date}')

    smri_rank2_date = mri_visits_sorted[1].split('_')[1]
    smri_rank2_path = op.join(recons_dir, f'{sid}_{smri_rank2_date}')

    # search for rank 1 and rank 2 fMRIs..
    fmri_rank1_potential = op.join(rsmri_dir, f'{sid}_{smri_rank1_date}')
    fmri_rank2_potential = op.join(rsmri_dir, f'{sid}_{smri_rank2_date}')

    if op.exists(fmri_rank1_potential):
        fmri_rank1_date = smri_rank1_date
        fmri_rank1_path = fmri_rank1_potential
        if op.exists(fmri_rank2_potential):
            fmri_rank2_date = smri_rank2_date
            fmri_rank2_path = fmri_rank2_potential
    else:
        fmri_rank1_date = 'None'
        fmri_rank1_path = 'None'
        fmri_rank2_date = 'None'
        fmri_rank2_path = 'None'


    if n_matches == 2:
        return smri_rank1_date, smri_rank1_path, fmri_rank1_date, fmri_rank1_path, \
               smri_rank2_date, smri_rank2_path, fmri_rank2_date, fmri_rank2_path

    else:
        smri_rank3_date = mri_visits_sorted[2].split('_')[1]
        smri_rank3_path = op.join(recons_dir, f'{sid}_{smri_rank3_date}')

        fmri_rank3_potential = op.join(rsmri_dir, f'{sid}_{smri_rank3_date}')
        if op.exists(fmri_rank3_potential):
            fmri_rank3_date = smri_rank3_date
            fmri_rank3_path = fmri_rank3_potential
        else:
            fmri_rank3_date = 'None'
            fmri_rank3_path = 'None'

        return smri_rank1_date, smri_rank1_path, fmri_rank1_date, fmri_rank1_path, \
               smri_rank2_date, smri_rank2_path, fmri_rank2_date, fmri_rank2_path, \
               smri_rank3_date, smri_rank3_path, fmri_rank3_date, fmri_rank3_path


subject_ids = []
fixation_visit_dates = []
fixation_data_paths = []

erm_data_paths = []

# iterate through fixation directory
for subject_folder_path, directory_names, filenames in os.walk(cfg.dir_of_interest):
    path_id = os.path.split(subject_folder_path)
    if 'visit' not in path_id[1]:
        continue
    visit_folder = path_id[1]
    # check if visit_folder is correctly formatted...
    if len(visit_folder.split('_')[1]) != 8:
        continue
    subject = os.path.split(path_id[0])[1]

    if subject.isnumeric() or 'AC' in subject:
        # acquire filenames
        fix_fname = filenames[0]
        fix_data_path = os.path.join(subject_folder_path, fix_fname)
        visit_date = visit_folder.split('_')[1]
        # we now have subject ID (subject), fixation date (visit_date), fixation path (path_to_fix_file)
        # append each of these
        subject_ids.append(subject)
        fixation_visit_dates.append(visit_date)
        fixation_data_paths.append(fix_data_path)
    
        # now begin looking at ERM... dates SHOULD match
        subject_erm_folder = os.path.join(cfg.erm_dir, subject)
        subject_erm_visit_dir = os.path.join(subject_erm_folder, visit_date)
        # check if subject ERM folder exists
        if os.path.exists(subject_erm_folder):
            if os.path.exists(subject_erm_visit_dir):
                erm_files = sorted(os.listdir(subject_erm_visit_dir))
                if len(erm_files) > 0:
                    erm_fname = erm_files[0]
                    erm_data_path = os.path.join(subject_erm_visit_dir, erm_fname)
                else:
                    # visit subfolder created but no data...
                    erm_data_path = 'Missing ERM data'
            else:
                # visit subfolder not created...
                erm_data_path = 'ERM visit subfolder not created'
        else:
            erm_data_path = 'ERM folder missing'
    
        erm_data_paths.append(erm_data_path)

# build fixation-ERM dataframe
fix_erm_df = pd.DataFrame(data={'Subject': subject_ids, 'Fixation_date': fixation_visit_dates,
                                'Fixation_data_path': fixation_data_paths, 'ERM_data_path': erm_data_paths})

smri_rank1_dates = []
smri_rank2_dates = []
smri_rank3_dates = []

smri_rank1_paths = []
smri_rank2_paths = []
smri_rank3_paths = []

fmri_rank1_dates = []
fmri_rank2_dates = []
fmri_rank3_dates = []

fmri_rank1_paths = []
fmri_rank2_paths = []
fmri_rank3_paths = []

for _, subj_row in fix_erm_df.iterrows():

    sid = subj_row['Subject'] # looks like leading zeroes have been preserved?
    fix_datestr = subj_row['Fixation_date']
    fixdate_parsed = parser.parse(fix_datestr)

    # first filter recons dir for subject folders matching subject ID
    subject_id_matches = fnmatch.filter(os.listdir(cfg.recons_dir), f'{sid}_????????')
    if len(subject_id_matches) == 0: # did not find any subject folders in recons with this subject ID

        smri_rank1_date = 'None'
        smri_rank2_date = 'None'
        smri_rank3_date = 'None'

        fmri_rank1_date = 'None'
        fmri_rank2_date = 'None'
        fmri_rank3_date = 'None'

        smri_rank1_path = 'None'
        smri_rank2_path = 'None'
        smri_rank3_path = 'None'

        fmri_rank1_path = 'None'
        fmri_rank2_path = 'None'
        fmri_rank3_path = 'None'
    # we can quickly eliminate the searching for ranks 2 and 3 given the number of matches found in recons
    elif len(subject_id_matches) == 1: # only one MRI visit found in recons, can eliminate search for ranks 2 and 3

        smri_rank2_date = 'None'
        smri_rank3_date = 'None'

        fmri_rank2_date = 'None'
        fmri_rank3_date = 'None'

        smri_rank2_path = 'None'
        smri_rank3_path = 'None'

        fmri_rank2_path = 'None'
        fmri_rank3_path = 'None'

        smri_rank1_date, smri_rank1_path, fmri_rank1_date, fmri_rank1_path = \
            find_closest_one_match(sid, subject_id_matches, cfg.recons_dir, cfg.rs_mri_dir)

    elif len(subject_id_matches) == 2:  # two MRI visits found... eliminate search for rank 3
        smri_rank3_date = 'None'
        fmri_rank3_date = 'None'
        smri_rank3_path = 'None'
        fmri_rank3_path = 'None'

        smri_rank1_date, smri_rank1_path, fmri_rank1_date, fmri_rank1_path,\
        smri_rank2_date, smri_rank2_path, fmri_rank2_date, fmri_rank2_path \
            = find_closest_matches(sid, subject_id_matches, fix_datestr, fixdate_parsed, cfg.recons_dir, cfg.rs_mri_dir, 2)

    else: # we have at least 3 matches

        smri_rank1_date, smri_rank1_path, fmri_rank1_date, fmri_rank1_path, \
        smri_rank2_date, smri_rank2_path, fmri_rank2_date, fmri_rank2_path, \
        smri_rank3_date, smri_rank3_path, fmri_rank3_date, fmri_rank3_path \
            = find_closest_matches(sid, subject_id_matches, fix_datestr, fixdate_parsed, cfg.recons_dir, cfg.rs_mri_dir, 3)


    # append appropriately
    smri_rank1_dates.append(smri_rank1_date)
    smri_rank2_dates.append(smri_rank2_date)
    smri_rank3_dates.append(smri_rank3_date)

    smri_rank1_paths.append(smri_rank1_path)
    smri_rank2_paths.append(smri_rank2_path)
    smri_rank3_paths.append(smri_rank3_path)

    fmri_rank1_dates.append(fmri_rank1_date)
    fmri_rank2_dates.append(fmri_rank2_date)
    fmri_rank3_dates.append(fmri_rank3_date)

    fmri_rank1_paths.append(fmri_rank1_path)
    fmri_rank2_paths.append(fmri_rank2_path)
    fmri_rank3_paths.append(fmri_rank3_path)

fix_erm_mri_data = {'Subject': subject_ids, 'Fixation date': fixation_visit_dates,
                    'Fixation data path': fixation_data_paths, 'ERM data path': erm_data_paths,
                    'sMRI_date_rank1': smri_rank1_dates, 'sMRI_path_rank1': smri_rank1_paths,
                    'sMRI_date_rank2': smri_rank2_dates, 'sMRI_path_rank2': smri_rank2_paths,
                    'sMRI_date_rank3': smri_rank3_dates, 'sMRI_path_rank3': smri_rank3_paths,
                    'fMRI_date_rank1': fmri_rank1_dates, 'fMRI_path_rank1': fmri_rank1_paths,
                    'fMRI_date_rank2': fmri_rank2_dates, 'fMRI_path_rank2': fmri_rank2_paths,
                    'fMRI_date_rank3': fmri_rank3_dates, 'fMRI_path_rank3': fmri_rank3_paths,
                    }

fix_erm_mri_df = pd.DataFrame(data=fix_erm_mri_data, dtype=str)


# making the FROM_DATE to CURRENT_DATE DataFrame...
since_date = cfg.since_datestr
since_date_parsed = parser.parse(since_date)

subjs = []
subj_fixdates = []
subj_fixdate_paths = []
subj_erm_paths = []
within_6mos = []
within_6mos_paths = []
within_12mos = []
within_12mos_paths = []
within_24mos = []
within_24mos_paths = []
for i, subj_row in fix_erm_mri_df.iterrows():
    
    subj = subj_row['Subject']
    fix_date = subj_row['Fixation date']
    fix_date_parsed = parser.parse(fix_date)
    
    fixdate_path = subj_row['Fixation data path']
    ermdate_path = subj_row['ERM data path']
    
    if fix_date_parsed < since_date_parsed:
        continue # look for fixation subjects only visited since input date
    else:
        # time to begin finding mri dates...
        # for each fix date, want to determine the MRIs within 6 months, 12 months, 24 months
        smri_date1 = subj_row['sMRI_date_rank1']
        smri_date2 = subj_row['sMRI_date_rank2']
        smri_date3 = subj_row['sMRI_date_rank3']
        
        smri_date1_path = subj_row['sMRI_path_rank1']
        smri_date2_path = subj_row['sMRI_path_rank2']
        smri_date3_path = subj_row['sMRI_path_rank3']
        
        within_6months_mri = 'None'
        within_6months_mri_path = 'None'
        within_12months_mri = 'None'
        within_12months_mri_path = 'None'
        within_24months_mri = 'None'
        within_24months_mri_path = 'None'
        
        smri_dates_list = [smri_date1, smri_date2, smri_date3]
        smri_date_paths_list = [smri_date1_path, smri_date2_path, smri_date3_path]
        
        for i, smri_date in enumerate(smri_dates_list):
            if smri_date == 'None':
                continue
            else:
                
                smri_date_parsed = parser.parse(smri_date)
                fix_smri_date_abs_relativedelta = abs(relativedelta(fix_date_parsed, smri_date_parsed))
                
                if fix_smri_date_abs_relativedelta.months <= 6 and fix_smri_date_abs_relativedelta.years < 1:
                    within_6months_mri = smri_date
                    within_6months_mri_path = smri_date_paths_list[i]
                    
                elif fix_smri_date_abs_relativedelta.years < 1:
                    within_12months_mri = smri_date
                    within_12months_mri_path = smri_date_paths_list[i]
                    
                elif fix_smri_date_abs_relativedelta.years == 1 and fix_smri_date_abs_relativedelta.months == 0:
                    within_12months_mri = smri_date
                    within_12months_mri_path = smri_date_paths_list[i]
                
                elif fix_smri_date_abs_relativedelta.years == 1:
                    within_24months_mri = smri_date
                    within_24months_mri_path = smri_date_paths_list[i]

                elif fix_smri_date_abs_relativedelta.years == 2 and fix_smri_date_abs_relativedelta.months == 0:
                    within_24months_mri = smri_date
                    within_24months_mri_path = smri_date_paths_list[i]

        subjs.append(subj)
        subj_fixdates.append(fix_date)
        subj_fixdate_paths.append(fixdate_path)
        subj_erm_paths.append(ermdate_path)
        within_6mos.append(within_6months_mri)
        within_12mos.append(within_12months_mri)
        within_24mos.append(within_24months_mri)
        
        within_6mos_paths.append(within_6months_mri_path)
        within_12mos_paths.append(within_12months_mri_path)
        within_24mos_paths.append(within_24months_mri_path)
            
                        
time_window_filtered_alignment_data = {'Subject': subjs,
                                       'Fixation date': subj_fixdates, 'Fixation data path': subj_fixdate_paths, 'ERM data path': subj_erm_paths,
                                       'mri_6mo': within_6mos, 'mri_6mo_path': within_6mos_paths,
                                       'mri_12mo': within_12mos, 'mri_12mo_path': within_12mos_paths,
                                       'mri_24mo': within_24mos, 'mri_24mo_path': within_24mos_paths}
time_window_filtered_alignment_df = pd.DataFrame(data=time_window_filtered_alignment_data)

today_formatted = datetime.datetime.today().strftime('%Y%m%d')

entire_alignment_savename = f'Fixation_ERM_MRI_alignment_updated_{today_formatted}.csv'
time_window_df_savename = f'Fixation_ERM_MRI_alignment_from_{since_date}_to_{today_formatted}.csv'

# entire_alignment_save_msg = f'*** Saving the alignment .csv from all-time as {entire_alignment_savename}...
# \n'
#print(entire_alignment_save_msg)
#fix_erm_mri_df.to_csv(entire_alignment_savename)

time_window_save_msg = f'*** Saving the alignment .csv from {since_date} as {time_window_df_savename}...\n'
print(time_window_save_msg)
time_window_filtered_alignment_df.to_csv(time_window_df_savename)

