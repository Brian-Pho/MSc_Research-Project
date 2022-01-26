from os.path import join, exists


class Result:
    def __init__(self, model, target, train, test, score, pvalue):
        self.model = model
        self.target = target
        self.train = train
        self.test = test
        self.score = score
        self.pvalue = pvalue
    
    def to_dict(self):
        return {
            'Model': self.model,
            'Target': self.target,
            'Train': self.train,
            'Test': self.test,
            'Score': self.score,
            'P-value': self.pvalue
        }


class CVResult(Result):
    def __init__(self, model, target, score, pvalue, population):
        super().__init__(model, target, score, pvalue)
        self.population = population
    
    def to_dict(self):
        result = super().to_dict()
        result['Population'] = self.population
        return result

    
def save_results(results, fn, output_folder):
    output_path = join(output_folder, fn)
    output_exists = exists(output_path)
    m = 'a' if output_exists else 'w'
    results.to_csv(output_path, mode=m, header=not output_exists)
