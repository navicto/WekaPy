__author__ = 'Victor'
from weka_utils.weka_cl.command import WekaCommand

class ClassifierCommand(WekaCommand):
    '''
    Initialize and execute weka commands for running classifiers
    '''
    def __init__(self, heap='16g', cp=None):
        super(ClassifierCommand, self).__init__(heap=heap, cp=cp)

    def set_training(self, training_set):
        self._training = training_set

    def set_test(self, test_set):
        self._test = test_set

    def set_output(self, out_predictions, out_model):
        self._output_predictions = out_predictions
        self._output_model = out_model

    def set_classifier(self, classifier, options=None):
        self._classifier = classifier
        self._classifier_opts = options
        self._string += ' ' + self._classifier + ' '
        if self._classifier_opts:
            for option, value in self._classifier_opts:
                self._string += '-' + option + ' ' + str(value) + ' '

class FilteredClassifierCommand(ClassifierCommand):
    '''
    Initialize and execute weka commands for running filtered classifiers
    '''
    def __init__(self, heap='16g', cp=None):
        super(FilteredClassifierCommand, self).__init__(heap=heap, cp=cp)
        self._string += 'weka.classifiers.meta.FilteredClassifier '

    def set_filter(self, w_filter, options=None):
        self._filter = w_filter
        self._filter_opts = options
        self._string += ' -F "' + self._filter + ' '
        if self._filter_opts:
            for option, value in self._filter_opts:
                self._string += '-' + option + ' ' + value + ' '
        self._string += '" '

    def set_classifier(self, classifier, options=None):
        self._classifier = classifier
        self._classifier_opts = options
        self._string +=  ' -W ' + classifier + ' -- '
        if self._classifier_opts:
            for option, value in self._classifier_opts:
                self._string += '-' + option + ' ' + str(value) + ' '