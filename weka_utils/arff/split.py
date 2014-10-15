from __future__ import division
__author__ = 'Victor'
'''
Random split of an *.arff dataset
'''

from weka_utils.weka_cl import command
from copy import deepcopy
from os.path import join
from os import remove
import merge

class SplitCommand(command.WekaCommand):
    def __init__(self, heap='16g', cp=None):
        super(SplitCommand, self).__init__(heap=heap, cp=cp)
        self._string += ' weka.filters.MultiFilter -F "weka.filters.unsupervised.instance.RemoveWithValues -C last -L '
    def set_percentage(self, percentage):
        if isinstance(percentage, str):
            self._percentage = percentage
        else:
            self._percentage = str(percentage)
    def set_seed(self, seed):
        if isinstance(seed, str):
            self._seed = seed
        else:
            self._seed = str(seed)
    def set_source(self, in_path):
        self._source = in_path
    def set_output(self, out_path):
        self._output = out_path

def split_arff(weka_cp, source, out_dir, out_names, percentage, seed=None, java_heap='16g'):
    '''
    Percentage split of an arff file with binary class
    :param weka_cp: classpath to weka .jar
    :param source: dataset to split
    :param out_dir: directory to store split datasets
    :param out_names: names to give to split datasets. e.g., ('Training', 'Test')
    :param percentage: Percentage to split the dataset. e.g., 70
    :param seed: seed for randomizing dataset before split
    :param java_heap: max memory for java heap
    :return: names of the output files generated (out_arff1, out_arff2)
    '''

    #split command initials
    cl = SplitCommand(heap=java_heap, cp=weka_cp)
    cl.set_percentage(percentage)
    cl.set_seed(seed)
    cl.set_source(source)

    #Remove class_label=F, leave percentage % of data
    cl_true_p = deepcopy(cl)
    cl_true_p.set_output(join(out_dir, 'True' + str(percentage) + '.arff'))
    cl_true_p.add2command('1 -V" -F "weka.filters.unsupervised.instance.Randomize -S %s" -F ' %cl_true_p._seed)
    cl_true_p.add2command('"weka.filters.unsupervised.instance.RemovePercentage -P ' + cl_true_p._percentage + ' -V" -i ')
    cl_true_p.add2command(cl_true_p._source + ' -o ' + cl_true_p._output)

    #Remove class_label=F, leave (100-percentage) % of data
    cl_true_q = deepcopy(cl)
    cl_true_q.set_output(join(out_dir, 'True' + str(100 - percentage) + '.arff'))
    cl_true_q.add2command('1 -V" -F "weka.filters.unsupervised.instance.Randomize -S %s" -F ' %cl_true_q._seed)
    cl_true_q.add2command('"weka.filters.unsupervised.instance.RemovePercentage -P ' + cl_true_q._percentage + '" -i ')
    cl_true_q.add2command(cl_true_q._source + ' -o ' + cl_true_q._output)

    #Remove class_label=T, leave percentage % of data
    cl_false_p = deepcopy(cl)
    cl_false_p.set_output(join(out_dir, 'False' + str(percentage) + '.arff'))
    cl_false_p.add2command('2 -V" -F "weka.filters.unsupervised.instance.Randomize -S %s" -F ' %cl_false_p._seed)
    cl_false_p.add2command('"weka.filters.unsupervised.instance.RemovePercentage -P ' + cl_false_p._percentage + ' -V" -i ')
    cl_false_p.add2command(cl_false_p._source + ' -o ' + cl_false_p._output)

    #Remove class_label=T, leave (100-percentage) % of data
    cl_false_q = deepcopy(cl)
    cl_false_q.set_output(join(out_dir, 'False' + str(100 - percentage) + '.arff'))
    cl_false_q.add2command('2 -V" -F "weka.filters.unsupervised.instance.Randomize -S %s" -F ' %cl_false_q._seed)
    cl_false_q.add2command('"weka.filters.unsupervised.instance.RemovePercentage -P ' + cl_false_q._percentage + '" -i ')
    cl_false_q.add2command(cl_false_q._source + ' -o ' + cl_false_q._output)

    #merge dataset pieces
    #arff file with percentage % of data
    merge_cl_p = merge.merge_two(cl_true_p._output, cl_false_p._output, join(out_dir, out_names[0]), heap=java_heap, cp=weka_cp)
    #arff file with (100-percentage)% of data
    merge_cl_q = merge.merge_two(cl_true_q._output, cl_false_q._output, join(out_dir, out_names[1]), heap=java_heap, cp=weka_cp)

    return command.concatenate(cl_true_p, cl_true_q, cl_false_p, cl_false_q, merge_cl_p, merge_cl_q)

#sample of how to use this function
# cp = '/Users/Victor/"Box Sync"/DBMI/ResearchProject/weka3-7-10/weka.jar'
# heap = '2g'
# source = '/Users/Victor/Desktop/weather.nominal.arff'
# out_dir = '/Users/Victor/Desktop'
# out_names = ('Training', 'Test')
# percentage = 60
# seed = 10
# cl = split_arff(cp, source, out_dir, out_names, percentage, seed=seed, java_heap=heap)
# cl.execute(verbose=True, shell=True)