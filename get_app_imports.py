#!/usr/bin/python

# This script is called by buildenv.sh
# on the app file, grabs all of its
# imports, adds them to a pip install com-
# mand, and passes the command back to
# buildenv.sh to be executed.

import os
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('f', type=str)
	args = parser.parse_args()
	
	# Determine whether the argument passed
	# contains the absolute file path. Then,
	# open the file argument, which contains
	# the project's function and read the
	# lines into a list.

	if args.f[0] == '/':	# File argument _does_ contain the absolute path ...
		lines = open(args.f).readlines()

	else:			# File argument _does not_ contain the absolute path ...
		test_file = args.f
		path_to_file = os.path.dirname(os.path.abspath(test_file))
		lines = open('{0}/{1}'.format(path_to_file,
					      test_file)).readlines()
		print(path_to_file, test_file)

	# Add lines to new list if they begin with the 
	# keywords 'from' or 'import', parse out the package
	# names from the split lines, and remove all packages
	# already contained in the standard library.

	standard_lib = ['csv', 'os', 'time', 'io', 'argparse',
		        'ssl', 'json', 'base64', 'http', 'sys',
			'distutils']
	packages = [line.split(' ')[0:2][1].rstrip('\n') for line in lines  if ('import' == line.split(' ')[0] or 'from' == line.split(' ')[0]) and line.split(' ')[0:2][1].rstrip('\n') not in standard_lib]

	# Take remaining packages and create a pip
	# command installing all of them. Return the
	# command string to buildenv.sh 

	install_command = 'pip install {}'.format(' '.join(packages))
	print(install_command)
	return install_command

if __name__ == "__main__":
	main()
