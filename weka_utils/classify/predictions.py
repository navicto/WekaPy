__author__ = 'Victor'
import re
import sys

class PredictionsFile(object):
    '''
    Manipulate predictions' files generated with weka classifiers
    '''
    def __init__(self, predictions_path):
        '''
        Initialize predictions file object from path to file
        :param predictions_path: path to predictions file
        :param header_row: row with column labels (0-indexed)
        :return: None
        '''
        with open(predictions_path, 'r') as predictions_file:
            self._lines = predictions_file.readlines()
            self._lines = [line.strip() for line in self._lines if line != ''] #remove blank lines
            #find header row
            i = 0
            for line in self._lines:
                if 'inst#' in line:
                    header_row = i
                    break
                else:
                    i += 1

            self._lines[0:header_row] = []


    def __str__(self, nrows=5):
        col_names = re.split(r',', self._lines[0])
        representation = 'File contains ' + str(len(col_names)) + ' columns:\n'
        representation += ', '.join(col_names) + '\n'
        representation += 'Number of rows: ' + str(len(self._lines) - 1) + '\n'

        if nrows:
            try:
                representation += 'First ' + str(nrows) + ' rows:\n'
                for i in range(nrows):
                    representation += self._lines[i + 1] + '\n'
            except Exception:
                pass
        return representation

    def map_value(self, value_from, value_to):
        '''
        Maps an original value to a new one (affects every instance)
        :param value_from: original value
        :param value_to: desired value
        :return: None
        '''

        for i in range(1, len(self._lines)):
            try:
                if re.search(value_from, self._lines[i]):
                    self._lines[i] = re.sub(value_from, value_to, self._lines[i])
            except:
                print 'could not process line: ' + str(self._lines[i])
                print 'value from: ', value_from
                print 'value_to: ', value_to
                raise Exception('could not process line')

    def rename_column(self, col_from, col_to):
        '''
        Changes the label of a column
        :param col_from: original column name
        :param col_to: new column name
        :return: None
        '''
        if col_from in self._lines[0]:
            line = re.split(r',', self._lines[0])
            line[line.index(col_from)] = col_to
            self._lines[0] = ','.join(line)
        else:
            raise NameError('Column ' + col_from + ' not found in predictions file\n' + self._lines[0])

    def to_file(self, out_path):
        '''
        Writes predictions to a new file
        :param out_path: desired file path
        :return: None
        '''
        with open(out_path, 'w') as out_file:
            print>>out_file, '\n'.join(self._lines)


def main():
    pass

if __name__ == '__main__':
    main()

#Demo:
# in_path = "D:\ResearchData\Readmission_AllCause\FeatureSelection\DRG\Predictions\predictions_nFeatures_1.csv"
# out_path = "D:\ResearchData\Readmission_AllCause\FeatureSelection\DRG\Predictions\predictions_nFeatures_78_new.csv"
#
# predictions = PredictionsFile(predictions_path=in_path, header_row=4)
# predictions.map_value('1:Y', 'T')
# predictions.map_value('2:N', 'F')
# predictions.map_value('\*', '')
# predictions.rename_column('distribution', 'p_T')
# predictions.rename_column('', 'p_F')
# # predictions.to_file(out_path)
# print predictions

