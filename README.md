# fixation_erm_mri_alignment
Script to align resting state (fix) MEG data with MEG ERM data, and closest structural MRIs to corresponding fixation visits

fixation_erm_mri_alignment_by_time_window.py <--> the main script you will run to generate an aligned .csv
fixation_erm_mri_alignment_config.py <---> the config file you will edit prior to running the main script

Running the script:
  1. Open the config file -> edit the since_datestr variable to match the date you would like to align from. Please follow the comments' instructions above this variale and use the YYYYMMDD convention.
  2. Save the config file once complete. Open a terminal, head to the location of these files.
  3. Set up your Python environment (bash/conda activate mne)
  4. Run the script - "python fixation_erm_mri_alignment_by_time_window"
  5. Check the terminal for a note on when it finishes - it will tell you exactly what the aligned .csv is named and saved as.




For the most part, this script uses Python-standard libraries - packages and modules by default included in a Python version. The below libraries are NOT included, and depending on one's environment, may need to be installed.

  1. pandas
  2. dateutil
  3. numpy 

^^ If you are using Anaconda or a similar data-science focused Python install - these will be included with your Python version.
  
