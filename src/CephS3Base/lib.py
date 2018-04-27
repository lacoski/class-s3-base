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
        #print(response)
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


class cephS3Directory(object):
    list_item = [
        '/UserA/object-1.PNG', 
        '/UserA/object-2.PNG',
        '/UserA/object-3.PNG',
        '/UserA/home/object-4.PNG',
        '/UserA/home/object-5.PNG',
        '/UserA/Download/object-6.PNG',
        '/UserA/Download/object-7.PNG',
        '/UserA/test/object-A.PNG',
        '/UserA/test/check/object-8.PNG',
        '/UserA/test/check/object-9.PNG',                
    ]
    helper = helper_cephS3Directory()
    current_direct = ''        
    def __init__(self):
        pass        

    def get_level_path(self, path_to):
        split_object = path_to.split('/')
        level = len(split_object) - 1
        return level  
    
    def check_path_exist(self, full_path_to):        
        for item in self.list_item:
            if item.startswith(full_path_to):
                return True
        return False

    def get_list_path(self, path_to=''):
        if not path_to:
            path_to = self.current_direct
    
        list_path = []
        level_path = self.get_level_path(path_to)
        for item in self.list_item:
            if not path_to in item:
                continue
            split_object = item.split('/')
            try:
                item_get = split_object[level_path] 
            except IndexError:
                item_get = None

            if not item_get in list_path and item_get:
                list_path.append(item_get)
        return list_path
    
    def valid_path(self, path_to=''):
        if not path_to.startswith("/"):
            path_to = '/' + self.current_direct + path_to
        if not path_to.endswith("/"):
            path_to = path_to + '/'
        return path_to

    def cd(self, path_to=''):
        print('cd: ---')
        if not path_to:
            self.current_direct = ''
        else:
            if not path_to.startswith("/"):
                path_to = self.valid_path(path_to)
            if self.check_path_exist(path_to):                
                self.current_direct = self.valid_path(path_to)
            else:
                print('Path not found')
            

    def ls(self, path=''):
        print('ls : ---')
        for item in self.get_list_path(path):
            print(item)

    def rm(self, path_to):
        if not path_to.startswith("/"):
            path_to = self.current_direct + path_to
        if self.check_path_exist(path_to):
            rm_list = []
            for item in self.list_item:
                if item.startswith(path_to):
                    rm_list.append(item)
                    #self.list_item.remove(item)
            self.list_item = self.helper.remove_sub_list(self.list_item, rm_list)
        print('rm done!')
        
    def pwd(self):
        print('pwd : ---')
        if self.current_direct:
            print('/')
        print(self.current_direct)            

    def mv(self):
        pass 

    def show_list_object(self):
        if not self.list_item:
            print("List None")
            return
        for item in self.list_item:
            print(item)
    