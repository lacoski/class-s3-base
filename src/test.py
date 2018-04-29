import os
import threading
import sys

import boto3
import botocore
from CephS3Base.lib import (
    cephS3API
)

def init_test_delete(s3client):
    s3client.s3_upload('/home/lacoski/Downloads/highlight.zip','/User_D/file3.zip')  
    s3client.s3_upload('/home/lacoski/Downloads/highlight.zip','/User_D/file4.zip')
    s3client.s3_upload('/home/lacoski/Downloads/highlight.zip','/User_D/home/file5.zip')
    s3client.s3_upload('/home/lacoski/Downloads/highlight.zip','/User_D/home/file6.zip')

def main():
    ceph_dir = cephS3API()
    ceph_dir.is_connected() 
    #ceph_dir.s3_ls('/User_A') 
    # ceph_dir.s3_cd('User_A')
    # ceph_dir.s3_pwd()
    ceph_dir.s3_ls()    
    #ceph_dir.s3_cd('/User_C')
    # ceph_dir.s3_pwd()
    # ceph_dir.s3_ls()    
    #ceph_dir.s3_get_objects()
    #ceph_dir.s3_upload('/home/lacoski/Downloads/highlight.zip','/User_A/home/file3.zip')
    #ceph_dir.s3_remove_object('/file1.zip/')
    #ceph_dir.s3_ls('User_A')
    #ceph_dir.s3_rm_directory('User_C')
    #ceph_dir.get_object('/User_B/')
    ceph_dir.s3_upload('/home/lacoski/Downloads/highlight.zip','/User_C/file6.zip')
    ceph_dir.s3_generate_download_url('/User_C/file6.zip')
    #ceph_dir.s3_rm_directory('/User_D/')
    #ceph_dir.s3_ls() 
    #ceph_dir.get_size_object('/User_A/home/file3.zip')
    #ceph_dir.s3_rm_object('/User_A/home/file3.zip')
    #ceph_dir.s3_remove_object('/file1.zip')
    #ceph_dir.is_file('/file1.zip')

if __name__ == '__main__':
    main() 