__author__ = 'victor'
import re



'''


HIGHLY EXPERIMENTAL!!!!!! DON'T USE


'''


def match_arff(map_from, to_map):
    '''
    giver an arff the same header as other arff file (doesn't check if attributes are in the same order)
    :param map_from:
    :param to_map:
    :return:
    '''
    with open(map_from, 'r') as arff_1, open(to_map, 'r') as arff_2, open(to_map[:-5] + '_mapped.arff') as out_arff:
        source = arff_1.read()
        target = arff_2.read()

        source_header = re.split(r'@data', source, re.IGNORECASE)[0]
        data_target = re.split(r'@data', target, re.IGNORECASE)[1]

        print>>out_arff, source_header
        print>>out_arff, data_target

    return
