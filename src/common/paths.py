from os.path import join

# Main data and script locations
BPHO_DIR = '/imaging3/owenlab/bpho'
REPO_DIR = '/home/bpho/Documents/MSc_Research-Project'

# Common folders
BIOBANK_LABELS = join(BPHO_DIR, 'Biobank Labels')
SCRATCH_DATA = join(REPO_DIR, 'scratch_data')
IMAGES = join(REPO_DIR, 'images')

# Power atlas labels
RAW_POWER = join(SCRATCH_DATA, 'power_atlas_labels.xls')
# POWER = join(SCRATCH_DATA, 'power_atlas_labels.csv')
POWER = join(SCRATCH_DATA, 'power_atlas_labels (extrapolate).csv')

# Bad subjects
BAD_SUBJECTS = join(SCRATCH_DATA, 'bad_subjects.csv')

# Functional connectivity
POWER_FC = join(BPHO_DIR, 'python_power_fc')

# WISC
RAW_WISC = join(BIOBANK_LABELS, 'Labels_Feb2_2021.csv')
WISC = join(BIOBANK_LABELS, 'Subjects_with_WISC.csv')
HEALTHY = join(BIOBANK_LABELS, 'Subjects_with_WISC (healthy).csv')
ADHD = join(BIOBANK_LABELS, 'Subjects_with_WISC (adhd).csv')
# ADHD_ONE = join(BIOBANK_LABELS, 'Subjects_with_WISC (adhd 1).csv')
# ADHD_TWO = join(BIOBANK_LABELS, 'Subjects_with_WISC (adhd 2).csv')

# Model weights
MODEL_WEIGHTS = join(SCRATCH_DATA, 'model_weights')
PLS_WEIGHTS = join(MODEL_WEIGHTS, 'PLS')
RIDGE_WEIGHTS = join(MODEL_WEIGHTS, 'Ridge')

# Model weight images
MODEL_WEIGHT_IMGS = join(IMAGES, 'Models')
RIDGE_WEIGHT_IMGS = join(MODEL_WEIGHT_IMGS, 'Ridge')
PLS_WEIGHT_IMGS = join(MODEL_WEIGHT_IMGS, 'PLS')

# Model results
MODEL_RESULTS = join(SCRATCH_DATA, 'model_results')
PLS_RESULTS = join(MODEL_RESULTS, 'PLS')
RIDGE_RESULTS = join(MODEL_RESULTS, 'Ridge')
CROSS_PRED_RESULTS = join(MODEL_RESULTS, 'Cross Prediction')
ICC_RESULTS = join(MODEL_RESULTS, 'ICC')

# Permutation scores
PERM_SCORES = join(SCRATCH_DATA, 'permutation_scores')
RIDGE_PSCORES = join(PERM_SCORES, 'Ridge')
PLS_PSCORES = join(PERM_SCORES, 'PLS')
CROSS_PRED_PSCORES = join(PERM_SCORES, 'Cross Prediction')
