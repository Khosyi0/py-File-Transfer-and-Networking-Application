import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        self.files_dir = 'files/'

    def list(self, params=[]):
        try:
            filelist = glob(self.files_dir + '*.*')
            return dict(status='OK', data=[os.path.basename(f) for f in filelist])
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, params=[]):
        try:
            filename = params[0]
            if filename == '':
                return None
            with open(os.path.join(self.files_dir, filename), 'rb') as fp:
                isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def upload(self, params=[]):
        try:
            filename = params[0]
            filecontent = params[1]
            with open(os.path.join(self.files_dir, filename), 'wb') as fp:
                fp.write(base64.b64decode(filecontent))
            return dict(status='OK', data='File uploaded successfully')
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def delete(self, params=[]):
        try:
            filename = params[0]
            os.remove(os.path.join(self.files_dir, filename))
            return dict(status='OK', data='File deleted successfully')
        except Exception as e:
            return dict(status='ERROR', data=str(e))


if __name__ == '__main__':
    f = FileInterface()
