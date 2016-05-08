import argparse
import time
import os

class MetricSender(object):
    def __init__(self):
        pass

    def parse_build_times(self, filepath):
        results = {}
        with open(filepath) as f:
            for line in f:
                arr = line.split(",")
                results[arr[1].strip()] = int(arr[0])
        return results

    def get_file_creation_time(self, path):
        with open(path) as f:
            return time.ctime(os.path.getctime(f))

    def prepare_request(self, username, scores, is_success, diff, env):
        result = {
            "username" : username,
            "scores" : scores,
            "is_success" : is_success}
        return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--root-dir', type=str,
                       help='root dir where all build.times files exists')
    parser.add_argument('--current', type=str,
                       help='path to file with current metrics')
    parser.add_argument('--previous', type=str,
                       help='path to file with previous metrics')
    args = parser.parse_args()

    print("Hello from python")
    print args