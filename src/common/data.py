import glob
import os

import numpy as np
import pandas as pd

from .paths import POWER_FC, YEO_FC, WISC
from .wisc import WISC_LEVEL

AGE_COL = 'assessment Basic_Demos,Age'
SEX_COL = 'assessment Basic_Demos,Sex'
DIAGNOSIS_COL = 'assessment Diagnosis_ClinicianConsensus,NoDX'

def get_data(atlas='Power', wisc_level=0):
    fcs = get_fc_data(atlas)
    wisc_labels = get_label_data()

    subject_ids = wisc_labels.index
    wisc_measures = WISC_LEVEL[wisc_level]

    fc_matrices = []
    ages = []
    sexes = []
    diagnosis = []
    measures = {measure: [] for measure in wisc_measures}

    for subject_id in subject_ids:
        if subject_id not in fcs:
            continue

        fc_matrices.append(fcs[subject_id])
        ages.append(wisc_labels.at[subject_id, AGE_COL])
        sexes.append(wisc_labels.at[subject_id, SEX_COL])
        diagnosis.append(wisc_labels.at[subject_id, DIAGNOSIS_COL])

        for measure in wisc_measures:
            measures[measure].append(
                wisc_labels.at[subject_id, f'assessment WISC,{measure}'])

    return np.array(fc_matrices), measures, np.array(ages), np.array(sexes), np.array(diagnosis)


def get_fc_data(atlas='Power'):
    # Search for all functional connectivity files and read them
    fc_path = POWER_FC if atlas == 'Power' else YEO_FC
    fc_filename = 'power_fc.npy' if atlas == 'Power' else 'yeo_fc.npy'
    fc_paths = glob.glob(fc_path + f'/**/{fc_filename}', recursive=True)

    fcs = {}
    for path in fc_paths:
        subject_id = _get_subject_from_path(path)
        subject_fc = np.load(path)
        fcs[subject_id] = subject_fc[np.triu_indices(264, k=1)]

    return fcs


def get_label_data():
    wisc_labels = pd.read_csv(WISC, index_col='assessment WISC,EID')
    return wisc_labels


def _get_subject_from_path(path):
    normalized_path = os.path.normpath(path)
    path_components = normalized_path.split(os.sep)
    return path_components[-2][4:]
