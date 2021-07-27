import os.path

BPHO_DIR = '/imaging3/owenlab/bpho'
REPO_DIR = '/home/bpho/Documents/MSc_Research-Project'

# Functional Connectivity
POWER_FC = os.path.join(BPHO_DIR, 'python_power_fc')
YEO_FC = os.path.join(BPHO_DIR, 'python_yeo_fc')

# WISC
WISC = os.path.join(BPHO_DIR, 'Biobank Labels', 'Subjects_with_WISC.csv')
BAD_SUBJECTS = os.path.join(REPO_DIR, 'scratch_data', 'bad_subjects.csv')

# Model Weights
PLS_WEIGHTS = os.path.join(REPO_DIR, 'scratch_data', 'pls_weights.npy')
RIDGE_WEIGHTS = os.path.join(REPO_DIR, 'scratch_data', 'ridge_weights.npy')
