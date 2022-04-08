from os.path import join

transcend_dir = '/autofs/cluster/transcend'

fix_dir = join(transcend_dir, 'MEG', 'fix')
erm_dir = join(transcend_dir, 'MEG', 'erm')

dicom_dir = join(transcend_dir, 'MRI', 'WMA', 'DICOM')
recons_dir = join(transcend_dir, 'MRI', 'WMA', 'recons')
rs_mri_dir = join(transcend_dir, 'MRI', 'WMA', 'rs_MRI')

# ENTER BELOW THE DATE YOU WOULD LIKE TO SEARCH FROM
# FORMAT MUST BE: YYYYMMDD
# example: August 29th, 2019 ---> 20190829
# PLEASE KEEP THIS VARIABLE NAME THE SAME - ELSE YOU WILL HAVE TO EDIT ITS IMPORT INTO THE MAIN SCRIPT ITSELF
since_datestr = '20201113'
