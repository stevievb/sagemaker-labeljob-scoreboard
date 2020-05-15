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

# function to help parse query params from bokeh server url
DEFAULT_PLOT_HEIGHT = 500
DEFAULT_PLOT_WIDTH = 800


def parse_args(args):
    try:
        height = int(args.get('height')[0])
    except:
        height = DEFAULT_PLOT_HEIGHT

    try:
        width = int(args.get('width')[0])
    except:
        width = DEFAULT_PLOT_WIDTH

    try:
        labeling_job_name = args.get('labeling_job_name')[0].decode('utf-8')
    except:
        print('A labeling job query parameter is required e.g, labeling_job_name=a-test-job-name')
        exit(1)

    try:
        bucket = args.get('bucket')[0].decode('utf-8')
    except:
        print('A bucket query parameter is required e.g, bucket=an-s3-bucket-name')
        exit(1)

    try:
        prefix = args.get('prefix')[0].decode('utf-8')
    except:
        print('A prefix parameter is required e.g, prefix=a/prefix/job-name/annotations/worker-response')
        exit(1)

    try:
        user_pool_id = args.get('user_pool_id')[0].decode('utf-8')
    except:
        print('A user_pool_id parameter is required e.g, user_pool_id=us-west-2_adfsdasf')
        exit(1)

    return height, width, labeling_job_name, bucket, prefix, user_pool_id