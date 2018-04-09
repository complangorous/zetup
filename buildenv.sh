#!/bin/bash

# The purpose of this script is to 
# automate the initial steps in 
# setting up a zappa-based Lambda
# app. 
#
# $1 path_to_file	$2 file_name	$3 get_app_imports.py (path to)
#
# $4 staging_preference

cd $1
printf "\n Creating virtual environment: $1/venv ...\n\n"
virtualenv venv
source venv/bin/activate

printf "\n Changing Python version in $1/venv ...\n\n"
virtualenv -p python3.6 venv
2to3 -w $2
python --version

printf "\n Installing script dependencies ...\n\n"
packages=$(python $3/get_app_imports.py $2)
printf packages
${packages}

echo Installing awscli and zappa ...
pip install awscli zappa

printf "\n Configuring aws certs ...\n\n"
aws configure set default.ca_bundle /etc/ssl/certs/ca-certificates.crt

printf "\n Initiating Zappa ... \n\n"
filename=$2
echo > zappa_settings.json

printf "\n Done.\n\n"
deactivate
