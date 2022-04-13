import glob
import os

import numpy as np
import pandas as pd

from .paths import POWER_FC, ADHD, PLS_WEIGHTS, RIDGE_WEIGHTS, BIOBANK_LABELS
from .wisc import WISC_LEVEL


def get_data(wisc_level=5, label_path=ADHD):
    """
    Get functional connectivity data, cognition data, and demographic data.
    
    Functional connectivity data is in the form of functional connectivity matrices
    derived from the Power et al. atlas of 264 ROIs.
    
    Cognition data is in the form of WISC-V measures.
    
    Demographic data is in the form of age and sex.
    """
    fcs = get_fc_data()
    labels = get_label_data(label_path)

    subject_ids = labels.index
    demographic_measures = ['Age', 'Sex']
    wisc_measures = WISC_LEVEL[wisc_level]
    population = check_population_diagnosis(labels)

    fc_matrices = []
#     fc_ids = []
    demographics = {measure: [] for measure in demographic_measures}
    wiscs = {measure: [] for measure in wisc_measures}

    for subject_id in subject_ids:
        if subject_id not in fcs:
            continue
        
#         fc_ids.append(subject_id)
        fc_matrices.append(fcs[subject_id])

        for measure in demographic_measures:
            demographics[measure].append(
                labels.at[subject_id, f'assessment Basic_Demos,{measure}'])

        for measure in wisc_measures:
            wiscs[measure].append(
                labels.at[subject_id, f'assessment WISC,{measure}'])
    
    wiscs = _convert_dict_list_to_dict_numpy(wiscs)
    demographics = _convert_dict_list_to_dict_numpy(demographics)
    
    return np.array(fc_matrices), wiscs, demographics, population


def get_fc_data():
    """
    Search for all functional connectivity files and load them.
    """
    fc_paths = glob.glob(POWER_FC + f'/**/power_fc.npy', recursive=True)

    fcs = {}
    for path in fc_paths:
        subject_id = get_subject_id_from_path(path)
        subject_fc = np.load(path)
        fcs[subject_id] = subject_fc[np.triu_indices(264, k=1)]

    return fcs


def get_label_data(label_path):
    """
    Get label file and read as a Pandas dataframe.
    """
    return pd.read_csv(label_path, index_col='assessment WISC,EID')


def get_subject_id_from_path(path):
    """
    Get subject ID from subject path.
    """
    normalized_path = os.path.normpath(path)
    path_components = normalized_path.split(os.sep)
    
    return path_components[-2][4:]


def _convert_dict_list_to_dict_numpy(dict_list):
    """
    Convert a dictionary with list values into a dictionary with
    numpy array values.
    
    Used because numpy array is more flexible to work with and has more functions.
    """
    dict_numpy = {}
    
    for k, v in dict_list.items():
        dict_numpy[k] = np.array(v)
    
    return dict_numpy


def check_population_diagnosis(labels):
    """
    Get diagnosis for the dataset.
    """
    has_diagnosis_col = 'assessment Diagnosis_ClinicianConsensus,NoDX'
    has_diagnosis = labels[has_diagnosis_col] == 'Yes'
    
    return 'adhd' if any(has_diagnosis) else 'healthy'
    

def get_model_weights(model, population, measure, age_group):
    """
    Read the model weights for a specific model, diagnosis, WISC measure, and age bin.
    """
    weight_filepath = None
    if model == 'pls':
        weight_filepath = os.path.join(PLS_WEIGHTS, f'{model}_{population}_{measure}_{age_group}.npy')
    else:
        weight_filepath = os.path.join(RIDGE_WEIGHTS, f'{model}_{population}_{measure}_{age_group}_coef.npy')
    
    return np.load(weight_filepath)


def get_subjects(subject_folder, desired_subjects=None):
    """
    Get a list of subjects only if they are subjects we want; ignores unspecificed subjects.
    """
    subjects = [folder for folder in os.listdir(subject_folder) if folder.startswith("sub-")]
    if desired_subjects:
        subjects = [subject for subject in subjects if subject in desired_subjects]
        
    return subjects


def generate_fake_data(X, y):
    X_mean, X_std = np.mean(X), np.std(X)
    y_mean, y_std = np.mean(y), np.std(y)
    
    X_fake = np.random.default_rng().normal(X_mean, X_std, size=X.shape)
    y_fake = np.random.default_rng().normal(y_mean, y_std, size=y.shape)
    
    return X_fake, y_fake
