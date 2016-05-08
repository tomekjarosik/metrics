import argparse
import time
import os
import requests
import filesystem_helper
import utils
import json

class MetricSender(object):
    ADD_METRIC_URL = "http://127.0.0.1:5000/buildmetrics/api/v1.0/add"
    def __init__(self):
        pass
    def parse_build_times(self, filepath):
        results = {}
        with open(filepath) as f:
            for line in f:
                arr = line.split(",")
                results[arr[1].strip()] = int(arr[0])
        return results

    def prepare_request_data(self, username, scores, is_success, diff, env):
        result = {
            "username" : username,
            "scores" : scores,
            "is_success" : is_success,
            "diff" : diff,
            "env" : env}
        return result

    def send_request(self, username, scores, is_success, diff, env):
        payload = self.prepare_request_data(username, scores, is_success, diff, env)
        json_payload = json.dumps(payload)
        return requests.post(self.ADD_METRIC_URL, json=json_payload )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--root_dir', type=str,
                       help='root dir where all build.times files exists')
    parser.add_argument('--current', type=str,
                       help='path to file with current metrics')
    parser.add_argument('--previous', type=str,
                       help='path to file with previous metrics')
    args = parser.parse_args()

    print("Sending metrics...")
    filesystemHelper = filesystem_helper.FilesystemHelper()
    platformInfo = utils.PlatformInfo()

    sender = MetricSender()
    # FIXME: last build time
    # last_build_time = filesystemHelper.get_file_creation_time(args.previous)
    # diff = filesystemHelper.files_modified_since(args.root_dir, last_build_time)
    diff = filesystemHelper.git_status()
    req = sender.send_request(platformInfo.username(),
                        sender.parse_build_times(args.current),
                        True,
                        diff,
                        platformInfo.info())

    print ("Stats sent with status {0}".format(req.status_code))
