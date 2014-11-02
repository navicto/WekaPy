__author__ = 'Victor'
from weka_utils.weka_cl.command import WekaCommand
from os.path import split, join
from os import listdir

class MultiFilterCommand(WekaCommand):
    '''
    Generates weka commands to apply multiple filters to an arff file
    '''
    def __init__(self, heap, cp):
        super(MultiFilterCommand, self).__init__(heap=heap, cp=cp)
        self._string += ' weka.filters.MultiFilter '
    def add_filter(self, w_filter, options):
        self.add2command(' -F "' + w_filter + ' ')
        if options:
            for option, value in options:
                self.add2command(' -' + option + ' ' + value)
            self.add2command('" ')
    def set_source(self, source):
        self._source = source
    def set_output(self, out_path):
        self._output = out_path

#Use case, help arturo apply multifilters to several arff files
# def arturo_multifilters(source, output, heap='16g', cp=None):
#     cl = MultiFilterCommand(heap=heap, cp=cp)
#     cl.add_filter('weka.filters.supervised.attribute.Discretize', [('R' , 'first-last')])
#     cl.add_filter('weka.filters.unsupervised.attribute.RemoveUseless', [('M', '100.0')])
#     cl.add_filter('weka.filters.supervised.attribute.AttributeSelection',
#                   [('E', '\\"weka.attributeSelection.ReliefFAttributeEval -W -M -1 -D 1 -K 10 -A 2\\"'),
#                    ('S', '\\"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N 30\\"')])
#     cl.add2command(' -c last')
#     cl.set_source(source)
#     cl.add2command(' -i ' + cl._source)
#     cl.set_output(output)
#     file_name = split(cl._source)[-1][:-5]
#     cl.add2command(' -o ' + file_name)
#     cl.execute(verbose=True, shell=True)
#
# data_dir = '/Users/Victor/Desktop/folds_arturo'
# arff_files = listdir(data_dir)
# arff_files = [f for f in arff_files if f.endswith('.arff')]
# cp = '/Users/Victor/"Box Sync"/DBMI/ResearchProject/weka3-7-10/weka.jar'
# heap = '2g'
#
# for f in arff_files:
#     arturo_multifilters(source=join(data_dir, f), output=join(data_dir, 'filtered', f), heap=heap, cp=cp)