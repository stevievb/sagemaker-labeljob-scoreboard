#  © 2020 Amgen Inc. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from collections import Counter
from multiprocessing import Pool
import json

import boto3
import holoviews as hv
import holoviews.plotting.bokeh
from bokeh.plotting import curdoc

from args import parse_args
from s3 import get_matching_s3_keys


# get the bokeh server query string args
args = curdoc().session_context.request.arguments

height, width, labeling_job_name, bucket, prefix, user_pool_id = parse_args(args=args)

s3_client = boto3.client('s3')
cognito_client = boto3.client('cognito-idp')
sg_client = boto3.client('sagemaker')

labeling_job_info = sg_client.describe_labeling_job(
    LabelingJobName=labeling_job_name
)

print('Creating a dashboard for the ' + labeling_job_name + ' labeling job')

labeled_so_far = labeling_job_info['LabelCounters']['HumanLabeled']
unlabeled = labeling_job_info['LabelCounters']['Unlabeled']

workTeamName = labeling_job_info['HumanTaskConfig']['WorkteamArn'].split('/')[-1]

worker_keys = get_matching_s3_keys(bucket=bucket, prefix=prefix)

def get_json_data(key):
    s3_client_obj = s3_client.get_object(Bucket=bucket, Key=key)
    s3_client_data = s3_client_obj['Body'].read().decode('utf-8')

    return json.loads(s3_client_data)

pool = Pool()
json_data = pool.map(get_json_data, worker_keys)

sg_client.describe_workteam(
    WorkteamName=workTeamName
)

response = cognito_client.list_users(
    UserPoolId=user_pool_id)

user_dict = {}
for user in response['Users']:
    for attr in user['Attributes']:
        if attr['Name'] == 'sub':
            user_dict[attr['Value']] = user

labels = []
for data in json_data:
    for a in data['answers']:
        sub = a['workerMetadata']['identityData']['sub']
        labels.append(user_dict[sub]['Username'])

renderer = hv.renderer('bokeh')

bars = hv.Bars(Counter(labels)).opts(width=width, height=height,
                                     title='Labeled/Unlabeled: ' + str(labeled_so_far) + '/' + str(unlabeled))

layout = bars

doc = renderer.server_doc(layout)
doc.title = 'Labeling Job Status'
