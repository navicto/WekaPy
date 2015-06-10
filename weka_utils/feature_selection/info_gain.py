__author__ = 'Victor'

from weka_utils.feature_selection.rank_features import SingleFeatureEvaluator


def info_gain(source, output, crossval=False, nfolds='1', threshold='-1.7E308', N_keep='-1', start_set=None, heap='32g',
              cp=None, missingAsCategory=False):
    '''
    :param source: arff source file
    :param output: file containing output ranking (should be text format)
    :param crossval: Whether to do crossvalidation (boolean)
    :param nfolds:  folds for crossvalidation
    :param threshold: minimum InfoGain value to include features in ranking
    :param N_keep: number of features to retain in the model
    :param start_set: features to ignore (by index). e.g., '1,2,32'
    :param heap: max memory for java heap
    :param cp: classpath to weka.jar
    :return cl: weka command for feature selection, ready to be executed (cl.execute())
    '''
    cl = SingleFeatureEvaluator(heap=heap, cp=cp)
    cl.ranking_method('weka.attributeSelection.InfoGainAttributeEval', None)
    cl.set_source(source)
    cl.set_output(output)
    options = []
    if start_set:
        options += [('P', start_set)]
    cl.search_method('weka.attributeSelection.Ranker', options + [('T', threshold), ('N', N_keep)])
    if crossval:
        cl.add2command(' -x ' + str(nfolds) + '')
    if missingAsCategory:
        cl.add2command(' -M ')
    cl.add2command(' -i ' + cl._source + ' > ' + cl._output)

    return cl

#sample of how to use info_gain function
# cp = '/Users/Victor/"Box Sync"/DBMI/ResearchProject/weka3-7-10/weka.jar'
# heap = '2g'
# source = '/Users/Victor/Desktop/weather.nominal.arff'
# out_path = '/Users/Victor/Desktop/ranking.txt'
# threshold = '0'
# keep = '-1'
# crossval = True
# nfolds = 10
# cl = info_gain(source, out_path, crossval=crossval, nfolds=nfolds, threshold=threshold, N_keep=keep, start_set=None, heap='32g', cp=cp)
# cl.execute(verbose=True, shell=True)