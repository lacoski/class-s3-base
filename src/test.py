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
    access_key = '1N8I3SDW0MIDUR0Z5MP8'
    secret_key = 'ecBlpo1SyN72KSo4I7jrj0KvXLEOsTNQzOoWATKS'
    s3_host = 'http://192.168.20.52:7480'

    bucket_name = 's3cloud'    

    # s3client = boto3.client('s3',
    #     aws_secret_access_key = secret_key,
    #     aws_access_key_id = access_key,
    #     endpoint_url = s3_host) 

    # s3client.upload_file(
    #     "/home/lacoski/Downloads/CSDL.zip", bucket_name, "CSDL.zip",
    #     Callback=ProgressPercentage("/home/lacoski/Downloads/CSDL.zip")
    # )
    test = '/home/lacoski/Downloads/CSDL.zip'
    name = test.split('/')
    print(name[-1])

if __name__ == '__main__':
    main() 