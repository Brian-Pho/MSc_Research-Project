"""
Holds the functions for getting the functional connectivity and WISC data.
"""
import glob
import os

import numpy as np
import pandas as pd

from common.paths import POWER_FC, ADHD
from common.power_atlas import to_power_fc_vector, get_power_fc_vector_labels
from common.wisc import WISC_LEVEL


def get_data(wisc_level=5, label_path=ADHD):
    """
    Gets functional connectivity data, cognition data, and demographic data.

    Functional connectivity data is in the form of functional connectivity
    matrices derived from the Power et al. atlas of 264 ROIs. Cognition data
    is in the form of WISC-V measures. Demographic data is in the form of age
    and sex.

    Parameters
    ----------
    wisc_level : int
    label_path : str

    Returns
    -------
    tuple
        A tuple containing the functional connectivity data, cognition data,
        demographic data, and which population (ADHD or TD).
    """
    fcs = get_fc_data()
    labels = get_label_data(label_path)

    subject_ids = labels.index
    demographic_measures = ['Age', 'Sex']
    wisc_measures = WISC_LEVEL[wisc_level]
    population = check_population_diagnosis(labels)

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

    return np.array(fc_matrices), wiscs, demographics, population


def get_fc_data():
    """
    Gets the functional connectivity data.

    Returns
    -------
    fcs: dict
        A dictionary mapping subject ID to subject functional connectivity
        matrix.

    """
    fc_paths = glob.glob(POWER_FC + f'/**/power_fc.npy', recursive=True)

    fcs = {}
    for path in fc_paths:
        subject_id = get_subject_id_from_path(path)
        subject_fc = np.load(path)
        fcs[subject_id] = to_power_fc_vector(subject_fc)

    return fcs


def get_label_data(label_path):
    """
    Gets the label data as a Pandas dataframe.

    Parameters
    ----------
    label_path : str

    Returns
    -------
    pd.DataFrame

    """
    return pd.read_csv(label_path, index_col='assessment WISC,EID')


def get_subject_id_from_path(path):
    """
    Gets the subject's ID from their file path.

    Parameters
    ----------
    path : str

    Returns
    -------
    str

    """
    path_components = os.path.normpath(path).split(os.sep)

    return path_components[-2][4:]


def _convert_dict_list_to_dict_numpy(dict_list):
    """
    Converts a dictionary with lists as values into a dictionary with numpy
    arrays as values.

    Used because numpy array is more flexible to work with and has more
    functions.

    Parameters
    ----------
    dict_list : dict

    Returns
    -------
    dict

    """
    return {k: np.array(v) for k, v in dict_list.items()}


def check_population_diagnosis(labels):
    """
    Gets the dataset's diagnosis.

    Parameters
    ----------
    labels : pd.DataFrame

    Returns
    -------
    str

    """
    # TODO: CHANGE FUNCTION NAME
    has_diagnosis_col = 'assessment Diagnosis_ClinicianConsensus,NoDX'
    has_diagnosis = labels[has_diagnosis_col] == 'Yes'

    return 'adhd' if any(has_diagnosis) else 'healthy'


def get_subjects(subject_folder, desired_subjects=None):
    """
    Filters a list of subjects for the subjects we want.

    Parameters
    ----------
    subject_folder : str
    desired_subjects : list

    Returns
    -------
    list

    """
    subjects = [folder for folder in os.listdir(subject_folder) if
                folder.startswith("sub-")]

    if desired_subjects:
        subjects = [subject for subject in subjects if
                    subject in desired_subjects]

    return subjects


def generate_fake_data(X, y):
    """
    Generates a fake dataset that matches the shape of X and y.

    The fake data is generated from a normal distribution with matching mean
    and standard deviation as X and y respectively.

    Parameters
    ----------
    X : np.array
    y : np.array

    Returns
    -------
    tuple

    """
    X_mean, X_std = np.mean(X), np.std(X)
    y_mean, y_std = np.mean(y), np.std(y)

    X_fake = np.random.default_rng().normal(X_mean, X_std, size=X.shape)
    y_fake = np.random.default_rng().normal(y_mean, y_std, size=y.shape)

    return X_fake, y_fake


def filter_data_by_network(
        X, network, only_within_network=False, keep_connections=False):
    """
    Filters the dataset by the given Power network.

    The output can be either only connections within a network or all
    connections where one endpoint is the network. The output shape can also
    change to the network connections or fill the unselected connections with
    zero (done to maintain original dataset shape).

    Parameters
    ----------
    X : np.array
    network : str
    only_within_network : bool
    keep_connections : bool

    Returns
    -------
    np.array

    """
    vector_labels = get_power_fc_vector_labels(True)

    network_connection_indices = []
    for index, connection in enumerate(vector_labels):
        if (only_within_network and connection[0] == network and
                connection[1] == network):
            network_connection_indices.append(index)
        elif connection[0] == network or connection[1] == network:
            network_connection_indices.append(index)

    if keep_connections:
        X_filtered = np.zeros(X.shape)
        X_filtered[:, network_connection_indices] = X[:, network_connection_indices]
    else:
        X_filtered = X[:, network_connection_indices]

    return X_filtered


def round_to_sig_fig(value, sig_figs=1):
    """
    Rounds a number to the specified number of significant figures.

    Parameters
    ----------
    value : float
    sig_figs : int

    Returns
    -------
    float

    """

    value_str = np.format_float_positional(
        value, precision=sig_figs, unique=False, fractional=False, trim='k')

    return float(value_str)
