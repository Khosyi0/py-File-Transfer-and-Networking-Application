import json
import logging
import shlex
from file_interface import FileInterface

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        try:
            if string_datamasuk.lower().startswith('upload'):
                parts = string_datamasuk.split(' ', 2)
                c_request = parts[0].strip().lower()
                filename = parts[1]
                filecontent = parts[2]
                logging.warning(f"uploading file: {filename} with content {filecontent}")
                params = [filename, filecontent]
            else:
                c = shlex.split(string_datamasuk)
                c_request = c[0].strip().lower()
                logging.warning(f"memproses request: {c_request}")
                params = c[1:]
            cl = getattr(self.file, c_request)(params)
            return json.dumps(cl)
        except Exception as e:
            logging.error(f"Error processing request: {str(e)}")
            return json.dumps(dict(status='ERROR', data='request tidak dikenali'))

if __name__ == '__main__':
    fp = FileProtocol()
