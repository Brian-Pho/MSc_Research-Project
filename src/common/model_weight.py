"""
Holds the functions for saving and loading model weights.
"""
import os

import numpy as np

from common.binning import BIN_LABELS
from common.paths import PLS_WEIGHTS, RIDGE_WEIGHTS
from common.wisc import WISC_LEVEL


def save_model_weight(model, population, measure, age_group, model_weight):
    """
    Saves the feature/model weights for a specific model, diagnosis,
    WISC measure, and age bin.
    
    Parameters
    ----------
    model : str
    population : str
    measure : str
    age_group : str
    model_weight : np.array

    Returns
    -------
    str
        Location of the saved model weight.
    
    """
    filename = f'{model}_{population}_{measure}_{age_group}.npy'
    model_weight_folder = PLS_WEIGHTS if model == 'pls' else RIDGE_WEIGHTS
    filepath = os.path.join(model_weight_folder, filename)
    np.save(filepath, model_weight)
    
    return filepath


def load_model_weight(model, population, measure, age_group):
    """
    Loads the feature/model weights for a specific model, diagnosis,
    WISC measure, and age bin.

    Parameters
    ----------
    model : str
    population : str
    measure : str
    age_group : str

    Returns
    -------
    np.array

    """
    if model == "pls":
        coef_filename, model_weight_path = "", PLS_WEIGHTS
    elif model == "ridge":
        coef_filename, model_weight_path = "_coef", RIDGE_WEIGHTS

    weight_filepath = os.path.join(
        model_weight_path,
        f'{model}_{population}_{measure}_{age_group}{coef_filename}.npy')

    return np.load(weight_filepath)


def load_all_model_weights(model, population):
    """
    Loads all model weights for a specific model and diagnosis.

    Parameters
    ----------
    model : str
    population : str

    Returns
    -------
    dict
        Mapping of bin to cognitive measure to feature weight.

    Examples
    --------
    >>> model_weights = load_all_model_weights(model, population)
    >>> print(model_weights.keys(), model_weights['All']['WISC_FSIQ'].shape)
    dict_keys(['All', 'Bin 1', 'Bin 2', 'Bin 3']) (34716,)

    """
    labels = BIN_LABELS if population == 'adhd' else BIN_LABELS[:1]
    model_weights = {k: None for k in labels}

    for bin_label in labels:
        bin_weights = {k: None for k in WISC_LEVEL[5]}

        for target in WISC_LEVEL[5]:
            bin_weights[target] = load_model_weight(model, population, target,
                                                    bin_label)

        model_weights[bin_label] = bin_weights

    return model_weights
