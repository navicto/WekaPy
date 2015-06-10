__author__ = 'Victor'
'''
Discretize ARFF
'''
from os.path import join, expanduser
import sys
home_dir = expanduser('~')
sys.path.append(join(home_dir, 'PycharmProjects', 'WekaPy'))
sys.path.append(join(home_dir, 'PycharmProjects', 'HospitalReadmission'))
from weka_utils.weka_cl.command import WekaCommand

class DiscretizeCommand(WekaCommand):
    def __init__(self, heap='16g', cp=None):
        super(DiscretizeCommand, self).__init__(heap=heap, cp=cp)
    def set_source(self, source):
        self._source = source
    def set_output(self, out_path):
        self._output = out_path
    def set_features(self, features):
        self._features = [str(f) for f in features]

def discretize(source, out_path, features=None, precision=6, reverse = False, heap='16g', cp=None):
    '''
    ATTENTION: DOCUMENTATION COPIED AND PASTED FROM THE REMOVE FILTER, SO TAKE IT WITH A GRAIN OF SALT
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
    cl = DiscretizeCommand(heap=heap, cp=cp)
    cl.set_source(source)
    cl.set_output(out_path)
    cl.set_features(features)

    if features:
        cl.add2command(' weka.filters.supervised.attribute.Discretize -R "%s" ' %','.join(cl._features))
    else:
        cl.add2command(' weka.filters.supervised.attribute.Discretize -R "%s" ' %'first-last')
    cl.add2command('-precision ' + str(precision) + ' ')

    if reverse:
        cl.add2command(' -V ')
    cl.add2command('-c last -i ' + cl._source + ' -o ' + cl._output)

    return cl



def main():
    source = "C:\\Users\\Victor\\Desktop\\LAB\\training.arff"
    weka_cp = '"C:\\Users\\Victor\\Box Sync\\DBMI\\ResearchProject\\weka3-7-10\\weka.jar"'
    features = range(1, 76)
    precision = 6
    cl = discretize(source=source, out_path="C:\\Users\\Victor\\Desktop\\discretized.arff",
               features=features, reverse=False, heap="16g", cp=weka_cp, precision=precision)
    cl.execute(verbose=True, shell=True)

if __name__ == '__main__':
    main()
