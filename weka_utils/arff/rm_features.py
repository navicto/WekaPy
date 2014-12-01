__author__ = 'Victor'
'''
Removes attributes of an *.arff dataset
'''
from weka_utils.weka_cl.command import WekaCommand

class RemoveCommand(WekaCommand):
    def __init__(self, heap='16g', cp=None):
        super(RemoveCommand, self).__init__(heap=heap, cp=cp)
    def rm_by(self, rm_type):
        self._rm_by = rm_type #options {'name', 'index'}
    def set_source(self, source):
        self._source = source
    def set_output(self, out_path):
        self._output = out_path
    def set_features(self, features):
        self._remove = [str(f) for f in features]

def rm_features(source, out_path, rm_by, features, reverse = False, heap='16g', cp=None):
    '''
    Removes features from *.arff dataset, whether by name, or by index (arff index)
    :param source: path to *.arff dataset
    :param out_path: destination arff
    :param rm_by: either name or index
    :param features: set of features (names or indices) to remove from source
    ;param reverse (boolean): whether to reverse selection (keep features instead of removing them)
    :param heap: maximum memory for java heap
    :param cp: classpath to weka.jar
    :return: cl: weka command ready to execute (with cl.execute())
    '''
    #initialize remove command
    cl = RemoveCommand(heap=heap, cp=cp)
    cl.set_source(source)
    cl.set_output(out_path)
    cl.rm_by(rm_by)
    cl.set_features(features)

    if cl._rm_by == 'name':
        cl.add2command(' weka.filters.unsupervised.attribute.RemoveByName -E "%s"' %'|'.join(cl._remove))
    elif cl._rm_by == 'index':
        cl.add2command(' weka.filters.unsupervised.attribute.Remove -R %s' %','.join(cl._remove))
    else:
        raise AttributeError('Remove by attribute either not specified, or differnet from "name" or "index"')
    if reverse:
        cl.add2command(' -V ')
    cl.add2command(' -i ' + cl._source + ' -o ' + cl._output)

    return cl

# #sample of how to use this function
# cp = '/Users/Victor/"Box Sync"/DBMI/ResearchProject/weka3-7-10/weka.jar'
# heap = '2g'
# source = '/Users/Victor/Desktop/weather.nominal.arff'
# out_path = '/Users/Victor/Desktop/weather.nominal_rm_1_3.arff'
# rm_by = 'index'
# features = [1,3]
# reverse = False
#
# cl = rm_features(source, out_path, rm_by, features, heap=heap, cp=cp, reverse=reverse)
# print cl
# # cl.execute(verbose=True, shell=True)

