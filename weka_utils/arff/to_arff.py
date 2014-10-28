__author__ = 'Victor'
def dataframe(data, attr_spec, out_path):
    '''
    Creates an arff file from a pandas DataFrame
    :param data: pandas DataFrame containing data
    :param attr_spec: specification (dictionary) of data type for arff file. E.g., for numeric attr = 'NUMERIC', for a categorical
        attr such as weather = '{Sunny, foggy, rainy}', for dates = 'DATE "yyyy-MM-dd HH:mm:ss"'
    :param out_path: path where arff file will be saved
    :return:
    '''
    #replace missing values in data
    data.fillna('?')
    #open file and declare relation (file info)
    with open(out_path, 'w') as out_arff:
        print>>out_arff, '@relation ' + out_path + '\n'

        #declare attributes in arff file
        for attr in data.columns.tolist():
            print>>out_arff, '@attribute ' + attr + ' ' + attr_spec[attr]

        #write data to arff file
        data_copy = data.copy()
        data_copy.fillna('?') #replace missing values and NaN with '?'

        print>>out_arff, '@data'
        for row in data.iterrows():
            print>>out_arff, ','.join([str(item) for item in row[1].tolist()])

    print 'created file: ', out_path










