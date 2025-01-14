from os.path import join

transcend_dir = '/autofs/cluster/transcend'
paradigm = 'AttenAud'

dir_of_interest = join(transcend_dir, 'MEG', paradigm)
erm_dir = join(transcend_dir, 'MEG', 'erm')

dicom_dir = join(transcend_dir, 'MRI', 'WMA', 'DICOM')
recons_dir = join(transcend_dir, 'MRI', 'WMA', 'recons')
rs_mri_dir = join(transcend_dir, 'MRI', 'WMA', 'rs_MRI')

# ENTER BELOW THE DATE YOU WOULD LIKE TO SEARCH FROM
# FORMAT MUST BE: YYYYMMDD
# example: August 29th, 2019 ---> 20190829
# PLEASE KEEP THIS VARIABLE NAME THE SAME - ELSE YOU WILL HAVE TO EDIT ITS IMPORT INTO THE MAIN SCRIPT ITSELF

all_dates_dict  = {'fix'       : '20220408', 
                   'AttenAud'  : '20190314', 
                   'AttenVis'  : '20190314', 
                   'Misophonia': '20230301'}

since_datestr   = all_dates_dict[paradigm] 

#For AttenVis paradigm: since_datestr = '20190901'
