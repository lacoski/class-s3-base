from CephS3Base.lib_base import cephS3API

def create_test_data(obj):
    obj.s3_upload('/home/lacoski/Downloads/highlight.zip',key_path='/User_A/file1.zip')
    obj.s3_upload('/home/lacoski/Downloads/highlight.zip',key_path='/User_A/home/file2.zip')
    obj.s3_upload('/home/lacoski/Downloads/highlight.zip',key_path='/User_A/home/file3.zip')
    obj.s3_upload('/home/lacoski/Downloads/highlight.zip',key_path='/User_A/Download/file4.zip')
    obj.s3_upload('/home/lacoski/Downloads/highlight.zip',key_path='/User_A/Download/file5.zip')
    obj.s3_upload('/home/lacoski/Downloads/highlight.zip',key_path='/User_A/Test/file6.zip')
    
    
def main():
    test = cephS3API()
    test.is_connected()    
    #create_test_data(test)
    
    test.s3_ls()
    

if __name__ == '__main__':
    main() 