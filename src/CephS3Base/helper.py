class helper_cephS3API(object):
    def split_path_to_name(self, path_to_file = ''):                
        name = path_to_file.split('/')
        #print(name)
        return name[-1]