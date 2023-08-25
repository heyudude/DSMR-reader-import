# DSMR-reader-import
Import of records in CSV format from Domoticz to DSMR_reader (https://www.domoticz.com/wiki/Main_Page and https://github.com/dsmrreader) or other sources.

Domoticz uses 2 tables one for the Gas meter readings, the other for the 4 counters from the Electricity.
The CSV file format can be used for other soures also, I included 2 examples

I started working on 2 existing scripts, python and windows scripting.
Both have been at the root of my python script: why another one?
Windows is not my thing ;) The python version is ok but it requires quite a bit of data ombutting. Both not optimal

Disclaimer: I created and tested this on a temporary version of DSMR-Reader, I will do the real conversion only after checking that it is actually correct ;)
The steps:

    Export Domoticz Database
    Export multimeter_calendar. and meter_calendar as CSV with a comma as separator
    Place the 2 files in the same directory as the python script: rename them or edit the script
    pip install pandas (takes care of the operations on the CSV files)
    Add your dsmreader APi key (enable the API) and the Index numbers of the Gas and electricity meters from Domoticz
    sudo supervisorctl stop dsm_backend and dsmr_datalogger
    Run the script
    sudo supervisorctl start all
    ./manage.py dsmr_stats_reconstruct_missing_day_statistics (and prices also if needed)

How does it work globally?
Reading in CSV structure,
filter on the right 2 indexes
Remove redundant columns
Merge electricity and gas measurements
import via the API

Try it first with 1 date and then everything else

The script:
