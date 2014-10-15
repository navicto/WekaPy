__author__ = 'Victor'
from weka_utils.weka_cl.command import WekaCommand
import re

class SingleFeatureEvaluator(WekaCommand):
    '''
    Generates weka command for generating feature rankings using methods that evaluate single features, e.g., InfoGain
    '''
    def __init__(self, heap='16g', cp=None):
        super(SingleFeatureEvaluator, self).__init__(heap=heap, cp=cp)
        self._ranking = None

    def ranking_method(self, method, options):
        '''
        :param method: Evaluator/ranking method. e.g.,  weka.attributeSelection.InfoGainAttributeEval
        :param options: parameters for evaluator/ranking [(name, value), ...] e.g., [('N', '-1'), ...]
        '''
        self._ranking = method
        self._ranking_opts = options
        self._string += ' ' + self._ranking + ' '
        if self._ranking_opts:
            for option, value in self._ranking_opts:
                self._string += '-' + option + ' ' + str(value) + ' '

    def search_method(self, method, options):
        '''
        :param method: search method to be used in conjuction with evaluator. e.g.,  weka.attributeSelection.Ranker
        :param options: parameters for search [(name, value), ...] e.g., [('T', '-1.8E89'), ...]
        '''
        if not self._ranking:
            raise AttributeError("Attributes _ranking_method and _ranking_opts must be defined with ranking_method() "
                                 "before specifying search method ")
        self._search = method
        self._search_opts = options
        self._string += ' -s "' + self._search + ' '
        if self._search_opts:
            for option, value in self._search_opts:
                self._string += '-' + option + ' ' + str(value) + ' '
        self._string += '"'

    def set_source(self, source):
        '''
        :param source: source arff file form which features will be ranked
        '''
        self._source = source

    def set_output(self, out_path):
        '''
        :param out_path: specify output file (*.txt or other simple text format)
        '''
        self._output = out_path

class WrapperSubsetEval(WekaCommand):
    '''
    Incrementally builds a weka command for performing feature selection with the wrapper subset evaluation technique
    '''
    def __init__(self, heap='16g', cp=None):
        super(WrapperSubsetEval, self).__init__(heap=heap, cp=cp)
        self._string += ' weka.attributeSelection.WrapperSubsetEval -B '

    def set_search(self, search_class, search_opts):
        self._searh = search_class
        self._search_opts = search_opts
        self._string += " "

    def set_classifier(self, classifier_class, classifier_opts = None):
        self._classifier = classifier_class
        self._classifier_opts = classifier_opts
        self._string += ' ' + self._classifier + ' '
        if self._classifier_opts:
            for option, value in self._classifier_opts:
                self._string += '-' + option + ' ' + str(value) + ' '


     # weka.attributeSelection.WrapperSubsetEval -s "weka.attributeSelection.GreedyStepwise -B -T -1.7976931348623157E308 -N -1 -num-slots 1" -B weka.classifiers.bayes.NaiveBayes -F 9 -T 0.01 -R 47 -E acc -- -D

class FeatureRanking(object):
    '''
    Reads a text file containing feature rankings (created with weka), and creates an object with rankings by index or
    name.
    '''
    def __init__(self, ranking_path):
        self._ranking_indices, self._ranking_names = [], []
        with open(ranking_path, 'r') as ranking_file:
            while 'Ranked attributes:' not in ranking_file.next():
                continue
            for line in ranking_file:
                if line.strip(): #line not blank
                    f_index, f_name = re.search(r'0\.\d+\s+(\d+)\s+(\w+)', line).groups()
                    self._ranking_indices += [f_index]
                    self._ranking_names += [f_name]
                    continue
                else:
                    break

    def subset_index(self, begin, end, exclude):
        candidates = self._ranking_indices[begin - 1:end]
        return [f for f in candidates if (candidates.index(f) + 1) not in exclude]

    def subset_names(self, begin, end, exclude):
        candidates = self._ranking_names[begin - 1:end]
        return [f for f in candidates if (candidates.index(f) + 1) not in exclude]






#Sample of how to use the FeatureRanking class
# ranking = FeatureRanking('/Users/Victor/Desktop/ranking_2.txt')
# print ranking._ranking_indices, ranking._ranking_names
# print ranking.subset_names(1,4,[2])

