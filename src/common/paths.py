import os.path

# Main data and script locations
BPHO_DIR = '/imaging3/owenlab/bpho'
REPO_DIR = '/home/bpho/Documents/MSc_Research-Project'

# Common folders
BIOBANK_LABELS = os.path.join(BPHO_DIR, 'Biobank Labels')
SCRATCH_DATA = os.path.join(REPO_DIR, 'scratch_data')

# Functional Connectivity
POWER_FC = os.path.join(BPHO_DIR, 'python_power_fc')
YEO_FC = os.path.join(BPHO_DIR, 'python_yeo_fc')

# WISC
RAW_WISC = os.path.join(BIOBANK_LABELS, 'Labels_Feb2_2021.csv')
# RAW_WISC = os.path.join(BIOBANK_LABELS, 'data-2020-07-21T15_31_07.904Z.csv')
WISC = os.path.join(BIOBANK_LABELS, 'Subjects_with_WISC.csv')
BAD_SUBJECTS = os.path.join(SCRATCH_DATA, 'bad_subjects.csv')

# Model Weights
MODEL_WEIGHTS = os.path.join(SCRATCH_DATA, 'model_weights')
RIDGE_WEIGHTS = os.path.join(SCRATCH_DATA, 'model_weights', 'ridge_weights.npy')

# Power atlas labels
RAW_POWER = os.path.join(SCRATCH_DATA, 'power_atlas_labels.xls')
POWER = os.path.join(SCRATCH_DATA, 'power_atlas_labels.csv')
