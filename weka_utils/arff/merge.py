__author__ = 'Victor'

from weka_utils.weka_cl import command

class CommandMerge(command.WekaCommand):
    pass

def merge_two(arff1, arff2, out_arff, heap='16g', cp='None'):
    '''
    Merges two arff sets with the same class and attributes
    :param arff1: path to first arff file
    :param arff2: path second arff file
    ;param out_arff: path to output arff dataset
    :param heap: maximum memory for java heap
    :param cp: classpath to weka .jar
    :return: WekaCommand object, ready to execute
    '''

    cl = command.WekaCommand(heap=heap, cp=cp)
    cl.add2command(' weka.core.Instances append ' + arff1 + ' ' + arff2 + ' > ' + out_arff)

    return cl