import argparse
import time
import os
import requests
import filesystem_helper
import utils
import json
import zlib
import datetime

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

    def prepare_request_data(self, username, timestamp, previous_timestamp, scores, is_success, diff, gitstatus, env):
        result = {
            "username" : username,
            "scores" : scores,
            "timestamp" : timestamp,
            "previous_timestamp" : previous_timestamp,
            "is_success" : is_success,
            "diff" : diff,
            "gitstatus" : gitstatus,
            "env" : env}
        return result

    def send_request(self, username, timestamp, previous_timestamp, scores, is_success, diff, gitstatus, env):
        payload = self.prepare_request_data(username,
                                            timestamp,
                                            previous_timestamp,
                                            scores,
                                            is_success,
                                            diff,
                                            gitstatus,
                                            env)
        json_payload = json.dumps(payload)
        #compressed_json_payload = zlib.compress(json_payload)
        return requests.post(self.ADD_METRIC_URL, json=json_payload )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--root_dir', type=str,
                       help='root dir where all build.times files exists')
    parser.add_argument('--current', type=str,
                       help='path to file with current metrics')
    parser.add_argument('--timestamp', type=int,
                       help='timestamp of current snapshot in seconds since epoch')
    parser.add_argument('--previous_timestamp', type=int,
                       help='previous build timestamp in seconds since epoch')
    args = parser.parse_args()

    print("Sending metrics...")
    filesystemHelper = filesystem_helper.FilesystemHelper()
    platformInfo = utils.PlatformInfo()

    sender = MetricSender()
    last_build_time = args.previous_timestamp/1000L
    diff = filesystemHelper.files_modified_since_with_timestamp(args.root_dir, last_build_time)
    req = sender.send_request(platformInfo.username(),
                              args.timestamp / 1000L,
                              last_build_time,
                        sender.parse_build_times(args.current),
                        True,
                        diff,
                        filesystemHelper.git_status(),
                        platformInfo.info())

    print ("Stats sent with status {0}".format(req.status_code))
