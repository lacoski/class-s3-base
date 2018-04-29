from .settings import (
    ACCESS_KEY,
    SECRET_KEY,
    BUCKET_NAME,
    S3_HOST,
    USER_NAME
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
    user_name = USER_NAME
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

#region public methods
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
        
    def get_list_object(self, path_to=''):
        """
        Tra lai danh sach item in path
            Ex: list ket [a_s3obj, b_s3obj, c_s3obj]
        return List_object
        """
        if not path_to:
            path_to = self.current_direct
        else:
            path_to = self.valid_path(path_to)
        response = self.client_s3.list_objects(Bucket=self.bucket_name, Prefix=path_to)
        if not 'Contents' in response:        
            #print('Null obj')
            return []
        list_s3_object = []
        level_path = self.get_level_path(path_to)
        for item in response['Contents']:
            temp_obj = s3_object(s_Size= item['Size'],s_Key= item['Key'],
                                s_LastModified= item['LastModified'],s_Owner= item['Owner'], i_Level=level_path)
            list_s3_object.append(temp_obj)            
        return list_s3_object   

    def is_file(self, path_to_file):
        try:
            obj_size = self.get_size_object(path_to_file)
            data = self.client_s3.get_object(Bucket=self.bucket_name,Key=path_to_file)
            #print(data)
            if obj_size != 0:
                return True
            else:
                return False
        except ClientError as e:
            print("Fall: {ex}".format(ex=e))
            return False
    
    def is_directory(self, path_to_directory):        
        obj_size = self.get_size_object(path_to_directory)
        if (
                len(self.get_list_object(path_to_directory)) > 1 or                 
                obj_size == 0
            ):
            return True
        else:
            return False

    # def get_object(self):
    #     """
    #     Get 1 object day du
    #     """
    #     # obj = s3_object(s_Size= data['Size'],s_Key= data['Key'],
    #     #                     s_LastModified= data['LastModified'],s_Owner= data['Owner'])
    #     pass

    def get_size_object(self, full_path_to):
        """
        Get size value object
        """
        try:
            data = self.client_s3.get_object(Bucket=self.bucket_name,Key=full_path_to)  
            #print(data['ContentLength']) 
            return data['ContentLength']
        except ClientError as e:
            print("Fall: {ex}".format(ex=e))
            return -1

    def check_path_exist(self, full_path_to):   
        """
        Kiem tra path co ton tai:
            Ex: /UserA/home, ..
        Return True/False
        
        """     
        for item in self.get_list_object(full_path_to):            
            if item.Key.startswith(full_path_to):
                return True
        return False  

    def s3_ls(self, path=''):        
        print("{username}@{bucket}: ~{current_dir}$ ls {path_input}".format(
            username = self.user_name, 
            bucket=self.bucket_name, 
            current_dir=self.current_direct,
            path_input = path
        ))
        list_path = []
        for item in self.get_list_object(path):
            if not item.get_key_level() in list_path:
                list_path.append(item.get_key_level())
        for item in list_path:
            print(item)
    
    def s3_cd(self, path_to=''):
        print("{username}@{bucket}: ~{current_dir}$ cd {path_input}".format(
            username = self.user_name, 
            bucket=self.bucket_name, 
            current_dir=self.current_direct,
            path_input = path_to
        ))
        if not path_to:
            self.current_direct = '/'
        else:
            full_path = self.valid_path(path_to)
            if self.check_path_exist(full_path):                
                self.current_direct = full_path
            else:
                print('Path not found')    

    def s3_pwd(self):       
        print("{username}@{bucket}: ~{current_dir}$ pwd".format(
            username = self.user_name, 
            bucket=self.bucket_name, current_dir=self.current_direct
        ))
        print(self.current_direct)
    
    def s3_mkdir(self, path_name=''):
        print("{username}@{bucket}: ~{current_dir}$ mkdir {path_input}".format(
            username = self.user_name, 
            bucket=self.bucket_name, 
            current_dir=self.current_direct,
            path_input = path_name
        ))
        if not path_name:
            print("Path name cannot null")
            return
        new_obj = self.valid_path(path_name)
        if not self.check_path_exist(new_obj):
            if self.create_new_directory(new_obj):
                print('Created directory!')
            else:
                print('Created fail')
        else:
            print('Directory exist!')

    def s3_upload(self, path_to_file, key_path = ''): 
        print("{username}@{bucket}: ~{current_dir}$ upload local:{path_input} {path_key}".format(
            username = self.user_name, 
            bucket=self.bucket_name, 
            current_dir=self.current_direct,
            path_input = path_to_file,
            path_key = key_path
        ))      
        if not os.path.isfile(path_to_file):
            print("File upload not found File")
        else: 
            new_obj = self.valid_path_key_file(key_path)
            if not self.check_path_exist(new_obj):                            
                self.client_s3.upload_file(
                    path_to_file, self.bucket_name, new_obj,                    
                    Callback=ProgressPercentage(path_to_file)
                )    
            print('\n')

    def s3_rm_object(self, path_to_obj):
        print("{username}@{bucket}: ~{current_dir}$ rmobj {path_input}".format(
            username = self.user_name, 
            bucket=self.bucket_name, 
            current_dir=self.current_direct,
            path_input = path_to_direct,            
        ))
        key_full = self.valid_path_key_file(path_to_obj)
        #print(key_full)
        if self.s3_remove_object(key_full):
            print('Delete Done')
        else:
            print('Delete Fall')

    def s3_rm_directory(self, path_to_direct):
        print("{username}@{bucket}: ~{current_dir}$ rmdir {path_input}".format(
            username = self.user_name, 
            bucket=self.bucket_name, 
            current_dir=self.current_direct,
            path_input = path_to_direct,            
        ))
        directory_full_path = self.valid_path(path_to_direct)
        if self.is_directory(directory_full_path):
            #print('directory')
            list_path = []
            for item in self.get_list_object(directory_full_path):                
                list_path.append(item.Key)
                print(item.Key)            
            for item in list_path:
                self.s3_remove_object_non_check(item)                
        else:
            print('Is not directory')

    def s3_get_objects(self):
        """
        Get all objects in s3 storage
        """     
        response = self.client_s3.list_objects(
            Bucket=self.bucket_name,
        )                
        if not 'Contents' in response:        
            print('Null list')
            return               
        for item in response['Contents']:
            print(item)

    def s3_generate_download_url(self, file_path):
        print("{username}@{bucket}: ~{current_dir}$ generate-url {path_input}".format(
            username = self.user_name, 
            bucket=self.bucket_name, 
            current_dir=self.current_direct,
            path_input = file_path,            
        ))
        target_obj = self.valid_path_key_file(file_path)
        if self.is_file(target_obj):
            #print('Is file')
            url = self.client_s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': target_obj
                }
            )
            print("URL generate: {uri}".format(uri=url))
        else:
            print('Is not file')        
        #print(url)
        #return url

#endregion

#region private methods
    def create_new_directory(self, path_to_dir):
        if path_to_dir:
            response = self.client_s3.put_object(
                Bucket=self.bucket_name,
                Body='',
                Key=path_to_dir
            )
            return True    
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

    
    def valid_path(self, path_to=''):
        """
        Kiem tra, tao duong danh day du
            EX: /UserA/home/docs/
        """
        if not path_to.startswith("/"):
            path_to = self.current_direct + path_to
        if not path_to.endswith("/"):
            path_to = path_to + '/'
        return path_to   
    
    def valid_path_key_file(self, path_to=''):
        """
        Kiem tra, tao duong danh day du
            EX: /UserA/home/docs/
        """
        if not path_to.startswith("/"):
            path_to = self.current_direct + path_to        
        return path_to   

    def valid_path_directory(self, path_to=''):
        #self.get_list_object(path)
        pass

    def s3_remove_object(self, key_obj=''):
        if self.is_file(key_obj) and key_obj:            
            self.client_s3.delete_object(
                Bucket=self.bucket_name,
                Key=key_obj,
            )
            return True    
        return False

    def s3_remove_object_non_check(self, key_obj=''):
        if key_obj:            
            self.client_s3.delete_object(
                Bucket=self.bucket_name,
                Key=key_obj,
            )
            return True    
        return False   

#endregion