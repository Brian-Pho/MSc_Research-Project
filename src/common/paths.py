from os.path import join

# Main data and script locations
BPHO_DIR = '/imaging3/owenlab/bpho'
REPO_DIR = '/home/bpho/Documents/MSc_Research-Project'

# Common folders
BIOBANK_LABELS = join(BPHO_DIR, 'Biobank Labels')
SCRATCH_DATA = join(REPO_DIR, 'scratch_data')

# Power atlas labels
RAW_POWER = join(SCRATCH_DATA, 'power_atlas_labels.xls')
POWER = join(SCRATCH_DATA, 'power_atlas_labels.csv')

# Bad subjects
BAD_SUBJECTS = join(SCRATCH_DATA, 'bad_subjects.csv')

# Functional connectivity
POWER_FC = join(BPHO_DIR, 'python_power_fc')

# WISC
RAW_WISC = join(BIOBANK_LABELS, 'Labels_Feb2_2021.csv')
WISC = join(BIOBANK_LABELS, 'Subjects_with_WISC.csv')
HEALTHY = join(BIOBANK_LABELS, 'Subjects_with_WISC (healthy).csv')

# Model weights
MODEL_WEIGHTS = join(SCRATCH_DATA, 'model_weights')
PLS_WEIGHTS = join(MODEL_WEIGHTS, 'PLS')
RIDGE_WEIGHTS = join(MODEL_WEIGHTS, 'Ridge')

# Model results
MODEL_RESULTS = join(SCRATCH_DATA, 'model_results')
PLS_RESULTS = join(MODEL_RESULTS, 'PLS')
RIDGE_RESULTS = join(MODEL_RESULTS, 'Ridge')
CROSS_PRED_RESULTS = join(MODEL_RESULTS, 'Cross Prediction')
