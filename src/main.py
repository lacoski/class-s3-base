from CephS3Base.lib import cephS3API

def main():
    test = cephS3API()
    
    #test.s3_upload('/home/lacoski/Downloads/GoTiengViet.zip')
    test.s3_ls()
    test.s3_generate_download_url('GoTiengViet.zip')

if __name__ == '__main__':
    main() 