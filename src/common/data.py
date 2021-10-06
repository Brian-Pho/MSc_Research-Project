import glob
import os

import numpy as np
import pandas as pd

from .paths import POWER_FC, YEO_FC, WISC
from .wisc import WISC_LEVEL


def get_data(atlas='Power', wisc_level=0):
    fcs = get_fc_data(atlas)
    labels = get_label_data()

    subject_ids = labels.index
    demographic_measures = ['Age', 'Sex']
    wisc_measures = WISC_LEVEL[wisc_level]

    fc_matrices = []
    demographics = {measure: [] for measure in demographic_measures}
    wiscs = {measure: [] for measure in wisc_measures}

    for subject_id in subject_ids:
        if subject_id not in fcs:
            continue

        fc_matrices.append(fcs[subject_id])

        for measure in demographic_measures:
            demographics[measure].append(
                labels.at[subject_id, f'assessment Basic_Demos,{measure}'])

        for measure in wisc_measures:
            wiscs[measure].append(
                labels.at[subject_id, f'assessment WISC,{measure}'])
    
    wiscs = _convert_dict_list_to_dict_numpy(wiscs)
    demographics = _convert_dict_list_to_dict_numpy(demographics)
    
    return np.array(fc_matrices), wiscs, demographics


def get_fc_data(atlas='Power'):
    # Search for all functional connectivity files and read them
    fc_path = POWER_FC if atlas == 'Power' else YEO_FC
    fc_filename = 'power_fc.npy' if atlas == 'Power' else 'yeo_fc.npy'
    fc_paths = glob.glob(fc_path + f'/**/{fc_filename}', recursive=True)

    fcs = {}
    for path in fc_paths:
        subject_id = get_subject_from_path(path)
        subject_fc = np.load(path)
        fcs[subject_id] = subject_fc[np.triu_indices(264, k=1)]

    return fcs


def get_label_data():
    return pd.read_csv(WISC, index_col='assessment WISC,EID')


def get_subject_from_path(path):
    normalized_path = os.path.normpath(path)
    path_components = normalized_path.split(os.sep)
    
    return path_components[-2][4:]


def _convert_dict_list_to_dict_numpy(dict_list):
    dict_numpy = {}
    
    for k, v in dict_list.items():
        dict_numpy[k] = np.array(v)
    
    return dict_numpy
