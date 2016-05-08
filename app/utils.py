import platform
import getpass
import datetime

class PlatformInfo(object):
    def info(self):
        res = {}
        res["machine"] = platform.machine()
        res["version"] = platform.version()
        res["platform"] = platform.platform()
        res["uname"] = platform.uname()
        res["cpu"] = platform.processor()
        res["java_ver"] = platform.java_ver()
        res["user"] = getpass.getuser()
        return res

    def username(self):
        return getpass.getuser()


class CustomSorter(object):
    @staticmethod
    def sort_scores(scores_dict, filter_total_time=True):
        if filter_total_time:
            scores_dict = filter(lambda x: x[0] != "total time", scores_dict.items())
        return list(sorted(scores_dict, key=lambda x: -x[1]))


def format_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

def timediff(t1, t2):
    return str(datetime.datetime.fromtimestamp(t1) - datetime.datetime.fromtimestamp(t2))

def listdiff(first, second):
    second = set(second)
    return [item for item in first if item not in second]