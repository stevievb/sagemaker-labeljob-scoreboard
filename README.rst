This is a bokeh app that shows how many items have been labeled by each user during a sagemaker labeling job (SageMaker Ground Truth).

It requires docker be installed wherever the app is being run

First build docker image. From within the repo directory:

    docker build . -t sagemaker_label_dashboard

AWS credentials must provide sagemaker full access and cognito read access policies attached

    arn:aws:iam::aws:policy/AmazonCognitoReadOnly

    arn:aws:iam::aws:policy/AmazonSageMakerFullAccess

Then to run

    docker run -p 5007:5006 -e AWS_ACCESS_KEY_ID=adfsasd -e AWS_SECRET_ACCESS_KEY=adfsda -e AWS_DEFAULT_REGION='us-west-2' sagemaker_label_dashboard

Then go to a browser

    http://localhost:5007/job_progress_barchart?labeling_job_name=a-test-job-name&bucket=an-s3-bucket-name&prefix=a/prefix/job-name/annotations/worker-response&user_pool_id=us-west-2_adfsdasf&width=800&height=500

Required Query params -
    labeling_job_name - the name of the sagemaker labeling job

        example - labeling_job_name=a-test-job-name

    bucket - the bucket where the labeling job info is stored

        example - bucket=an-s3-bucket-name

    prefix - a prefix of where the job annotations are stored

        example - prefix=a/prefix/job-name/annotations/worker-response

    user_pool_id - the cognito user pool id of the workforce

        example - user_pool_id=us-west-2_adfsdasf

Optional Query params -

    height - the height of the plot

        example - height=500

    width - the width of the plot

        example - width=500
