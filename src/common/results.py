"""
Holds the functions for saving and loading the model's results and permutation test results.
"""
from os.path import join, exists

import numpy as np
import pandas as pd


class Result:
    """
    Class containing the results from modeling.

    Used to keep the reporting of results consistent across models and
    methodologies.
    """
    def __init__(self, model, target, train, test, score, pvalue):
        """
        Initializes the class with a set of results.

        Parameters
        ----------
        model : str
        target : str
        train : str
        test : str
        score : float
        pvalue : float

        """
        self.model = model
        self.target = target
        self.train = train
        self.test = test
        self.score = score
        self.pvalue = pvalue

    def to_dict(self):
        """
        Converts the class into a dictionary.

        Returns
        -------
        dict

        """
        return {
            'Model': self.model,
            'Target': self.target,
            'Train': self.train,
            'Test': self.test,
            'Score': self.score,
            'P-value': self.pvalue
        }


class CVResult(Result):
    """
    Class containing the results from cross-validation modeling.

    Used to keep the reporting of results consistent across models and
    methodologies.
    """
    def __init__(
            self, model, target, train, test, score, pvalue, population,
            n_permutations):
        """
       Initializes the class with a set of results.

        Parameters
        ----------
        model : str
        target : str
        train : str
        test : str
        score : float
        pvalue : float
        population : str
        n_permutations : int

        """
        super().__init__(model, target, train, test, score, pvalue)
        self.population = population
        self.n_permutations = n_permutations

    def to_dict(self):
        """
        Converts the class into a dictionary.

        Returns
        -------
        dict

        """
        result = super().to_dict()
        result['Population'] = self.population
        result['Num Permutations'] = self.n_permutations

        return result

    def to_string(self):
        """
        Converts the class into a string.

        Returns
        -------
        str

        """
        result = f"""
        Model: {self.model}, Target: {self.target}, Train: {self.train}, 
        Test: {self.test}, Population: {self.population}, 
        Num Perm: {self.n_permutations}"""

        return result


def save_results(results, fn, output_folder, append=False):
    """
    Saves the results to a csv file.

    If the csv file exists, then append the results to that file.

    Parameters
    ----------
    results : pd.DataFrame
    fn : str
    output_folder : str
    append : bool, optional.

    Returns
    -------
    output_path : str

    """
    if not fn.endswith('.csv'):
        fn += '.csv'
    output_path = join(output_folder, fn)

    m = 'a' if exists(output_path) and append else 'w'
    h = False if m == 'a' else True
    results.to_csv(output_path, mode=m, header=h)

    return output_path


def load_results(fn, input_folder):
    """
    Loads the results from a csv file.

    Parameters
    ----------
    fn : str
    input_folder : str

    Returns
    -------
    results : pd.Dataframe
    input_path : str

    """
    if not fn.endswith('.csv'):
        fn += '.csv'
    input_path = join(input_folder, fn)
    results = pd.read_csv(input_path, index_col=0)

    return results, input_path


def save_perm_score(perm_scores, fn, output_folder):
    """
    Saves the permutation scores to a NumPy array file.

    Parameters
    ----------
    perm_scores : np.array
    fn : str
    output_folder : str

    Returns
    -------
    output_path : str

    """
    if not fn.endswith('.npy'):
        fn += '.npy'
    output_path = join(output_folder, fn)
    np.save(output_path, perm_scores)

    return output_path


def load_perm_score(fn, input_folder):
    """
    Loads the permutation scores from a NumPy array file.

    Parameters
    ----------
    fn : str
    input_folder : str

    Returns
    -------
    perm_scores : np.array

    """
    if not fn.endswith('.npy'):
        fn += '.npy'
    input_path = join(input_folder, fn)
    perm_scores = np.load(input_path)

    return perm_scores
