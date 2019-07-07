"""
This is a script to easily execute circle CI jobs from other repository builds. 
Useful if you have a dependent build that you need to run to ensure the latest code is up to date with the parent build.

This script will:

  - Fire a build in another circle CI repository
  - Loop and call the build_url to continuously get the status
  - Wait until the job finishes
  - If the job fails this script will exit 1 which will fail the job. 
  - Else it will exit 0 which will pass the job.
  
**You will need to download this script and put it in the base of your repository**

Usage:
    - python trigger_build.py --repo user/repo --branch branch_name --token CIRCLE_TOKEN --build ENV_VARIABLE=value --build ENV_VARIABLE2=value2
    
Example:
    - python trigger_build.py --repo masoniteframework/validation --branch circle-ci --token $CIRCLE_TOKEN --build MASONITE_BRANCH=$CIRCLE_BRANCH

NOTE: You can get your CircleCI access token via your dashboard. If no token is specified it will use the CIRCLE_TOKEN in your job dashboard.
So if you don't want to pass in the token then put it in the environment variable in your job's dashboard.

Example config:
version: 2
jobs:
    Masonite Validation:
      docker:
        - image: circleci/python:3.6
      steps:
        - checkout
        - run: python trigger_build.py --repo masoniteframework/validation --branch circle-ci --build MASONITE_DEPENDENT_BRANCH=$CIRCLE_BRANCH
"""

import requests
import time
import os
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-r", "--repo", help="Repository name")
parser.add_argument("-b", "--branch", help="Branch name")
parser.add_argument("-t", "--token", help="Circle CI Token")
parser.add_argument('-a', '--build', action='append', help='Set Build Arguments')
parser.add_argument('-p', '--poll', help='How long the script should sleep before checking status')
args = parser.parse_args()

repo = args.repo
branch = args.branch or 'master'
token = args.token or os.getenv('CIRCLE_TOKEN')
poll = args.poll or 5

parameters = {}
for argument in args.build or []:
    if not '=' in argument:
        print("ERROR: '--build' argument must contain a '=' sign. Got '{}'".format(argument))
        exit(1)
    key = argument.split('=')[0]
    value = argument.split('=')[1]

    if key == 'BUILD_BRANCH' and value == 'dynamic' and os.getenv('CIRCLE_PULL_REQUEST'):
        value = requests.get('https://api.github.com/repos/{}/pulls/{}'.format(repo, os.getenv('CIRCLE_BRANCH').replace('pull/', ''))).json()['head']['ref']
    
    parameters.update({key: value})

build_parameters = {'build_parameters': parameters}

r = requests.post('https://circleci.com/api/v1/project/{}/tree/{}?circle-token={}'.format(repo, branch, token), json=build_parameters)

if 'build_num' not in r.json():
    print('ERROR: Could not find repository {} or with the branch {}'.format(repo, branch))
    print(r.json())
    exit(1)

print('Building: ', r.json()['build_num'])

status = requests.get('https://circleci.com/api/v1.1/project/github/{}/{}?circle-token={}'.format(repo, r.json()['build_num'], token))
print('Build Status: ', status.json()['lifecycle'])
while status.json()['lifecycle'] != 'finished':
    time.sleep(poll)
    print('Build Status: ', status.json()['lifecycle'])
    status = requests.get('https://circleci.com/api/v1.1/project/github/{}/{}?circle-token={}'.format(repo, r.json()['build_num'], token))

print('Finished. Failed? ', status.json()['failed'])
if status.json()['failed']:
    exit(1)
