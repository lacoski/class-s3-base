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
    helper_cephS3API
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

    def create_bucket(self, name):
        try:
            self.client_s3.create_bucket(Bucket=name)
        except ClientError as e:            
            print("Fall: {ex}".format(ex=e))
            return False
    
    def list_bucket(self):
        try:
            response = self.client_s3.list_buckets()
            buckets = [bucket['Name'] for bucket in response['Buckets']]
            # Print out the bucket list
            print("Bucket List: %s" % buckets)
        except ClientError as e:            
            print("Fall: {ex}".format(ex=e))
            return False

    def get_s3_config(self):
        """
            get seup config s3 bucket
        """
        print(self.access_key)
        print(self.secret_key)
        print(self.bucket_name)
        print(self.s3_host)

    def get_name_id_identify(self):
        pass

    def is_connected(self):
        """
        Tra lai trang thai ket noi
        return: (true/false)
        """
        try:            
            response = self.client_s3.list_buckets()
            print("Connect to S3 storage success!")
            return True
        except ClientError as e:            
            print("Fall: {ex}".format(ex=e))
            return False                  

    def s3_ls(self):
        """
        ls bucket
        return: list obj
        """
        #bucket_target = s3.Bucket('s3cloud')
        list_s3_object = []
        response = self.client_s3.list_objects(
            Bucket=self.bucket_name,
        )
        for item in response['Contents']:
            print(item)
            temp_obj = s3_object(item['Size'], item['Key'], item['LastModified'], item['Owner'])
            list_s3_object.append(temp_obj)

        # for item in list_s3_object:
        #     item.show_object()

    def s3_cd(self):
        pass

    def s3_mkdir(self):
        pass

    def s3_pwd(self):
        pass

    def s3_rm(self):
        pass

    def s3_cat(self, key_path):        
        response = self.client_s3.get_object(Bucket=self.bucket_name,Key=key_path)
        print(response)

    def s3_upload(self, path_to_file, metadata_extend = None, key_path = ''):       
        if not os.path.isfile(path_to_file):
            print("Not found File")
        else: 
            file_name = ''
            if not key_path:
                file_name = self.helper_class.split_path_to_name(path_to_file)
            else: 
                file_name = key_path
            #print(file_name)
            if metadata_extend:
                self.client_s3.upload_file(
                    path_to_file, self.bucket_name, file_name,
                    ExtraArgs={"Metadata": metadata_extend},
                    Callback=ProgressPercentage(path_to_file)
                )
            else:
                self.client_s3.upload_file(
                    path_to_file, self.bucket_name, file_name,                    
                    Callback=ProgressPercentage(path_to_file)
                )

    def s3_upload_with_metadata(self, path_to_file, metadata_extend = None, key_path = ''):       
        if not os.path.isfile(path_to_file):
            print("Not found File")
        else:                       
            file_name = key_path
            #print(file_name)
            self.client_s3.upload_file(
                path_to_file, self.bucket_name, file_name,
                ExtraArgs={"Metadata": {"mykey": "myvalue"}},
                Callback=ProgressPercentage(path_to_file)
            )            



    def s3_generate_download_url(self, name_file):
        url = self.client_s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': name_file
            }
        )
        print(url)
        return url