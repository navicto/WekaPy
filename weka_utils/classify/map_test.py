__author__ = 'victor'
from weka_utils.arff import reorder
from weka_utils.arff import rm_features
import subprocess

def format_test_arff(train, test, out_path, weka_cp, heap):
    '''
    Maps a test arff so it has the same features and in the same order of a training arff file
    :param train: training arff
    :param test: test arff
    :param out_path: new, filtered and reformatted arff
    :return:
    '''
    #remove useless features
    attrs_train = reorder.arff_features(train)
    rm_path = 'training_remove.arff'
    rm_cl = rm_features.rm_features(source = test, out_path = rm_path,
                                rm_by='name', features=attrs_train, heap=heap, cp=weka_cp, reverse=True)
    rm_cl.execute(verbose=True, shell=True)
    #reorder
    reorder_cl = reorder.reorder(arff_path=rm_path, out_path=out_path, feature_order=attrs_train, order_by='Name',
                  weka_cp=weka_cp, heap=heap)
    reorder_cl.execute(verbose=True, shell=True)
    #delete temp file
    subprocess.call('rm ' + rm_path, shell=True)
    return
