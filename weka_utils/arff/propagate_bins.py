from __future__ import division
__author__ = 'Victor'
from os.path import expanduser, join, split
from collections import OrderedDict
import sys
home_dir = expanduser('~')
sys.path.append(join(home_dir, 'PycharmProjects', 'HospitalReadmission'))
from weka_utils.arff import reorder, discretize
import numpy as np
import re

def feature_bins(arff_line):
    '''
    This function takes a raww arff line and returns a dictionary to map values
    output bins: {(lowerBound, upperBound) : 'String representation of bin', ...}
    '''
    raw_bins = re.search(r'\{(.+)\}', arff_line).group(1)
    raw_bins = re.split(r',', raw_bins)
    bins = OrderedDict()
    for raw_bin in raw_bins:
        if 'All' in raw_bin: #feature has only one bin (trivial interval)
            new_bin = (-np.inf, np.inf)
        elif '(-inf' in raw_bin and 'inf)' in raw_bin: #interval is -inf - inf
            new_bin = (-np.inf, np.inf)
            new_bin = raw_bin
        elif '(-inf' in raw_bin and 'inf)' not in raw_bin: #lower bound is -inf
            if '--' in raw_bin: #upper bound is a negative number (because weka)
                upper = re.search(r'-(-\d+\.*\d*)', raw_bin).group(1)
                new_bin = (-np.inf, float(upper))
            else:
                upper = re.search(r'(\d+\.*\d*)', raw_bin).group(1)
                new_bin = (-np.inf, float(upper))
        elif '(-inf' not in raw_bin and 'inf)' in raw_bin: #upper bound is inf
            lower = re.search(r'(\-*\d+\.*\d*)', raw_bin).group(1)
            new_bin = (float(lower), np.inf)
        elif '(-inf' not in raw_bin and 'inf)' not in raw_bin: #finite bin bounds
            if '--' in raw_bin: #upper bound is a negative number
                lower, upper = re.split(r'\-\-', raw_bin) #split string by '--' (will render upper bound positive)
                lower = re.search(r'(\-*\d+\.*\d*)', lower).group(1)
                upper = re.search(r'(\d+\.*\d*)', upper).group(1)
                new_bin = (float(lower), -1 * float(upper))
            else: #upper bound is not negative
                lower = re.search(r'\((\-*\d+\.*\d*)', raw_bin).group(1)
                upper = re.search(r'(\d+\.*\d*)\]', raw_bin).group(1)
                new_bin = (float(lower), float(upper))
        #add new_bin to output dictionary
        bins[new_bin] = raw_bin
    return bins

def map_value(value, mapping):
    '''
    Maps a value according to a mapping dictionary and returns the mapped value
    '''
    for attr_bin in mapping:
        if value > attr_bin[0] and value <= attr_bin[1]:
            return mapping[attr_bin]
    return

def get_arff_map(arff_path):
    '''
    Creates an interval:labels map of each discretized attribute in an ARFF file
    '''
    mapping = {}
    with open(arff_path, 'r') as arff:
        stop = False #stop=False means we haven't found the first @attribute line
        for line in arff:
            test = re.search(r'@attribute', line.strip(), re.IGNORECASE)
            if not test and not stop:
                continue
            elif not test and stop:
                return mapping
            elif test:
                if not stop:
                    stop = True
                if "All" not in line and '(-inf' not in line and 'inf]' not in line:
                    continue #this means the feature was not discretized (categorical)
                attr = re.split(r'\s+', line.strip())[1]
                mapping[attr] = feature_bins(line)
        return mapping

def map_instance(instance, arff_map, all_features):
    '''
    Maps a weka instance (raw row with csv's) to an arff map (see get_arff_map() )
    '''
    mapped = []
    for i in range(len(instance)):
        feature = all_features[i]
        if feature not in arff_map or instance[i] == '?':
            mapped += [instance[i]] # either missing value or attr was not discretized
        else: #feature found in mapping index
            mapped += [map_value(value=float(instance[i]), mapping=arff_map[feature])]
    return mapped

def raw_attr_values(attr, arff):
    '''
    Get the raw string of the values of an attribute. E.g., {Y,N} from an arff dataset
    '''
    with open(arff, 'r') as in_file:
        for line in in_file:
            pattern = re.compile('@attribute\s+' + attr, re.IGNORECASE)
            target = re.search(pattern, line.strip())
            if target:
                return re.search(r'(\{.+\})', line.strip()).group(1)
        return None

def map_arff(source_path, target_path, out_path):
    '''
    Propagates the source's discretization scheme to a target dataset
    '''
    #Check if both arff files have the same features
    arff_map = get_arff_map(source_path) #contains how to map values to interval labels
    source_attrs = reorder.arff_features(source_path)
    target_attrs = reorder.arff_features(target_path) #features in target arff
    if set(source_attrs) != set(target_attrs):
        print "Warning: source and target ARFF files don't have the same set of features\n"
    #start
    arff_map = get_arff_map(source_path) #instructions to map values to interval labels
    with open(target_path, 'r') as target, open(out_path, 'w') as out_arff:
        #First, we are gonna create ARFF header (relation + attr declarations)
        for line in target: #parse target arff (the one to propagate on)
            data_label = re.search(r'@data', line, re.IGNORECASE) #check if data about to start
            if data_label:
                print>>out_arff, line.strip()
                break #ready to start mapping instances
            elif not re.search(r'@attribute', line.strip(), re.IGNORECASE):
                print>>out_arff, line.strip()
                continue #neither data nor attribute declaration, continue.
            else: #line is an attribute declaration, i.e., @attribute etc.
                attribute = re.split(r'\s+', line.strip())[1]
                if attribute not in arff_map: #either not discretized or doesn't exist in source
                    print>>out_arff, line.strip()
                    continue
                description = '{' + ','.join(arff_map[attribute].values()) + '}'
                print>>out_arff, '@attribute ' + attribute + ' ' + description
                continue
        #Now we start mapping instances
        for line in target:
            instance = re.split(r',', line.strip())
            instance_mapped = map_instance(instance=instance, arff_map=arff_map, all_features=target_attrs)
            print>>out_arff, ','.join(instance_mapped)
        print 'Created: ', out_path
        return