import datetime as dt
import os
import subprocess
import datetime


class FilesystemHelper(object):
    def files_modified_since(self, dirpath, ago_dt):
        result = []
        for root, dirs, files in os.walk(dirpath):
            for fname in files:
                path = os.path.join(root, fname)
                st = os.stat(path)
                mtime = dt.datetime.fromtimestamp(st.st_mtime)
                if mtime > ago_dt:
                    result.append(path)

        return result

    def files_modified_since_with_timestamp(self, dirpath, ago_seconds_epoch):
        return self.files_modified_since(dirpath, datetime.datetime.fromtimestamp(ago_seconds_epoch))

    def git_status(self):
        proc = subprocess.Popen(["git", "status"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        return out

    def get_file_creation_time(self, path):
        return datetime.datetime.fromtimestamp(os.path.getctime(path))