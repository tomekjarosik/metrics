import platform
import getpass

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