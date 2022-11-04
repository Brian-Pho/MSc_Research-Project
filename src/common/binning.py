import numpy as np

BIN_LABELS = ["All", "Bin 1", "Bin 2", "Bin 3"]
ONLY_BIN_LABELS = ["Bin 1", "Bin 2", "Bin 3"]
EQUAL_BIN_LABELS = ["Bin 1", "Bin 2 Equal", "Bin 3"]


def get_age_bins_indices(ages, num_bins):
    """
    Gets the indices that bins the participant by age.

    This does not return the samples binned by age, but the age bins
    containing indices of samples. To actually bin the data by age, use the
    list returned by this function and index the samples or use bin_by_age().

    Parameters
    ----------
    ages : np.array
        List of participant ages.
    num_bins : int
        Number of age bins.

    Returns
    -------
    bin_indices : list
        List where the length is num_bins and each element is a list of
        indices for each age bin.

    """
    bin_indices = []

    if num_bins == 3:
        bin_1 = np.where(ages <= 9)
        bin_2 = np.where(np.logical_and(9 < ages, ages <= 12))
        bin_3 = np.where(12 < ages)
        bin_indices = [bin_1, bin_2, bin_3]
    elif num_bins == 2:
        bin_1 = np.where(ages <= 10)
        bin_2 = np.where(10 < ages)
        bin_indices = [bin_1, bin_2]

    return bin_indices


def bin_by_age(X, y, ages, num_bins):
    """
    Bins the data by age.

    Parameters
    ----------
    X : np.array
    y : np.array
    ages : np.array
    num_bins : int

    Returns
    -------
    bins: list
        List where it's length is equal to the number of age bins and each
        element is a list of tuples containing the samples and targets for
        that age bin.

    Notes
    -----
    Typically bins the data into three age bins: 6-8, 9-11, and 12-16.

    """
    bin_indices = get_age_bins_indices(ages, num_bins)

    if y.ndim == 1:
        bins = [(X[bin_index], y[bin_index]) for bin_index in bin_indices]
    else:
        bins = [(X[bin_index], y[bin_index, :]) for bin_index in bin_indices]

    return bins


def bin_data(X, y, ages=None, include_all=False, num_bins=3):
    """
    Bins the data by age or returns the original data.

    Used to wrap the bin_by_age() function when running multiple modeling
    sessions.

    Parameters
    ----------
    X : np.array
    y : np.array
    ages : np.array, optional
    include_all : bool, optional
    num_bins : int, optional

    Returns
    -------
    tuple
        A tuple containing the samples, targets, and bin labels

    """
    if ages is not None and ages.any():
        bins = bin_by_age(X, y, ages, num_bins)

        X_bins, y_bins, bin_labels = [], [], []

        if include_all:
            X_bins.append(X)
            y_bins.append(y)
            bin_labels.append('All')

        for bin_num, age_bin in enumerate(bins, start=1):
            X_bins.append(age_bin[0])
            y_bins.append(age_bin[1])
            bin_labels.append(f'Bin {bin_num}')

    else:
        X_bins = [X]
        y_bins = [y]
        bin_labels = ["All"]

    return (np.array(X_bins, dtype=object), np.array(y_bins, dtype=object),
            np.array(bin_labels, dtype=object))
