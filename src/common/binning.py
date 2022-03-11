import numpy as np

BIN_LABELS = ["All", "Bin 1", "Bin 2", "Bin 3"]
ONLY_BIN_LABELS = ["Bin 1", "Bin 2", "Bin 3"]

def get_age_bins_indices(ages):
    """
    Locate the subjects/indicies where the condition is true.
    """
    bin_1 = np.where(ages <= 9)
    bin_2 = np.where(np.logical_and(9 < ages, ages <= 12))
    bin_3 = np.where(12 < ages)
    bin_indices = [bin_1, bin_2, bin_3]
    
    return bin_indices


def bin_by_age(X, y, ages):
    """
    Bin the dataset by age.
    
    Returns three age bins: 6-> 9, 9 -> 12, and 12 -> 16.
    """
    bin_indices = get_age_bins_indices(ages)
    
    # Bin the data by those indices
    if y.ndim == 1:
        bins = [(X[bin_index], y[bin_index]) for bin_index in bin_indices]
    else:
        bins = [(X[bin_index], y[bin_index, :]) for bin_index in bin_indices]

    return bins


def bin_data(X, y, ages=None):
    """
    Bin the dataset by age if ages is given.
    
    Returns either the original data or the binned data.
    """
    if ages is not None and ages.any():
        bins = bin_by_age(X, y, ages)
        bin_1, bin_2, bin_3 = bins[0], bins[1], bins[2]
#         X_all = [X, bin_1[0], bin_2[0], bin_3[0]]
#         y_all = [y, bin_1[1], bin_2[1], bin_3[1]]
#         bin_labels = BIN_LABELS

        X_all = [bin_1[0], np.concatenate((bin_2[0], bin_3[0]), axis=0)]
        y_all = [bin_1[1], np.concatenate((bin_2[1], bin_3[1]), axis=0)]
        bin_labels = ["Bin 1", "Bin 2 + 3"]
    else:
        X_all = [X]
        y_all = [y]
        bin_labels = ["All"]
    
    return X_all, y_all, bin_labels
