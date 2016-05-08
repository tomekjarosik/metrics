import os
import app
import unittest
import filesystem_helper

class AppTests(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_send_request(self):
        return self.app.post('/login', data=dict(
            username="aaa",
            password="bbb"
        ), follow_redirects=True)

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

class FilesystemHelperTests(unittest.TestCase):

    def setUp(self):
        self.helper = filesystem_helper.FilesystemHelper()
        pass

    def tearDown(self):
        pass

    def test_files_modified_since(self):
        import datetime as dt, time
        names = ["_t1.txt", "_t2.txt"]
        root = "."
        f1 = open(names[0], "w")
        result = self.helper.files_modified_since(root, dt.datetime.now() - dt.timedelta(seconds=1))
        self.assertEquals(os.path.join(root, names[0]), result[0])
        self.assertEquals(1, result.__len__())
        time.sleep(0.5)
        f2 = open(names[1], "w")
        result = self.helper.files_modified_since(root, dt.datetime.now() - dt.timedelta(seconds=1))
        self.assertEquals(os.path.join(root, names[1]), result[1])
        self.assertEquals(2, result.__len__())

        time.sleep(0.7)
        result = self.helper.files_modified_since(root, dt.datetime.now() - dt.timedelta(seconds=1))
        self.assertEquals(os.path.join(root, names[1]), result[0])
        self.assertEquals(1, result.__len__())

        f1.close()
        f2.close()
        for name in names:
            os.remove(os.path.join(root, name))

    def test_git_status(self):
        res = self.helper.git_status()
        self.assertTrue(res.startswith("# On branch master"))

class PlatformInfoTest(unittest.TestCase):

    def setUp(self):
        from utils import PlatformInfo
        self.info = PlatformInfo().info()

    def test_platform_info(self):
        self.assertIsNotNone(self.info["machine"])
        self.assertIsNotNone(self.info["user"])

if __name__ == '__main__':
    unittest.main()
