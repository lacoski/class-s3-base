import os
import threading
import sys

import boto3
import botocore
from CephS3Base.lib_base import (
    cephS3Directory
)

def main():
    ceph_dir = Directory()
    ceph_dir.cd()
    ceph_dir.ls()
    ceph_dir.cd('UserA')
    ceph_dir.pwd()
    ceph_dir.mkdir('Demo')
    ceph_dir.mkdir('Demo1')
    ceph_dir.mkdir('Demo2')
    ceph_dir.mkdir('Demo')
    ceph_dir.ls()
if __name__ == '__main__':
    main() 