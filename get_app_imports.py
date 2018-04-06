#!/usr/bin/python

# This script is called by buildenv.sh
# on the app file, grabs all of its
# imports, adds them to a pip install com-
# mand, and passes the command back to
# buildenv.sh to be executed.

import os
import argparse

# extract_import_statements(lines)
#
# The purpose of this function is to extract the import statements from
# a list of plain text file lines, correct naming conventions to avoid
# pip errors, and exclude packages already in the standard library.
def extract_import_statements(lines):
	
	# Add lines to new list if they begin with the 
        # keywords 'from' or 'import', parse out the package
        # names from the split lines, and remove all packages
        # already contained in the standard library.

        standard_lib = ['csv', 'os', 'time', 'io', 'argparse',
                        'ssl', 'json', 'base64', 'http', 'sys',
                        'distutils', 'datetime', 'warnings']
        packages = [line.split(' ')[0:2][1].strip('\n_').replace('_','-').split('.')[0] for line in lines
                    if ('import' == line.split(' ')[0] or 'from' == line.split(' ')[0]) and
                        line.split(' ')[0:2][1].rstrip('\n') not in standard_lib]
        return packages

# read_function_file_contents(f)
#
# The purpose of this function is to determine whether the path of the
# passed file argument is relative or absolute, read the file, and return
# the contents as a list of plain text lines.

def read_function_file_contents(f):
	# Determine whether the argument passed
        # contains the absolute file path. Then,
        # open the file argument, which contains
        # the project's function and read the
        # lines into a list.

        if f[0] == '/':    # File argument _does_ contain the absolute path ...
                lines = open(f).readlines()

        else:                   # File argument _does not_ contain the absolute path ...
                test_file = f
                path_to_file = os.path.dirname(os.path.abspath(test_file))
                lines = open('{0}/{1}'.format(path_to_file,
					      test_file)).readlines()

        return lines

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('f', type=str)
	args = parser.parse_args()
	
	packages = extract_import_statements(read_function_file_contents(args.f))
	
	# Take remaining packages and create a pip
	# command installing all of them. Return the
	# command string to buildenv.sh 

	install_command = 'pip install {}'.format(' '.join(packages))
	print(install_command)
	return install_command

if __name__ == "__main__":
	main()
