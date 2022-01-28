from os.path import join, exists


class Result:
    """
    Hold the results from modeling.
    
    Used to keep the reporting of results consistent across models and methodologies.
    """
    def __init__(self, model, target, train, test, score, pvalue):
        """
        Initialize the class with the results.
        """
        self.model = model
        self.target = target
        self.train = train
        self.test = test
        self.score = score
        self.pvalue = pvalue
    
    def to_dict(self):
        """
        Convert the class into a dictionary.
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
        Initialize the class with the results.
        """
        super().__init__(model, target, train, test, score, pvalue)
        self.population = population
        self.n_permutations = n_permutations
    
    def to_dict(self):
        """
        Convert the class into a dictionary.
        """
        result = super().to_dict()
        result['Population'] = self.population
        result['Num Permutations'] = self.n_permutations
        return result

    
def save_results(results, fn, output_folder):
    """
    Save the modeling results to a csv file.
    """
    output_path = join(output_folder, fn)
    output_exists = exists(output_path)
    m = 'a' if output_exists else 'w'
    results.to_csv(output_path, mode=m, header=not output_exists)
    return output_path
