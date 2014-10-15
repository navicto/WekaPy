__author__ = 'Victor'
from weka_utils.weka_cl.command import WekaCommand
from os.path import join

class FilterFolds(WekaCommand):
    '''
    Initialize and execute weka commands for running classifiers
    '''
    def __init__(self, heap='16g', cp=None):
        super(FilterFolds, self).__init__(heap=heap, cp=cp)

    def set_training(self, training_set):
        self._training = training_set
        self._string += ' -i ' + self._training

    def set_out_dir(self, out_dir):
        self._out_dir = out_dir

    def set_filter(self, w_filter, options=None):
        self._filter = w_filter
        self._filter_opts = options
        self._string += ' ' + self._filter + ' '
        if self._filter_opts:
            for option, value in self._filter_opts:
                self._string += '-' + option + ' ' + str(value) + ' '


def filter_folds(training_set, out_dir, seed=0, nFolds=10, heap='16g', cp=None):
    for fold in range(1, nFolds + 1):
        cl = FilterFolds(heap=heap, cp=cp)
        cl.set_filter('weka.filters.supervised.instance.StratifiedRemoveFolds', [('S', seed), ('F', fold)])
        cl.set_training(training_set)
        cl.set_out_dir(out_dir)
        cl.add2command(' -o ' + join(out_dir, 'test_fold' + str(fold) + '.arff') + ' -c last')
        cl.execute(verbose=True, shell=True)

        cl_v = FilterFolds(heap=heap, cp=cp)
        cl_v.set_filter('weka.filters.supervised.instance.StratifiedRemoveFolds', [('V', ''),('S', seed), ('F', fold)])
        cl_v.set_training(training_set)
        cl_v.set_out_dir(out_dir)
        cl_v.add2command(' -o ' + join(out_dir, 'train_fold' + str(fold) + '.arff') + ' -c last')
        cl_v.execute(verbose=True, shell=True)






cp = '/Users/Victor/"Box Sync"/DBMI/ResearchProject/weka3-7-10/weka.jar'
heap = '2g'
source = '/Users/Victor/Desktop/TCGA-methy-adc-scc.arff'
out_dir = '/Users/Victor/Desktop/folds_arturo'

filter_folds(training_set=source, out_dir=out_dir, seed=0, nFolds=10, heap=heap, cp=cp)