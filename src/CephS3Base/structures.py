import os
import threading
import sys

class s3_object(object):
    LastModified = None
    Owner = None
    Size = ''
    Key = ''  
    Level = ''
    def __init__(self, s_Size='', s_LastModified=None, s_Owner=None, s_Key='', i_Level=0):
        self.LastModified = s_LastModified
        self.Size = s_Size
        self.Key = s_Key
        self.Owner = s_Owner
        self.Level = i_Level

    def show_object(self):
        print("{name} - {size} - {dt} - {owner}".format(name=self.Key, size=self.Size, 
                                                        dt=self.LastModified, owner=self.Owner))
    def get_key_level(self):
        print
        try:
            key_level = self.Key.split('/')[self.Level]
        except IndexError:
            key_level = ''
        return key_level

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