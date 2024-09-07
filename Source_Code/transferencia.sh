#!/bin/bash
##source /home/ovsicori/miniconda3/etc/profile.d/conda.sh
conda activate eq_env
python "mydir/TRANSFER.py" --base_dir=directorio_origen --waves_in_dir=directorio_ondas --startdate=ano-dia --enddate=ano-conuno > "directorio_origen/LOGS/trans_logs/trans_experiment.txt"
