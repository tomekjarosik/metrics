# gets the time frame we are going to look back and builds a placeholder list to passover the info from our mtime to slay
import datetime as dt
import os
import subprocess
import datetime

class FilesystemHelper(object):
    def files_modified_since(self, dirpath, ago):
        now=dt.datetime.now()
        result = []
        for root,dirs,files in os.walk(dirpath):
            for fname in files:
                path=os.path.join(root,fname)
                st=os.stat(path)
                mtime=dt.datetime.fromtimestamp(st.st_mtime)
                if mtime>ago:
                    result.append(path)

        return result

    def git_status(self):
        proc = subprocess.Popen(["git", "status"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        return out

    def get_file_creation_time(self, path):
        return datetime.datetime.fromtimestamp(os.path.getctime(path))