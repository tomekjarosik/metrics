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