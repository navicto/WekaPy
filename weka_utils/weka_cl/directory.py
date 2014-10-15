__author__ = 'Victor'
from os import chdir, getcwd, makedirs
from os.path import exists

class ChangeDir(object):
    '''
    Context manager for switching to a different directory, and then return to the current directory (the current before
    using the context manager).
    E.g., change to folder F
    with ChangeDir(F)
        do ...
    #When leaving the 'with', current directory will switch back to what it used to be
    '''
    def __init__(self, new_dir):
        self._new_dir = new_dir
        self._old_dir = getcwd()

    def __enter__(self):
        chdir(self._new_dir)
        print 'changing from:' + self._old_dir + ', to:' + getcwd()

    def __exit__(self, exc_type, exc_val, exc_tb):
        chdir(self._old_dir)
        print 'returning to\n' + getcwd()

def mk_nonExist_dirs(*dirs, **kwargs):
    '''
    Checks if a directory(s) exist(s). If not, it will create it(them)
    :param verbose: whether to print a confirmation of directory creation
    :param dirs: directories to check/create
    :return: None
    '''
    for folder in dirs:
        if not exists(folder):
            makedirs(folder)
            if 'verbose' in kwargs:
                if kwargs['verbose']:
                    print 'Created directory: ' + folder

mk_nonExist_dirs('/Users/Victor/Desktop/Test', verbose=True)
mk_nonExist_dirs('/Users/Victor/Desktop/FeatureSelection', verbose=True)
