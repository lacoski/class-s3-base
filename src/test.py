import os
import threading
import sys

import boto3
import botocore

class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

def main():
    access_key = 'JJDEGLZSRPEM355GJC0O'
    secret_key = 'DkECQdTNxOeORL5RpFSX9gdxwaeFSptUKoQ75DvU'
    s3_host = 'http://192.168.2.134:7480'

    bucket_name = 's3cloud'   
    # s3client = boto3.client('cognito-identity',
    #     aws_secret_access_key = access_key,
    #     aws_access_key_id = secret_key,
    #     endpoint_url = s3_host,
    # )      
      
    s3 = boto3.resource('s3',
            aws_secret_access_key = secret_key,
            aws_access_key_id = access_key,
            endpoint_url = s3_host,
        )
    bucket_target = s3.Bucket('s3cloud')
    print(bucket_target)
    for obj in bucket_target.objects.filter(Prefix='/user_a/'):
        print('{0}:{1}'.format(bucket_target.name, obj.key))


if __name__ == '__main__':
    main() 