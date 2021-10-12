import os.path

# Main data and script locations
BPHO_DIR = '/imaging3/owenlab/bpho'
REPO_DIR = '/home/bpho/Documents/MSc_Research-Project'

# Common folders
BIOBANK_LABELS = os.path.join(BPHO_DIR, 'Biobank Labels')
SCRATCH_DATA = os.path.join(REPO_DIR, 'scratch_data')

# Functional Connectivity
POWER_FC = os.path.join(BPHO_DIR, 'python_power_fc')

# WISC
RAW_WISC = os.path.join(BIOBANK_LABELS, 'Labels_Feb2_2021.csv')
WISC = os.path.join(BIOBANK_LABELS, 'Subjects_with_WISC.csv')
BAD_SUBJECTS = os.path.join(SCRATCH_DATA, 'bad_subjects.csv')

# Model Weights
MODEL_WEIGHTS = os.path.join(SCRATCH_DATA, 'model_weights')
PLS_WEIGHTS = os.path.join(MODEL_WEIGHTS, 'PLS')
RIDGE_WEIGHTS = os.path.join(MODEL_WEIGHTS, 'Ridge')

# Power atlas labels
RAW_POWER = os.path.join(SCRATCH_DATA, 'power_atlas_labels.xls')
POWER = os.path.join(SCRATCH_DATA, 'power_atlas_labels.csv')
