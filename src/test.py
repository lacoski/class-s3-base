import os
import threading
import sys

import boto3
import botocore
from CephS3Base.lib import (
    cephS3Directory
)

def main():
    ceph_dir = cephS3Directory()
    ceph_dir.rm('UserA')
    ceph_dir.ls()
if __name__ == '__main__':
    main() 