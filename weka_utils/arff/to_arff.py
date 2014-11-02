__author__ = 'Victor'
import numpy as np
import copy
def dataframe2ARFF(data, attr_spec, out_path, missing_to='?'):
    '''
    Creates an arff file from a pandas DataFrame
    :param data_copy: pandas DataFrame containing data
    :param attr_spec: specification (dictionary) of data type for arff file. E.g., for numeric attr = 'NUMERIC', for
    dates = 'DATE "yyyy-MM-dd HH:mm:ss"' DO NOT SPECIFY IF ATTRIBUTE IS NOMINAL
    :param out_path: path where arff file will be saved
    :return:
    '''
    #replace missing values in data
    data_copy = data.copy()
    data_copy.fillna('?')
    #open file and declare relation (file info)
    with open(out_path, 'w') as out_arff:
        print>>out_arff, '@relation ' + out_path + '\n'

        #declare attributes in arff file
        for attr in data_copy.columns.tolist():
            if attr in attr_spec:
                print>>out_arff, '@attribute ' + attr + ' ' + attr_spec[attr]
            else:
                print>>out_arff, '@attribute ' + attr + ' ' + nominal_values(data=data_copy[attr])

        #write data to arff file
        print>>out_arff, '@data'
        for row in data_copy.iterrows():
            line = [str(item) for item in row[1].tolist()]
            print>>out_arff, ','.join(replace_missing(line=line, new_value=missing_to))

    print 'created file: ', out_path

def nominal_values(data):
    '''
    Extracts the values of a nominal variable
    :param data: pandas dataframe containing the variable with its instantiations
    :return: string for arff constructions. e.g., "{male,female}"
    '''
    values = data.unique().tolist()
    # print data
    # print '{' + ','.join([str(x) for x in values if x and x not in [np.nan, 'nan', 'NaN', 'NAN']]) + '}'
    return '{' + ','.join([str(x) for x in values if x not in [np.nan, 'nan', 'NaN', 'NAN', '?']]) + '}'

def replace_missing(line, new_value):
    '''
    Replaces values in line with new_value
    :param line: list containing values of a data line
    :param new_value: value to replace missing dta with
    :return: new_line, where missing values have been replaced
    '''
    missing_values = ['nan', 'NaN', 'NAN']
    if any((x in missing_values) for x in line):
        new_line = []
        for value in line:
            if value not in missing_values:
                new_line += [value]
            else:
                new_line += [new_value]
        return new_line
    else:
        return line









