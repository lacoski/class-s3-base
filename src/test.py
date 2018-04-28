import os
import threading
import sys

import boto3
import botocore
from CephS3Base.lib import (
    cephS3API
)

def main():
    ceph_dir = cephS3API()
    ceph_dir.is_connected() 
    ceph_dir.s3_ls('/User_A')   
if __name__ == '__main__':
    main() 