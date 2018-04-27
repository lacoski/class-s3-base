from .settings import (
    ACCESS_KEY,
    SECRET_KEY,
    BUCKET_NAME,
    S3_HOST,
)
from .structures import (
    s3_object,
    ProgressPercentage
)
from .helper import (
    helper_cephS3API,
    helper_cephS3Directory
)
import boto3
from botocore.exceptions import ClientError
import os.path
import botocore

class cephS3API(object):
    access_key = ACCESS_KEY
    secret_key = SECRET_KEY
    s3_host = S3_HOST
    bucket_name = BUCKET_NAME
    current_direct = ''
    client_s3 = None
    resource_s3 = None
    helper_class = helper_cephS3API()

    def __init__(self):        
        s3client = boto3.client('s3',
            aws_secret_access_key = self.secret_key,
            aws_access_key_id = self.access_key,
            endpoint_url = self.s3_host
        )
       
        s3resource = boto3.resource('s3',
            aws_secret_access_key = self.secret_key,
            aws_access_key_id = self.access_key,
            endpoint_url = self.s3_host
        )

        self.client_s3 = s3client
        self.resource_s3 = s3resource

    def s3_ls(self):
        pass
    
    def s3_cd(self):
        pass

    def s3_pwd(self):
        pass

    def s3_ls(self):
        pass



    