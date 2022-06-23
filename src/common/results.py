from os.path import join, exists
import numpy as np
import pandas as pd


class Result:
    """
    Holds the results from modeling.
    
    Used to keep the reporting of results consistent across models and methodologies.
    """
    def __init__(self, model, target, train, test, score, pvalue):
        """
        Initializes the class with the results.
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
    def __init__(self, model, target, train, test, score, pvalue, population, n_permutations):
        """
        Initializes the class with the results.
        """
        super().__init__(model, target, train, test, score, pvalue)
        self.population = population
        self.n_permutations = n_permutations
    
    def to_dict(self):
        """
        Converts the class into a dictionary.
        """
        result = super().to_dict()
        result['Population'] = self.population
        result['Num Permutations'] = self.n_permutations
        return result
    
    def to_string(self):
        """
        Converts the class into a string.
        """
        result = f'Model: {self.model}, Target: {self.target}, Train: {self.train}, Test: {self.test}, Population: {self.population}, Num Perm: {self.n_permutations}'
        return result
        
    
def save_results(results, fn, output_folder, append=False):
    """
    Saves by appending the modeling results to a csv file.
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
    Loads modeling results from a csv file.
    """
    if not fn.endswith('.csv'):
        fn += '.csv'
    input_path = join(input_folder, fn)
    results = pd.read_csv(input_path, index_col=0)
    return results, input_path


def save_perm_score(perm_scores, fn, output_folder):
    """
    Saves the permutation scores to a NumPy array file.
    """
    if not fn.endswith('.npy'):
        fn += '.npy'
    output_path = join(output_folder, fn)
    np.save(output_path, perm_scores)
    return output_path


def load_perm_score(fn, input_folder):
    """
    Loads a NumPy array file of permutation scores.
    """
    if not fn.endswith('.npy'):
        fn += '.npy'
    input_path = join(input_folder, fn)
    perm_scores = np.load(input_path)
    return perm_scores
