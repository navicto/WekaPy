__author__ = 'Victor'
import numpy as np
import subprocess
import re
import pandas as pd

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

def csv_to_arff(in_path, out_path, missing_char, attr_spec, remove_index=True):
    '''
    Converts a csv file into an arff dataset
    :param in_path: path to csv file
    :param out_path: path to output arff file
    :param missing_char: character with which to replace missing data (missing = '')
    :param attr_spec: dictionary spec of attributes (same as in dataframe2ARFF
    :param remove_index: whether the first column of each row should be suppressed (e.g., SID used as index)
    :return: None
    '''
    with open(in_path, 'r') as in_file, open(out_path, 'w') as out_file:
        print>>out_file, '@relation ' + out_path + '\n'
        header = in_file.next().strip()
        #declare attributes in arff file
        for attr in re.split(r',', header):
            if attr in attr_spec:
                print>>out_file, '@attribute ' + attr + ' ' + attr_spec[attr]
            else:
                print>>out_file, '@attribute ' + attr + ' {T,F,M}'
        print>>out_file, '\n'

        #write data to arff
        i = 1
        print>>out_file, '@data'
        for line in in_file:
            line_data = re.split(r',', line.strip())
            line_data = [x if x else missing_char for x in line_data]
            if remove_index:
                line_data[0:1] = []
            print>>out_file, ','.join(line_data)
            if i%1000 == 0: print i
            i += 1

    print 'created file: ', out_path

def ARFF2DataFrame(arff_path, weka_cp, heap='64g'):
    '''
    Creates a pandas dataframe from an arff file
    :param arff_path: path to arff file
    :param weka_cp: path to weka.jar
    :param heap: memory heap size
    :return: df
    '''
    #convert arff to csv:
    cl = 'java -Xmx' + heap + ' -cp ' + weka_cp + ' weka.core.converters.CSVSaver -i ' + arff_path + ' -o temp.csv'
    subprocess.call(cl, shell=True)
    #get pickle from csv
    df = pd.read_csv('temp.csv')
    subprocess.call('rm temp.csv', shell=True)
    return df

def nominal_values(data):
    '''
    Extracts the values of a nominal variable
    :param data: pandas dataframe containing the variable with its instantiations
    :return: string for arff constructions. e.g., "{male,female}"
    '''
    values = sorted(data.unique().tolist())
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









