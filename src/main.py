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
    # test.create_bucket('test1')
    # test.list_bucket()
    
    #create_test_data(test)
    #test.s3_ls()
    #test.s3_rm('Direct/object-1.PNG')
    #test.create_bucket('s3storage')
    test.s3_ls()
    #test.s3_cat('/user_a/highlight22.zip')
    #test.s3_upload_with_metadata('/home/lacoski/Downloads/highlight.zip',key_path='/user_a/highlight2.zip')
    #test.s3_ls()
    #test.s3_generate_download_url('GoTiengViet.zip')

if __name__ == '__main__':
    main() 