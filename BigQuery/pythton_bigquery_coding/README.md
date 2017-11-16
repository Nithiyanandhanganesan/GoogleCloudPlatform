pip install -r requirements.txt

Main scripts are:

intel/inteljob.py and load_new_event/load_new_event.py


load_new_event.py determines the which files to load from GCS to BQ. This script loads for retailnext, kochava, and meraki. After loading from GCS, it run sql and save the data to specified dataset/tables

inteljob.py runs all the sql files and save them to dateset/tables