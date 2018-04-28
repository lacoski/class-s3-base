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
    current_direct = '/'
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
    
    def get_level_path(self, path_to):
        """
        Tra lai bac: 
            EX: /UserA/home/test.txt => bac 3 => level = 3-1 = 2
            EX: / => bac 2 => level = 2-1; VD: /, ls => User A
        Return int
        """
        split_object = path_to.split('/')
        level = len(split_object) - 1
        return level 

    def get_list_object(self, path_to=''):
        """
        Tra lai danh sach item in path
            Ex: list ket [a,b,c]
        return List_object
        """
        if not path_to:
            path_to = self.current_direct
        response = self.client_s3.list_objects(Bucket=self.bucket_name, Prefix=path_to)
        if not 'Contents' in response:        
            print('Null obj')
            return []
        list_s3_object = []
        level_path = self.get_level_path(path_to)
        for item in response['Contents']:
            temp_obj = s3_object(s_Size= item['Size'],s_Key= item['Key'],
                                s_LastModified= item['LastModified'],s_Owner= item['Owner'], i_Level=level_path)
            list_s3_object.append(temp_obj)
        
        # level_path = self.get_level_path(path_to)
        # for item in self.list_item:
        #     if not path_to in item:
        #         continue
        #     split_object = item.split('/')
        #     try:
        #         item_get = split_object[level_path] 
        #     except IndexError:
        #         item_get = None

        #     if not item_get in list_path and item_get:
        #         list_path.append(item_get)
        return list_s3_object
    
    def s3_ls(self, path=''):        
        print('ls : ---')
        list_path = []
        for item in self.get_list_object(path):
            if not item.get_key_level() in list_path:
                list_path.append(item.get_key_level())
        for item in list_path:
            print(item)
    
    def s3_cd(self):
        pass

    def s3_pwd(self):
        pass
    



    