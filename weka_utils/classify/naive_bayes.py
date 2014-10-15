__author__ = 'Victor'

from weka_utils.classify.classifier import ClassifierCommand, FilteredClassifierCommand

def nbayes(training, output_predictions, output_model=None, crossval=False, nFolds=1, test=None, classifier_opts=None,
                decimals=6, heap='16g', cp=None):
    '''
    Train a naive bayes classifier. You can specify whether to output the model to a .model file
    :param training: training dataset
    :param output_predictions: file that will contain predictions of the classifier
    :param output_model: optional, .model file to save the trained model
    :param crossval: boolean, whether to do crossvalidation for generating predictions
    :param nFolds: optional, number of folds for crossvalidation
    :param test: optional, test dataset
    :param classifier_opts: additional options for the classifier. e.g., [(option, value),...]
    :param decimals: number of decimal points to include in prediction probabilities
    :param heap: maximum memory for java heap
    :param cp: classpath to weka.jar
    :return: cl, weka command ready to be executed
    '''
    cl = ClassifierCommand(heap=heap, cp=cp)
    cl.set_training(training)
    cl.set_test(test)
    cl.set_output(out_predictions=output_predictions, out_model=output_model)
    cl.set_classifier('weka.classifiers.bayes.NaiveBayes', options=classifier_opts)
    if crossval:
        cl.add2command(' -x ' + str(nFolds) + ' ')
    cl.add2command(' -t ' + cl._training)
    if cl._test:
        cl.add2command(' -T ' + cl._test + ' ')
    if cl._output_model:
        cl.add2command(' -d ' + cl._output_model + ' ')
    cl.add2command('-p -classifications "weka.classifiers.evaluation.output.prediction.CSV -distribution -decimals ')
    cl.add2command(str(decimals) + '" > ' + cl._output_predictions)

    return cl

def nbayes_feature_subset(training, output_predictions, features, classifier_opts=None, heap='16g', cp=None, test=None,
                          output_model=None, crossval=False, nFolds=1, decimals=6):
    '''
    Train a naive Bayes classifier using only a subset of featuers, specified by indices. e.g., '1,2,3,last'
    :param training: training dataset
    :param output_predictions: specify file to save predictions
    :param features: features to be used in the classifier (indices separated by commas)
    :param classifier_opts: options for the naive Bayes classifier. Format --> [(option, value),...]
    :param heap: maximum memory for java heap
    :param cp: classpath to weka.jar
    :param test: Optional. Default=None. Test dataset for predictions
    :param output_model: Boolean. Whether to save the model (.model file)
    :param crossval: whether to use crossvalidation for testing
    :param nFolds: number of folds for crossvalidation
    :param decimals: number of decimal points to use for probabilities in the prediction file
    :return: cl. Weka command ready to be executed
    '''
    cl = FilteredClassifierCommand(heap=heap, cp=cp)
    cl.set_training(training)
    cl.set_test(test)
    cl.set_output(out_predictions=output_predictions, out_model=output_model)
    if 'last' not in features:
        features += ',last'
    if crossval:
        cl.add2command(' -x ' + str(nFolds) + ' ')
    cl.add2command(' -t ' + cl._training)
    if cl._output_model:
        cl.add2command(' -d ' + cl._output_model + ' ')
    if cl._test:
        cl.add2command(' -T ' + cl._test + ' ')
    cl.add2command('-p -classifications "weka.classifiers.evaluation.output.prediction.CSV -distribution -decimals ' + str(decimals) + '" ')
    cl.set_filter('weka.filters.unsupervised.attribute.Remove', [('V', ''), ('R', features)])
    cl.set_classifier('weka.classifiers.bayes.NaiveBayes', options=classifier_opts)
    cl.add2command(' > ' + cl._output_predictions)

    return cl



#demos
#naive bayes classifier
# cp = '/Users/Victor/"Box Sync"/DBMI/ResearchProject/weka3-7-10/weka.jar'
# heap = '2g'
# source = '/Users/Victor/Desktop/weather.nominal.arff'
# out_predictions = '/Users/Victor/Desktop/predictions.csv'
# out_model = '/Users/Victor/Desktop/naiveBayes_5.model'
# crossval = True
# nfolds = 10
# classifier_opts = None
# test_file = source
# cl = nbayes(training=source, output_predictions=out_predictions, output_model=out_model, crossval=crossval, nFolds=nfolds,
#             test=test_file, classifier_opts=classifier_opts,decimals=6, heap=heap, cp=cp)
# cl.execute(verbose=True, shell=True)

#Naive bayes classifier using only a subset of features
# cp = '/Users/Victor/"Box Sync"/DBMI/ResearchProject/weka3-7-10/weka.jar'
# heap = '2g'
# source = '/Users/Victor/Desktop/weather.nominal.arff'
# out_predictions = '/Users/Victor/Desktop/predictions.csv'
# out_model = '/Users/Victor/Desktop/naiveBayes_4.model'
# crossval = True
# nfolds = 10
# classifier_opts = None
# test_file = source
# features = '1,4,last'
# cl = nbayes_feature_subset(source, out_predictions, features, classifier_opts=classifier_opts, heap=heap, cp=cp, test=test_file,
#                           output_model=out_model, crossval=True, nFolds=nfolds, decimals=6)
# cl.execute(verbose=True, shell=True)
