from CephS3Base.lib import cephS3API

def main():
    test = cephS3API()
    test.is_connected()
    # test.create_bucket('test1')
    # test.list_bucket()
    
    #test.s3_upload('/home/lacoski/Downloads/highlight.zip',key_path='/user_b/home/file2.zip')
    test.s3_ls()
    #test.s3_cat('/user_a/highlight22.zip')
    #test.s3_upload_with_metadata('/home/lacoski/Downloads/highlight.zip',key_path='/user_a/highlight2.zip')
    #test.s3_ls()
    #test.s3_generate_download_url('GoTiengViet.zip')

if __name__ == '__main__':
    main() 